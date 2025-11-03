"""Pytest configuration and fixtures."""

import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.config import settings

# Import all models to ensure they are registered with Base.metadata
from app.models.user import User
from app.models.strategy import Strategy
from app.models.signal import Signal
from app.models.order import Order, Trade
from app.models.holding import Holding
from app.models.market_data import MarketData
from app.models.backtest import BacktestResult, BacktestTrade

# Test database URL (use in-memory SQLite for tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine with StaticPool to share the same connection
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Important: use StaticPool for in-memory SQLite
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    # Create all tables before each test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestSessionLocal() as session:
        yield session

    # Clean up tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client."""

    # Import here to avoid circular import
    from app.main import app

    # Override get_db dependency to use test session
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Create test client with custom transport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client

    # Clear overrides
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_data() -> dict:
    """Test user data."""
    return {
        "email": "test@example.com",
        "password": "Test1234!",
        "full_name": "Test User",
    }


@pytest.fixture
def test_user_data_2() -> dict:
    """Another test user data."""
    return {
        "email": "test2@example.com",
        "password": "Test5678!",
        "full_name": "Test User 2",
    }
