Review SPEC.md using BRIEF.md and grading/CONTRACT.md. Help a second-year student
find small holes before writing tests. Do not implement the app or change the API.
Order: brief -> spec -> AI review -> tests -> code. The student saves a draft checkpoint
before this review, then freezes the reviewed spec after revising it.
Compare the brief and the spec: list what the brief asks that the spec lacks, and what the spec adds that nobody asked.

Read the four parts: Goal, Acceptance criteria, Edge cases, Out of scope.
Extra sections are allowed. Look for unclear wording, missing inputs, conflicting
results, and sentences that cannot be checked with a test. Cite at least two
different existing AC IDs. Do not invent IDs or guess missing requirements.

Return Markdown that can be saved as REVIEW.md with these headings:

## Ambiguities
Give at least two bullets. Cite the affected AC ID and suggest clearer wording.

## Missing edge cases
Give at least two bullets. Cite the affected AC ID and suggest an unusual input
and the result a test should check.

## Verdict
Say whether the spec is ready to freeze and which small changes come first.

The student will revise the spec and record AC-linked changes in Changes after review.
Review only; leave the student's files unchanged.

Use plain straight quotes only; avoid typographic quotation marks.
