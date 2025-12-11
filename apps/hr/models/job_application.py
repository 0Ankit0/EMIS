"""HR Job Application Model"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .job_posting import JobPosting

User = get_user_model()


class JobApplication(TimeStampedModel):
    """Job Application from Candidates"""
    
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        SCREENING = 'screening', 'Under Screening'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        INTERVIEW_SCHEDULED = 'interview_scheduled', 'Interview Scheduled'
        SELECTED = 'selected', 'Selected'
        REJECTED = 'rejected', 'Rejected'
        OFFER_SENT = 'offer_sent', 'Offer Sent'
        OFFER_ACCEPTED = 'offer_accepted', 'Offer Accepted'
        OFFER_DECLINED = 'offer_declined', 'Offer Declined'
        JOINED = 'joined', 'Joined'
    
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    
    # Candidate Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    current_location = models.CharField(max_length=200)
    
    total_experience_years = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0)])
    current_company = models.CharField(max_length=200, blank=True)
    current_designation = models.CharField(max_length=200, blank=True)
    current_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    notice_period_days = models.IntegerField(null=True, blank=True)
    
    resume = models.FileField(upload_to='hr/applications/resumes/%Y/%m/')
    cover_letter = models.TextField(blank=True)
    
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SUBMITTED, db_index=True)
    
    application_date = models.DateTimeField(default=timezone.now)
    
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='hr_reviewed_applications')
    review_notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hr_job_applications'
        ordering = ['-application_date']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        indexes = [
            models.Index(fields=['job_posting', 'status']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_posting.title}"
