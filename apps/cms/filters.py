"""
Cms Filters
"""
import django_filters
from .models import CmsItem


class CmsItemFilter(django_filters.FilterSet):
    """
    Filter for CmsItem
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = CmsItem
        fields = ['name', 'description', 'status', 'created_at']
