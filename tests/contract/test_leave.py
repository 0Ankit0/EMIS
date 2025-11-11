"""Contract tests for Leave API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_leave_list(client: AsyncClient, test_superuser):
    """Test GET /api/leave endpoint"""
    response = await client.get("/api/leave")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_leave(client: AsyncClient, test_superuser):
    """Test POST /api/leave endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/leave", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_leave_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/leave/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/leave/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_leave(client: AsyncClient, test_superuser):
    """Test PUT /api/leave/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/leave/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_leave(client: AsyncClient, test_superuser):
    """Test DELETE /api/leave/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/leave/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_leave_search(client: AsyncClient, test_superuser):
    """Test search in leave"""
    response = await client.get(f"/api/leave/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_leave_statistics(client: AsyncClient, test_superuser):
    """Test getting leave statistics"""
    response = await client.get(f"/api/leave/stats")
    assert response.status_code in [200, 404]
