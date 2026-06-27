from fastapi import APIRouter

from app.schemas.auth_schema import RegisterRequest, LoginRequest
from app.services.auth_service import register_user, login_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(auth: RegisterRequest):
    return await register_user(auth)


@router.post("/login")
async def login(auth: LoginRequest):
    return await login_user(auth)