import uuid
from django.db import models
from .page import Page
from .post import Post

class SEO(models.Model):
    """SEO settings for pages"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    page = models.OneToOneField(
        Page,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='seo'
    )
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='seo'
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    keywords = models.CharField(max_length=500, blank=True)
    og_title = models.CharField(max_length=300, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='cms/seo/og/', blank=True, null=True)
    twitter_title = models.CharField(max_length=300, blank=True)
    twitter_description = models.TextField(blank=True)
    twitter_image = models.ImageField(upload_to='cms/seo/twitter/', blank=True, null=True)
    schema_type = models.CharField(max_length=50, blank=True)
    schema_data = models.JSONField(default=dict, blank=True)
    index = models.BooleanField(default=True)
    follow = models.BooleanField(default=True)
    canonical_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'cms_seo'
        verbose_name = 'SEO'
        verbose_name_plural = 'SEO'
    def __str__(self):
        if self.page:
            return f'SEO for {self.page.title}'
        elif self.post:
            return f'SEO for {self.post.title}'
        return 'SEO Settings'
