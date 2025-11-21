"""
Students Filters
"""
import django_filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
    """
    Filter for Student
    """
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    student_id = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'email', 'student_status', 'program', 'admission_year']
