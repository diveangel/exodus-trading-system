"""MarketData Pydantic schemas for request/response validation."""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.models.market_data import TimeInterval


class MarketDataBase(BaseModel):
    """Base market data schema."""
    symbol: str = Field(..., min_length=1, max_length=20)
    timestamp: datetime
    open: float = Field(..., gt=0)
    high: float = Field(..., gt=0)
    low: float = Field(..., gt=0)
    close: float = Field(..., gt=0)
    volume: float = Field(..., ge=0)
    interval: TimeInterval


class MarketDataCreate(MarketDataBase):
    """Schema for creating market data."""
    pass


class MarketDataResponse(MarketDataBase):
    """Schema for market data response."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MarketDataListResponse(BaseModel):
    """Schema for market data list."""
    data: list[MarketDataResponse]
    symbol: str
    interval: TimeInterval
    start_date: datetime
    end_date: datetime
    total: int


class PriceResponse(BaseModel):
    """Schema for current price response."""
    symbol: str
    price: float
    change: float
    change_percent: float
    volume: float
    timestamp: datetime


class ChartDataPoint(BaseModel):
    """Schema for a single chart data point."""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class ChartDataResponse(BaseModel):
    """Schema for chart data response."""
    symbol: str
    interval: TimeInterval
    data: list[ChartDataPoint]
