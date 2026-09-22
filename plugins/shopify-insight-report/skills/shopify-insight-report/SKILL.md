---
name: shopify-insight-report
description: Builds a merchant-facing insight report from a store's own Shopify analytics (ShopifyQL), with the events that might explain a change marked on every chart, and delivers it as an HTML page the merchant can re-run query by query. Use whenever a merchant, prospect, or teammate says conversion, CVR, sales, AOV, orders, or traffic dropped or changed on a Shopify store and they can't say why; whenever someone asks if a specific change (a theme publish, app install, checkout, shipping, payment, price, discount, campaign, migration, or A/B test) hurt the store; and whenever someone wants a trend, anomaly, or "what happened to this store" report, even if they never say "report".
---

# Shopify Insight Report

Answer one merchant question with the merchant's own data: what changed, when, and was it the thing they suspect? Shopify's reports are the source the merchant already trusts, so every number in the report comes from a ShopifyQL query they can paste into Shopify Analytics and re-run.

The method is the same with a suspect ("sales dropped since the theme publish") and without one ("CVR dropped this month and we can't figure out why"). Without a suspect, the data finds the hour first and the merchant names what changed then.

## Principles

1. **Events before metrics.** The report is metric versus events, so list the events first, in store-local time, each with what it touched and who saw it. The merchant's own "since" date is one of those events, and it is a hypothesis to test, not a fact.
2. **The baseline is a range, not a mean.** "Sep 11 to 15 ran 13 to 19 orders; August's lowest days were 17 to 19" is a finding. "Below the August average" is not. Judge a window against the range, never against its own best day.
3. **Find the step, then the day, then the hour.** The funnel step that moved names the class of cause. The hour is what the merchant matches against their store's activity log, and it is what separates "3.5 days after the change" from "when the change was made".
4. **Storewide or one segment.** A break in every channel, device, and country at the same hour is a storewide change. A break in one segment points at whatever reaches only that segment.
5. **A change can only break what it touches.** Check the suspect's own mechanism directly. A flat line there, with the break elsewhere, is the strongest exoneration the report can offer.
6. **Every number is reproducible.** Fact and interpretation are separate paragraphs, and the query that produced each chart sits next to it.
7. **Read only.** Whatever the data path, the skill never changes anything in the store.

## Intake

Ask in one message; proceed with whatever comes back. Only the data path blocks.

1. **The claim, verbatim.** Metric, window, and the implied "it was fine before". All three get checked.
2. **Known events**, with dates and times: theme publish or edit, app installed or removed, checkout or payment settings, shipping rates, discount start or end, price change, product launch or stockout, campaign or spend change, domain or redirect change, Shopify plan or checkout upgrade, A/B test started or paused. "Nothing changed" is an answer worth writing down.
3. **Data path.** A Shopify MCP connected to the store; or a read-only Admin API token used only through `scripts/shopifyql.py`; or CSV exports the merchant makes in the ShopifyQL editor. Each reads production analytics, so get a clear yes first. Details, including how to pass a token without it touching the chat, are in `references/shopifyql.md`.

Timezone comes from the shop info the MCP returns, from `--shop` on the script, or from the merchant. Day rows are store-local; hour rows from the API are UTC. Convert once.

## Method

Queries for every step, and links to Shopify's official pages for any field they don't cover, are in `references/shopifyql.md`. Never guess a field name; run each query with `LIMIT 5` before the full pull.

**1. Timeline.** Every event from intake, store-local, one line of context each.

**2. Baseline.** Daily `sales` and `sessions` for four to eight weeks before the earliest event, through today. For a conversion-rate claim, split the ratio first: sessions up with orders flat is traffic quality (campaign, bots, a viral post) and the investigation moves to sessions by source and landing page; sessions flat with orders down is a funnel problem.

**3. Funnel step, day, hour.** Plot sessions, added to cart, reached checkout, completed checkout, and the step-to-step ratios per day.

| Step that fell | Points at |
|---|---|
| Sessions | Traffic: ads, campaigns, SEO, bot filter, redirects, a change on landing pages |
| Add to cart | Product page, price, stock, reviews or media apps, a change on the product page |
| Reached checkout | Cart page, cart drawer, cart or upsell apps, discount logic, checkout redirect |
| Completed checkout | Checkout settings, payments, shipping rates, taxes, a checkout or shipping change |

Then `TIMESERIES hour` over the break day plus two on each side, binned to 4 hours. A metric that fades over a week instead of stepping on one hour is a different class of cause (seasonality, ad fatigue, a competitor, stock running down); say so.

**4. Segments.** Re-run the funnel by day and `referrer_source`, `session_device_type`, `session_country`, `landing_page_path`, and `sales_channel`. One device points at layout or a script on that device; one channel or landing page at a campaign, redirect, or page change; one country at shipping, payments, market pricing, or a geo block.

**5. The suspect's mechanism.**

| Suspect | Could move | Check |
|---|---|---|
| Theme publish or edit, app install, any injected script (including an A/B test) | Page speed, layout, add-to-cart | `web_performance` storewide and on the touched page by `device_type`; add-to-cart on touched pages |
| Checkout settings, payments, checkout upgrade | Checkout completion | `sessions_that_completed_checkout` by device; orders by `sales_channel` |
| Shipping rates | Checkout completion | `sessions_that_completed_checkout` by country; `shipping_charges` |
| Price change | AOV, add-to-cart | `average_order_value`, `sessions_with_cart_additions`, sales on the changed products |
| Discount start or end | Reached and completed checkout, AOV | `discounts`, `orders`, `average_order_value` around the date |
| Campaign or spend change | Sessions, bounce, the CVR denominator | `sessions` by `referrer_source`, `utm_campaign`, `landing_page_path`; `bounce_rate` |
| Stockout or launch | Add-to-cart on that product | `sales` and the funnel on the product's page |
| Domain or redirect change | Sessions, landing pages | `sessions` by `landing_page_path`, `referrer_source` |

Without a suspect, put the hour in front of the merchant first and run this step on what they name.

**6. Report.** Build from `assets/report-template.html`; structure and writing rules are in `references/report-shape.md`. Three conclusions at the top, a timeline, one exhibit per question with its chart, Fact, Interpretation, and query. Publish as an artifact or page where the client has one, otherwise save `report.html`. It holds a merchant's sales figures: share it with the merchant only, never commit it.

## Traps

- **Hour rows are UTC**, day rows store-local. Shift before binning and say so in the footer.
- **The current day is partial.** Label it; keep it out of averages.
- **`web_performance` lags about two days.** Missing rows, not zeros.
- **`GROUP BY day, <dimension>` needs an explicit `LIMIT`** (3000 is safe for 60 days by channel) or the tail is cut silently.
- **Filter `human_or_bot_session = 'human'`** on every funnel query. For a CVR claim, run it once without, since the admin's number may include what the filter removes.
- **Reached checkout over added to cart can exceed 1** (saved carts, Buy it now, abandoned-checkout emails). Present it as before-and-after, not a rate.
- **`sales` counts every sales channel.** Split by `sales_channel` before comparing with online sessions.
- **Volume sets the resolution.** Twenty orders a day has daily noise of about five: read runs of days, never one. A thousand a day can be read at the hour.
