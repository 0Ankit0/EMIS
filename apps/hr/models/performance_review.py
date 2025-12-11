"""HR Performance Review Model"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from .employee import Employee

User = get_user_model()


class PerformanceReview(TimeStampedModel):
    """Employee Performance Review/Appraisal"""
    
    class ReviewType(models.TextChoices):
        PROBATION = 'probation', 'Probation Review'
        QUARTERLY = 'quarterly', 'Quarterly Review'
        HALF_YEARLY = 'half_yearly', 'Half-Yearly Review'
        ANNUAL = 'annual', 'Annual Review'
        SPECIAL = 'special', 'Special Review'
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
    
    class Rating(models.IntegerChoices):
        POOR = 1, 'Poor'
        BELOW_AVERAGE = 2, 'Below Average'
        AVERAGE = 3, 'Average'
        GOOD = 4, 'Good'
        EXCELLENT = 5, 'Excellent'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    
    review_type = models.CharField(max_length=20, choices=ReviewType.choices)
    review_period_start = models.DateField()
    review_period_end = models.DateField()
    
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='conducted_reviews')
    
    # Ratings
    technical_skills = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    communication = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    teamwork = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    leadership = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    punctuality = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    quality_of_work = models.IntegerField(choices=Rating.choices, null=True, blank=True)
    
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    
    strengths = models.TextField(blank=True)
    areas_of_improvement = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    goals_for_next_period = models.TextField(blank=True)
    
    comments = models.TextField(blank=True)
    employee_comments = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    review_date = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'hr_performance_reviews'
        ordering = ['-review_period_end']
        verbose_name = 'Performance Review'
        verbose_name_plural = 'Performance Reviews'
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.review_type} ({self.review_period_end})"
    
    def calculate_overall_rating(self):
        """Calculate overall rating from individual ratings"""
        ratings = [
            self.technical_skills, self.communication, self.teamwork,
            self.leadership, self.punctuality, self.quality_of_work
        ]
        valid_ratings = [r for r in ratings if r is not None]
        
        if valid_ratings:
            return round(sum(valid_ratings) / len(valid_ratings), 2)
        return None
