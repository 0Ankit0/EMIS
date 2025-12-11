"""HR Training Participant Model"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .employee import Employee
from .training import Training


class TrainingParticipant(TimeStampedModel):
    """Training Participants"""
    
    class Status(models.TextChoices):
        ENROLLED = 'enrolled', 'Enrolled'
        ATTENDED = 'attended', 'Attended'
        COMPLETED = 'completed', 'Completed'
        DROPPED = 'dropped', 'Dropped'
    
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='participants')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='training_participations')
    
    enrollment_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ENROLLED)
    
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    assessment_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    certificate_issued = models.BooleanField(default=False)
    certificate = models.FileField(upload_to='hr/training_certificates/%Y/', blank=True, null=True)
    
    feedback = models.TextField(blank=True)
    
    class Meta:
        db_table = 'hr_training_participants'
        unique_together = ['training', 'employee']
        ordering = ['-enrollment_date']
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.training.title}"
