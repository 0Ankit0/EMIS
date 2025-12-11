from django.db import models
from apps.core.models import TimeStampedModel
from .lesson import Lesson

class Quiz(TimeStampedModel):
    """Quiz/Assessment"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=60, validators=[models.Min(0), models.Max(100)])
    max_attempts = models.IntegerField(default=3, validators=[models.Min(1)])
    time_limit_minutes = models.IntegerField(null=True, blank=True, validators=[models.Min(1)])
    is_mandatory = models.BooleanField(default=False)
    show_correct_answers = models.BooleanField(default=True)
    randomize_questions = models.BooleanField(default=False)
    class Meta:
        db_table = 'lms_quizzes'
        ordering = ['lesson']
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quizzes'
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"
