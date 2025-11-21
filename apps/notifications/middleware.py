"""
Notifications Middleware
"""
from django.utils.deprecation import MiddlewareMixin
from .models import Notification


class NotificationMiddleware(MiddlewareMixin):
    """
    Middleware to attach unread notification count to request
    """
    
    def process_request(self, request):
        if request.user.is_authenticated:
            request.unread_notifications_count = (
                Notification.objects.for_user(request.user).unread().count()
            )
        else:
            request.unread_notifications_count = 0
