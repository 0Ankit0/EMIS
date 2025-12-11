from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .enrollment import Enrollment

class Certificate(TimeStampedModel):
    """Course Completion Certificate"""
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    certificate_number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField(default=timezone.now)
    certificate_file = models.FileField(upload_to='lms/certificates/%Y/', blank=True, null=True)
    verification_url = models.URLField(blank=True)
    class Meta:
        db_table = 'lms_certificates'
        ordering = ['-issue_date']
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'
    def __str__(self):
        return f"{self.certificate_number} - {self.enrollment.student.user.email}"
