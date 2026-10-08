Review SPEC.md using BRIEF.md and grading/CONTRACT.md. Help a second-year student
find unclear or missing requirements before writing tests. Do not implement the app or change the API.
Why: review clarifies the fixed task before tests and code.
Order: brief -> spec -> AI review -> tests -> code. The student saves a draft checkpoint
before this review, then freezes the reviewed spec after revising it.
Compare the brief with the spec. List missing requirements and features the spec adds without a request.

Read the four parts: Goal, Acceptance criteria, Edge cases, Out of scope.
Extra sections are allowed. Look for unclear wording, missing inputs, conflicting
results, and sentences that cannot be checked with a test. Cite at least two
different existing AC IDs. Do not invent IDs or guess missing requirements.
Why: comments linked to existing ACs help the student make specific revisions.

Return Markdown that can be saved as REVIEW.md with these headings. Why: the grader checks these parts of the review:

## Ambiguities
Give at least two bullets. Cite the affected AC ID and suggest clearer wording. Why: several comments check more than one issue.

## Missing edge cases
Give at least two bullets. Cite the affected AC ID and suggest an unusual input
and the result a test should check. Why: concrete cases help the student write useful tests.

## Verdict
Say whether the spec is ready to freeze and which small changes come first. Why: the student needs a clear decision.

The student will revise the spec and record AC-linked changes in Changes after review.
Review only; leave the student's files unchanged. Why: the student decides which advice to apply.

Use plain straight quotes only. Why: students must be able to copy code examples without changing quote characters.
