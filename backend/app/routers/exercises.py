from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user
from ..utils.cooldown import is_cooldown_ok, remaining_cooldown_hours
from ..utils.overload import get_or_create_progress

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("/", response_model=List[schemas.ExerciseOut])
def list_exercises(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    q = db.query(models.Exercise)
    if category:
        q = q.filter(models.Exercise.category == category)
    return q.all()

@router.get("/progress", response_model=List[schemas.UserProgressOut])
def my_progress(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    exercises = db.query(models.Exercise).all()
    result = []
    for ex in exercises:
        prog = get_or_create_progress(db, current_user.id, ex)
        next_w = prog.current_weight + ex.increment
        result.append(schemas.UserProgressOut(
            exercise_id=ex.id,
            exercise_name=ex.name,
            category=ex.category,
            current_weight=prog.current_weight,
            next_weight=next_w,
            last_trained=prog.last_trained,
            cooldown_ok=is_cooldown_ok(prog.last_trained),
        ))
    return result

@router.get("/available")
def available_exercises(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """48시간 쿨다운이 지난 운동만 반환 (선택 가능 목록)"""
    q = db.query(models.Exercise)
    if category:
        q = q.filter(models.Exercise.category == category)
    exercises = q.all()
    result = []
    for ex in exercises:
        prog = get_or_create_progress(db, current_user.id, ex)
        ok = is_cooldown_ok(prog.last_trained)
        remaining = remaining_cooldown_hours(prog.last_trained)
        result.append({
            "id": ex.id,
            "name": ex.name,
            "category": ex.category,
            "injury_risk": ex.injury_risk,
            "current_weight": prog.current_weight,
            "next_weight": prog.current_weight + ex.increment,
            "cooldown_ok": ok,
            "remaining_hours": remaining,
        })
    return result
