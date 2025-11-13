"""Strategy types and enums."""

from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class StrategyType(str, Enum):
    """Trading strategy types."""
    MOMENTUM = "MOMENTUM"
    MEAN_REVERSION = "MEAN_REVERSION"
    BREAKOUT = "BREAKOUT"
    CUSTOM = "CUSTOM"


class SignalType(str, Enum):
    """Trading signal types."""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


class StrategyStatus(str, Enum):
    """Strategy execution status."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BACKTESTING = "BACKTESTING"


class Signal(BaseModel):
    """Trading signal model."""
    timestamp: datetime = Field(..., description="Signal generation timestamp")
    symbol: str = Field(..., description="Stock symbol")
    signal_type: SignalType = Field(..., description="Signal type (BUY/SELL/HOLD)")
    price: float = Field(..., description="Current price at signal generation")
    quantity: Optional[int] = Field(None, description="Recommended quantity")
    reason: str = Field(..., description="Signal generation reason")
    confidence: float = Field(..., ge=0, le=1, description="Signal confidence (0-1)")

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-11-04T10:30:00",
                "symbol": "005930",
                "signal_type": "BUY",
                "price": 75000,
                "quantity": 10,
                "reason": "Golden cross detected (MA5 > MA20)",
                "confidence": 0.85
            }
        }
