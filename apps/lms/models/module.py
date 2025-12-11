from django.db import models
from apps.core.models import TimeStampedModel
from .course import Course

class Module(TimeStampedModel):
    """Course Module/Section"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    class Meta:
        db_table = 'lms_modules'
        ordering = ['course', 'order']
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
    def __str__(self):
        return f"{self.course.code} - {self.title}"
