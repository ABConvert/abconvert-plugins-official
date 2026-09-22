#!/usr/bin/env bash
# PreToolUse hook: refuse any shell command that sends a GraphQL mutation to a
# Shopify Admin API. The insight-report skill only ever reads, so a mutation in
# a shell command is a mistake by construction. Exit 2 blocks the call and
# returns the message to Claude.
set -u
input=$(cat)
cmd=$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null || true)
[ -z "$cmd" ] && exit 0
if printf '%s' "$cmd" | grep -qiE '(/admin/api/|myshopify\.com|X-Shopify-Access-Token)' \
   && printf '%s' "$cmd" | grep -qE '(^|[^A-Za-z_])mutation([^A-Za-z_]|$)'; then
  echo "Blocked: this command sends a GraphQL mutation to a Shopify Admin API. The shopify-insight-report skill is read-only; run ShopifyQL through scripts/shopifyql.py instead." >&2
  exit 2
fi
exit 0
