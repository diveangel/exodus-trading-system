"""Order and Trade Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.models.order import OrderType, OrderSide, OrderStatus


# Order schemas
class OrderBase(BaseModel):
    """Base order schema."""
    symbol: str = Field(..., min_length=1, max_length=20)
    order_type: OrderType
    side: OrderSide
    quantity: int = Field(..., gt=0)
    price: Optional[float] = Field(None, gt=0)


class OrderCreate(OrderBase):
    """Schema for creating a new order."""
    signal_id: Optional[int] = None


class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    status: Optional[OrderStatus] = None
    filled_quantity: Optional[int] = Field(None, ge=0)
    filled_price: Optional[float] = Field(None, gt=0)
    commission: Optional[float] = Field(None, ge=0)
    tax: Optional[float] = Field(None, ge=0)
    external_order_id: Optional[str] = None


class OrderResponse(OrderBase):
    """Schema for order response."""
    id: int
    user_id: int
    signal_id: Optional[int] = None
    status: OrderStatus
    filled_quantity: int
    filled_price: Optional[float] = None
    commission: float
    tax: float
    external_order_id: Optional[str] = None
    created_at: datetime
    submitted_at: Optional[datetime] = None
    filled_at: Optional[datetime] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(BaseModel):
    """Schema for paginated order list."""
    orders: list[OrderResponse]
    total: int
    page: int
    page_size: int


# Trade schemas
class TradeBase(BaseModel):
    """Base trade schema."""
    symbol: str = Field(..., min_length=1, max_length=20)
    side: OrderSide
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    commission: float = Field(default=0.0, ge=0)
    tax: float = Field(default=0.0, ge=0)
    total_amount: float


class TradeCreate(TradeBase):
    """Schema for creating a new trade."""
    order_id: int
    user_id: int


class TradeResponse(TradeBase):
    """Schema for trade response."""
    id: int
    order_id: int
    user_id: int
    executed_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TradeListResponse(BaseModel):
    """Schema for paginated trade list."""
    trades: list[TradeResponse]
    total: int
    page: int
    page_size: int
