"""Strategy model for investment strategies."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class StrategyType(str, enum.Enum):
    """Strategy type enumeration."""
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    FACTOR = "factor"
    CUSTOM = "custom"


class Strategy(Base):
    """Investment strategy model."""

    __tablename__ = "strategies"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key to user
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Strategy information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    strategy_type: Mapped[StrategyType] = mapped_column(
        SQLEnum(StrategyType, name="strategy_type", native_enum=False),
        nullable=False
    )

    # Strategy parameters (stored as JSON)
    # Example: {"short_window": 5, "long_window": 20, "rsi_period": 14}
    parameters: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="strategies")
    signals: Mapped[List["Signal"]] = relationship(
        "Signal",
        back_populates="strategy",
        cascade="all, delete-orphan"
    )
    backtest_results: Mapped[List["BacktestResult"]] = relationship(
        "BacktestResult",
        back_populates="strategy",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Strategy(id={self.id}, name={self.name}, type={self.strategy_type})>"
