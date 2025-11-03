"""Create test user for UI testing."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.core.security import get_password_hash
from app.config import settings
from app.db.base import Base


async def create_test_user():
    """Create a test user with email: test and password: 123456."""

    # Create engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
    )

    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.email == "test")
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            print(f"❌ User 'test' already exists with ID: {existing_user.id}")
            print("   Deleting existing user...")
            await session.delete(existing_user)
            await session.commit()

        # Create test user
        test_user = User(
            email="test",
            full_name="Test User",
            hashed_password=get_password_hash("123456"),
            is_active=True,
            is_verified=True,
        )

        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)

        print("\n" + "=" * 60)
        print("✅ Test user created successfully!")
        print("=" * 60)
        print(f"Email:     test")
        print(f"Password:  123456")
        print(f"User ID:   {test_user.id}")
        print(f"Full Name: {test_user.full_name}")
        print(f"Active:    {test_user.is_active}")
        print(f"Verified:  {test_user.is_verified}")
        print("=" * 60)
        print("\nYou can now use these credentials to test login via UI:")
        print("  - Email: test")
        print("  - Password: 123456")
        print("=" * 60 + "\n")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_test_user())
