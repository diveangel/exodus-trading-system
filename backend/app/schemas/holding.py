"""Holding Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class HoldingBase(BaseModel):
    """Base holding schema."""
    symbol: str = Field(..., min_length=1, max_length=20)
    company_name: Optional[str] = Field(None, max_length=100)
    quantity: int = Field(..., gt=0)
    average_price: float = Field(..., gt=0)
    current_price: float = Field(..., gt=0)


class HoldingCreate(HoldingBase):
    """Schema for creating a new holding."""
    user_id: int


class HoldingUpdate(BaseModel):
    """Schema for updating a holding."""
    quantity: Optional[int] = Field(None, gt=0)
    average_price: Optional[float] = Field(None, gt=0)
    current_price: Optional[float] = Field(None, gt=0)
    company_name: Optional[str] = Field(None, max_length=100)


class HoldingResponse(HoldingBase):
    """Schema for holding response."""
    id: int
    user_id: int
    total_cost: float
    current_value: float
    unrealized_pnl: float
    unrealized_pnl_percent: float
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HoldingListResponse(BaseModel):
    """Schema for holdings list with summary."""
    holdings: list[HoldingResponse]
    total_cost: float
    total_value: float
    total_unrealized_pnl: float
    total_unrealized_pnl_percent: float


class PortfolioSummary(BaseModel):
    """Schema for portfolio summary."""
    total_holdings: int
    total_investment: float
    current_value: float
    total_pnl: float
    total_pnl_percent: float
    cash_balance: float
    total_assets: float
