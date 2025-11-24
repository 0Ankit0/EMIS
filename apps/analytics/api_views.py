"""Analytics API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from django.utils import timezone

from .models import DashboardMetric, Report
from .serializers import DashboardMetricSerializer, ReportSerializer


class DashboardMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Dashboard Metrics"""
    queryset = DashboardMetric.objects.filter(is_active=True)
    serializer_class = DashboardMetricSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['metric_name', 'metric_key']
    
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Trigger metric recalculation"""
        metric_key = request.data.get('metric_key')
        if metric_key:
            try:
                metric = DashboardMetric.objects.get(metric_key=metric_key)
                # Trigger recalculation logic here
                metric.last_computed_at = timezone.now()
                metric.save()
                return Response({'message': 'Metric refreshed successfully'})
            except DashboardMetric.DoesNotExist:
                return Response({'error': 'Metric not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'metric_key required'}, status=status.HTTP_400_BAD_REQUEST)


class ReportViewSet(viewsets.ModelViewSet):
    """ViewSet for Reports"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'format', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'generated_at']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """Generate report"""
        report = self.get_object()
        if report.status == 'completed':
            return Response({'error': 'Report already generated'}, status=status.HTTP_400_BAD_REQUEST)
        
        report.status = 'processing'
        report.save()
        # Trigger async report generation here
        return Response({'message': 'Report generation started'})
