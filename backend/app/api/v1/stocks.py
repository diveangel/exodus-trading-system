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
from pydantic import BaseModel

router = APIRouter()


class StockFiltersResponse(BaseModel):
    """Available filter options for stocks"""
    sectors: list[str]
    industries: list[str]
    depts: list[str]
    market_types: list[str] = ["KOSPI", "KOSDAQ"]


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


@router.get("/filters", response_model=StockFiltersResponse)
async def get_stock_filters(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get available filter options for stocks.

    Returns:
        - **sectors**: List of unique sectors
        - **industries**: List of unique industries
        - **depts**: List of unique KRX departments
        - **market_types**: List of market types (KOSPI, KOSDAQ)
    """
    # Get unique sectors
    sector_stmt = select(Stock.sector).where(Stock.sector.isnot(None)).distinct().order_by(Stock.sector)
    sector_result = await db.execute(sector_stmt)
    sectors = [row[0] for row in sector_result.all()]

    # Get unique industries
    industry_stmt = select(Stock.industry).where(Stock.industry.isnot(None)).distinct().order_by(Stock.industry)
    industry_result = await db.execute(industry_stmt)
    industries = [row[0] for row in industry_result.all()]

    # Get unique depts
    dept_stmt = select(Stock.dept).where(Stock.dept.isnot(None)).distinct().order_by(Stock.dept)
    dept_result = await db.execute(dept_stmt)
    depts = [row[0] for row in dept_result.all()]

    return StockFiltersResponse(
        sectors=sectors,
        industries=industries,
        depts=depts
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
    sector: str | None = Query(None, description="Filter by sector"),
    industry: str | None = Query(None, description="Filter by industry"),
    dept: str | None = Query(None, description="Filter by KRX department (부문)"),
    sort_by: str = Query("market_cap", description="Sort field: market_cap, name, symbol"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of results"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List all stocks with filtering, sorting, and pagination.

    - **market_type**: Filter by market (KOSPI, KOSDAQ, or ALL)
    - **sector**: Filter by sector (Technology, Finance, Healthcare, etc.)
    - **industry**: Filter by industry
    - **dept**: Filter by KRX department (우량기업부, 중견기업부, etc.)
    - **sort_by**: Sort by field (market_cap, name, symbol)
    - **sort_order**: Sort order (asc, desc)
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of results (1-100)

    Returns a paginated list of stocks.
    """
    # Build query
    stmt = select(Stock)
    count_stmt = select(func.count(Stock.id))

    # Add market type filter
    if market_type and market_type != "ALL":
        if market_type not in ["KOSPI", "KOSDAQ"]:
            raise HTTPException(status_code=400, detail="Invalid market_type. Use KOSPI, KOSDAQ, or ALL")
        stmt = stmt.filter(Stock.market_type == market_type)
        count_stmt = count_stmt.filter(Stock.market_type == market_type)

    # Add sector filter
    if sector:
        stmt = stmt.filter(Stock.sector == sector)
        count_stmt = count_stmt.filter(Stock.sector == sector)

    # Add industry filter
    if industry:
        stmt = stmt.filter(Stock.industry == industry)
        count_stmt = count_stmt.filter(Stock.industry == industry)

    # Add dept filter
    if dept:
        stmt = stmt.filter(Stock.dept == dept)
        count_stmt = count_stmt.filter(Stock.dept == dept)

    # Apply sorting
    if sort_by not in ["market_cap", "name", "symbol"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by. Use market_cap, name, or symbol")

    if sort_order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort_order. Use asc or desc")

    sort_column = getattr(Stock, sort_by)

    # For market_cap, handle NULL values (put them at the end)
    if sort_by == "market_cap":
        if sort_order == "desc":
            stmt = stmt.order_by(sort_column.desc().nullslast())
        else:
            stmt = stmt.order_by(sort_column.asc().nullslast())
    else:
        if sort_order == "desc":
            stmt = stmt.order_by(sort_column.desc())
        else:
            stmt = stmt.order_by(sort_column.asc())

    # Apply pagination
    stmt = stmt.offset(skip).limit(limit)

    # Execute query
    result = await db.execute(stmt)
    stocks = result.scalars().all()

    # Get total count
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    return StockListResponse(
        total=total,
        stocks=[StockSchema.model_validate(stock) for stock in stocks]
    )
