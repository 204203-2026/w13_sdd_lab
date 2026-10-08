#!/usr/bin/env bash
# One setup may use network; required checks are offline after this succeeds.
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT" || exit 1
missing=0
for tool in git python3 uv; do
  command -v "$tool" >/dev/null 2>&1 || { echo "MISSING $tool: install it, then rerun bash init.sh. Why: setup needs this tool."; missing=$((missing + 1)); }
done
[ "$missing" -eq 0 ] || exit 1
uv sync --frozen || { echo "Setup failed: use an installed Python 3.11–3.13 and retry on a working connection. Why: lab tools need these versions and downloads."; exit 1; }
mkdir -p results
uv run --offline --frozen --no-sync python -c 'import fastapi, httpx, pytest; print("OK: required Python tools are saved on your computer. bash check.sh now runs without a network connection.")'
