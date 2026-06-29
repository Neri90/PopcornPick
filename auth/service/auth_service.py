from auth.repository.user_repo import UserRepository
import bcrypt
from fastapi import HTTPException
import jwt
import os
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from fastapi import Depends

from auth.schema import user
from db import get_db

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "popcornpick_secret_key_change_in_production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

security = HTTPBearer()

def create_access_token(data: dict) -> str:
    """
    Access Token (JWT)을 생성합니다.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        decoded_jwt = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_jwt
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="토큰이 만료되었습니다.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

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

def get_current_user(credentials = Depends(security), db = Depends(get_db)):
    payload = decode_access_token(credentials.credentials)
    user_id = int(payload.get("sub"))
    repo = UserRepository(db)
    user = repo.get_user_by_id(user_id)
    return user

def register_user(username: str, email: str, password_raw: str, db) -> dict:
    """
    회원가입의 비즈니스 논리를 처리합니다.
    1. 이메일 중복 체크
    2. 비밀번호 평문 해시화
    3. 레포지토리를 통한 회원 정보 DB 영속화
    """
    # TODO: 회원가입 성공 시 생성된 회원 정보를 딕셔너리 형태로 반환하세요.
    # 1
    repo = UserRepository(db)
    existing_user = repo.get_user_by_email(email)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")
    # 2
    password_hash = hash_password(password_raw)
    # 3
    row = repo.create_user(username, email, password_hash)
    return {
        "user_id": row["user_id"],
        "email": row["email"],
        "username": row["username"],
        "created_at": row["created_at"]
    }

def authenticate_user(email: str, password_raw: str, db) -> dict:
    """
    로그인(인증)의 비즈니스 논리를 처리합니다.
    1. 이메일로 사용자 조회
    2. 비밀번호 불일치 시 HTTP 401 Unauthorized 에러 발생
    3. 성공 시 사용자 정보 딕셔너리 반환
    """
    # 1
    repo = UserRepository(db)
    user = repo.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="존재하지 않는 이메일입니다.")
    # 2
    is_valid = verify_password(password_raw, user["password"])
    if not is_valid:
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")
    # 3
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "email": user["email"]
    }

def update_user(user_id:int, username: str, password_raw: str, db) -> dict:
    """
    1. password가 있으면 해시화하기 (hash_password 함수 이미 있어요)
    2. repo의 update_user 호출하기
    3. 결과 반환하기
    """
    #1
    password_hash = hash_password(password_raw) if password_raw else None
    username = username if username else None
    #2
    repo = UserRepository(db)
    updating_user = repo.update_user(user_id, username, password_hash)
    #3
    return {
        "user_id": updating_user["user_id"],
        "email": updating_user["email"],
        "username": updating_user["username"],
        "created_at": updating_user["created_at"]
    }

def create_refresh_token(data: dict) -> str:
    """
    Refresh Token (JWT) 생성
    """
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def refresh_access_token(token: str, db) -> str:
    """
    1. 클라이언트가 보낸 Refresh Token을 DB에서 찾기
    2. 없으면 401 에러
    3. 있으면 새 Access Token 발급해서 반환
    """
    #1
    repo = UserRepository(db)
    stored_token = repo.get_refresh_token(token)
    #2
    if not stored_token:
        raise HTTPException(status_code=401, detail="유효하지 않은 Refresh Token 입니다.")
    #3
    payload = decode_access_token(token)
    new_access_token = create_access_token({"sub": payload.get("sub"), "email": payload.get("email")})
    return new_access_token

def logout(user_id: int, token: str, db) -> None:
    repo = UserRepository(db)
    repo.delete_refresh_token(user_id, token)

def save_refresh_token(user_id: int, token: str, db) -> None:
    repo = UserRepository(db)
    repo.save_refresh_token(user_id, token)