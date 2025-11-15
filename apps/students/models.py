"""
Student models for EMIS
"""
from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel, AuditModel
import uuid


class StudentStatus(models.TextChoices):
    """Student status choices"""
    APPLICANT = 'applicant', 'Applicant'
    ACTIVE = 'active', 'Active'
    SUSPENDED = 'suspended', 'Suspended'
    WITHDRAWN = 'withdrawn', 'Withdrawn'
    GRADUATED = 'graduated', 'Graduated'
    ALUMNI = 'alumni', 'Alumni'


class Gender(models.TextChoices):
    """Gender choices"""
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'
    OTHER = 'other', 'Other'
    PREFER_NOT_TO_SAY = 'prefer_not_to_say', 'Prefer not to say'


class Student(AuditModel):
    """
    Student model representing a student in the system.
    Tracks from application through graduation to alumni.
    """
    # Unique identifier
    student_number = models.CharField(
        max_length=50, 
        unique=True, 
        db_index=True,
        help_text="Unique student identification number"
    )
    
    # Personal information
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=30, 
        choices=Gender.choices, 
        blank=True, 
        null=True
    )
    nationality = models.CharField(max_length=100, blank=True, null=True)
    
    # Address
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Emergency contact
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)
    
    # Academic info
    status = models.CharField(
        max_length=20,
        choices=StudentStatus.choices,
        default=StudentStatus.APPLICANT,
        db_index=True
    )
    admission_date = models.DateTimeField(blank=True, null=True)
    graduation_date = models.DateTimeField(blank=True, null=True)
    degree_earned = models.CharField(max_length=200, blank=True, null=True)
    honors = models.CharField(max_length=100, blank=True, null=True)
    
    # GPA tracking
    current_gpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Current cumulative GPA"
    )
    
    # User account reference (one student = one user account)
    user = models.OneToOneField(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_profile'
    )
    
    class Meta:
        db_table = 'students'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student_number']),
            models.Index(fields=['email']),
            models.Index(fields=['status']),
            models.Index(fields=['last_name', 'first_name']),
        ]
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.student_number} - {self.get_full_name()}"
    
    def get_full_name(self):
        """Return full name"""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return ' '.join(parts)
    
    @property
    def full_name(self):
        """Full name property"""
        return self.get_full_name()
    
    @property
    def is_active(self):
        """Check if student is currently active"""
        return self.status == StudentStatus.ACTIVE
    
    @property
    def is_graduated(self):
        """Check if student has graduated"""
        return self.status == StudentStatus.GRADUATED
    
    @property
    def age(self):
        """Calculate student's current age"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    def admit(self, admission_date=None):
        """
        Admit student (change status from applicant to active)
        """
        if self.status != StudentStatus.APPLICANT:
            raise ValueError("Only applicants can be admitted")
        
        self.status = StudentStatus.ACTIVE
        self.admission_date = admission_date or timezone.now()
        self.save(update_fields=['status', 'admission_date', 'updated_at'])
    
    def suspend(self):
        """Suspend student"""
        if self.status != StudentStatus.ACTIVE:
            raise ValueError("Only active students can be suspended")
        
        self.status = StudentStatus.SUSPENDED
        self.save(update_fields=['status', 'updated_at'])
    
    def withdraw(self):
        """Withdraw student"""
        if self.status not in [StudentStatus.ACTIVE, StudentStatus.SUSPENDED]:
            raise ValueError("Only active or suspended students can be withdrawn")
        
        self.status = StudentStatus.WITHDRAWN
        self.save(update_fields=['status', 'updated_at'])
    
    def graduate(self, graduation_date=None, degree_earned=None, honors=None):
        """Graduate student"""
        if self.status != StudentStatus.ACTIVE:
            raise ValueError("Only active students can graduate")
        
        self.status = StudentStatus.GRADUATED
        self.graduation_date = graduation_date or timezone.now()
        if degree_earned:
            self.degree_earned = degree_earned
        if honors:
            self.honors = honors
        self.save(update_fields=['status', 'graduation_date', 'degree_earned', 'honors', 'updated_at'])
    
    def make_alumni(self):
        """Convert graduated student to alumni status"""
        if self.status != StudentStatus.GRADUATED:
            raise ValueError("Only graduated students can become alumni")
        
        self.status = StudentStatus.ALUMNI
        self.save(update_fields=['status', 'updated_at'])
    
    def generate_student_number(self):
        """
        Generate unique student number
        Format: STU-YYYY-XXXXX
        """
        from datetime import date
        year = date.today().year
        
        # Get count of students created this year
        count = Student.objects.filter(
            created_at__year=year
        ).count() + 1
        
        return f"STU-{year}-{count:05d}"
    
    def save(self, *args, **kwargs):
        """Override save to generate student number if not set"""
        if not self.student_number:
            self.student_number = self.generate_student_number()
        super().save(*args, **kwargs)
