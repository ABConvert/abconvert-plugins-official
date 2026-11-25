# Rivo layout variation code

Every block here ran on a live store before it was written down. In the layout part change only the
values marked REPLACE; in CSS only the values marked REPLACE. Everything else stays as is.

## Contents

1. Read the store's Rivo setup (read-only)
2. Layout part (one per test group that changes Rivo)
3. Example: a filled layout part
4. Anti-flicker guard (custom CSS, with every layout part)
5. Look: colors, font sizes, one element (custom CSS)
6. Widget-open event part (every test group, Control included)
7. Verify a test group

## 1. Read the store's Rivo setup

Run on a storefront page (a page-script tool or the browser console). Read-only. It shows the store's
own values even in a tab where a test group's layout part ran.

```js
(() => {
  const R = window.Rivo;
  if (!R || !R.loy_config) return { rivo: 'missing: Rivo app embed is off on this theme' };
  const s = { ...(R.loy_config.account_widget_settings || {}) };
  const byLocale = (R.common && R.common.translations && R.common.translations.account_widget) || {};
  const alpine = window.RivoProfileAlpine;
  const locale = String((alpine && alpine.store && alpine.store('locale')) || (window.Shopify && window.Shopify.locale) || 'en').toLowerCase();
  const t = { ...(byLocale.en || {}), ...(byLocale[locale] || byLocale[locale.split('-')[0]] || {}) };
  // A test group's layout part writes its settings into window.Rivo; it keeps the store's originals here.
  const kept = window.__abcRivoOriginal;
  if (kept) { Object.assign(s, kept.settings); Object.assign(t, kept.texts); }
  const visible = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const hooks = ['onload_javascript', 'on_hash_change_javascript', 'post_sign_in_javascript', 'refresh_cart_javascript', 'variant_id_javascript'];
  return {
    testGroupOnThisPage: window.__abcRivoLayout ? `yes (${window.__abcRivoLayout}); values below are the store's own` : 'no',
    // Visible links on the page (not inside the widget) that open it. 0 = shoppers may have no way in.
    waysToOpen: [...document.querySelectorAll('a[href*="#rivo"]')].filter(a => !a.closest('#rivo-account-slideout') && visible(a)).length,
    replaceAccountLinks: s.replace_account_links,
    languages: Object.keys(byLocale),
    homeButtons: [1, 2, 3].map(n => ({ n, on: s[`home_cta_${n}_enabled`], text: t[`home_cta_${n}_text`], url: s[`home_cta_${n}_url`] })),
    switchesOn: Object.keys(s).filter(k => k.endsWith('_enabled') && s[k] === true),
    customSections: (R.loy_config.account_widget_sections || []).map(x => `${x.id}: ${x.enabled ? 'on' : 'off'}, ${x.position_type || 'append'} ${x.position_selector}`),
    rivoHooksSet: hooks.filter(k => s[k]),
    programs: {
      points: R.loy_config.points_program_enabled, vip: R.loy_config.vip_program_enabled,
      referrals: R.loy_config.referral_program_enabled,
      rewards: (R.loy_config.rewards || []).map(r => r.name),
      vipTiers: (R.loy_config.vip_tiers || []).map(v => `${v.name} from ${v.threshold}`),
    },
  };
})();
```

- `waysToOpen: 0`: check by signing in as a customer and clicking the theme's account icon. If it opens
  Shopify's own menu, nothing on the page opens Rivo's widget; the merchant must add a link to `#rivo`
  (a menu item or button) before launch.
- `rivoHooksSet` not empty: read those hooks; one that changes the widget can fight a test group.
- `customSections`: the merchant's own Rivo sections; a test group's `SECTIONS` keeps them.

## 2. Layout part

`editor_edit` on the test group → `target: {"group": "customJS"}`,
`set: {"part": {"id": "rivo-layout", "code": <below, values filled in>}}`.

