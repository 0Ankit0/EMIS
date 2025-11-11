"""Tests for Dashboard Service"""
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.dashboard_service import DashboardService


@pytest.fixture
def dashboard_service():
    return DashboardService()


@pytest.mark.asyncio
async def test_get_dashboard_metrics(db_session: AsyncSession, dashboard_service: DashboardService):
    """Test getting dashboard metrics"""
    metrics = await dashboard_service.get_metrics(db_session)
    
    assert metrics is not None
    assert "total_students" in metrics
    assert "total_faculty" in metrics
    assert "active_courses" in metrics


@pytest.mark.asyncio
async def test_get_enrollment_statistics(db_session: AsyncSession, dashboard_service: DashboardService):
    """Test enrollment statistics"""
    stats = await dashboard_service.get_enrollment_stats(db_session)
    
    assert stats is not None
    assert "total_enrolled" in stats


@pytest.mark.asyncio
async def test_get_financial_overview(db_session: AsyncSession, dashboard_service: DashboardService):
    """Test financial overview"""
    overview = await dashboard_service.get_financial_overview(db_session)
    
    assert overview is not None
    assert "total_revenue" in overview
    assert "total_expenses" in overview


@pytest.mark.asyncio
async def test_get_attendance_trends(db_session: AsyncSession, dashboard_service: DashboardService):
    """Test attendance trends"""
    trends = await dashboard_service.get_attendance_trends(
        db_session,
        days=30
    )
    
    assert trends is not None
    assert isinstance(trends, list)


@pytest.mark.asyncio
async def test_get_recent_activities(db_session: AsyncSession, dashboard_service: DashboardService):
    """Test recent activities"""
    activities = await dashboard_service.get_recent_activities(
        db_session,
        limit=10
    )
    
    assert activities is not None
    assert len(activities) <= 10


@pytest.mark.asyncio
async def test_get_pending_tasks(db_session: AsyncSession, dashboard_service: DashboardService):
    """Test pending tasks"""
    tasks = await dashboard_service.get_pending_tasks(
        db_session,
        user_id=uuid4()
    )
    
    assert tasks is not None
    assert isinstance(tasks, list)
