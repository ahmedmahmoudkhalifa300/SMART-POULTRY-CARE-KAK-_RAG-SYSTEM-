from sqlalchemy import Column, Integer, String, Float, DateTime
import datetime
from .database import Base

class PredictionHistory(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    predicted_disease = Column(String, index=True)
    confidence_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)


class Flock(Base):
    __tablename__ = "flocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    initial_size = Column(Integer)  # عدد الطيور عند البداية
    cycle_age = Column(Integer)  # العمر بالأيام
    mortality = Column(Integer, default=0)  # عدد النافق
    feed_consumed = Column(Float, default=0.0)  # الكمية بالطن
    season = Column(String, default="summer")  # صيف أو شتاء
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
