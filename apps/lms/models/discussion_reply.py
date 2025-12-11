from django.db import models
from apps.core.models import TimeStampedModel
from .discussion import Discussion
from django.contrib.auth import get_user_model

User = get_user_model()

class DiscussionReply(TimeStampedModel):
    """Reply to Discussion Thread"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child_replies')
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lms_discussion_replies')
    is_answer = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    class Meta:
        db_table = 'lms_discussion_replies'
        ordering = ['created_at']
        verbose_name = 'Discussion Reply'
        verbose_name_plural = 'Discussion Replies'
    def __str__(self):
        return f"Reply to {self.discussion.title}"
