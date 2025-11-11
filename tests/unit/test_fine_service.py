"""Unit tests for Fine Service"""
import pytest
from datetime import date, timedelta
from unittest.mock import Mock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.fine_service import FineService
from src.models.library_settings import LibrarySettings, MemberType, FineWaiver


@pytest.fixture
def mock_db():
    """Fixture for mocked database session"""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def fine_service(mock_db):
    """Fixture for FineService instance"""
    return FineService(mock_db)


class TestFineService:
    """Test suite for FineService"""
    
    @pytest.mark.asyncio
    async def test_calculate_fine_no_overdue(self, fine_service, mock_db):
        """Test fine calculation when book is returned on time"""
        # Arrange
        settings = LibrarySettings(
            member_type=MemberType.STUDENT,
            fine_per_day=5.0,
            grace_period_days=0,
            max_fine_amount=500.0
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=settings)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        due_date = date.today()
        return_date = date.today()
        
        # Act
        fine_amount, days_overdue = await fine_service.calculate_fine(
            MemberType.STUDENT, due_date, return_date
        )
        
        # Assert
        assert fine_amount == 0.0
        assert days_overdue == 0
        
    @pytest.mark.asyncio
    async def test_calculate_fine_with_overdue_no_grace(self, fine_service, mock_db):
        """Test fine calculation with overdue days and no grace period"""
        # Arrange
        settings = LibrarySettings(
            member_type=MemberType.STUDENT,
            fine_per_day=5.0,
            grace_period_days=0,
            max_fine_amount=500.0
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=settings)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        due_date = date.today() - timedelta(days=10)
        return_date = date.today()
        
        # Act
        fine_amount, days_overdue = await fine_service.calculate_fine(
            MemberType.STUDENT, due_date, return_date
        )
        
        # Assert
        assert days_overdue == 10
        assert fine_amount == 50.0  # 10 days * 5.0 per day
        
    @pytest.mark.asyncio
    async def test_calculate_fine_with_grace_period(self, fine_service, mock_db):
        """Test fine calculation with grace period"""
        # Arrange
        settings = LibrarySettings(
            member_type=MemberType.FACULTY,
            fine_per_day=0.0,
            grace_period_days=7,
            max_fine_amount=0.0
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=settings)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        due_date = date.today() - timedelta(days=5)
        return_date = date.today()
        
        # Act
        fine_amount, days_overdue = await fine_service.calculate_fine(
            MemberType.FACULTY, due_date, return_date
        )
        
        # Assert
        assert days_overdue == 5
        assert fine_amount == 0.0  # Within grace period
        
    @pytest.mark.asyncio
    async def test_calculate_fine_exceeds_max(self, fine_service, mock_db):
        """Test fine calculation with max fine cap"""
        # Arrange
        settings = LibrarySettings(
            member_type=MemberType.ALUMNI,
            fine_per_day=10.0,
            grace_period_days=0,
            max_fine_amount=500.0
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=settings)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        due_date = date.today() - timedelta(days=60)
        return_date = date.today()
        
        # Act
        fine_amount, days_overdue = await fine_service.calculate_fine(
            MemberType.ALUMNI, due_date, return_date
        )
        
        # Assert
        assert days_overdue == 60
        assert fine_amount == 500.0  # Capped at max fine (not 600)
        
    @pytest.mark.asyncio
    async def test_create_library_settings(self, fine_service, mock_db):
        """Test creating library settings"""
        # Arrange
        settings_data = {
            "member_type": MemberType.STUDENT,
            "max_books_allowed": 5,
            "borrowing_period_days": 14,
            "fine_per_day": 5.0,
            "grace_period_days": 0,
            "max_fine_amount": 500.0
        }
        
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        # Check if exists
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=None)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Act
        result = await fine_service.create_library_settings(**settings_data)
        
        # Assert
        assert mock_db.add.called
        assert mock_db.commit.called
        
    @pytest.mark.asyncio
    async def test_create_fine_waiver(self, fine_service, mock_db):
        """Test creating a fine waiver"""
        # Arrange
        waiver_data = {
            "fine_id": 123,
            "member_id": 456,
            "original_amount": 150.0,
            "waived_amount": 100.0,
            "reason": "Medical emergency",
            "approved_by": 789
        }
        
        mock_db.add = Mock()
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        
        # Act
        result = await fine_service.create_fine_waiver(**waiver_data)
        
        # Assert
        assert mock_db.add.called
        assert mock_db.commit.called
        
    @pytest.mark.asyncio
    async def test_get_library_settings(self, fine_service, mock_db):
        """Test retrieving library settings by member type"""
        # Arrange
        mock_settings = LibrarySettings(
            id=1,
            member_type=MemberType.STUDENT,
            fine_per_day=5.0
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=mock_settings)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        # Act
        result = await fine_service.get_library_settings(MemberType.STUDENT)
        
        # Assert
        assert result == mock_settings
        assert result.member_type == MemberType.STUDENT
        
    @pytest.mark.asyncio
    async def test_calculate_fine_default_return_date(self, fine_service, mock_db):
        """Test fine calculation with default return date (today)"""
        # Arrange
        settings = LibrarySettings(
            member_type=MemberType.STUDENT,
            fine_per_day=5.0,
            grace_period_days=0,
            max_fine_amount=500.0
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none = Mock(return_value=settings)
        mock_db.execute = AsyncMock(return_value=mock_result)
        
        due_date = date.today() - timedelta(days=3)
        
        # Act
        fine_amount, days_overdue = await fine_service.calculate_fine(
            MemberType.STUDENT, due_date
        )
        
        # Assert
        assert days_overdue == 3
        assert fine_amount == 15.0
