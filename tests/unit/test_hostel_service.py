"""Tests for Hostel Service"""
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.hostel_service import HostelService


@pytest.fixture
def hostel_service():
    return HostelService()


@pytest.mark.asyncio
async def test_allocate_room(db_session: AsyncSession, hostel_service: HostelService):
    """Test room allocation"""
    allocation = await hostel_service.allocate_room(
        db_session,
        student_id=uuid4(),
        room_id=uuid4()
    )
    
    assert allocation is not None


@pytest.mark.asyncio
async def test_get_available_rooms(db_session: AsyncSession, hostel_service: HostelService):
    """Test getting available rooms"""
    rooms = await hostel_service.get_available_rooms(
        db_session,
        hostel_id=uuid4()
    )
    
    assert isinstance(rooms, list)


@pytest.mark.asyncio
async def test_vacate_room(db_session: AsyncSession, hostel_service: HostelService):
    """Test room vacation"""
    success = await hostel_service.vacate_room(
        db_session,
        allocation_id=uuid4()
    )
    
    assert isinstance(success, bool)
