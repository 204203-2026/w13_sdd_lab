"""Instructor test oracle: in-memory notes app."""
from datetime import datetime, timezone
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator

app = FastAPI()
notes = {}
next_id = 1

class NoteInput(BaseModel):
    title: str
    body: str

    @field_validator("title")
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError("Title must not be blank")
        return value

@app.get("/")
def index():
    return FileResponse(Path("app/static/index.html"))

@app.post("/api/notes", status_code=201)
def create(payload: NoteInput):
    global next_id
    note = {"id": next_id, "title": payload.title, "body": payload.body,
            "created_at": datetime.now(timezone.utc).isoformat()}
    notes[next_id] = note
    next_id += 1
    return note

@app.get("/api/notes")
def listing():
    return list(notes.values())

@app.delete("/api/notes/{note_id}", status_code=204)
def delete(note_id: str):
    key = int(note_id) if note_id.isdigit() else None
    if key not in notes:
        raise HTTPException(404, "Note not found")
    del notes[key]
    return Response(status_code=204)

@app.get("/api/health")
def health():
    return {"status": "ok", "spec": json.loads(Path("SPEC.lock").read_text())["spec_sha256"]}
