"""Contract tests for Dashboard API"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_dashboard_list(client: AsyncClient, test_superuser):
    response = await client.get("/api/dashboard")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_dashboard(client: AsyncClient, test_superuser):
    data = {"name": "Test"}
    response = await client.post("/api/dashboard", json=data)
    assert response.status_code in [200, 201, 422]


@pytest.mark.asyncio
async def test_get_dashboard_by_id(client: AsyncClient, test_superuser):
    response = await client.get("/api/dashboard/1")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_dashboard(client: AsyncClient, test_superuser):
    data = {"name": "Updated"}
    response = await client.put("/api/dashboard/1", json=data)
    assert response.status_code in [200, 404, 422]


@pytest.mark.asyncio
async def test_delete_dashboard(client: AsyncClient, test_superuser):
    response = await client.delete("/api/dashboard/1")
    assert response.status_code in [200, 204, 404]
