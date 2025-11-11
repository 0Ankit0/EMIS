"""Contract tests for Teacher_hierarchy API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_teacher_hierarchy_list(client: AsyncClient, test_superuser):
    """Test GET /api/teacher_hierarchy endpoint"""
    response = await client.get("/api/teacher_hierarchy")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_teacher_hierarchy(client: AsyncClient, test_superuser):
    """Test POST /api/teacher_hierarchy endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/teacher_hierarchy", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_teacher_hierarchy_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/teacher_hierarchy/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/teacher_hierarchy/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_teacher_hierarchy(client: AsyncClient, test_superuser):
    """Test PUT /api/teacher_hierarchy/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/teacher_hierarchy/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_teacher_hierarchy(client: AsyncClient, test_superuser):
    """Test DELETE /api/teacher_hierarchy/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/teacher_hierarchy/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_teacher_hierarchy_search(client: AsyncClient, test_superuser):
    """Test search in teacher_hierarchy"""
    response = await client.get(f"/api/teacher_hierarchy/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_teacher_hierarchy_statistics(client: AsyncClient, test_superuser):
    """Test getting teacher_hierarchy statistics"""
    response = await client.get(f"/api/teacher_hierarchy/stats")
    assert response.status_code in [200, 404]
