"""SEO Analytics Model"""
from django.db import models
from apps.core.models import TimeStampedModel


class SEOAnalytics(TimeStampedModel):
    """SEO Analytics and Tracking"""
    
    class AnalyticsPlatform(models.TextChoices):
        GOOGLE_ANALYTICS = 'ga', 'Google Analytics'
        GOOGLE_TAG_MANAGER = 'gtm', 'Google Tag Manager'
        FACEBOOK_PIXEL = 'fb', 'Facebook Pixel'
        HOTJAR = 'hotjar', 'Hotjar'
        CUSTOM = 'custom', 'Custom Script'
    
    name = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=AnalyticsPlatform.choices)
    
    tracking_id = models.CharField(max_length=200, blank=True, help_text='GA Tracking ID, GTM ID, etc.')
    script_code = models.TextField(blank=True, help_text='Custom tracking script')
    
    # Placement
    in_head = models.BooleanField(default=True, help_text='Include in <head> tag')
    in_body_start = models.BooleanField(default=False, help_text='Include at start of <body>')
    in_body_end = models.BooleanField(default=False, help_text='Include at end of <body>')
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'seo_analytics'
        verbose_name = 'SEO Analytics'
        verbose_name_plural = 'SEO Analytics'
    
    def __str__(self):
        return f"{self.name} ({self.get_platform_display()})"
