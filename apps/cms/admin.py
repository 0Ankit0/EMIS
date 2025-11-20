"""
CMS Admin Configuration
"""
from django.contrib import admin
from .models import (
    Category, Tag, Page, Post, Media, Comment,
    Menu, MenuItem, Slider, Widget, Newsletter, SEO
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin"""
    list_display = ['name', 'slug', 'parent', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin"""
    list_display = ['name', 'slug', 'color', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Page admin"""
    list_display = [
        'title', 'slug', 'status', 'is_homepage', 'show_in_menu',
        'author', 'view_count', 'created_at'
    ]
    list_filter = ['status', 'is_homepage', 'show_in_menu', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'excerpt')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Organization', {
            'fields': ('parent', 'template', 'order')
        }),
        ('Status', {
            'fields': ('status', 'is_homepage', 'show_in_menu')
        }),
        ('Metadata', {
            'fields': ('author', 'updated_by', 'view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post admin"""
    list_display = [
        'title', 'slug', 'post_type', 'category', 'status',
        'is_featured', 'author', 'view_count', 'published_at'
    ]
    list_filter = [
        'post_type', 'status', 'is_featured', 'is_pinned',
        'category', 'published_at', 'created_at'
    ]
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = [
        'view_count', 'like_count', 'comment_count', 'share_count',
        'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'post_type')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': (
                'status', 'is_featured', 'is_pinned', 'allow_comments',
                'scheduled_for'
            )
        }),
        ('Event Information', {
            'fields': ('event_date', 'event_end_date', 'event_location'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': (
                'view_count', 'like_count', 'comment_count', 'share_count'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': (
                'author', 'updated_by', 'published_at',
                'created_at', 'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    """Media library admin"""
    list_display = [
        'title', 'file_type', 'mime_type', 'file_size',
        'download_count', 'uploaded_by', 'uploaded_at'
    ]
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['title', 'alt_text', 'caption', 'description']
    readonly_fields = [
        'file_size', 'mime_type', 'width', 'height',
        'download_count', 'uploaded_at'
    ]
    filter_horizontal = ['tags']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin"""
    list_display = [
        'get_author', 'post', 'status', 'is_pinned',
        'like_count', 'created_at'
    ]
    list_filter = ['status', 'is_pinned', 'created_at']
    search_fields = ['content', 'author_name', 'author_email']
    readonly_fields = ['author_ip', 'created_at', 'updated_at']
    
    def get_author(self, obj):
        if obj.author:
            return obj.author.username
        return obj.author_name
    get_author.short_description = 'Author'


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    """Menu admin"""
    list_display = ['name', 'location', 'is_active', 'created_at']
    list_filter = ['location', 'is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Menu item admin"""
    list_display = [
        'title', 'menu', 'link_type', 'parent', 'order', 'is_active'
    ]
    list_filter = ['menu', 'link_type', 'is_active']
    search_fields = ['title', 'custom_url']
    ordering = ['menu', 'order']


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    """Slider admin"""
    list_display = [
        'title', 'order', 'is_active', 'start_date', 'end_date', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    """Widget admin"""
    list_display = [
        'title', 'widget_type', 'position', 'order', 'is_active'
    ]
    list_filter = ['widget_type', 'position', 'is_active']
    search_fields = ['title', 'content']
    filter_horizontal = ['show_on_pages']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Newsletter admin"""
    list_display = [
        'email', 'name', 'status', 'subscribed_at', 'unsubscribed_at'
    ]
    list_filter = ['status', 'subscribed_at']
    search_fields = ['email', 'name']
    readonly_fields = ['ip_address', 'user_agent', 'subscribed_at', 'unsubscribed_at']


@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    """SEO admin"""
    list_display = ['__str__', 'title', 'index', 'follow', 'updated_at']
    search_fields = ['title', 'description', 'keywords']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Basic SEO', {
            'fields': ('page', 'post', 'title', 'description', 'keywords')
        }),
        ('Open Graph', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',)
        }),
        ('Twitter Card', {
            'fields': ('twitter_title', 'twitter_description', 'twitter_image'),
            'classes': ('collapse',)
        }),
        ('Schema.org', {
            'fields': ('schema_type', 'schema_data'),
            'classes': ('collapse',)
        }),
        ('Indexing', {
            'fields': ('index', 'follow', 'canonical_url')
        }),
    )
