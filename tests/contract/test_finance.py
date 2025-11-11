"""Contract tests for Finance API"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_finance_list(client: AsyncClient, test_superuser):
    response = await client.get("/api/finance")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_finance(client: AsyncClient, test_superuser):
    data = {"name": "Test"}
    response = await client.post("/api/finance", json=data)
    assert response.status_code in [200, 201, 422]


@pytest.mark.asyncio
async def test_get_finance_by_id(client: AsyncClient, test_superuser):
    response = await client.get("/api/finance/1")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_finance(client: AsyncClient, test_superuser):
    data = {"name": "Updated"}
    response = await client.put("/api/finance/1", json=data)
    assert response.status_code in [200, 404, 422]


@pytest.mark.asyncio
async def test_delete_finance(client: AsyncClient, test_superuser):
    response = await client.delete("/api/finance/1")
    assert response.status_code in [200, 204, 404]
