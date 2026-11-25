# What a test group can change in Rivo's account widget

Store: **S** = put it in `SETTINGS`, **T** = put it in `TEXTS` (per language). A key in the wrong store
changes nothing. The tables cover what merchants usually test; the "Keys Rivo reads" snippet at the end
lists every key on the merchant's own store with its store and current value. Run it before promising a
key that is not listed here.

## Contents

- Home view
- Signed-out view (sign-in)
- Orders view
- Profile, preferences and addresses
- Rewards, VIP and referrals
- Product cards and favorites
- Messages (toasts)
- Look: colors and font sizes
- Custom sections (add or place content)
- Not changeable by a test group
- Keys Rivo reads (snippet)

## Home view

| Key | Store | What it does |
|---|---|---|
| `home_cta_1_enabled`, `home_cta_2_enabled`, `home_cta_3_enabled` | S | Show home button 1, 2, 3 |
| `home_cta_N_url` | S | Where button N links: a path (`/collections/all`) or a widget view (`#rivo-orders`) |
| `home_cta_N_text` | T | Button label |
| `home_additional_button_1_enabled`, `_2_enabled`, `_url` | S | Two more home buttons |
| `home_additional_button_1_text`, `_2_text` | T | Their labels |
| `home_loyalty_button_enabled` | S | Points balance button |
| `home_button_balance_points_text`, `home_button_balance_points_cta_text` | T | Its label and link text |
| `home_membership_button_enabled`, `home_button_membership_url` | S | Membership button |
| `home_button_membership_cta_text`, `home_button_membership_paywall_cta_text` | S | Membership button texts (settings store) |
| `home_gift_card_button_enabled` | S | Store credit button |
| `home_button_gift_card_cta_text`, `home_button_membership_text` | T | Store credit texts |
| `home_logged_out_title`, `home_logged_out_subtitle` | T | Signed-out home heading and line under it |
| `home_logged_in_title`, `home_logged_in_subtitle` | T | Signed-in greeting and points line. They hold `<span rivo-ax-…>` parts for the name and live balance: change the words around them and keep each span exactly. |
| `home_expiration_message_enabled` | S | Points or credit expiry line |
| `home_expiration_message_text` | T | Its text |
| `recently_viewed_enabled`, `recently_viewed_collections_enabled` | S | Recently viewed products, collections |
| `recently_viewed_title` | T | Its heading |
| `popular_today_enabled` | S | Popular Today products |
| `popular_today_title` | T | Its heading |
| `featured_home_content_enabled`, `featured_content_image_url`, `featured_content_link` | S | Featured content card |
| `featured_content_title`, `featured_content_subtitle` | T | Its texts |
| `drops_block_enabled` | S | Expiring drop credits block |
| `community_enabled`, `community_cta_url` | S | Community block |
| `footer_icons_enabled` | S | Icons in the bottom tab bar |
| `footer_home_text`, `footer_orders_text`, `footer_profile_text` | T | Tab bar labels |

## Signed-out view (sign-in)

| Key | Store | What it does |
|---|---|---|
| `shop_pay_login_button_enabled` | S | Sign in with Shop button |
| `google_login_enabled`, `external_login_enabled`, `external_login_url`, `alternate_login_enabled` | S | Other sign-in methods |
| `login_accepts_marketing_enabled`, `loyalty_opt_in_checkbox_enabled`, `accepts_sms_marketing_enabled` | S | Opt-in checkboxes |
| `loyalty_opt_in_checkbox_text` | S | Loyalty opt-in label (settings store) |
| `login_button_text`, `login_accepts_marketing_text`, `login_footer_text`, `accepts_sms_marketing_text`, `shop_pay_login_text` | T | Sign-in form words |
| `home_logged_out_orders_title`, `home_logged_out_profile_title`, `home_logged_out_favorites_title` (and `_subtitle`) | T | What signed-out shoppers see on Orders, Profile, Favorites |

## Orders view

| Key | Store | What it does |
|---|---|---|
| `order_track_shipment_enabled`, `order_tracking_partner`, `order_tracking_custom_link` | S | Track shipment button and where it goes |
| `order_buy_again_enabled` | S | Buy again button |
| `order_returns_enabled`, `order_returns_partner`, `order_returns_custom_link`, `order_returns_fulfilled_only` | S | Start a return button |
| `order_cancel_button_enabled`, `order_cancel_button_threshold_in_minutes` | S | Cancel order button and its time window |
| `order_limited_time_button_enabled`, `_url`, `_threshold_in_minutes`, `order_limited_time_button_text` | S | Time-limited button after an order (its text is in the settings store) |
| `orders_additional_button_enabled`, `_url`; `orders_secondary_additional_button_enabled`, `_url` | S | Extra buttons |
| `order_tracking_button_text`, `order_buy_again_button_text`, `order_returns_button_text`, `order_cancel_button_text`, `orders_additional_button_text`, `orders_logged_in_title`, `orders_empty_state_text` | T | Orders texts |

