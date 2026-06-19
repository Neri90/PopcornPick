from fastapi import APIRouter, HTTPException, status, Depends
from auth.schema.user import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, LoginResponse
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
    
    return LoginResponse(
        success=True,
        message="로그인 성공",
        access_token=access_token,
        user_id=user["user_id"],
        username=user["username"]
    )
