"""Students API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count

from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """ViewSet for Students"""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['program', 'current_semester', 'status', 'enrollment_year']
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'user__email']
    ordering_fields = ['created_at', 'enrollment_date']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get detailed student profile"""
        student = self.get_object()
        serializer = self.get_serializer(student)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        """Get student's course enrollments"""
        from apps.courses.models import Enrollment
        from apps.courses.serializers import EnrollmentSerializer
        
        student = self.get_object()
        enrollments = Enrollment.objects.filter(student=student)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get student's attendance records"""
        from apps.attendance.models import AttendanceRecord
        from apps.attendance.serializers import AttendanceRecordSerializer
        
        student = self.get_object()
        records = AttendanceRecord.objects.filter(student=student)
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get student statistics"""
        queryset = self.get_queryset()
        stats = {
            'total': queryset.count(),
            'by_status': dict(queryset.values('status').annotate(count=Count('id')).values_list('status', 'count')),
            'by_program': dict(queryset.values('program__name').annotate(count=Count('id')).values_list('program__name', 'count')),
        }
        return Response(stats)
