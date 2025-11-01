"""Market data API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/price/{symbol}")
async def get_price(symbol: str):
    """Get current price for a symbol."""
    return {"message": f"Get price for {symbol} endpoint - to be implemented"}


@router.get("/chart/{symbol}")
async def get_chart_data(symbol: str):
    """Get chart data for a symbol."""
    return {"message": f"Get chart data for {symbol} endpoint - to be implemented"}


@router.get("/search")
async def search_symbols(query: str):
    """Search for stock symbols."""
    return {"message": f"Search symbols with query '{query}' endpoint - to be implemented"}
