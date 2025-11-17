"""Celery task for periodic dashboard refresh"""
from celery import shared_task
from apps.analytics.services.dashboard_service import DashboardService


@shared_task
def refresh_dashboard_metrics():
    """Periodic task to refresh dashboard metrics"""
    DashboardService.refresh_metrics()
    return "Dashboard metrics refreshed successfully"
