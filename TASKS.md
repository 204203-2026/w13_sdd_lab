# Lab 13 — Write, review, test, build

About **3 hours (2.5–4 hours)**. The parts below add up to 175 minutes.
Due **Friday 16 October 2026, 23:59 (Asia/Bangkok)**.

You will build a small notes app. Read the fixed behaviour in BRIEF.md first.
An API defines requests your app accepts and results it returns.
An acceptance criterion (AC) is one sentence whose result you can check.
An edge case is an unusual input or situation. A checkpoint is a saved snapshot.
Contract: names and behaviors the grader expects (grading/CONTRACT.md). A selector identifies one page element.
data-testid is an HTML label tests use to find an element. Copy the six values exactly and put v-for on note-item.
Why: page checks use these values and expect note-item itself to repeat.

A repository is a project folder whose changes git records. Cloning copies it and its history to your computer.
Use a terminal inside this repository. Why: commands use paths relative to this folder. Code blocks marked bash are commands.
Read the printed check names; FAIL is expected while work is still missing.

> Released Friday 9 October 2026 after the lecture. Due Friday 16 October 2026, 23:59 (Asia/Bangkok).
> Order: brief -> spec -> AI review -> tests -> code. BRIEF.md is the fixed request; SPEC.md is your answer to it.
> The lab's helper scripts (init.sh, freeze.sh, check.sh, submit.sh) save commits and tags for you.
> They also write the fingerprint file. Never edit SPEC.lock or move a tag. Why: the grader needs unchanged snapshots and fingerprints.
> An endpoint is one API address and request method. One required endpoint reads one value from SPEC.lock (BRIEF.md).
> Optional bonus: 6 points, outside the 175 minutes. Read "Bonus" before Part 2.
> The second review (B3) must happen before you freeze the reviewed spec. Add extra edge tests (B2) before the failing-test checkpoint.
> Why: specs and tests become read-only, so later bonus changes can need a new attempt.
> check.sh is the lab's definition of done. When all required checks pass, the lab is finished.

## Part 0 — Start (10 minutes)

Create your student repository with "Use this template" or the course's GitHub
Classroom link, then clone it. Why: you need your own copy to edit and submit. Read the brief.
The instructor wrote the fixed request in BRIEF.md. Do not change it. SPEC.md is your answer: sentences tests can check.
Why: changing the request cannot change what the grader checks.
Prepare the tools and see the starting score. Why: this confirms setup works before you write anything.

```bash
bash init.sh
bash check.sh
cat results/report.json
cat BRIEF.md grading/CONTRACT.md
```

Files created: `.venv/` (installed Python tools) and `results/report.json`.
Checks: `contract_intact` and `impl_original` (0-point protection checks).
The starting score is 0/20. Both protection checks should pass.

Troubleshooting:

- `SETUP MISSING`: run `bash init.sh` once on a working connection, then retry. Why: setup downloads tools for offline checks.
- uv missing: use the course setup instructions to install uv, then retry. Why: scripts use uv to run Python tools.
- Python unsupported: use Python 3.11–3.13. For an installed Python 3.13, run
  `uv sync --python python3.13 --frozen`. Why: lab tools need a supported Python version.
- Windows: use WSL Ubuntu and bash. Save files with LF line endings;
  .gitattributes also keeps repository line endings consistent. Why: WSL runs Linux shell commands; LF prevents newline errors.
- Network unavailable: complete setup on a working connection first. Then check offline
  tools with `uv run --offline --frozen --no-sync python -c 'import fastapi, httpx, pytest'`. Why: setup needs downloads; later checks do not.
- `contract_intact` fails: compare instructor files with a fresh template in another
  folder. Save a backup of any edited file before restoring its original version. Why: a backup preserves your changes.

## Part 1 — Write the spec (40 minutes)

Edit SPEC.md by hand. Replace TODO text and example placeholders. Why: you must decide expected behavior before AI writes code.
Use these four headings, in this order. Why: the grader finds required content under these headings:

```markdown
## Goal
## Acceptance criteria
## Edge cases
## Out of scope
```

