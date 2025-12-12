"""
LMS API Filters
"""
import django_filters
from ..models import Course, Module, Lesson, Enrollment


class CourseFilter(django_filters.FilterSet):
    """Filter for Course model"""
    title = django_filters.CharFilter(lookup_expr='icontains')
    instructor = django_filters.NumberFilter(field_name='instructor__id')
    category = django_filters.CharFilter(lookup_expr='icontains')
    level = django_filters.CharFilter(lookup_expr='exact')
    is_published = django_filters.BooleanFilter()
    
    class Meta:
        model = Course
        fields = ['title', 'instructor', 'category', 'level', 'is_published']


class ModuleFilter(django_filters.FilterSet):
    """Filter for Module model"""
    course = django_filters.NumberFilter(field_name='course__id')
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Module
        fields = ['course', 'title']


class LessonFilter(django_filters.FilterSet):
    """Filter for Lesson model"""
    module = django_filters.NumberFilter(field_name='module__id')
    course = django_filters.NumberFilter(field_name='module__course__id')
    title = django_filters.CharFilter(lookup_expr='icontains')
    lesson_type = django_filters.CharFilter(lookup_expr='exact')
    
    class Meta:
        model = Lesson
        fields = ['module', 'course', 'title', 'lesson_type']


class EnrollmentFilter(django_filters.FilterSet):
    """Filter for Enrollment model"""
    student = django_filters.NumberFilter(field_name='student__id')
    course = django_filters.NumberFilter(field_name='course__id')
    status = django_filters.CharFilter(lookup_expr='exact')
    
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'status']
