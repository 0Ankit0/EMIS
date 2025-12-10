"""
Attendance Models
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.core.models import TimeStampedModel

User = get_user_model()


class AttendanceRecord(TimeStampedModel):
    """
    Individual attendance record for a student in a session
    """
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
        ('sick_leave', 'Sick Leave'),
        ('authorized_absence', 'Authorized Absence'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    session = models.ForeignKey(
        'AttendanceSession',
        on_delete=models.CASCADE,
        related_name='records',
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='attendance_records',
        null=True,
        blank=True
    )
    date = models.DateField(db_index=True)
    
    # Status and timing
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='present',
        db_index=True
    )
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    
    # Additional details
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendances'
    )
    marked_at = models.DateTimeField(auto_now_add=True)
    
    # Leave documentation
    leave_document = models.FileField(
        upload_to='attendance/leave_docs/%Y/%m/',
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'attendance_records'
        unique_together = ['student', 'course', 'date']
        ordering = ['-date', 'student']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['student', 'date']),
            models.Index(fields=['course', 'date']),
            models.Index(fields=['status', 'date']),
        ]
    
    def __str__(self):
        return f"{self.student} - {self.course} - {self.date} ({self.status})"
    
    def is_present(self):
        return self.status == 'present'
    
    def is_late(self):
        return self.status == 'late'
    
    def is_absent(self):
        return self.status in ['absent', 'sick_leave']


class AttendanceSession(TimeStampedModel):
    """
    Attendance session for a specific class/course
    """
    SESSION_TYPE_CHOICES = [
        ('lecture', 'Lecture'),
        ('lab', 'Laboratory'),
        ('tutorial', 'Tutorial'),
        ('seminar', 'Seminar'),
        ('exam', 'Examination'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='attendance_sessions'
    )
    title = models.CharField(max_length=255)
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        default='lecture'
    )
    
    # Scheduling
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        db_index=True
    )
    
    # Faculty
    instructor = models.ForeignKey(
        'faculty.Faculty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_sessions'
    )
    
    # Location
    room = models.CharField(max_length=100, blank=True)
    building = models.CharField(max_length=100, blank=True)
    
    # Attendance tracking
    total_students = models.IntegerField(default=0)
    present_count = models.IntegerField(default=0)
    absent_count = models.IntegerField(default=0)
    late_count = models.IntegerField(default=0)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'attendance_sessions'
        ordering = ['-date', '-start_time']
        verbose_name = 'Attendance Session'
        verbose_name_plural = 'Attendance Sessions'
        indexes = [
            models.Index(fields=['course', 'date']),
            models.Index(fields=['date', 'status']),
        ]
    
    def __str__(self):
        return f"{self.course} - {self.title} ({self.date})"
    
    def update_counts(self):
        """Update attendance counts"""
        records = self.records.all()
        self.total_students = records.count()
        self.present_count = records.filter(status='present').count()
        self.absent_count = records.filter(status__in=['absent', 'sick_leave']).count()
        self.late_count = records.filter(status='late').count()
        self.save(update_fields=['total_students', 'present_count', 'absent_count', 'late_count'])
    
    def get_attendance_rate(self):
        """Calculate attendance rate"""
        if self.total_students == 0:
            return 0
        return round((self.present_count / self.total_students) * 100, 2)


class AttendancePolicy(TimeStampedModel):
    """
    Attendance policy for courses/programs
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    # Policy parameters
    minimum_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Minimum attendance percentage required"
    )
    grace_period_days = models.IntegerField(
        default=0,
        help_text="Grace period for late marks"
    )
    
    # Penalties
    warning_threshold = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Threshold for attendance warning"
    )
    penalty_threshold = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Threshold for penalties"
    )
    
    # Application
    applies_to_program = models.CharField(max_length=100, blank=True)
    applies_to_year = models.IntegerField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'attendance_policies'
        ordering = ['name']
        verbose_name = 'Attendance Policy'
        verbose_name_plural = 'Attendance Policies'
    
    def __str__(self):
        return f"{self.name} ({self.minimum_percentage}%)"


class AttendanceReport(TimeStampedModel):
    """
    Generated attendance reports
    """
    REPORT_TYPE_CHOICES = [
        ('student', 'Student Report'),
        ('course', 'Course Report'),
        ('program', 'Program Report'),
        ('daily', 'Daily Report'),
        ('monthly', 'Monthly Report'),
        ('custom', 'Custom Report'),
    ]
    
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
        ('excel', 'Excel'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    
    # Date range
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Filters
    filters = models.JSONField(default=dict, help_text="Report filter parameters")
    
    # Generated data
    report_data = models.JSONField(default=dict)
    file_path = models.FileField(upload_to='reports/attendance/%Y/%m/', null=True, blank=True)
    
    # Metadata
    generated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendance_reports'
    )
    
    class Meta:
        db_table = 'attendance_reports'
        ordering = ['-created_at']
        verbose_name = 'Attendance Report'
        verbose_name_plural = 'Attendance Reports'
    
    def __str__(self):
        return f"{self.title} ({self.start_date} to {self.end_date})"

