"""Test cases for authentication API."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


class TestRegister:
    """Test user registration."""

    @pytest.mark.asyncio
    async def test_register_success(
        self, client: AsyncClient, test_user_data: dict
    ):
        """Test successful user registration."""
        response = await client.post("/api/v1/auth/register", json=test_user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "id" in data
        assert "password" not in data
        assert "hashed_password" not in data

    @pytest.mark.asyncio
    async def test_register_duplicate_email(
        self, client: AsyncClient, test_user_data: dict
    ):
        """Test registration with duplicate email."""
        # First registration
        await client.post("/api/v1/auth/register", json=test_user_data)

        # Second registration with same email
        response = await client.post("/api/v1/auth/register", json=test_user_data)

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "Test1234!",
                "full_name": "Test User",
            },
        )

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_register_short_password(
        self, client: AsyncClient, test_user_data: dict
    ):
        """Test registration with short password."""
        data = test_user_data.copy()
        data["password"] = "short"

        response = await client.post("/api/v1/auth/register", json=data)

        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    async def test_register_missing_fields(self, client: AsyncClient):
        """Test registration with missing required fields."""
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com"},
        )

        assert response.status_code == 422  # Validation error


class TestLogin:
    """Test user login."""

    @pytest.mark.asyncio
    async def test_login_success(
        self, client: AsyncClient, test_user_data: dict
    ):
        """Test successful login."""
        # Register user first
        await client.post("/api/v1/auth/register", json=test_user_data)

        # Login
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user_data["email"],
                "password": test_user_data["password"],
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user_data["email"]

    @pytest.mark.asyncio
    async def test_login_wrong_password(
        self, client: AsyncClient, test_user_data: dict
    ):
        """Test login with wrong password."""
        # Register user first
        await client.post("/api/v1/auth/register", json=test_user_data)

        # Login with wrong password
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user_data["email"],
                "password": "WrongPassword123!",
            },
        )

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "Test1234!",
            },
        )

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_inactive_user(
        self, client: AsyncClient, test_user_data: dict, db_session: AsyncSession
    ):
        """Test login with inactive user."""
        # Register user
        await client.post("/api/v1/auth/register", json=test_user_data)

        # TODO: Deactivate user in database
        # For now, skip this test
        pytest.skip("User deactivation not implemented yet")


class TestRefreshToken:
    """Test token refresh."""

    @pytest.mark.asyncio
    async def test_refresh_token_success(
        self, client: AsyncClient, test_user_data: dict
    ):
        """Test successful token refresh."""
        # Register and login
        await client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user_data["email"],
                "password": test_user_data["password"],
            },
        )
        refresh_token = login_response.json()["refresh_token"]

        # Refresh token
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_refresh_token_invalid(self, client: AsyncClient):
        """Test refresh with invalid token."""
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"},
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_refresh_token_expired(self, client: AsyncClient):
        """Test refresh with expired token."""
        # TODO: Create expired token and test
        pytest.skip("Expired token test not implemented yet")


class TestCurrentUser:
    """Test getting current user."""

    @pytest.mark.asyncio
    async def test_get_current_user_success(
        self, client: AsyncClient, test_user_data: dict
    ):
        """Test getting current user with valid token."""
        # Register and login
        await client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user_data["email"],
                "password": test_user_data["password"],
            },
        )
        access_token = login_response.json()["access_token"]

        # Get current user
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert data["full_name"] == test_user_data["full_name"]
        assert "id" in data
        assert "password" not in data

    @pytest.mark.asyncio
    async def test_get_current_user_no_token(self, client: AsyncClient):
        """Test getting current user without token."""
        response = await client.get("/api/v1/auth/me")

        assert response.status_code == 403  # Forbidden

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"},
        )

        assert response.status_code == 401  # Unauthorized


class TestLogout:
    """Test user logout."""

    @pytest.mark.asyncio
    async def test_logout_success(
        self, client: AsyncClient, test_user_data: dict
    ):
        """Test successful logout."""
        # Register and login
        await client.post("/api/v1/auth/register", json=test_user_data)
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user_data["email"],
                "password": test_user_data["password"],
            },
        )
        access_token = login_response.json()["access_token"]

        # Logout
        response = await client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        assert "message" in response.json()
