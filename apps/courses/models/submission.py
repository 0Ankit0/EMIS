from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel


class Submission(TimeStampedModel):
    GRADE_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('graded', 'Graded'),
        ('returned', 'Returned to Student'),
    ]

    assignment = models.ForeignKey(
        'courses.Assignment',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    
    # Submission details
    submitted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    files = models.JSONField(
        default=list,
        blank=True,
        help_text="Array of file paths/URLs for submitted files"
    )
    
    # Grading
    grade_status = models.CharField(
        max_length=20,
        choices=GRADE_STATUS_CHOICES,
        default='pending'
    )
    score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    feedback = models.TextField(blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='graded_submissions'
    )
    
    # Late submission tracking
    is_late = models.BooleanField(default=False)
    late_penalty_applied = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text="Percentage penalty applied"
    )
    
    class Meta:
        db_table = 'submissions'
        ordering = ['-submitted_at']
        unique_together = [['assignment', 'student']]
        indexes = [
            models.Index(fields=['assignment']),
            models.Index(fields=['student']),
            models.Index(fields=['grade_status']),
        ]

    def __str__(self):
        return f"{self.student.user.email} - {self.assignment.title}"
    
    def calculate_late_penalty(self):
        """Calculate if submission is late and apply penalty"""
        if self.submitted_at > self.assignment.due_date:
            self.is_late = True
            days_late = (self.submitted_at - self.assignment.due_date).days + 1
            self.late_penalty_applied = min(
                self.assignment.late_penalty_percentage * days_late,
                100.00
            )
        else:
            self.is_late = False
            self.late_penalty_applied = 0.00
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.calculate_late_penalty()
        super().save(*args, **kwargs)
