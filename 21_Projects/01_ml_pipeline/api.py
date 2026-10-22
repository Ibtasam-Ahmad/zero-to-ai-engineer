"""
FastAPI service for diabetes prediction model.
Endpoints: POST /predict, GET /health, GET /model-info
"""

import os
from typing import Dict, List, Optional

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Diabetes Prediction API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MODEL_PATH = "models/best_model.joblib"
META_PATH  = "models/model_meta.joblib"

_model = None
_meta  = None


def get_model():
    global _model, _meta
    if _model is None or _meta is None:
        if not (os.path.exists(MODEL_PATH) and os.path.exists(META_PATH)):
            raise HTTPException(status_code=503, detail="Model not found. Run main.py first.")
        model, meta = joblib.load(MODEL_PATH), joblib.load(META_PATH)  # only keep them if BOTH load
        _model, _meta = model, meta
    return _model, _meta


class PredictRequest(BaseModel):
    # The dataset is standardised (values about -0.14 to 0.20); ge/le reject raw numbers like age=50
    age:  float = Field(..., ge=-0.5, le=0.5, description="Age (normalized)", example=0.038)
    sex:  float = Field(..., ge=-0.5, le=0.5, description="Sex (normalized)", example=0.050)
    bmi:  float = Field(..., ge=-0.5, le=0.5, description="BMI (normalized)", example=0.062)
    bp:   float = Field(..., ge=-0.5, le=0.5, description="Blood pressure (normalized)", example=-0.025)
    s1:   float = Field(..., ge=-0.5, le=0.5, description="Serum measurement 1", example=-0.044)
    s2:   float = Field(..., ge=-0.5, le=0.5, description="Serum measurement 2", example=-0.034)
    s3:   float = Field(..., ge=-0.5, le=0.5, description="Serum measurement 3", example=-0.043)
    s4:   float = Field(..., ge=-0.5, le=0.5, description="Serum measurement 4", example=-0.002)
    s5:   float = Field(..., ge=-0.5, le=0.5, description="Serum measurement 5", example=0.019)
    s6:   float = Field(..., ge=-0.5, le=0.5, description="Serum measurement 6", example=-0.017)


class PredictResponse(BaseModel):
    prediction: float
    model_config = ConfigDict(protected_namespaces=())  # allow field names starting with "model_"
    prediction_lower: Optional[float]   # None for old model files without interval info
    prediction_upper: Optional[float]
    interval_level: Optional[float]     # 0.9 = 90% prediction interval
    model_used: str
    features_received: Dict[str, float]


class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    status: str
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_name: str
    metrics: Dict[str, float]
    feature_names: List[str]
    all_results: Dict


@app.get("/health", response_model=HealthResponse)
def health():
    try:
        get_model()
        return {"status": "ok", "model_loaded": True}
    except Exception:
        return {"status": "ok", "model_loaded": False}


@app.get("/model-info", response_model=ModelInfoResponse)
def model_info():
    _, meta = get_model()
    return {
        "model_name":    meta["best_model"],
        "metrics":       meta["metrics"],
        "feature_names": meta["feature_names"],
        "all_results":   meta["all_results"],
    }


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    model, meta = get_model()
    X = pd.DataFrame([req.dict()], columns=meta["feature_names"])  # same column names as in training
    pred = float(model.predict(X)[0])
    interval = meta.get("interval")  # offsets from cross-validated residuals (replaces the made-up ±10%)
    return {
        "prediction":       round(pred, 2),
        "prediction_lower": round(pred + interval["lower_offset"], 2) if interval else None,
        "prediction_upper": round(pred + interval["upper_offset"], 2) if interval else None,
        "interval_level":   interval["level"] if interval else None,
        "model_used":       meta["best_model"],
        "features_received": req.dict(),
    }


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
