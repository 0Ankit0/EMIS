"""Tests for Teacher Hierarchy Service"""
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.teacher_hierarchy_service import TeacherHierarchyService


@pytest.fixture
def teacher_hierarchy_service():
    return TeacherHierarchyService()


@pytest.mark.asyncio
async def test_assign_hod(db_session: AsyncSession, teacher_hierarchy_service: TeacherHierarchyService):
    """Test assigning Head of Department"""
    assignment = await teacher_hierarchy_service.assign_hod(
        db_session,
        department_id=uuid4(),
        faculty_id=uuid4()
    )
    
    assert assignment is not None


@pytest.mark.asyncio
async def test_assign_coordinator(db_session: AsyncSession, teacher_hierarchy_service: TeacherHierarchyService):
    """Test assigning program coordinator"""
    assignment = await teacher_hierarchy_service.assign_coordinator(
        db_session,
        program_id=uuid4(),
        faculty_id=uuid4()
    )
    
    assert assignment is not None


@pytest.mark.asyncio
async def test_get_department_hierarchy(db_session: AsyncSession, teacher_hierarchy_service: TeacherHierarchyService):
    """Test getting department hierarchy"""
    hierarchy = await teacher_hierarchy_service.get_hierarchy(
        db_session,
        department_id=uuid4()
    )
    
    assert hierarchy is not None or isinstance(hierarchy, dict)


@pytest.mark.asyncio
async def test_assign_mentor(db_session: AsyncSession, teacher_hierarchy_service: TeacherHierarchyService):
    """Test assigning mentor to students"""
    assignment = await teacher_hierarchy_service.assign_mentor(
        db_session,
        faculty_id=uuid4(),
        student_ids=[uuid4(), uuid4(), uuid4()]
    )
    
    assert assignment is not None


@pytest.mark.asyncio
async def test_get_faculty_subordinates(db_session: AsyncSession, teacher_hierarchy_service: TeacherHierarchyService):
    """Test getting faculty subordinates"""
    subordinates = await teacher_hierarchy_service.get_subordinates(
        db_session,
        faculty_id=uuid4()
    )
    
    assert isinstance(subordinates, list)


@pytest.mark.asyncio
async def test_remove_from_hierarchy(db_session: AsyncSession, teacher_hierarchy_service: TeacherHierarchyService):
    """Test removing faculty from hierarchy"""
    success = await teacher_hierarchy_service.remove_from_hierarchy(
        db_session,
        faculty_id=uuid4()
    )
    
    assert isinstance(success, bool)
