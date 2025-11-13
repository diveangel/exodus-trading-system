"""User Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.models.user import UserRole, TradingMode


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

    # Optional KIS API credentials (not used during registration)
    # Users should set credentials in Settings page after registration


# Schema for updating user
class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)

    # KIS API credentials (deprecated, use mode-specific endpoints)
    pass


# Schema for updating Real trading KIS credentials
class RealKISCredentialsUpdate(BaseModel):
    """Schema for updating Real trading KIS credentials."""
    real_app_key: str
    real_app_secret: str
    real_account_number: str
    real_account_code: str


# Schema for updating Mock trading KIS credentials
class MockKISCredentialsUpdate(BaseModel):
    """Schema for updating Mock trading KIS credentials."""
    mock_app_key: str
    mock_app_secret: str
    mock_account_number: str
    mock_account_code: str


# Schema for user response (without sensitive data)
class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    is_verified: bool
    has_real_credentials: bool = False
    has_mock_credentials: bool = False
    kis_trading_mode: TradingMode = TradingMode.MOCK
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema for detailed user response (with KIS account info)
class UserDetailResponse(UserResponse):
    """Schema for detailed user response including KIS account info."""
    # Real trading account info (masked)
    real_account_number: Optional[str] = None
    real_account_code: Optional[str] = None

    # Mock trading account info (masked)
    mock_account_number: Optional[str] = None
    mock_account_code: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Schema for login
class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str
    kis_trading_mode: TradingMode = TradingMode.MOCK


# Schema for token response
class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Schema for login response (includes token and user info)
class LoginResponse(Token):
    """Schema for login response with user information."""
    user: UserResponse


# Schema for refresh token request
class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str


# Schema for token data
class TokenData(BaseModel):
    """Schema for token payload data."""
    user_id: Optional[int] = None
    email: Optional[str] = None