```js
// Rivo account widget for this test group.
// Each value is a Rivo account widget setting, so a winner copies 1:1 into Rivo's admin.
(function () {
  if (window.__abcRivoLayout) return;
  window.__abcRivoLayout = 'waiting';

  // REPLACE: this test group's values. Keys must be ones Rivo reads, in the store Rivo reads them
  // from (references/rivo-settings.md). Leave an object empty if the group changes nothing there.
  var SETTINGS = {
    // setting_key: value,
  };
  var TEXTS = {
    // Texts per language. 'en' is used when the page's language has no entry.
    en: {
      // text_key: 'Words shoppers see',
    }
  };
  var SECTIONS = [
    // Optional custom sections (references/rivo-settings.md, "Custom sections"), e.g.
    // { id: 'abc-note', enabled: true, position_selector: '#rivo-tabpanel-rivo .rivo-aw-home-button-list',
    //   position_type: 'insert_after', position: 1, visible_when: 'always', html: '<p>...</p>', css: '' },
  ];

  // Anti-flicker: the group's custom CSS hides the widget's contents until this mark is set.
  function reveal() { document.documentElement.setAttribute('data-abc-rivo-ready', ''); }
  setTimeout(reveal, 1500); // whatever happens, never hide the widget longer than this

  function stores() {
    var alpine = window.RivoProfileAlpine;
    if (!alpine || typeof alpine.store !== 'function') return null;
    var settings = alpine.store('rivo_aw_settings');
    var translation = alpine.store('rivo_aw_translation');
    if (!settings || !translation) return null;
    return { alpine: alpine, settings: settings, translation: translation, config: alpine.store('loy_config') };
  }

  // Rivo's own order: the page's language, then its first part ('fr' for 'fr-CA'), then English.
  function texts(alpine) {
    var locale = String(alpine.store('locale') || (window.Shopify && window.Shopify.locale) || 'en').toLowerCase();
    return TEXTS[locale] || TEXTS[locale.split('-')[0]] || TEXTS.en || {};
  }

  // The values this group replaces, as the store had them, for the setup check
  // (Rivo's settings store is window.Rivo's own object, so it shows this group's values afterwards).
  function keepOriginals(s, words) {
    if (window.__abcRivoOriginal) return;
    var original = { settings: {}, texts: {} };
    Object.keys(SETTINGS).forEach(function (key) { original.settings[key] = s.settings[key]; });
    Object.keys(words).forEach(function (key) { original.texts[key] = s.translation[key]; });
    window.__abcRivoOriginal = original;
  }

  function patch(how) {
    var s = stores();
    if (!s) return false;
    var words = texts(s.alpine);
    keepOriginals(s, words);
    Object.assign(s.settings, SETTINGS);
    Object.assign(s.translation, words);
    if (SECTIONS.length && s.config) {
      var ids = SECTIONS.map(function (section) { return section.id; });
      var kept = (s.config.account_widget_sections || []).filter(function (section) { return ids.indexOf(section.id) === -1; });
      s.config.account_widget_sections = kept.concat(SECTIONS);
    }
    window.__abcRivoLayout = how;
    return true;
  }

  // Normal path. Rivo creates its stores in its own alpine:init listener on document and draws
  // right after every alpine:init listener has run. A window listener runs after document
  // listeners (the event bubbles up to window), so the stores exist here and nothing is drawn yet.
  window.addEventListener('alpine:init', function () {
    if (patch('alpine:init')) reveal();
  });

  // Fallback once Rivo has drawn: write each switch through a change so the parts drawn from the
  // old value draw again, then show the widget. Runs at most once, and never after the normal path.
  function repatchDrawn() {
    if (window.__abcRivoLayout !== 'waiting') return true;
    var s = stores();
    if (!s) return false;
    keepOriginals(s, texts(s.alpine));
    window.__abcRivoLayout = 'redrawing';
    Object.keys(SETTINGS).forEach(function (key) {
      if (typeof SETTINGS[key] === 'boolean') s.settings[key] = !SETTINGS[key];
    });
    setTimeout(function () {
      patch('after-draw');
      setTimeout(reveal, 50);
    }, 0);
    return true;
  }

  // This ran after Rivo drew (the editor tab, or a late group assignment).
  if (window.RivoProfileAlpine && document.querySelector('#rivo-tabpanel-rivo [rivo-ax-text]')) {
    document.addEventListener('DOMContentLoaded', repatchDrawn);
    if (document.readyState !== 'loading') repatchDrawn();
  }

  // Safety net: if the normal path did not apply (a Rivo update moved its setup or stopped the
  // event reaching window), apply once Rivo says it has drawn, or at the latest when the page loads.
  document.addEventListener('alpine:initialized', repatchDrawn);
  window.addEventListener('load', repatchDrawn);
})();
```

- Put each key in the store Rivo reads it from: `SETTINGS` for the settings store, `TEXTS` for the
  texts store (catalog, Store column). A key in the wrong store changes nothing.
- `window.__abcRivoLayout` reads `alpine:init` on a shopper's page and `after-draw` in the editor tab.

## 3. Example: a filled layout part

Only the value block differs from the template. This group shows a third home button, the rewards
carousel, hides Popular Today, and renames two texts:

```js
  var SETTINGS = {
    home_cta_3_enabled: true,
    home_cta_3_url: '/collections/all',
    redeem_rewards_block_enabled: true,
    popular_today_enabled: false
  };
  var TEXTS = {
    en: {
      home_cta_1_text: 'Redeem my points',
      home_cta_3_text: 'Shop best sellers'
    }
  };
  var SECTIONS = [];
```

## 4. Anti-flicker guard

