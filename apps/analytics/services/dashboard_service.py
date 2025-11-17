"""Dashboard service for aggregating all metrics"""
from typing import Dict, Any
from django.utils import timezone
from django.core.cache import cache
from apps.analytics.models import DashboardMetric
from apps.analytics.services.admissions_metrics_service import AdmissionsMetricsService
from apps.analytics.services.attendance_metrics_service import AttendanceMetricsService
from apps.analytics.services.fee_metrics_service import FeeMetricsService
from apps.analytics.services.course_metrics_service import CourseMetricsService


class DashboardService:
    """Service for dashboard metric aggregation and caching"""
    
    CACHE_TIMEOUT = 3600  # 1 hour
    
    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        """Get complete dashboard summary with all metrics"""
        
        # Try cache first
        cached = cache.get('dashboard_summary')
        if cached:
            return cached
        
        # Calculate all metrics
        summary = {
            'admissions_metrics': AdmissionsMetricsService.calculate_funnel(),
            'attendance_metrics': AttendanceMetricsService.calculate_rates(),
            'finance_metrics': FeeMetricsService.calculate_collection(),
            'course_metrics': CourseMetricsService.calculate_completion(),
            'last_updated': timezone.now().isoformat(),
        }
        
        # Cache the result
        cache.set('dashboard_summary', summary, DashboardService.CACHE_TIMEOUT)
        
        # Store in database
        DashboardService._store_metrics(summary)
        
        return summary
    
    @staticmethod
    def _store_metrics(summary: Dict[str, Any]):
        """Store calculated metrics in database"""
        for category, metrics in summary.items():
            if category == 'last_updated':
                continue
            
            metric_key = f"{category}_summary"
            DashboardMetric.objects.update_or_create(
                metric_key=metric_key,
                defaults={
                    'metric_name': category.replace('_', ' ').title(),
                    'computed_value': metrics,
                    'category': category.split('_')[0],
                    'is_active': True,
                }
            )
    
    @staticmethod
    def refresh_metrics():
        """Force refresh all metrics"""
        cache.delete('dashboard_summary')
        return DashboardService.get_dashboard_summary()
