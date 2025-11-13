"""Base strategy class."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from app.core.strategy.types import StrategyType, StrategyStatus, Signal


class BaseStrategy(ABC):
    """Abstract base class for all trading strategies."""

    def __init__(
        self,
        name: str,
        strategy_type: StrategyType,
        parameters: Dict[str, Any],
        status: StrategyStatus = StrategyStatus.INACTIVE
    ):
        """
        Initialize base strategy.

        Args:
            name: Strategy name
            strategy_type: Strategy type enum
            parameters: Strategy parameters
            status: Initial status
        """
        self.name = name
        self.strategy_type = strategy_type
        self.parameters = parameters
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    @abstractmethod
    async def generate_signals(
        self,
        symbol: str,
        market_data: List[Dict[str, Any]],
        current_price: float
    ) -> List[Signal]:
        """
        Generate trading signals based on market data.

        Args:
            symbol: Stock symbol
            market_data: Historical market data
            current_price: Current stock price

        Returns:
            List of trading signals
        """
        pass

    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters.

        Returns:
            True if parameters are valid

        Raises:
            ValueError: If required parameters are missing
        """
        required_params = self.get_required_parameters()
        for param in required_params:
            if param not in self.parameters:
                raise ValueError(f"Missing required parameter: {param}")
        return True

    @abstractmethod
    def get_required_parameters(self) -> List[str]:
        """
        Get list of required parameters for this strategy.

        Returns:
            List of parameter names
        """
        pass

    def get_required_data_period(self) -> int:
        """
        Calculate required data period in days.

        Returns:
            Number of days of historical data needed
        """
        # Default: 60 days
        return 60

    def update_status(self, status: StrategyStatus) -> None:
        """
        Update strategy status.

        Args:
            status: New status
        """
        self.status = status
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert strategy to dictionary.

        Returns:
            Dictionary representation
        """
        return {
            "name": self.name,
            "strategy_type": self.strategy_type.value,
            "parameters": self.parameters,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
