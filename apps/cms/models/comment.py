import uuid
from django.db import models
from apps.authentication.models import User
from .post import Post

class Comment(models.Model):
    """Comments on posts"""
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        SPAM = 'spam', 'Spam'
        TRASH = 'trash', 'Trash'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
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
    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    is_pinned = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
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

