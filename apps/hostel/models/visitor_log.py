from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from django.contrib.auth import get_user_model

User = get_user_model()

class VisitorLog(TimeStampedModel):
    """Visitor Entry/Exit Log"""
    class Purpose(models.TextChoices):
        PARENT = 'parent', 'Parent Visit'
        FRIEND = 'friend', 'Friend Visit'
        RELATIVE = 'relative', 'Relative'
        OFFICIAL = 'official', 'Official'
        DELIVERY = 'delivery', 'Delivery'
        OTHER = 'other', 'Other'
    
    hostel = models.ForeignKey('hostel.Hostel', on_delete=models.CASCADE, related_name='visitor_logs')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='hostel_visitors')
    visitor_name = models.CharField(max_length=200)
    visitor_phone = models.CharField(max_length=20)
    visitor_id_type = models.CharField(max_length=50, help_text="e.g., Aadhar, Driving License")
    visitor_id_number = models.CharField(max_length=50)
    purpose = models.CharField(max_length=20, choices=Purpose.choices)
    purpose_details = models.TextField(blank=True)
    entry_time = models.DateTimeField(default=timezone.now)
    exit_time = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_visitors')
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hostel_visitor_logs'
        ordering = ['-entry_time']
        verbose_name = 'Visitor Log'
        verbose_name_plural = 'Visitor Logs'
        indexes = [
            models.Index(fields=['hostel', 'entry_time']),
            models.Index(fields=['student']),
        ]
    
    def __str__(self):
        return f"{self.visitor_name} visiting {self.student.user.email}"

