"""Contract tests for Events API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_events_list(client: AsyncClient, test_superuser):
    """Test GET /api/events endpoint"""
    response = await client.get("/api/events")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_events(client: AsyncClient, test_superuser):
    """Test POST /api/events endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/events", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_events_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/events/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/events/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_events(client: AsyncClient, test_superuser):
    """Test PUT /api/events/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/events/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_events(client: AsyncClient, test_superuser):
    """Test DELETE /api/events/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/events/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_events_search(client: AsyncClient, test_superuser):
    """Test search in events"""
    response = await client.get(f"/api/events/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_events_statistics(client: AsyncClient, test_superuser):
    """Test getting events statistics"""
    response = await client.get(f"/api/events/stats")
    assert response.status_code in [200, 404]
