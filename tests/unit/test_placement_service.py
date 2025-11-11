"""Tests for Placement Service"""
import pytest
from datetime import date
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.placement_service import PlacementService


@pytest.fixture
def placement_service():
    return PlacementService()


@pytest.mark.asyncio
async def test_register_company(db_session: AsyncSession, placement_service: PlacementService):
    """Test company registration"""
    company = await placement_service.register_company(
        db_session,
        company_name="TechCorp",
        contact_email="hr@techcorp.com"
    )
    
    assert company is not None


@pytest.mark.asyncio
async def test_schedule_drive(db_session: AsyncSession, placement_service: PlacementService):
    """Test scheduling placement drive"""
    drive = await placement_service.schedule_drive(
        db_session,
        company_id=uuid4(),
        drive_date=date(2024, 6, 15)
    )
    
    assert drive is not None


@pytest.mark.asyncio
async def test_register_student_for_drive(db_session: AsyncSession, placement_service: PlacementService):
    """Test student registration for drive"""
    registration = await placement_service.register_student(
        db_session,
        drive_id=uuid4(),
        student_id=uuid4()
    )
    
    assert registration is not None


@pytest.mark.asyncio
async def test_update_placement_status(db_session: AsyncSession, placement_service: PlacementService):
    """Test updating placement status"""
    success = await placement_service.update_status(
        db_session,
        registration_id=uuid4(),
        status="selected"
    )
    
    assert isinstance(success, bool)
