"""Dashboard response schemas."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DashboardStats(BaseModel):
    """Dashboard statistics summary."""

    total_balance: float = Field(..., description="Total account balance in KRW")
    profit_loss: float = Field(..., description="Total profit/loss in KRW")
    profit_loss_percent: float = Field(..., description="Total profit/loss percentage")
    active_strategies: int = Field(..., description="Number of active strategies")
    today_trades: int = Field(..., description="Number of trades executed today")


class ActiveStrategy(BaseModel):
    """Active strategy summary for dashboard."""

    id: int
    name: str
    status: str
    profit_loss: float = Field(..., description="Strategy profit/loss in KRW")
    profit_loss_percent: float = Field(..., description="Strategy profit/loss percentage")


class RecentActivity(BaseModel):
    """Recent trading activity."""

    id: int
    type: str = Field(..., description="Trade type: BUY or SELL")
    symbol: str = Field(..., description="Stock symbol/name")
    quantity: int = Field(..., description="Number of shares")
    price: float = Field(..., description="Execution price per share")
    time: str = Field(..., description="Execution time (HH:MM:SS)")
    created_at: Optional[datetime] = None


class DashboardResponse(BaseModel):
    """Complete dashboard data response."""

    stats: DashboardStats
    active_strategies: List[ActiveStrategy] = []
    recent_activities: List[RecentActivity] = []

    class Config:
        from_attributes = True
