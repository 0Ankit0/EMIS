"""
Reports API Filters
"""
import django_filters
from ..models import ReportTemplate, GeneratedReport


class ReportTemplateFilter(django_filters.FilterSet):
    """Filter for ReportTemplate model"""
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = ReportTemplate
        fields = ['name']


class GeneratedReportFilter(django_filters.FilterSet):
    """Filter for GeneratedReport model"""
    template = django_filters.NumberFilter(field_name='template__id')
    
    class Meta:
        model = GeneratedReport
        fields = ['template']


class ScheduledReportFilter(django_filters.FilterSet):
    """Placeholder for ScheduledReport filter"""
    pass
