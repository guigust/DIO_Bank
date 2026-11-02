from fastapi import APIRouter

from src.schemas.auth import LoginIn
from src.security import JWTToken, sign_jwt

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post(
    "/login",
    summary="Autenticar usuário",
    description="Emite um token JWT para o usuário informado.",
    response_model=JWTToken,
)
async def login(data: LoginIn):
    return sign_jwt(user_id=data.user_id)