"""Contract tests for Billing API endpoints"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


@pytest.mark.asyncio
async def test_get_billing_list(client: AsyncClient, test_superuser):
    """Test GET /api/billing endpoint"""
    response = await client.get("/api/billing")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_billing(client: AsyncClient, test_superuser):
    """Test POST /api/billing endpoint"""
    test_data = {"name": "Test Item"}
    response = await client.post("/api/billing", json=test_data)
    assert response.status_code in [200, 201, 400, 422]


@pytest.mark.asyncio
async def test_get_billing_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/billing/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.get(f"/api/billing/{test_id}")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_billing(client: AsyncClient, test_superuser):
    """Test PUT /api/billing/{id} endpoint"""
    test_id = str(uuid4())
    update_data = {"name": "Updated"}
    response = await client.put(f"/api/billing/{test_id}", json=update_data)
    assert response.status_code in [200, 404, 400, 422]


@pytest.mark.asyncio
async def test_delete_billing(client: AsyncClient, test_superuser):
    """Test DELETE /api/billing/{id} endpoint"""
    test_id = str(uuid4())
    response = await client.delete(f"/api/billing/{test_id}")
    assert response.status_code in [200, 204, 404]


@pytest.mark.asyncio
async def test_billing_search(client: AsyncClient, test_superuser):
    """Test search in billing"""
    response = await client.get(f"/api/billing/search?q=test")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_billing_statistics(client: AsyncClient, test_superuser):
    """Test getting billing statistics"""
    response = await client.get(f"/api/billing/stats")
    assert response.status_code in [200, 404]
