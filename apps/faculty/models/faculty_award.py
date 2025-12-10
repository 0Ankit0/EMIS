from django.db import models
from apps.core.models import TimeStampedModel
from .faculty import Faculty

class FacultyAward(TimeStampedModel):
    """Awards and Achievements of Faculty"""
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=300)
    awarding_body = models.CharField(max_length=300)
    date_received = models.DateField()
    description = models.TextField(blank=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('teaching', 'Teaching Excellence'),
            ('research', 'Research Excellence'),
            ('service', 'Service'),
            ('national', 'National Level'),
            ('international', 'International Level'),
            ('other', 'Other'),
        ],
        default='other'
    )
    certificate = models.FileField(upload_to='faculty/awards/%Y/%m/', blank=True, null=True)
    class Meta:
        db_table = 'faculty_awards'
        ordering = ['-date_received']
        verbose_name = 'Faculty Award'
        verbose_name_plural = 'Faculty Awards'
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.title}"
