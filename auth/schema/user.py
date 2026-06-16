from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserRegisterRequest(BaseModel):
    """
    회원가입 요청 바디 스키마
    """
    email: EmailStr
    username: str
    password: str

class UserRegisterResponse(BaseModel):
    """
    회원가입 응답 바디 스키마
    """
    user_id: int
    email: EmailStr
    username: str
    created_at: datetime

class UserLoginRequest(BaseModel):
    """
    로그인 요청 바디 스키마
    """
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """
    로그인 결과 응답 스키마
    """
    success: bool
    message: str