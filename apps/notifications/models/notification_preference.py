from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()

class NotificationPreference(TimeStampedModel):
    """
    User notification preferences
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_preference'
    )
    enable_email = models.BooleanField(default=True)
    enable_sms = models.BooleanField(default=False)
    enable_push = models.BooleanField(default=True)
    enable_in_app = models.BooleanField(default=True)
    class Meta:
        db_table = 'notification_preferences'
        verbose_name = 'Notification Preference'
        verbose_name_plural = 'Notification Preferences'
    def __str__(self):
        return f"Preferences for {self.user.get_full_name()}"
