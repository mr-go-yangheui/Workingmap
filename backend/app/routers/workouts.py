from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user
from ..utils.overload import get_or_create_progress, update_progress
from ..utils.cooldown import is_cooldown_ok

router = APIRouter(prefix="/workouts", tags=["Workouts"])

TARGET_SETS = 5
TARGET_REPS = 12

@router.post("/log", response_model=schemas.WorkoutLogOut, status_code=201)
def log_workout(
    log_in: schemas.WorkoutLogCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == log_in.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="존재하지 않는 운동입니다.")

    # 48시간 쿨다운 체크
    prog = get_or_create_progress(db, current_user.id, exercise)
    if not is_cooldown_ok(prog.last_trained):
        raise HTTPException(status_code=400, detail="48시간 회복 시간이 지나지 않았습니다.")

    # 세트 수 검증
    if len(log_in.set_results) != TARGET_SETS:
        raise HTTPException(status_code=400, detail=f"세트 수는 반드시 {TARGET_SETS}세트여야 합니다.")

    all_success = all(log_in.set_results)
    success_sets = sum(log_in.set_results)
    volume = log_in.weight * success_sets * TARGET_REPS
    now = datetime.now(timezone.utc)

    # 로그 저장
    log = models.WorkoutLog(
        user_id=current_user.id,
        exercise_id=log_in.exercise_id,
        weight=log_in.weight,
        target_reps=TARGET_REPS,
        target_sets=TARGET_SETS,
        set_results=log_in.set_results,
        all_success=all_success,
        volume=volume,
        date=now,
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    # 무게 업데이트 (성공 시 +increment, 실패 시 유지)
    update_progress(db, current_user.id, exercise, all_success, now)
    return log

@router.get("/history", response_model=List[schemas.WorkoutLogOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.WorkoutLog)             .filter(models.WorkoutLog.user_id == current_user.id)             .order_by(models.WorkoutLog.date.desc())             .all()

@router.get("/history/{exercise_id}")
def get_exercise_history(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    logs = db.query(models.WorkoutLog)             .filter_by(user_id=current_user.id, exercise_id=exercise_id)             .order_by(models.WorkoutLog.date.asc())             .all()
    return [{"date": l.date, "weight": l.weight, "all_success": l.all_success,
             "set_results": l.set_results, "volume": l.volume} for l in logs]
