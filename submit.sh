#!/usr/bin/env bash
ROOT=$(cd "$(dirname "$0")" && pwd)
cd "$ROOT" || exit 1
conflicted=$(git diff --name-only --diff-filter=U)
if [ -n "$conflicted" ]; then
  printf "Resolve conflicts in:\n%s\nThen git add the resolved files and run bash submit.sh again.\n" "$conflicted"
  exit 1
fi
bash check.sh
if ! uv run --offline --frozen --no-sync python grader/gate.py; then
  echo "WARNING: required gate failed. Partial work will still be submitted; inspect results/report.json."
fi
git add -A || exit 1
if ! git diff --cached --quiet; then
  git commit -m "chore: submit spec-driven lab" -m "Record the implementation and local grading results. CI recomputes feedback; the course re-grades after the deadline." || exit 1
fi
branch=$(git branch --show-current)
if [ -z "$branch" ]; then
  echo "Detached HEAD: run git switch main (or your branch), then rerun bash submit.sh."
  exit 1
fi
if [ "$branch" != main ] && [ "$branch" != master ]; then
  echo "WARNING: CI grades main. You are on '$branch'. To grade this work: git switch main && git merge $branch, then rerun bash submit.sh."
fi
git fetch origin || exit 1
if git rev-parse --verify "refs/remotes/origin/$branch" >/dev/null 2>&1 &&
   ! git merge-base --is-ancestor "refs/remotes/origin/$branch" HEAD; then
  if ! git pull --no-rebase --no-edit origin "$branch"; then
    conflicts=(); other=()
    while IFS= read -r file; do
      [ -n "$file" ] || continue
      conflicts+=("$file")
      case "$file" in results/*) ;; *) other+=("$file") ;; esac
    done < <(git diff --name-only --diff-filter=U)
    if [ "${#conflicts[@]}" -eq 0 ]; then
      echo "Pull failed. Inspect git status and your connection, then run bash submit.sh again."
      exit 1
    fi
    if [ "${#other[@]}" -gt 0 ]; then
      printf 'Conflicting files: %s\n' "${conflicts[@]}"
      echo "Please resolve them, git add the resolved files and run bash submit.sh again."
      exit 1
    fi
    for file in "${conflicts[@]}"; do
      if [ -e "$file" ]; then cp -a "$file" "$file.bak_$(date +%s)" || exit 1; fi
      if git cat-file -e ":3:$file" 2>/dev/null; then
        git checkout --theirs -- "$file" || exit 1
        git add -- "$file" || exit 1
      else
        git rm -- "$file" || exit 1
      fi
    done
    git commit --no-edit || exit 1
  fi
fi
tags=()
for tag in spec-draft spec-frozen tests-red; do
  if git rev-parse --verify "refs/tags/$tag" >/dev/null 2>&1; then
    tags+=("+refs/tags/$tag:refs/tags/$tag")
  else
    echo "WARNING: missing tag $tag (its checks will fail)"
  fi
done
git push --atomic -u origin "$branch" "${tags[@]}" || {
  echo "Push failed. Check git remote -v and your connection, then run bash submit.sh again."
  exit 1
}

if [ "${#tags[@]}" -gt 0 ]; then echo "Moved remote checkpoint tags to this attempt."; fi
