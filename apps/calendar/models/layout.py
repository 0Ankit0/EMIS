from django.db import models
from django.conf import settings
from .base import BaseModel

class CalendarLayout(BaseModel):
    """Model representing a user's calendar layout preference."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='calendar_layouts')
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)
    configuration = models.JSONField(default=dict, help_text="JSON configuration for the layout")

    def save(self, *args, **kwargs):
        if self.active:
            # Deactivate other layouts for this user
            CalendarLayout.objects.filter(user=self.user, active=True).exclude(pk=self.pk).update(active=False)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} ({self.user})"

    class Meta:
        verbose_name = "Calendar Layout"
        verbose_name_plural = "Calendar Layouts"
        ordering = ['-active', 'name']
