"""
FastAPI Production Application
Includes: Auth, DB, ML Model Serving, Metrics, Middleware
"""

from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import Response
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import numpy as np
import joblib
import json
import time
import logging

from database import engine, Base, get_db
from models import User, Prediction
from schemas import (
    UserCreate, UserResponse, Token,
    PredictionRequest, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse
)
from auth import (
    verify_password, get_password_hash,
    create_access_token, get_current_user_token
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Shared model registry
ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Load ML model (mock replace with real model)
    ml_models["classifier"] = None  # joblib.load("model.pkl")
    ml_models["scaler"] = None       # joblib.load("scaler.pkl")
    ml_models["version"] = "v1.0.0"
    logger.info("Application started, DB ready")
    yield
    # Shutdown
    ml_models.clear()
    await engine.dispose()
    logger.info("Application shutdown complete")


app = FastAPI(
    title="AI Learning Platform API",
    description="FastAPI app with Auth, DB, and ML serving",
    version="1.0.0",
    lifespan=lifespan
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.1f}ms")
    response.headers["X-Process-Time"] = f"{duration:.1f}ms"
    return response


# --- Health ---
@app.get("/health", tags=["system"])
async def health():
    return {
        "status": "healthy",
        "model_version": ml_models.get("version"),
        "timestamp": time.time()
    }


# --- Auth Routes ---
@app.post("/auth/register", response_model=UserResponse, tags=["auth"])
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@app.post("/auth/token", response_model=Token, tags=["auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserResponse, tags=["users"])
async def get_me(
    token_data=Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.username == token_data.username))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# --- ML Prediction Routes ---
@app.post("/predict", response_model=PredictionResponse, tags=["ml"])
async def predict(
    request: PredictionRequest,
    background_tasks: BackgroundTasks,
    token_data=Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
):
    start = time.time()
    features = np.array([[request.feature_1, request.feature_2,
                          request.feature_3, request.feature_4]])

    # Real inference (uncomment when model is loaded):
    # scaled = ml_models["scaler"].transform(features)
    # pred_id = int(ml_models["classifier"].predict(scaled)[0])
    # confidence = float(ml_models["classifier"].predict_proba(scaled).max())

    pred_id = 0  # mock
    confidence = 0.95
    result_label = ["setosa", "versicolor", "virginica"][pred_id]
    latency = (time.time() - start) * 1000

    # Log to DB in background
    async def log_prediction():
        async with engine.begin() as conn:
            pass  # insert prediction record

    background_tasks.add_task(log_prediction)

    return PredictionResponse(
        result=result_label,
        confidence=confidence,
        model_version=ml_models.get("version", "v1"),
        latency_ms=round(latency, 2),
        input_data=json.dumps(request.model_dump())
    )


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["ml"])
async def predict_batch(
    request: BatchPredictionRequest,
    token_data=Depends(get_current_user_token)
):
    start = time.time()
    results = []
    for sample in request.samples:
        results.append(PredictionResponse(
            result="setosa",
            confidence=0.95,
            model_version=ml_models.get("version", "v1"),
            latency_ms=0.5
        ))
    total_latency = (time.time() - start) * 1000
    return BatchPredictionResponse(
        predictions=results,
        total=len(results),
        batch_latency_ms=round(total_latency, 2)
    )
