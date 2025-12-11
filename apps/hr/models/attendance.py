"""HR Attendance Model"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from .employee import Employee

User = get_user_model()


class Attendance(TimeStampedModel):
    """Employee Attendance"""
    
    class Status(models.TextChoices):
        PRESENT = 'present', 'Present'
        ABSENT = 'absent', 'Absent'
        HALF_DAY = 'half_day', 'Half Day'
        LATE = 'late', 'Late'
        ON_LEAVE = 'on_leave', 'On Leave'
        WORK_FROM_HOME = 'work_from_home', 'Work From Home'
        HOLIDAY = 'holiday', 'Holiday'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    working_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_hr_attendance')
    remarks = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hr_attendance'
        unique_together = ['employee', 'date']
        ordering = ['-date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['employee', 'date']),
            models.Index(fields=['date', 'status']),
        ]
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"
