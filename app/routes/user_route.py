from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.services.user_service import get_users, get_user_by_id

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
async def users(current_user=Depends(get_current_user)):
    return await get_users()


@router.get("/{user_id}")
async def user(user_id: str, current_user=Depends(get_current_user)):
    return await get_user_by_id(user_id)


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return current_user