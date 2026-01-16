from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime


class UserRole(str, Enum):
    admin = "admin"
    student = "student"


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.student


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    role: UserRole | None = None
    password: str | None = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: UserRole
    is_verified: bool

    class Config:
        from_attributes = True

class UserAdminRead(UserRead):
    created_at: datetime
