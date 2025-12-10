import uuid
from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    """Content tags"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6B7280')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'cms_tags'
        ordering = ['name']
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
