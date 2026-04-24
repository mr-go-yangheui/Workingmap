from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ── Auth ──
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ── Exercise ──
class ExerciseOut(BaseModel):
    id: int
    name: str
    category: str
    injury_risk: bool
    start_weight: float
    increment: float
    description: str
    class Config:
        from_attributes = True

# ── WorkoutLog ──
class WorkoutLogCreate(BaseModel):
    exercise_id: int
    weight: float
    set_results: List[bool]   # [True, False, True, True, True]

class WorkoutLogOut(BaseModel):
    id: int
    exercise_id: int
    date: datetime
    weight: float
    set_results: List[bool]
    all_success: bool
    volume: float
    class Config:
        from_attributes = True

# ── UserProgress ──
class UserProgressOut(BaseModel):
    exercise_id: int
    exercise_name: str
    category: str
    current_weight: float
    next_weight: float          # 성공 시 다음 무게
    last_trained: Optional[datetime]
    cooldown_ok: bool           # 48시간 지났는지
    class Config:
        from_attributes = True
