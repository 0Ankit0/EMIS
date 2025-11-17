"""Dashboard API endpoints"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.analytics.services.dashboard_service import DashboardService
from apps.analytics.services.admissions_metrics_service import AdmissionsMetricsService
from apps.analytics.services.attendance_metrics_service import AttendanceMetricsService
from apps.analytics.services.fee_metrics_service import FeeMetricsService
from apps.analytics.services.course_metrics_service import CourseMetricsService
from apps.analytics.serializers.dashboard import DashboardSummarySerializer
from apps.core.middleware.rbac import require_permission


class DashboardViewSet(viewsets.ViewSet):
    """ViewSet for dashboard metrics"""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    @require_permission('analytics', 'read')
    def summary(self, request):
        """
        Get complete dashboard summary
        
        GET /dashboard/summary/
        """
        summary = DashboardService.get_dashboard_summary()
        serializer = DashboardSummarySerializer(summary)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    @require_permission('analytics', 'read')
    def admissions(self, request):
        """
        Get admissions funnel metrics
        
        GET /dashboard/admissions/
        """
        metrics = AdmissionsMetricsService.calculate_funnel()
        return Response(metrics)
    
    @action(detail=False, methods=['get'])
    @require_permission('analytics', 'read')
    def attendance(self, request):
        """
        Get attendance metrics
        
        GET /dashboard/attendance/
        """
        metrics = AttendanceMetricsService.calculate_rates()
        return Response(metrics)
    
    @action(detail=False, methods=['get'])
    @require_permission('analytics', 'read')
    def finance(self, request):
        """
        Get fee collection metrics
        
        GET /dashboard/finance/
        """
        metrics = FeeMetricsService.calculate_collection()
        return Response(metrics)
    
    @action(detail=False, methods=['get'])
    @require_permission('analytics', 'read')
    def courses(self, request):
        """
        Get course completion metrics
        
        GET /dashboard/courses/
        """
        metrics = CourseMetricsService.calculate_completion()
        return Response(metrics)
    
    @action(detail=False, methods=['post'])
    @require_permission('analytics', 'update')
    def refresh(self, request):
        """
        Force refresh all metrics
        
        POST /dashboard/refresh/
        """
        summary = DashboardService.refresh_metrics()
        return Response({
            'message': 'Dashboard metrics refreshed successfully',
            'data': summary
        })
