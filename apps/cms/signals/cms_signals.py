"""
CMS Signals
"""
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Page, Post, Media, Comment
from .utils import generate_unique_slug, get_file_type, get_image_dimensions
import os

@receiver(pre_save, sender=Page)
def page_pre_save(sender, instance, **kwargs):
    """Handle page pre-save"""
    # Generate unique slug if not provided
    if not instance.slug:
        instance.slug = generate_unique_slug(Page, instance.title, instance.id)

@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, **kwargs):
    """Handle post pre-save"""
    # Generate unique slug if not provided
    if not instance.slug:
        instance.slug = generate_unique_slug(Post, instance.title, instance.id)
    # Generate excerpt if not provided
    if not instance.excerpt and instance.content:
        from .utils import generate_excerpt
        instance.excerpt = generate_excerpt(instance.content)

@receiver(pre_save, sender=Media)
def media_pre_save(sender, instance, **kwargs):
    """Handle media pre-save"""
    if instance.file:
        # Determine file type
        if not instance.file_type:
            instance.file_type = get_file_type(instance.file)
        # Get file size
        instance.file_size = instance.file.size
        # Get mime type
        import mimetypes
        mime_type, _ = mimetypes.guess_type(instance.file.name)
        instance.mime_type = mime_type or 'application/octet-stream'
        # Get image dimensions if image
        if instance.file_type == 'image':
            width, height = get_image_dimensions(instance.file)
            instance.width = width
            instance.height = height

@receiver(post_delete, sender=Media)
def media_post_delete(sender, instance, **kwargs):
    """Delete file when media object is deleted"""
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    """Update post comment count"""
    if created:
        post = instance.post
        post.comment_count = post.comments.filter(status='approved').count()
        post.save(update_fields=['comment_count'])

@receiver(post_delete, sender=Comment)
def comment_post_delete(sender, instance, **kwargs):
    """Update post comment count"""
    post = instance.post
    post.comment_count = post.comments.filter(status='approved').count()
    post.save(update_fields=['comment_count'])
