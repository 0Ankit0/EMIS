from django.db import models
from apps.core.models import TimeStampedModel
from .lesson import Lesson

class Assignment(TimeStampedModel):
    """Course Assignment"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=300)
    description = models.TextField()
    instructions = models.TextField(blank=True)
    max_points = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    due_date = models.DateTimeField(null=True, blank=True)
    allow_late_submission = models.BooleanField(default=True)
    late_penalty_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    attachment = models.FileField(upload_to='lms/assignment_files/', blank=True, null=True)
    class Meta:
        db_table = 'lms_assignments'
        ordering = ['lesson', '-due_date']
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"
