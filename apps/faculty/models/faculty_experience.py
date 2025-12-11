from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .faculty import Faculty
from ..managers import FacultyExperienceManager

class FacultyExperience(TimeStampedModel):
    """Work Experience of Faculty"""
    class ExperienceType(models.TextChoices):
        TEACHING = 'teaching', 'Teaching'
        RESEARCH = 'research', 'Research'
        INDUSTRY = 'industry', 'Industry'
        ADMINISTRATIVE = 'administrative', 'Administrative'
        OTHER = 'other', 'Other'
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='experiences')
    organization = models.CharField(max_length=300)
    designation = models.CharField(max_length=200)
    experience_type = models.CharField(max_length=20, choices=ExperienceType.choices, default=ExperienceType.TEACHING)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    responsibilities = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    certificate = models.FileField(upload_to='faculty/experience/%Y/%m/', blank=True, null=True)
    
    objects = FacultyExperienceManager()
    
    class Meta:
        db_table = 'faculty_experience'
        ordering = ['-start_date']
        verbose_name = 'Faculty Experience'
        verbose_name_plural = 'Faculty Experiences'
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.designation} at {self.organization}"
    
    def get_duration_years(self):
        end = self.end_date if self.end_date else timezone.now().date()
        delta = end - self.start_date
        return delta.days / 365.25

