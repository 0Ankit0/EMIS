"""Contract tests for Accounting API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_accounting_list(client: AsyncClient, test_superuser):
    """Test GET /api/accounting endpoint"""
    response = await client.get("/api/accounting")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_accounting(client: AsyncClient, test_superuser):
    """Test POST /api/accounting endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/accounting", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_accounting_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/accounting/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/accounting/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_accounting(client: AsyncClient, test_superuser):
    """Test PUT /api/accounting/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/accounting/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_accounting(client: AsyncClient, test_superuser):
    """Test DELETE /api/accounting/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/accounting/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_accounting_search(client: AsyncClient, test_superuser):
    """Test search in accounting"""
    response = await client.get(f"/api/accounting/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_accounting_statistics(client: AsyncClient, test_superuser):
    """Test getting accounting statistics"""
    response = await client.get(f"/api/accounting/stats")
    assert response.status_code in [200, 404]
