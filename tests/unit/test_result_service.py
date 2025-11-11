"""Tests for Result Service"""
import pytest
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.result_service import ResultService


@pytest.fixture
def result_service():
    return ResultService()


@pytest.mark.asyncio
async def test_publish_result(db_session: AsyncSession, result_service: ResultService):
    """Test publishing exam result"""
    result_data = {
        "student_id": uuid4(),
        "exam_id": uuid4(),
        "course_id": uuid4(),
        "marks_obtained": Decimal("85.0"),
        "total_marks": Decimal("100.0"),
        "grade": "A"
    }
    
    result = await result_service.publish_result(db_session, result_data)
    
    assert result is not None
    assert result.grade == "A"


@pytest.mark.asyncio
async def test_calculate_percentage(result_service: ResultService):
    """Test percentage calculation"""
    percentage = result_service.calculate_percentage(
        Decimal("85.0"),
        Decimal("100.0")
    )
    
    assert percentage == Decimal("85.0")


@pytest.mark.asyncio
async def test_generate_marksheet(db_session: AsyncSession, result_service: ResultService):
    """Test generating marksheet"""
    student_id = uuid4()
    
    # Add some results
    for i in range(3):
        result_data = {
            "student_id": student_id,
            "exam_id": uuid4(),
            "course_id": uuid4(),
            "marks_obtained": Decimal(f"{80 + i}.0"),
            "total_marks": Decimal("100.0"),
            "grade": "A"
        }
        await result_service.publish_result(db_session, result_data)
    
    marksheet = await result_service.generate_marksheet(db_session, student_id)
    
    assert marksheet is not None
    assert len(marksheet["results"]) == 3


@pytest.mark.asyncio
async def test_calculate_final_grade(result_service: ResultService):
    """Test final grade calculation"""
    grades = ["A", "A+", "B", "A"]
    
    final_grade = result_service.calculate_final_grade(grades)
    
    assert final_grade in ["A", "A+", "B"]


@pytest.mark.asyncio
async def test_check_pass_fail(result_service: ResultService):
    """Test pass/fail determination"""
    assert result_service.is_pass(Decimal("40.0"), Decimal("100.0")) is True
    assert result_service.is_pass(Decimal("30.0"), Decimal("100.0")) is False


@pytest.mark.asyncio
async def test_get_semester_results(db_session: AsyncSession, result_service: ResultService):
    """Test getting semester results"""
    student_id = uuid4()
    
    result_data = {
        "student_id": student_id,
        "exam_id": uuid4(),
        "course_id": uuid4(),
        "marks_obtained": Decimal("90.0"),
        "total_marks": Decimal("100.0"),
        "semester": 1
    }
    await result_service.publish_result(db_session, result_data)
    
    results = await result_service.get_semester_results(
        db_session,
        student_id=student_id,
        semester=1
    )
    
    assert len(results) >= 1
