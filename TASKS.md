# Lab 13 — Write, review, test, build

About **3 hours (2.5–4 hours)**. The parts below add up to 175 minutes.
Due **Friday 16 October 2026, 23:59 (Asia/Bangkok)**.

You will build a small notes app. Read the fixed behaviour in BRIEF.md first.
An API is the set of requests a program accepts and the results it returns.
An acceptance criterion (AC) is one sentence whose result you can check.
An edge case is an unusual input or situation. A checkpoint is a saved snapshot.
Contract: the names and behaviours the grader expects (grading/CONTRACT.md). A selector names one page element; data-testid is the HTML attribute used for it. Copy the six values exactly and put v-for on note-item.

Use a terminal inside this repository. Code blocks marked bash are commands.
Read the printed check names; FAIL is expected while work is still missing.

> Released Friday 9 October 2026 after the lecture. Due Friday 16 October 2026, 23:59 (Asia/Bangkok).
> Order: brief -> spec -> AI review -> tests -> code. BRIEF.md is the fixed request; SPEC.md is your answer to it.
> The lab's helper scripts (init.sh, freeze.sh, check.sh, submit.sh) make the git commits, tags and the fingerprint
> file for you. Never edit SPEC.lock or move a tag. One required endpoint reads one value from SPEC.lock (BRIEF.md).
> Optional bonus: 6 points, outside the 175 minutes. Read "Bonus" before Part 2: the second review (B3) must happen
> before you freeze the reviewed spec, and extra edge tests (B2) before the failing-test checkpoint.
> check.sh is the lab's definition of done: when all required checks pass, the lab is finished.

## Part 0 — Start (10 minutes)

Create your student repository with "Use this template" or the course's GitHub
Classroom link, then clone it. Read the brief.
BRIEF.md is the fixed request: what is asked, written by the instructor; you do not change it. SPEC.md is your answer: precise sentences a test can check.
Prepare the tools and see the starting score.

```bash
bash init.sh
bash check.sh
cat results/report.json
cat BRIEF.md grading/CONTRACT.md
```

Leaves: `.venv/` (installed Python tools) and `results/report.json`.
Checks: `contract_intact` and `impl_original` (0-point protection checks).
The starting score is 0/20. Both protection checks should pass.

Troubleshooting:

- `SETUP MISSING`: run `bash init.sh` once on a working connection, then retry.
- uv missing: use the course setup instructions to install uv, then retry.
- Python unsupported: use Python 3.11–3.13. For an installed Python 3.13, run
  `uv sync --python python3.13 --frozen`.
- Windows: use WSL Ubuntu and bash. Save files with LF line endings;
  .gitattributes also keeps repository line endings consistent.
- Network down: complete setup on a working connection first. Then check offline
  tools with `uv run --offline --frozen --no-sync python -c 'import fastapi, httpx, pytest'`.
- `contract_intact` fails: compare instructor files with a fresh template in another
  folder. Back up any edited file before copying its original version back.

## Part 1 — Write the spec (40 minutes)

Edit SPEC.md by hand. Replace the TODO text and all example placeholders.
Use these four headings, in this order:

```markdown
## Goal
## Acceptance criteria
## Edge cases
## Out of scope
```

Write a goal in one or two plain sentences. Add at least five AC lines, numbered
from AC-01 without gaps. Write at least 30 characters in the sentence after `AC-NN:`
and a result a test can check. Six small ACs for create, list, delete, blank titles, health,
and the page are a useful starting point. Keep the API from BRIEF.md.
Put at least one concrete bullet under Edge cases and Out of scope.
Extra sections are fine. EP/UI labels from the contract are optional; if you use
one, use a real ID in its own brackets, such as `[EP-1]`.

Tiny worked example for a **different toy feature**, not this lab's notes app:

```markdown
# Ping check
## Goal
Let a caller check that the service responds.
## Acceptance criteria
- AC-01: GET /api/ping returns 200 and JSON {"pong": true}.
## Edge cases
- An unknown path returns 404.
## Out of scope
- This does not monitor other services.
```

That shows the shape; your notes spec needs at least five ACs.
### What freeze.sh is, what it does, and why

- What it is: a short shell script (about 90 lines) that ships inside this repo.
  We wrote it; it is not a standard tool and you cannot install it.
  freeze.sh is a helper that makes the git commit and the tag the grader looks for.
- What it does:
  1. Checks the order (spec before tests before code).
  2. For the failing-test checkpoint only, runs your tests and refuses unless they all fail.
  3. Saves the checkpoint: a git commit plus a name tag, and SPEC.lock, a fingerprint
     file the grader reads (SPEC.lock is written only for the reviewed spec and tests).
- What is in it: nothing new: git commands plus the Week 4 shell ideas (a case on
  the flag, if checks, running a command and reading its exit status).
