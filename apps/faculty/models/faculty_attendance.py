from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from .faculty import Faculty

User = get_user_model()

class FacultyAttendance(TimeStampedModel):
    """Daily Attendance for Faculty"""
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        ON_LEAVE = 'on_leave', 'On Leave'
        HALF_DAY = 'half_day', 'Half Day'
        LATE = 'late', 'Late'
        WORK_FROM_HOME = 'work_from_home', 'Work From Home'
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_faculty_attendance')
    
    class Meta:
        db_table = 'faculty_attendance'
        ordering = ['-date']
        unique_together = ['faculty', 'date']
        verbose_name = 'Faculty Attendance'
        verbose_name_plural = 'Faculty Attendance Records'
        indexes = [
            models.Index(fields=['faculty', 'date']),
            models.Index(fields=['date', 'status']),
        ]
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.date} - {self.status}"

