"""Integration tests for Exam Workflow"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.exam import Exam, ExamSchedule, ExamResult
from src.models.student import Student
from src.models.course import Course


@pytest.mark.asyncio
async def test_complete_exam_workflow(db_session: AsyncSession):
    """Test complete exam workflow from creation to result publication"""
    # Step 1: Create course
    course = Course(
        id=uuid4(),
        course_code="CS101",
        course_name="Programming",
        credits=4,
        status="active"
    )
    db_session.add(course)
    await db_session.commit()
    
    # Step 2: Create student
    student = Student(
        id=uuid4(),
        student_id="STU001",
        first_name="Test",
        last_name="Student",
        email="student@example.com",
        program="B.Tech",
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    
    # Step 3: Create exam
    exam = Exam(
        id=uuid4(),
        exam_name="Mid-Term",
        course_id=course.id,
        exam_type="written",
        total_marks=Decimal("100.0"),
        duration_minutes=180,
        status="scheduled"
    )
    db_session.add(exam)
    await db_session.commit()
    
    # Step 4: Schedule exam
    schedule = ExamSchedule(
        id=uuid4(),
        exam_id=exam.id,
        exam_date=date(2024, 12, 15),
        start_time=datetime(2024, 12, 15, 10, 0),
        venue="Hall A",
        status="confirmed"
    )
    db_session.add(schedule)
    await db_session.commit()
    
    # Step 5: Conduct exam
    exam.status = "completed"
    await db_session.commit()
    
    # Step 6: Submit result
    result = ExamResult(
        id=uuid4(),
        exam_id=exam.id,
        student_id=student.id,
        marks_obtained=Decimal("85.0"),
        total_marks=Decimal("100.0"),
        percentage=Decimal("85.0"),
        grade="A",
        status="published"
    )
    db_session.add(result)
    await db_session.commit()
    
    # Step 7: Publish results
    exam.results_published = True
    exam.published_at = datetime.utcnow()
    await db_session.commit()
    
    # Assertions
    assert exam.results_published is True
    assert result.grade == "A"
    assert result.percentage == Decimal("85.0")
