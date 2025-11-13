"""Strategy management API endpoints."""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.core.strategy.types import StrategyStatus
from app.schemas.strategy import (
    StrategyCreate,
    StrategyUpdate,
    StrategyResponse,
    StrategyListResponse,
    StrategyExecuteRequest,
    StrategyExecuteResponse,
)
from app.services.strategy_service import StrategyService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("", response_model=StrategyListResponse)
async def list_strategies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records"),
    status: Optional[StrategyStatus] = Query(None, description="Filter by status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all strategies for the current user.

    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        status: Optional status filter (ACTIVE, INACTIVE, BACKTESTING)
        db: Database session
        current_user: Current authenticated user

    Returns:
        StrategyListResponse with paginated strategies
    """
    try:
        strategies, total = await StrategyService.list_strategies(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            status=status
        )

        return StrategyListResponse(
            strategies=[StrategyResponse.model_validate(s) for s in strategies],
            total=total,
            page=skip // limit + 1,
            page_size=limit
        )

    except Exception as e:
        logger.error(f"[Strategy API] Error listing strategies: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list strategies: {str(e)}"
        )


@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get strategy details by ID.

    Args:
        strategy_id: Strategy ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        StrategyResponse with strategy details
    """
    try:
        strategy = await StrategyService.get_strategy(
            db=db,
            strategy_id=strategy_id,
            user_id=current_user.id
        )

        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )

        return StrategyResponse.model_validate(strategy)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Strategy API] Error getting strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get strategy: {str(e)}"
        )


@router.post("", response_model=StrategyResponse, status_code=201)
async def create_strategy(
    strategy_data: StrategyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new strategy.

    Args:
        strategy_data: Strategy creation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        StrategyResponse with created strategy
    """
    try:
        strategy = await StrategyService.create_strategy(
            db=db,
            user_id=current_user.id,
            strategy_data=strategy_data
        )

        logger.info(f"[Strategy API] Created strategy: {strategy.name} (ID: {strategy.id})")

        return StrategyResponse.model_validate(strategy)

    except Exception as e:
        logger.error(f"[Strategy API] Error creating strategy: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create strategy: {str(e)}"
        )


@router.put("/{strategy_id}", response_model=StrategyResponse)
async def update_strategy(
    strategy_id: int,
    strategy_data: StrategyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing strategy.

    Args:
        strategy_id: Strategy ID
        strategy_data: Strategy update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        StrategyResponse with updated strategy
    """
    try:
        strategy = await StrategyService.update_strategy(
            db=db,
            strategy_id=strategy_id,
            user_id=current_user.id,
            strategy_data=strategy_data
        )

        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )

        logger.info(f"[Strategy API] Updated strategy: {strategy.name} (ID: {strategy_id})")

        return StrategyResponse.model_validate(strategy)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Strategy API] Error updating strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update strategy: {str(e)}"
        )


@router.delete("/{strategy_id}", status_code=204)
async def delete_strategy(
    strategy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a strategy.

    Args:
        strategy_id: Strategy ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        No content (204) on success
    """
    try:
        deleted = await StrategyService.delete_strategy(
            db=db,
            strategy_id=strategy_id,
            user_id=current_user.id
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )

        logger.info(f"[Strategy API] Deleted strategy ID: {strategy_id}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Strategy API] Error deleting strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete strategy: {str(e)}"
        )


@router.post("/{strategy_id}/activate", response_model=StrategyResponse)
async def activate_strategy(
    strategy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Activate a strategy (set status to ACTIVE).

    Args:
        strategy_id: Strategy ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        StrategyResponse with activated strategy
    """
    try:
        strategy = await StrategyService.update_strategy_status(
            db=db,
            strategy_id=strategy_id,
            user_id=current_user.id,
            status=StrategyStatus.ACTIVE
        )

        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )

        logger.info(f"[Strategy API] Activated strategy: {strategy.name} (ID: {strategy_id})")

        return StrategyResponse.model_validate(strategy)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Strategy API] Error activating strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to activate strategy: {str(e)}"
        )


