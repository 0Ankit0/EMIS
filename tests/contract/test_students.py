"""Contract tests for Students API endpoints"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_students_list(client: AsyncClient, test_superuser):
    """Test GET /api/students endpoint"""
    response = await client.get("/api/students")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, (list, dict))


@pytest.mark.asyncio
async def test_create_student(client: AsyncClient, test_superuser):
    """Test POST /api/students endpoint"""
    student_data = {
        "first_name": "Test",
        "last_name": "Student",
        "email": "teststudent@example.com",
        "phone": "1234567890",
        "program": "B.Tech",
        "date_of_birth": "2005-01-01"
    }
    
    response = await client.post("/api/students", json=student_data)
    
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["email"] == "teststudent@example.com"


@pytest.mark.asyncio
async def test_get_student_by_id(client: AsyncClient, test_superuser):
    """Test GET /api/students/{id} endpoint"""
    # First create a student
    student_data = {
        "first_name": "Get",
        "last_name": "Test",
        "email": "get@example.com",
        "phone": "9876543210",
        "program": "MBA"
    }
    create_response = await client.post("/api/students", json=student_data)
    created = create_response.json()
    
    # Then retrieve it
    response = await client.get(f"/api/students/{created['id']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created["id"]


@pytest.mark.asyncio
async def test_update_student(client: AsyncClient, test_superuser):
    """Test PUT /api/students/{id} endpoint"""
    student_data = {
        "first_name": "Update",
        "last_name": "Test",
        "email": "update@example.com",
        "phone": "1111111111",
        "program": "M.Tech"
    }
    create_response = await client.post("/api/students", json=student_data)
    created = create_response.json()
    
    # Update
    update_data = {"phone": "2222222222"}
    response = await client.put(f"/api/students/{created['id']}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "2222222222"


@pytest.mark.asyncio
async def test_delete_student(client: AsyncClient, test_superuser):
    """Test DELETE /api/students/{id} endpoint"""
    student_data = {
        "first_name": "Delete",
        "last_name": "Test",
        "email": "delete@example.com",
        "phone": "3333333333",
        "program": "BBA"
    }
    create_response = await client.post("/api/students", json=student_data)
    created = create_response.json()
    
    # Delete
    response = await client.delete(f"/api/students/{created['id']}")
    
    assert response.status_code in [200, 204]


@pytest.mark.asyncio
async def test_search_students(client: AsyncClient, test_superuser):
    """Test GET /api/students/search endpoint"""
    response = await client.get("/api/students/search?q=Test")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_student_by_program(client: AsyncClient, test_superuser):
    """Test GET /api/students/program/{program} endpoint"""
    response = await client.get("/api/students/program/B.Tech")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_student_analytics(client: AsyncClient, test_superuser):
    """Test GET /api/students/analytics endpoint"""
    response = await client.get("/api/students/analytics")
    
    assert response.status_code == 200
    data = response.json()
    assert "total" in data or "total_students" in data
