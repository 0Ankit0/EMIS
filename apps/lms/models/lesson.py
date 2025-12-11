from django.db import models
from apps.core.models import TimeStampedModel
from .module import Module

class Lesson(TimeStampedModel):
    """Course Lesson/Lecture"""
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('text', 'Text/Article'),
        ('pdf', 'PDF Document'),
        ('quiz', 'Quiz'),
        ('assignment', 'Assignment'),
        ('live', 'Live Session'),
    ]
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=300)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)
    text_content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='lms/lesson_videos/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='lms/lesson_pdfs/', blank=True, null=True)
    attachments = models.JSONField(default=list, blank=True)
    external_links = models.JSONField(default=list, blank=True)
    is_preview = models.BooleanField(default=False, help_text="Can be accessed without enrollment")
    is_published = models.BooleanField(default=False)
    class Meta:
        db_table = 'lms_lessons'
        ordering = ['module', 'order']
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
    def __str__(self):
        return f"{self.module.course.code} - {self.title}"