Write a goal in one or two plain sentences. Add at least five AC lines, numbered from AC-01 without gaps.
Write at least 30 characters after `AC-NN:` and a result a test can check.
Why: the grader needs detailed ACs with continuous IDs to match requirements to tests.
Six small ACs for create, list, delete, blank titles, health, and the page are a useful starting point.
Keep the API from BRIEF.md. Why: the grader checks this fixed API.
Put at least one specific bullet under Edge cases and Out of scope. Why: these record unusual inputs and excluded features.
Extra sections are fine. EP labels identify endpoints; UI labels identify page elements in the contract.
These labels are optional. If you use one, use a real ID in its own brackets, such as `[EP-1]`.
Why: the grader rejects labels absent from the contract.

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

- What it is: a short shell script (about 90 lines) included in this repository.
  We wrote it; it is not a standard tool and you cannot install it.
  freeze.sh is a helper that makes the git commit and the tag the grader looks for.
- What it does:
  1. Checks the order (spec before tests before code).
  2. For the failing-test checkpoint only, runs your tests and refuses unless they all fail.
  3. Saves the checkpoint: a git commit plus a git tag.
     For the reviewed spec and tests, it also writes SPEC.lock, a fingerprint file the grader reads.
- What is in it: git commands and Week 4 shell ideas.
  These include case for choosing a flag, if checks, and command exit values.
- Why:
  - The grader needs proof that the spec came before the tests and the tests before the code.
  - A commit can be rewritten, so the script also saves a fingerprint of the spec.
  - The agent must not change the requirements to make its code pass.
- Why the draft checkpoint comes BEFORE the review: the AI writes REVIEW.md; you edit SPEC.md.
  The saved draft shows those edits. You can return to it if the advice was bad.
  The grader uses it as proof of revision. review_applied compares your draft checkpoint with your frozen spec.
  `git diff spec-draft spec-frozen -- SPEC.md` must show a change.
  `## Changes after review` must name an existing AC.
- In your own projects: you will not have freeze.sh. Keep the habit: save a
  checkpoint with plain git (`git commit`, optionally `git tag`) before a review
  or an agent changes things.

Save your draft checkpoint (the script flag is --draft) before review.
Why: the draft preserves your first version and proves that review changed it.
review_applied compares your draft checkpoint with your frozen spec.

```bash
bash check.sh
./freeze.sh --draft
```

Files created: SPEC.md and a saved draft checkpoint. The script prints `Saved draft checkpoint spec-draft at <sha>.`
Checks: `spec_sections` (2), `spec_acs` (2).

Troubleshooting:

- Sections fail: add all four headings, a goal, and specific bullets under the last two. Why: these are required content.
- ACs fail: use AC-01, AC-02, and so on, with no gaps or duplicates.
  Write a specific sentence of at least 30 characters after `AC-NN:`. Remove TODO, lorem, and `<your ...>` placeholder text.
  Why: the grader rejects incomplete ACs.
- Capitalisation, a colon after a heading, `*` bullets, and AC-1 numbering are accepted.
- Optional EP/UI label fails: compare its ID with grading/CONTRACT.md, or omit the label. Why: labels must exist there.
- Checkpoint cannot save: run `git config user.name "Your Name"` and
  `git config user.email "you@example.com"`, then retry. Why: git needs an author name and email for commits.
- Draft already saved: keep the saved draft unchanged. The review needs your actual first draft.

## Part 2 — Review and revise (20 minutes)

Give an AI BRIEF.md (the request), your SPEC.md (your answer), grading/CONTRACT.md and the review prompt.
Save its answer in REVIEW.md. Read the comments and make a small real clarification.
Why: review finds unclear requirements before you write tests for the wrong behavior.
Add `## Changes after review` at the end of SPEC.md, then a dated level-3 heading
and one bullet per change. A level-3 heading starts with ###. Why: dated blocks record each review round and its AC changes.
For example:

```markdown
## Changes after review
### 2026-10-09 Review one
- AC-03: clarified deleting a note twice returns 404.
```

```bash
cat prompts/review_prompt.md
bash check.sh
```

Files created: REVIEW.md and revised SPEC.md.
Checks: `review_file` (1), `review_crossref` (1), `review_applied` (2, finishes in Part 3).
REVIEW.md needs Ambiguities, Missing edge cases, and Verdict headings. The first two
need at least two bullets each. Cite at least two different existing AC IDs overall.
Ambiguities have more than one possible meaning; Verdict means final decision. Why: these minimums link several review comments to your requirements.

