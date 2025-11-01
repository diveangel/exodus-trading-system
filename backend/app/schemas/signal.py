"""Signal Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from app.models.signal import SignalType


# Base schema
class SignalBase(BaseModel):
    """Base signal schema."""
    symbol: str = Field(..., min_length=1, max_length=20)
    signal_type: SignalType
    confidence: float = Field(..., ge=0.0, le=1.0)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    reason: Dict[str, Any] = Field(default_factory=dict)


# Schema for creating signal
class SignalCreate(SignalBase):
    """Schema for creating a new signal."""
    strategy_id: int


# Schema for updating signal
class SignalUpdate(BaseModel):
    """Schema for updating a signal."""
    is_executed: Optional[bool] = None
    executed_at: Optional[datetime] = None


# Schema for signal response
class SignalResponse(SignalBase):
    """Schema for signal response."""
    id: int
    strategy_id: int
    is_executed: bool
    executed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema for signal list response
class SignalListResponse(BaseModel):
    """Schema for paginated signal list."""
    signals: list[SignalResponse]
    total: int
    page: int
    page_size: int
