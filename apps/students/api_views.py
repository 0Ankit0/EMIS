"""
Student API views
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.utils import timezone

from .models import Student, StudentStatus
from .serializers import (
    StudentListSerializer,
    StudentDetailSerializer,
    StudentCreateSerializer,
    StudentUpdateSerializer,
    AdmissionSerializer,
    GraduationSerializer,
    StatusChangeSerializer,
    StudentBulkUploadSerializer
)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Student CRUD operations and workflows
    
    Endpoints:
    - GET /api/v1/students/ - List all students
    - POST /api/v1/students/ - Create new student
    - GET /api/v1/students/{id}/ - Get student details
    - PUT /api/v1/students/{id}/ - Update student
    - DELETE /api/v1/students/{id}/ - Delete student
    - POST /api/v1/students/{id}/admit/ - Admit student
    - POST /api/v1/students/{id}/graduate/ - Graduate student
    - POST /api/v1/students/{id}/change_status/ - Change status
    - GET /api/v1/students/statistics/ - Get statistics
    """
    
    queryset = Student.objects.select_related('user', 'created_by', 'updated_by').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering
    filterset_fields = {
        'status': ['exact', 'in'],
        'gender': ['exact'],
        'admission_date': ['gte', 'lte'],
        'created_at': ['gte', 'lte'],
    }
    
    # Search
    search_fields = [
        'student_number', 'first_name', 'last_name', 'email', 
        'phone', 'city', 'country'
    ]
    
    # Ordering
    ordering_fields = [
        'student_number', 'first_name', 'last_name', 'email',
        'status', 'admission_date', 'created_at', 'current_gpa'
    ]
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return StudentListSerializer
        elif self.action == 'create':
            return StudentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return StudentUpdateSerializer
        elif self.action == 'admit':
            return AdmissionSerializer
        elif self.action == 'graduate':
            return GraduationSerializer
        elif self.action == 'change_status':
            return StatusChangeSerializer
        elif self.action == 'bulk_upload':
            return StudentBulkUploadSerializer
        return StudentDetailSerializer
    
    def perform_create(self, serializer):
        """Set created_by when creating student"""
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        """Set updated_by when updating student"""
        serializer.save(updated_by=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get student statistics
        GET /api/v1/students/statistics/
        """
        stats = {
            'total': Student.objects.count(),
            'by_status': {},
            'active': Student.objects.filter(status=StudentStatus.ACTIVE).count(),
            'applicants': Student.objects.filter(status=StudentStatus.APPLICANT).count(),
            'graduated': Student.objects.filter(status=StudentStatus.GRADUATED).count(),
            'suspended': Student.objects.filter(status=StudentStatus.SUSPENDED).count(),
            'withdrawn': Student.objects.filter(status=StudentStatus.WITHDRAWN).count(),
            'alumni': Student.objects.filter(status=StudentStatus.ALUMNI).count(),
            'average_gpa': Student.objects.filter(
                status=StudentStatus.ACTIVE,
                current_gpa__isnull=False
            ).aggregate(avg_gpa=Avg('current_gpa'))['avg_gpa'],
            'recent_admissions': Student.objects.filter(
                admission_date__gte=timezone.now().replace(day=1)
            ).count(),
        }
        
        # Count by status
        status_counts = Student.objects.values('status').annotate(
            count=Count('id')
        )
        for item in status_counts:
            stats['by_status'][item['status']] = item['count']
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def admit(self, request, pk=None):
        """
        Admit a student (applicant -> active)
        POST /api/v1/students/{id}/admit/
        
        Body: {
            "admission_date": "2024-01-15T10:00:00Z"  // optional
        }
        """
        student = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'student': student})
        serializer.is_valid(raise_exception=True)
        
        try:
            admission_date = serializer.validated_data.get('admission_date')
            student.admit(admission_date=admission_date)
            
            return Response({
                'message': 'Student admitted successfully',
                'student': StudentDetailSerializer(student).data
            })
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def graduate(self, request, pk=None):
        """
        Graduate a student (active -> graduated)
        POST /api/v1/students/{id}/graduate/
        
        Body: {
            "graduation_date": "2024-05-15T10:00:00Z",  // optional
            "degree_earned": "Bachelor of Science",
            "honors": "Cum Laude"  // optional
        }
        """
        student = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'student': student})
        serializer.is_valid(raise_exception=True)
        
        try:
            student.graduate(
                graduation_date=serializer.validated_data.get('graduation_date'),
                degree_earned=serializer.validated_data.get('degree_earned'),
                honors=serializer.validated_data.get('honors')
            )
            
            return Response({
                'message': 'Student graduated successfully',
                'student': StudentDetailSerializer(student).data
            })
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """
        Change student status (suspend, withdraw, make_alumni)
        POST /api/v1/students/{id}/change_status/
        
        Body: {
            "action": "suspend|withdraw|make_alumni",
            "reason": "Optional reason"
        }
        """
        student = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'student': student})
        serializer.is_valid(raise_exception=True)
        
        action_name = serializer.validated_data['action']
        
        try:
            if action_name == 'suspend':
                student.suspend()
                message = 'Student suspended successfully'
            elif action_name == 'withdraw':
                student.withdraw()
                message = 'Student withdrawn successfully'
            elif action_name == 'make_alumni':
                student.make_alumni()
                message = 'Student status changed to alumni'
            
            return Response({
                'message': message,
                'student': StudentDetailSerializer(student).data
            })
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Get all active students
        GET /api/v1/students/active/
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(status=StudentStatus.ACTIVE)
        )
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def applicants(self, request):
        """
        Get all applicants
        GET /api/v1/students/applicants/
        """
        queryset = self.filter_queryset(
            self.get_queryset().filter(status=StudentStatus.APPLICANT)
        )
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """
        Bulk upload students from CSV/Excel
        POST /api/v1/students/bulk_upload/
        
        Upload a CSV or Excel file with student data
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        file = serializer.validated_data['file']
        
        # TODO: Implement bulk upload logic
        # This would parse the file and create multiple students
        
        return Response({
            'message': 'Bulk upload feature coming soon',
            'file_name': file.name
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
    
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        Get detailed student profile with related data
        GET /api/v1/students/{id}/profile/
        """
        student = self.get_object()
        serializer = StudentDetailSerializer(student)
        
        # TODO: Add related data (courses, grades, attendance, etc.)
        data = serializer.data
        data['enrollments'] = []  # Placeholder for enrollments
        data['grades'] = []  # Placeholder for grades
        
        return Response(data)
