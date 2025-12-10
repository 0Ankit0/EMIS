from django.db import models
from apps.core.models import TimeStampedModel

class Floor(TimeStampedModel):
    """Floor in a Hostel"""
    hostel = models.ForeignKey('hostel.Hostel', on_delete=models.CASCADE, related_name='floors')
    floor_number = models.IntegerField(validators=[models.Min(0)])
    total_rooms = models.IntegerField(validators=[models.Min(1)])
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'hostel_floors'
        unique_together = ['hostel', 'floor_number']
        ordering = ['hostel', 'floor_number']
        verbose_name = 'Floor'
        verbose_name_plural = 'Floors'
    def __str__(self):
        return f"{self.hostel.name} - Floor {self.floor_number}"
