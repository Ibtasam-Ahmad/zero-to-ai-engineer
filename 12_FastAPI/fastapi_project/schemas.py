from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# --- User Schemas ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


# --- ML Prediction Schemas ---
class PredictionRequest(BaseModel):
    feature_1: float = Field(..., description="First feature value")
    feature_2: float = Field(..., description="Second feature value")
    feature_3: float = Field(..., description="Third feature value")
    feature_4: float = Field(..., description="Fourth feature value")


class PredictionResponse(BaseModel):
    id: Optional[int] = None
    result: str
    confidence: float
    model_version: str
    latency_ms: float
    input_data: Optional[str] = None

    class Config:
        from_attributes = True


class BatchPredictionRequest(BaseModel):
    samples: List[PredictionRequest]


class BatchPredictionResponse(BaseModel):
    predictions: List[PredictionResponse]
    total: int
    batch_latency_ms: float
