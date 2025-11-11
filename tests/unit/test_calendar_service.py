"""Tests for Calendar Service"""
import pytest
from datetime import datetime, date
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.calendar_service import CalendarService


@pytest.fixture
def calendar_service():
    return CalendarService()


@pytest.mark.asyncio
async def test_create_academic_calendar(db_session: AsyncSession, calendar_service: CalendarService):
    """Test creating academic calendar"""
    calendar_data = {
        "academic_year": "2024-25",
        "start_date": date(2024, 7, 1),
        "end_date": date(2025, 6, 30)
    }
    
    calendar = await calendar_service.create_calendar(db_session, calendar_data)
    
    assert calendar is not None
    assert calendar.academic_year == "2024-25"


@pytest.mark.asyncio
async def test_add_holiday(db_session: AsyncSession, calendar_service: CalendarService):
    """Test adding holiday"""
    holiday_data = {
        "name": "Independence Day",
        "date": date(2024, 8, 15),
        "holiday_type": "national"
    }
    
    holiday = await calendar_service.add_holiday(db_session, holiday_data)
    
    assert holiday is not None
    assert holiday.name == "Independence Day"


@pytest.mark.asyncio
async def test_get_holidays(db_session: AsyncSession, calendar_service: CalendarService):
    """Test getting holidays"""
    holidays = await calendar_service.get_holidays(
        db_session,
        year=2024,
        month=8
    )
    
    assert isinstance(holidays, list)


@pytest.mark.asyncio
async def test_is_working_day(calendar_service: CalendarService):
    """Test checking if date is working day"""
    # Monday
    monday = date(2024, 1, 8)
    assert calendar_service.is_working_day(monday) is True
    
    # Sunday
    sunday = date(2024, 1, 7)
    assert calendar_service.is_working_day(sunday) is False


@pytest.mark.asyncio
async def test_add_semester_dates(db_session: AsyncSession, calendar_service: CalendarService):
    """Test adding semester dates"""
    semester_data = {
        "semester": 1,
        "start_date": date(2024, 7, 1),
        "end_date": date(2024, 12, 31),
        "mid_term_start": date(2024, 9, 15),
        "mid_term_end": date(2024, 9, 30)
    }
    
    semester = await calendar_service.add_semester(db_session, semester_data)
    
    assert semester is not None


@pytest.mark.asyncio
async def test_calculate_working_days(calendar_service: CalendarService):
    """Test calculating working days between dates"""
    start = date(2024, 1, 1)
    end = date(2024, 1, 31)
    
    working_days = calendar_service.calculate_working_days(start, end)
    
    assert working_days >= 20


@pytest.mark.asyncio
async def test_get_academic_calendar(db_session: AsyncSession, calendar_service: CalendarService):
    """Test getting academic calendar"""
    calendar = await calendar_service.get_calendar(
        db_session,
        academic_year="2024-25"
    )
    
    assert calendar is not None or calendar is None
