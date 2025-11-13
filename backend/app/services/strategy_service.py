"""Strategy service for managing trading strategies."""

import logging
from typing import List, Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.strategy import Strategy
from app.core.strategy.types import StrategyStatus
from app.schemas.strategy import StrategyCreate, StrategyUpdate

logger = logging.getLogger(__name__)


class StrategyService:
    """Service for strategy CRUD operations."""

    @staticmethod
    async def create_strategy(
        db: AsyncSession,
        user_id: int,
        strategy_data: StrategyCreate
    ) -> Strategy:
        """
        Create a new strategy.

        Args:
            db: Database session
            user_id: Owner user ID
            strategy_data: Strategy creation data

        Returns:
            Created Strategy model
        """
        strategy = Strategy(
            user_id=user_id,
            name=strategy_data.name,
            description=strategy_data.description,
            strategy_type=strategy_data.strategy_type,
            parameters=strategy_data.parameters,
            status=StrategyStatus.INACTIVE
        )

        db.add(strategy)
        await db.commit()
        await db.refresh(strategy)

        logger.info(f"[StrategyService] Created strategy: {strategy.name} (ID: {strategy.id})")
        return strategy

    @staticmethod
    async def get_strategy(
        db: AsyncSession,
        strategy_id: int,
        user_id: int
    ) -> Optional[Strategy]:
        """
        Get strategy by ID for a specific user.

        Args:
            db: Database session
            strategy_id: Strategy ID
            user_id: Owner user ID

        Returns:
            Strategy model or None if not found
        """
        stmt = select(Strategy).where(
            Strategy.id == strategy_id,
            Strategy.user_id == user_id
        )
        result = await db.execute(stmt)
        strategy = result.scalar_one_or_none()

        if strategy:
            logger.debug(f"[StrategyService] Found strategy: {strategy.name} (ID: {strategy_id})")
        else:
            logger.debug(f"[StrategyService] Strategy not found: ID={strategy_id}, user={user_id}")

        return strategy

    @staticmethod
    async def list_strategies(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[StrategyStatus] = None
    ) -> tuple[List[Strategy], int]:
        """
        List strategies for a user with pagination.

        Args:
            db: Database session
            user_id: Owner user ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Optional status filter

        Returns:
            Tuple of (strategies list, total count)
        """
        # Build base query
        stmt = select(Strategy).where(Strategy.user_id == user_id)

        # Apply status filter if provided
        if status is not None:
            stmt = stmt.where(Strategy.status == status)

        # Get total count
        count_stmt = select(Strategy).where(Strategy.user_id == user_id)
        if status is not None:
            count_stmt = count_stmt.where(Strategy.status == status)
        count_result = await db.execute(count_stmt)
        total = len(count_result.scalars().all())

        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)

        # Execute query
        result = await db.execute(stmt)
        strategies = result.scalars().all()

        logger.debug(
            f"[StrategyService] Listed {len(strategies)} strategies "
            f"(user={user_id}, skip={skip}, limit={limit}, status={status})"
        )

        return list(strategies), total

    @staticmethod
    async def update_strategy(
        db: AsyncSession,
        strategy_id: int,
        user_id: int,
        strategy_data: StrategyUpdate
    ) -> Optional[Strategy]:
        """
        Update strategy.

        Args:
            db: Database session
            strategy_id: Strategy ID
            user_id: Owner user ID
            strategy_data: Strategy update data

        Returns:
            Updated Strategy model or None if not found
        """
        strategy = await StrategyService.get_strategy(db, strategy_id, user_id)

        if not strategy:
            return None

        # Update fields if provided
        update_data = strategy_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(strategy, field, value)

        await db.commit()
        await db.refresh(strategy)

        logger.info(f"[StrategyService] Updated strategy: {strategy.name} (ID: {strategy_id})")
        return strategy

    @staticmethod
    async def delete_strategy(
        db: AsyncSession,
        strategy_id: int,
        user_id: int
    ) -> bool:
        """
        Delete strategy.

        Args:
            db: Database session
            strategy_id: Strategy ID
            user_id: Owner user ID

        Returns:
            True if deleted, False if not found
        """
        strategy = await StrategyService.get_strategy(db, strategy_id, user_id)

        if not strategy:
            return False

        await db.delete(strategy)
        await db.commit()

        logger.info(f"[StrategyService] Deleted strategy: {strategy.name} (ID: {strategy_id})")
        return True

    @staticmethod
    async def update_strategy_status(
        db: AsyncSession,
        strategy_id: int,
        user_id: int,
        status: StrategyStatus
    ) -> Optional[Strategy]:
        """
        Update strategy status.

        Args:
            db: Database session
            strategy_id: Strategy ID
            user_id: Owner user ID
            status: New status

        Returns:
            Updated Strategy model or None if not found
        """
        strategy = await StrategyService.get_strategy(db, strategy_id, user_id)

        if not strategy:
            return None

        strategy.status = status
        await db.commit()
        await db.refresh(strategy)

        logger.info(
            f"[StrategyService] Updated strategy status: {strategy.name} "
            f"(ID: {strategy_id}, status={status.value})"
        )
        return strategy
