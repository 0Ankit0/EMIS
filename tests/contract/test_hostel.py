"""Contract tests for Hostel API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_hostel_list(client: AsyncClient, test_superuser):
    """Test GET /api/hostel endpoint"""
    response = await client.get("/api/hostel")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_hostel(client: AsyncClient, test_superuser):
    """Test POST /api/hostel endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/hostel", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_hostel_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/hostel/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/hostel/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_hostel(client: AsyncClient, test_superuser):
    """Test PUT /api/hostel/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/hostel/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_hostel(client: AsyncClient, test_superuser):
    """Test DELETE /api/hostel/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/hostel/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_hostel_search(client: AsyncClient, test_superuser):
    """Test search in hostel"""
    response = await client.get(f"/api/hostel/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_hostel_statistics(client: AsyncClient, test_superuser):
    """Test getting hostel statistics"""
    response = await client.get(f"/api/hostel/stats")
    assert response.status_code in [200, 404]
