#!/usr/bin/env python3
"""Run one ShopifyQL query against a store with an Admin API access token.

This is the only sanctioned way to use a token from this skill, and it is
read-only by construction:
  1. It sends only the fixed GraphQL documents below (scopes, shop info, and
     `shopifyqlQuery`). The ShopifyQL string travels as a variable, so nothing
     in it can become a mutation.
  2. Before the first query it reads the token's access scopes and exits if
     any `write_*` scope is present. A token that can write is the wrong
     token for an analytics job, whoever holds it.

Standard library only; runs anywhere python3 runs.

Usage:
  SHOPIFY_STORE=example.myshopify.com SHOPIFY_ACCESS_TOKEN=shpat_... \\
    python3 scripts/shopifyql.py "FROM sales SHOW orders TIMESERIES day SINCE -7d UNTIL today"
  python3 scripts/shopifyql.py --check          # scope check only
  python3 scripts/shopifyql.py --shop           # store name, timezone, currency
  python3 scripts/shopifyql.py --csv "<query>"  # CSV instead of JSON

The token comes from the environment, never from a chat message or a file
in the report: either SHOPIFY_ACCESS_TOKEN, or SHOPIFY_ACCESS_TOKEN_CMD, a
command that prints it (a password-manager or keychain lookup), so no command
the agent writes ever contains the secret. Set SHOPIFY_API_VERSION to
override the default version.
"""
import csv
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

STORE = os.environ.get("SHOPIFY_STORE")
TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN")
TOKEN_CMD = os.environ.get("SHOPIFY_ACCESS_TOKEN_CMD")
VERSION = os.environ.get("SHOPIFY_API_VERSION", "2026-07")

args = sys.argv[1:]
check_only = "--check" in args
shop_only = "--shop" in args
as_csv = "--csv" in args
query = " ".join(a for a in args if not a.startswith("--")).strip()

# Read-only scopes this skill ever needs. Anything else is a reason to stop.
ALLOWED_SCOPES = {"read_reports", "read_orders", "read_products", "read_customers", "read_analytics"}

SCOPES_QUERY = "query AccessScopes { currentAppInstallation { accessScopes { handle } } }"
SHOP_QUERY = "query ShopInfo { shop { name myshopifyDomain ianaTimezone currencyCode } }"
SHOPIFYQL_QUERY = """query ShopifyQL($query: String!) {
  shopifyqlQuery(query: $query) {
    parseErrors
    tableData { columns { name dataType displayName } rows }
  }
}"""


def fail(msg, code=1):
    sys.stderr.write(f"shopifyql: {msg}\n")
    sys.exit(code)


if not TOKEN and TOKEN_CMD:
    # A command that prints the token, e.g. `op read 'op://Clients/Acme/shopify-token'`
    # or `security find-generic-password -s shopify-token -w`. The secret never
    # appears in a command the agent writes; only the lookup does.
    import subprocess

    try:
        TOKEN = subprocess.run(TOKEN_CMD, shell=True, capture_output=True, text=True, check=True, timeout=30).stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        fail(f"SHOPIFY_ACCESS_TOKEN_CMD failed: {getattr(e, 'stderr', '') or e}")
if not STORE or not TOKEN:
    fail("set SHOPIFY_STORE (xxx.myshopify.com) and SHOPIFY_ACCESS_TOKEN (or SHOPIFY_ACCESS_TOKEN_CMD) in the environment")
if not check_only and not shop_only and not query:
    fail("pass a ShopifyQL query string, --check, or --shop")


def ssl_context():
    """Prefer certifi's CA bundle when installed; python.org builds on macOS often ship without system CAs."""
    try:
        import certifi  # noqa: F401

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def graphql(document, variables=None):
    req = urllib.request.Request(
        f"https://{STORE}/admin/api/{VERSION}/graphql.json",
        data=json.dumps({"query": document, "variables": variables or {}}).encode(),
        headers={"Content-Type": "application/json", "X-Shopify-Access-Token": TOKEN},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60, context=ssl_context()) as res:
            body = json.load(res)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            fail(f"HTTP {e.code} from {STORE}: the token was rejected. Check SHOPIFY_ACCESS_TOKEN and that the custom app is installed on this store.")
        fail(f"HTTP {e.code} from {STORE}")
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e.reason):
            fail(
                "this Python has no CA certificates (common with python.org installs on macOS). "
                "Fix with `pip3 install certifi`, or run `Install Certificates.command` from the Python "
                "folder in /Applications."
            )
        fail(f"cannot reach {STORE}: {e.reason}. Check SHOPIFY_STORE (it should end in .myshopify.com).")
    if body.get("errors"):
        fail("; ".join(err.get("message", "") for err in body["errors"]))
    return body.get("data") or {}


def check_scopes():
    data = graphql(SCOPES_QUERY)
    handles = sorted(s["handle"] for s in (data.get("currentAppInstallation") or {}).get("accessScopes", []))
    writes = [h for h in handles if h.startswith("write_")]
    extras = [h for h in handles if not h.startswith("write_") and h not in ALLOWED_SCOPES]
    if writes:
        fail(
            f"this token can write ({', '.join(writes)}). Use a custom app with read scopes only "
            f"(read_reports is enough for ShopifyQL). Nothing was queried.",
            2,
        )
    if "read_reports" not in handles:
        fail(f"token lacks read_reports, which ShopifyQL needs. Scopes: {', '.join(handles)}")
    return handles, extras


handles, extras = check_scopes()
if check_only:
    print(json.dumps({"store": STORE, "readOnly": True, "scopes": handles, "unexpectedReadScopes": extras}, indent=2))
    sys.exit(0)

if shop_only:
    print(json.dumps(graphql(SHOP_QUERY).get("shop"), indent=2))
    sys.exit(0)

node = graphql(SHOPIFYQL_QUERY, {"query": query}).get("shopifyqlQuery") or {}
if node.get("parseErrors"):
    fail("parse error: " + "; ".join(node["parseErrors"]))
table = node.get("tableData") or {}
columns = [c["name"] for c in table.get("columns", [])]
rows = table.get("rows", [])

if as_csv:
    w = csv.writer(sys.stdout, lineterminator="\n")
    w.writerow(columns)
    w.writerows(rows)
else:
    print(json.dumps({"query": query, "columns": columns, "rows": rows}, indent=2))
