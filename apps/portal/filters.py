import django_filters
from .models import (
    Dashboard, Announcement, PortalActivity
)


class DashboardFilter(django_filters.FilterSet):
    role = django_filters.ChoiceFilter(choices=Dashboard.ROLE_CHOICES)
    is_active = django_filters.BooleanFilter()
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Dashboard
        fields = ['role', 'is_active']


class AnnouncementFilter(django_filters.FilterSet):
    priority = django_filters.ChoiceFilter(choices=Announcement.PRIORITY_CHOICES)
    is_published = django_filters.BooleanFilter()
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Announcement
        fields = ['priority', 'is_published', 'author']


class PortalActivityFilter(django_filters.FilterSet):
    activity_type = django_filters.ChoiceFilter(choices=PortalActivity.ACTIVITY_TYPE_CHOICES)
    date_from = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = PortalActivity
        fields = ['user', 'activity_type']
