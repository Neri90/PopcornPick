from fastapi import APIRouter, HTTPException, status
from auth.schema.user import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, LoginResponse
from auth.service import auth_service

router = APIRouter()

@router.post("/register", response_model=UserRegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest):
    """
    신규 사용자 등록(회원가입) API 엔드포인트입니다.
    """
    # TODO: auth_service.register_user 함수를 호출하여 회원가입을 완료하고 결과를 반환하세요.
    return auth_service.register_user(payload.username, payload.email, payload.password)

@router.post("/login", response_model=LoginResponse)
def login(payload: UserLoginRequest):
    """
    사용자 로그인 API 엔드포인트입니다.
    """
    # TODO: auth_service.authenticate_user 함수를 호출하여 로그인을 검증하고 결과를 반환하세요.
    result = auth_service.authenticate_user(payload.email, payload.password)
    return LoginResponse(success=result, message="로그인 성공")