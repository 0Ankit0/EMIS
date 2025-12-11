from django.db import models

class NotificationChannel(models.TextChoices):
    """Notification delivery channels"""
    IN_APP = 'in_app', 'In-App'
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PUSH = 'push', 'Push Notification'
