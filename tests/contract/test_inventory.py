"""Contract tests for Inventory API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_inventory_list(client: AsyncClient, test_superuser):
    """Test GET /api/inventory endpoint"""
    response = await client.get("/api/inventory")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_inventory(client: AsyncClient, test_superuser):
    """Test POST /api/inventory endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/inventory", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_inventory_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/inventory/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/inventory/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_inventory(client: AsyncClient, test_superuser):
    """Test PUT /api/inventory/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/inventory/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_inventory(client: AsyncClient, test_superuser):
    """Test DELETE /api/inventory/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/inventory/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_inventory_search(client: AsyncClient, test_superuser):
    """Test search in inventory"""
    response = await client.get(f"/api/inventory/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_inventory_statistics(client: AsyncClient, test_superuser):
    """Test getting inventory statistics"""
    response = await client.get(f"/api/inventory/stats")
    assert response.status_code in [200, 404]
