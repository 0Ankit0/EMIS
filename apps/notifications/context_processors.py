"""
Notifications Context Processors
"""
from .models import Notification


def notification_count(request):
    """
    Add unread notification count to template context
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.for_user(request.user).unread().count()
        recent_notifications = Notification.objects.for_user(request.user)[:5]
    else:
        unread_count = 0
        recent_notifications = []
    
    return {
        'unread_notification_count': unread_count,
        'recent_notifications': recent_notifications,
    }
