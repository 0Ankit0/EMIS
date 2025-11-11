"""Authentication Security Tests"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.security
async def test_password_not_exposed(client: AsyncClient):
    """Test password is never exposed in responses"""
    response = await client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "first_name": "Test",
        "last_name": "User"
    })
    
    if response.status_code in [200, 201]:
        data = response.json()
        assert "password" not in str(data).lower()


@pytest.mark.asyncio
@pytest.mark.security
async def test_unauthorized_access_denied(client: AsyncClient):
    """Test unauthorized access is denied"""
    response = await client.get("/api/students")
    assert response.status_code in [401, 403]
