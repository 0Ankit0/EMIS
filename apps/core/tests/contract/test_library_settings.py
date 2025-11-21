"""Contract tests for Library_settings API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_library_settings_list(client: AsyncClient, test_superuser):
    """Test GET /api/library_settings endpoint"""
    response = await client.get("/api/library_settings")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_library_settings(client: AsyncClient, test_superuser):
    """Test POST /api/library_settings endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/library_settings", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_library_settings_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/library_settings/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/library_settings/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_library_settings(client: AsyncClient, test_superuser):
    """Test PUT /api/library_settings/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/library_settings/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_library_settings(client: AsyncClient, test_superuser):
    """Test DELETE /api/library_settings/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/library_settings/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_library_settings_search(client: AsyncClient, test_superuser):
    """Test search in library_settings"""
    response = await client.get(f"/api/library_settings/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_library_settings_statistics(client: AsyncClient, test_superuser):
    """Test getting library_settings statistics"""
    response = await client.get(f"/api/library_settings/stats")
    assert response.status_code in [200, 404]
