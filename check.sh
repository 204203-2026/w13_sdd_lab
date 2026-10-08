#!/usr/bin/env bash
# Required checks are offline. JSON carries the grade; this script always exits 0.
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT" || exit 0
export UV_OFFLINE=1 UV_PYTHON_DOWNLOADS=never
export W13_CONTRACT_SHA256="ffd867b4d9d84e48862bfffab82c2ec5c79a84a4573dc44a7ca3fa8db58cbc33"
mkdir -p results
REQ_ITEMS=""; BONUS_ITEMS=""; FAIL=0; TOTAL=0
record() {
  REQ_ITEMS="${REQ_ITEMS}${3},"
  TOTAL=$((TOTAL + 1))
  if [ "$2" = PASS ]; then echo "PASS $1"; else FAIL=$((FAIL + 1)); echo "FAIL $1"; fi
}
record_bonus() { BONUS_ITEMS="${BONUS_ITEMS}${3},"; echo "$2 $1 (optional)"; }
required() {
  row=""; rc=1
  if [ "$SETUP_MISSING" -eq 0 ]; then
    row=$(uv run --offline --frozen --no-sync python grader/check.py "$1")
    rc=$?
  fi
  if [ -z "$row" ]; then row="{\"name\":\"$1\",\"status\":\"fail\",\"points\":0,\"max\":$2}"; rc=1; fi
  if [ "$rc" -eq 0 ]; then record "$1" PASS "$row"; else record "$1" FAIL "$row"; fi
}
bonus() {
  row=""; rc=1
  if [ "$SETUP_MISSING" -eq 0 ]; then
    row=$(uv run --offline --frozen --no-sync python grader/check.py "$1")
    rc=$?
  fi
  if [ -z "$row" ]; then row="{\"name\":\"$1\",\"status\":\"todo\",\"points\":0,\"max\":$2}"; rc=1; fi
  if [ "$rc" -eq 0 ]; then record_bonus "$1" DONE "$row"; else record_bonus "$1" TODO "$row"; fi
}
SETUP_MISSING=0
if { [ ! -f .venv/bin/python ] && [ ! -f .venv/Scripts/python.exe ]; } ||
   ! uv run --offline --frozen --no-sync python -c 'import fastapi, httpx, pytest'; then
  echo "SETUP MISSING: run bash init.sh once on a working connection, then rerun bash check.sh. Why: setup downloads tools for offline checks."
  SETUP_MISSING=1
fi
required contract_intact 0
required impl_original 0
required spec_sections 2
required spec_acs 2
required review_file 1
required review_crossref 1
required review_applied 2
required spec_frozen 1
required ac_test_map 2
required red_evidence 2
required tests_green 1
required grader_api 2
required ui_static 1
required tests_pass_correct 1
required tests_catch_wrong 2
bonus ui_behaviour 2
bonus edge_case_tests 1
bonus review_round2 1
bonus deployed 2
# Reporting needs only stdlib; avoid creating an environment when setup is missing.
REPORT_ARGS=()
if [ "$SETUP_MISSING" -eq 1 ]; then
  REPORT_ARGS=(--no-project --python ">=3.11,<3.14")
fi
uv run --offline --frozen --no-sync "${REPORT_ARGS[@]}" python grader/check.py --reports "[${REQ_ITEMS%,}]" "[${BONUS_ITEMS%,}]"
uv run --offline --frozen --no-sync "${REPORT_ARGS[@]}" python - <<'PYREPORT'
import json
r = json.load(open('results/report.json', encoding='utf-8'))
b = json.load(open('results/challenge_report.json', encoding='utf-8'))
print(f"Score: {r['score']}/{r['total']} required | Bonus: {b['bonus']}/{b['bonus_total']}")
PYREPORT
exit 0
