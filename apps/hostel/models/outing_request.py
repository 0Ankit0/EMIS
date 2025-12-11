from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from ..managers import OutingRequestManager

User = get_user_model()

class OutingRequest(TimeStampedModel):
    """Student Outing/Leave Request"""
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        RETURNED = 'returned', 'Returned'
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='outing_requests')
    hostel = models.ForeignKey('hostel.Hostel', on_delete=models.CASCADE, related_name='outing_requests')
    out_date = models.DateField()
    out_time = models.TimeField()
    expected_return_date = models.DateField()
    expected_return_time = models.TimeField()
    actual_return_date = models.DateField(null=True, blank=True)
    actual_return_time = models.TimeField(null=True, blank=True)
    destination = models.CharField(max_length=200)
    purpose = models.TextField()
    parent_contact = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_outings')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_outing_requests'
        ordering = ['-created_at']
        verbose_name = 'Outing Request'
        verbose_name_plural = 'Outing Requests'
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['hostel', 'out_date']),
        ]
    def __str__(self):
        return f"{self.student.user.email} - {self.out_date}"
