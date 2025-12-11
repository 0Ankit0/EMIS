from django.db import models
from apps.core.models import TimeStampedModel
from .enrollment import Enrollment
from .lesson import Lesson

class LessonProgress(TimeStampedModel):
    """Track student progress on lessons"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    time_spent_minutes = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    class Meta:
        db_table = 'lms_lesson_progress'
        unique_together = ['enrollment', 'lesson']
        ordering = ['enrollment', 'lesson']
    def __str__(self):
        return f"{self.enrollment.student.user.email} - {self.lesson.title}"
