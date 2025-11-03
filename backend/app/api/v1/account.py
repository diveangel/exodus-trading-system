"""Account management API endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserKISUpdate, UserDetailResponse
from app.core.deps import get_current_active_user
from app.services.kis_client import KISClient

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/balance")
async def get_balance(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get account balance from Korea Investment & Securities.

    Requires the user to have KIS API credentials configured.
    """
    logger.info(f"[GET /balance] Request from user_id={current_user.id}, email={current_user.email}")

    # Check if user has KIS credentials
    if not current_user.has_kis_credentials:
        logger.warning(f"[GET /balance] User {current_user.id} has no KIS credentials")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="KIS API credentials not configured. Please set up your credentials in Settings."
        )

    try:
        logger.info(f"[GET /balance] User credentials:")
        logger.info(f"  - Account Number: {current_user.kis_account_number}")
        logger.info(f"  - Account Code: {current_user.kis_account_code}")
        logger.info(f"  - Trading Mode: {current_user.kis_trading_mode}")
        logger.info(f"  - App Key (first 10 chars): {current_user.kis_app_key[:10]}...")
        logger.info(f"  - App Secret (first 10 chars): {current_user.kis_app_secret[:10]}...")

        # Initialize KIS client with user's credentials and trading mode
        kis_client = KISClient(
            app_key=current_user.kis_app_key,
            app_secret=current_user.kis_app_secret,
            account_number=current_user.kis_account_number,
            account_code=current_user.kis_account_code,
            trading_mode=current_user.kis_trading_mode,
        )

        logger.info(f"[GET /balance] Calling KIS API get_account_balance()...")

        # Get account balance from KIS API
        balance_data = await kis_client.get_account_balance()

        logger.info(f"[GET /balance] Success! Received balance data")
        return balance_data

    except Exception as e:
        logger.error(f"[GET /balance] Error: {type(e).__name__}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch account balance from KIS API: {str(e)}"
        )


@router.get("/holdings")
async def get_holdings():
    """Get current holdings."""
    return {"message": "Get holdings endpoint - to be implemented"}


@router.get("/trades")
async def get_trades():
    """Get trade history."""
    return {"message": "Get trades endpoint - to be implemented"}


@router.get("/orders")
async def get_orders():
    """Get order history."""
    return {"message": "Get orders endpoint - to be implemented"}


@router.get("/profit-loss")
async def get_profit_loss():
    """Get profit and loss summary."""
    return {"message": "Get P&L endpoint - to be implemented"}


@router.get("/kis-credentials", response_model=UserDetailResponse)
async def get_kis_credentials(
    current_user: User = Depends(get_current_active_user),
):
    """
    Get current user's KIS API credentials (masked).

    Returns account number and account code but masks the API keys.
    """
    return current_user


@router.put("/kis-credentials", response_model=UserDetailResponse)
async def update_kis_credentials(
    kis_data: UserKISUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update Korea Investment API credentials.

    Stores the API keys securely and marks the user as having KIS credentials.
    """
    # Update KIS credentials
    current_user.kis_app_key = kis_data.kis_app_key
    current_user.kis_app_secret = kis_data.kis_app_secret
    current_user.kis_account_number = kis_data.kis_account_number
    current_user.kis_account_code = kis_data.kis_account_code
    current_user.kis_trading_mode = kis_data.kis_trading_mode
    current_user.has_kis_credentials = True

    # Commit changes
    await db.commit()
    await db.refresh(current_user)

    return current_user


@router.delete("/kis-credentials", status_code=status.HTTP_204_NO_CONTENT)
async def delete_kis_credentials(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete Korea Investment API credentials.

    Removes all KIS API credentials from the user account.
    """
    # Clear KIS credentials
    current_user.kis_app_key = None
    current_user.kis_app_secret = None
    current_user.kis_account_number = None
    current_user.kis_account_code = None
    current_user.has_kis_credentials = False

    # Commit changes
    await db.commit()

    return None
