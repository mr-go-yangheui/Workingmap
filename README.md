# 💪 Progressive Overload Workout Tracker

점진적 과부화를 이용한 운동 트래커 앱 — FastAPI + SQLite + HTML/JS

## 실행 방법

```bash
cd backend
cp .env.example .env        # 환경변수 설정
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API 문서: http://localhost:8000/docs

## 배포 (Render.com 무료)
1. GitHub에 push
2. Render.com → New Web Service → GitHub 연결
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## API 엔드포인트
| Method | URL | 설명 |
|--------|-----|------|
| POST | /auth/register | 회원가입 |
| POST | /auth/login | 로그인 (JWT) |
| GET  | /users/me | 내 정보 |
| GET  | /exercises/ | 운동 목록 |
| GET  | /exercises/available | 선택 가능 운동 (48h 쿨다운) |
| GET  | /exercises/progress | 나의 진행 무게 |
| POST | /workouts/log | 운동 기록 저장 |
| GET  | /workouts/history | 전체 운동 히스토리 |
| GET  | /workouts/history/{exercise_id} | 종목별 히스토리 |
