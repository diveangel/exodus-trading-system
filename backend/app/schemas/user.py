"""User Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.models.user import UserRole


# Base schema with common fields
class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    role: UserRole = UserRole.USER


# Schema for creating a new user
class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=100)

    # Optional KIS API credentials
    kis_app_key: Optional[str] = None
    kis_app_secret: Optional[str] = None
    kis_account_number: Optional[str] = None
    kis_account_code: Optional[str] = None


# Schema for updating user
class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)

    # KIS API credentials
    kis_app_key: Optional[str] = None
    kis_app_secret: Optional[str] = None
    kis_account_number: Optional[str] = None
    kis_account_code: Optional[str] = None


# Schema for updating KIS credentials only
class UserKISUpdate(BaseModel):
    """Schema for updating Korea Investment API credentials."""
    kis_app_key: str
    kis_app_secret: str
    kis_account_number: str
    kis_account_code: str


# Schema for user response (without sensitive data)
class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    is_verified: bool
    has_kis_credentials: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema for detailed user response (with KIS account info)
class UserDetailResponse(UserResponse):
    """Schema for detailed user response including KIS account info."""
    kis_account_number: Optional[str] = None
    kis_account_code: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Schema for login
class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


# Schema for token response
class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Schema for token data
class TokenData(BaseModel):
    """Schema for token payload data."""
    user_id: Optional[int] = None
    email: Optional[str] = None
