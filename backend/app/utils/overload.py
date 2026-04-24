"""
점진적 과부화 무게 계산 유틸리티
"""
from sqlalchemy.orm import Session
from .. import models

def get_or_create_progress(db: Session, user_id: int, exercise: models.Exercise) -> models.UserProgress:
    prog = db.query(models.UserProgress).filter_by(
        user_id=user_id, exercise_id=exercise.id
    ).first()
    if not prog:
        prog = models.UserProgress(
            user_id=user_id,
            exercise_id=exercise.id,
            current_weight=exercise.start_weight,
            last_trained=None,
        )
        db.add(prog)
        db.commit()
        db.refresh(prog)
    return prog

def calc_next_weight(exercise: models.Exercise, current_weight: float, all_success: bool) -> float:
    """모든 세트 성공 시 increment 증가, 실패 시 유지"""
    if all_success:
        return current_weight + exercise.increment
    return current_weight

def update_progress(db: Session, user_id: int, exercise: models.Exercise,
                    all_success: bool, trained_at) -> models.UserProgress:
    prog = get_or_create_progress(db, user_id, exercise)
    prog.current_weight = calc_next_weight(exercise, prog.current_weight, all_success)
    prog.last_trained   = trained_at
    db.commit()
    db.refresh(prog)
    return prog
