---
name: rivo-layout-variations
description: Sets up an A/B test of the Rivo loyalty app's account widget with ABConvert - the slide-out account, rewards or loyalty panel customers open from the store (Rivo opens it at #rivo). Use when a merchant wants to test different buttons, texts, sections, colors or layout in that customer account or rewards drawer, even if they never say "Rivo widget". Each test group changes Rivo's own settings, so nothing flickers and a winner copies straight into Rivo's admin. Not for Rivo's floating loyalty launcher panel, Rivo's loyalty landing page, Rivo checkout blocks, or Shopify's own customer account pages.
---

# Rivo layout variations

Rivo's account widget has one configuration per store. To test several, each ABConvert test group
changes Rivo's settings in the shopper's browser right before Rivo draws the widget, and Rivo draws that
version itself.

**Only use the templates in `references/scripts.md`: a test group's custom script and custom CSS.**
Never edit the widget's elements with Visual Editor element changes. Rivo draws the widget after the
page loads, so element changes flash Rivo's original first, land on the wrong element once a group
turns a button off, freeze live values such as the points balance, and cannot be copied back to Rivo.

References:
- `references/rivo-settings.md`: what a test group can change, and in which store.
- `references/scripts.md`: the code to paste, and the checks to run.
- `references/how-it-works.md`: why it works; read it when a check fails or after a Rivo update.

The tools named below are the ABConvert MCP's Visual Editor tools (`editor_open`, `editor_edit`,
`editor_list_changes`). Use the ABConvert connection signed in to the merchant's store; if there is
none, the merchant connects it first (https://docs.abconvert.io/mcp/quickstart). The checks in
`scripts.md` run on a storefront page: use a browser tool that can run page JavaScript, or ask the
merchant to paste them into their browser's console and send back the output.

## Workflow

1. **Check the store.** On any storefront page, run "Read the store's Rivo setup" (`scripts.md`,
   section 1). Stop and tell the merchant if:
   - Rivo is missing: Rivo's app embed is off.
   - `waysToOpen` is 0 and the theme's account icon opens Shopify's own account menu for a signed-in
     customer. Then nothing opens Rivo's widget and the test would reach almost no one: ask the
     merchant to add a link to `#rivo` (a menu item or button) first.
   - A Rivo program the change relies on is off (for example "Redeem my points" while the points
     program is off), or `rivoHooksSet` lists a hook that changes the widget.
   The output is Control: the store's widget as it is today.

2. **Agree each test group** with the merchant as a list of Rivo settings and texts from
   `rivo-settings.md`. Keep Control as Rivo's live widget unless the merchant asks otherwise. For a key
   not in the catalog, run "Keys Rivo reads" there first. If the merchant asks for something with no
   Rivo setting (a shape, the order of Rivo's own blocks), say so, and say how it would be tested (CSS)
   and that a winner then needs doing by hand in Rivo.

3. **Create the test** with `editor_open` (`page_url: "/"`, a `test_name`): a Visual Editor draft with
   Control and Variant A. Leave page targeting empty: the widget opens on every page, and a test group's
   custom code runs on every page the test runs on. Run one Rivo widget test at a time on a store: if
   another is in Preview or running, a shopper in a variant of both gets only the first one's layout,
   silently. List the store's tests first, and end the other one or put both in a mutually exclusive
   group. Open the returned `editor_url` in a browser the
   merchant can see. The editor link uses the address's `#` for its own key, so the widget starts
   closed: add `#rivo` to the address. Signed-in views need a customer signed in on that tab; the
   merchant signs in, never you.

4. **Write each variant** with `editor_edit` on that group's `group_index`:
   - `target: {"group": "customJS"}`, `set: {"part": {"id": "rivo-layout", "code": …}}`: the layout
     part (`scripts.md`, section 2) with this group's `SETTINGS`, `TEXTS` and optional `SECTIONS`
     filled in. Replace every REPLACE value; leave nothing from the example.
   - `target: {"group": "customCSS"}`, `set: {"css": …}`: the anti-flicker guard (section 4), then any
     look rules (section 5). The guard and the layout part only work as a pair.

5. **Add the widget-open event to every test group, Control included**: part `rivo-widget-opened`
   (section 6). The test counts every visitor to any page as exposed, including the many who never open
   the widget; this event lets results be filtered to those who did. The event must exist in ABConvert
   as a **custom** event named exactly `Rivo widget opened`, which gives it the ID `rivo_widget_opened`.
   The MCP cannot create it: ask the merchant to create it under Custom Events before launch.

6. **Verify** each group with "Verify a test group" (section 7), in a browser tab that is in front.
   For a draft, the editor tab shows each group (switch with the group picker at the bottom left, then
   add `#rivo` again, since switching reloads the page). For a test in Preview, use the force link in
   section 7.

7. **Tell the merchant** what shoppers see in each test group, in plain words, and what they must do
   themselves (step 1 and step 5). On the preview link, the widget's dimmed backdrop covers the
   ABConvert Preview panel: close the widget before switching test groups there.

8. **After launch**: in the test's results, open **Manage custom metrics** and add "Rivo widget opened"
   (offered only once the test has a start date, for an event created before it). Then filter results
   to visitors who triggered it, or call `get_experiment_results` with
   `customEventRuleId: "rivo_widget_opened"` and `customEventSegment: "include"`. A test in Draft or
   Preview has no results.

9. **Winner**: read the winning group's `SETTINGS`, `TEXTS` and `SECTIONS` out as Rivo admin changes
   ("Home CTA 3: on, text 'Shop best sellers', link /collections/all"). Look rules that override a
   `--rivo-aw-*` variable name their Rivo setting; other CSS goes into Rivo's custom CSS by hand or stays
   running in ABConvert.
