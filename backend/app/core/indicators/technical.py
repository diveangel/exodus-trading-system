"""Technical indicators calculation."""

from typing import List, Literal


def calculate_sma(data: List[float], period: int) -> List[float]:
    """
    Calculate Simple Moving Average (SMA).

    Args:
        data: List of prices (e.g., closing prices)
        period: Moving average period

    Returns:
        List of SMA values (same length as input, with None for insufficient data points)

    Example:
        >>> prices = [100, 102, 101, 103, 105, 107, 106, 108, 110, 109]
        >>> sma_5 = calculate_sma(prices, 5)
        >>> # First 4 values will be None, then 5-period averages
    """
    if not data or period <= 0:
        return []

    if period > len(data):
        return [None] * len(data)

    sma_values = []

    # First (period - 1) values are None (not enough data points)
    for i in range(period - 1):
        sma_values.append(None)

    # Calculate SMA for remaining values
    for i in range(period - 1, len(data)):
        window = data[i - period + 1:i + 1]
        sma = sum(window) / period
        sma_values.append(sma)

    return sma_values


def calculate_ema(data: List[float], period: int) -> List[float]:
    """
    Calculate Exponential Moving Average (EMA).

    Args:
        data: List of prices (e.g., closing prices)
        period: EMA period

    Returns:
        List of EMA values (same length as input, with None for insufficient data points)

    Example:
        >>> prices = [100, 102, 101, 103, 105, 107, 106, 108, 110, 109]
        >>> ema_5 = calculate_ema(prices, 5)
    """
    if not data or period <= 0:
        return []

    if period > len(data):
        return [None] * len(data)

    ema_values = []
    multiplier = 2 / (period + 1)

    # First (period - 1) values are None
    for i in range(period - 1):
        ema_values.append(None)

    # First EMA value is SMA
    first_sma = sum(data[:period]) / period
    ema_values.append(first_sma)

    # Calculate EMA for remaining values
    # EMA = (Close - EMA(previous day)) * multiplier + EMA(previous day)
    for i in range(period, len(data)):
        ema = (data[i] - ema_values[-1]) * multiplier + ema_values[-1]
        ema_values.append(ema)

    return ema_values


def detect_crossover(
    fast_ma: List[float],
    slow_ma: List[float]
) -> Literal["golden", "death", "none"]:
    """
    Detect moving average crossover.

    Args:
        fast_ma: Fast moving average values (shorter period)
        slow_ma: Slow moving average values (longer period)

    Returns:
        "golden": Golden cross (fast MA crosses above slow MA) - BUY signal
        "death": Death cross (fast MA crosses below slow MA) - SELL signal
        "none": No crossover detected

    Example:
        >>> fast_ma = [100, 101, 102, 103, 104]  # Rising
        >>> slow_ma = [102, 102, 102, 102, 102]  # Flat
        >>> # If fast_ma[-2] < slow_ma[-2] and fast_ma[-1] > slow_ma[-1] => golden cross
    """
    if not fast_ma or not slow_ma:
        return "none"

    if len(fast_ma) < 2 or len(slow_ma) < 2:
        return "none"

    # Check if we have valid values for last 2 periods
    if (fast_ma[-1] is None or fast_ma[-2] is None or
            slow_ma[-1] is None or slow_ma[-2] is None):
        return "none"

    # Current and previous values
    fast_current = fast_ma[-1]
    fast_previous = fast_ma[-2]
    slow_current = slow_ma[-1]
    slow_previous = slow_ma[-2]

    # Golden cross: fast MA crosses above slow MA
    # Previous: fast < slow, Current: fast > slow
    if fast_previous < slow_previous and fast_current > slow_current:
        return "golden"

    # Death cross: fast MA crosses below slow MA
    # Previous: fast > slow, Current: fast < slow
    if fast_previous > slow_previous and fast_current < slow_current:
        return "death"

    return "none"
