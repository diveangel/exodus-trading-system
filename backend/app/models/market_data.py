"""MarketData model for storing OHLCV time-series data."""

from datetime import datetime
from sqlalchemy import String, DateTime, Float, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.db.base import Base


class TimeInterval(str, enum.Enum):
    """Time interval enumeration for market data."""
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    TEN_MINUTES = "10m"
    THIRTY_MINUTES = "30m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"


class MarketData(Base):
    """Market data model for OHLCV time-series data."""

    __tablename__ = "market_data"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Symbol and timestamp
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    # OHLCV data
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(Float, nullable=False)  # Using Float to handle large volumes

    # Time interval
    interval: Mapped[TimeInterval] = mapped_column(
        SQLEnum(TimeInterval, name="time_interval", native_enum=False),
        nullable=False,
        index=True
    )

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Composite indexes for efficient querying
    __table_args__ = (
        Index('idx_market_data_symbol_timestamp', 'symbol', 'timestamp'),
        Index('idx_market_data_symbol_interval_timestamp', 'symbol', 'interval', 'timestamp'),
        # Unique constraint to prevent duplicate data
        Index('idx_market_data_unique', 'symbol', 'timestamp', 'interval', unique=True),
    )

    def __repr__(self) -> str:
        return f"<MarketData(symbol={self.symbol}, timestamp={self.timestamp}, close={self.close}, interval={self.interval})>"
