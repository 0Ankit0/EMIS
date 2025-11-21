"""
Exams Filters
"""
import django_filters
from .models import Exam, ExamResult, ExamSchedule


class ExamFilter(django_filters.FilterSet):
    """
    Filter for Exam
    """
    exam_code = django_filters.CharFilter(lookup_expr='icontains', label='Exam Code')
    exam_name = django_filters.CharFilter(lookup_expr='icontains', label='Exam Name')
    academic_year = django_filters.CharFilter(lookup_expr='exact', label='Academic Year')
    exam_date = django_filters.DateFromToRangeFilter(label='Exam Date Range')
    
    class Meta:
        model = Exam
        fields = ['exam_code', 'exam_name', 'course', 'exam_type', 'status', 'semester', 'academic_year', 'exam_date']


class ExamResultFilter(django_filters.FilterSet):
    """
    Filter for ExamResult
    """
    marks_obtained = django_filters.RangeFilter(label='Marks Range')
    
    class Meta:
        model = ExamResult
        fields = ['exam', 'student', 'grade', 'is_passed', 'is_absent', 'marks_obtained']


class ExamScheduleFilter(django_filters.FilterSet):
    """
    Filter for ExamSchedule
    """
    name = django_filters.CharFilter(lookup_expr='icontains', label='Schedule Name')
    start_date = django_filters.DateFromToRangeFilter(label='Start Date Range')
    
    class Meta:
        model = ExamSchedule
        fields = ['name', 'academic_year', 'semester', 'is_published', 'start_date']
