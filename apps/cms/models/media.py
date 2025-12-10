import uuid
from django.db import models
from apps.authentication.models import User
from .tag import Tag

class Media(models.Model):
    """Media library"""
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    file = models.FileField(upload_to='cms/media/%Y/%m/')
    file_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    file_size = models.BigIntegerField(help_text="Size in bytes")
    mime_type = models.CharField(max_length=100)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    alt_text = models.CharField(max_length=300, blank=True)
    caption = models.TextField(blank=True)
    description = models.TextField(blank=True)
    folder = models.CharField(max_length=300, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='media')
    download_count = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_media'
    )
    class Meta:
        db_table = 'cms_media'
        verbose_name_plural = 'Media'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['file_type']),
            models.Index(fields=['uploaded_at']),
        ]
    def __str__(self):
        return self.title
