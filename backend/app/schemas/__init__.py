"""Pydantic schemas module."""

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    RealKISCredentialsUpdate,
    MockKISCredentialsUpdate,
    UserResponse,
    UserDetailResponse,
    UserLogin,
    Token,
    TokenData,
)
from app.schemas.strategy import (
    StrategyCreate,
    StrategyUpdate,
    StrategyResponse,
    StrategyListResponse,
)
from app.schemas.signal import (
    SignalCreate,
    SignalUpdate,
    SignalResponse,
    SignalListResponse,
)
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderListResponse,
    TradeCreate,
    TradeResponse,
    TradeListResponse,
)
from app.schemas.holding import (
    HoldingCreate,
    HoldingUpdate,
    HoldingResponse,
    HoldingListResponse,
    PortfolioSummary,
)
from app.schemas.market_data import (
    MarketDataCreate,
    MarketDataResponse,
    MarketDataListResponse,
    PriceResponse,
    ChartDataResponse,
)
from app.schemas.backtest import (
    BacktestConfig,
    BacktestRun,
    BacktestMetrics,
    BacktestResultResponse,
    BacktestResultListResponse,
    BacktestTradeResponse,
    BacktestTradeListResponse,
    BacktestSummary,
)

__all__ = [
    # User
    "UserCreate",
    "UserUpdate",
    "RealKISCredentialsUpdate",
    "MockKISCredentialsUpdate",
    "UserResponse",
    "UserDetailResponse",
    "UserLogin",
    "Token",
    "TokenData",
    # Strategy
    "StrategyCreate",
    "StrategyUpdate",
    "StrategyResponse",
    "StrategyListResponse",
    # Signal
    "SignalCreate",
    "SignalUpdate",
    "SignalResponse",
    "SignalListResponse",
    # Order and Trade
    "OrderCreate",
    "OrderUpdate",
    "OrderResponse",
    "OrderListResponse",
    "TradeCreate",
    "TradeResponse",
    "TradeListResponse",
    # Holding
    "HoldingCreate",
    "HoldingUpdate",
    "HoldingResponse",
    "HoldingListResponse",
    "PortfolioSummary",
    # Market Data
    "MarketDataCreate",
    "MarketDataResponse",
    "MarketDataListResponse",
    "PriceResponse",
    "ChartDataResponse",
    # Backtest
    "BacktestConfig",
    "BacktestRun",
    "BacktestMetrics",
    "BacktestResultResponse",
    "BacktestResultListResponse",
    "BacktestTradeResponse",
    "BacktestTradeListResponse",
    "BacktestSummary",
]
