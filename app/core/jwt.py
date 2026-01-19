from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from typing import Any

from app.core.config import settings


def create_access_token(subject: int, role: str) -> str:
    payload = {
        "sub": str(subject),  # Convert to string
        "role": role,
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.now(tz=timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(
        payload,
        settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(subject: int) -> str:
    payload = {
        "sub": str(subject),  # Convert to string
        "iat": datetime.now(tz=timezone.utc),
        "exp": datetime.now(tz=timezone.utc)
        + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    }

    return jwt.encode(
        payload,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.JWT_ACCESS_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )


def decode_refresh_token(token: str) -> dict[str, Any]:
    return jwt.decode(
        token,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
