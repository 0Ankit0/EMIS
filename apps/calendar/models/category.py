from django.db import models
from .base import TimeStampedModel

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, blank=True, help_text="Hex color code")
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
