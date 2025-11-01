"""Backtest models for strategy backtesting results."""

from datetime import datetime, date
from typing import Optional, Dict, Any, List
from sqlalchemy import String, DateTime, Date, Integer, Float, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BacktestResult(Base):
    """Backtest result model for storing backtest performance metrics."""

    __tablename__ = "backtest_results"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    strategy_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("strategies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Backtest configuration
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    initial_capital: Mapped[float] = mapped_column(Float, nullable=False)
    final_capital: Mapped[float] = mapped_column(Float, nullable=False)

    # Performance metrics
    total_return: Mapped[float] = mapped_column(Float, nullable=False)  # Percentage
    annual_return: Mapped[float] = mapped_column(Float, nullable=False)  # Percentage
    max_drawdown: Mapped[float] = mapped_column(Float, nullable=False)  # Percentage
    sharpe_ratio: Mapped[float] = mapped_column(Float, nullable=False)

    # Trading statistics
    total_trades: Mapped[int] = mapped_column(Integer, nullable=False)
    winning_trades: Mapped[int] = mapped_column(Integer, nullable=False)
    losing_trades: Mapped[int] = mapped_column(Integer, nullable=False)
    win_rate: Mapped[float] = mapped_column(Float, nullable=False)  # Percentage

    # Profit/Loss statistics
    average_win: Mapped[float] = mapped_column(Float, nullable=False)
    average_loss: Mapped[float] = mapped_column(Float, nullable=False)
    profit_loss_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    largest_win: Mapped[float] = mapped_column(Float, nullable=False)
    largest_loss: Mapped[float] = mapped_column(Float, nullable=False)

    # Additional metrics
    average_holding_period: Mapped[float] = mapped_column(Float, nullable=False)  # Days

    # Detailed results stored as JSON
    # Example: {"daily_returns": [...], "equity_curve": [...], "drawdown_curve": [...]}
    results_detail: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # Relationships
    strategy: Mapped["Strategy"] = relationship("Strategy", back_populates="backtest_results")
    user: Mapped["User"] = relationship("User", back_populates="backtest_results")
    trades: Mapped[List["BacktestTrade"]] = relationship(
        "BacktestTrade",
        back_populates="backtest",
        cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index('idx_backtest_user_created', 'user_id', 'created_at'),
        Index('idx_backtest_strategy_created', 'strategy_id', 'created_at'),
    )

    def __repr__(self) -> str:
        return f"<BacktestResult(id={self.id}, name={self.name}, return={self.total_return:.2f}%)>"


class BacktestTrade(Base):
    """Backtest trade model for individual trades during backtest."""

    __tablename__ = "backtest_trades"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key
    backtest_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("backtest_results.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Trade details
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    side: Mapped[str] = mapped_column(String(10), nullable=False)  # buy or sell
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Fees
    commission: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Trade metadata
    trade_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # Signal reason (JSON)
    signal_reason: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    backtest: Mapped["BacktestResult"] = relationship("BacktestResult", back_populates="trades")

    # Indexes
    __table_args__ = (
        Index('idx_backtest_trades_backtest_date', 'backtest_id', 'trade_date'),
    )

    def __repr__(self) -> str:
        return f"<BacktestTrade(id={self.id}, symbol={self.symbol}, side={self.side}, qty={self.quantity})>"
