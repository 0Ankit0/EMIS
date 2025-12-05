from django.db import models
from django.core.exceptions import ValidationError

from apps.calendar.models.base import BaseModel
from . import Student
import uuid

class AcademicRecord(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    semester = models.CharField(max_length=20)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    total_credits = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)

    def clean(self):
        if self.gpa is not None:
            if self.gpa < 0 or self.gpa > 4.00:
                raise ValidationError('GPA must be between 0.00 and 4.00.')
        
        if self.total_credits is not None and self.total_credits < 0:
            raise ValidationError('Total credits cannot be negative.')

    def __str__(self):
        return f"Academic Record of {self.student.first_name} {self.student.last_name} for {self.semester}"

    
    class Meta(): # type: ignore
        db_table = 'academic_records'
        ordering = ['-semester']
