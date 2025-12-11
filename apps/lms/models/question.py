from django.db import models
from apps.core.models import TimeStampedModel
from .quiz import Quiz

class Question(TimeStampedModel):
    """Quiz Question"""
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
        ('essay', 'Essay'),
    ]
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    points = models.DecimalField(max_digits=5, decimal_places=2, default=1, validators=[models.Min(0)])
    order = models.IntegerField(default=0)
    options = models.JSONField(default=list, blank=True, help_text="List of answer options")
    correct_answer = models.TextField(help_text="Correct answer or answer key")
    explanation = models.TextField(blank=True)
    class Meta:
        db_table = 'lms_questions'
        ordering = ['quiz', 'order']
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"
