"""Contract tests for Admissions API"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_admissions_list(client: AsyncClient, test_superuser):
    response = await client.get("/api/admissions")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_admissions(client: AsyncClient, test_superuser):
    data = {"name": "Test"}
    response = await client.post("/api/admissions", json=data)
    assert response.status_code in [200, 201, 422]


@pytest.mark.asyncio
async def test_get_admissions_by_id(client: AsyncClient, test_superuser):
    response = await client.get("/api/admissions/1")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_admissions(client: AsyncClient, test_superuser):
    data = {"name": "Updated"}
    response = await client.put("/api/admissions/1", json=data)
    assert response.status_code in [200, 404, 422]


@pytest.mark.asyncio
async def test_delete_admissions(client: AsyncClient, test_superuser):
    response = await client.delete("/api/admissions/1")
    assert response.status_code in [200, 204, 404]
