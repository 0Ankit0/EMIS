"""Tests for dashboard functionality"""
import pytest
from apps.analytics.services.dashboard_service import DashboardService


@pytest.mark.django_db
class TestDashboard:
    """Test dashboard metrics"""
    
    def test_dashboard_summary(self):
        """Test dashboard summary generation"""
        summary = DashboardService.get_dashboard_summary()
        
        assert 'admissions_metrics' in summary
        assert 'attendance_metrics' in summary
        assert 'finance_metrics' in summary
        assert 'course_metrics' in summary
        assert 'last_updated' in summary
    
    def test_dashboard_with_zero_data(self):
        """Test dashboard handles zero data gracefully"""
        summary = DashboardService.get_dashboard_summary()
        
        # Should not raise errors even with no data
        assert summary['admissions_metrics']['total_applications'] >= 0
        assert summary['finance_metrics']['total_invoiced'] >= 0
