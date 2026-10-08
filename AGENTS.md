# Week 13 implementation agent rules

## Read-only files

A checkpoint is a saved snapshot. SPEC.md is read-only after you freeze the reviewed spec (`spec-frozen`).
tests/test_spec.py is read-only after the failing-test checkpoint (`tests-red`). Do not change either to make code pass.
Why: saved requirements and tests prove that you chose expected behavior before implementation.

- tests/conftest.py, grading/contract.json, grading/contract.sha256, and
  grading/impls/*.py belong to the instructor and are always read-only.
- grader/, check.sh, freeze.sh, submit.sh and .github/ also belong to the instructor.
  Why: instructor files keep checks consistent for all students.
- Do not open or read grading/impls/*.py. These are test oracles (apps used to check
  the tests), not starter code. Never copy them into app/main.py. Why: the grader requires your own implementation.
- Propose spec or test corrections in REVIEW.md. If frozen tests conflict with
  the contract, explain the conflict. Wait for a student to start a new reviewed attempt.
  Do not weaken checks or move existing checkpoint tags. Why: existing checkpoints preserve the original review and test evidence.

## Implementation workflow

Read BRIEF.md, SPEC.md, and grading/CONTRACT.md. The spec uses Goal, Acceptance
criteria, Edge cases, and Out of scope. Extra sections are allowed. BRIEF.md fixes
the API; do not redesign it or demand extra spec sections or contract tags. Why: the brief fixes required behavior.
Order: brief -> spec -> AI review -> tests -> code. Save the draft checkpoint (`spec-draft`) before AI review.
Freeze the reviewed spec (`spec-frozen`) after review. Save the failing-test checkpoint (`tests-red`) before code. Why: the grader checks this order.

Use Superpowers `writing-plans` to plan implementation only, then `executing-plans` inline and `test-driven-development`.
Inline means in the current conversation. Why: these skills guide implementation and testing of the fixed spec.
Run the frozen tests and see them fail before coding. Why: failure shows that tests detect missing behavior.
Work on the current branch. Why: submission sends this branch and its checkpoints.
Write app/main.py and app/static/index.html; put any extra implementation module under app/.
Why: this keeps your code separate from instructor files. Module-level in-memory state means variables outside functions, stored in Python memory.
It must reset on importlib.reload. Do not add a database or note files. Why: tests reload the app for empty notes.

Run `uv run --offline --frozen --no-sync pytest -q tests/test_spec.py` after changes.
Run `bash check.sh`, inspect both reports, and run `uv run --offline --frozen --no-sync python grader/gate.py` before
finishing. Why: reports show earned points, and the gate checks required completion.
Required total is 20; bonus total is 6. Bonus TODO does not block completion.
Leave submission to the student. Why: the student must inspect results and decide when to send work.

## Commits

Use Conventional Commits: a short subject starting with type: and an action verb. Add a body explaining why and what you verified.
Why: this format records the change, its reason, and its checks. freeze.sh creates its specified `freeze: <stage>` snapshots.
Keep the failing-test checkpoint (`tests-red`) before implementation. Why: it proves tests failed before code.
submit.sh sends the branch and checkpoints.
