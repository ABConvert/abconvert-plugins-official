# ShopifyQL: docs, queries, and running them

## Official documentation

Shopify documents every dataset, field, and clause. Read the official page for anything the queries below don't cover; never guess a field name. Append `.md` to any shopify.dev URL for the page as plain markdown, with the API version in its frontmatter. If a query below and the docs disagree, the docs win.

| What | Official page |
|---|---|
| Syntax overview | https://shopify.dev/docs/api/shopifyql/latest/syntax.md |
| FROM and SHOW | https://shopify.dev/docs/api/shopifyql/latest/syntax/from-and-show.md |
| WHERE | https://shopify.dev/docs/api/shopifyql/latest/syntax/where.md |
| GROUP BY | https://shopify.dev/docs/api/shopifyql/latest/syntax/group-by.md |
| TIMESERIES | https://shopify.dev/docs/api/shopifyql/latest/syntax/timeseries.md |
| SINCE, UNTIL, DURING | https://shopify.dev/docs/api/shopifyql/latest/syntax/since-until-during.md |
| ORDER BY, LIMIT, HAVING | https://shopify.dev/docs/api/shopifyql/latest/syntax/order-by.md, .../limit.md, .../having.md |
| All datasets | https://shopify.dev/docs/api/shopifyql/latest/schemas.md |
| `sales` | https://shopify.dev/docs/api/shopifyql/latest/schemas/sales_revenue/sales.md |
| `discounts` | https://shopify.dev/docs/api/shopifyql/latest/schemas/sales_revenue/discounts.md |
| `sessions` | https://shopify.dev/docs/api/shopifyql/latest/schemas/sessions_and_behavior/sessions.md |
| `web_performance` | https://shopify.dev/docs/api/shopifyql/latest/schemas/sessions_and_behavior/web_performance.md |

Note `sessions` uses `referrer_*` and `sales` uses `referring_channel` / `order_referrer_*`; they are different taxonomies, so never join them by value.

## Query pack

These ran cleanly on a real store. Dates are placeholders; `UNTIL` is exclusive.

**Baseline (step 2)**

```
FROM sales
  SHOW total_sales, net_sales, orders, average_order_value, orders_first_time, orders_returning
  TIMESERIES day SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC
```

```
FROM sessions
  SHOW sessions, online_store_visitors, pageviews, bounce_rate,
       sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate
  WHERE human_or_bot_session = 'human'
  TIMESERIES day SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC
```

For a conversion-rate claim, also run the `sessions` query without the `WHERE`, and:

```
FROM sessions
  SHOW sessions, bounce_rate, sessions_with_cart_additions, sessions_that_completed_checkout
  WHERE human_or_bot_session = 'human'
  GROUP BY day, referrer_source SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC LIMIT 3000
```

**The hour (step 3).** Rows come back in UTC; shift to store-local before binning.

```
FROM sessions
  SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout
  WHERE human_or_bot_session = 'human'
  TIMESERIES hour SINCE 2026-09-09 UNTIL 2026-09-13 ORDER BY hour ASC
```

**Segments (step 4).** Swap the dimension for `session_device_type`, `session_country`, `landing_page_path`, or `utm_campaign`. Always add `LIMIT`.

```
FROM sessions
  SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout
  WHERE human_or_bot_session = 'human'
  GROUP BY day, referrer_source SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC LIMIT 3000
```

```
FROM sales
  SHOW orders, total_sales, average_order_value
  GROUP BY day, sales_channel SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC LIMIT 3000
```

**Mechanism (step 5)**

```
FROM web_performance
  SHOW page_loads, lcp_p75_ms, fcp_p75_ms, ttfb_p75_ms, p75_cls, inp_p75_ms
  TIMESERIES day SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC
```

```
FROM web_performance
  SHOW page_loads, lcp_p50_ms, lcp_p75_ms, lcp_p90_ms, fcp_p75_ms, ttfb_p75_ms, p75_cls
  WHERE page_path = '/products/<handle>'
  GROUP BY day, device_type SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC LIMIT 3000
```

```
FROM sales
  SHOW orders, gross_sales, discounts, net_sales, average_order_value
  TIMESERIES day SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC
```

```
FROM sales
  SHOW orders, net_sales, average_order_value
  WHERE product_id = '<numeric id>'
  TIMESERIES day SINCE 2026-08-01 UNTIL 2026-09-17 ORDER BY day ASC
```

## Running queries

All three paths read production analytics; get the user's go-ahead before the first query. Copy raw rows into the report's `DATA`; never retype numbers.

**1. A Shopify MCP is connected.** Use its analytics query tool (Shopify's own connector calls it `run-analytics-query`); switch store first if several are connected. An agency's collaborator account needs only the Reports and Dashboards permissions.

**2. An access token**, only through `scripts/shopifyql.py` (standard library, any python3). Ask the merchant for a custom app with the `read_reports` scope and nothing else. `--check` prints the scopes, `--shop` prints name, timezone, and currency, `--csv` prints CSV.

```
SHOPIFY_STORE=example.myshopify.com python3 scripts/shopifyql.py --check
SHOPIFY_STORE=example.myshopify.com python3 scripts/shopifyql.py "FROM sales SHOW orders TIMESERIES day SINCE -60d UNTIL today ORDER BY day ASC"
```

Read-only is enforced, not promised. The token carries no `write_*` scope, so Shopify rejects writes from it. The script sends three fixed query documents (scopes, shop info, `shopifyqlQuery`) with the ShopifyQL string as a variable, and exits before querying if the token has any write scope. Never write a `curl` or `fetch` against `/admin/api/` yourself. In Claude Code the plugin also ships a hook that blocks any shell command carrying a mutation to an Admin API.

*Passing the token* so it never touches the chat, in order of preference:

1. The merchant grants the agency's collaborator account "Develop apps", so the agency creates the read-only app itself and the token never travels. Otherwise the merchant shares it through a password manager, never email or chat.
2. Set `SHOPIFY_ACCESS_TOKEN_CMD` to a lookup that prints it, such as `op read 'op://Clients/Acme/shopify-token'` or `security find-generic-password -s shopify-token -w`. The script runs it; the transcript shows the lookup, never the value.
3. `export SHOPIFY_ACCESS_TOKEN=...` in your own terminal, then start the agent from that shell.

Never paste it into the conversation, a repo, or a settings file, and never `echo` it. ChatGPT has no shell and no outbound network, so this path does not apply there.

**3. Manual export.** The merchant opens Shopify Analytics, Reports, New exploration, ShopifyQL, pastes a query, and exports the CSV. Send the queries with dates filled in, in method order, one CSV each, with the file names you want. Confirm the export's hour rows against one hour in the admin's Sessions report before trusting the timezone.
