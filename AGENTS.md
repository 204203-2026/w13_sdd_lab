# Week 13 implementation agent rules

## Read-only files

A checkpoint is a saved snapshot. SPEC.md is read-only after you freeze the reviewed spec (`spec-frozen`). tests/test_spec.py is read-only after the failing-test checkpoint
(`tests-red`). Do not change either to make code pass.

- tests/conftest.py, grading/contract.json, grading/contract.sha256, and
  grading/impls/*.py belong to the instructor and are always read-only.
- grader/, check.sh, freeze.sh, submit.sh and .github/ also belong to the instructor.
- Do not open or read grading/impls/*.py. These are test oracles (apps used to check
  the tests), not starter code. Never copy them into app/main.py.
- Propose spec or test corrections in REVIEW.md. If frozen tests conflict with
  the contract, explain the conflict and wait for a student to start a new reviewed
  attempt. Do not weaken checks or move existing checkpoint tags.

## Implementation workflow

Read BRIEF.md, SPEC.md, and grading/CONTRACT.md. The spec uses Goal, Acceptance
criteria, Edge cases, and Out of scope. Extra sections are allowed. BRIEF.md fixes
the API; do not redesign it or demand extra spec sections or contract tags.
Order: brief -> spec -> AI review -> tests -> code. Save the draft checkpoint
(`spec-draft`) before AI review; freeze the reviewed spec (`spec-frozen`) after
review, then save the failing-test checkpoint (`tests-red`) before code.

Use Superpowers writing-plans to plan implementation only, then executing-plans
inline and test-driven-development. Run the frozen tests and see them fail before
coding. Work on the current branch. Write app/main.py and app/static/index.html;
put any extra implementation module under app/. Module-level in-memory state
must reset on importlib.reload. Do not add a database or note files.

Run `uv run --offline --frozen --no-sync pytest -q tests/test_spec.py` after changes.
Run `bash check.sh`, inspect both reports, and run `uv run --offline --frozen --no-sync python grader/gate.py` before
finishing. Required total is 20; bonus total is 6. Bonus TODO does not block completion.
Leave submission to the student.

## Commits

Use Conventional Commits with a short imperative subject and a body explaining why
and what was verified. freeze.sh creates its specified `freeze: <stage>` snapshots.
Keep the failing-test checkpoint (`tests-red`) before implementation. submit.sh sends the branch and checkpoints.
