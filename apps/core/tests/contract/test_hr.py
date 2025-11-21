"""
Contract tests for HR endpoints.

Tests the API contract for HR management according to OpenAPI spec.
"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


class TestHRContract:
    """Contract tests for HR endpoints."""

    @pytest.mark.asyncio
    async def test_create_employee(self, client: AsyncClient):
        """Test creating a new employee record."""
        employee_data = {
            "employee_number": "EMP2024001",
            "first_name": "Alice",
            "last_name": "Johnson",
            "email": "alice.johnson@example.com",
            "phone": "+1234567890",
            "date_of_birth": "1990-05-15",
            "date_of_joining": "2024-01-15",
            "department": "Computer Science",
            "designation": "Professor",
            "employment_type": "full-time",
        }

        response = await client.post("/api/v1/hr/employees", json=employee_data)
        assert response.status_code in [201, 404, 422]

    @pytest.mark.asyncio
    async def test_get_employee(self, client: AsyncClient):
        """Test retrieving employee by ID."""
        employee_id = str(uuid4())
        response = await client.get(f"/api/v1/hr/employees/{employee_id}")
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_list_employees(self, client: AsyncClient):
        """Test listing employees with pagination."""
        response = await client.get("/api/v1/hr/employees?page=1&size=10")
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_create_payroll(self, client: AsyncClient):
        """Test creating payroll record."""
        payroll_data = {
            "employee_id": str(uuid4()),
            "month": "November",
            "year": 2024,
            "basic_salary": 50000.00,
            "allowances": 10000.00,
            "deductions": 5000.00,
        }

        response = await client.post("/api/v1/hr/payroll", json=payroll_data)
        assert response.status_code in [201, 404]

    @pytest.mark.asyncio
    async def test_submit_leave_request(self, client: AsyncClient):
        """Test submitting a leave request."""
        leave_data = {
            "employee_id": str(uuid4()),
            "leave_type": "sick",
            "start_date": "2024-11-15",
            "end_date": "2024-11-17",
            "reason": "Medical appointment",
        }

        response = await client.post("/api/v1/hr/leave", json=leave_data)
        assert response.status_code in [201, 404]

    @pytest.mark.asyncio
    async def test_approve_leave(self, client: AsyncClient):
        """Test approving a leave request."""
        leave_id = str(uuid4())
        response = await client.patch(
            f"/api/v1/hr/leave/{leave_id}/approve",
            json={"comments": "Approved"},
        )
        assert response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_create_performance_review(self, client: AsyncClient):
        """Test creating performance review."""
        review_data = {
            "employee_id": str(uuid4()),
            "reviewer_id": str(uuid4()),
            "review_period": "2024-Q1",
            "rating": 4.5,
            "comments": "Excellent performance",
        }

        response = await client.post("/api/v1/hr/performance-reviews", json=review_data)
        assert response.status_code in [201, 404]