Troubleshooting:

- Review says only "looks good": ask it to check blank inputs and missing IDs.
  Also ask how the page shows an error. Request specific questions linked to your ACs. Why: general praise gives no guidance for revision.
- Review check fails: add the three headings and enough bullets. Remove invented AC IDs. Why: the grader checks review structure and links.
- AI unavailable or account limit reached: review the same cases yourself. Write REVIEW.md by hand. Required points check the files, not the provider.
- Want the second-review bonus: do it now. Save REVIEW2.md in the same format and
  add a second dated block under Changes after review before Part 3. Why: the spec becomes read-only in Part 3.

## Part 3 - Freeze the reviewed spec (5 minutes)

Freeze the reviewed spec before writing tests or app code.
review_applied compares your draft checkpoint with your frozen spec, so the draft
must already be saved (Part 1). Your revision must name an AC under Changes after review.

What it is:

- A short shell script included in this repository.
- Written by us; not a standard tool you install.
- A helper that saves a git commit and gives it a git tag.

What it does:

- Checks the order: spec before tests before code.
- Runs tests for the failing-test checkpoint and refuses unless all fail.
- Saves a commit and tag; writes SPEC.lock for the reviewed spec and tests.

Why:

- The grader needs proof of the spec, tests, code order.
- A commit can be rewritten, so the script saves a spec fingerprint too.
- The agent must not change the requirements to make its code pass.

Full box: Part 1.

```bash
./freeze.sh
bash check.sh
```

Files created: SPEC.lock and the reviewed spec checkpoint. The script prints `Froze the reviewed spec: spec-frozen at <sha>.`
Checks: `review_applied` (2), `spec_frozen` (1).
Running ./freeze.sh again without file changes prints `Already saved spec-frozen at <sha>; nothing to do.`

Troubleshooting:

- Review-applied fails: make a real AC clarification after the saved draft and record
  it under Changes after review. Changes only to spaces, tabs, or line breaks do not count.
- Spec changed after this step: see Part 6, "Starting a fresh reviewed attempt".
  Keep the old folder as your backup; redo the review and checkpoints in order.
- Checkpoint command reports missing setup: return to `bash init.sh` in Part 0.

## Part 4 — Write tests and watch them fail (45 minutes)

Create tests/test_spec.py. A test calls the app and uses `assert` to check its result.
Use the supplied `client` argument: it calls the app without a running server and
starts each test with empty notes. Write one `def test_ac_NN_description(client):` per AC, using two digits in the test name.
Each `test_ac_NN_...` function needs an `assert` and a call through `client`.
Why: these names and checks let the grader match tests to ACs. Either may be in the test or a helper it calls directly.
Name that helper's parameter `client`. Why: the grader recognizes app calls through this name.
The grader follows one helper level only. You may store a request path in a named value.
You do not need to write the path text directly in each test.

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
Do not add the ping route or test to your notes lab. Why: ping is outside the notes brief.

For your notes tests, run:

```bash
uv run --offline --frozen --no-sync pytest -q tests/test_spec.py
bash check.sh
# Read results/report.json: check ac_test_map, tests_pass_correct, and tests_catch_wrong before saving.
./freeze.sh --red
bash check.sh
```

Files created: tests/test_spec.py, updated SPEC.lock, and the failing-test checkpoint.
Checks: `ac_test_map` (2), `red_evidence` (2).
Every test must fail on the starting app: **zero passed, no collection errors**.
A collection error means pytest cannot load tests. Why: failures must show missing behavior, not invalid test files.
The checkpoint command prints failing tests and `Saved failing-test checkpoint tests-red at <sha>.` when ready.
The grader also tries your tests on one correct app and four deliberately wrong apps.
Why: tests must accept correct behavior and detect mistakes.
A page-content test can keep `tests_pass_correct` failing until Part 5 creates
your page: these test apps use your HTML file. Do not weaken that valid page test.

Troubleshooting:

- A missing-ID test passes: the blank app already returns 404. First create a note
  and assert success, then try the missing or already deleted ID.
