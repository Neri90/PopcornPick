from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from pydantic_core.core_schema import none_schema


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

class UserCurrentResponse(BaseModel):
    """
    내 정보 조회 응답 바디 스키마
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
    access_token: Optional[str] = None
    user_id: Optional[int] = None
    username: Optional[str] = None
    refresh_token: Optional[str] = None

class UserUpdateRequest(BaseModel):
    """
    회원 정보 수정 요청 스키마
    """
    username: Optional[str] = None
    password: Optional[str] = None

class UserUpdateResponse(BaseModel):
    """
    회원 정보 수정 응답 스키마
    """
    user_id: int
    email: EmailStr
    username: str
    created_at: datetime

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str