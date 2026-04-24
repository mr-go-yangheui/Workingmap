"""
48시간 쿨다운 체크
"""
from datetime import datetime, timezone, timedelta
from typing import Optional

COOLDOWN_HOURS = 48

def is_cooldown_ok(last_trained: Optional[datetime]) -> bool:
    """last_trained 이후 48시간이 지났으면 True"""
    if last_trained is None:
        return True
    now = datetime.now(timezone.utc)
    # naive datetime 처리
    if last_trained.tzinfo is None:
        last_trained = last_trained.replace(tzinfo=timezone.utc)
    return (now - last_trained) >= timedelta(hours=COOLDOWN_HOURS)

def remaining_cooldown_hours(last_trained: Optional[datetime]) -> float:
    """남은 쿨다운 시간(시간 단위), 0이면 가능"""
    if last_trained is None:
        return 0.0
    now = datetime.now(timezone.utc)
    if last_trained.tzinfo is None:
        last_trained = last_trained.replace(tzinfo=timezone.utc)
    elapsed = (now - last_trained).total_seconds() / 3600
    remaining = COOLDOWN_HOURS - elapsed
    return max(0.0, round(remaining, 1))
