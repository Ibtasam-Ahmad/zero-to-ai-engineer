"""Production FastAPI service for sentiment classification."""

import time
import uuid
from typing import Annotated, List, Optional

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

import main as model_module
import monitoring

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Sentiment Analysis API Production", version="1.0.0")
app.state.limiter = limiter
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    print(f"{request.method} {request.url.path} {response.status_code} {duration:.1f}ms")
    return response


class PredictRequest(BaseModel):
    text:          str = Field(..., min_length=1, max_length=10000)
    model_version: Optional[str] = Field("baseline", pattern="^(baseline|bert)$")


class PredictResponse(BaseModel):
    request_id:    str
    text_preview:  str
    label:         str
    confidence:    float
    model_version: str
    inference_ms:  float


class BatchRequest(BaseModel):
    # 1-50 texts, each 1-10000 characters; same model_version rule as /predict
    texts:         List[Annotated[str, Field(min_length=1, max_length=10000)]] = Field(..., min_length=1, max_length=50)
    model_version: Optional[str] = Field("baseline", pattern="^(baseline|bert)$")


@app.post("/predict", response_model=PredictResponse)
@limiter.limit("60/minute")
def predict(request: Request, req: PredictRequest):
    try:
        result = model_module.predict(req.text, req.model_version)
    except FileNotFoundError:
        raise HTTPException(503, "Model not found run python main.py to train first")
    request_id = str(uuid.uuid4())[:8]  # one id, used in the response AND the prediction log
    monitoring.log_prediction(req.text, result, request_id)
    return {
        "request_id":    request_id,
        "text_preview":  req.text[:100] + ("..." if len(req.text) > 100 else ""),
        **result,
    }


@app.post("/predict/batch")
@limiter.limit("20/minute")
def predict_batch(request: Request, req: BatchRequest):
    results = []
    for text in req.texts:
        try:
            result = model_module.predict(text, req.model_version)
        except FileNotFoundError:
            raise HTTPException(503, "Model not found run python main.py to train first")
        request_id = str(uuid.uuid4())[:8]
        monitoring.log_prediction(text, result, request_id)
        results.append({"request_id": request_id, "text_preview": text[:60], **result})
    return {"count": len(results), "results": results}


@app.get("/health")
def health():
    model_ok = True
    try:
        import os
        if not os.path.exists(model_module.BASELINE_PATH):
            model_ok = False
    except Exception:
        model_ok = False
    return {"status": "ok" if model_ok else "degraded", "model_loaded": model_ok}


@app.get("/model-info")
def model_info():
    return {
        "available_models": ["baseline", "bert"],
        "baseline": "TF-IDF + Logistic Regression",
        "bert":     "Fine-tuned DistilBERT (if trained)",
        "labels":   model_module.LABELS,
    }


@app.get("/metrics")
def metrics():
    summary = monitoring.get_metrics_summary()
    drift   = monitoring.check_drift()
    prom_bytes, _ = monitoring.get_prometheus_metrics()
    return {"summary": summary, "drift": drift, "prometheus_available": monitoring.PROMETHEUS_AVAILABLE}


@app.get("/metrics/prometheus")
def prometheus_metrics():
    data, content_type = monitoring.get_prometheus_metrics()
    return Response(content=data, media_type=content_type)


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8005, reload=False)
