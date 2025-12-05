from django.db import models
from .base import BaseModel

class Calendar(BaseModel):
    """Model representing a calendar."""
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self) -> str: # what to return when we print an object of this class
        return self.title
    
    class Meta: # type: ignore
        verbose_name = "Calendar"
        verbose_name_plural = "Calendars"
        ordering = ['start_date']
