from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .assignment import Assignment
from .enrollment import Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()

class AssignmentSubmission(TimeStampedModel):
    """Student Assignment Submission"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('graded', 'Graded'),
        ('returned', 'Returned'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='assignment_submissions')
    submission_date = models.DateTimeField(default=timezone.now)
    is_late = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='lms/assignment_submissions/%Y/%m/', blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_assignments')
    graded_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    class Meta:
        db_table = 'lms_assignment_submissions'
        unique_together = ['assignment', 'enrollment']
        ordering = ['-submission_date']
        verbose_name = 'Assignment Submission'
        verbose_name_plural = 'Assignment Submissions'
    def __str__(self):
        return f"{self.enrollment.student.user.email} - {self.assignment.title}"
