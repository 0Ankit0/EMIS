"""Student model extending User"""
import uuid
from django.db import models
from apps.authentication.models import User


class Student(User):
    """Student model extending User with student-specific fields"""
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        ON_LEAVE = 'on_leave', 'On Leave'
        GRADUATED = 'graduated', 'Graduated'
        WITHDRAWN = 'withdrawn', 'Withdrawn'
        SUSPENDED = 'suspended', 'Suspended'
        EXPELLED = 'expelled', 'Expelled'
    
    student_id = models.CharField(max_length=20, unique=True, db_index=True, default='')
    admission_year = models.IntegerField(db_index=True, default=2024)
    
    # Academic Information
    program = models.CharField(max_length=100, db_index=True, default='')
    batch = models.CharField(max_length=50, default='')
    section = models.CharField(max_length=10, blank=True, default='')
    
    # Guardian Information
    guardian_name = models.CharField(max_length=200, default='')
    guardian_phone = models.CharField(max_length=20, default='')
    guardian_email = models.EmailField(blank=True, default='')
    guardian_relation = models.CharField(max_length=50, default='')
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, default='')
    emergency_contact_phone = models.CharField(max_length=20, default='')
    
    # Student Status
    student_status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    
    # Application reference
    application = models.OneToOneField('admissions.Application', on_delete=models.SET_NULL, 
                                      null=True, blank=True, related_name='student_record')
    
    class Meta:
        db_table = 'students'
        ordering = ['student_id']
    
    def __str__(self):
        return f"{self.student_id} - {self.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            # Generate student ID: STU-YYYY-XXXXX
            from django.utils import timezone
            year = self.admission_year or timezone.now().year
            count = Student.objects.filter(admission_year=year).count() + 1
            self.student_id = f"STU-{year}-{count:05d}"
        super().save(*args, **kwargs)
