"""Merit list model for ranking applications"""
import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class MeritList(TimeStampedModel):
    """Model representing a generated merit list"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    program = models.CharField(max_length=100, db_index=True)
    admission_year = models.IntegerField(db_index=True)
    admission_semester = models.CharField(max_length=20)
    
    # Generation metadata
    generation_timestamp = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True)
    
    # Criteria used for ranking
    criteria = models.JSONField(default=dict, help_text="Criteria used for merit calculation")
    
    # Merit list data
    ranked_applications = models.JSONField(default=list, help_text="List of ranked application IDs")
    total_applications = models.IntegerField(default=0)
    
    # Versioning
    version = models.IntegerField(default=1)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Cutoff information
    cutoff_rank = models.IntegerField(null=True, blank=True)
    cutoff_score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    class Meta:
        db_table = 'merit_lists'
        ordering = ['-generation_timestamp']
        unique_together = [['program', 'admission_year', 'admission_semester', 'version']]
        indexes = [
            models.Index(fields=['program', 'admission_year', 'is_published']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.program} ({self.admission_year})"
