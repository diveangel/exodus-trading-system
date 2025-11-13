"""Watchlist schemas for API request/response."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WatchlistBase(BaseModel):
    """Base watchlist schema."""

    symbol: str = Field(..., description="Stock symbol")
    name: Optional[str] = Field(None, description="Watchlist group name")
    notes: Optional[str] = Field(None, description="Notes about this stock")


class WatchlistCreate(WatchlistBase):
    """Schema for creating a watchlist entry."""

    pass


class WatchlistUpdate(BaseModel):
    """Schema for updating a watchlist entry."""

    name: Optional[str] = None
    notes: Optional[str] = None


class WatchlistResponse(WatchlistBase):
    """Watchlist response schema with all fields."""

    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WatchlistListResponse(BaseModel):
    """Response for watchlist list."""

    total: int = Field(..., description="Total number of watchlist entries")
    watchlists: list[WatchlistResponse] = Field(..., description="List of watchlist entries")
