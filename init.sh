#!/usr/bin/env bash
# One setup may use network; required checks are offline after this succeeds.
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT" || exit 1
missing=0
for tool in git python3 uv; do
  command -v "$tool" >/dev/null 2>&1 || { echo "MISSING $tool: install it, then rerun bash init.sh"; missing=$((missing + 1)); }
done
[ "$missing" -eq 0 ] || exit 1
uv sync --frozen || { echo "Setup failed: use an installed Python 3.11–3.13 and retry on a working connection."; exit 1; }
mkdir -p results
uv run --offline --frozen --no-sync python -c 'import fastapi, httpx, pytest; print("OK dependencies cached; bash check.sh is now offline")'
