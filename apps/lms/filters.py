"""
LMS Filters
"""
import django_filters
from .models import Course, Enrollment, Module, Lesson, Quiz, Assignment


class CourseFilter(django_filters.FilterSet):
    """Filter for Course"""
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Course
        fields = ['title', 'category', 'status', 'difficulty_level', 'is_free', 'instructor']


class EnrollmentFilter(django_filters.FilterSet):
    """Filter for Enrollment"""
    enrollment_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Enrollment
        fields = ['status', 'payment_status', 'course', 'student']


class ModuleFilter(django_filters.FilterSet):
    """Filter for Module"""
    
    class Meta:
        model = Module
        fields = ['course', 'is_published']


class LessonFilter(django_filters.FilterSet):
    """Filter for Lesson"""
    
    class Meta:
        model = Lesson
        fields = ['module', 'content_type', 'is_published', 'is_preview']
