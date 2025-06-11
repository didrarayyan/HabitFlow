"""
User schemas for request/response validation.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    timezone: str = "UTC"
    theme: str = "light"


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    timezone: Optional[str] = None
    theme: Optional[str] = None
    avatar_url: Optional[str] = None


class UserInDBBase(UserBase):
    """Base user schema with database fields."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_verified: bool = False
    avatar_url: Optional[str] = None
    google_id: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    """User schema for responses."""
    pass


class UserInDB(UserInDBBase):
    """User schema with hashed password."""
    hashed_password: str


# Authentication schemas
class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class PasswordReset(BaseModel):
    """Password reset schema."""
    token: str
    new_password: str


class PasswordResetRequest(BaseModel):
    """Password reset request schema."""
    email: EmailStr

