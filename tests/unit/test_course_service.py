"""Tests for Course Service"""
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.course_service import CourseService


@pytest.fixture
def course_service():
    return CourseService()


@pytest.mark.asyncio
async def test_create_course(db_session: AsyncSession, course_service: CourseService):
    """Test creating a course"""
    course_data = {
        "course_code": "CS101",
        "course_name": "Introduction to Programming",
        "credits": 4,
        "semester": 1,
        "department_id": uuid4()
    }
    
    course = await course_service.create_course(db_session, course_data)
    
    assert course is not None
    assert course.course_code == "CS101"
    assert course.credits == 4


@pytest.mark.asyncio
async def test_get_course_by_code(db_session: AsyncSession, course_service: CourseService):
    """Test retrieving course by code"""
    course_data = {
        "course_code": "CS102",
        "course_name": "Data Structures",
        "credits": 4
    }
    created = await course_service.create_course(db_session, course_data)
    
    course = await course_service.get_course_by_code(db_session, "CS102")
    
    assert course is not None
    assert course.course_code == "CS102"


@pytest.mark.asyncio
async def test_assign_faculty(db_session: AsyncSession, course_service: CourseService):
    """Test assigning faculty to course"""
    course_data = {"course_code": "CS103", "course_name": "Algorithms", "credits": 3}
    course = await course_service.create_course(db_session, course_data)
    
    success = await course_service.assign_faculty(
        db_session,
        course_id=course.id,
        faculty_id=uuid4()
    )
    
    assert success is True


@pytest.mark.asyncio
async def test_get_courses_by_semester(db_session: AsyncSession, course_service: CourseService):
    """Test getting courses by semester"""
    for i in range(3):
        course_data = {
            "course_code": f"CS10{i+4}",
            "course_name": f"Course {i+1}",
            "credits": 3,
            "semester": 1
        }
        await course_service.create_course(db_session, course_data)
    
    courses = await course_service.get_courses_by_semester(db_session, semester=1)
    
    assert len(courses) >= 3


@pytest.mark.asyncio
async def test_enroll_student(db_session: AsyncSession, course_service: CourseService):
    """Test enrolling student in course"""
    course_data = {"course_code": "CS107", "course_name": "Database", "credits": 4}
    course = await course_service.create_course(db_session, course_data)
    
    success = await course_service.enroll_student(
        db_session,
        course_id=course.id,
        student_id=uuid4()
    )
    
    assert success is True


@pytest.mark.asyncio
async def test_update_course(db_session: AsyncSession, course_service: CourseService):
    """Test updating course details"""
    course_data = {"course_code": "CS108", "course_name": "Networks", "credits": 3}
    course = await course_service.create_course(db_session, course_data)
    
    updated = await course_service.update_course(
        db_session,
        course_id=course.id,
        update_data={"credits": 4}
    )
    
    assert updated.credits == 4
