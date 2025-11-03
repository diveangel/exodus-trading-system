"""KIS API Token Manager - Handles token persistence and lifecycle."""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class KISToken(BaseModel):
    """KIS authentication token model."""
    access_token: str
    token_type: str
    expires_in: int
    issued_at: datetime

    def is_expired(self, buffer_seconds: int = 300) -> bool:
        """
        Check if token is expired.

        Args:
            buffer_seconds: Safety buffer before actual expiration (default: 5 minutes)

        Returns:
            True if token is expired or will expire soon
        """
        if self.expires_in < 0:
            return True

        expiry_time = self.issued_at + timedelta(seconds=self.expires_in - buffer_seconds)
        is_expired = datetime.now() >= expiry_time

        if is_expired:
            logger.info(f"[Token] Token expired at {expiry_time}")

        return is_expired

    def get_expiry_datetime(self) -> datetime:
        """Get the exact expiry datetime."""
        return self.issued_at + timedelta(seconds=self.expires_in)


class KISTokenManager:
    """Manages KIS API token persistence and lifecycle."""

    def __init__(self, app_key: str, trading_mode: str = "mock"):
        """
        Initialize token manager.

        Args:
            app_key: KIS API app key (used for unique token file naming)
            trading_mode: Trading mode ("mock" or "real")
        """
        self.app_key = app_key
        self.trading_mode = trading_mode

        # Create token storage directory
        self.token_dir = Path.home() / "KIS" / "tokens"
        self.token_dir.mkdir(parents=True, exist_ok=True)

        # Token file path: ~/KIS/tokens/token_{app_key_prefix}_{mode}.json
        app_key_prefix = app_key[:10] if len(app_key) >= 10 else app_key
        self.token_file = self.token_dir / f"token_{app_key_prefix}_{trading_mode}.json"

        logger.info(f"[TokenManager] Initialized for {trading_mode} mode")
        logger.info(f"[TokenManager] Token file: {self.token_file}")

    def save_token(self, token: KISToken) -> None:
        """
        Save token to local file.

        Args:
            token: KISToken object to save
        """
        try:
            token_data = {
                "access_token": token.access_token,
                "token_type": token.token_type,
                "expires_in": token.expires_in,
                "issued_at": token.issued_at.isoformat(),
                "expiry_datetime": token.get_expiry_datetime().isoformat()
            }

            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump(token_data, f, indent=2, ensure_ascii=False)

            logger.info(f"[TokenManager] Token saved successfully")
            logger.info(f"  - Issued at: {token.issued_at}")
            logger.info(f"  - Expires at: {token.get_expiry_datetime()}")
            logger.info(f"  - Valid for: {token.expires_in} seconds")

        except Exception as e:
            logger.error(f"[TokenManager] Failed to save token: {e}")
            raise

    def load_token(self) -> Optional[KISToken]:
        """
        Load token from local file.

        Returns:
            KISToken object if valid token exists, None otherwise
        """
        if not self.token_file.exists():
            logger.info(f"[TokenManager] No token file found")
            return None

        try:
            with open(self.token_file, 'r', encoding='utf-8') as f:
                token_data = json.load(f)

            # Parse issued_at datetime
            issued_at = datetime.fromisoformat(token_data['issued_at'])

            token = KISToken(
                access_token=token_data['access_token'],
                token_type=token_data['token_type'],
                expires_in=token_data['expires_in'],
                issued_at=issued_at
            )

            logger.info(f"[TokenManager] Token loaded from file")
            logger.info(f"  - Issued at: {token.issued_at}")
            logger.info(f"  - Expires at: {token.get_expiry_datetime()}")

            # Check if token is expired
            if token.is_expired():
                logger.warning(f"[TokenManager] Loaded token is expired")
                return None

            logger.info(f"[TokenManager] Token is valid")
            return token

        except Exception as e:
            logger.error(f"[TokenManager] Failed to load token: {e}")
            return None

    def delete_token(self) -> None:
        """Delete token file."""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
                logger.info(f"[TokenManager] Token file deleted")
        except Exception as e:
            logger.error(f"[TokenManager] Failed to delete token: {e}")

    def get_token_info(self) -> Optional[Dict[str, Any]]:
        """
        Get token information without loading the full token.

        Returns:
            Dictionary with token metadata or None if no token exists
        """
        if not self.token_file.exists():
            return None

        try:
            with open(self.token_file, 'r', encoding='utf-8') as f:
                token_data = json.load(f)

            return {
                "issued_at": token_data['issued_at'],
                "expiry_datetime": token_data['expiry_datetime'],
                "token_type": token_data['token_type'],
                "file_path": str(self.token_file)
            }
        except Exception as e:
            logger.error(f"[TokenManager] Failed to get token info: {e}")
            return None
