"""
CMS Utility Functions
"""
from django.utils.text import slugify as django_slugify
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import mimetypes


def generate_unique_slug(model, title, instance_id=None):
    """Generate unique slug for model"""
    base_slug = django_slugify(title)
    slug = base_slug
    counter = 1
    
    queryset = model.objects.all()
    if instance_id:
        queryset = queryset.exclude(id=instance_id)
    
    while queryset.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug


def resize_image(image_file, max_width=1920, max_height=1080, quality=85):
    """Resize image while maintaining aspect ratio"""
    img = Image.open(image_file)
    
    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    # Calculate new dimensions
    width, height = img.size
    
    if width > max_width or height > max_height:
        # Calculate aspect ratio
        aspect = width / height
        
        if width > height:
            new_width = max_width
            new_height = int(new_width / aspect)
        else:
            new_height = max_height
            new_width = int(new_height * aspect)
        
        # Resize
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save to BytesIO
    output = BytesIO()
    img.save(output, format='JPEG', quality=quality, optimize=True)
    output.seek(0)
    
    return output


def get_file_type(file):
    """Determine file type from file"""
    mime_type, _ = mimetypes.guess_type(file.name)
    
    if not mime_type:
        return 'other'
    
    if mime_type.startswith('image/'):
        return 'image'
    elif mime_type.startswith('video/'):
        return 'video'
    elif mime_type.startswith('audio/'):
        return 'audio'
    elif mime_type in [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    ]:
        return 'document'
    else:
        return 'other'


def get_image_dimensions(image_file):
    """Get image width and height"""
    try:
        img = Image.open(image_file)
        return img.size
    except Exception:
        return None, None


def sanitize_filename(filename):
    """Sanitize filename"""
    name, ext = os.path.splitext(filename)
    name = django_slugify(name)
    return f"{name}{ext}"


def get_reading_time(content):
    """Calculate reading time in minutes"""
    words = len(content.split())
    minutes = round(words / 200)  # Average reading speed: 200 words per minute
    return max(1, minutes)


def truncate_html(html, length=200):
    """Truncate HTML content while preserving tags"""
    from html.parser import HTMLParser
    
    class HTMLTruncator(HTMLParser):
        def __init__(self, length):
            super().__init__()
            self.length = length
            self.text_length = 0
            self.result = []
            self.open_tags = []
            
        def handle_starttag(self, tag, attrs):
            if self.text_length < self.length:
                attr_str = ''.join([f' {k}="{v}"' for k, v in attrs])
                self.result.append(f'<{tag}{attr_str}>')
                self.open_tags.append(tag)
        
        def handle_endtag(self, tag):
            if self.open_tags and self.open_tags[-1] == tag:
                self.result.append(f'</{tag}>')
                self.open_tags.pop()
        
        def handle_data(self, data):
            if self.text_length < self.length:
                remaining = self.length - self.text_length
                if len(data) > remaining:
                    data = data[:remaining] + '...'
                self.result.append(data)
                self.text_length += len(data)
        
        def get_result(self):
            # Close any open tags
            while self.open_tags:
                tag = self.open_tags.pop()
                self.result.append(f'</{tag}>')
            return ''.join(self.result)
    
    truncator = HTMLTruncator(length)
    truncator.feed(html)
    return truncator.get_result()


def extract_first_image(content):
    """Extract first image URL from HTML content"""
    import re
    match = re.search(r'<img[^>]+src="([^"]+)"', content)
    if match:
        return match.group(1)
    return None


def generate_excerpt(content, length=200):
    """Generate excerpt from content"""
    from django.utils.html import strip_tags
    
    text = strip_tags(content)
    if len(text) <= length:
        return text
    
    return text[:length].rsplit(' ', 1)[0] + '...'


def get_related_posts(post, limit=4):
    """Get related posts based on category and tags"""
    from django.db.models import Count, Q
    from .models import Post
    
    related = Post.objects.filter(
        status='published',
        post_type=post.post_type
    ).exclude(id=post.id)
    
    # Filter by category
    if post.category:
        related = related.filter(category=post.category)
    
    # Filter by tags
    if post.tags.exists():
        related = related.filter(tags__in=post.tags.all())
        related = related.annotate(
            same_tags=Count('tags')
        ).order_by('-same_tags', '-published_at')
    else:
        related = related.order_by('-published_at')
    
    return related.distinct()[:limit]


def generate_sitemap_data():
    """Generate data for XML sitemap"""
    from .models import Page, Post
    
    data = {
        'pages': [],
        'posts': [],
    }
    
    # Pages
    pages = Page.objects.filter(status='published')
    for page in pages:
        data['pages'].append({
            'url': f'/pages/{page.slug}/',
            'lastmod': page.updated_at,
            'changefreq': 'monthly',
            'priority': 0.8 if page.is_homepage else 0.6,
        })
    
    # Posts
    posts = Post.objects.filter(status='published')
    for post in posts:
        data['posts'].append({
            'url': f'/blog/{post.slug}/',
            'lastmod': post.updated_at,
            'changefreq': 'weekly',
            'priority': 0.7,
        })
    
    return data
