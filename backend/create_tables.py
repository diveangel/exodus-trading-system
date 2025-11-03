"""Create database tables manually."""

import asyncio
from app.db.base import Base
from app.db.session import engine

# Import all models to ensure they are registered
from app.models import (
    User,
    Strategy,
    Signal,
    Order,
    Trade,
    Holding,
    MarketData,
    BacktestResult,
    BacktestTrade,
)


async def create_tables():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
