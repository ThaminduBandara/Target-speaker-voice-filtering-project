from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import urllib.parse
import os
from backend.services.separation_service import OUTPUT_DIR

from backend.services.record_service import record_enroll
from backend.services.embedding_service import extract_embedding
from backend.services.separation_service import run_full_pipeline

app = FastAPI()

# ------------------------------------------------------
# CORS SETTINGS (required for React)
# ------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------
# ROUTES
# ------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Voice Filtering Backend Running 🚀"}


# ------------------------------------------------------
# 1. RECORD ENROLL AUDIO (STEP 1)
# ------------------------------------------------------
@app.post("/record-enroll")
def api_record_enroll():
    path = record_enroll()
    return {"saved": path}


# ------------------------------------------------------
# 2. EXTRACT EMBEDDING (STEP 2)
# ------------------------------------------------------
@app.post("/extract-embedding")
def api_extract_embedding():
    path = extract_embedding()
    return {"embedding": path}


# ------------------------------------------------------
# 3. SEPARATE AUDIO (STEP 3)
# ------------------------------------------------------

# @app.post("/separate")
# def api_separate():
#     mixture_path, clean_path = run_full_pipeline()

#     return {
#         "mixture_url": f"/file?path={urllib.parse.quote(mixture_path)}",
#         "cleaned_url": f"/file?path={urllib.parse.quote(clean_path)}"
#     }

@app.post("/separate")
def api_separate():
    results = run_full_pipeline()

    return {
        "mixture_url": f"/file/{results['mixture']}",
        "cleaned_url": f"/file/{results['cleaned']}"
    }


# @app.post("/separate")
# def api_separate():
#     """
#     run_full_pipeline() now returns:
#     {
#         "mixture": "/path/to/mixture.wav",
#         "cleaned": "/path/to/cleaned.wav"
#     }
#     """

#     results = run_full_pipeline()

#     return {
#         "mixture_url": f"/file?path={results['mixture']}",
#         "cleaned_url": f"/file?path={results['cleaned']}"
#     }


# ------------------------------------------------------
# FILE ENDPOINT — serves audio files for React
# ------------------------------------------------------

@app.get("/file/{filename}")
def get_file(filename: str):
    # Build absolute file path
    path = os.path.join(OUTPUT_DIR, filename)

    print("Requested:", path)

    if not os.path.exists(path):
        return {"error": "File not found"}

    return FileResponse(
        path,
        media_type="audio/wav",
        filename=filename,
               headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }       
    )





# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import FileResponse

# from backend.services.record_service import record_enroll
# from backend.services.embedding_service import extract_embedding
# from backend.services.separation_service import run_full_pipeline

# app = FastAPI()

# # ------------------------------------------------------
# # CORS SETTINGS (required for React)
# # ------------------------------------------------------
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],          # React frontend allowed
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ------------------------------------------------------
# # ROUTES
# # ------------------------------------------------------
# @app.get("/")
# def home():
#     return {"message": "Voice Filtering Backend Running 🚀"}

# @app.post("/record-enroll")
# def api_record_enroll():
#     path = record_enroll()  # backend records clean voice
#     return {"saved": path}

# @app.post("/extract-embedding")
# def api_extract_embedding():
#     path = extract_embedding()  # ECAPA embedding
#     return {"embedding": path}

# @app.post("/separate")
# def api_separate():
#     path = run_full_pipeline()  # record mixture → separate → pick best
#     return FileResponse(path, media_type="audio/wav", filename="clean_voice.wav")

