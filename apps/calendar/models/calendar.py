"""Calendar Model"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class Calendar(TimeStampedModel):
    """Calendar to organize events"""
    
    class CalendarType(models.TextChoices):
        PERSONAL = 'personal', 'Personal'
        ACADEMIC = 'academic', 'Academic'
        INSTITUTIONAL = 'institutional', 'Institutional'
        DEPARTMENT = 'department', 'Department'
        SHARED = 'shared', 'Shared'
    
    class Visibility(models.TextChoices):
        PRIVATE = 'private', 'Private'
        PUBLIC = 'public', 'Public'
        RESTRICTED = 'restricted', 'Restricted'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    calendar_type = models.CharField(
        max_length=20,
        choices=CalendarType.choices,
        default=CalendarType.PERSONAL
    )
    
    # Owner and permissions
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_calendars'
    )
    
    # Shared access
    shared_with = models.ManyToManyField(
        User,
        blank=True,
        related_name='shared_calendars',
        help_text="Users who have access to this calendar"
    )
    
    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PRIVATE
    )
    
    # Settings
    time_zone = models.CharField(max_length=50, default='UTC')
    color_code = models.CharField(
        max_length=7,
        default='#4285f4',
        help_text="Default color for calendar"
    )
    
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False, help_text="Default calendar for the owner")
    
    class Meta:
        db_table = 'calendars'
        ordering = ['name']
        verbose_name = 'Calendar'
        verbose_name_plural = 'Calendars'
        unique_together = [['owner', 'name']]
    
    def __str__(self):
        return f"{self.name} ({self.owner.get_full_name()})"
