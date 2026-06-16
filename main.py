from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from db import engine
from contextlib import asynccontextmanager
from batch_recommendation.api.recommendation_router import router as recommendation_router
from realtime_log.api.log_router import router as log_router
from popular_movie.api.popular_movie_router import router as popular_movie_router
from auth.api.auth_router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("DB 연결 성공")
    except Exception as e:
        print(f"DB 연결 실패: {e}")
    yield

app = FastAPI(title="PopcornPick API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(recommendation_router, prefix="/recommendations", tags=["recommendations"])
app.include_router(log_router, prefix="/logs", tags=["logs"])
app.include_router(popular_movie_router, prefix="/movies", tags=["movies"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": str(e)}