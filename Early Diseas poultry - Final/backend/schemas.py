# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    id: int
    filename: str
    predicted_disease: str
    confidence_score: float
    timestamp: datetime

    class Config:
        from_attributes = True


class FlockBase(BaseModel):
    name: str
    initial_size: int
    cycle_age: int
    mortality: int = 0
    feed_consumed: float = 0.0
    season: str = "summer"


class FlockCreate(FlockBase):
    pass


class FlockUpdate(BaseModel):
    cycle_age: int = None
    mortality: int = None
    feed_consumed: float = None
    season: str = None


class FlockResponse(FlockBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
