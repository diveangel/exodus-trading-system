"""Stock schemas for API request/response."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class StockBase(BaseModel):
    """Base stock schema."""

    symbol: str = Field(..., description="Stock symbol code")
    standard_code: str = Field(..., description="Standard code")
    name: str = Field(..., description="Korean stock name")
    market_type: Literal["KOSPI", "KOSDAQ"] = Field(..., description="Market type")


class StockCreate(StockBase):
    """Schema for creating a stock."""

    pass


class StockUpdate(BaseModel):
    """Schema for updating a stock."""

    name: str | None = None
    standard_code: str | None = None


class Stock(StockBase):
    """Stock schema with all fields."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StockSearchParams(BaseModel):
    """Stock search parameters."""

    query: str = Field(..., min_length=1, description="Search query (name or symbol)")
    market_type: Literal["KOSPI", "KOSDAQ", "ALL"] = Field(default="ALL", description="Market type filter")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of results")


class StockListResponse(BaseModel):
    """Response for stock list/search."""

    total: int = Field(..., description="Total number of stocks found")
    stocks: list[Stock] = Field(..., description="List of stocks")
