from django.db import models
from apps.core.models import TimeStampedModel
from .course import Course
from .lesson import Lesson
from django.contrib.auth import get_user_model

User = get_user_model()

class Discussion(TimeStampedModel):
    """Course Discussion Thread"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='discussions')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='discussions')
    title = models.CharField(max_length=300)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lms_discussions')
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    class Meta:
        db_table = 'lms_discussions'
        ordering = ['-is_pinned', '-created_at']
        verbose_name = 'Discussion'
        verbose_name_plural = 'Discussions'
    def __str__(self):
        return f"{self.course.code} - {self.title}"