## Profile, preferences and addresses

| Key | Store | What it does |
|---|---|---|
| `profile_pos_qr_enabled` | S | In-store sign-in QR code |
| `profile_pos_qr_title`, `profile_pos_qr_subtitle` | T | Its texts |
| `profile_list_links` | T | Extra links listed on Profile (a list) |
| `my_preferences_text`, `my_addresses_text`, `profile_log_out_text`, `update_profile_text`, `shipping_addresses_title` | T | Profile texts |
| `province_text`, `select_province_text` | S | Address form labels (settings store) |

## Rewards, VIP and referrals

These show only when the matching Rivo program is on (setup check, `programs`).

| Key | Store | What it does |
|---|---|---|
| `redeem_rewards_block_enabled`, `redeem_rewards_display_style` (`horizontal`, `vertical`), `redeem_rewards_filter` | S | Rewards carousel on home |
| `redeem_rewards_title`, `redeem_rewards_url_text`, `redeem_rewards_unlock_text`, `redeem_rewards_points_away_text` | T | Its texts |
| `vip_progress_block_enabled`, `vip_progress_block_show_highest_tier`, `vip_tier_progress_url` | S | VIP tier progress block |
| `vip_tier_progress_title`, `vip_tier_progress_subtitle`, `vip_tier_progress_link_text` | T | Its texts (they hold live `<span rivo-ax-…>` parts) |
| `home_referral_enabled`, `home_referral_url` | S | Refer a friend block |
| `home_referral_title`, `home_referral_subtitle`, `home_referral_page_subtitle` | T | Its texts |
| `ways_to_earn_title`, `ways_to_earn_transactions_url_text` | T | Ways to earn texts |

## Product cards and favorites

| Key | Store | What it does |
|---|---|---|
| `view_product_action_button_enabled`, `mini_block_product_title_enabled`, `mini_block_product_price_enabled`, `product_compare_at_price_enabled`, `hide_sold_out_products` | S | What product cards show |
| `favorites_enabled`, `saved_cart_enabled`, `share_favorite_collections_enabled` | S | Favorites and Saved from cart |
| `add_to_cart_text`, `view_product_action_button_text`, `favorites_title`, `saved_cart_title`, `sold_out_text` | T | Their texts |

## Messages (toasts)

`add_to_cart_notification_text`, `profile_updated_notification_text`, `address_saved_notification_text`
and the other `*_notification_text` keys: several exist in both stores. Set the same text in both
`SETTINGS` and `TEXTS`, and check it in the widget.

## Look: colors and font sizes

Override the variable in the group's custom CSS (`scripts.md`, section 5). The winner is the setting.

| Variable | Rivo setting |
|---|---|
| `--rivo-aw-background-color` | `slideout_background_color` |
| `--rivo-aw-primary-color` | `primary_color` |
| `--rivo-aw-heading-font-color`, `--rivo-aw-body-primary-font-color`, `--rivo-aw-body-secondary-font-color` | `slideout_heading_font_color`, `slideout_body_primary_font_color`, `slideout_body_secondary_font_color` |
| `--rivo-aw-border-color`, `--rivo-aw-subdued-color`, `--rivo-aw-icon-color` | `slideout_border_color`, `slideout_subdued_color`, `slideout_icon_color` |
| `--rivo-aw-favorite-button-active-color`, `--rivo-aw-compare-at-price-color` | `favorite_button_active_color`, `compare_at_price_color` |
| `--rivo-aw-toast-background-color`, `--rivo-aw-toast-font-color` | `toast_background_color`, `toast_font_color` |
| `--rivo-aw-default-font-size`, `--rivo-aw-input-font-size`, `--rivo-aw-section-title-font-size`, `--rivo-aw-logged-out-title-font-size` | `default_font_size`, `input_font_size`, `section_title_font_size`, `logged_out_title_font_size` |
| `--rivo-aw-mini-block-title-font-size`, `--rivo-aw-mini-block-subtitle-font-size`, `--rivo-aw-footer-font-size`, `--rivo-aw-login-footer-font-size` | `mini_block_title_font_size`, `mini_block_subtitle_font_size`, `footer_font_size`, `login_footer_font_size` |
| `--rivo-aw-home-featured-content-image-position` | `featured_content_image_position` |
| `--rivo-aw-desktop-sidebar-left`, `-right`, `--rivo-aw-desktop-slidein-translate-x`, `--rivo-aw-desktop-slideout-translate-x` | `desktop_placement` (left or right): change all four together |

