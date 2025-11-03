"""Dashboard API endpoints."""

from datetime import datetime, date
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardStats,
    ActiveStrategy,
    RecentActivity,
)
from app.core.deps import get_current_active_user

router = APIRouter()


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get dashboard overview data.

    Returns:
        - Account statistics (balance, P&L, active strategies, today's trades)
        - Active strategies with performance
        - Recent trading activities
    """

    # TODO: Implement actual data fetching from database
    # For now, return mock data matching the frontend expectations

    stats = DashboardStats(
        total_balance=10000000.0,
        profit_loss=523000.0,
        profit_loss_percent=5.23,
        active_strategies=3,
        today_trades=12,
    )

    active_strategies = [
        ActiveStrategy(
            id=1,
            name="모멘텀 전략 A",
            status="running",
            profit_loss=234000.0,
            profit_loss_percent=2.34,
        ),
        ActiveStrategy(
            id=2,
            name="평균회귀 전략 B",
            status="running",
            profit_loss=189000.0,
            profit_loss_percent=1.89,
        ),
        ActiveStrategy(
            id=3,
            name="변동성 돌파 전략 C",
            status="running",
            profit_loss=100000.0,
            profit_loss_percent=1.0,
        ),
    ]

    recent_activities = [
        RecentActivity(
            id=1,
            type="BUY",
            symbol="삼성전자",
            quantity=10,
            price=71000.0,
            time="10:23:15",
        ),
        RecentActivity(
            id=2,
            type="SELL",
            symbol="SK하이닉스",
            quantity=5,
            price=132000.0,
            time="09:45:32",
        ),
        RecentActivity(
            id=3,
            type="BUY",
            symbol="NAVER",
            quantity=8,
            price=205000.0,
            time="09:12:08",
        ),
    ]

    return DashboardResponse(
        stats=stats,
        active_strategies=active_strategies,
        recent_activities=recent_activities,
    )
