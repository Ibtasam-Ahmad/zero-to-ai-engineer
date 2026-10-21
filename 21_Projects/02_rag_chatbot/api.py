"""FastAPI server for the RAG chatbot."""

import io
import uuid
from typing import List, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import main as rag

app = FastAPI(title="RAG Chatbot API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class SourceDoc(BaseModel):
    text: str
    source: str
    distance: float


class ChatResponse(BaseModel):
    response: str
    session_id: str
    sources: List[SourceDoc]


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    try:
        response, chunks = rag.chat(session_id, req.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "response":   response,
        "session_id": session_id,
        "sources":    chunks,
    }


@app.post("/upload-doc")
async def upload_doc(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")
    path = f"./docs/{file.filename}"
    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)
    # Re-ingest this file
    chunks_added = rag.ingest_documents("./docs")
    return {"filename": file.filename, "chunks_ingested": chunks_added}


@app.get("/sessions")
def sessions():
    return {"sessions": rag.list_sessions()}


@app.delete("/session/{session_id}")
def delete_session(session_id: str):
    ok = rag.delete_session(session_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"deleted": session_id}


@app.websocket("/ws/{session_id}")
async def websocket_chat(ws: WebSocket, session_id: str):
    await ws.accept()
    try:
        while True:
            message = await ws.receive_text()
            response, chunks = rag.chat(session_id, message)
            await ws.send_json({
                "response": response,
                "sources": [{"text": c["text"][:200], "source": c["source"]} for c in chunks],
            })
    except WebSocketDisconnect:
        pass


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)
