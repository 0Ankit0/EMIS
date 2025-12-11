from django.db import models

class NotificationType(models.TextChoices):
    """Notification types"""
    INFO = 'info', 'Information'
    SUCCESS = 'success', 'Success'
    WARNING = 'warning', 'Warning'
    ERROR = 'error', 'Error'
    ANNOUNCEMENT = 'announcement', 'Announcement'
    REMINDER = 'reminder', 'Reminder'
