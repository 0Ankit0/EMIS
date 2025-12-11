from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from .room import Room
from ..managers import ComplaintManager

User = get_user_model()

class Complaint(TimeStampedModel):
    """Hostel Complaints"""
    class Category(models.TextChoices):
        MAINTENANCE = 'maintenance', 'Maintenance'
        ELECTRICITY = 'electricity', 'Electricity'
        WATER = 'water', 'Water Supply'
        CLEANLINESS = 'cleanliness', 'Cleanliness'
        FOOD = 'food', 'Food/Mess'
        SECURITY = 'security', 'Security'
        INTERNET = 'internet', 'Internet/WiFi'
        OTHER = 'other', 'Other'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'
    
    class Status(models.TextChoices):
        SUBMITTED = 'submitted', 'Submitted'
        ACKNOWLEDGED = 'acknowledged', 'Acknowledged'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        CLOSED = 'closed', 'Closed'
        REJECTED = 'rejected', 'Rejected'
    
    hostel = models.ForeignKey('hostel.Hostel', on_delete=models.CASCADE, related_name='complaints')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='hostel_complaints')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    complaint_number = models.CharField(max_length=50, unique=True, db_index=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED, db_index=True)
    submitted_date = models.DateTimeField(default=timezone.now)
    acknowledged_date = models.DateTimeField(null=True, blank=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    resolution = models.TextField(blank=True)
    attachment = models.FileField(upload_to='hostel/complaints/%Y/%m/', blank=True, null=True)
    
    class Meta:
        db_table = 'hostel_complaints'
        ordering = ['-submitted_date']
        verbose_name = 'Complaint'
        verbose_name_plural = 'Complaints'
        indexes = [
            models.Index(fields=['complaint_number']),
            models.Index(fields=['hostel', 'status']),
            models.Index(fields=['student']),
        ]
    
    def __str__(self):
        return f"{self.complaint_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.complaint_number:
            year = timezone.now().year
            from django.db.models import Count
            count = Complaint.objects.filter(created_at__year=year).count() + 1
            self.complaint_number = f"COMP-{year}-{count:06d}"
        super().save(*args, **kwargs)