All buttons at once: `primary_button_class_names` and `secondary_button_class_names` (S) set the class
every primary or secondary button gets. One button only: CSS by its setting (`scripts.md`, section 5).

## Custom sections (add or place content)

Rivo's own way to add HTML to the widget, and the only way to add or move content with a Rivo
equivalent. A group adds sections with the layout part's `SECTIONS`; the merchant's existing sections
stay. Fields:

| Field | Meaning |
|---|---|
| `id` | Unique; the section is drawn as `#rivo-custom-section-<id>` |
| `enabled` | `true` to show |
| `position_selector` | CSS selector of the widget element to place it at, e.g. `#rivo-tabpanel-rivo .rivo-aw-home-button-list` |
| `position_type` | `append`, `prepend`, `insert_before`, `insert_after`, or `replace` (hides the target while shown) |
| `position` | Order among sections at the same place (lower first) |
| `html`, `css`, `js` | Content; `js` runs with the section's element as `container` |
| `visible_when` | `always`, `logged_in`, `logged_out` |
| `visible_on_hashes` | Views to show it on, e.g. `["#rivo"]` (`*` allowed); empty = every view |
| `visible_tags` | Customer tags that may see it; empty = everyone |

Rivo draws sections on each view change, and on the first view when the layout part runs on time
(verified). A winner is re-created as a custom section in Rivo's admin. Sections add content; they do
not move Rivo's own blocks (`replace` hides the target block while the section shows). Rivo has no
setting for the order of its own blocks: say so before promising a reorder.

## Not changeable by a test group

- Shapes and placement as settings (`buttons_shape`, `cards_shape`, `container_shape`, `inputs_shape`,
  `launcher_shape`, `desktop_sidebar_position`), and `home_cta_N_primary_button` (filled or outlined):
  turned into CSS when the page loads. Use section "Look" or one-element CSS instead.
- Read once while Rivo starts: `onload_javascript`, `locale_urls_enabled`, `replace_account_links`,
  `replace_legacy_app_links`, `enabled`.
- `custom_css`, `css_variables`: Rivo's own stylesheet; use the group's custom CSS.
- Anything in Rivo's floating loyalty panel (`floating_widget_settings`, an iframe) or Rivo's loyalty
  landing page: a different Rivo surface.

## Keys Rivo reads

Run on a storefront page with no test group forced. Lists every key Rivo's widget reads, in its markup
or its script, with the store, the current value, and where it is read. Keys read only at start-up
(section "Not changeable") appear too: leave them out.

```js
(async () => {
  const keys = new Map();
  const add = (store, key, where) => {
    const id = (store === 'settings' ? 'S ' : 'T ') + key;
    const prev = keys.get(id);
    keys.set(id, prev && prev !== where ? 'markup+script' : where);
  };
  const RE = /rivo_aw_(settings|translation)["')\]]*\??\.([a-z0-9_]+)/g;
  const scan = (text, where) => {
    for (const m of text.matchAll(RE)) add(m[1], m[2], where);
    for (const m of text.matchAll(/awSettings\??\.([a-z0-9_]+)/g)) add('settings', m[1], where);
  };
  const walk = node => node.querySelectorAll('*').forEach(el => {
    for (const a of el.attributes) scan(a.value, 'markup');
    if (el.tagName === 'TEMPLATE') walk(el.content);
  });
  const root = document.getElementById('rivo-account-slideout');
  if (!root) return 'Rivo account widget is not on this page';
  walk(root);
  const script = [...document.scripts].find(s => /ba_rivo_profile/.test(s.src));
  if (script) scan(await fetch(script.src).then(r => r.text()), 'script');
  const s = window.Rivo.loy_config.account_widget_settings;
  const t = window.RivoProfileAlpine.store('rivo_aw_translation');
  return [...keys].sort().map(([id, where]) => {
    const [store, key] = id.split(' ');
    const value = store === 'S' ? s[key] : t[key];
    return `${id} = ${JSON.stringify(value)?.slice(0, 60)} (${where})`;
  }).join('\n');
})();
```

A key read only in the script is read when the shopper uses that part of the widget (a product card,
a form, a message), which is after the layout part runs. Keys a store does not have print `undefined`.
