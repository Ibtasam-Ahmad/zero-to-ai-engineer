"""FastAPI server for the multi-agent research system."""

import asyncio
import uuid
from typing import Dict, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from graph import run_pipeline

app = FastAPI(title="Multi-Agent Research API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

_tasks: Dict[str, Dict] = {}


class ResearchRequest(BaseModel):
    topic: str


@app.post("/research")
def start_research(req: ResearchRequest):
    task_id = str(uuid.uuid4())
    _tasks[task_id] = {"status": "pending", "topic": req.topic, "log": [], "report": None}

    async def _run():
        _tasks[task_id]["status"] = "running"
        try:
            result = await asyncio.to_thread(run_pipeline, req.topic)
            _tasks[task_id]["status"]  = "complete"
            _tasks[task_id]["log"]     = result.get("log", [])
            _tasks[task_id]["report"]  = result.get("final_report", "")
        except Exception as e:
            _tasks[task_id]["status"] = "error"
            _tasks[task_id]["error"]  = str(e)

    asyncio.create_task(_run())
    return {"task_id": task_id, "topic": req.topic}


@app.get("/task/{task_id}")
def get_task(task_id: str):
    t = _tasks.get(task_id)
    if not t:
        from fastapi import HTTPException
        raise HTTPException(404, "Task not found")
    return {
        "task_id": task_id,
        "status":  t["status"],
        "topic":   t["topic"],
        "log":     t["log"],
        "partial": t.get("report", "")[:500] if t.get("report") else "",
    }


@app.get("/report/{task_id}")
def get_report(task_id: str):
    t = _tasks.get(task_id)
    if not t:
        from fastapi import HTTPException
        raise HTTPException(404, "Task not found")
    return {"task_id": task_id, "status": t["status"], "report": t.get("report", "")}


@app.websocket("/ws/{task_id}")
async def ws_progress(ws: WebSocket, task_id: str):
    await ws.accept()
    try:
        prev_log_len = 0
        while True:
            t = _tasks.get(task_id, {})
            log = t.get("log", [])
            if len(log) > prev_log_len:
                for entry in log[prev_log_len:]:
                    await ws.send_json({"type": "log", "message": entry})
                prev_log_len = len(log)
            if t.get("status") in ("complete", "error"):
                await ws.send_json({"type": "done", "status": t["status"], "report": t.get("report", "")})
                break
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass


@app.get("/health")
def health():
    return {"status": "ok", "active_tasks": len(_tasks)}


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8004, reload=False)
