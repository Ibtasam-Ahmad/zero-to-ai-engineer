"""FastAPI server for the Forecasting Dashboard."""

import io
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

import main as fc

app = FastAPI(title="Forecasting Dashboard API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MIN_POINTS = 40  # the models need enough history (14 lags + an 80/20 split)


class ForecastRequest(BaseModel):
    horizon: int = Field(30, ge=1, le=365)  # 1 to 365 steps ahead
    models: Optional[List[str]] = None
    # Optional: your own series (e.g. the uploaded CSV). If omitted, the sample data is used.
    dates:  Optional[List[str]] = None
    values: Optional[List[float]] = None


def _request_df(req: ForecastRequest) -> pd.DataFrame:
    """Build the DataFrame to forecast: the caller's data if given, else the sample series."""
    if req.values is None:
        return fc.generate_sample_data(365)
    if len(req.values) < MIN_POINTS:
        raise HTTPException(400, f"Need at least {MIN_POINTS} values to forecast, got {len(req.values)}")
    if req.dates is not None and len(req.dates) != len(req.values):
        raise HTTPException(400, "'dates' and 'values' must have the same length")
    if req.dates is not None:
        try:
            ds = pd.to_datetime(req.dates)
        except Exception as e:
            raise HTTPException(400, f"Could not read 'dates': {e}")
    else:
        ds = pd.date_range("2022-01-01", periods=len(req.values), freq="D")
    return pd.DataFrame({"ds": ds, "y": req.values})


@app.get("/sample-data")
def sample_data():
    df = fc.generate_sample_data(365)
    return {
        "dates":  df["ds"].dt.strftime("%Y-%m-%d").tolist(),
        "values": df["y"].round(3).tolist(),
    }


@app.post("/forecast")
def forecast(req: ForecastRequest):
    df = _request_df(req)
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
        # The upload is only validated and echoed back; the dashboard keeps it and
        # sends it with each POST /forecast (dates + values), so the server stays stateless.
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
