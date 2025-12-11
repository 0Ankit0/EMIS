from django.db import models
from apps.core.models import TimeStampedModel
from .quiz_attempt import QuizAttempt
from .question import Question

class QuizAnswer(TimeStampedModel):
    """Student Answer to Quiz Question"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(null=True, blank=True)
    points_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    feedback = models.TextField(blank=True)
    class Meta:
        db_table = 'lms_quiz_answers'
        unique_together = ['attempt', 'question']
    def __str__(self):
        return f"{self.attempt} - {self.question}"
