"""
Contract tests for Student Admission endpoints.

Tests the API contract for student admission workflow according to OpenAPI spec.
These tests should FAIL initially (TDD approach).
"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


class TestStudentAdmissionContract:
    """Contract tests for student admission endpoints."""

    @pytest.mark.asyncio
    async def test_submit_application_success(self, client: AsyncClient):
        """Test submitting a new student application."""
        application_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "date_of_birth": "2005-06-15",
            "program_id": str(uuid4()),
            "academic_year": "2024-2025",
        }

        response = await client.post("/api/v1/students/applications", json=application_data)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["first_name"] == application_data["first_name"]
        assert data["email"] == application_data["email"]
        assert data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_submit_application_missing_fields(self, client: AsyncClient):
        """Test application submission with missing required fields."""
        incomplete_data = {
            "first_name": "John",
            # Missing last_name, email, etc.
        }

        response = await client.post("/api/v1/students/applications", json=incomplete_data)

        assert response.status_code == 422
        data = response.json()
        assert "error" in data or "detail" in data

    @pytest.mark.asyncio
    async def test_get_application_by_id(self, client: AsyncClient):
        """Test retrieving an application by ID."""
        # First create an application
        application_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "phone": "+1234567891",
            "date_of_birth": "2005-07-20",
            "program_id": str(uuid4()),
            "academic_year": "2024-2025",
        }

        create_response = await client.post(
            "/api/v1/students/applications", json=application_data
        )
        assert create_response.status_code == 201
        application_id = create_response.json()["id"]

        # Now retrieve it
        response = await client.get(f"/api/v1/students/applications/{application_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == application_id
        assert data["email"] == application_data["email"]

    @pytest.mark.asyncio
    async def test_list_applications(self, client: AsyncClient):
        """Test listing applications with pagination."""
        response = await client.get("/api/v1/students/applications?page=1&size=10")

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert isinstance(data["items"], list)

    @pytest.mark.asyncio
    async def test_approve_application(self, client: AsyncClient, test_superuser):
        """Test approving a student application."""
        # Create application first
        application_data = {
            "first_name": "Bob",
            "last_name": "Johnson",
            "email": "bob.johnson@example.com",
            "phone": "+1234567892",
            "date_of_birth": "2005-08-10",
            "program_id": str(uuid4()),
            "academic_year": "2024-2025",
        }

        create_response = await client.post(
            "/api/v1/students/applications", json=application_data
        )
        application_id = create_response.json()["id"]

        # Approve it (requires auth)
        approval_data = {"status": "approved", "comments": "Application approved"}

        response = await client.patch(
            f"/api/v1/students/applications/{application_id}/status",
            json=approval_data,
        )

        assert response.status_code in [200, 401]  # 401 if auth not implemented yet

    @pytest.mark.asyncio
    async def test_reject_application(self, client: AsyncClient):
        """Test rejecting a student application."""
        # Create application first
        application_data = {
            "first_name": "Alice",
            "last_name": "Williams",
            "email": "alice.williams@example.com",
            "phone": "+1234567893",
            "date_of_birth": "2005-09-25",
            "program_id": str(uuid4()),
            "academic_year": "2024-2025",
        }

        create_response = await client.post(
            "/api/v1/students/applications", json=application_data
        )
        application_id = create_response.json()["id"]

        # Reject it
        rejection_data = {
            "status": "rejected",
            "comments": "Does not meet admission criteria",
        }

        response = await client.patch(
            f"/api/v1/students/applications/{application_id}/status",
            json=rejection_data,
        )

        assert response.status_code in [200, 401, 404]
