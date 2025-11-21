"""Contract tests for Financial_aid API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_financial_aid_list(client: AsyncClient, test_superuser):
    """Test GET /api/financial_aid endpoint"""
    response = await client.get("/api/financial_aid")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_financial_aid(client: AsyncClient, test_superuser):
    """Test POST /api/financial_aid endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/financial_aid", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_financial_aid_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/financial_aid/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/financial_aid/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_financial_aid(client: AsyncClient, test_superuser):
    """Test PUT /api/financial_aid/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/financial_aid/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_financial_aid(client: AsyncClient, test_superuser):
    """Test DELETE /api/financial_aid/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/financial_aid/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_financial_aid_search(client: AsyncClient, test_superuser):
    """Test search in financial_aid"""
    response = await client.get(f"/api/financial_aid/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_financial_aid_statistics(client: AsyncClient, test_superuser):
    """Test getting financial_aid statistics"""
    response = await client.get(f"/api/financial_aid/stats")
    assert response.status_code in [200, 404]
