from fastapi import APIRouter

from src.schemas.auth import LoginIn
from src.security import JWTToken, sign_jwt

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=JWTToken)
async def login(data: LoginIn):
    return sign_jwt(user_id=data.user_id)