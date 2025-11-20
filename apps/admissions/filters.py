"""
Admissions Filters
"""
import django_filters
from .models import Application, MeritList


class ApplicationFilter(django_filters.FilterSet):
    """
    Filter for Application
    """
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    application_number = django_filters.CharFilter(lookup_expr='icontains')
    program = django_filters.CharFilter(lookup_expr='icontains')
    submitted_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Application
        fields = ['first_name', 'last_name', 'email', 'application_number', 'status', 'program', 'admission_year', 'admission_semester', 'submitted_at']
