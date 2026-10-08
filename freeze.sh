#!/usr/bin/env bash
# Freeze only process evidence; preserve unrelated student work.
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT" || exit 1
case "${1:-}" in
  --draft) stage=spec-draft ;;
  "") stage=spec-frozen ;;
  --red) stage=tests-red ;;
  *) echo "Usage: ./freeze.sh --draft (draft checkpoint) | ./freeze.sh (freeze the reviewed spec) | ./freeze.sh --red (failing-test checkpoint)"; exit 1 ;;
esac
[ "$#" -le 1 ] || { echo "Choose only one checkpoint: draft, reviewed spec, or failing tests. Why: each command saves one checkpoint."; exit 1; }
if [ "$stage" != spec-draft ] && ! git rev-parse --verify refs/tags/spec-draft >/dev/null 2>&1; then
  echo "run ./freeze.sh --draft first; it saves your draft before the review"
  exit 1
fi
[ -f SPEC.md ] || { echo "Write SPEC.md first. Why: a checkpoint needs your spec file."; exit 1; }
if [ "$stage" = tests-red ]; then
  [ -f tests/test_spec.py ] && [ -f SPEC.lock ] || { echo "Freeze SPEC.md, then write tests/test_spec.py first. Why: reviewed requirements must exist before the test checkpoint."; exit 1; }
  git rev-parse --verify refs/tags/spec-frozen >/dev/null 2>&1 || { echo "Missing spec-frozen; run ./freeze.sh first. Why: the test checkpoint needs the reviewed spec checkpoint."; exit 1; }
fi
if [ ! -f .venv/bin/python ] && [ ! -f .venv/Scripts/python.exe ]; then
  echo "SETUP MISSING: run bash init.sh once on a working connection, then retry. Why: checkpoint checks need installed lab tools."
  exit 1
fi
python3 - "$stage" <<'PYNOOP'
import hashlib, json, subprocess, sys
from pathlib import Path
stage = sys.argv[1]
def lf(data): return data.replace(b'\r\n', b'\n')
def exists(tag):
    return subprocess.run(['git', 'rev-parse', '--verify', 'refs/tags/' + tag],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
if stage == 'spec-draft' and exists('spec-frozen'):
    sys.exit('spec-frozen exists: a new draft would remove proof of your review changes. Keep this checkpoint. Start a fresh reviewed attempt in another folder. See TASKS.md Part 6, Starting a fresh reviewed attempt.')
if exists(stage):
    name = 'tests/test_spec.py' if stage == 'tests-red' else 'SPEC.md'
    old = subprocess.run(['git', 'show', f'{stage}:{name}'], capture_output=True, timeout=60)
    current = lf(Path(name).read_bytes())
    data = json.loads(Path('SPEC.lock').read_text(encoding='utf-8')) if Path('SPEC.lock').exists() else {}
    key = 'tests_sha256' if stage == 'tests-red' else 'spec_sha256'
    if old.returncode == 0 and lf(old.stdout) == current and (
            stage == 'spec-draft' or data.get(key) == hashlib.sha256(current).hexdigest()):
        short = subprocess.check_output(['git', 'rev-parse', '--short', stage], text=True).strip()
        print(f'Already saved {stage} at {short}; nothing to do.')
        sys.exit(10)
    sys.exit(f'{stage} already exists with different content. Keep this checkpoint. Why: it preserves your original spec or tests. Start a fresh reviewed attempt in another folder. The script changed no files or checkpoints. See TASKS.md Part 6, Starting a fresh reviewed attempt.')
PYNOOP
rc=$?
[ "$rc" -ne 10 ] || exit 0
[ "$rc" -eq 0 ] || exit 1
if [ "$stage" = tests-red ]; then
  UV_OFFLINE=1 UV_PYTHON_DOWNLOADS=never uv run --offline --frozen --no-sync python grader/check.py --red-preview
  if [ "$?" -ne 0 ]; then
    echo "Not frozen: every test must fail on the current app before --red. Add checks to the tests listed above, then retry. A test for a missing ID must first create a note. Why: the blank app already returns 404, which alone does not prove a test detects missing behavior."
    exit 1
  fi
fi
if [ "$stage" != spec-draft ]; then
  python3 - "$stage" <<'PY'
import hashlib, json, shutil, sys, time
from datetime import datetime, timezone
from pathlib import Path
stage = sys.argv[1]
p = Path('SPEC.lock')
data = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
def lf(data): return data.replace(b'\r\n', b'\n')
digest = hashlib.sha256(lf(Path('SPEC.md').read_bytes())).hexdigest()
if stage == 'tests-red':
    if data.get('spec_sha256') != digest:
        sys.exit('SPEC.md changed: review and freeze it before freezing tests. Why: the test checkpoint must refer to the same saved spec fingerprint.')
    data['tests_sha256'] = hashlib.sha256(lf(Path('tests/test_spec.py').read_bytes())).hexdigest()
else:
    if data.get('spec_sha256') != digest:
        data = {'spec_sha256': digest, 'frozen_at': datetime.now(timezone.utc).isoformat()}
    data.setdefault('frozen_at', datetime.now(timezone.utc).isoformat())
content = json.dumps(data, indent=2) + '\n'
if not p.exists() or p.read_text(encoding='utf-8') != content:
    if p.exists(): shutil.copy2(p, str(p) + '.bak_' + str(time.time_ns()))
    p.write_text(content, encoding='utf-8')
PY
  [ "$?" -eq 0 ] || exit 1
fi
case "$stage" in
  spec-draft) paths=(SPEC.md) ;;
  spec-frozen)
    paths=(SPEC.md SPEC.lock)
    for file in REVIEW.md REVIEW2.md; do [ ! -f "$file" ] || paths+=("$file"); done ;;
  tests-red) paths=(SPEC.lock tests/) ;;
esac
git add -- "${paths[@]}" || exit 1
if ! git diff --cached --quiet -- "${paths[@]}"; then
  git commit -m "freeze: $stage" -- "${paths[@]}" || { echo "Commit failed: set git user.name/user.email and retry. Why: git needs your name and email to identify the commit author."; exit 1; }
fi
# Refuse a tag created concurrently too; never replace a saved checkpoint.
git tag "$stage" || exit 1
case "$stage" in
  spec-draft) echo "Saved draft checkpoint spec-draft at $(git rev-parse --short HEAD)." ;;
  spec-frozen) echo "Froze the reviewed spec: spec-frozen at $(git rev-parse --short HEAD). bash check.sh compares SPEC.lock fingerprints with saved files." ;;
  tests-red) echo "Saved failing-test checkpoint tests-red at $(git rev-parse --short HEAD). bash check.sh compares SPEC.lock fingerprints with saved files." ;;
esac
