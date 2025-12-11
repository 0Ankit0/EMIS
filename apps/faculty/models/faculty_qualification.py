from django.db import models
from apps.core.models import TimeStampedModel
from .faculty import Faculty
from ..managers import FacultyQualificationManager

class FacultyQualification(TimeStampedModel):
    """Educational Qualifications of Faculty"""
    class Degree(models.TextChoices):
        PHD = 'phd', 'Ph.D.'
        MASTERS = 'masters', 'Masters'
        BACHELORS = 'bachelors', 'Bachelors'
        DIPLOMA = 'diploma', 'Diploma'
        CERTIFICATION = 'certification', 'Certification'
        OTHER = 'other', 'Other'
    
    class GradeSystem(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        CGPA_10 = 'cgpa_10', 'CGPA (10 Point)'
        CGPA_4 = 'cgpa_4', 'CGPA (4 Point)'
        GRADE = 'grade', 'Grade'
    
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='qualifications')
    degree = models.CharField(max_length=50, choices=Degree.choices)
    degree_name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    institution = models.CharField(max_length=300)
    university = models.CharField(max_length=300)
    year_of_passing = models.IntegerField()
    percentage_or_cgpa = models.CharField(max_length=20)
    grade_system = models.CharField(max_length=20, choices=GradeSystem.choices, default=GradeSystem.PERCENTAGE)
    certificate = models.FileField(upload_to='faculty/qualifications/%Y/%m/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    objects = FacultyQualificationManager()
    
    class Meta:
        db_table = 'faculty_qualifications'
        ordering = ['-year_of_passing']
        verbose_name = 'Faculty Qualification'
        verbose_name_plural = 'Faculty Qualifications'
    
    def __str__(self):
        return f"{self.faculty.get_full_name()} - {self.degree_name}"

