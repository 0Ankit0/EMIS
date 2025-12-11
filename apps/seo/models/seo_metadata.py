"""SEO Metadata Model"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.core.models import TimeStampedModel


class SEOMetadata(TimeStampedModel):
    """SEO Metadata for any content"""
    
    class RobotsChoice(models.TextChoices):
        INDEX_FOLLOW = 'index, follow', 'Index, Follow'
        NO_INDEX_FOLLOW = 'noindex, follow', 'NoIndex, Follow'
        INDEX_NO_FOLLOW = 'index, nofollow', 'Index, NoFollow'
        NO_INDEX_NO_FOLLOW = 'noindex, nofollow', 'NoIndex, NoFollow'
    
    class TwitterCardType(models.TextChoices):
        SUMMARY = 'summary', 'Summary'
        SUMMARY_LARGE = 'summary_large_image', 'Summary Large Image'
        APP = 'app', 'App'
        PLAYER = 'player', 'Player'
    
    # Generic relation to any model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Basic SEO
    meta_title = models.CharField(max_length=200, help_text='SEO Title (60-70 chars)')
    meta_description = models.TextField(max_length=300, help_text='SEO Description (150-160 chars)')
    meta_keywords = models.CharField(max_length=500, blank=True, help_text='Comma-separated keywords')
    
    canonical_url = models.URLField(blank=True, help_text='Canonical URL for duplicate content')
    robots = models.CharField(
        max_length=50,
        choices=RobotsChoice.choices,
        default=RobotsChoice.INDEX_FOLLOW
    )
    
    # Open Graph (Facebook)
    og_title = models.CharField(max_length=200, blank=True)
    og_description = models.TextField(max_length=300, blank=True)
    og_image = models.ImageField(upload_to='seo/og_images/', blank=True, null=True)
    og_type = models.CharField(max_length=50, default='website', blank=True)
    og_url = models.URLField(blank=True)
    
    # Twitter Card
    twitter_card = models.CharField(
        max_length=50,
        choices=TwitterCardType.choices,
        default=TwitterCardType.SUMMARY,
        blank=True
    )
    twitter_title = models.CharField(max_length=200, blank=True)
    twitter_description = models.TextField(max_length=300, blank=True)
    twitter_image = models.ImageField(upload_to='seo/twitter_images/', blank=True, null=True)
    twitter_site = models.CharField(max_length=50, blank=True, help_text='@username')
    twitter_creator = models.CharField(max_length=50, blank=True, help_text='@username')
    
    # JSON-LD Schema
    schema_markup = models.JSONField(blank=True, null=True, help_text='Structured data JSON-LD')
    
    # Sitemap
    include_in_sitemap = models.BooleanField(default=True)
    sitemap_priority = models.DecimalField(
        max_digits=2, decimal_places=1, default=0.5,
        help_text='Priority (0.0 - 1.0)'
    )
    sitemap_changefreq = models.CharField(
        max_length=20, default='weekly',
        choices=[
            ('always', 'Always'),
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('never', 'Never'),
        ]
    )
    
    objects = models.Manager()
    
    class Meta:
        db_table = 'seo_metadata'
        unique_together = ['content_type', 'object_id']
        verbose_name = 'SEO Metadata'
        verbose_name_plural = 'SEO Metadata'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return f"SEO for {self.content_object}"
    
    def save(self, *args, **kwargs):
        if not self.og_title:
            self.og_title = self.meta_title
        if not self.og_description:
            self.og_description = self.meta_description
        if not self.twitter_title:
            self.twitter_title = self.meta_title
        if not self.twitter_description:
            self.twitter_description = self.meta_description
        
        super().save(*args, **kwargs)
