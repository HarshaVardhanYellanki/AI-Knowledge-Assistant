from datetime import datetime, UTC

from fastapi import HTTPException, status
from pwdlib import PasswordHash

from app.core.security import create_access_token
from app.database.mongodb import users_collection
from app.schemas.auth_schema import RegisterRequest, LoginRequest

password_hash = PasswordHash.recommended()


def hash_password(password: str):
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)


async def register_user(auth: RegisterRequest):

    existing_user = await users_collection.find_one(
        {"email": auth.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    user = {
        "name": auth.name,
        "email": auth.email,
        "password": hash_password(auth.password),
        "created_at": datetime.now(UTC)
    }

    result = await users_collection.insert_one(user)

    return {
        "message": "User Registered Successfully",
        "user_id": str(result.inserted_id)
    }


async def login_user(auth: LoginRequest):

    user = await users_collection.find_one(
        {"email": auth.email}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password"
        )

    if not verify_password(
        auth.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email or Password"
        )

    token = create_access_token(
        str(user["_id"])
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }