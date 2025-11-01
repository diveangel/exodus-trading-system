"""Holding model for current portfolio positions."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Holding(Base):
    """Holding model for current portfolio positions."""

    __tablename__ = "holdings"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Stock information
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Position details
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    average_price: Mapped[float] = mapped_column(Float, nullable=False)
    current_price: Mapped[float] = mapped_column(Float, nullable=False)

    # Calculated values
    total_cost: Mapped[float] = mapped_column(Float, nullable=False)  # quantity * average_price
    current_value: Mapped[float] = mapped_column(Float, nullable=False)  # quantity * current_price
    unrealized_pnl: Mapped[float] = mapped_column(Float, nullable=False)  # current_value - total_cost
    unrealized_pnl_percent: Mapped[float] = mapped_column(Float, nullable=False)  # (unrealized_pnl / total_cost) * 100

    # Timestamps
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="holdings")

    # Indexes
    __table_args__ = (
        Index('idx_holdings_user_symbol', 'user_id', 'symbol', unique=True),
    )

    def __repr__(self) -> str:
        return f"<Holding(id={self.id}, symbol={self.symbol}, qty={self.quantity}, pnl={self.unrealized_pnl:.2f})>"
