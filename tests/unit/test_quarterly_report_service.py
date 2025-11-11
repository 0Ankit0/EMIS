"""Tests for Quarterly Report Service"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.quarterly_report_service import QuarterlyReportService


@pytest.fixture
def quarterly_report_service():
    return QuarterlyReportService()


@pytest.mark.asyncio
async def test_generate_quarterly_report(db_session: AsyncSession, quarterly_report_service: QuarterlyReportService):
    """Test generating quarterly report"""
    report = await quarterly_report_service.generate_report(
        db_session,
        year=2024,
        quarter=1
    )
    
    assert report is not None


@pytest.mark.asyncio
async def test_get_enrollment_trends(db_session: AsyncSession, quarterly_report_service: QuarterlyReportService):
    """Test enrollment trends"""
    trends = await quarterly_report_service.get_enrollment_trends(
        db_session,
        year=2024,
        quarter=1
    )
    
    assert trends is not None


@pytest.mark.asyncio
async def test_get_financial_performance(db_session: AsyncSession, quarterly_report_service: QuarterlyReportService):
    """Test financial performance for quarter"""
    performance = await quarterly_report_service.get_financial_performance(
        db_session,
        year=2024,
        quarter=1
    )
    
    assert performance is not None


@pytest.mark.asyncio
async def test_get_attendance_summary(db_session: AsyncSession, quarterly_report_service: QuarterlyReportService):
    """Test attendance summary"""
    summary = await quarterly_report_service.get_attendance_summary(
        db_session,
        year=2024,
        quarter=1
    )
    
    assert summary is not None


@pytest.mark.asyncio
async def test_compare_quarters(db_session: AsyncSession, quarterly_report_service: QuarterlyReportService):
    """Test comparing quarters"""
    comparison = await quarterly_report_service.compare_quarters(
        db_session,
        year=2024,
        quarter1=1,
        quarter2=2
    )
    
    assert comparison is not None
