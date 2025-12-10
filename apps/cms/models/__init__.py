"""
Comprehensive CMS Models for EMIS
"""
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from apps.authentication.models import User
import uuid


class Category(models.Model):
    """Content categories"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    
    # Display
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#3B82F6')
    order = models.IntegerField(default=0)
    
    # Meta
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_categories'
    )
    
    class Meta:
        db_table = 'cms_categories'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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


class Page(models.Model):
    """Static pages"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    
    # Content
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="Short description")
    
    # Meta
    meta_title = models.CharField(max_length=300, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Featured image
    featured_image = models.ImageField(upload_to='cms/pages/%Y/%m/', blank=True, null=True)
    
    # Organization
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    template = models.CharField(max_length=100, default='default')
    order = models.IntegerField(default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_homepage = models.BooleanField(default=False)
    show_in_menu = models.BooleanField(default=True)
    
    # Publishing
    published_at = models.DateTimeField(null=True, blank=True)
    
    # Views and stats
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Authors
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
        
        # Set published_at on first publish
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        # Only one homepage
        if self.is_homepage:
            Page.objects.filter(is_homepage=True).update(is_homepage=False)
        
        super().save(*args, **kwargs)


class Post(models.Model):
    """Blog posts and news articles"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('scheduled', 'Scheduled'),
        ('archived', 'Archived'),
    ]
    
    POST_TYPES = [
        ('post', 'Blog Post'),
        ('news', 'News'),
        ('announcement', 'Announcement'),
        ('event', 'Event'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    
    # Content
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    
    # Type
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='post')
    
    # Categorization
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    
    # Media
    featured_image = models.ImageField(upload_to='cms/posts/%Y/%m/', blank=True, null=True)
    gallery_images = models.JSONField(default=list, blank=True)
    
    # Meta
    meta_title = models.CharField(max_length=300, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    allow_comments = models.BooleanField(default=True)
    
    # Publishing
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    
    # Event specific (if post_type='event')
    event_date = models.DateTimeField(null=True, blank=True)
    event_location = models.CharField(max_length=300, blank=True)
    event_end_date = models.DateTimeField(null=True, blank=True)
    
    # Stats
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Authors
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
        
        # Auto-publish scheduled posts
        if self.status == 'scheduled' and self.scheduled_for:
            if timezone.now() >= self.scheduled_for:
                self.status = 'published'
                self.published_at = timezone.now()
        
        # Set published_at on first publish
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)


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
    
    # Image specific
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    
    # Metadata
    alt_text = models.CharField(max_length=300, blank=True)
    caption = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    # Organization
    folder = models.CharField(max_length=300, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='media')
    
    # Stats
    download_count = models.IntegerField(default=0)
    
    # Timestamps
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


class Comment(models.Model):
    """Comments on posts"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('spam', 'Spam'),
        ('trash', 'Trash'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    # Author info
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='comments'
    )
    author_name = models.CharField(max_length=200, blank=True)
    author_email = models.EmailField(blank=True)
    author_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Content
    content = models.TextField()
    
    # Threading
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_pinned = models.BooleanField(default=False)
    
    # Stats
    like_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cms_comments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        author = self.author.username if self.author else self.author_name
        return f'Comment by {author} on {self.post.title}'


class Menu(models.Model):
    """Navigation menus"""
    LOCATIONS = [
        ('header', 'Header'),
        ('footer', 'Footer'),
        ('sidebar', 'Sidebar'),
        ('mobile', 'Mobile'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=20, choices=LOCATIONS)
    description = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cms_menus'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Menu items"""
    LINK_TYPES = [
        ('page', 'Page'),
        ('post', 'Post'),
        ('category', 'Category'),
        ('custom', 'Custom URL'),
        ('external', 'External URL'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    
    # Content
    title = models.CharField(max_length=200)
    link_type = models.CharField(max_length=20, choices=LINK_TYPES)
    
    # Links
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    custom_url = models.CharField(max_length=500, blank=True)
    
    # Display
    icon = models.CharField(max_length=50, blank=True)
    css_class = models.CharField(max_length=100, blank=True)
    target = models.CharField(
        max_length=20,
        choices=[('_self', 'Same Window'), ('_blank', 'New Window')],
        default='_self'
    )
    
    # Hierarchy
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    order = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'cms_menu_items'
        ordering = ['order']
    
    def __str__(self):
        return f'{self.menu.name} - {self.title}'
    
    def get_url(self):
        """Get the URL for this menu item"""
        if self.link_type == 'page' and self.page:
            return f'/pages/{self.page.slug}/'
        elif self.link_type == 'post' and self.post:
            return f'/blog/{self.post.slug}/'
        elif self.link_type == 'category' and self.category:
            return f'/category/{self.category.slug}/'
        elif self.link_type in ['custom', 'external']:
            return self.custom_url
        return '#'


class Slider(models.Model):
    """Homepage sliders/carousels"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    
    # Image
    image = models.ImageField(upload_to='cms/sliders/')
    mobile_image = models.ImageField(upload_to='cms/sliders/', blank=True, null=True)
    
    # Link
    link_text = models.CharField(max_length=100, blank=True)
    link_url = models.CharField(max_length=500, blank=True)
    
    # Display
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Scheduling
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sliders'
    )
    
    class Meta:
        db_table = 'cms_sliders'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title


class Widget(models.Model):
    """Sidebar widgets"""
    WIDGET_TYPES = [
        ('html', 'HTML'),
        ('recent_posts', 'Recent Posts'),
        ('popular_posts', 'Popular Posts'),
        ('categories', 'Categories'),
        ('tags', 'Tags'),
        ('search', 'Search'),
        ('newsletter', 'Newsletter'),
        ('social', 'Social Media'),
        ('custom', 'Custom'),
    ]
    
    POSITIONS = [
        ('sidebar_left', 'Left Sidebar'),
        ('sidebar_right', 'Right Sidebar'),
        ('footer_1', 'Footer Column 1'),
        ('footer_2', 'Footer Column 2'),
        ('footer_3', 'Footer Column 3'),
        ('footer_4', 'Footer Column 4'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    position = models.CharField(max_length=20, choices=POSITIONS)
    
    # Content
    content = models.TextField(blank=True)
    settings = models.JSONField(default=dict, blank=True)
    
    # Display
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    # Visibility
    show_on_pages = models.ManyToManyField(Page, blank=True)
    show_on_posts = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cms_widgets'
        ordering = ['position', 'order']
    
    def __str__(self):
        return f'{self.title} ({self.position})'


class Newsletter(models.Model):
    """Newsletter subscriptions"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('unsubscribed', 'Unsubscribed'),
        ('bounced', 'Bounced'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'cms_newsletter'
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class SEO(models.Model):
    """SEO settings for pages"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Links
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
    
    # Meta
    title = models.CharField(max_length=300)
    description = models.TextField()
    keywords = models.CharField(max_length=500, blank=True)
    
    # Open Graph
    og_title = models.CharField(max_length=300, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to='cms/seo/og/', blank=True, null=True)
    
    # Twitter
    twitter_title = models.CharField(max_length=300, blank=True)
    twitter_description = models.TextField(blank=True)
    twitter_image = models.ImageField(upload_to='cms/seo/twitter/', blank=True, null=True)
    
    # Schema
    schema_type = models.CharField(max_length=50, blank=True)
    schema_data = models.JSONField(default=dict, blank=True)
    
    # Indexing
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
