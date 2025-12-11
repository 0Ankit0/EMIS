from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .quiz import Quiz
from .enrollment import Enrollment

class QuizAttempt(TimeStampedModel):
    """Student Quiz Attempt"""
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='quiz_attempts')
    attempt_number = models.IntegerField(default=1)
    started_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_points = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    passed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    class Meta:
        db_table = 'lms_quiz_attempts'
        ordering = ['-started_at']
        verbose_name = 'Quiz Attempt'
        verbose_name_plural = 'Quiz Attempts'
    def __str__(self):
        return f"{self.enrollment.student.user.email} - {self.quiz.title} (Attempt {self.attempt_number})"
