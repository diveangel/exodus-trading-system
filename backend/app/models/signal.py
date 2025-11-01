"""Signal model for trading signals."""

from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, Boolean, DateTime, Integer, Float, ForeignKey, Enum as SQLEnum, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class SignalType(str, enum.Enum):
    """Signal type enumeration."""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class Signal(Base):
    """Trading signal model."""

    __tablename__ = "signals"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key to strategy
    strategy_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("strategies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Signal information
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    signal_type: Mapped[SignalType] = mapped_column(
        SQLEnum(SignalType, name="signal_type", native_enum=False),
        nullable=False
    )

    # Signal details
    confidence: Mapped[float] = mapped_column(Float, nullable=False)  # 0.0 to 1.0
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Signal reason (JSON with strategy details)
    # Example: {"indicator": "SMA_CROSS", "short_ma": 50.5, "long_ma": 48.2}
    reason: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )

    # Execution status
    is_executed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # Relationships
    strategy: Mapped["Strategy"] = relationship("Strategy", back_populates="signals")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="signal")

    # Indexes
    __table_args__ = (
        Index('idx_signals_strategy_created', 'strategy_id', 'created_at'),
        Index('idx_signals_symbol_created', 'symbol', 'created_at'),
    )

    def __repr__(self) -> str:
        return f"<Signal(id={self.id}, symbol={self.symbol}, type={self.signal_type}, executed={self.is_executed})>"