- Any test passes: check a missing behaviour from its AC before saving the checkpoint.
- Collection error: fix Python syntax or imports; use a `client` parameter in each test.
  Leave tests/conftest.py unchanged. Why: this instructor file provides client and resets notes for each test.
- Mapping fails: match each AC with `test_ac_01_...`, `test_ac_02_...`, etc.; include
  an actual assert and a call through client.
- Wrong-app test passes: strengthen API assertions before saving this checkpoint.
  Check status codes, blank titles, deletion twice, and all four response fields.
- tests_catch_wrong looks full but tests_pass_correct fails: ignore the mutant rows until tests_pass_correct passes.
  A mutant is a deliberately wrong app used to check tests. A page test that fails on every app
  because your page does not exist yet makes tests_catch_wrong look full.
  Strengthen API assertions before saving. Why: failing on every app does not prove tests detect specific mistakes.
- tests_pass_correct fails: compare expected API results in your tests with BRIEF.md now. A valid page
  test may wait for HTML in Part 5. Optional page polish is outside these app tests.
- AI unavailable: write the tests by hand. pytest runs without an agent account.

## Part 5 — Let the agent implement (45 minutes)

Superpowers is a Codex plugin with planning, implementation, and testing instructions.
Before you start, check its installation: `bash check_superpowers.sh`. Why: the prompt uses skills this plugin provides.
It is worth 0 points and saves `results/superpowers_check.txt`. A skill is a set of instructions Codex can follow.
Add `--probe` to also ask Codex to name its skills. Why: installed files alone do not prove a session can use them.

Give Codex this prompt after the failing-test checkpoint is saved. TDD means writing
failing tests first, then adding code until they pass.

```text
Implement SPEC.md on the current branch. Follow AGENTS.md.
Use Superpowers writing-plans, executing-plans inline, and test-driven-development.
Inline means in this conversation. Why: these skills guide implementation of the fixed spec.
SPEC.md and tests/test_spec.py are read-only. Why: unchanged requirements and tests prove the code meets the reviewed task.
Run the saved tests first and confirm they fail. Why: failure shows they detect missing behavior.
Write app/main.py and app/static/index.html until the tests pass.
Keep notes in variables outside functions in Python memory. Load Vue 3 from a CDN; no build and no database.
Why: reload must clear notes, and Vue loads directly from an online script.
Do not open grading/impls. Why: instructor apps check tests; they must not become your code.
Put extra modules under app/. Why: this separates your implementation from instructor files.
Describe conflicts in REVIEW.md; never weaken tests. Why: the student must review conflicts without losing saved test evidence.
Run bash check.sh and inspect the reports. Why: reports show earned points and missing work.
Leave submission to me. Why: I must inspect results and decide when to submit.
```

Run the checks and save the implementation. Why: this records your tested code before submission:

```bash
uv run --offline --frozen --no-sync pytest -q tests/test_spec.py
bash check.sh
git add app/
git commit -m "feat: implement reviewed notes specification" -m "Implement the saved acceptance criteria without changing tests. Verified the offline student suite."
```

Files created: app/main.py, app/static/index.html, and a saved implementation commit.
Checks: `tests_green` (1), `grader_api` (2), `ui_static` (1), `tests_pass_correct` (1),
`tests_catch_wrong` (2), `impl_original` (0-point protection check).

Optional: ask a second AI to review the finished change against SPEC.md and AGENTS.md
(code review). Record anything it finds in REVIEW.md. No points depend on it.

Troubleshooting:

- Agent or Superpowers unavailable: implement by hand. All required points remain available.
- Agent edits saved spec or tests: see Part 6, "Starting a fresh reviewed attempt".
  Tell the agent to respect read-only files. Do not hide edits in the checkpoint.
- API check fails: compare methods, statuses, note fields, blank titles, and deletion twice with BRIEF.md.
  Also compare empty initial memory and the health result. Why: these are required API behaviors.
- Static page check fails: serve the page at `/` and use all six double-quoted data-testid values.
  Put v-for on note-item itself and use fetch with `/api/notes`.
  Why: static checks look for these exact labels in double quotes and these page structures.
- `impl_original` fails: write your own code from the brief. Renaming copied instructor
  reference apps (grading/impls, called test oracles in AGENTS.md) does not count as original work.
