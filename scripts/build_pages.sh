#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# The optional output path keeps local checks separate from `zola serve`.
output="${1:-public}"
base_url="$(python3 -c 'import tomllib; print(tomllib.load(open("zola.toml", "rb"))["base_url"])')"

if [[ "${CF_PAGES:-}" == "1" && "${CF_PAGES_BRANCH:-}" != "main" ]]; then
  : "${CF_PAGES_URL:?Cloudflare must supply the preview deployment URL}"
  base_url="$CF_PAGES_URL"
fi

if [[ "$(zola --version)" != "zola 0.23.4" ]]; then
  echo "This site requires Zola 0.23.4. Set ZOLA_VERSION=0.23.4 in Pages." >&2
  exit 1
fi

zola check --skip-external-links
node --check static/js/site.js
node --check static/js/feedback.js
zola build --base-url "$base_url" --output-dir "$output" --force
python3 scripts/check_site.py "$output" "$base_url"
