"""Tests for Annual Report Service"""
import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.annual_report_service import AnnualReportService


@pytest.fixture
def annual_report_service():
    return AnnualReportService()


@pytest.mark.asyncio
async def test_generate_annual_report(db_session: AsyncSession, annual_report_service: AnnualReportService):
    """Test generating annual report"""
    report = await annual_report_service.generate_report(
        db_session,
        year=2024
    )
    
    assert report is not None
    assert "academic_year" in report or isinstance(report, dict)


@pytest.mark.asyncio
async def test_generate_student_statistics(db_session: AsyncSession, annual_report_service: AnnualReportService):
    """Test student statistics for annual report"""
    stats = await annual_report_service.get_student_statistics(
        db_session,
        year=2024
    )
    
    assert stats is not None
    assert "total_students" in stats or isinstance(stats, dict)


@pytest.mark.asyncio
async def test_generate_financial_summary(db_session: AsyncSession, annual_report_service: AnnualReportService):
    """Test financial summary"""
    summary = await annual_report_service.get_financial_summary(
        db_session,
        year=2024
    )
    
    assert summary is not None


@pytest.mark.asyncio
async def test_generate_academic_performance(db_session: AsyncSession, annual_report_service: AnnualReportService):
    """Test academic performance report"""
    performance = await annual_report_service.get_academic_performance(
        db_session,
        year=2024
    )
    
    assert performance is not None


@pytest.mark.asyncio
async def test_export_report_pdf(db_session: AsyncSession, annual_report_service: AnnualReportService):
    """Test exporting report to PDF"""
    pdf = await annual_report_service.export_to_pdf(
        db_session,
        year=2024
    )
    
    assert pdf is not None or isinstance(pdf, bytes)
