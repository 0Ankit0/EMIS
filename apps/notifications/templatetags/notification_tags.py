"""
Template tags for notifications
"""
from django import template
from apps.notifications.models import Notification

register = template.Library()


@register.simple_tag
def unread_notification_count(user):
    """
    Get unread notification count for user
    Usage: {% unread_notification_count user %}
    """
    if user.is_authenticated:
        return Notification.objects.for_user(user).unread().count()
    return 0


@register.simple_tag
def recent_notifications(user, limit=5):
    """
    Get recent notifications for user
    Usage: {% recent_notifications user 10 %}
    """
    if user.is_authenticated:
        return Notification.objects.for_user(user)[:limit]
    return []


@register.filter
def notification_icon(notification_type):
    """
    Get icon class for notification type
    Usage: {{ notification.notification_type|notification_icon }}
    """
    icons = {
        'info': 'fas fa-info-circle text-blue-500',
        'success': 'fas fa-check-circle text-green-500',
        'warning': 'fas fa-exclamation-triangle text-yellow-500',
        'error': 'fas fa-times-circle text-red-500',
        'announcement': 'fas fa-bullhorn text-purple-500',
        'reminder': 'fas fa-bell text-orange-500',
    }
    return icons.get(notification_type, 'fas fa-info-circle')


@register.filter
def notification_color(notification_type):
    """
    Get color class for notification type
    Usage: {{ notification.notification_type|notification_color }}
    """
    colors = {
        'info': 'bg-blue-100 border-blue-500',
        'success': 'bg-green-100 border-green-500',
        'warning': 'bg-yellow-100 border-yellow-500',
        'error': 'bg-red-100 border-red-500',
        'announcement': 'bg-purple-100 border-purple-500',
        'reminder': 'bg-orange-100 border-orange-500',
    }
    return colors.get(notification_type, 'bg-gray-100 border-gray-500')


@register.inclusion_tag('notifications/includes/notification_badge.html')
def notification_badge(user):
    """
    Display notification badge with count
    Usage: {% notification_badge user %}
    """
    if user.is_authenticated:
        count = Notification.objects.for_user(user).unread().count()
    else:
        count = 0
    
    return {'count': count}


@register.inclusion_tag('notifications/includes/notification_list.html')
def notification_dropdown(user, limit=5):
    """
    Display notification dropdown
    Usage: {% notification_dropdown user %}
    """
    if user.is_authenticated:
        notifications = Notification.objects.for_user(user)[:limit]
        unread_count = Notification.objects.for_user(user).unread().count()
    else:
        notifications = []
        unread_count = 0
    
    return {
        'notifications': notifications,
        'unread_count': unread_count,
        'user': user
    }


@register.filter
def time_ago(notification):
    """
    Get human-readable time since notification was created
    Usage: {{ notification|time_ago }}
    """
    from django.utils.timesince import timesince
    return timesince(notification.created_at)
