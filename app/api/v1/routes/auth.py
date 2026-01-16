from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.db.session import get_db
from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
)
from app.schemas.user import UserRead
from app.services.auth_service import AuthService
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        user = service.register(data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        access, refresh, user = service.login(data.email, data.password)

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,     # False only for local dev without HTTPS
            samesite="lax",
            max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
        )

        return TokenResponse(
            access_token=access,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserRead.model_validate(user),
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
@router.post("/refresh")
def refresh(
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    service = AuthService(db)

    try:
        access, refresh = service.refresh(refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    response = JSONResponse({"access_token": access})
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )
    return response


@router.post("/logout")
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if refresh_token:
        AuthService(db).logout(refresh_token)

    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}

