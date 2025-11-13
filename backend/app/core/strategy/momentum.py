"""Momentum strategy implementation."""

import logging
from typing import Dict, Any, List
from datetime import datetime

from app.core.strategy.base import BaseStrategy
from app.core.strategy.types import StrategyType, Signal, SignalType
from app.core.indicators import calculate_sma, calculate_ema, detect_crossover

logger = logging.getLogger(__name__)


class MomentumStrategy(BaseStrategy):
    """
    Momentum strategy based on Moving Average crossover.

    This strategy generates:
    - BUY signal: Golden cross (fast MA crosses above slow MA)
    - SELL signal: Death cross (fast MA crosses below slow MA)
    - HOLD signal: No crossover detected

    Required Parameters:
    - fast_period: Fast moving average period (e.g., 5)
    - slow_period: Slow moving average period (e.g., 20)
    - ma_type: Moving average type ("SMA" or "EMA")
    """

    def __init__(
        self,
        name: str,
        parameters: Dict[str, Any],
        **kwargs
    ):
        """
        Initialize momentum strategy.

        Args:
            name: Strategy name
            parameters: Strategy parameters
            **kwargs: Additional arguments for BaseStrategy
        """
        super().__init__(
            name=name,
            strategy_type=StrategyType.MOMENTUM,
            parameters=parameters,
            **kwargs
        )

        # Validate parameters on initialization
        self.validate_parameters()

    def get_required_parameters(self) -> List[str]:
        """
        Get required parameter names.

        Supports both naming conventions:
        - fast_period/slow_period (original)
        - short_window/long_window (alternative)

        Returns:
            List of required parameter names
        """
        # Check which parameter naming convention is used
        if "short_window" in self.parameters or "long_window" in self.parameters:
            return ["short_window", "long_window"]
        return ["fast_period", "slow_period"]

    def get_required_data_period(self) -> int:
        """
        Calculate required data period.

        Returns:
            Number of days needed (slow_period * 2 for stability)
        """
        # Support both naming conventions
        slow_period = self.parameters.get("slow_period") or self.parameters.get("long_window", 20)
        return slow_period * 2

    async def generate_signals(
        self,
        symbol: str,
        market_data: List[Dict[str, Any]],
        current_price: float
    ) -> List[Signal]:
        """
        Generate trading signals based on MA crossover.

        Args:
            symbol: Stock symbol
            market_data: Historical market data (list of dicts with 'close' prices)
            current_price: Current stock price

        Returns:
            List of signals (usually one signal or empty list)
        """
        try:
            # Extract parameters - support both naming conventions
            fast_period = self.parameters.get("fast_period") or self.parameters.get("short_window")
            slow_period = self.parameters.get("slow_period") or self.parameters.get("long_window")
            ma_type = self.parameters.get("ma_type", "SMA").upper()

            if not fast_period or not slow_period:
                raise ValueError("Missing required parameters: fast_period/short_window and slow_period/long_window")

            # Validate data
            if len(market_data) < slow_period:
                logger.warning(
                    f"[{self.name}] Insufficient data: {len(market_data)} < {slow_period}"
                )
                return []

            # Extract closing prices
            close_prices = [float(data["close"]) for data in market_data]

            # Calculate moving averages
            if ma_type == "EMA":
                fast_ma = calculate_ema(close_prices, fast_period)
                slow_ma = calculate_ema(close_prices, slow_period)
            else:  # SMA
                fast_ma = calculate_sma(close_prices, fast_period)
                slow_ma = calculate_sma(close_prices, slow_period)

            # Detect crossover
            crossover = detect_crossover(fast_ma, slow_ma)

            # Generate signal based on crossover
            if crossover == "golden":
                # BUY signal
                confidence = self._calculate_confidence(fast_ma, slow_ma, "golden")
                signal = Signal(
                    timestamp=datetime.now(),
                    symbol=symbol,
                    signal_type=SignalType.BUY,
                    price=current_price,
                    quantity=None,  # Quantity should be determined by risk management
                    reason=f"Golden cross detected: {ma_type}{fast_period} crossed above {ma_type}{slow_period}",
                    confidence=confidence
                )
                logger.info(f"[{self.name}] BUY signal generated for {symbol}: {signal.reason}")
                return [signal]

            elif crossover == "death":
                # SELL signal
                confidence = self._calculate_confidence(fast_ma, slow_ma, "death")
                signal = Signal(
                    timestamp=datetime.now(),
                    symbol=symbol,
                    signal_type=SignalType.SELL,
                    price=current_price,
                    quantity=None,
                    reason=f"Death cross detected: {ma_type}{fast_period} crossed below {ma_type}{slow_period}",
                    confidence=confidence
                )
                logger.info(f"[{self.name}] SELL signal generated for {symbol}: {signal.reason}")
                return [signal]

            else:
                # HOLD - no crossover
                logger.debug(f"[{self.name}] No crossover detected for {symbol}")
                return []

        except KeyError as e:
            logger.error(f"[{self.name}] Missing parameter: {e}")
            raise
        except Exception as e:
            logger.error(f"[{self.name}] Error generating signals: {e}")
            raise

    def _calculate_confidence(
        self,
        fast_ma: List[float],
        slow_ma: List[float],
        crossover_type: str
    ) -> float:
        """
        Calculate signal confidence based on MA separation.

        Args:
            fast_ma: Fast moving average values
            slow_ma: Slow moving average values
            crossover_type: "golden" or "death"

        Returns:
            Confidence score (0-1)
        """
        if not fast_ma or not slow_ma:
            return 0.5

        # Get current values
        fast_current = fast_ma[-1]
        slow_current = slow_ma[-1]

        if fast_current is None or slow_current is None:
            return 0.5

        # Calculate percentage difference
        diff_percent = abs(fast_current - slow_current) / slow_current * 100

        # Higher separation = higher confidence
        # 0-1%: 0.6, 1-2%: 0.7, 2-3%: 0.8, 3%+: 0.9
        if diff_percent < 1:
            confidence = 0.6
        elif diff_percent < 2:
            confidence = 0.7
        elif diff_percent < 3:
            confidence = 0.8
        else:
            confidence = 0.9

        logger.debug(
            f"Confidence calculation: diff={diff_percent:.2f}%, confidence={confidence:.2f}"
        )

        return confidence
