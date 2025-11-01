"""Backtest API endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/run")
async def run_backtest():
    """Run a backtest."""
    return {"message": "Run backtest endpoint - to be implemented"}


@router.get("/results/{backtest_id}")
async def get_backtest_results(backtest_id: int):
    """Get backtest results."""
    return {"message": f"Get backtest results {backtest_id} endpoint - to be implemented"}


@router.get("/history")
async def get_backtest_history():
    """Get backtest history."""
    return {"message": "Get backtest history endpoint - to be implemented"}
