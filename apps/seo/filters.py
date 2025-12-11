"""SEO Filters"""
from django_filters import rest_framework as filters
from .models import SEOMetadata, Redirect


class SEOMetadataFilter(filters.FilterSet):
    """Filter for SEO Metadata"""
    meta_title = filters.CharFilter(lookup_expr='icontains')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = SEOMetadata
        fields = ['content_type', 'robots', 'include_in_sitemap', 'meta_title']


class RedirectFilter(filters.FilterSet):
    """Filter for Redirects"""
    old_path = filters.CharFilter(lookup_expr='icontains')
    new_path = filters.CharFilter(lookup_expr='icontains')
    min_hits = filters.NumberFilter(field_name='hit_count', lookup_expr='gte')
    max_hits = filters.NumberFilter(field_name='hit_count', lookup_expr='lte')
    
    class Meta:
        model = Redirect
        fields = ['redirect_type', 'is_active', 'old_path', 'new_path']
