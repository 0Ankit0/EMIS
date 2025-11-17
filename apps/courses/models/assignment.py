from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel


class Assignment(TimeStampedModel):
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructions = models.TextField(blank=True)
    
    # Grading configuration
    max_score = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    grading_rubric = models.JSONField(default=dict, blank=True)
    
    # Deadlines
    due_date = models.DateTimeField()
    available_from = models.DateTimeField(null=True, blank=True)
    late_submission_allowed = models.BooleanField(default=True)
    late_penalty_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10.00,
        help_text="Percentage penalty per day for late submissions"
    )
    
    # Assignment type
    assignment_type = models.CharField(
        max_length=50,
        choices=[
            ('homework', 'Homework'),
            ('quiz', 'Quiz'),
            ('exam', 'Exam'),
            ('project', 'Project'),
            ('lab', 'Lab Work'),
        ],
        default='homework'
    )
    
    # Visibility
    is_published = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'assignments'
        ordering = ['-due_date']
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.course.code} - {self.title}"
    
    def is_overdue(self):
        return timezone.now() > self.due_date
