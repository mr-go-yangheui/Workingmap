from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, exercises, workouts, users
from . import models

# DB 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Progressive Overload API",
    description="점진적 과부화 운동 트래커 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 배포 시 프론트엔드 URL로 제한
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(exercises.router)
app.include_router(workouts.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Progressive Overload API is running 💪"}

@app.on_event("startup")
def seed_exercises():
    """앱 최초 실행 시 운동 종목 기본 데이터 삽입"""
    from .database import SessionLocal
    db = SessionLocal()
    if db.query(models.Exercise).count() == 0:
        exercises_data = [
            # 가슴
            {"name":"벤치프레스",       "category":"chest",    "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"인클라인 벤치프레스","category":"chest",   "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"딥스",             "category":"chest",    "injury_risk":True,  "start_weight":3,  "increment":1},
            {"name":"덤벨 플라이",       "category":"chest",   "injury_risk":True,  "start_weight":3,  "increment":1},
            # 등
            {"name":"데드리프트",        "category":"back",    "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"바벨 로우",         "category":"back",    "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"랫 풀다운",         "category":"back",    "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"시티드 케이블 로우", "category":"back",   "injury_risk":False, "start_weight":20, "increment":5},
            # 어깨
            {"name":"오버헤드 프레스",   "category":"shoulder", "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"사이드 레터럴 레이즈","category":"shoulder","injury_risk":True, "start_weight":3,  "increment":1},
            {"name":"프론트 레이즈",     "category":"shoulder", "injury_risk":True,  "start_weight":3,  "increment":1},
            {"name":"페이스 풀",         "category":"shoulder", "injury_risk":True,  "start_weight":3,  "increment":1},
            # 하체
            {"name":"스쿼트",           "category":"leg",      "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"레그 프레스",       "category":"leg",     "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"런지",             "category":"leg",      "injury_risk":False, "start_weight":20, "increment":5},
            {"name":"레그 컬",           "category":"leg",     "injury_risk":False, "start_weight":20, "increment":5},
            # 팔
            {"name":"바벨 컬",           "category":"arm",     "injury_risk":True,  "start_weight":3,  "increment":1},
            {"name":"해머 컬",           "category":"arm",     "injury_risk":True,  "start_weight":3,  "increment":1},
            {"name":"EZ바 컬",           "category":"arm",     "injury_risk":True,  "start_weight":3,  "increment":1},
            {"name":"케이블 푸시다운",   "category":"arm",     "injury_risk":True,  "start_weight":3,  "increment":1},
            # 코어
            {"name":"플랭크",            "category":"core",    "injury_risk":False, "start_weight":0,  "increment":0},
            {"name":"크런치",            "category":"core",    "injury_risk":False, "start_weight":0,  "increment":0},
            {"name":"케이블 우드찹",     "category":"core",    "injury_risk":False, "start_weight":20, "increment":5},
        ]
        for d in exercises_data:
            db.add(models.Exercise(**d, description=""))
        db.commit()
    db.close()
