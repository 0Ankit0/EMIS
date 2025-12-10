"""Scholarship and financial aid models"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel


class Scholarship(TimeStampedModel):
    """Scholarship programs"""
    
    TYPE_CHOICES = [
        ('merit', 'Merit Based'),
        ('need', 'Need Based'),
        ('sports', 'Sports'),
        ('minority', 'Minority'),
        ('government', 'Government'),
        ('institutional', 'Institutional'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    
    scholarship_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    eligibility_criteria = models.TextField(help_text="Eligibility requirements")
    
    total_slots = models.IntegerField(validators=[MinValueValidator(1)], help_text="Total number of scholarships available")
    filled_slots = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    valid_from = models.DateField()
    valid_to = models.DateField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    
    application_start_date = models.DateField(null=True, blank=True)
    application_end_date = models.DateField(null=True, blank=True)
    
    attachment = models.FileField(upload_to='finance/scholarships/%Y/', blank=True, null=True)
    
    class Meta:
        db_table = 'finance_scholarships'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def available_slots(self):
        return self.total_slots - self.filled_slots
    
    @property
    def is_open_for_application(self):
        if not self.application_start_date or not self.application_end_date:
            return False
        today = timezone.now().date()
        return self.application_start_date <= today <= self.application_end_date


class ScholarshipApplication(TimeStampedModel):
    """Student scholarship applications"""
    
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('awarded', 'Awarded'),
    ]
    
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='scholarship_applications')
    
    application_date = models.DateTimeField(default=timezone.now)
    
    justification = models.TextField(help_text="Why student deserves this scholarship")
    documents = models.FileField(upload_to='finance/scholarship_applications/%Y/%m/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted', db_index=True)
    
    reviewed_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_scholarship_applications')
    review_date = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True)
    
    awarded_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    award_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'finance_scholarship_applications'
        ordering = ['-application_date']
        unique_together = (('scholarship', 'student'),)
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['scholarship', 'status']),
        ]
    
    def __str__(self):
        return f"{self.student.user.email} - {self.scholarship.name}"
