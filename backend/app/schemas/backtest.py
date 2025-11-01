"""Backtest Pydantic schemas for request/response validation."""

from datetime import datetime, date
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


# Backtest Result schemas
class BacktestConfig(BaseModel):
    """Schema for backtest configuration."""
    strategy_id: int
    name: str = Field(..., min_length=1, max_length=100)
    start_date: date
    end_date: date
    initial_capital: float = Field(..., gt=0)
    symbols: Optional[list[str]] = None  # Optional: specific symbols to test


class BacktestRun(BaseModel):
    """Schema for running a backtest."""
    config: BacktestConfig


class BacktestMetrics(BaseModel):
    """Schema for backtest performance metrics."""
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    average_win: float
    average_loss: float
    profit_loss_ratio: float
    largest_win: float
    largest_loss: float
    average_holding_period: float


class BacktestResultResponse(BaseModel):
    """Schema for backtest result response."""
    id: int
    strategy_id: int
    user_id: int
    name: str
    start_date: date
    end_date: date
    initial_capital: float
    final_capital: float

    # Performance metrics
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe_ratio: float

    # Trading statistics
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float

    # P&L statistics
    average_win: float
    average_loss: float
    profit_loss_ratio: float
    largest_win: float
    largest_loss: float

    average_holding_period: float
    results_detail: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BacktestResultListResponse(BaseModel):
    """Schema for paginated backtest result list."""
    results: list[BacktestResultResponse]
    total: int
    page: int
    page_size: int


# Backtest Trade schemas
class BacktestTradeResponse(BaseModel):
    """Schema for backtest trade response."""
    id: int
    backtest_id: int
    symbol: str
    side: str
    quantity: int
    price: float
    commission: float
    trade_date: date
    signal_reason: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BacktestTradeListResponse(BaseModel):
    """Schema for backtest trades list."""
    trades: list[BacktestTradeResponse]
    total: int


# Backtest summary for quick overview
class BacktestSummary(BaseModel):
    """Schema for backtest summary."""
    id: int
    name: str
    strategy_id: int
    start_date: date
    end_date: date
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    total_trades: int
    win_rate: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
