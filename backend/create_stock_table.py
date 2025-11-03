"""Create stocks table in the database."""

import asyncio
from app.db.session import engine
from app.db.base import Base
from app.models.stock import Stock


async def create_tables():
    """Create stocks table."""
    async with engine.begin() as conn:
        print("Creating stocks table...")
        await conn.run_sync(Base.metadata.create_all)
        print("✓ Stocks table created successfully")


if __name__ == "__main__":
    asyncio.run(create_tables())