- Why:
  - The grader needs proof that the spec came before the tests and the tests before the code.
  - A commit can be rewritten, so the script also saves a fingerprint of the spec.
  - The agent must not be able to move the goalposts.
- Why the draft checkpoint comes BEFORE the review: the AI writes REVIEW.md;
  you edit SPEC.md. The saved draft shows exactly what the review made you change,
  lets you go back if the advice was bad, and is the proof for the grader that the
  spec was revised after the review. review_applied compares your draft checkpoint
  with your frozen spec: `git diff spec-draft spec-frozen -- SPEC.md` must be
  non-empty AND `## Changes after review` must cite an existing AC.
- In your own projects: you will not have freeze.sh. Keep the habit: save a
  checkpoint with plain git (`git commit`, optionally `git tag`) before a review
  or an agent changes things.

Save your draft checkpoint (the script flag is --draft). Why now, before the
review: the AI writes REVIEW.md and you edit SPEC.md; the saved draft shows exactly
what the review made you change, lets you go back if the advice was bad, and proves
the spec was revised after the review. review_applied compares your draft checkpoint
with your frozen spec.

```bash
bash check.sh
./freeze.sh --draft
```

Leaves: SPEC.md and a saved draft checkpoint. The script prints `Saved draft checkpoint spec-draft at <sha>.`
Checks: `spec_sections` (2), `spec_acs` (2).

Troubleshooting:

- Sections fail: add all four headings, a goal, and real bullets under the last two.
- ACs fail: use AC-01, AC-02, and so on, with no gaps or duplicates. Write concrete
  at least 30 characters in the sentence after `AC-NN:`. Remove TODO, lorem, and `<your ...>` text.
- Capitalisation, a colon after a heading, `*` bullets, and AC-1 numbering are accepted.
- Optional tag fails: compare its ID with grading/CONTRACT.md, or omit the tag.
- Checkpoint cannot save: run `git config user.name "Your Name"` and
  `git config user.email "you@example.com"`, then retry.
- Draft already saved: leave it in place. The review needs your actual first draft.

## Part 2 — Review and revise (20 minutes)

Give an AI BRIEF.md (the request), your SPEC.md (your answer), grading/CONTRACT.md and the review prompt.
Save its answer in REVIEW.md. Read the comments and make a small real clarification.
Add `## Changes after review` at the end of SPEC.md, then a dated level-3 heading
and one bullet per change, for example:

```markdown
## Changes after review
### 2026-10-09 Review one
- AC-03: clarified deleting a note twice returns 404.
```

```bash
cat prompts/review_prompt.md
bash check.sh
```

Leaves: REVIEW.md and revised SPEC.md.
Checks: `review_file` (1), `review_crossref` (1), `review_applied` (2, finishes in Part 3).
REVIEW.md needs Ambiguities, Missing edge cases, and Verdict headings. The first two
need at least two bullets each. Cite at least two different existing AC IDs overall.

Troubleshooting:

- Review says only "looks good": ask it to check blank inputs, missing IDs, and how
  the page shows an error. Request concrete questions linked to your ACs.
- Review check fails: add the three headings and enough bullets. Remove invented AC IDs.
- Agent down or quota used up: review the same cases yourself and write REVIEW.md
  by hand. Required points check the files, not the provider.
- Want the second-review bonus: do it now. Save REVIEW2.md in the same format and
  add a second dated block under Changes after review before Part 3.

## Part 3 - Freeze the reviewed spec (5 minutes)

Freeze the reviewed spec before writing tests or app code.
review_applied compares your draft checkpoint with your frozen spec, so the draft
must already be saved (Part 1) and your revision must cite an AC under Changes after review.

What it is:

- A short shell script shipped inside this repo.
- Written by us; not a standard tool you install.
- A helper that makes a git commit and a name tag.

What it does:

- Checks the order: spec before tests before code.
- Runs tests for the failing-test checkpoint and refuses unless all fail.
- Saves a commit and tag; writes SPEC.lock for the reviewed spec and tests.

Why:

- The grader needs proof of the spec, tests, code order.
- A commit can be rewritten, so the script saves a spec fingerprint too.
- The agent must not be able to move the goalposts.

Full box: Part 1.

```bash
./freeze.sh
bash check.sh
```

Leaves: SPEC.lock and the reviewed spec checkpoint. The script prints `Froze the reviewed spec: spec-frozen at <sha>.`
Checks: `review_applied` (2), `spec_frozen` (1).
Re-running this command on unchanged files prints `Already saved spec-frozen at <sha>; nothing to do.`

Troubleshooting:

- Review-applied fails: make a real AC clarification after the saved draft and record
  it under Changes after review. Whitespace-only changes do not count.
