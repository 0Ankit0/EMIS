"""
Reports Filters
"""
import django_filters
from .models import ReportTemplate, GeneratedReport, ScheduledReport


class ReportTemplateFilter(django_filters.FilterSet):
    """Filter for ReportTemplate"""
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = ReportTemplate
        fields = ['name', 'description', 'category', 'is_active', 'default_format', 'created_at']


class GeneratedReportFilter(django_filters.FilterSet):
    """Filter for GeneratedReport"""
    title = django_filters.CharFilter(lookup_expr='icontains')
    generated_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = GeneratedReport
        fields = ['title', 'template', 'format', 'status', 'generated_by', 'generated_at']


class ScheduledReportFilter(django_filters.FilterSet):
    """Filter for ScheduledReport"""
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = ScheduledReport
        fields = ['name', 'template', 'schedule_type', 'is_active']
