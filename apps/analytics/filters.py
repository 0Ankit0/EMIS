"""
Analytics Filters
"""
import django_filters
from .models import Report, AnalyticsQuery


class ReportFilter(django_filters.FilterSet):
    """
    Filter for Report
    """
    title = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Report
        fields = ['title', 'report_type', 'status', 'format', 'created_at']


class AnalyticsQueryFilter(django_filters.FilterSet):
    """
    Filter for AnalyticsQuery
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    query_type = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = AnalyticsQuery
        fields = ['name', 'query_type', 'is_public', 'is_featured']
