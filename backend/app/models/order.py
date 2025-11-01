"""Order and Trade models for order execution and trading history."""

from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Integer, Float, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class OrderType(str, enum.Enum):
    """Order type enumeration."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"


class OrderSide(str, enum.Enum):
    """Order side enumeration."""
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, enum.Enum):
    """Order status enumeration."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    PARTIALLY_FILLED = "partially_filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


class Order(Base):
    """Order model for tracking order execution."""

    __tablename__ = "orders"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    signal_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("signals.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Order details
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    order_type: Mapped[OrderType] = mapped_column(
        SQLEnum(OrderType, name="order_type", native_enum=False),
        nullable=False
    )
    side: Mapped[OrderSide] = mapped_column(
        SQLEnum(OrderSide, name="order_side", native_enum=False),
        nullable=False
    )

    # Quantity and price
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # None for market orders

    # Execution details
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus, name="order_status", native_enum=False),
        default=OrderStatus.PENDING,
        nullable=False,
        index=True
    )
    filled_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    filled_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Fees
    commission: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    tax: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # External reference (KIS API order ID)
    external_order_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    filled_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    signal: Mapped[Optional["Signal"]] = relationship("Signal", back_populates="orders")
    trades: Mapped[list["Trade"]] = relationship(
        "Trade",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    # Indexes
    __table_args__ = (
        Index('idx_orders_user_created', 'user_id', 'created_at'),
        Index('idx_orders_symbol_created', 'symbol', 'created_at'),
        Index('idx_orders_status_created', 'status', 'created_at'),
    )

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, symbol={self.symbol}, side={self.side}, status={self.status})>"


class Trade(Base):
    """Trade model for executed trades."""

    __tablename__ = "trades"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign keys
    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Trade details
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    side: Mapped[OrderSide] = mapped_column(
        SQLEnum(OrderSide, name="trade_side", native_enum=False),
        nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Fees
    commission: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    tax: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Total amount (quantity * price + commission + tax for buy, quantity * price - commission - tax for sell)
    total_amount: Mapped[float] = mapped_column(Float, nullable=False)

    # Timestamps
    executed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="trades")
    user: Mapped["User"] = relationship("User", back_populates="trades")

    # Indexes
    __table_args__ = (
        Index('idx_trades_user_executed', 'user_id', 'executed_at'),
        Index('idx_trades_symbol_executed', 'symbol', 'executed_at'),
    )

    def __repr__(self) -> str:
        return f"<Trade(id={self.id}, symbol={self.symbol}, side={self.side}, qty={self.quantity}, price={self.price})>"
