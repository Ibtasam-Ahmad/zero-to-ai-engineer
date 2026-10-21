"""FastAPI server for the Computer Vision app."""

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

import main as cv

app = FastAPI(title="Computer Vision API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def check_image(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: {file.content_type}")


@app.post("/classify")
async def classify(file: UploadFile = File(...), top_k: int = 5):
    check_image(file)
    data = await file.read()
    try:
        results = cv.classify(data, top_k=top_k)
        return {"filename": file.filename, "predictions": results}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    check_image(file)
    data = await file.read()
    try:
        boxes = cv.detect(data)
        return {"filename": file.filename, "detections": boxes}
    except Exception as e:
        raise HTTPException(500, str(e))


@app.post("/segment")
async def segment(file: UploadFile = File(...)):
    check_image(file)
    data = await file.read()
    try:
        result = cv.segment(data)
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
