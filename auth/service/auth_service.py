from typing import Optional
from auth.repository.user_repo import create_user, get_user_by_email
import bcrypt
from fastapi import HTTPException
import jwt
import os
from datetime import datetime, timedelta

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "popcornpick_secret_key_change_in_production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict) -> str:
    """
    Access Token (JWT)을 생성합니다.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def hash_password(password: str) -> str:
    """
    비밀번호 평문을 안전하게 해시화합니다.
    """
    # TODO: 해시 패키지(예: bcrypt)를 사용해 비밀번호를 단방향 암호화하여 반환하세요.
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호와 해시 비밀번호를 비교합니다.
    """
    # TODO: 입력 비밀번호와 DB 해시 비밀번호의 일치 여부를 검증하세요.
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def register_user(username: str, email: str, password_raw: str) -> dict:
    """
    회원가입의 비즈니스 논리를 처리합니다.
    1. 이메일 중복 체크
    2. 비밀번호 평문 해시화
    3. 레포지토리를 통한 회원 정보 DB 영속화
    """
    # TODO: 회원가입 성공 시 생성된 회원 정보를 딕셔너리 형태로 반환하세요.
    # 1
    existing_user = get_user_by_email(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")
    # 2
    password_hash = hash_password(password_raw)
    # 3
    row = create_user(username, email, password_hash)
    return {
        "user_id": row[0],
        "email": row[1],
        "username": row[2],
        "created_at": row[3]
    }

def authenticate_user(email: str, password_raw: str) -> dict:
    """
    로그인(인증)의 비즈니스 논리를 처리합니다.
    1. 이메일로 사용자 조회
    2. 비밀번호 불일치 시 HTTP 401 Unauthorized 에러 발생
    3. 성공 시 사용자 정보 딕셔너리 반환
    """
    # 1
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="존재하지 않는 이메일입니다.")
    # 2
    is_valid = verify_password(password_raw, user[3])
    if not is_valid:
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")
    # 3
    return {
        "user_id": user[0],
        "username": user[1],
        "email": user[2]
    }
