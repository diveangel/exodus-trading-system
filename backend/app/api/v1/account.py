"""Account management API endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User, TradingMode
from app.schemas.user import RealKISCredentialsUpdate, MockKISCredentialsUpdate, UserDetailResponse
from app.core.deps import get_current_active_user
from app.services.kis_client import KISClient
from app.services.kis_account import KISAccount

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
    logger.info(f"[GET /balance] Current trading mode: {current_user.kis_trading_mode}")

    # Get credentials based on current trading mode
    if current_user.kis_trading_mode == TradingMode.REAL:
        if not current_user.has_real_credentials:
            logger.warning(f"[GET /balance] User {current_user.id} has no REAL trading credentials")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Real trading API credentials not configured. Please set up your credentials in Settings."
            )
        app_key = current_user.real_app_key
        app_secret = current_user.real_app_secret
        account_number = current_user.real_account_number
        account_code = current_user.real_account_code
    else:  # MOCK mode
        if not current_user.has_mock_credentials:
            logger.warning(f"[GET /balance] User {current_user.id} has no MOCK trading credentials")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mock trading API credentials not configured. Please set up your credentials in Settings."
            )
        app_key = current_user.mock_app_key
        app_secret = current_user.mock_app_secret
        account_number = current_user.mock_account_number
        account_code = current_user.mock_account_code

    try:
        logger.info(f"[GET /balance] User credentials:")
        logger.info(f"  - Account Number: {account_number}")
        logger.info(f"  - Account Code: {account_code}")
        logger.info(f"  - Trading Mode: {current_user.kis_trading_mode}")
        logger.info(f"  - App Key (first 10 chars): {app_key[:10]}...")
        logger.info(f"  - App Secret (first 10 chars): {app_secret[:10]}...")

        # Initialize KIS client with user's credentials and trading mode
        kis_client = KISClient(
            app_key=app_key,
            app_secret=app_secret,
            account_number=account_number,
            account_code=account_code,
            trading_mode=current_user.kis_trading_mode,
        )

        logger.info(f"[GET /balance] Calling KIS API get_account_balance()...")

        # Initialize KIS Account service
        kis_account = KISAccount(kis_client)

        # Get account balance from KIS API
        balance_data = await kis_account.get_account_balance()

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

    Returns account numbers and codes for both real and mock trading,
    but does not expose the actual API keys.
    """
    return current_user


@router.put("/kis-credentials/real", response_model=UserDetailResponse)
async def update_real_kis_credentials(
    kis_data: RealKISCredentialsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update Real Trading KIS API credentials.

    Stores the real trading API keys securely.
    """
    logger.info(f"[PUT /kis-credentials/real] Updating real trading credentials for user {current_user.id}")

    # Update Real KIS credentials
    current_user.real_app_key = kis_data.real_app_key
    current_user.real_app_secret = kis_data.real_app_secret
    current_user.real_account_number = kis_data.real_account_number
    current_user.real_account_code = kis_data.real_account_code
    current_user.has_real_credentials = True

    # Commit changes
    await db.commit()
    await db.refresh(current_user)

    logger.info(f"[PUT /kis-credentials/real] Successfully updated real trading credentials")
    return current_user


@router.put("/kis-credentials/mock", response_model=UserDetailResponse)
async def update_mock_kis_credentials(
    kis_data: MockKISCredentialsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update Mock Trading KIS API credentials.

    Stores the mock trading API keys securely.
    """
    logger.info(f"[PUT /kis-credentials/mock] Updating mock trading credentials for user {current_user.id}")

    # Update Mock KIS credentials
    current_user.mock_app_key = kis_data.mock_app_key
    current_user.mock_app_secret = kis_data.mock_app_secret
    current_user.mock_account_number = kis_data.mock_account_number
    current_user.mock_account_code = kis_data.mock_account_code
    current_user.has_mock_credentials = True

    # Commit changes
    await db.commit()
    await db.refresh(current_user)

    logger.info(f"[PUT /kis-credentials/mock] Successfully updated mock trading credentials")
    return current_user


@router.delete("/kis-credentials/real", status_code=status.HTTP_204_NO_CONTENT)
async def delete_real_kis_credentials(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete Real Trading KIS API credentials.

    Removes all real trading KIS API credentials from the user account.
    """
    logger.info(f"[DELETE /kis-credentials/real] Deleting real trading credentials for user {current_user.id}")

    # Clear Real KIS credentials
    current_user.real_app_key = None
    current_user.real_app_secret = None
    current_user.real_account_number = None
    current_user.real_account_code = None
    current_user.has_real_credentials = False

    # Commit changes
    await db.commit()

    logger.info(f"[DELETE /kis-credentials/real] Successfully deleted real trading credentials")
    return None


@router.delete("/kis-credentials/mock", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mock_kis_credentials(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete Mock Trading KIS API credentials.

    Removes all mock trading KIS API credentials from the user account.
    """
    logger.info(f"[DELETE /kis-credentials/mock] Deleting mock trading credentials for user {current_user.id}")

    # Clear Mock KIS credentials
    current_user.mock_app_key = None
    current_user.mock_app_secret = None
    current_user.mock_account_number = None
    current_user.mock_account_code = None
    current_user.has_mock_credentials = False

    # Commit changes
    await db.commit()

    logger.info(f"[DELETE /kis-credentials/mock] Successfully deleted mock trading credentials")
    return None
