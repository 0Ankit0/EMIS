"""Unit tests for Schedule Service"""
import pytest
from datetime import time, date, timedelta
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.schedule_service import ScheduleService
from src.models.class_schedule import ClassSchedule, DayOfWeek


@pytest.fixture
def mock_db():
    """Fixture for mocked database session"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def schedule_service(mock_db):
    """Fixture for ScheduleService instance"""
    return ScheduleService(mock_db)


class TestScheduleService:
    """Test suite for ScheduleService"""
    
    @pytest.mark.asyncio
    async def test_create_schedule_success(self, schedule_service, mock_db):
        """Test successful schedule creation"""
        # Arrange
        schedule_data = {
            "course_id": 1,
            "instructor_id": 5,
            "day_of_week": DayOfWeek.MONDAY,
            "start_time": time(9, 0),
            "end_time": time(10, 30),
            "effective_from": date.today(),
            "room_number": "A-101",
            "building": "Main Block"
        }
        
        mock_schedule = ClassSchedule(id=1, **schedule_data)
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        # Act
        result = await schedule_service.create_schedule(**schedule_data)
        
        # Assert
        assert mock_db.add.called
        assert mock_db.commit.called
        
    @pytest.mark.asyncio
    async def test_check_schedule_conflict_with_conflict(self, schedule_service, mock_db):
        """Test schedule conflict detection when conflict exists"""
        # Arrange
        existing_schedule = ClassSchedule(
            id=1,
            course_id=1,
            instructor_id=5,
            day_of_week=DayOfWeek.MONDAY,
            start_time=time(9, 0),
            end_time=time(10, 30),
            effective_from=date.today()
        )
        
        mock_result = Mock()
        mock_result.scalars = Mock(return_value=Mock(first=Mock(return_value=existing_schedule)))
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Act
        has_conflict = await schedule_service.check_schedule_conflict(
            instructor_id=5,
            room_number=None,
            day_of_week=DayOfWeek.MONDAY,
            start_time=time(9, 30),
            end_time=time(11, 0)
        )
        
        # Assert
        assert has_conflict is True
        
    @pytest.mark.asyncio
    async def test_check_schedule_conflict_no_conflict(self, schedule_service, mock_db):
        """Test schedule conflict detection when no conflict exists"""
        # Arrange
        mock_result = Mock()
        mock_result.scalars = Mock(return_value=Mock(first=Mock(return_value=None)))
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Act
        has_conflict = await schedule_service.check_schedule_conflict(
            instructor_id=5,
            room_number="A-101",
            day_of_week=DayOfWeek.TUESDAY,
            start_time=time(14, 0),
            end_time=time(15, 30)
        )
        
        # Assert
        assert has_conflict is False
        
    @pytest.mark.asyncio
    async def test_get_schedule_by_id_found(self, schedule_service, mock_db):
        """Test retrieving schedule by ID when it exists"""
        # Arrange
        mock_schedule = ClassSchedule(
            id=1,
            course_id=1,
            day_of_week=DayOfWeek.MONDAY,
            start_time=time(9, 0),
            end_time=time(10, 30),
            effective_from=date.today()
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=mock_schedule)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Act
        result = await schedule_service.get_schedule_by_id(1)
        
        # Assert
        assert result == mock_schedule
        assert result.id == 1
        
    @pytest.mark.asyncio
    async def test_get_schedule_by_id_not_found(self, schedule_service, mock_db):
        """Test retrieving schedule by ID when it doesn't exist"""
        # Arrange
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=None)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Act
        result = await schedule_service.get_schedule_by_id(999)
        
        # Assert
        assert result is None
        
    @pytest.mark.asyncio
    async def test_get_schedules_by_course(self, schedule_service, mock_db):
        """Test retrieving schedules by course ID"""
        # Arrange
        mock_schedules = [
            ClassSchedule(id=1, course_id=1, day_of_week=DayOfWeek.MONDAY),
            ClassSchedule(id=2, course_id=1, day_of_week=DayOfWeek.WEDNESDAY)
        ]
        
        mock_result = Mock()
        mock_result.scalars = Mock(return_value=Mock(all=Mock(return_value=mock_schedules)))
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Act
        result = await schedule_service.get_schedules_by_course(1)
        
        # Assert
        assert len(result) == 2
        assert result[0].course_id == 1
        
    @pytest.mark.asyncio
    async def test_update_schedule_success(self, schedule_service, mock_db):
        """Test successful schedule update"""
        # Arrange
        existing_schedule = ClassSchedule(
            id=1,
            course_id=1,
            day_of_week=DayOfWeek.MONDAY,
            start_time=time(9, 0),
            end_time=time(10, 30),
            effective_from=date.today()
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=existing_schedule)
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        updates = {
            "start_time": time(10, 0),
            "end_time": time(11, 30)
        }
        
        # Act
        result = await schedule_service.update_schedule(1, updates)
        
        # Assert
        assert mock_db.commit.called
        assert result.start_time == time(10, 0)
        
    @pytest.mark.asyncio
    async def test_delete_schedule_success(self, schedule_service, mock_db):
        """Test successful schedule deletion"""
        # Arrange
        existing_schedule = ClassSchedule(id=1, course_id=1)
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=existing_schedule)
        mock_db.execute = AsyncMock(return_value=mock_result)
        mock_db.delete = AsyncMock()
        mock_db.commit = AsyncMock()
        
        # Act
        result = await schedule_service.delete_schedule(1)
        
        # Assert
        assert result is True
        assert mock_db.delete.called
        assert mock_db.commit.called
        
    @pytest.mark.asyncio
    async def test_delete_schedule_not_found(self, schedule_service, mock_db):
        """Test deleting non-existent schedule"""
        # Arrange
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=None)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Act
        result = await schedule_service.delete_schedule(999)
        
        # Assert
        assert result is False
        assert not mock_db.delete.called
