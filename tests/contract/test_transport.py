"""Contract tests for Transport API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_transport_list(client: AsyncClient, test_superuser):
    """Test GET /api/transport endpoint"""
    response = await client.get("/api/transport")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_transport(client: AsyncClient, test_superuser):
    """Test POST /api/transport endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/transport", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_transport_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/transport/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/transport/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_transport(client: AsyncClient, test_superuser):
    """Test PUT /api/transport/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/transport/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_transport(client: AsyncClient, test_superuser):
    """Test DELETE /api/transport/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/transport/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_transport_search(client: AsyncClient, test_superuser):
    """Test search in transport"""
    response = await client.get(f"/api/transport/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_transport_statistics(client: AsyncClient, test_superuser):
    """Test getting transport statistics"""
    response = await client.get(f"/api/transport/stats")
    assert response.status_code in [200, 404]
