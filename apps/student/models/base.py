from django.db import models
import uuid

class BaseModel(models.Model):
    """Abstract base class that provides ``ukid``,
    ``created_at`` and ``updated_at`` fields."""
    ukid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
