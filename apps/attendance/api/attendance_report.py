"""Attendance Report API Views"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from ..models import AttendanceReport
from ..serializers import AttendanceReportSerializer


class AttendanceReportViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AttendanceReport (read-only)"""
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student', 'course', 'month', 'year', 'status']
    search_fields = ['student__first_name', 'student__last_name']
    
    def get_queryset(self):
        return AttendanceReport.objects.select_related(
            'student', 'course'
        ).all()
    
    @action(detail=False, methods=['get'])
    def low_attendance(self, request):
        """Get students with low attendance"""
        threshold = request.query_params.get('threshold', 75)
        reports = self.get_queryset().filter(
            attendance_percentage__lt=threshold
        ).order_by('attendance_percentage')
        
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)
