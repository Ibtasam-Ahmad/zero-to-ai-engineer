"""FastAPI server for the Computer Vision app."""

import io

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from PIL import Image, UnidentifiedImageError

import main as cv

app = FastAPI(title="Computer Vision API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def check_image(file: UploadFile) -> bytes:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: {file.content_type}")
    data = file.file.read()
    try:  # the content type is only what the client claims: check the bytes too
        Image.open(io.BytesIO(data)).verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(400, "The file is not a readable image")
    return data


# Plain `def` endpoints: FastAPI runs them in worker threads, so slow inference does not block the server


@app.post("/classify")
def classify(file: UploadFile = File(...), top_k: int = Query(5, ge=1, le=20)):
    data = check_image(file)
    try:
        results = cv.classify(data, top_k=top_k)
        return {"filename": file.filename, "predictions": results}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/detect")
def detect(file: UploadFile = File(...)):
    data = check_image(file)
    try:
        result = cv.detect(data)
        return {"filename": file.filename, **result}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/segment")
def segment(file: UploadFile = File(...), mode: str = Query("objects", pattern="^(objects|everything)$")):
    data = check_image(file)
    try:
        result = cv.segment(data, mode=mode)
        return {"filename": file.filename, **result}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8002, reload=True)
