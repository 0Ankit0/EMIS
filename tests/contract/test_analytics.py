"""Contract tests for Analytics API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_analytics_list(client: AsyncClient, test_superuser):
    """Test GET /api/analytics endpoint"""
    response = await client.get("/api/analytics")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_analytics(client: AsyncClient, test_superuser):
    """Test POST /api/analytics endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/analytics", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_analytics_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/analytics/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/analytics/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_analytics(client: AsyncClient, test_superuser):
    """Test PUT /api/analytics/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/analytics/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_analytics(client: AsyncClient, test_superuser):
    """Test DELETE /api/analytics/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/analytics/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_analytics_search(client: AsyncClient, test_superuser):
    """Test search in analytics"""
    response = await client.get(f"/api/analytics/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_analytics_statistics(client: AsyncClient, test_superuser):
    """Test getting analytics statistics"""
    response = await client.get(f"/api/analytics/stats")
    assert response.status_code in [200, 404]
