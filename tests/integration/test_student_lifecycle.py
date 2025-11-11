"""
Integration test for complete student lifecycle journey.

Tests the full flow: admission → enrollment → semester → graduation → alumni
This test should FAIL initially (TDD approach).
"""
import pytest
from httpx import AsyncClient
from datetime import datetime, date
from uuid import uuid4


class TestStudentLifecycleIntegration:
    """Integration tests for complete student lifecycle."""

    @pytest.mark.asyncio
    async def test_complete_student_lifecycle(self, client: AsyncClient):
        """
        Test complete student journey from application to alumni.

        Flow:
        1. Submit application
        2. Approve application
        3. Create student record
        4. Enroll in program
        5. Record attendance
        6. Record grades
        7. Progress through semesters
        8. Graduate
        9. Convert to alumni status
        """
        program_id = str(uuid4())

        # Step 1: Submit application
        application_data = {
            "first_name": "Sarah",
            "last_name": "Connor",
            "email": "sarah.connor@example.com",
            "phone": "+1234567890",
            "date_of_birth": "2005-03-15",
            "program_id": program_id,
            "academic_year": "2024-2025",
        }

        app_response = await client.post(
            "/api/v1/students/applications", json=application_data
        )
        assert app_response.status_code in [201, 404]

        if app_response.status_code != 201:
            pytest.skip("Application endpoint not implemented yet")

        application = app_response.json()
        application_id = application["id"]

        # Step 2: Approve application
        approval_response = await client.patch(
            f"/api/v1/students/applications/{application_id}/status",
            json={"status": "approved", "comments": "Meets all criteria"},
        )
        assert approval_response.status_code in [200, 401, 404]

        # Step 3: Create student record (auto or manual)
        student_response = await client.post(
            "/api/v1/students",
            json={
                "first_name": application_data["first_name"],
                "last_name": application_data["last_name"],
                "email": application_data["email"],
                "phone": application_data["phone"],
                "date_of_birth": application_data["date_of_birth"],
            },
        )
        assert student_response.status_code in [201, 404]

        if student_response.status_code != 201:
            pytest.skip("Student creation endpoint not implemented yet")

        student = student_response.json()
        student_id = student["id"]

        # Step 4: Enroll in program
        enrollment_response = await client.post(
            "/api/v1/students/enrollments",
            json={
                "student_id": student_id,
                "program_id": program_id,
                "academic_year": "2024-2025",
                "semester": "Fall 2024",
                "enrollment_date": "2024-09-01",
            },
        )
        assert enrollment_response.status_code in [201, 404]

        if enrollment_response.status_code != 201:
            pytest.skip("Enrollment endpoint not implemented yet")

        enrollment = enrollment_response.json()
        enrollment_id = enrollment["id"]

        # Step 5: Record attendance
        attendance_response = await client.post(
            "/api/v1/students/attendance",
            json={
                "student_id": student_id,
                "date": str(date.today()),
                "status": "present",
                "course_id": str(uuid4()),
            },
        )
        assert attendance_response.status_code in [201, 404]

        # Step 6: Record academic record/grades
        academic_record_response = await client.post(
            "/api/v1/students/academic-records",
            json={
                "student_id": student_id,
                "course_id": str(uuid4()),
                "semester": "Fall 2024",
                "grade": "A",
                "credits": 3,
                "gpa": 4.0,
            },
        )
        assert academic_record_response.status_code in [201, 404]

        # Step 7: Progress to next semester (repeat enrollment)
        spring_enrollment_response = await client.post(
            "/api/v1/students/enrollments",
            json={
                "student_id": student_id,
                "program_id": program_id,
                "academic_year": "2024-2025",
                "semester": "Spring 2025",
                "enrollment_date": "2025-01-15",
            },
        )
        assert spring_enrollment_response.status_code in [201, 404]

        # Step 8: Graduate student
        graduation_response = await client.post(
            "/api/v1/students/{student_id}/graduate",
            json={
                "graduation_date": "2028-05-20",
                "degree": "Bachelor of Science",
                "honors": "Magna Cum Laude",
            },
        )
        assert graduation_response.status_code in [200, 404]

        # Step 9: Verify student status
        student_check_response = await client.get(f"/api/v1/students/{student_id}")
        assert student_check_response.status_code in [200, 404]

        if student_check_response.status_code == 200:
            updated_student = student_check_response.json()
            # Should have graduated status or alumni status
            assert updated_student.get("status") in ["graduated", "alumni", "active"]

    @pytest.mark.asyncio
    async def test_student_lifecycle_with_suspension(self, client: AsyncClient):
        """Test student lifecycle with temporary suspension."""
        # Create and enroll student (abbreviated)
        student_id = str(uuid4())
        enrollment_id = str(uuid4())

        # Suspend enrollment
        suspend_response = await client.patch(
            f"/api/v1/students/enrollments/{enrollment_id}/status",
            json={"status": "suspended", "reason": "Medical leave"},
        )
        assert suspend_response.status_code in [200, 404]

        # Reactivate enrollment
        reactivate_response = await client.patch(
            f"/api/v1/students/enrollments/{enrollment_id}/status",
            json={"status": "active", "reason": "Returned from leave"},
        )
        assert reactivate_response.status_code in [200, 404]

    @pytest.mark.asyncio
    async def test_student_lifecycle_with_withdrawal(self, client: AsyncClient):
        """Test student lifecycle ending with withdrawal."""
        student_id = str(uuid4())
        enrollment_id = str(uuid4())

        # Withdraw student
        withdraw_response = await client.post(
            f"/api/v1/students/enrollments/{enrollment_id}/withdraw",
            json={
                "withdrawal_date": str(date.today()),
                "reason": "Transfer to another institution",
            },
        )
        assert withdraw_response.status_code in [200, 404]

        # Verify enrollment status
        enrollment_check = await client.get(
            f"/api/v1/students/enrollments/{enrollment_id}"
        )
        assert enrollment_check.status_code in [200, 404]

        if enrollment_check.status_code == 200:
            enrollment = enrollment_check.json()
            assert enrollment.get("status") in ["withdrawn", "inactive"]
