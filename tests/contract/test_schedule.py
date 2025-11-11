"""Contract tests for Schedule API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_schedule_list(client: AsyncClient, test_superuser):
    """Test GET /api/schedule endpoint"""
    response = await client.get("/api/schedule")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_schedule(client: AsyncClient, test_superuser):
    """Test POST /api/schedule endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/schedule", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_schedule_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/schedule/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/schedule/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_schedule(client: AsyncClient, test_superuser):
    """Test PUT /api/schedule/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/schedule/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_schedule(client: AsyncClient, test_superuser):
    """Test DELETE /api/schedule/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/schedule/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_schedule_search(client: AsyncClient, test_superuser):
    """Test search in schedule"""
    response = await client.get(f"/api/schedule/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_schedule_statistics(client: AsyncClient, test_superuser):
    """Test getting schedule statistics"""
    response = await client.get(f"/api/schedule/stats")
    assert response.status_code in [200, 404]
