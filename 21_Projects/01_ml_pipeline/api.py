"""
FastAPI service for diabetes prediction model.
Endpoints: POST /predict, GET /health, GET /model-info
"""

import os
from typing import Dict, List, Optional

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI(title="Diabetes Prediction API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MODEL_PATH = "models/best_model.joblib"
META_PATH  = "models/model_meta.joblib"

_model = None
_meta  = None


def get_model():
    global _model, _meta
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(status_code=503, detail="Model not found. Run main.py first.")
        _model = joblib.load(MODEL_PATH)
        _meta  = joblib.load(META_PATH)
    return _model, _meta


class PredictRequest(BaseModel):
    age:  float = Field(..., description="Age (normalized)", example=0.038)
    sex:  float = Field(..., description="Sex (normalized)", example=0.050)
    bmi:  float = Field(..., description="BMI (normalized)", example=0.062)
    bp:   float = Field(..., description="Blood pressure (normalized)", example=-0.025)
    s1:   float = Field(..., description="Serum measurement 1", example=-0.044)
    s2:   float = Field(..., description="Serum measurement 2", example=-0.034)
    s3:   float = Field(..., description="Serum measurement 3", example=-0.043)
    s4:   float = Field(..., description="Serum measurement 4", example=-0.002)
    s5:   float = Field(..., description="Serum measurement 5", example=0.019)
    s6:   float = Field(..., description="Serum measurement 6", example=-0.017)


class PredictResponse(BaseModel):
    prediction: float
    prediction_lower: float
    prediction_upper: float
    model_used: str
    features_received: Dict[str, float]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool


class ModelInfoResponse(BaseModel):
    model_name: str
    metrics: Dict[str, float]
    feature_names: List[str]
    all_results: Dict


@app.get("/health", response_model=HealthResponse)
def health():
    try:
        get_model()
        return {"status": "ok", "model_loaded": True}
    except HTTPException:
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
    features = [req.age, req.sex, req.bmi, req.bp, req.s1, req.s2, req.s3, req.s4, req.s5, req.s6]
    X = np.array(features).reshape(1, -1)
    pred = float(model.predict(X)[0])
    margin = pred * 0.10  # ±10% confidence band
    return {
        "prediction":       round(pred, 2),
        "prediction_lower": round(pred - margin, 2),
        "prediction_upper": round(pred + margin, 2),
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
