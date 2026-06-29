from fastapi import APIRouter, HTTPException, status, Depends

import db
from auth.schema import user
from auth.schema.user import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, LoginResponse, \
    UserCurrentResponse, UserUpdateResponse, UserUpdateRequest, RefreshRequest, LogoutRequest
from auth.service import auth_service
from sqlalchemy.orm import Session
from db import get_db

router = APIRouter()

@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest,db: Session = Depends(get_db)):
    """
    신규 사용자 등록(회원가입) API 엔드포인트입니다.
    """
    # TODO: auth_service.register_user 함수를 호출하여 회원가입을 완료하고 결과를 반환하세요.
    return auth_service.register_user(payload.username, payload.email, payload.password, db)

@router.post("/login", response_model=LoginResponse)
def login(payload: UserLoginRequest,db: Session = Depends(get_db)):
    """
    사용자 로그인 API 엔드포인트입니다.
    """
    user = auth_service.authenticate_user(payload.email, payload.password, db)

    # JWT 토큰 생성
    token_data = {"sub": str(user["user_id"]), "email": user["email"]}
    access_token = auth_service.create_access_token(token_data)
    # Refreshed Token (JWT) DB 저장
    refresh_token = auth_service.create_refresh_token(token_data)
    auth_service.save_refresh_token(user["user_id"], refresh_token, db)

    return LoginResponse(
        success=True,
        message="로그인 성공",
        access_token=access_token,
        user_id=user["user_id"],
        username=user["username"],
        refresh_token=refresh_token
    )

@router.get("/me", response_model=UserCurrentResponse)
def me(current_user = Depends(auth_service.get_current_user)):
    """
    내 정보 조회 API 엔드포인트
    """
    return current_user

@router.put("/profile", response_model=UserUpdateResponse)
def profile(payload: UserUpdateRequest, current_user = Depends(auth_service.get_current_user),db: Session = Depends(get_db)):
    """
    사용자 정보 수정 API 엔드포인트
    """
    return auth_service.update_user(current_user["user_id"], payload.username, payload.password, db)

@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    new_access_token = auth_service.refresh_access_token(payload.refresh_token, db)
    return {"access_token": new_access_token}

@router.post("/logout")
def logout(payload: LogoutRequest, current_user = Depends(auth_service.get_current_user),db: Session = Depends(get_db)):
    auth_service.logout((current_user["user_id"]), payload.refresh_token, db)
    return {"message": "로그아웃 성공"}