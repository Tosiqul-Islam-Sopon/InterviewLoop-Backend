from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import JWTError

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.auth import RegisterRequest
from app.core.security import hash_password, verify_password, hash_token
from app.core.jwt import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.core.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    # ---------------- REGISTER ----------------
    def register(self, data: RegisterRequest) -> User:
        if data.password != data.confirm_password:
            raise ValueError("Passwords do not match")

        email = data.email.lower().strip()

        existing = self.db.query(User).filter(User.email == email).first()
        if existing:
            raise ValueError("User already exists")

        user = User(
            email=email,
            password_hash=hash_password(data.password),
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    # ---------------- LOGIN ----------------
    def login(self, email: str, password: str):
        user = self.db.query(User).filter(
            User.email == email.lower().strip()
        ).first()

        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("Inactive account")

        # 🔒 Optional: revoke previous refresh tokens
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user.id
        ).delete()

        access_token = create_access_token(user.id, user.role.value)
        refresh_token = create_refresh_token(user.id)

        refresh_token_db = RefreshToken(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=datetime.now(tz=timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        self.db.add(refresh_token_db)
        self.db.commit()

        return access_token, refresh_token, user

    # ---------------- REFRESH ----------------
    def refresh(self, refresh_token: str) -> tuple[str, str]:
        try:
            payload = decode_refresh_token(refresh_token)
            user_id: int = payload["sub"]
        except JWTError:
            raise ValueError("Invalid refresh token")

        token_hash = hash_token(refresh_token)

        db_token = (
            self.db.query(RefreshToken)
            .filter(
                RefreshToken.user_id == user_id,
                RefreshToken.token_hash == token_hash,
            )
            .first()
        )

        if not db_token:
            raise ValueError("Refresh token revoked")

        if db_token.expires_at < datetime.now(tz=timezone.utc):
            raise ValueError("Refresh token expired")

        # 🔄 ROTATION
        self.db.delete(db_token)

        access_token = create_access_token(
            subject=user_id,
            role=db_token.user.role.value,
        )
        new_refresh_token = create_refresh_token(subject=user_id)

        new_refresh_db = RefreshToken(
            user_id=user_id,
            token_hash=hash_token(new_refresh_token),
            expires_at=datetime.now(tz=timezone.utc)
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )

        self.db.add(new_refresh_db)
        self.db.commit()

        return access_token, new_refresh_token

    # ---------------- LOGOUT ----------------
    def logout(self, refresh_token: str):
        token_hash = hash_token(refresh_token)

        self.db.query(RefreshToken).filter(
            RefreshToken.token_hash == token_hash
        ).delete()

        self.db.commit()
