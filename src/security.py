import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from src.config import settings

ALGORITHM = "HS256"
ISSUER = "desafio-bank.com.br"
AUDIENCE = "desafio-bank"
TOKEN_LIFETIME_SECONDS = 60 * 30


class AccessToken(BaseModel):
    iss: str
    sub: str
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: str


def sign_jwt(user_id: int) -> JWTToken:
    now = time.time()

    payload = {
        "iss": ISSUER,
        "sub": str(user_id),
        "aud": AUDIENCE,
        "exp": now + TOKEN_LIFETIME_SECONDS,
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=ALGORITHM,
    )

    return JWTToken(access_token=token)


async def decode_jwt(token: str) -> AccessToken | None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            audience=AUDIENCE,
            issuer=ISSUER,
            algorithms=[ALGORITHM],
        )
        return AccessToken.model_validate(payload)
    except (jwt.InvalidTokenError, ValueError):
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessToken:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code.",
            )

        if scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme.",
            )

        payload = await decode_jwt(credentials)

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token.",
            )

        return payload


async def get_current_user(
    token: Annotated[AccessToken, Depends(JWTBearer())],
) -> dict[str, int]:
    return {"user_id": int(token.sub)}


def login_required(
    current_user: Annotated[
        dict[str, int],
        Depends(get_current_user),
    ],
) -> dict[str, int]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return current_user