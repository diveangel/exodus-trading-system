"""Watchlist management API endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.watchlist import Watchlist
from app.models.stock import Stock
from app.schemas.watchlist import (
    WatchlistCreate,
    WatchlistUpdate,
    WatchlistResponse,
    WatchlistListResponse,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("", response_model=WatchlistResponse, status_code=201)
async def add_to_watchlist(
    watchlist_data: WatchlistCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a stock to user's watchlist.

    Args:
        watchlist_data: Watchlist creation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        WatchlistResponse with created watchlist entry
    """
    try:
        # Check if stock exists
        stock_stmt = select(Stock).where(Stock.symbol == watchlist_data.symbol)
        stock_result = await db.execute(stock_stmt)
        stock = stock_result.scalar_one_or_none()

        if not stock:
            raise HTTPException(
                status_code=404,
                detail=f"Stock with symbol '{watchlist_data.symbol}' not found"
            )

        # Check if already in watchlist
        existing_stmt = select(Watchlist).where(
            and_(
                Watchlist.user_id == current_user.id,
                Watchlist.symbol == watchlist_data.symbol,
                Watchlist.name == watchlist_data.name
            )
        )
        existing_result = await db.execute(existing_stmt)
        existing = existing_result.scalar_one_or_none()

        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Stock '{watchlist_data.symbol}' already in watchlist"
            )

        # Create watchlist entry
        watchlist = Watchlist(
            user_id=current_user.id,
            symbol=watchlist_data.symbol,
            name=watchlist_data.name,
            notes=watchlist_data.notes
        )

        db.add(watchlist)
        await db.commit()
        await db.refresh(watchlist)

        logger.info(f"[Watchlist API] Added {watchlist_data.symbol} to watchlist for user {current_user.id}")

        return WatchlistResponse.model_validate(watchlist)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Watchlist API] Error adding to watchlist: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add to watchlist: {str(e)}"
        )


@router.get("", response_model=WatchlistListResponse)
async def get_watchlist(
    name: str = Query(None, description="Filter by watchlist group name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user's watchlist.

    Args:
        name: Optional watchlist group name filter
        skip: Number of records to skip
        limit: Maximum number of records
        db: Database session
        current_user: Current authenticated user

    Returns:
        WatchlistListResponse with watchlist entries
    """
    try:
        # Build query
        conditions = [Watchlist.user_id == current_user.id]

        if name:
            conditions.append(Watchlist.name == name)

        stmt = (
            select(Watchlist)
            .where(and_(*conditions))
            .order_by(Watchlist.created_at.desc())
            .offset(skip)
            .limit(limit)
        )

        result = await db.execute(stmt)
        watchlists = result.scalars().all()

        # Get total count
        count_stmt = select(func.count(Watchlist.id)).where(and_(*conditions))
        count_result = await db.execute(count_stmt)
        total = count_result.scalar_one()

        return WatchlistListResponse(
            total=total,
            watchlists=[WatchlistResponse.model_validate(w) for w in watchlists]
        )

    except Exception as e:
        logger.error(f"[Watchlist API] Error getting watchlist: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get watchlist: {str(e)}"
        )


@router.get("/symbols", response_model=list[str])
async def get_watchlist_symbols(
    name: str = Query(None, description="Filter by watchlist group name"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of symbols in user's watchlist.

    Args:
        name: Optional watchlist group name filter
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of stock symbols
    """
    try:
        conditions = [Watchlist.user_id == current_user.id]

        if name:
            conditions.append(Watchlist.name == name)

        stmt = (
            select(Watchlist.symbol)
            .where(and_(*conditions))
            .order_by(Watchlist.created_at.desc())
        )

        result = await db.execute(stmt)
        symbols = result.scalars().all()

        return list(symbols)

    except Exception as e:
        logger.error(f"[Watchlist API] Error getting watchlist symbols: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get watchlist symbols: {str(e)}"
        )


@router.put("/{watchlist_id}", response_model=WatchlistResponse)
async def update_watchlist(
    watchlist_id: int,
    watchlist_data: WatchlistUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a watchlist entry.

    Args:
        watchlist_id: Watchlist entry ID
        watchlist_data: Update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        WatchlistResponse with updated watchlist entry
    """
    try:
        # Get watchlist entry
        stmt = select(Watchlist).where(
            and_(
                Watchlist.id == watchlist_id,
                Watchlist.user_id == current_user.id
            )
        )
        result = await db.execute(stmt)
        watchlist = result.scalar_one_or_none()

        if not watchlist:
            raise HTTPException(
                status_code=404,
                detail=f"Watchlist entry with ID {watchlist_id} not found"
            )

        # Update fields
        if watchlist_data.name is not None:
            watchlist.name = watchlist_data.name
        if watchlist_data.notes is not None:
            watchlist.notes = watchlist_data.notes

        await db.commit()
        await db.refresh(watchlist)

        logger.info(f"[Watchlist API] Updated watchlist entry {watchlist_id}")

        return WatchlistResponse.model_validate(watchlist)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Watchlist API] Error updating watchlist: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update watchlist: {str(e)}"
        )


@router.delete("/{watchlist_id}", status_code=204)
async def delete_from_watchlist(
    watchlist_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove a stock from user's watchlist.

    Args:
        watchlist_id: Watchlist entry ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        None (204 No Content)
    """
    try:
        # Get watchlist entry
        stmt = select(Watchlist).where(
            and_(
                Watchlist.id == watchlist_id,
                Watchlist.user_id == current_user.id
            )
        )
        result = await db.execute(stmt)
        watchlist = result.scalar_one_or_none()

        if not watchlist:
            raise HTTPException(
                status_code=404,
                detail=f"Watchlist entry with ID {watchlist_id} not found"
            )

        await db.delete(watchlist)
        await db.commit()

        logger.info(f"[Watchlist API] Removed watchlist entry {watchlist_id}")

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Watchlist API] Error deleting from watchlist: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete from watchlist: {str(e)}"
        )
