from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.schemas.user import UserRead

# Registration

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)


class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    role: str


# Login

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserRead

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class JWTPayload(BaseModel):
    sub: int
    role: str
    iat: datetime
    exp: datetime