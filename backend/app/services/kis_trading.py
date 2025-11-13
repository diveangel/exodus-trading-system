"""KIS API - Trading & Order Services."""

import logging
from typing import Dict, Any

from app.services.kis_client import KISClient

logger = logging.getLogger(__name__)


class KISTrading:
    """
    KIS API client for trading and order services.

    This class provides methods for:
    - Placing buy/sell orders
    - Order modification
    - Order cancellation
    """

    def __init__(self, client: KISClient):
        """
        Initialize KIS Trading service.

        Args:
            client: Authenticated KIS base client
        """
        self.client = client

    async def place_order(
        self,
        symbol: str,
        order_type: str,
        quantity: int,
        price: int
    ) -> Dict[str, Any]:
        """
        Place a buy or sell order.

        Args:
            symbol: Stock symbol
            order_type: "buy" or "sell"
            quantity: Number of shares
            price: Price per share

        Returns:
            Dictionary containing order result
        """
        await self.client._ensure_token()

        # Different TR IDs for buy and sell
        tr_id = "TTTC0802U" if order_type == "buy" else "TTTC0801U"

        url = f"{self.client.base_url}/uapi/domestic-stock/v1/trading/order-cash"
        headers = self.client._get_headers(tr_id)
        payload = {
            "CANO": self.client.account_number,
            "ACNT_PRDT_CD": self.client.account_code,
            "PDNO": symbol,
            "ORD_DVSN": "00",
            "ORD_QTY": str(quantity),
            "ORD_UNPR": str(price),
        }

        logger.info(f"[KIS Trading] Placing {order_type} order")
        logger.info(f"  - Symbol: {symbol}")
        logger.info(f"  - Quantity: {quantity}")
        logger.info(f"  - Price: {price}")

        return await self.client.post(url, headers, payload)
