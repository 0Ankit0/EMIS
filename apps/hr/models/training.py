"""HR Training Model"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel

User = get_user_model()


class Training(TimeStampedModel):
    """Training Programs"""
    
    class Status(models.TextChoices):
        PLANNED = 'planned', 'Planned'
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    
    trainer_name = models.CharField(max_length=200)
    trainer_organization = models.CharField(max_length=200, blank=True)
    
    start_date = models.DateField()
    end_date = models.DateField()
    duration_hours = models.IntegerField(validators=[MinValueValidator(1)])
    
    location = models.CharField(max_length=200)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    
    cost_per_participant = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLANNED)
    
    organized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organized_trainings')
    
    class Meta:
        db_table = 'hr_trainings'
        ordering = ['-start_date']
        verbose_name = 'Training'
        verbose_name_plural = 'Trainings'
    
    def __str__(self):
        return f"{self.code} - {self.title}"
