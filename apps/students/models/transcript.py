from django.db import models
from apps.core.models import TimeStampedModel


class Transcript(TimeStampedModel):
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='transcripts'
    )
    
    # Snapshot of grade records at time of generation
    grade_records_snapshot = models.JSONField(
        default=dict,
        help_text="JSON snapshot of all finalized grade records"
    )
    
    # Academic summary
    total_credits_attempted = models.IntegerField(default=0)
    total_credits_earned = models.IntegerField(default=0)
    cumulative_gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    
    # Generation metadata
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='generated_transcripts'
    )
    
    # Transcript type
    transcript_type = models.CharField(
        max_length=50,
        choices=[
            ('official', 'Official Transcript'),
            ('unofficial', 'Unofficial Transcript'),
            ('interim', 'Interim Transcript'),
        ],
        default='unofficial'
    )
    
    # Time period
    academic_year = models.CharField(max_length=20, blank=True)
    semester = models.CharField(max_length=50, blank=True)
    
    # Validation
    is_certified = models.BooleanField(default=False)
    certification_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'transcripts'
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['transcript_type']),
            models.Index(fields=['generated_at']),
        ]

    def __str__(self):
        return f"Transcript for {self.student.user.email} - {self.generated_at.date()}"
