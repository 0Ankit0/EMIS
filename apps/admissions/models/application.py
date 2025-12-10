"""Application model for managing admission applications"""
import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class Application(TimeStampedModel):
    """Model representing an admission application"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SUBMITTED = 'submitted', 'Submitted'
        UNDER_REVIEW = 'under_review', 'Under Review'
        DOCUMENTS_PENDING = 'documents_pending', 'Documents Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        WAITLISTED = 'waitlisted', 'Waitlisted'
        ENROLLED = 'enrolled', 'Enrolled'
        WITHDRAWN = 'withdrawn', 'Withdrawn'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application_number = models.CharField(max_length=20, unique=True, db_index=True)
    
    # Applicant Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20)
    
    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Academic Information
    previous_school = models.CharField(max_length=255)
    previous_grade = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Program Selection
    program = models.CharField(max_length=100, db_index=True)
    admission_year = models.IntegerField(db_index=True)
    admission_semester = models.CharField(max_length=20)
    
    # Application Data
    applicant_data = models.JSONField(default=dict, help_text="Additional applicant information")
    documents = models.JSONField(default=list, help_text="List of submitted documents")
    
    # Status and Review
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    submitted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    reviewed_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, 
                                    null=True, blank=True, related_name='admissions_reviewed_applications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True)
    
    # Merit and Ranking
    merit_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True, db_index=True)
    
    class Meta:
        db_table = 'applications'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['status', 'submitted_at']),
            models.Index(fields=['program', 'admission_year']),
        ]
    
    def __str__(self):
        return f"{self.application_number} - {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            # Generate application number: APP-YYYY-XXXXXX
            from django.utils import timezone
            year = timezone.now().year
            count = Application.objects.filter(admission_year=year).count() + 1
            self.application_number = f"APP-{year}-{count:06d}"
        super().save(*args, **kwargs)
