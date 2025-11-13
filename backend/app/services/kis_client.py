"""Korea Investment & Securities API Base Client."""

import httpx
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from app.config import settings
from app.services.kis_token_manager import KISTokenManager, KISToken

logger = logging.getLogger(__name__)

# KIS API URLs
KIS_MOCK_URL = "https://openapivts.koreainvestment.com:29443"  # 모의투자
KIS_REAL_URL = "https://openapi.koreainvestment.com:9443"  # 실전투자


class KISClient:
    """
    Base client for interacting with Korea Investment & Securities API.

    This class handles:
    - Authentication and token management
    - Common request headers
    - Base URL configuration

    Specific API operations are implemented in separate modules:
    - kis_quotation.py: Market data and price queries
    - kis_account.py: Account balance and order history
    - kis_trading.py: Order placement and trading
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        account_number: str,
        account_code: str,
        trading_mode: str = "MOCK",
        base_url: Optional[str] = None
    ):
        """
        Initialize KIS base client.

        Args:
            app_key: KIS API app key
            app_secret: KIS API app secret
            account_number: Trading account number
            account_code: Trading account code
            trading_mode: Trading mode ("MOCK" or "REAL")
            base_url: Optional base URL (overrides trading_mode)
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.account_number = account_number
        self.account_code = account_code
        self.trading_mode = trading_mode

        # Set base URL based on trading mode
        if base_url:
            self.base_url = base_url
        elif trading_mode == "REAL":
            self.base_url = KIS_REAL_URL
        else:
            self.base_url = KIS_MOCK_URL

        # Initialize token manager for persistent token storage
        self._token_manager = KISTokenManager(app_key=app_key, trading_mode=trading_mode.lower())
        self._access_token: Optional[KISToken] = None

        logger.info(f"[KISClient] Initialized")
        logger.info(f"  - Trading Mode: {trading_mode}")
        logger.info(f"  - Base URL: {self.base_url}")
        logger.info(f"  - Account: {account_number}")

    async def _ensure_token(self) -> None:
        """
        Ensure we have a valid access token.

        Flow:
        1. Check if in-memory token exists and is valid
        2. If not, try to load from file
        3. If file token is invalid/missing, request new token from API
        4. Save new token to file
        """
        # Check in-memory token first
        if self._access_token and not self._access_token.is_expired():
            logger.debug(f"[KISClient] Using in-memory token")
            return

        # Try to load from file
        logger.info(f"[KISClient] Checking for cached token...")
        self._access_token = self._token_manager.load_token()

        if self._access_token:
            logger.info(f"[KISClient] Using cached token from file")
            return

        # Request new token from API
        logger.info(f"[KISClient] No valid cached token, requesting new token...")
        self._access_token = await self._request_new_token()

        # Save to file for future use
        self._token_manager.save_token(self._access_token)

    def _get_headers(self, tr_id: str) -> Dict[str, str]:
        """
        Get request headers with authentication.

        Args:
            tr_id: Transaction ID for the API call

        Returns:
            Dictionary of headers
        """
        return {
            "Content-Type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": tr_id,
        }

    async def _request_new_token(self) -> KISToken:
        """
        Request new OAuth access token from KIS API.

        Returns:
            KISToken object

        Raises:
            httpx.HTTPStatusError: If API returns error status
            Exception: For other errors
        """
        url = f"{self.base_url}/oauth2/tokenP"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
        }

        logger.info(f"[KIS API] Requesting new access token")
        logger.info(f"  - URL: {url}")
        logger.info(f"  - App Key (first 10 chars): {self.app_key[:10]}...")
        logger.info(f"  - App Secret (first 10 chars): {self.app_secret[:10]}...")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)

                logger.info(f"[KIS API] Response Status: {response.status_code}")

                # Log detailed error information
                if response.status_code != 200:
                    logger.error(f"[KIS API] Error Response:")
                    logger.error(f"  - Status: {response.status_code}")
                    logger.error(f"  - Body: {response.text}")
                    logger.error(f"  - Headers: {dict(response.headers)}")

                response.raise_for_status()
                data = response.json()

                logger.info(f"[KIS API] Token Response:")
                logger.info(f"  - Access Token (first 20 chars): {data.get('access_token', '')[:20]}...")
                logger.info(f"  - Expires In: {data.get('expires_in')} seconds")
                logger.info(f"  - Token Type: {data.get('token_type')}")

                return KISToken(
                    access_token=data["access_token"],
                    token_type=data["token_type"],
                    expires_in=data["expires_in"],
                    issued_at=datetime.now(),
                )

        except httpx.HTTPStatusError as e:
            logger.error(f"[KIS API] HTTP Error: {e}")
            logger.error(f"  - Response: {e.response.text if hasattr(e, 'response') else 'N/A'}")
            raise
        except Exception as e:
            logger.error(f"[KIS API] Unexpected error: {e}")
            raise

    async def get(self, url: str, headers: Dict[str, str], params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make authenticated GET request to KIS API.

        Args:
            url: Full API endpoint URL
            headers: Request headers (from _get_headers)
            params: Query parameters

        Returns:
            API response as dictionary
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()

    async def post(self, url: str, headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make authenticated POST request to KIS API.

        Args:
            url: Full API endpoint URL
            headers: Request headers (from _get_headers)
            payload: Request body

        Returns:
            API response as dictionary
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
