from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")
