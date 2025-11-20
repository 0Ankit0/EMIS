"""
Attendance Custom Managers
"""
from django.db import models


class AttendanceRecordManager(models.Manager):
    """Custom manager for AttendanceRecord"""
    
    def present(self):
        return self.filter(status='present')
    
    def absent(self):
        return self.filter(status__in=['absent', 'sick_leave'])
    
    def late(self):
        return self.filter(status='late')
    
    def for_date(self, date):
        return self.filter(date=date)
    
    def for_student(self, student):
        return self.filter(student=student)
