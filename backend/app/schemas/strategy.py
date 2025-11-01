"""Strategy Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from app.models.strategy import StrategyType


# Base schema
class StrategyBase(BaseModel):
    """Base strategy schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    strategy_type: StrategyType
    parameters: Dict[str, Any] = Field(default_factory=dict)


# Schema for creating strategy
class StrategyCreate(StrategyBase):
    """Schema for creating a new strategy."""
    pass


# Schema for updating strategy
class StrategyUpdate(BaseModel):
    """Schema for updating a strategy."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    strategy_type: Optional[StrategyType] = None
    parameters: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


# Schema for strategy response
class StrategyResponse(StrategyBase):
    """Schema for strategy response."""
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema for strategy list response
class StrategyListResponse(BaseModel):
    """Schema for paginated strategy list."""
    strategies: list[StrategyResponse]
    total: int
    page: int
    page_size: int
