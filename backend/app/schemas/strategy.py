"""Strategy Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

from app.core.strategy.types import StrategyType, StrategyStatus


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
    status: Optional[StrategyStatus] = None


# Schema for strategy response
class StrategyResponse(StrategyBase):
    """Schema for strategy response."""
    id: int
    user_id: int
    status: StrategyStatus
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


# Schema for strategy execution request
class StrategyExecuteRequest(BaseModel):
    """Schema for executing strategy on multiple symbols."""
    symbols: list[str] = Field(..., min_length=1, description="List of stock symbols to execute strategy on")
    source: Optional[str] = Field(None, description="Source of symbols (manual, watchlist, screening)")


# Schema for signal in execution response
class SignalResponse(BaseModel):
    """Schema for a single trading signal."""
    timestamp: str
    symbol: str
    signal_type: str
    price: float
    quantity: Optional[int] = None
    reason: Optional[str] = None
    confidence: Optional[float] = None


# Schema for strategy execution response
class StrategyExecuteResponse(BaseModel):
    """Schema for strategy execution response."""
    strategy_id: int
    strategy_name: str
    symbols: list[str]
    executed_at: str
    signals: list[SignalResponse]
    total_signals: int
    total_symbols: int
