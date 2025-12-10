import uuid
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from apps.authentication.models import User
from .category import Category
from .tag import Tag

class Post(models.Model):
    """Blog posts and news articles"""
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        SCHEDULED = 'scheduled', 'Scheduled'
        ARCHIVED = 'archived', 'Archived'
    
    class PostType(models.TextChoices):
        POST = 'post', 'Blog Post'
        NEWS = 'news', 'News'
        ANNOUNCEMENT = 'announcement', 'Announcement'
        EVENT = 'event', 'Event'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    post_type = models.CharField(max_length=20, choices=PostType.choices, default=PostType.POST)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    featured_image = models.ImageField(upload_to='cms/posts/%Y/%m/', blank=True, null=True)
    gallery_images = models.JSONField(default=list, blank=True)
    meta_title = models.CharField(max_length=300, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    event_location = models.CharField(max_length=300, blank=True)
    event_end_date = models.DateTimeField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_posts'
    )
    
    class Meta:
        db_table = 'cms_posts'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'published_at']),
            models.Index(fields=['post_type', 'status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == Status.SCHEDULED and self.scheduled_for:
            if timezone.now() >= self.scheduled_for:
                self.status = Status.PUBLISHED
                self.published_at = timezone.now()
        if self.status == Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

