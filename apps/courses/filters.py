"""
Courses Filters
"""
import django_filters
from .models import CoursesItem


class CoursesItemFilter(django_filters.FilterSet):
    """
    Filter for CoursesItem
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = CoursesItem
        fields = ['name', 'description', 'status', 'created_at']
