"""Create market_data table in the database."""

import asyncio
from app.db.session import engine
from app.db.base import Base
from app.models.market_data import MarketData


async def create_tables():
    """Create all tables."""
    async with engine.begin() as conn:
        # Import all models to ensure they're registered
        from app.models import user, strategy, signal, order, holding, market_data, backtest

        print("Creating tables...")
        await conn.run_sync(Base.metadata.create_all)
        print("✓ All tables created successfully")


if __name__ == "__main__":
    asyncio.run(create_tables())
