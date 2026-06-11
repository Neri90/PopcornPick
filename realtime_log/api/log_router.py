from datetime import datetime
from enum import Enum
from db import get_connection

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import create_engine, text

from realtime_log.service.log_service import save_log

router = APIRouter()

class LogRequest(BaseModel):
    user_id: int
    movie_id: int
    genres: str
    action_type: str
    rating_value: Optional[int] = None

@router.post("")
async def create_log(payload: LogRequest):
    save_log(payload)
    return {"status": "success"}