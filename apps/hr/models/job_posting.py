"""HR Job Posting Model"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from .department import Department
from .designation import Designation

User = get_user_model()


class JobPosting(TimeStampedModel):
    """Job Opening/Vacancy Posting"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        OPEN = 'open', 'Open'
        CLOSED = 'closed', 'Closed'
        ON_HOLD = 'on_hold', 'On Hold'
        FILLED = 'filled', 'Filled'
    
    title = models.CharField(max_length=200)
    job_code = models.CharField(max_length=50, unique=True, db_index=True)
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='job_postings')
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name='job_postings')
    
    number_of_positions = models.IntegerField(validators=[MinValueValidator(1)])
    employment_type = models.CharField(max_length=20)
    
    description = models.TextField()
    required_qualifications = models.TextField()
    required_experience_years = models.IntegerField(validators=[MinValueValidator(0)])
    required_skills = models.TextField()
    
    responsibilities = models.TextField()
    
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    location = models.CharField(max_length=200)
    
    posted_date = models.DateField(auto_now_add=True)
    application_deadline = models.DateField()
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posted_jobs')
    
    class Meta:
        db_table = 'hr_job_postings'
        ordering = ['-posted_date']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'
    
    def __str__(self):
        return f"{self.job_code} - {self.title}"
