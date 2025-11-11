"""Contract tests for Exams API"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_exams_list(client: AsyncClient, test_superuser):
    response = await client.get("/api/exams")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_exams(client: AsyncClient, test_superuser):
    data = {"name": "Test"}
    response = await client.post("/api/exams", json=data)
    assert response.status_code in [200, 201, 422]


@pytest.mark.asyncio
async def test_get_exams_by_id(client: AsyncClient, test_superuser):
    response = await client.get("/api/exams/1")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_exams(client: AsyncClient, test_superuser):
    data = {"name": "Updated"}
    response = await client.put("/api/exams/1", json=data)
    assert response.status_code in [200, 404, 422]


@pytest.mark.asyncio
async def test_delete_exams(client: AsyncClient, test_superuser):
    response = await client.delete("/api/exams/1")
    assert response.status_code in [200, 204, 404]
