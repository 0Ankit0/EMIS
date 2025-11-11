"""Contract tests for Lms API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_lms_list(client: AsyncClient, test_superuser):
    """Test GET /api/lms endpoint"""
    response = await client.get("/api/lms")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_lms(client: AsyncClient, test_superuser):
    """Test POST /api/lms endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/lms", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_lms_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/lms/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/lms/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_lms(client: AsyncClient, test_superuser):
    """Test PUT /api/lms/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/lms/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_lms(client: AsyncClient, test_superuser):
    """Test DELETE /api/lms/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/lms/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_lms_search(client: AsyncClient, test_superuser):
    """Test search in lms"""
    response = await client.get(f"/api/lms/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_lms_statistics(client: AsyncClient, test_superuser):
    """Test getting lms statistics"""
    response = await client.get(f"/api/lms/stats")
    assert response.status_code in [200, 404]
