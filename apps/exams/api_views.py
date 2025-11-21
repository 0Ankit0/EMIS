"""
Exams API Views
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from django.utils import timezone

from .models import Exam, ExamResult, ExamSchedule
from .serializers import (
    ExamSerializer, ExamListSerializer,
    ExamResultSerializer, ExamResultListSerializer,
    ExamScheduleSerializer
)
from .filters import ExamFilter, ExamResultFilter, ExamScheduleFilter
from .permissions import CanManageExams, CanViewResults, CanEnterResults


class ExamViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Exam model
    """
    queryset = Exam.objects.select_related('course', 'invigilator').all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExamFilter
    search_fields = ['exam_code', 'exam_name', 'course__course_name']
    ordering_fields = ['exam_date', 'created_at', 'exam_code']
    ordering = ['-exam_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ExamListSerializer
        return ExamSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start an exam"""
        exam = self.get_object()
        exam.start_exam()
        return Response({'status': 'Exam started'})
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Complete an exam"""
        exam = self.get_object()
        exam.complete_exam()
        return Response({'status': 'Exam completed'})
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for an exam"""
        exam = self.get_object()
        results = exam.results.all()
        
        stats = {
            'total_students': results.count(),
            'passed': results.filter(is_passed=True).count(),
            'failed': results.filter(is_passed=False, is_absent=False).count(),
            'absent': results.filter(is_absent=True).count(),
            'pass_percentage': exam.get_pass_percentage(),
            'average_marks': results.filter(is_absent=False).aggregate(
                avg=Avg('marks_obtained')
            )['avg'] or 0,
            'grade_distribution': dict(
                results.values('grade').annotate(count=Count('grade')).values_list('grade', 'count')
            )
        }
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming exams"""
        exams = self.queryset.filter(status='scheduled').order_by('exam_date', 'start_time')[:10]
        serializer = ExamListSerializer(exams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def publish_results(self, request, pk=None):
        """Publish exam results"""
        exam = self.get_object()
        exam.is_published = True
        exam.save()
        return Response({'status': 'Results published'})


class ExamResultViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for ExamResult model
    """
    queryset = ExamResult.objects.select_related('exam', 'student').all()
    serializer_class = ExamResultSerializer
    permission_classes = [IsAuthenticated, CanViewResults]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExamResultFilter
    search_fields = ['student__first_name', 'student__last_name', 'student__roll_number', 'exam__exam_code']
    ordering_fields = ['marks_obtained', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ExamResultListSerializer
        return ExamResultSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Students can only see their own results
        if hasattr(self.request.user, 'student'):
            queryset = queryset.filter(student=self.request.user.student)
        
        # Filter by exam if provided
        exam_id = self.request.query_params.get('exam', None)
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        
        return queryset
    
    def perform_create(self, serializer):
        evaluated_by = None
        if hasattr(self.request.user, 'faculty'):
            evaluated_by = self.request.user.faculty
        
        serializer.save(
            evaluated_by=evaluated_by,
            evaluated_at=timezone.now()
        )
    
    @action(detail=False, methods=['get'])
    def my_results(self, request):
        """Get current user's exam results"""
        if not hasattr(request.user, 'student'):
            return Response(
                {'error': 'User is not a student'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = self.queryset.filter(student=request.user.student)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def grade_distribution(self, request):
        """Get grade distribution"""
        exam_id = request.query_params.get('exam', None)
        queryset = self.queryset
        
        if exam_id:
            queryset = queryset.filter(exam_id=exam_id)
        
        distribution = queryset.values('grade').annotate(
            count=Count('grade')
        ).order_by('grade')
        
        return Response(distribution)


class ExamScheduleViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for ExamSchedule model
    """
    queryset = ExamSchedule.objects.all()
    serializer_class = ExamScheduleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExamScheduleFilter
    search_fields = ['name', 'academic_year']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def exams(self, request, pk=None):
        """Get all exams in this schedule"""
        schedule = self.get_object()
        exams = Exam.objects.filter(
            exam_date__gte=schedule.start_date,
            exam_date__lte=schedule.end_date,
            academic_year=schedule.academic_year,
            semester=schedule.semester
        ).order_by('exam_date', 'start_time')
        
        serializer = ExamListSerializer(exams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publish the schedule"""
        schedule = self.get_object()
        schedule.is_published = True
        schedule.save()
        return Response({'status': 'Schedule published'})
    
    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        """Unpublish the schedule"""
        schedule = self.get_object()
        schedule.is_published = False
        schedule.save()
        return Response({'status': 'Schedule unpublished'})