- Spec changed after this step: see Part 6, "Starting a fresh reviewed attempt".
  Keep the old folder as your backup; redo the review and checkpoints in order.
- Checkpoint command reports missing setup: return to `bash init.sh` in Part 0.

## Part 4 — Write tests and watch them fail (45 minutes)

Create tests/test_spec.py. A test calls the app and uses `assert` to check its result.
Use the supplied `client` argument: it calls the app without a running server and
starts each test with empty state. Write one `def test_ac_NN_description(client):`
per AC, using two digits in the test name. Each `test_ac_NN_...` function needs an
`assert` and a call through `client`. Either may be in the test itself or in a
helper the test calls directly; name that helper's parameter `client`. The grader
follows one helper level only. Path constants are fine; no special literal strings
are required.

The ping example from Part 1 becomes this test in a **separate toy project**:

```python
def test_ac_01_ping(client):
    response = client.get('/api/ping')
    assert response.status_code == 200
    assert response.json() == {'pong': True}
```

Run `uv run --offline --frozen --no-sync pytest -q tests/test_ping.py` there before
adding the route. A blank app returns 404, so the test reports `1 failed`:
`assert 404 == 200`. That is red: the test found the missing feature.
Do not add the ping route or test to your notes lab.

For your notes tests, run:

```bash
uv run --offline --frozen --no-sync pytest -q tests/test_spec.py
bash check.sh
# Inspect ac_test_map and test-quality rows before saving.
./freeze.sh --red
bash check.sh
```

Leaves: tests/test_spec.py, updated SPEC.lock, and the failing-test checkpoint.
Checks: `ac_test_map` (2), `red_evidence` (2).
Every test must fail on the starting app: **zero passed, no collection errors**.
The checkpoint command prints failing tests and `Saved failing-test checkpoint tests-red at <sha>.` when ready.
Tests will also be tried on one correct app and four deliberately wrong apps.
A page-content test can keep `tests_pass_correct` failing until Part 5 creates
your page: these test apps use your HTML file. Do not weaken that valid page test.

Troubleshooting:

- A missing-ID test passes: the blank app already returns 404. First create a note
  and assert success, then try the missing or already deleted ID.
- Any test passes: check a missing behaviour from its AC before saving the checkpoint.
- Collection error: fix Python syntax or imports; use a `client` parameter in each test.
  Leave tests/conftest.py unchanged.
- Mapping fails: match each AC with `test_ac_01_...`, `test_ac_02_...`, etc.; include
  an actual assert and a call through client.
- Wrong-app test passes: strengthen API assertions before saving this checkpoint.
  Check status codes, blank titles, deletion twice, and all four response fields.
- tests_catch_wrong looks full but tests_pass_correct fails: ignore the mutant
  rows until tests_pass_correct passes. A page test that fails on every app
  (because your page does not exist yet) makes tests_catch_wrong look full;
  strengthen API assertions before saving.
- Correct-app test fails: compare API assertions with BRIEF.md now. A valid page
  test may wait for HTML in Part 5. Optional page polish is outside these app tests.
- Agent down: write the tests by hand. pytest runs without an agent account.

## Part 5 — Let the agent implement (45 minutes)

Give Codex this prompt after the failing-test checkpoint is saved. TDD means writing
failing tests first, then adding code until they pass.

```text
Implement SPEC.md on the current branch. Follow AGENTS.md.
Use Superpowers writing-plans, executing-plans inline, and test-driven-development.
SPEC.md and tests/test_spec.py are read-only. Run the frozen tests red first.
Write app/main.py and app/static/index.html until the tests pass.
Use module-level in-memory state, Vue 3 CDN, no build and no database.
Do not open grading/impls. Put extra modules under app/.
Describe conflicts in REVIEW.md; never weaken tests.
Run bash check.sh and inspect the reports. Leave submission to me.
```

Run the checks and save the implementation:

```bash
uv run --offline --frozen --no-sync pytest -q tests/test_spec.py
bash check.sh
git add app/
git commit -m "feat: implement reviewed notes specification" -m "Implement the saved acceptance criteria without changing tests. Verified the offline student suite."
```

Leaves: app/main.py, app/static/index.html, and a saved implementation commit.
Checks: `tests_green` (1), `grader_api` (2), `ui_static` (1), `tests_pass_correct` (1),
`tests_catch_wrong` (2), `impl_original` (0-point protection check).

Optional: ask a second AI to review the finished change against SPEC.md and AGENTS.md
(code review). Record anything it finds in REVIEW.md. No points depend on it.

Troubleshooting:

- Agent or Superpowers unavailable: implement by hand. All required points remain available.
- Agent edits saved spec or tests: see Part 6, "Starting a fresh reviewed attempt".
  Tell the agent to respect read-only files. Do not hide edits in the checkpoint.
