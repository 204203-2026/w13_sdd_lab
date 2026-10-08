# Lab 13 — A small spec, review, and tests

Week 13, 204203-2026.
Released Friday 9 October 2026 after the lecture. Due Friday 16 October 2026, 23:59 (Asia/Bangkok).
About **3 hours (2.5–4 hours)**, plus optional bonus work.

A spec describes what your app must do. An agent is AI that edits files and runs commands.
Order: brief -> spec -> AI review -> tests -> code. BRIEF.md is the fixed request; SPEC.md is your answer.
Write a small SPEC.md. Review it for unclear or missing requirements. Write one test per checkable sentence.
A test checks a result; pytest runs Python tests. Watch tests fail, then let an agent make them pass.
Why: clear requirements guide tests; failing tests show they detect missing features. You can do every step by hand if AI is unavailable.

Teams use different SPEC.md formats. This lab uses **Goal**, **Acceptance criteria**, **Edge cases**, and **Out of scope**.
An acceptance criterion (AC) states a result you can test. Edge cases are unusual inputs or situations.
Out of scope means features you will not build. An API defines requests your app accepts and results it returns.
Keep the notes API in BRIEF.md. Why: the grader checks this fixed API.
A checkpoint is a saved snapshot. A git commit saves files in project history. A git tag names a commit.
The helper scripts (`init.sh`, freeze.sh, check.sh, submit.sh) save commits, tags, and SPEC.lock for you.
A fingerprint is a value calculated from file contents. Never edit SPEC.lock or move a tag.
Save a draft checkpoint before AI review. Freeze the reviewed spec afterwards, then save the failing-test checkpoint before code.
Why: these snapshots and fingerprints let the grader check that requirements and tests came before code.

Read `BRIEF.md`, grading/CONTRACT.md, then `TASKS.md`. Why: this order gives you required behavior and names before the steps. Start here:

```bash
bash init.sh
bash check.sh
cat results/report.json
```

After `bash init.sh`, the fresh template earns **0/20**. Most checks fail because your spec, review, tests, and app are missing. The two checks protecting instructor files
and original work pass. That is the expected starting point.

Required work earns **20 points**. It runs offline after the first setup.
Bonus work earns **6 points**. Browser or deployment failures leave bonus checks
as TODO and do not reduce required points. Python 3.11–3.13, git, and uv are needed.
uv installs and runs Python tools in the lab environment. WSL Ubuntu runs Linux tools inside Windows.
Windows users should use WSL Ubuntu. Why: these scripts need bash and Linux shell commands.
LF is the Linux newline format. Use LF line endings; .gitattributes handles them. Why: this prevents script errors from Windows newlines.
A CDN supplies online files, such as the Vue script. Vue 3 uses a CDN script.
No JavaScript build tool, database, or container is needed.

check.sh is the lab's definition of done. When all required checks pass, the lab is finished.
`bash check.sh` always exits 0: it tells the terminal it finished, even if checks failed.
Read the reports or run `uv run --offline --frozen --no-sync python grader/gate.py`.
Why: this command passes only at 20/20 with both protection checks passing.
CI (the automatic check on GitHub) recomputes feedback on main or master.
After the deadline, the course checks your work again with its saved grader version, grader-v2.
Both automatic workflows give feedback. The instructor uses the saved grader to calculate your official grade.
Editing reports or grader files cannot change it. Partial work still earns its passing checks.
