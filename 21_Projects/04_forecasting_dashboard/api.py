"""FastAPI server for the Forecasting Dashboard."""

import io
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

import main as fc

app = FastAPI(title="Forecasting Dashboard API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ForecastRequest(BaseModel):
    horizon: int = 30
    models: Optional[List[str]] = None


@app.get("/sample-data")
def sample_data():
    df = fc.generate_sample_data(365)
    return {
        "dates":  df["ds"].dt.strftime("%Y-%m-%d").tolist(),
        "values": df["y"].round(3).tolist(),
    }


@app.post("/forecast")
def forecast(req: ForecastRequest):
    df = fc.generate_sample_data(365)
    results = fc.run_forecast(df, horizon=req.horizon, models=req.models)
    return {"horizon": req.horizon, "results": results}


@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    content = await file.read()
    try:
        df = pd.read_csv(io.StringIO(content.decode()))
        if "ds" not in df.columns or "y" not in df.columns:
            raise ValueError("CSV must have 'ds' (date) and 'y' (value) columns")
        df["ds"] = pd.to_datetime(df["ds"])
        return {
            "rows":   len(df),
            "dates":  df["ds"].dt.strftime("%Y-%m-%d").tolist(),
            "values": df["y"].round(3).tolist(),
        }
    except Exception as e:
        raise HTTPException(400, str(e))


@app.get("/models")
def list_models():
    return {"models": ["arima", "prophet", "xgboost", "lstm"]}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index():
    with open("templates/index.html") as f:
        return f.read()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8003, reload=True)