@router.post("/{strategy_id}/deactivate", response_model=StrategyResponse)
async def deactivate_strategy(
    strategy_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Deactivate a strategy (set status to INACTIVE).

    Args:
        strategy_id: Strategy ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        StrategyResponse with deactivated strategy
    """
    try:
        strategy = await StrategyService.update_strategy_status(
            db=db,
            strategy_id=strategy_id,
            user_id=current_user.id,
            status=StrategyStatus.INACTIVE
        )

        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )

        logger.info(f"[Strategy API] Deactivated strategy: {strategy.name} (ID: {strategy_id})")

        return StrategyResponse.model_validate(strategy)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Strategy API] Error deactivating strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to deactivate strategy: {str(e)}"
        )


@router.post("/{strategy_id}/execute", response_model=StrategyExecuteResponse)
async def execute_strategy(
    strategy_id: int,
    request: StrategyExecuteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Execute a strategy on multiple symbols and generate trading signals.

    Args:
        strategy_id: Strategy ID
        request: Execution request with list of symbols
        db: Database session
        current_user: Current authenticated user

    Returns:
        StrategyExecuteResponse with generated signals for all symbols
    """
    from datetime import datetime, timedelta
    from app.core.strategy import MomentumStrategy, StrategyType
    from app.services.market_data_service import MarketDataService
    from app.models.market_data import TimeInterval

    try:
        # Get strategy from database
        strategy = await StrategyService.get_strategy(
            db=db,
            strategy_id=strategy_id,
            user_id=current_user.id
        )

        if not strategy:
            raise HTTPException(
                status_code=404,
                detail=f"Strategy with ID {strategy_id} not found"
            )

        # Instantiate strategy based on type
        if strategy.strategy_type == StrategyType.MOMENTUM:
            strategy_instance = MomentumStrategy(
                name=strategy.name,
                parameters=strategy.parameters
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Strategy type {strategy.strategy_type.value} is not yet supported"
            )

        # Execute strategy for each symbol
        all_signals = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=60)  # 60 days of data

        for symbol in request.symbols:
            try:
                # Get market data for the symbol
                market_data_list = await MarketDataService.get_market_data(
                    db=db,
                    symbol=symbol,
                    interval=TimeInterval.ONE_DAY,
                    start_date=start_date,
                    end_date=end_date,
                    limit=100
                )

                if not market_data_list:
                    logger.warning(
                        f"[Strategy API] No market data found for symbol {symbol}, skipping"
                    )
                    continue

                # Get current price (last close price)
                current_price = float(market_data_list[-1].close)

                # Convert market data to dict format
                market_data_dicts = [
                    {
                        "timestamp": data.timestamp,
                        "open": float(data.open),
                        "high": float(data.high),
                        "low": float(data.low),
                        "close": float(data.close),
                        "volume": float(data.volume)
                    }
                    for data in market_data_list
                ]

                # Generate signals for this symbol
                signals = await strategy_instance.generate_signals(
                    symbol=symbol,
                    market_data=market_data_dicts,
                    current_price=current_price
                )

                # Add signals to results
                all_signals.extend([
                    {
                        "timestamp": signal.timestamp.isoformat(),
                        "symbol": signal.symbol,
                        "signal_type": signal.signal_type.value,
                        "price": signal.price,
                        "quantity": signal.quantity,
                        "reason": signal.reason,
                        "confidence": signal.confidence
                    }
                    for signal in signals
                ])

                logger.info(
                    f"[Strategy API] Executed strategy for {symbol}, "
                    f"generated {len(signals)} signal(s)"
                )

            except Exception as e:
                logger.error(
                    f"[Strategy API] Error executing strategy for symbol {symbol}: {e}"
                )
                # Continue with next symbol instead of failing entire request
                continue

        logger.info(
            f"[Strategy API] Executed strategy: {strategy.name} (ID: {strategy_id}) "
            f"for {len(request.symbols)} symbols, generated {len(all_signals)} total signal(s)"
        )

        return StrategyExecuteResponse(
            strategy_id=strategy_id,
            strategy_name=strategy.name,
            symbols=request.symbols,
            executed_at=datetime.now().isoformat(),
            signals=all_signals,
            total_signals=len(all_signals),
            total_symbols=len(request.symbols)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[Strategy API] Error executing strategy {strategy_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to execute strategy: {str(e)}"
        )
