import uuid
from django.db import models
from apps.core.models import TimeStampedModel

class AttendancePolicy(TimeStampedModel):
    """
    Attendance policy for courses/programs
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    minimum_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Minimum attendance percentage required"
    )
    grace_period_days = models.IntegerField(
        default=0,
        help_text="Grace period for late marks"
    )
    warning_threshold = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Threshold for attendance warning"
    )
    penalty_threshold = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Threshold for penalties"
    )
    applies_to_program = models.CharField(max_length=100, blank=True)
    applies_to_year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'attendance_policies'
        ordering = ['name']
        verbose_name = 'Attendance Policy'
        verbose_name_plural = 'Attendance Policies'
    def __str__(self):
        return f"{self.name} ({self.minimum_percentage}%)"
