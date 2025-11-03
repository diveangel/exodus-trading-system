"""Stock information API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.stock import Stock
from app.models.user import User
from app.schemas.stock import (
    Stock as StockSchema,
    StockListResponse,
    StockSearchParams,
)

router = APIRouter()


@router.get("/search", response_model=StockListResponse)
async def search_stocks(
    query: str = Query(..., min_length=1, description="Search query (name or symbol)"),
    market_type: str = Query("ALL", description="Market type filter: KOSPI, KOSDAQ, or ALL"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Search stocks by name or symbol.

    - **query**: Search text (Korean name or stock symbol)
    - **market_type**: Filter by market (KOSPI, KOSDAQ, or ALL)
    - **limit**: Maximum number of results (1-100)

    Returns a list of matching stocks.
    """
    # Build query
    stmt = select(Stock)

    # Add text search filter
    search_filter = or_(
        Stock.name.ilike(f"%{query}%"),
        Stock.symbol.ilike(f"%{query}%"),
    )
    stmt = stmt.filter(search_filter)

    # Add market type filter
    if market_type and market_type != "ALL":
        if market_type not in ["KOSPI", "KOSDAQ"]:
            raise HTTPException(status_code=400, detail="Invalid market_type. Use KOSPI, KOSDAQ, or ALL")
        stmt = stmt.filter(Stock.market_type == market_type)

    # Order by relevance (exact matches first, then by name)
    stmt = stmt.order_by(
        # Exact symbol match first
        (Stock.symbol == query).desc(),
        # Then by name similarity
        Stock.name
    )

    # Apply limit
    stmt = stmt.limit(limit)

    # Execute query
    result = await db.execute(stmt)
    stocks = result.scalars().all()

    # Get total count for this search
    count_stmt = select(func.count(Stock.id)).filter(search_filter)
    if market_type and market_type != "ALL":
        count_stmt = count_stmt.filter(Stock.market_type == market_type)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    return StockListResponse(
        total=total,
        stocks=[StockSchema.model_validate(stock) for stock in stocks]
    )


@router.get("/{symbol}", response_model=StockSchema)
async def get_stock(
    symbol: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get stock information by symbol.

    - **symbol**: Stock symbol code (e.g., "005930" for Samsung Electronics)

    Returns detailed stock information.
    """
    stmt = select(Stock).filter(Stock.symbol == symbol)
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()

    if not stock:
        raise HTTPException(status_code=404, detail=f"Stock with symbol '{symbol}' not found")

    return StockSchema.model_validate(stock)


@router.get("/", response_model=StockListResponse)
async def list_stocks(
    market_type: str = Query("ALL", description="Market type filter: KOSPI, KOSDAQ, or ALL"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all stocks with pagination.

    - **market_type**: Filter by market (KOSPI, KOSDAQ, or ALL)
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of results (1-100)

    Returns a paginated list of stocks.
    """
    # Build query
    stmt = select(Stock)

    # Add market type filter
    if market_type and market_type != "ALL":
        if market_type not in ["KOSPI", "KOSDAQ"]:
            raise HTTPException(status_code=400, detail="Invalid market_type. Use KOSPI, KOSDAQ, or ALL")
        stmt = stmt.filter(Stock.market_type == market_type)

    # Order by symbol
    stmt = stmt.order_by(Stock.symbol)

    # Apply pagination
    stmt = stmt.offset(skip).limit(limit)

    # Execute query
    result = await db.execute(stmt)
    stocks = result.scalars().all()

    # Get total count
    count_stmt = select(func.count(Stock.id))
    if market_type and market_type != "ALL":
        count_stmt = count_stmt.filter(Stock.market_type == market_type)
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    return StockListResponse(
        total=total,
        stocks=[StockSchema.model_validate(stock) for stock in stocks]
    )
