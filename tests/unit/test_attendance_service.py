"""Unit tests for AttendanceService"""
import pytest
from datetime import datetime, date, timedelta
from uuid import uuid4
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.attendance_service import AttendanceService
from src.models.attendance import Attendance


@pytest.fixture
def attendance_service():
    """Create attendance service instance"""
    return AttendanceService()


class TestAttendanceService:
    """Test cases for AttendanceService"""

    def test_calculate_attendance_percentage(self, attendance_service):
        """Test attendance percentage calculation"""
        total_classes = 100
        attended_classes = 85
        
        percentage = attendance_service.calculate_percentage(
            attended_classes, total_classes
        )
        
        assert percentage == 85.0

    def test_calculate_attendance_percentage_zero_total(self, attendance_service):
        """Test percentage calculation with zero total classes"""
        percentage = attendance_service.calculate_percentage(5, 0)
        assert percentage == 0.0

    def test_is_attendance_low(self, attendance_service):
        """Test checking if attendance is low"""
        assert attendance_service.is_low_attendance(70.0, threshold=75.0) is True
        assert attendance_service.is_low_attendance(80.0, threshold=75.0) is False
        assert attendance_service.is_low_attendance(75.0, threshold=75.0) is False

    def test_calculate_required_classes(self, attendance_service):
        """Test calculating required classes to meet threshold"""
        # Current: 70 attended out of 100 (70%)
        # Target: 75%
        # Need to attend next N classes to reach 75%
        
        current_attended = 70
        current_total = 100
        target_percentage = 75.0
        
        required = attendance_service.calculate_required_classes(
            current_attended, current_total, target_percentage
        )
        
        # (70 + required) / (100 + required) = 0.75
        # 70 + required = 75 + 0.75 * required
        # 0.25 * required = 5
        # required = 20
        
        assert required == 20

    def test_validate_attendance_date(self, attendance_service):
        """Test validating attendance date"""
        # Future date should be invalid
        future_date = datetime.utcnow() + timedelta(days=1)
        assert attendance_service.is_valid_attendance_date(future_date) is False
        
        # Today should be valid
        today = datetime.utcnow()
        assert attendance_service.is_valid_attendance_date(today) is True
        
        # Past date should be valid
        past_date = datetime.utcnow() - timedelta(days=1)
        assert attendance_service.is_valid_attendance_date(past_date) is True

    def test_get_attendance_status(self, attendance_service):
        """Test getting attendance status based on percentage"""
        assert attendance_service.get_status(90.0) == "excellent"
        assert attendance_service.get_status(80.0) == "good"
        assert attendance_service.get_status(75.0) == "satisfactory"
        assert attendance_service.get_status(70.0) == "low"
        assert attendance_service.get_status(60.0) == "critical"

    def test_calculate_monthly_attendance(self, attendance_service):
        """Test calculating attendance for a month"""
        attendance_records = [
            {"date": date(2024, 1, 1), "status": "present"},
            {"date": date(2024, 1, 2), "status": "present"},
            {"date": date(2024, 1, 3), "status": "absent"},
            {"date": date(2024, 1, 4), "status": "present"},
            {"date": date(2024, 1, 5), "status": "late"},
        ]
        
        present_count = sum(1 for r in attendance_records if r["status"] in ["present", "late"])
        total_count = len(attendance_records)
        
        percentage = attendance_service.calculate_percentage(present_count, total_count)
        
        assert percentage == 80.0  # 4 out of 5

    def test_format_attendance_report(self, attendance_service):
        """Test formatting attendance report"""
        report_data = {
            "total_classes": 100,
            "attended": 85,
            "absent": 15,
            "percentage": 85.0,
            "status": "good"
        }
        
        formatted = attendance_service.format_report(report_data)
        
        assert "85.0%" in formatted
        assert "85/100" in formatted or "attended" in formatted.lower()

    def test_get_working_days(self, attendance_service):
        """Test calculating working days in a month"""
        # January 2024 has 31 days
        # Assuming 5-day work week (Mon-Fri)
        
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 31)
        
        working_days = attendance_service.get_working_days(start_date, end_date)
        
        # This is a simplified test - actual working days would depend on holidays
        assert working_days >= 20  # At least 20 working days in a month
        assert working_days <= 23  # At most 23 working days

    def test_is_weekend(self, attendance_service):
        """Test checking if a date is weekend"""
        # Saturday
        saturday = date(2024, 1, 6)  # January 6, 2024 is Saturday
        assert attendance_service.is_weekend(saturday) is True
        
        # Sunday
        sunday = date(2024, 1, 7)
        assert attendance_service.is_weekend(sunday) is True
        
        # Monday
        monday = date(2024, 1, 8)
        assert attendance_service.is_weekend(monday) is False

    def test_calculate_consecutive_absences(self, attendance_service):
        """Test calculating consecutive absences"""
        attendance_records = [
            {"date": date(2024, 1, 1), "status": "present"},
            {"date": date(2024, 1, 2), "status": "absent"},
            {"date": date(2024, 1, 3), "status": "absent"},
            {"date": date(2024, 1, 4), "status": "absent"},
            {"date": date(2024, 1, 5), "status": "present"},
        ]
        
        max_consecutive = attendance_service.get_max_consecutive_absences(
            attendance_records
        )
        
        assert max_consecutive == 3

    def test_needs_warning(self, attendance_service):
        """Test checking if student needs warning"""
        # Low attendance
        assert attendance_service.needs_warning(70.0, threshold=75.0) is True
        
        # Good attendance
        assert attendance_service.needs_warning(85.0, threshold=75.0) is False
        
        # At threshold
        assert attendance_service.needs_warning(75.0, threshold=75.0) is False
