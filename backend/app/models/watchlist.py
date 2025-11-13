"""Watchlist model for user's favorite stocks."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Watchlist(Base):
    """User's watchlist (favorite stocks) model."""

    __tablename__ = "watchlists"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    symbol: Mapped[str] = mapped_column(
        String(10),
        ForeignKey("stocks.symbol"),
        nullable=False,
        index=True
    )

    # Watchlist information
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="watchlists")
    stock: Mapped["Stock"] = relationship("Stock")

    def __repr__(self) -> str:
        return f"<Watchlist(id={self.id}, user_id={self.user_id}, symbol={self.symbol}, name={self.name})>"