Always the start of the custom CSS of a group that has a layout part; the two only work together.
`editor_edit` → `target: {"group": "customCSS"}`, `set: {"css": <guard, then any section 5 rules>}`
(this replaces the group's whole stylesheet).

```css
/* Anti-flicker: the widget's contents stay invisible until this test group's Rivo settings are in
   (the layout part sets data-abc-rivo-ready). The animation shows them after 1.5 s even if the
   script never runs, so the widget can never stay hidden. */
html:not([data-abc-rivo-ready]) #rivo-account-slideout .rivo-slideout__content {
  opacity: 0;
  pointer-events: none;
  animation: abc-rivo-reveal 0s linear 1.5s forwards;
}
@keyframes abc-rivo-reveal { to { opacity: 1; pointer-events: auto; } }
```

Tested in Chromium: marked ready at 300 ms shows at 300 ms; never marked shows at 1.5 s.

## 5. Look: colors, font sizes, one element

Rivo turns its color and font-size settings into `--rivo-aw-*` variables on the page. Override the
variable, and a winner names the exact Rivo setting (catalog, "Look"). Use `html:root`: Rivo's own
`:root` rule loads later in the page and would win over a plain `:root`.

```css
/* Look: Rivo variables for this test group. */
html:root {
  --rivo-aw-primary-color: REPLACE;      /* Rivo setting primary_color */
}
```

For one element no variable covers (a single button), select it by the Rivo setting it shows, never
by position (`:nth-of-type`, `:first-child`), which shifts when a group turns a button or section off.
Home buttons take their look from the theme, so set the theme's button variables too:

```css
/* Home button 1 (Rivo setting home_cta_1) in REPLACE color. */
#rivo-tabpanel-rivo a[rivo-ax-html="$store.rivo_aw_translation.home_cta_1_text"] {
  --button-background-color: REPLACE;
  --button-border-color: REPLACE;
  --button-color: REPLACE;
  background-color: REPLACE !important;
  border-color: REPLACE !important;
  color: REPLACE !important;
}
```

A look that has no Rivo variable or setting has no copy-back: a winner goes into Rivo's custom CSS by
hand, or stays running in ABConvert.

## 6. Widget-open event part

Needs the custom event `Rivo widget opened` (type custom, ID `rivo_widget_opened`) in ABConvert. Add to
every test group, Control included: `editor_edit` → `target: {"group": "customJS"}`,
`set: {"part": {"id": "rivo-widget-opened", "code": <below>}}`.

```js
// Sends the custom event rivo_widget_opened once per page, when Rivo's account widget opens.
// Same part in every test group, so results can be filtered to shoppers who opened the widget.
(function () {
  if (window.__abcRivoOpenWatch) return;
  window.__abcRivoOpenWatch = 'watching';
  function send() {
    if (window.__abcRivoOpenWatch === 'sent') return;
    window.__abcRivoOpenWatch = 'sent';
    if (window.ABConvert && typeof window.ABConvert.track === 'function') window.ABConvert.track('rivo_widget_opened');
    else (window.abconvertQ = window.abconvertQ || []).push(['track', 'rivo_widget_opened']);
  }
  function isOpen(el) {
    return el.classList.contains('is-open') && el.getAttribute('aria-hidden') === 'false';
  }
  function watch() {
    var el = document.getElementById('rivo-account-slideout');
    if (!el) return false;
    if (isOpen(el)) { send(); return true; }
    var observer = new MutationObserver(function () {
      if (!isOpen(el)) return;
      send();
      observer.disconnect();
    });
    observer.observe(el, { attributes: true, attributeFilter: ['class', 'aria-hidden'] });
    return true;
  }
  if (!watch()) document.addEventListener('DOMContentLoaded', watch);
})();
```

`ABConvert.track()` ignores a name with no matching custom event. On a storefront page,
`window.abconvertCustomEventConfig.rules` lists the events the store loaded; `rivo_widget_opened` must
be there.

## 7. Verify a test group

Open `https://<store>/?abconvert_force=<numeric test id>:<group index>#rivo` in a tab that is in front
(a background tab barely redraws and looks broken), wait a few seconds, then run:

```js
(() => {
  const home = document.querySelector('#rivo-tabpanel-rivo');
  const slideout = document.getElementById('rivo-account-slideout');
  return {
    group: window.ABConvert.getAssignments().map(a => `${a.experimentId}: ${a.testGroup.name}`),
    layout: window.__abcRivoLayout || 'no layout part (expected in Control)',
    guardReady: document.documentElement.hasAttribute('data-abc-rivo-ready'),
    replaced: window.__abcRivoOriginal || null,
    openEvent: window.__abcRivoOpenWatch || 'open-event part missing',
    widgetOpen: slideout.classList.contains('is-open'),
    eventLoaded: (window.abconvertCustomEventConfig?.rules || []).some(r => r.ruleId === 'rivo_widget_opened'),
    customSections: [...document.querySelectorAll('#rivo-account-slideout .rivo-custom-section')].map(e => e.id),
    homeButtons: [...home.querySelectorAll('.rivo-aw-home-button-list a')]
      .map(a => [a.textContent.trim(), getComputedStyle(a).backgroundColor]),
    homeText: home.innerText.replace(/\n+/g, ' | ').slice(0, 400),
  };
})();
```

Expect in a variant: `layout: "alpine:init"` (on a shopper's page; `after-draw` there means the safety
net ran because Rivo changed how it starts: see how-it-works.md, "After a Rivo update"),
`guardReady: true`, `replaced` listing the store's own values for what the group changed, the
group's buttons and sections, and `openEvent: "sent"` once the widget is open. In Control: no layout
part, the store's own widget, and `openEvent`. A force link with another group index replaces the
tab's group.
