#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# The optional output path keeps local checks separate from `zola serve`.
output="${1:-public}"

# A newly connected Pages project serves only the closed bootstrap until Access
# has been verified and ASTRO90_BUILD_MODE=site is set in Cloudflare.
if [[ "${CF_PAGES:-}" == "1" ]]; then
  case "${ASTRO90_BUILD_MODE:-bootstrap}" in
    bootstrap)
      python3 - "$output" <<'PY'
from pathlib import Path
import shutil
import sys

root = Path.cwd()
output = Path(sys.argv[1]).resolve()
if output != root / "public" and root / ".local" not in output.parents:
    raise SystemExit("Bootstrap output must be public/ or inside .local/.")
if output.exists():
    shutil.rmtree(output)
shutil.copytree(root / "scripts/cloudflare-bootstrap", output)
print("Built the private bootstrap. No website content is included.")
PY
      exit 0
      ;;
    site) ;;
    *) echo "ASTRO90_BUILD_MODE must be bootstrap or site." >&2; exit 1 ;;
  esac
fi

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
