from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String, unique=True, index=True, nullable=False)
    username   = Column(String, unique=True, index=True, nullable=False)
    hashed_pw  = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    logs       = relationship("WorkoutLog", back_populates="user")
    progresses = relationship("UserProgress", back_populates="user")

class Exercise(Base):
    __tablename__ = "exercises"
    id           = Column(Integer, primary_key=True, index=True)
    name         = Column(String, nullable=False)
    category     = Column(String, nullable=False)   # chest/back/shoulder/leg/arm/core
    injury_risk  = Column(Boolean, default=False)   # True → 팔꿈치·어깨 부상위험
    start_weight = Column(Float, default=20.0)       # injury_risk=True → 3.0
    increment    = Column(Float, default=5.0)        # injury_risk=True → 1.0
    description  = Column(String, default="")

class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    date        = Column(DateTime(timezone=True), server_default=func.now())
    weight      = Column(Float, nullable=False)
    target_reps = Column(Integer, default=12)
    target_sets = Column(Integer, default=5)
    set_results = Column(JSON, nullable=False)  # [true,false,true,true,true]
    all_success = Column(Boolean, nullable=False)
    volume      = Column(Float, nullable=False)  # weight * 성공세트수 * reps
    user        = relationship("User", back_populates="logs")
    exercise    = relationship("Exercise")

class UserProgress(Base):
    __tablename__ = "user_progress"
    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id    = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    current_weight = Column(Float, nullable=False)
    last_trained   = Column(DateTime(timezone=True), nullable=True)
    user           = relationship("User", back_populates="progresses")
    exercise       = relationship("Exercise")
