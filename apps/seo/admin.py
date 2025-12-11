"""SEO Admin"""
from django.contrib import admin
from .models import SEOMetadata, Redirect, SitemapConfig, RobotsConfig, SEOAnalytics


@admin.register(SEOMetadata)
class SEOMetadataAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'meta_title', 'robots', 'include_in_sitemap', 'created_at']
    list_filter = ['robots', 'include_in_sitemap', 'content_type']
    search_fields = ['meta_title', 'meta_description', 'meta_keywords']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Content', {
            'fields': ('content_type', 'object_id')
        }),
        ('Basic SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url', 'robots')
        }),
        ('Open Graph (Facebook)', {
            'fields': ('og_title', 'og_description', 'og_image', 'og_type', 'og_url'),
            'classes': ('collapse',)
        }),
        ('Twitter Card', {
            'fields': ('twitter_card', 'twitter_title', 'twitter_description', 'twitter_image', 
                      'twitter_site', 'twitter_creator'),
            'classes': ('collapse',)
        }),
        ('Structured Data', {
            'fields': ('schema_markup',),
            'classes': ('collapse',)
        }),
        ('Sitemap', {
            'fields': ('include_in_sitemap', 'sitemap_priority', 'sitemap_changefreq')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ['old_path', 'new_path', 'redirect_type', 'hit_count', 'is_active', 'created_at']
    list_filter = ['redirect_type', 'is_active']
    search_fields = ['old_path', 'new_path']
    readonly_fields = ['hit_count', 'created_at', 'updated_at']


@admin.register(SitemapConfig)
class SitemapConfigAdmin(admin.ModelAdmin):
    list_display = ['app_label', 'model_name', 'priority', 'changefreq', 'is_enabled']
    list_filter = ['is_enabled', 'changefreq']
    search_fields = ['app_label', 'model_name']


@admin.register(RobotsConfig)
class RobotsConfigAdmin(admin.ModelAdmin):
    list_display = ['user_agent', 'crawl_delay', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['user_agent']
    ordering = ['order', 'user_agent']


@admin.register(SEOAnalytics)
class SEOAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'tracking_id', 'is_active']
    list_filter = ['platform', 'is_active']
    search_fields = ['name', 'tracking_id']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'platform', 'tracking_id', 'is_active')
        }),
        ('Script', {
            'fields': ('script_code',)
        }),
        ('Placement', {
            'fields': ('in_head', 'in_body_start', 'in_body_end')
        }),
    )
