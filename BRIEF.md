# Fixed brief: Notes

This brief is the fixed request. Your SPEC.md answers it; do not change this file.
Why: changing this file cannot change what the grader checks.

Build a small notes list for one user. The user can create, list, and delete notes
through the API and a Vue 3 page at `/`. Use **in-memory module-level globals in `app/main.py`**.
These are variables outside functions; data exists only in Python memory. A module is a Python file.
Loading this module, or loading it again, must clear notes.
Do not write notes to files, SQLite, a remote database, or browser storage.
Why: tests reload the app to start with empty notes.

A note has `id`, `title`, `body`, and `created_at`. IDs distinguish live notes;
`created_at` is text containing a date and time in ISO 8601 format. A new app starts with an empty list.
A status code is a number describing a request result. POST creates a note; valid requests return 201 and all four fields.
201 means the app created the note.
JSON is text data with lists and named values. GET reads notes and returns a JSON list.
DELETE removes a note and returns 204 with no response content. A missing or deleted ID returns 404: not found.
An empty title or a title containing only spaces, tabs, or newlines is invalid.
It returns 422, meaning invalid input, without adding a note.
An empty body is valid. Required input fields are `title` and `body` strings.
`GET /api/health` returns exactly `{"status":"ok","spec":"<frozen hash>"}`;
read `spec_sha256` from `SPEC.lock` in the main lab folder **at request time**.
Why: reading it on every request shows the fingerprint currently saved in the file.

Example (with `json` and `Path` imported):

```python
# inside the GET /api/health handler, on every request:
spec = json.loads(Path("SPEC.lock").read_text(encoding="utf-8"))["spec_sha256"]
return {"status": "ok", "spec": spec}
```

`grading/CONTRACT.md` and `grading/contract.json` list fixed names, methods, status codes, and selectors.
Keep these and protected instructor files unchanged. Why: the grader uses them to check every student's work consistently.
The UI (user interface) is the page users see and use.
It has a form, a title input, a notes list, and repeated note items.
It also has a delete control and a visible validation error.
Use the six fixed `data-testid` values. Use `v-for` on the element carrying `note-item` and `fetch('/api/notes', ...)`.
v-for repeats an element for each list item. Why: page checks use these labels and expect note-item itself to repeat.
Serve `app/static/index.html` through FastAPI, the Python library that handles app requests.
Why: the grader requests the page from your app. Load Vue 3 from a CDN using the global build, `vue.global.js`.
Do not use a JavaScript build tool. Why: this script loads Vue directly in the browser.

The grader's reference app keeps valid titles exactly as sent, including spaces at the ends.
It lists notes in creation order. It allows duplicate titles and has no title length limit.
It returns 404 for any unknown ID, including a non-numeric one.
Specify these behaviors or leave them unspecified. Why: your tests must pass on this correct app.
You choose how the page shows and clears errors, and how an empty list looks. Small appearance improvements are optional.
Keep required behavior small. Why: extra features take time without earning required points.

Your SPEC.md uses Goal, Acceptance criteria, Edge cases, and Out of scope.
The API above is fixed. You do not need to design it again or write a separate API table. Write at least five checkable AC sentences. Describe unusual
inputs as Edge cases bullets. Accounts, sharing, editing, persistence, and
attachments are useful Out of scope bullets. Persistence means keeping notes after the app restarts.
Why: these sections record required results, unusual inputs, and features you will not build.
