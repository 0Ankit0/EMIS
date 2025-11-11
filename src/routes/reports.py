"""Reports API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
import os
from io import BytesIO

from src.database import get_db
from src.services.quarterly_report_service import QuarterlyReportService
from src.services.annual_report_service import AnnualReportService
from src.models.reports import ReportType, ReportStatus
from src.middleware.rbac import require_permissions
from src.lib.pdf_generator import PDFGenerator
from src.lib.excel_export import ExcelExporter

router = APIRouter(prefix="/reports", tags=["reports"])


class QuarterlyReportResponse(BaseModel):
    id: int
    report_number: str
    financial_year: str
    quarter: int
    total_income: float
    total_expenses: float
    net_profit_loss: float
    student_count: int
    employee_count: int
    fee_collection_rate: float
    status: ReportStatus
    
    class Config:
        from_attributes = True


class AnnualReportResponse(BaseModel):
    id: int
    report_number: str
    financial_year: str
    total_annual_revenue: float
    total_annual_expenses: float
    net_annual_profit_loss: float
    annual_profit_margin: float
    status: ReportStatus
    
    class Config:
        from_attributes = True


@router.post("/quarterly", response_model=QuarterlyReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_quarterly_report(
    financial_year: str,
    quarter: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:generate"]))
):
    """Generate quarterly financial report"""
    if quarter < 1 or quarter > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quarter must be between 1 and 4"
        )
    
    service = QuarterlyReportService(db)
    report = await service.generate_quarterly_report(
        financial_year=financial_year,
        quarter=quarter,
        generated_by=current_user.get("id")
    )
    
    return report


@router.get("/quarterly/{report_id}", response_model=QuarterlyReportResponse)
async def get_quarterly_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """Get quarterly report by ID"""
    service = QuarterlyReportService(db)
    report = await service.get_report_by_id(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )
    
    return report


@router.get("/quarterly", response_model=List[QuarterlyReportResponse])
async def list_quarterly_reports(
    financial_year: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """List all quarterly reports"""
    service = QuarterlyReportService(db)
    reports = await service.get_all_reports(financial_year)
    return reports


@router.get("/quarterly/{report_id}/pdf")
async def download_report_pdf(
    report_id: int,
    download: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """Generate and download/view report PDF
    
    Args:
        report_id: ID of the report
        download: If True, forces download. If False, displays inline (for print)
    
    Returns:
        PDF file as response
    """
    service = QuarterlyReportService(db)
    report = await service.get_report_by_id(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )
    
    pdf_generator = PDFGenerator()
    filepath = f"/tmp/report_{report.report_number}.pdf"
    
    pdf_generator.generate_quarterly_report_pdf(
        report=report,
        filepath=filepath
    )
    
    # Determine content disposition based on download parameter
    content_disposition = "attachment" if download else "inline"
    filename = f"Quarterly_Report_Q{report.quarter}_{report.financial_year}.pdf"
    
    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f'{content_disposition}; filename="{filename}"',
            "Cache-Control": "no-cache"
        }
    )


@router.get("/quarterly/{report_id}/excel")
async def download_report_excel(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """Generate and download report as Excel file"""
    service = QuarterlyReportService(db)
    report = await service.get_report_by_id(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )
    
    excel_exporter = ExcelExporter()
    filepath = f"/tmp/report_{report.report_number}.xlsx"
    
    excel_exporter.export_quarterly_report(
        report=report,
        filepath=filepath
    )
    
    filename = f"Quarterly_Report_Q{report.quarter}_{report.financial_year}.xlsx"
    
    return FileResponse(
        path=filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache"
        }
    )


@router.get("/quarterly/{report_id}/print")
async def print_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """Generate print-optimized PDF for direct printing
    
    Returns PDF with inline disposition to open in browser print dialog
    """
    service = QuarterlyReportService(db)
    report = await service.get_report_by_id(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report {report_id} not found"
        )
    
    pdf_generator = PDFGenerator()
    filepath = f"/tmp/report_print_{report.report_number}.pdf"
    
    pdf_generator.generate_quarterly_report_pdf(
        report=report,
        filepath=filepath
    )
    
    filename = f"Print_Quarterly_Report_Q{report.quarter}_{report.financial_year}.pdf"
    
    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "no-cache",
            "X-Print-Preview": "true"
        }
    )


# Annual Report Endpoints

@router.post("/annual", response_model=AnnualReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_annual_report(
    financial_year: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:generate"]))
):
    """Generate comprehensive annual financial report"""
    service = AnnualReportService(db)
    report = await service.generate_annual_report(
        financial_year=financial_year,
        generated_by=current_user.get("id")
    )
    
    return report


@router.get("/annual/{report_id}", response_model=AnnualReportResponse)
async def get_annual_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """Get annual report by ID"""
    service = AnnualReportService(db)
    report = await service.get_report_by_id(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annual report {report_id} not found"
        )
    
    return report


@router.get("/annual", response_model=List[AnnualReportResponse])
async def list_annual_reports(
    financial_year: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """List all annual reports"""
    service = AnnualReportService(db)
    reports = await service.get_all_reports(financial_year)
    return reports


@router.get("/annual/{report_id}/pdf")
async def download_annual_report_pdf(
    report_id: int,
    download: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """Download or view annual report as PDF"""
    service = AnnualReportService(db)
    report = await service.get_report_by_id(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annual report {report_id} not found"
        )
    
    pdf_generator = PDFGenerator()
    filepath = f"/tmp/annual_report_{report.report_number}.pdf"
    
    pdf_generator.generate_annual_report_pdf(
        report=report,
        filepath=filepath
    )
    
    content_disposition = "attachment" if download else "inline"
    filename = f"Annual_Report_{report.financial_year}.pdf"
    
    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f'{content_disposition}; filename="{filename}"',
            "Cache-Control": "no-cache"
        }
    )


@router.get("/annual/{report_id}/excel")
async def download_annual_report_excel(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """Download annual report as Excel"""
    service = AnnualReportService(db)
    report = await service.get_report_by_id(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annual report {report_id} not found"
        )
    
    excel_exporter = ExcelExporter()
    filepath = f"/tmp/annual_report_{report.report_number}.xlsx"
    
    excel_exporter.export_annual_report(
        report=report,
        filepath=filepath
    )
    
    filename = f"Annual_Report_{report.financial_year}.xlsx"
    
    return FileResponse(
        path=filepath,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-cache"
        }
    )


@router.get("/annual/{report_id}/print")
async def print_annual_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:read"]))
):
    """Generate print-optimized PDF for annual report"""
    service = AnnualReportService(db)
    report = await service.get_report_by_id(report_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annual report {report_id} not found"
        )
    
    pdf_generator = PDFGenerator()
    filepath = f"/tmp/annual_report_print_{report.report_number}.pdf"
    
    pdf_generator.generate_annual_report_pdf(
        report=report,
        filepath=filepath
    )
    
    filename = f"Print_Annual_Report_{report.financial_year}.pdf"
    
    return FileResponse(
        path=filepath,
        media_type="application/pdf",
        filename=filename,
        headers={
            "Content-Disposition": f'inline; filename="{filename}"',
            "Cache-Control": "no-cache",
            "X-Print-Preview": "true"
        }
    )


@router.post("/annual/{report_id}/approve")
async def approve_annual_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["reports:approve"]))
):
    """Approve an annual report"""
    service = AnnualReportService(db)
    
    try:
        report = await service.approve_report(report_id, current_user.get("id"))
        return {
            "message": "Report approved successfully",
            "report_id": report.id,
            "approved_by": report.approved_by,
            "approved_at": report.approved_at
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
