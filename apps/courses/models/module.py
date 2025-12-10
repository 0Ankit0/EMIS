from django.db import models
from apps.core.models import TimeStampedModel


class Module(TimeStampedModel):
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='modules'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sequence_order = models.IntegerField(default=0)
    
    # Content can be rich text, URLs, or references to external materials
    content = models.TextField(blank=True)
    content_type = models.CharField(
        max_length=50,
        choices=[
            ('text', 'Text'),
            ('video', 'Video'),
            ('document', 'Document'),
            ('link', 'External Link'),
            ('mixed', 'Mixed Content'),
        ],
        default='text'
    )
    
    # Optional: Duration in minutes
    duration_minutes = models.IntegerField(null=True, blank=True)
    
    # Visibility control
    is_published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'course_modules'
        ordering = ['course', 'sequence_order']
        unique_together = (('course', 'sequence_order'),)
        indexes = [
            models.Index(fields=['course', 'sequence_order']),
        ]

    def __str__(self):
        return f"{self.course.code} - Module {self.sequence_order}: {self.title}"
