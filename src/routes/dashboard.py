"""Dashboard API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from pydantic import BaseModel

from src.database import get_db
from src.services.dashboard_service import DashboardService
from src.middleware.rbac import require_permissions

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class DashboardMetricsResponse(BaseModel):
    metric_date: date
    daily_revenue: float
    monthly_revenue: float
    daily_expenses: float
    monthly_expenses: float
    daily_profit: float
    monthly_profit: float
    total_students: int
    new_admissions_today: int
    fees_collected_today: float
    fees_pending: float
    fee_collection_rate: float
    
    class Config:
        from_attributes = True


@router.get("/metrics", response_model=DashboardMetricsResponse)
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:read"]))
):
    """Get latest dashboard metrics"""
    service = DashboardService(db)
    
    # Calculate fresh metrics for today
    metrics = await service.calculate_today_metrics()
    
    return metrics


@router.post("/metrics/refresh", response_model=DashboardMetricsResponse)
async def refresh_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:admin"]))
):
    """Manually refresh dashboard metrics"""
    service = DashboardService(db)
    metrics = await service.calculate_today_metrics()
    return metrics


@router.get("/financial-summary")
async def get_financial_summary(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:read"]))
):
    """Get financial summary"""
    service = DashboardService(db)
    summary = await service.get_financial_summary()
    return summary


@router.get("/student-summary")
async def get_student_summary(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:read"]))
):
    """Get student summary"""
    service = DashboardService(db)
    summary = await service.get_student_summary()
    return summary


@router.get("/library-summary")
async def get_library_summary(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:read"]))
):
    """Get library summary"""
    service = DashboardService(db)
    summary = await service.get_library_summary()
    return summary


# T270: Real-time data refresh endpoints
@router.get("/real-time/financial")
async def get_real_time_financial(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:read"]))
):
    """Get real-time financial metrics with auto-refresh"""
    service = DashboardService(db)
    
    # Get live data
    today = date.today()
    metrics = await service.calculate_today_metrics()
    
    # Get trending data
    trends = await service.get_financial_trends()
    
    return {
        "timestamp": today.isoformat(),
        "metrics": {
            "daily_revenue": metrics.daily_revenue,
            "monthly_revenue": metrics.monthly_revenue,
            "daily_expenses": metrics.daily_expenses,
            "monthly_expenses": metrics.monthly_expenses,
            "daily_profit": metrics.daily_profit,
            "monthly_profit": metrics.monthly_profit,
            "collection_efficiency": metrics.fee_collection_rate
        },
        "trends": trends
    }


@router.get("/real-time/students")
async def get_real_time_students(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:read"]))
):
    """Get real-time student metrics"""
    service = DashboardService(db)
    
    summary = await service.get_student_summary()
    
    return {
        "timestamp": date.today().isoformat(),
        **summary
    }


@router.get("/real-time/attendance")
async def get_real_time_attendance(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:read"]))
):
    """Get real-time attendance metrics"""
    service = DashboardService(db)
    
    attendance = await service.get_attendance_summary()
    
    return {
        "timestamp": date.today().isoformat(),
        **attendance
    }


@router.get("/kpi/overview")
async def get_kpi_overview(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["dashboard:read"]))
):
    """Get Key Performance Indicators overview"""
    service = DashboardService(db)
    
    return await service.get_kpi_overview()
