# How the method works

Background for debugging and for maintaining the templates. An agent setting up a test only needs
SKILL.md and the templates; read this when a check fails or Rivo has changed.

## Contents

- Rivo's widget in the browser
- The three stores and what writing them does
- Timing: why the layout part runs at the right moment
- Flicker and the anti-flicker guard
- The safety net
- Languages
- Rivo's own JavaScript hooks
- After a Rivo update

## Rivo's widget in the browser

- The account widget is plain page markup (no iframe, no shadow root), driven by Rivo's own copy of
  Alpine.js, `window.RivoProfileAlpine`, with directives named `rivo-ax-*`. Root
  `#rivo-account-slideout`; home view `#rivo-tabpanel-rivo`; contents `.rivo-slideout__content`.
- Rivo's widget script (`ba_rivo_profile.js`) loads `async defer`. At its end it starts Alpine, which
  fires `alpine:init` on `document` (bubbling), draws, then fires `alpine:initialized`.
- Views are hash routes: `#rivo` (home), `#rivo-orders`, `#rivo-profile`, `#rivo-transactions`,
  `#rivo-preferences`, `#rivo-shipping-addresses`, `#rivo-vip-tier--<id>` and others.
- The widget opens from links whose address contains `#rivo`. With `replace_account_links` on, Rivo
  rewrites the page's `/account` links to `#rivo` (done by `ba_loy_init.js`). A theme account icon
  that is a button, not a link, opens Shopify's own account menu instead. Rivo's floating loyalty
  launcher (`loy_config.floating_widget_settings`, `#ba-loy-container`) belongs to a different Rivo
  panel, an iframe, and does not open the account widget.
- Rivo's own `rivo-accounts:widget:open` event fires only from its open method, not when the widget
  opens from the address, so the widget-open part watches the widget's `is-open` class and
  `aria-hidden` instead.

## The three stores and what writing them does

Rivo fills these inside its own `alpine:init` listener on `document`:

| Store | What it is | Writing it |
|---|---|---|
| `rivo_aw_settings` | The very object `window.Rivo.loy_config.account_widget_settings` | Changes `window.Rivo` too. A read of `window.Rivo` afterwards shows the test group's values; the layout part keeps the originals in `window.__abcRivoOriginal` for the setup check. |
| `rivo_aw_translation` | A fresh merge: English texts, then the page language's texts on top | Affects this page only; `window.Rivo` keeps the originals. |
| `loy_config` | A copy of `window.Rivo.loy_config` | `account_widget_sections` here is what Rivo draws custom sections from. |

Some texts live in the settings store, not the texts store (for example `order_limited_time_button_text`,
`home_button_membership_cta_text`, `province_text`); writing them to the other store does nothing. The
catalog's Store column says which.

A key only changes the widget if Rivo reads it after the layout part has written it:
- Read by the widget markup (`rivo-ax-*` attributes, including inside `<template>`): yes.
- Read by Rivo's script while the shopper uses the widget (product cards, address forms, toasts, VIP
  progress): yes.
- Read once while Rivo starts, before or inside its own `alpine:init` listener: no. Known ones:
  `onload_javascript`, `locale_urls_enabled`, `replace_account_links`, `replace_legacy_app_links`.
- Turned into CSS when the page loads (shapes, placement, colors, font sizes,
  `home_cta_N_primary_button`): no as a setting. Colors and font sizes have `--rivo-aw-*` CSS
  variables a test group can override instead (catalog, "Look").

## Timing: why the layout part runs at the right moment

The test group's script runs when ABConvert assigns the group, early in the page and in practice before
Rivo starts (on the reference store Rivo started about 0.3 s in; it varies by store because Rivo's
script is async). The layout part registers an `alpine:init` listener on `window`:

1. Alpine fires `alpine:init` on `document`. Every `document` listener runs first, whatever order they
   were added in, so Rivo's own listener fills the stores.
2. The event bubbles to `window`; the layout part writes this group's values.
3. Alpine draws only after every `alpine:init` listener has returned, so the first draw is the variant.

Verified in Rivo's code: `document.addEventListener("alpine:init", …)`, and Alpine dispatches the event
with `bubbles: true`.

Writing the stores later updates the values but does not redraw what Rivo drew from them (a section
behind a `<template rivo-ax-if>` stays as drawn). That is why the late path sets each on/off switch to
its opposite first and then to the wanted value: the change forces Rivo to redraw those parts.

## Flicker and the anti-flicker guard

Rivo's widget is not in the page's HTML; Rivo builds it in the browser. When the layout part runs on
time there is no original to flash. The guard (custom CSS + `reveal()` in the layout part) hides the
widget's contents until the values are in, so a late run shows a short blank rather than Rivo's
original followed by a redraw. A CSS animation shows the contents after 1.5 s even if the script never
runs. The guard arrives with the test group, like the script, so it cannot cover the moment before
ABConvert assigns the group: if assignment ever came after Rivo drew (an audience filter waiting for
the shopper's country, for example), Rivo's original could show briefly first.

ABConvert's own anti-flicker hides elements that have Visual Editor page changes. These tests have
none, so it plays no part.

## The safety net

If the normal path does not apply (Rivo moves its listener to `window`, stops the event bubbling, or
stops using the Alpine events), the layout part applies on `alpine:initialized` or, at the latest, on
page load, through the redraw path and behind the guard. Tested against a simulated Rivo for each case:
every case ends on the variant, never silently on Control. On a shopper's page `after-draw` therefore
means Rivo changed how it starts; in the editor tab `after-draw` is normal (the script runs after Rivo).

## Languages

Rivo builds the texts store from English plus the page language: the locale Rivo stored, else the
page's locale, matched exactly or by its first part (`fr` for `fr-CA`), with the language from the
address when `locale_urls_enabled` is on. The layout part's `TEXTS` follows the same order (exact,
first part, English). For stores with several languages, give each language the merchant cares about
its own entry; a language with no entry gets the English texts.

## Rivo's own JavaScript hooks

A merchant can set `onload_javascript`, `on_hash_change_javascript`, `post_sign_in_javascript`,
`refresh_cart_javascript` and `variant_id_javascript` in Rivo. They run in every test group. If one
changes the widget, it can undo or fight a test group's values: read them in the setup check before
promising a variant.

## After a Rivo update

Everything here relies on Rivo internals Rivo does not document: `RivoProfileAlpine`, the store names,
the `alpine:init` order, the `rivo-ax-*` attributes and `.rivo-slideout__content`. After a Rivo update,
re-run the verify check on a live test and the "Keys Rivo reads" snippet, and read Rivo's
`alpine:init` listener again if the layout part reports `after-draw` on a shopper's page.
