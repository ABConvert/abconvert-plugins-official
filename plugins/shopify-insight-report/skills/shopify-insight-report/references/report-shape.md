# Report shape

The reader is the merchant, or the CS teammate forwarding it to the merchant. They read the top three tiles and maybe one chart. Everything below the tiles is there so the conclusion survives a skeptical re-check, not to be read in order.

`assets/report-template.html` is the starting point: the CSS, the `chart()` helper, the timeline strip, and the three standard exhibits with every store-specific string as a `{{PLACEHOLDER}}`. Fill `DATA`, `WINDOW`, `BASELINE_UNTIL`, `EVENTS`, and `TIMELINE`.

## Structure

```
h1: <Store> <what happened>                  "Acme Outdoors sales drop"

Verdict: three tiles
  Conclusion 1  The suspect didn't affect <metric>        + the 2-3 numbers that carry it
  Conclusion 2  The suspect didn't affect <its mechanism>  + numbers
  Conclusion 3  <What actually happened>. <Action>         + numbers
  (no suspect: 1 = what moved and what didn't, 2 = which step and segment,
   3 = the hour + "check what changed then")

Timeline (SVG): suspect started / break the data found / suspect ended, store-local times,
  one line of context each ("Facebook visitors only", "ratio falls from 1.0 to 0.3")

Exhibit, one per question, in the order the reader needs them:
  h2 question-as-title                        "Orders and sales per day, Aug 1 to Sep 16"
  chip: source dataset                        "Shopify · sales"
  sub: one sentence saying what the chart shows and where to look
  grid:
    panel: legend + chart(s), suspect window shaded, event markers on every chart
    aside:
      Fact            numbers only, no adjectives
      Interpretation  what the numbers mean for the question
      What to check   (optional) the merchant's next action
      qbox            the ShopifyQL that produced the chart, with Copy

Footer
  Source and how to check   timezone, pull time, partial day, dataset lag, hourly UTC shift
  Definitions               every field name used, and any ratio that can look wrong
```

Exhibit order for a "did X do this" report: the headline metric first (sales), then the exoneration (the suspect's mechanism, page speed for anything that touched the theme), then the observation (funnel step that broke), then the localization (hour), then segments if they add attribution. With no suspect, drop the exoneration exhibit and put the segment cut that attributes the break in its place. The example ran the channel and device queries (they are in its `QUERIES`) but published no segment exhibit: the test targeted Facebook visitors only, while the funnel break was storewide, and the timeline carries that contrast.

## Writing

Ranked. When two rules pull in different directions, the higher one wins.

1. **Every statement comes from the data.** A sentence goes in only if it traces to rows the query beside it returned. That covers causes as much as counts: "the checkout changed" is a finding only when a checkout metric moved. Anything the data cannot show is written under What to check, never as a fact.
2. **Read once, top to bottom.** The merchant reads the tiles, then down the page, and never scrolls back. Explain every term, ratio, and event the first time it appears, before it is used: define "reached checkout over added to cart" in the exhibit that first plots it, not in the footer. A sentence that needs a later section to make sense is in the wrong place.
3. **A chart earns its place by carrying a finding.** Each chart supports one sentence in a tile or a Fact paragraph. A chart that only shows more data pulls attention from the one that matters, so drop it and keep its query in the footer if the merchant may want it. Three or four charts is normal; eight means the argument is not yet clear.
4. **Shopify's words.** Use the names the merchant sees in Shopify Analytics: sessions, orders, conversion rate, added to cart, reached checkout, completed checkout, average order value, online store, sales channel, referrer source, discount. Not "funnel stage", "traffic", or an abbreviation the admin does not show. When a ShopifyQL field must appear, it sits in `mono` next to the plain words.
5. **Short, plain sentences.** One idea per sentence, common words, no adjectives; the numbers carry the weight. A merchant reading on a phone between other tasks should get each sentence on the first pass.

## Tiles

Each tile is one sentence in the `v` slot and two or three sentences of numbers in the `s` slot. The `v` sentence must be true on its own without the numbers. "Cart-to-checkout dropped on Sep 11. Check what changed" is a tile. "Interesting pattern in the checkout funnel" is not.

Three tiles, always. If you have two conclusions, the third is the action. If you have five, the last two are exhibits, not verdicts.

## Fact / Interpretation

**Fact** contains only what the query returned: counts, ranges, dates, ratios. No "sharply", "only", "healthy". Write ranges, not means, where the point is "this is within normal" ("days between 17 and 38 orders").

**Interpretation** is one to three sentences on what the fact means for the question in the tile. It may name a cause class ("something changed between the cart and the checkout") but not a specific culprit unless the data shows it.

**What to check** appears only when the merchant can act. Name the place in their admin ("the store activity log in your Shopify admin settings lists edits by time"), not a Shopify URL that may move.

## Charts

- Bars for counts per day (orders, sales); lines for rates, ratios, and anything compared across series (funnel steps, LCP by device).
- The suspect window is shaded on every daily chart. Event markers are the same colors everywhere: amber for the suspect's start, red dashed for the break the data found, grey for the suspect's end. Other known events (a theme publish, a campaign start) get amber too, labelled.
- One reference line per chart at most: the baseline average, or 1.0 on a ratio chart.
- Hover gives the exact numbers, so axis labels stay sparse.
- Hourly charts bin to 4 hours in store-local time and label only midnights on the axis.
- Do not put two y-axes on one chart. Stack two charts instead (orders above sales in the example).

## Copy rules

- Second person, present tense, sentence case headings. No em dashes.
- Store-local time with the zone named once in the footer. Write "Sep 11, about 10:00 am", never ISO timestamps in prose.
- "test" not "experiment"; "test group" not "variant"; "product variant" for the Shopify catalog object. Bare "variant" means an A/B group.
- Numbers as the merchant sees them in Shopify: `$41,200 USD`, `52 orders`, `1.3 s`. Round to what the decision needs.
- Name Shopify's own field in `mono` when it defines a chart (`sessions_that_reached_checkout`), so the merchant can find it in the ShopifyQL editor. Never expose internals of any tool (collection names, BigQuery tables).
- Never blame a named third-party app or the merchant's team. "Check the store's change history for that morning" is the furthest the report goes.

## Publishing

Before publishing, check that every number in a tile appears in an exhibit's Fact paragraph and comes from the query beside it; that hour rows were shifted to store-local and the footer says by how much; that the current day is labelled partial and excluded from averages; that the timeline and every daily chart carry the same event markers; and that no `{{...}}` placeholder remains.

The page is self-contained HTML with fonts from Google Fonts and nothing else external, so it opens in any browser. In a client with artifacts or pages, publish it there and send the link. Otherwise save it as `report.html` and hand the file over. Title is the h1.
