"""
Notifications Filters
"""
import django_filters
from .models import Notification, NotificationTemplate, ScheduledNotification


class NotificationFilter(django_filters.FilterSet):
    """Filter for Notification"""
    
    title = django_filters.CharFilter(lookup_expr='icontains')
    message = django_filters.CharFilter(lookup_expr='icontains')
    created_at = django_filters.DateFromToRangeFilter()
    is_read = django_filters.BooleanFilter()
    notification_type = django_filters.ChoiceFilter(choices=lambda: Notification._meta.get_field('notification_type').choices)
    
    class Meta:
        model = Notification
        fields = ['title', 'message', 'notification_type', 'is_read', 'created_at']


class NotificationTemplateFilter(django_filters.FilterSet):
    """Filter for NotificationTemplate"""
    
    name = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    notification_type = django_filters.ChoiceFilter(choices=lambda: NotificationTemplate._meta.get_field('notification_type').choices)
    
    class Meta:
        model = NotificationTemplate
        fields = ['name', 'code', 'notification_type', 'is_active']


class ScheduledNotificationFilter(django_filters.FilterSet):
    """Filter for ScheduledNotification"""
    
    title = django_filters.CharFilter(lookup_expr='icontains')
    is_sent = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()
    is_recurring = django_filters.BooleanFilter()
    scheduled_for = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = ScheduledNotification
        fields = ['title', 'is_sent', 'is_active', 'is_recurring', 'scheduled_for']