- Saved tests reveal a mistake: record it in REVIEW.md and see Part 6, "Starting a fresh reviewed attempt".
  Do not rewrite saved tests to make code pass. Why: checkpoints must preserve tests chosen before implementation.

## Part 6 — Check and submit (10 minutes)

check.sh is the lab's definition of done. When all required checks pass, the lab is finished.
Read the results, then submit whatever you completed. Why: reports show earned points and missing work before submission.

```bash
bash check.sh
uv run --offline --frozen --no-sync python grader/gate.py
cat results/report.json results/challenge_report.json
bash submit.sh
```

Files created: results/*.json, submitted branch and checkpoints, and GitHub feedback.
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
  submit.sh automatically fixes report-file conflicts using the copy from GitHub.
  A merge conflict means git cannot combine two file versions automatically.
  Other conflicts stop submit.sh with a file list. Edit each listed file to keep the intended content.
  `git add` it, `git commit`, then rerun `bash submit.sh`. Why: git needs your chosen content before submission can continue.
- A checkpoint is missing: return to its part. Save draft, review, reviewed spec, and failing tests before code.
  If app code exists, see "Starting a fresh reviewed attempt" below. Do not replace saved checkpoints.
  Why: the grader needs proof that specs and tests came before code.
- Network unavailable: keep your local work and reports; rerun submission when connected.

### Starting a fresh reviewed attempt

Keep the old folder as your backup. Clone your own student repository with its history.
Why: you preserve old work and avoid merging unrelated histories at submission.
Repositories made with "Use this template" or Classroom start with one template snapshot commit. The root below is that snapshot.

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

Your repository may include the template history. Its first commit is then the old v1 commit (`1276955`).
LIGHT v2 is this lab's template version. Before replacing files, find the starting snapshot with `git log --reverse --oneline`.
Choose the commit whose message says "template snapshot". Ask the instructor if unsure.
Set `root=<that commit's hash>` instead of using the root command above. Do not use the old v1 root.
Why: the old root has different lab files. Missing local tags print an error; the command deletes existing named tags.
Continue with the commit and init commands. Why: missing tags do not prevent saving the new starting version.

Repeat Part 1 to Part 5 in order. Submit only from this new folder. Why: the course uses your latest submission.
`git rm -r app` removes extra modules an agent added, too. `git tag -d` only deletes LOCAL tags in the new folder.
submit.sh replaces checkpoint tags on GitHub. Why: the grader must use checkpoints from your new attempt.

## Bonus — Optional (outside the 175 minutes)

```bash
bash check.sh
cat results/challenge_report.json
```

Files created: optional tests, REVIEW2.md, or vercel_url.txt, plus bonus report.
Checks: `ui_behaviour` (2), `edge_case_tests` (1), `review_round2` (1), `deployed` (2).
Total: **6 bonus points**. TODO does not reduce required points.

- B1: browser interaction checks creating, validation, and deletion. Playwright is
  the browser test tool; CI prepares it when available.
- B2: before Part 4's checkpoint, add at least one `test_ac_NN_edge_...` test.
  Or reference that test's AC in an Edge cases bullet. Why: this links an unusual case to a saved test before implementation.
- B3: before you freeze the reviewed spec, do a second review (REVIEW2.md, same headings, two AC IDs).
  Add a second `### YYYY-MM-DD` block under Changes after review.
  Why: the second review must improve the spec before it becomes read-only; dated blocks record the rounds.
- B4: deploy with Vercel's Python/FastAPI support. Deployment means putting your app online; Vercel is the hosting service.
  Include SPEC.lock, and save your HTTPS URL in vercel_url.txt. An HTTPS URL is a web address starting with https://.
  Why: SPEC.lock supplies the health fingerprint, and vercel_url.txt tells the grader which app to check.
  No deployment account is required for the main lab.

Troubleshooting:

- Browser or CDN unavailable: B1 stays TODO; required static checks still run offline.
- Deployment unreachable: B4 stays TODO. Check its URL and `/api/health`, then retry.
- Deployment health differs from local: include the saved SPEC.lock and redeploy.
- Bonus needs a spec or test change: plan it before the checkpoints. Keep saved files read-only.
