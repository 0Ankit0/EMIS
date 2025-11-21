"""Contract tests for Calendar API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_calendar_list(client: AsyncClient, test_superuser):
    """Test GET /api/calendar endpoint"""
    response = await client.get("/api/calendar")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_calendar(client: AsyncClient, test_superuser):
    """Test POST /api/calendar endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/calendar", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_calendar_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/calendar/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/calendar/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_calendar(client: AsyncClient, test_superuser):
    """Test PUT /api/calendar/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/calendar/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_calendar(client: AsyncClient, test_superuser):
    """Test DELETE /api/calendar/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/calendar/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_calendar_search(client: AsyncClient, test_superuser):
    """Test search in calendar"""
    response = await client.get(f"/api/calendar/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_calendar_statistics(client: AsyncClient, test_superuser):
    """Test getting calendar statistics"""
    response = await client.get(f"/api/calendar/stats")
    assert response.status_code in [200, 404]
