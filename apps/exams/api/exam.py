"""Exam API Views"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from django.utils import timezone

from ..models import Exam
from ..serializers import ExamSerializer, ExamListSerializer
from ..filters import ExamFilter
from ..permissions import CanManageExams

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
