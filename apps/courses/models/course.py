from django.db import models
from apps.core.models import TimeStampedModel


class Course(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        ACTIVE = 'active', 'Active'
        ARCHIVED = 'archived', 'Archived'

    title = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    syllabus = models.TextField(blank=True)
    credits = models.IntegerField(default=3)
    
    # Prerequisites stored as array of course IDs
    prerequisites = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of prerequisite course UUIDs"
    )
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses_created'
    )
    
    # Academic details
    department = models.CharField(max_length=100, blank=True)
    semester = models.CharField(max_length=50, blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
            models.Index(fields=['created_by']),
        ]

    def __str__(self):
        return f"{self.code} - {self.title}"

