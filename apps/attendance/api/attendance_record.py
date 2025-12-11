"""Attendance Record API Views"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from ..models import AttendanceRecord
from ..serializers import AttendanceRecordSerializer, AttendanceRecordListSerializer


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for AttendanceRecord"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'session', 'status']
    search_fields = ['student__first_name', 'student__last_name', 'remarks']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AttendanceRecordListSerializer
        return AttendanceRecordSerializer
    
    def get_queryset(self):
        queryset = AttendanceRecord.objects.select_related(
            'student', 'session', 'marked_by'
        ).all()
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def bulk_mark(self, request):
        """Bulk mark attendance for multiple students"""
        students = request.data.get('students', [])
        session_id = request.data.get('session')
        status_value = request.data.get('status', 'present')
        
        if not students or not session_id:
            return Response(
                {'error': 'students and session are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        records = []
        for student_id in students:
            record = AttendanceRecord.objects.create(
                student_id=student_id,
                session_id=session_id,
                status=status_value,
                marked_by=request.user
            )
            records.append(record)
        
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def student_history(self, request):
        """Get attendance history for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        records = self.get_queryset().filter(student_id=student_id)
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)
