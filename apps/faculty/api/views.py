"""
Faculty API Views - RESTful API for Faculty Management
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from django.utils import timezone

from .models import (
    Department, Faculty, FacultyQualification, FacultyExperience,
    FacultyAttendance, FacultyLeave, FacultyPublication, FacultyAward
)
from .serializers import (
    DepartmentSerializer, FacultyListSerializer, FacultyDetailSerializer,
    FacultyCreateUpdateSerializer, FacultyQualificationSerializer,
    FacultyExperienceSerializer, FacultyAttendanceSerializer,
    FacultyLeaveSerializer, FacultyPublicationSerializer, FacultyAwardSerializer
)
from .permissions import IsFacultyOwner, CanFacultyManage
from .filters import FacultyFilter, FacultyLeaveFilter, FacultyAttendanceFilter


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department CRUD operations"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    @action(detail=True, methods=['get'])
    def faculty_members(self, request, pk=None):
        """Get all faculty members of a department"""
        department = self.get_object()
        faculty = department.faculty_members.filter(status='active')
        serializer = FacultyListSerializer(faculty, many=True)
        return Response(serializer.data)


class FacultyViewSet(viewsets.ModelViewSet):
    """ViewSet for Faculty CRUD operations"""
    queryset = Faculty.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FacultyFilter
    search_fields = ['employee_id', 'first_name', 'last_name', 'official_email', 'phone']
    ordering_fields = ['employee_id', 'first_name', 'last_name', 'date_of_joining', 'created_at']
    ordering = ['employee_id']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return FacultyListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FacultyCreateUpdateSerializer
        return FacultyDetailSerializer
    
    def perform_create(self, serializer):
        """Set created_by when creating faculty"""
        serializer.save(created_by=self.request.user)


class FacultyQualificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Faculty Qualifications"""
    queryset = FacultyQualification.objects.all()
    serializer_class = FacultyQualificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['faculty', 'degree', 'is_verified']
    ordering = ['-year_of_passing']


class FacultyExperienceViewSet(viewsets.ModelViewSet):
    """ViewSet for Faculty Experience"""
    queryset = FacultyExperience.objects.all()
    serializer_class = FacultyExperienceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['faculty', 'experience_type', 'is_current']
    ordering = ['-start_date']


class FacultyAttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for Faculty Attendance"""
    queryset = FacultyAttendance.objects.all()
    serializer_class = FacultyAttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FacultyAttendanceFilter
    ordering = ['-date']
    
    def perform_create(self, serializer):
        """Set marked_by when creating attendance"""
        serializer.save(marked_by=self.request.user)


class FacultyLeaveViewSet(viewsets.ModelViewSet):
    """ViewSet for Faculty Leave"""
    queryset = FacultyLeave.objects.all()
    serializer_class = FacultyLeaveSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = FacultyLeaveFilter
    ordering = ['-start_date']


class FacultyPublicationViewSet(viewsets.ModelViewSet):
    """ViewSet for Faculty Publications"""
    queryset = FacultyPublication.objects.all()
    serializer_class = FacultyPublicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['faculty', 'publication_type', 'year', 'is_indexed']
    search_fields = ['title', 'authors', 'journal_or_conference', 'keywords']
    ordering = ['-year', '-created_at']


class FacultyAwardViewSet(viewsets.ModelViewSet):
    """ViewSet for Faculty Awards"""
    queryset = FacultyAward.objects.all()
    serializer_class = FacultyAwardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['faculty', 'category']
    ordering = ['-date_received']
