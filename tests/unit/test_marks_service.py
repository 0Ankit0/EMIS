"""Tests for Marks Service"""
import pytest
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.marks_service import MarksService


@pytest.fixture
def marks_service():
    return MarksService()


@pytest.mark.asyncio
async def test_record_marks(db_session: AsyncSession, marks_service: MarksService):
    """Test recording student marks"""
    marks_data = {
        "student_id": uuid4(),
        "course_id": uuid4(),
        "exam_id": uuid4(),
        "theory_marks": Decimal("40.0"),
        "practical_marks": Decimal("45.0"),
        "total_marks": Decimal("85.0")
    }
    
    marks = await marks_service.record_marks(db_session, marks_data)
    
    assert marks is not None
    assert marks.total_marks == Decimal("85.0")


@pytest.mark.asyncio
async def test_calculate_sgpa(marks_service: MarksService):
    """Test SGPA calculation"""
    grade_points = [
        {"grade": "A+", "credits": 4, "points": 10},
        {"grade": "A", "credits": 3, "points": 9},
        {"grade": "B", "credits": 3, "points": 8}
    ]
    
    sgpa = marks_service.calculate_sgpa(grade_points)
    
    # (10*4 + 9*3 + 8*3) / (4+3+3) = (40+27+24)/10 = 91/10 = 9.1
    assert sgpa == Decimal("9.1")


@pytest.mark.asyncio
async def test_calculate_cgpa(marks_service: MarksService):
    """Test CGPA calculation"""
    sgpa_list = [Decimal("9.0"), Decimal("8.5"), Decimal("9.2")]
    
    cgpa = marks_service.calculate_cgpa(sgpa_list)
    
    # (9.0 + 8.5 + 9.2) / 3 = 26.7/3 = 8.9
    assert cgpa == Decimal("8.9")


@pytest.mark.asyncio
async def test_get_marks_by_student(db_session: AsyncSession, marks_service: MarksService):
    """Test getting marks for a student"""
    student_id = uuid4()
    
    # Record some marks
    marks_data = {
        "student_id": student_id,
        "course_id": uuid4(),
        "exam_id": uuid4(),
        "total_marks": Decimal("85.0")
    }
    await marks_service.record_marks(db_session, marks_data)
    
    marks_list = await marks_service.get_student_marks(db_session, student_id)
    
    assert len(marks_list) >= 1


@pytest.mark.asyncio
async def test_calculate_grade_from_marks(marks_service: MarksService):
    """Test converting marks to grade"""
    assert marks_service.marks_to_grade(Decimal("95.0")) == "A+"
    assert marks_service.marks_to_grade(Decimal("85.0")) == "A"
    assert marks_service.marks_to_grade(Decimal("75.0")) == "B"
    assert marks_service.marks_to_grade(Decimal("65.0")) == "C"
    assert marks_service.marks_to_grade(Decimal("50.0")) == "D"
    assert marks_service.marks_to_grade(Decimal("35.0")) == "F"


@pytest.mark.asyncio
async def test_get_top_scorers(db_session: AsyncSession, marks_service: MarksService):
    """Test getting top scorers"""
    course_id = uuid4()
    
    # Add marks for multiple students
    for i in range(5):
        marks_data = {
            "student_id": uuid4(),
            "course_id": course_id,
            "exam_id": uuid4(),
            "total_marks": Decimal(f"{80 + i * 2}.0")
        }
        await marks_service.record_marks(db_session, marks_data)
    
    top_scorers = await marks_service.get_top_scorers(db_session, course_id, limit=3)
    
    assert len(top_scorers) == 3
