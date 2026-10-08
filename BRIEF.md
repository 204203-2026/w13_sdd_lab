# Fixed brief: Notes

This brief is the fixed request. Your SPEC.md answers it; do not change this file.

Build a small notes list for one user. The user can create, list, and delete notes
through the API and a Vue 3 page at `/`. Storage must be **in-memory module-level
globals in `app/main.py`**. Importing/reloading that module resets the state.
Do not write notes to files, SQLite, a remote database, or browser storage.

A note has `id`, `title`, `body`, and `created_at`. IDs distinguish live notes;
`created_at` is an ISO 8601 timestamp string. A new app starts with an empty list.
Valid POST requests return 201 and all four fields. GET returns a JSON list of
notes. DELETE returns 204 with no body; a missing/deleted ID returns 404.
An empty or whitespace-only title is invalid and returns 422 without adding a note.
An empty body is valid. Required input fields are `title` and `body` strings.
`GET /api/health` returns exactly `{"status":"ok","spec":"<frozen hash>"}`;
read `spec_sha256` from root `SPEC.lock` **at request time**.

Example (with `json` and `Path` imported):

```python
# inside the GET /api/health handler, on every request:
spec = json.loads(Path("SPEC.lock").read_text(encoding="utf-8"))["spec_sha256"]
return {"status": "ok", "spec": spec}
```

Locked names/methods/statuses/selectors are in `grading/CONTRACT.md` and
`grading/contract.json`. Do not rename them or change pinned instructor files.
The UI has a form, a title input, a notes list with repeated note items, a delete
control, and a visible validation error. Use the six locked `data-testid` values.
Use `v-for` on the element carrying `note-item` and `fetch('/api/notes', ...)`.
Serve `app/static/index.html` through FastAPI.
Use Vue 3 via a CDN script (the global build, `vue.global.js`), no build.

The grader's reference app keeps valid titles exactly as sent (no trimming), lists notes
in creation order, allows duplicate titles, has no title length limit, and returns 404 for
any unknown ID, including a non-numeric one. Your tests must pass on it, so specify these
behaviours or leave them unspecified; do not specify a different policy. You decide how
the page shows and clears the validation error, what an empty list looks like, and small optional page polish. Keep the required behaviour small.

Your SPEC.md uses Goal, Acceptance criteria, Edge cases, and Out of scope.
The API above is already fixed; you do not need to design it again or write a
separate API table. Write at least five checkable AC sentences. Describe unusual
inputs as Edge cases bullets. Accounts, sharing, editing, persistence, and
attachments are sensible Out of scope bullets.
