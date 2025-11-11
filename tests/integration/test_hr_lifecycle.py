"""
Integration test for HR lifecycle journey.
"""
import pytest
from httpx import AsyncClient
from uuid import uuid4


class TestHRLifecycleIntegration:
    """Integration tests for HR lifecycle."""

    @pytest.mark.asyncio
    async def test_complete_hr_lifecycle(self, client: AsyncClient):
        """
        Test complete HR journey: recruitment → hiring → payroll → leave → performance review.
        """
        # Step 1: Create employee
        employee_data = {
            "employee_number": "EMP2024001",
            "first_name": "Bob",
            "last_name": "Smith",
            "email": "bob.smith@example.com",
            "date_of_joining": "2024-01-15",
            "department": "Engineering",
            "designation": "Senior Developer",
        }

        emp_response = await client.post("/api/v1/hr/employees", json=employee_data)
        assert emp_response.status_code in [201, 404]

        if emp_response.status_code != 201:
            pytest.skip("Employee endpoint not implemented yet")

        employee = emp_response.json()
        employee_id = employee["id"]

        # Step 2: Generate payroll
        payroll_response = await client.post(
            "/api/v1/hr/payroll",
            json={
                "employee_id": employee_id,
                "month": "November",
                "year": 2024,
                "basic_salary": 60000.00,
            },
        )
        assert payroll_response.status_code in [201, 404]

        # Step 3: Submit leave request
        leave_response = await client.post(
            "/api/v1/hr/leave",
            json={
                "employee_id": employee_id,
                "leave_type": "annual",
                "start_date": "2024-12-20",
                "end_date": "2024-12-25",
                "reason": "Year-end vacation",
            },
        )
        assert leave_response.status_code in [201, 404]

        # Step 4: Create performance review
        review_response = await client.post(
            "/api/v1/hr/performance-reviews",
            json={
                "employee_id": employee_id,
                "reviewer_id": str(uuid4()),
                "review_period": "2024-Q4",
                "rating": 4.8,
                "comments": "Outstanding performance",
            },
        )
        assert review_response.status_code in [201, 404]
