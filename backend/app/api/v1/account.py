"""Account management API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/balance")
async def get_balance():
    """Get account balance."""
    return {"message": "Get account balance endpoint - to be implemented"}


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
