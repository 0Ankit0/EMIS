"""Exam Schedule Model"""
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ExamSchedule(models.Model):
    """Exam schedule model"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    academic_year = models.CharField(max_length=20)
    semester = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='exam_schedules_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'exam_schedules'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} - {self.academic_year}"
