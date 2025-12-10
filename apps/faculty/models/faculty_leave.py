from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from .faculty import Faculty

User = get_user_model()

class FacultyLeave(TimeStampedModel):
    """Leave Applications for Faculty"""
    class LeaveType(models.TextChoices):
        CASUAL = 'casual', 'Casual Leave'
        SICK = 'sick', 'Sick Leave'
        EARNED = 'earned', 'Earned Leave'
        MATERNITY = 'maternity', 'Maternity Leave'
        PATERNITY = 'paternity', 'Paternity Leave'
        COMPENSATORY = 'compensatory', 'Compensatory Off'
        UNPAID = 'unpaid', 'Unpaid Leave'
        OTHER = 'other', 'Other'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='leave_applications')
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_days = models.IntegerField(validators=[MinValueValidator(1)])
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_faculty_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    supporting_document = models.FileField(upload_to='faculty/leave_documents/%Y/%m/', blank=True, null=True)
    
    class Meta:
        db_table = 'faculty_leaves'
        ordering = ['-start_date']
        verbose_name = 'Faculty Leave'
        verbose_name_plural = 'Faculty Leaves'
        indexes = [
            models.Index(fields=['faculty', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.leave_type} ({self.start_date} to {self.end_date})"
    
    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            delta = self.end_date - self.start_date
            self.number_of_days = delta.days + 1
        super().save(*args, **kwargs)

