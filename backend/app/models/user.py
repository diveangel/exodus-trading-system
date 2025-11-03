"""User model for authentication and user management."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class TradingMode(str, enum.Enum):
    """Trading mode enumeration."""
    MOCK = "MOCK"  # 모의투자
    REAL = "REAL"  # 실전투자


class User(Base):
    """User model for authentication and profile management."""

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Authentication
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Profile information
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole, name="user_role", native_enum=False),
        default=UserRole.USER,
        nullable=False
    )

    # Korea Investment API credentials (encrypted)
    kis_app_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    kis_app_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    kis_account_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    kis_account_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    has_kis_credentials: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    kis_trading_mode: Mapped[TradingMode] = mapped_column(
        SQLEnum(TradingMode, name="trading_mode", native_enum=False),
        default=TradingMode.MOCK,
        nullable=False
    )

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

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
    strategies: Mapped[List["Strategy"]] = relationship(
        "Strategy",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    orders: Mapped[List["Order"]] = relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    trades: Mapped[List["Trade"]] = relationship(
        "Trade",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    holdings: Mapped[List["Holding"]] = relationship(
        "Holding",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    backtest_results: Mapped[List["BacktestResult"]] = relationship(
        "BacktestResult",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
