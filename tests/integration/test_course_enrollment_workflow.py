"""Integration tests for Course Enrollment Workflow"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student
from src.models.course import Course, Enrollment


@pytest.mark.asyncio
async def test_complete_course_enrollment_workflow(db_session: AsyncSession):
    """Test complete course enrollment from registration to completion"""
    # Step 1: Create student
    student = Student(
        id=uuid4(),
        student_id="STU001",
        first_name="Alice",
        last_name="Student",
        email="alice@example.com",
        program="B.Tech",
        semester=1,
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    
    # Step 2: Create courses
    courses = []
    for i in range(5):
        course = Course(
            id=uuid4(),
            course_code=f"CS10{i+1}",
            course_name=f"Course {i+1}",
            credits=4,
            semester=1,
            max_students=60,
            enrolled_students=0,
            status="active"
        )
        db_session.add(course)
        courses.append(course)
    await db_session.commit()
    
    # Step 3: Enroll in courses
    enrollments = []
    for course in courses:
        enrollment = Enrollment(
            id=uuid4(),
            student_id=student.id,
            course_id=course.id,
            enrollment_date=datetime.utcnow(),
            status="enrolled"
        )
        db_session.add(enrollment)
        enrollments.append(enrollment)
        course.enrolled_students += 1
    
    await db_session.commit()
    
    # Step 4: Complete semester - assign grades
    for enrollment in enrollments:
        enrollment.grade = "A"
        enrollment.grade_points = Decimal("9.0")
        enrollment.credits_earned = 4
        enrollment.status = "completed"
    
    await db_session.commit()
    
    # Step 5: Calculate SGPA
    total_grade_points = sum(e.grade_points * e.credits_earned for e in enrollments)
    total_credits = sum(e.credits_earned for e in enrollments)
    sgpa = total_grade_points / total_credits
    
    student.sgpa = sgpa
    await db_session.commit()
    
    # Assertions
    assert len(enrollments) == 5
    assert all(e.status == "completed" for e in enrollments)
    assert student.sgpa == Decimal("9.0")
    assert all(c.enrolled_students == 1 for c in courses)