- API check fails: compare methods, statuses, note fields, blank titles, deletion twice,
  empty initial memory, and the health result with BRIEF.md.
- Static page check fails: serve the page at `/`, use all six double-quoted data-testid
  values, put v-for on note-item itself, and use fetch with `/api/notes`.
- `impl_original` fails: write your own code from the brief. Renaming copied instructor
  reference apps (grading/impls, called test oracles in AGENTS.md) does not count as original work.
- Saved tests reveal a mistake: record it in REVIEW.md and see Part 6, "Starting a
  fresh reviewed attempt"; do not rewrite saved tests to make code pass.

## Part 6 — Check and submit (10 minutes)

check.sh is the lab's definition of done: when all required checks pass, the lab is finished.
Read the results, then submit whatever you completed.

```bash
bash check.sh
uv run --offline --frozen --no-sync python grader/gate.py
cat results/report.json results/challenge_report.json
bash submit.sh
```

Leaves: results/*.json, submitted branch and checkpoints, and GitHub feedback.
Checks: all required checks, **20 points** total. Bonus is separate.
check.sh always exits 0; gate.py passes only when every required check passes.
submit.sh accepts partial work with a warning. CI means GitHub's automatic checks.
It grades main (or master for older repositories) and recomputes the reports.
After the deadline the course re-grades with the saved instructor grader.

Troubleshooting:

- CI is red: read its failing rows. A partial score is still useful.
- Branch is neither main nor master: submit.sh prints the merge command for main.
  If your repository uses master, substitute master. Preserve the current branch.
- Push says "fetch first": rerun `bash submit.sh`; it merges GitHub's report updates.
  Report-file conflicts are resolved automatically using the remote version.
  Any other conflict stops submit.sh with the file list: resolve each file,
  `git add` it, `git commit`, then rerun `bash submit.sh`.
- A checkpoint is missing: return to its part and follow the honest order. If app code
  already exists, see "Starting a fresh reviewed attempt" below. Do not replace saved checkpoints.
- Network down: keep your local work and reports; rerun submission when connected.

### Starting a fresh reviewed attempt

Keep the old folder as your backup. Clone your own student repository, preserving
its history, so submission needs no merge with your old attempt. Repositories made
with "Use this template" or Classroom start with one template snapshot commit;
the root below is that snapshot.

```bash
git clone <your repository URL> lab13-attempt2
cd lab13-attempt2
root=$(git rev-list --max-parents=0 HEAD | tail -1)
git rm -r -q app && git checkout "$root" -- SPEC.md app
git rm -q --ignore-unmatch REVIEW.md REVIEW2.md SPEC.lock tests/test_spec.py
git tag -d spec-draft spec-frozen tests-red
git commit -m "chore: start a fresh reviewed attempt"
bash init.sh
```

If your repository carries the template's own history, its root is the old v1
commit (`1276955`), not LIGHT v2. Before the reset, find the starting snapshot with
`git log --reverse --oneline`: choose the commit whose message says "template
snapshot" (or ask the instructor which starting commit to use), then set
`root=<that commit's hash>` instead of the root command above. Do not use the old
v1 root. Missing local tags print an error but existing named tags are deleted;
continue with the commit and init commands.

Then redo Part 1 to Part 5 in order; submit only from this new folder (the last
submit wins). `git rm -r app` removes extra modules an agent added, too. `git tag -d`
only deletes LOCAL tags in the new folder; submit.sh replaces the remote checkpoint tags.

## Bonus — Optional (outside the 175 minutes)

```bash
bash check.sh
cat results/challenge_report.json
```

Leaves: optional tests, REVIEW2.md, or vercel_url.txt, plus bonus report.
Checks: `ui_behaviour` (2), `edge_case_tests` (1), `review_round2` (1), `deployed` (2).
Total: **6 bonus points**. TODO does not reduce required points.

- B1: browser interaction checks creating, validation, and deletion. Playwright is
  the browser test tool; CI prepares it when available.
- B2: before Part 4's checkpoint, add at least one `test_ac_NN_edge_...` test, or
  reference that test's AC in an Edge cases bullet.
- B3: before you freeze the reviewed spec, do a second review (REVIEW2.md, same
  headings, two AC IDs) and add a second `### YYYY-MM-DD` block under Changes after review.
- B4: deploy with Vercel's Python/FastAPI support. Include SPEC.lock, and save your
  HTTPS URL in vercel_url.txt. No deployment account is required for the main lab.

Troubleshooting:

- Browser or CDN unavailable: B1 stays TODO; required static checks still run offline.
- Deployment unreachable: B4 stays TODO. Check its URL and `/api/health`, then retry.
- Deployment health differs from local: include the saved SPEC.lock and redeploy.
- Bonus needs a spec or test change: plan it before the checkpoints. Keep saved files read-only.
