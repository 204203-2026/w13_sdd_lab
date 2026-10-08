# Lab 13 — A small spec, review, and tests

Week 13, 204203-2026.
Released Friday 9 October 2026 after the lecture. Due Friday 16 October 2026, 23:59 (Asia/Bangkok).
About **3 hours (2.5–4 hours)**, plus optional bonus work.

Order: brief -> spec -> AI review -> tests -> code. BRIEF.md is the fixed request;
SPEC.md is your answer to it. Write a small SPEC.md. Review it for holes. Write one test per checkable sentence.
Watch the tests fail, then let an agent make them pass. You can also do every step
by hand if the agent is unavailable.

There is no single industry-standard SPEC.md format. Teams use different formats.
This lab uses four shared parts: **Goal**, **Acceptance criteria**, **Edge cases**,
and **Out of scope**. The notes API is already fixed in BRIEF.md; do not redesign it.
A checkpoint means a saved snapshot. Run the sheet's commands to save each checkpoint.
The lab's helper scripts (init.sh, freeze.sh, check.sh, submit.sh) make the git commits,
tags and the fingerprint file for you. Never edit SPEC.lock or move a tag.
Save a draft checkpoint before AI review; freeze the reviewed spec afterwards,
then save the failing-test checkpoint before code.

Read BRIEF.md, grading/CONTRACT.md, then TASKS.md. Start here:

```bash
bash init.sh
bash check.sh
cat results/report.json
```

After `bash init.sh`, the fresh template earns **0/20**. Most checks fail because you have not written
the spec, review, tests, or app yet. The two checks protecting instructor files
and original work pass. That is the expected starting point.

Required work earns **20 points**. It runs offline after the first setup.
Bonus work earns **6 points**. Browser or deployment failures leave bonus checks
as TODO and do not reduce required points. Python 3.11–3.13, git, and uv are needed.
Windows users should use WSL Ubuntu. Use LF line endings; .gitattributes handles them.
Vue 3 uses a CDN script; no JavaScript build tool, database, or container is needed.

check.sh is the lab's definition of done: when all required checks pass, the lab is finished.
`bash check.sh` always exits 0. Read the reports or run `uv run --offline --frozen --no-sync python grader/gate.py`:
that command passes only at 20/20 with both protection checks passing.
CI (the automatic check on GitHub) recomputes feedback on main or master.
After the deadline the course re-grades with the saved grader-v2 release.
Both feedback workflows are feedback only; the instructor re-grade with the saved grader is the grade of record. Editing reports or grader files
cannot change it. Partial work still earns its passing checks.
