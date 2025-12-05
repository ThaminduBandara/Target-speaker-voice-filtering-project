from fastapi import FastAPI
from fastapi.responses import FileResponse

from backend.services.record_service import record_enroll
from backend.services.embedding_service import extract_embedding
from backend.services.separation_service import run_full_pipeline

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Voice Filtering Backend Running 🚀"}

@app.post("/record-enroll")
def api_record_enroll():
    path = record_enroll()
    return {"saved": path}

@app.post("/extract-embedding")
def api_extract_embedding():
    path = extract_embedding()
    return {"embedding": path}

@app.post("/separate")
def api_separate():
    path = run_full_pipeline()
    return FileResponse(path, media_type="audio/wav")
