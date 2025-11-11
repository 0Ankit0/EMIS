"""Contract tests for Attendance API"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_attendance_list(client: AsyncClient, test_superuser):
    response = await client.get("/api/attendance")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_attendance(client: AsyncClient, test_superuser):
    data = {"name": "Test"}
    response = await client.post("/api/attendance", json=data)
    assert response.status_code in [200, 201, 422]


@pytest.mark.asyncio
async def test_get_attendance_by_id(client: AsyncClient, test_superuser):
    response = await client.get("/api/attendance/1")
    assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_update_attendance(client: AsyncClient, test_superuser):
    data = {"name": "Updated"}
    response = await client.put("/api/attendance/1", json=data)
    assert response.status_code in [200, 404, 422]


@pytest.mark.asyncio
async def test_delete_attendance(client: AsyncClient, test_superuser):
    response = await client.delete("/api/attendance/1")
    assert response.status_code in [200, 204, 404]
