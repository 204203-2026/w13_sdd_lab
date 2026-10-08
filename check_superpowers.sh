#!/usr/bin/env bash
# Is Superpowers INSTALLED and LOADED for Codex? Run before Part 5. Worth 0 points; it only tells you.
#   bash check_superpowers.sh          offline: plugin row + skill files on disk
#   bash check_superpowers.sh --probe  also asks Codex to name its skills (needs network, ~30 s)
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT" || exit 1
mkdir -p results
OUT=results/superpowers_check.txt
need="writing-plans executing-plans test-driven-development"
fail=0
say() { echo "$*" | tee -a "$OUT"; }
: > "$OUT"
say "superpowers check $(date '+%Y-%m-%d %H:%M')"

# 1. INSTALLED: Codex lists the plugin as "installed, enabled".
if ! command -v codex >/dev/null 2>&1; then
  say "FAIL installed: codex command not found. Install Codex first. Why: this check needs the codex command."; exit 1
fi
row=$(codex plugin list 2>&1 | grep -E 'superpowers@[^ ]+ +installed, *enabled +[0-9]+\.[0-9]+' | head -1)
if [ -n "$row" ]; then say "PASS installed: $(echo "$row" | tr -s ' ' | cut -c1-90)"
else say "FAIL installed: the Codex plugin list does not show superpowers as installed and enabled. Why: the lab prompt uses its skills. Run: codex plugin add superpowers@superpowers-marketplace"; fail=1; fi

# 2. LOADED (files): the three skills this lab uses exist in Codex's plugin cache.
for s in $need; do
  f=$(ls "$HOME"/.codex/plugins/cache/*/superpowers/*/skills/"$s"/SKILL.md 2>/dev/null | head -1)
  if [ -n "$f" ]; then say "PASS skill file: $s"; else say "FAIL skill file: $s not in ~/.codex/plugins/cache, where Codex saves plugin files. Reinstall the plugin, then restart Codex. Why: Codex needs these skill files."; fail=1; fi
done

# 3. LOADED (live, optional): a fresh Codex session can name the skills.
if [ "$1" = "--probe" ]; then
  q="List the names of your available skills that belong to superpowers. Names only, one line."
  qf=$(mktemp); printf '%s\n' "$q" > "$qf"
  ans=$(codex exec --skip-git-repo-check - < "$qf" 2>/dev/null); rm -f "$qf"
  for s in $need; do
    if echo "$ans" | grep -q "$s"; then say "PASS probe: Codex names $s"; else say "FAIL probe: Codex did not name $s. Restart Codex and retry. Why: a new session can load skills installed after the previous session started."; fail=1; fi
  done
fi

if [ "$fail" -eq 0 ]; then say "RESULT ok: Superpowers is installed and its skill files exist. Use --probe to check whether Codex can name the skills."; else say "RESULT not ready: fix the FAIL lines, or implement by hand (all points stay available)."; fi
echo "Saved: $OUT"
exit "$fail"
