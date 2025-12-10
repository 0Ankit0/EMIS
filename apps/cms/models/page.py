import uuid
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from apps.authentication.models import User

class Page(models.Model):
    """Static pages"""
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="Short description")
    meta_title = models.CharField(max_length=300, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    featured_image = models.ImageField(upload_to='cms/pages/%Y/%m/', blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    template = models.CharField(max_length=100, default='default')
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_homepage = models.BooleanField(default=False)
    show_in_menu = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pages'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_pages'
    )
    
    class Meta:
        db_table = 'cms_pages'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'published_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        if self.is_homepage:
            Page.objects.filter(is_homepage=True).update(is_homepage=False)
        super().save(*args, **kwargs)

