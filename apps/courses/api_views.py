"""Courses API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, Module, Assignment, Submission, GradeRecord
from .serializers import (
    CourseCreateSerializer, CourseUpdateSerializer, CourseResponseSerializer,
    ModuleCreateSerializer, ModuleResponseSerializer,
    AssignmentCreateSerializer, AssignmentResponseSerializer,
    SubmissionCreateSerializer, SubmissionResponseSerializer,
    GradeRecordCreateSerializer, GradeRecordResponseSerializer
)


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Courses"""
    queryset = Course.objects.all()
    serializer_class = CourseResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'code', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CourseCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return CourseUpdateSerializer
        return CourseResponseSerializer
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        """Get modules for a course"""
        course = self.get_object()
        modules = Module.objects.filter(course=course)
        serializer = ModuleResponseSerializer(modules, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get assignments for a course"""
        course = self.get_object()
        assignments = Assignment.objects.filter(course=course)
        serializer = AssignmentResponseSerializer(assignments, many=True)
        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    """ViewSet for Modules"""
    queryset = Module.objects.all()
    serializer_class = ModuleResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ModuleCreateSerializer
        return ModuleResponseSerializer


class AssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Assignments"""
    queryset = Assignment.objects.all()
    serializer_class = AssignmentResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course', 'module']
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    ordering = ['-due_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AssignmentCreateSerializer
        return AssignmentResponseSerializer
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get submissions for an assignment"""
        assignment = self.get_object()
        submissions = Submission.objects.filter(assignment=assignment)
        serializer = SubmissionResponseSerializer(submissions, many=True)
        return Response(serializer.data)


class SubmissionViewSet(viewsets.ModelViewSet):
    """ViewSet for Submissions"""
    queryset = Submission.objects.all()
    serializer_class = SubmissionResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['assignment', 'student', 'status']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    ordering_fields = ['submitted_at', 'created_at']
    ordering = ['-submitted_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SubmissionCreateSerializer
        return SubmissionResponseSerializer
    
    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        """Grade a submission"""
        submission = self.get_object()
        score = request.data.get('score')
        feedback = request.data.get('feedback', '')
        
        if score is None:
            return Response({'error': 'score required'}, status=status.HTTP_400_BAD_REQUEST)
        
        submission.score = score
        submission.feedback = feedback
        submission.status = 'graded'
        submission.save()
        
        return Response({'message': 'Submission graded successfully'})


class GradeRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for Grade Records"""
    queryset = GradeRecord.objects.all()
    serializer_class = GradeRecordResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'course']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return GradeRecordCreateSerializer
        return GradeRecordResponseSerializer
