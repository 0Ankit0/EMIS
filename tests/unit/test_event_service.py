"""Tests for Event Service"""
import pytest
from datetime import datetime
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.event_service import EventService


@pytest.fixture
def event_service():
    return EventService()


@pytest.mark.asyncio
async def test_create_event(db_session: AsyncSession, event_service: EventService):
    """Test creating event"""
    event = await event_service.create_event(
        db_session,
        event_name="Tech Fest",
        event_date=datetime(2024, 6, 15),
        venue="Main Auditorium"
    )
    
    assert event is not None


@pytest.mark.asyncio
async def test_register_participant(db_session: AsyncSession, event_service: EventService):
    """Test participant registration"""
    registration = await event_service.register_participant(
        db_session,
        event_id=uuid4(),
        student_id=uuid4()
    )
    
    assert registration is not None


@pytest.mark.asyncio
async def test_get_event_participants(db_session: AsyncSession, event_service: EventService):
    """Test getting event participants"""
    participants = await event_service.get_participants(
        db_session,
        event_id=uuid4()
    )
    
    assert isinstance(participants, list)
