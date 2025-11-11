"""Comprehensive tests for Exam Service"""
import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.exam import Exam, ExamSchedule, ExamResult
from src.services.exam_service import ExamService


@pytest.fixture
def exam_service():
    return ExamService()


@pytest.mark.asyncio
async def test_create_exam(db_session: AsyncSession, exam_service: ExamService):
    """Test creating an exam"""
    exam_data = {
        "exam_name": "Mid-Term Exam",
        "course_id": uuid4(),
        "exam_type": "written",
        "total_marks": Decimal("100.0"),
        "duration_minutes": 180,
        "academic_year": "2024-25",
        "semester": 1
    }
    
    exam = await exam_service.create_exam(db_session, exam_data)
    
    assert exam is not None
    assert exam.exam_name == "Mid-Term Exam"
    assert exam.total_marks == Decimal("100.0")


@pytest.mark.asyncio
async def test_schedule_exam(db_session: AsyncSession, exam_service: ExamService):
    """Test scheduling an exam"""
    exam_data = {
        "exam_name": "Final Exam",
        "course_id": uuid4(),
        "exam_type": "written",
        "total_marks": Decimal("100.0"),
        "duration_minutes": 180
    }
    exam = await exam_service.create_exam(db_session, exam_data)
    
    schedule_data = {
        "exam_date": date(2024, 12, 15),
        "start_time": datetime(2024, 12, 15, 10, 0),
        "venue": "Main Exam Hall",
        "invigilators": [uuid4(), uuid4()]
    }
    
    schedule = await exam_service.schedule_exam(
        db_session,
        exam_id=exam.id,
        **schedule_data
    )
    
    assert schedule is not None
    assert schedule.venue == "Main Exam Hall"


@pytest.mark.asyncio
async def test_submit_exam_result(db_session: AsyncSession, exam_service: ExamService):
    """Test submitting exam results"""
    exam_data = {
        "exam_name": "Quiz 1",
        "course_id": uuid4(),
        "total_marks": Decimal("50.0")
    }
    exam = await exam_service.create_exam(db_session, exam_data)
    
    result_data = {
        "student_id": uuid4(),
        "marks_obtained": Decimal("42.5"),
        "grade": "A"
    }
    
    result = await exam_service.submit_result(
        db_session,
        exam_id=exam.id,
        **result_data
    )
    
    assert result is not None
    assert result.marks_obtained == Decimal("42.5")
    assert result.grade == "A"


@pytest.mark.asyncio
async def test_calculate_grade(exam_service: ExamService):
    """Test grade calculation"""
    assert exam_service.calculate_grade(Decimal("95.0"), Decimal("100.0")) == "A+"
    assert exam_service.calculate_grade(Decimal("85.0"), Decimal("100.0")) == "A"
    assert exam_service.calculate_grade(Decimal("75.0"), Decimal("100.0")) == "B"
    assert exam_service.calculate_grade(Decimal("65.0"), Decimal("100.0")) == "C"
    assert exam_service.calculate_grade(Decimal("50.0"), Decimal("100.0")) == "D"
    assert exam_service.calculate_grade(Decimal("35.0"), Decimal("100.0")) == "F"


@pytest.mark.asyncio
async def test_publish_results(db_session: AsyncSession, exam_service: ExamService):
    """Test publishing exam results"""
    exam_data = {
        "exam_name": "End-Term",
        "course_id": uuid4(),
        "total_marks": Decimal("100.0")
    }
    exam = await exam_service.create_exam(db_session, exam_data)
    
    success = await exam_service.publish_results(
        db_session,
        exam_id=exam.id,
        published_by=uuid4()
    )
    
    assert success is True


@pytest.mark.asyncio
async def test_get_student_results(db_session: AsyncSession, exam_service: ExamService):
    """Test getting student exam results"""
    student_id = uuid4()
    
    # Create exam and result
    exam_data = {"exam_name": "Test", "course_id": uuid4(), "total_marks": Decimal("100.0")}
    exam = await exam_service.create_exam(db_session, exam_data)
    
    await exam_service.submit_result(
        db_session,
        exam_id=exam.id,
        student_id=student_id,
        marks_obtained=Decimal("80.0"),
        grade="A"
    )
    
    results = await exam_service.get_student_results(db_session, student_id)
    
    assert len(results) >= 1
    assert results[0].student_id == student_id


@pytest.mark.asyncio
async def test_calculate_percentage(exam_service: ExamService):
    """Test percentage calculation"""
    percentage = exam_service.calculate_percentage(
        Decimal("85.0"),
        Decimal("100.0")
    )
    assert percentage == Decimal("85.0")


@pytest.mark.asyncio
async def test_get_exam_statistics(db_session: AsyncSession, exam_service: ExamService):
    """Test getting exam statistics"""
    exam_data = {
        "exam_name": "Statistics Test",
        "course_id": uuid4(),
        "total_marks": Decimal("100.0")
    }
    exam = await exam_service.create_exam(db_session, exam_data)
    
    # Add some results
    for i in range(5):
        await exam_service.submit_result(
            db_session,
            exam_id=exam.id,
            student_id=uuid4(),
            marks_obtained=Decimal(f"{70 + i * 5}.0"),
            grade="B"
        )
    
    stats = await exam_service.get_statistics(db_session, exam.id)
    
    assert stats is not None
    assert "average_marks" in stats
    assert "highest_marks" in stats
    assert "lowest_marks" in stats
