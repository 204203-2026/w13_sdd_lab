# Instructor-owned notes contract

These names are locked. SPEC.md can clarify edge cases but cannot change this table.

| ID | Request | Required result |
|---|---|---|
| EP-1 | POST /api/notes, JSON title and body | 201; id, title, body, created_at |
| EP-2 | GET /api/notes | 200; JSON list, initially empty |
| EP-3 | DELETE /api/notes/{id} | 204 empty body; missing/deleted, unknown or non-numeric ID 404 |
| EP-4 | POST /api/notes, empty/blank title | 422; no note inserted |
| EP-5 | GET /api/health | 200; status="ok", spec=SPEC.lock.spec_sha256, read at request time |

IDs are int or string identifiers; created_at is an ISO 8601 string. Empty body is
valid. In-memory state resets on module reload. No files or database for notes.

| ID | data-testid value | Element |
|---|---|---|
| UI-1 | note-form | Create form |
| UI-2 | note-title | Title input |
| UI-3 | note-list | List container |
| UI-4 | note-item | Each note, with v-for on this element |
| UI-5 | note-delete | Delete control |
| UI-6 | note-error | Validation error |

Use literal double-quoted `data-testid="value"` attributes. The served `/` page
must contain all six selectors, repeated note markup, and a fetch to /api/notes.
Static checks run without a CDN or browser. Browser interaction is optional bonus.

SPEC.md uses Goal, Acceptance criteria, Edge cases, and Out of scope.
Extra sections are allowed and ignored. Goal must be non-empty. Edge cases and
Out of scope each need at least one non-placeholder bullet.

Write at least five acceptance criteria under Acceptance criteria.
Start each one with `- AC-NN:` and write at least 30 characters after `AC-NN:`.
IDs start at 01 and continue with no gaps and no duplicates.
`AC-1` and `AC-01` count the same. `*` bullets, heading case, trailing colons or spaces, and CRLF are accepted.
Do not leave TODO, lorem, or `<your ...>` in the spec.
Contract tags such as `[EP-1]` are optional; any used EP/UI tag must exist above.
There is no all-IDs coverage requirement or separate spec API-table check.

Each AC has a `test_ac_NN_*` function in tests/test_spec.py, with a two-digit ID.
Each `test_ac_NN_...` function needs an `assert` and a call through `client`. Either
may be in the test itself or in a helper the test calls directly; name that helper's
parameter `client`. The grader follows one helper level only. Path constants are
allowed; literal methods, paths, and testid strings are not required for mapping.
The grader also sends real requests to your app and runs your tests against instructor apps.
REVIEW.md cites at least two distinct existing AC IDs and has Ambiguities,
Missing edge cases, and Verdict headings, with two bullets in the first two.
Changes after review records an AC-linked change. Checkpoints retain the original
review/process evidence requirements.

contract_intact checks that the fixed contract and the instructor files are unchanged.
impl_original checks that app/main.py is your own work, not a renamed copy of an instructor app.
If a protection check fails, these four checks earn zero points: grader_api, ui_static, tests_pass_correct, tests_catch_wrong.
Partial mutant credit is 0.5 for each wrong implementation caught by a failed test;
collection/import errors do not earn mutant credit. Gate requires all 20 points
and all zero-point gates passing. Bonus never controls CI's required gate.
