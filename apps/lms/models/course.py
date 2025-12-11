from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from ..managers import CourseManager

User = get_user_model()

class Course(TimeStampedModel):
    """Online Course"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    title = models.CharField(max_length=300)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    instructor = models.ForeignKey('faculty.Faculty', on_delete=models.SET_NULL, null=True, related_name='lms_courses')
    thumbnail = models.ImageField(upload_to='lms/course_thumbnails/', blank=True, null=True)
    intro_video = models.FileField(upload_to='lms/course_videos/', blank=True, null=True)
    duration_hours = models.IntegerField(help_text="Estimated course duration in hours")
    prerequisites = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_free = models.BooleanField(default=False)
    max_enrollments = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    enrollment_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', db_index=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_courses')
    objects = CourseManager()
    class Meta:
        db_table = 'lms_courses'
        ordering = ['-created_at']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status', 'publish_date']),
        ]
    def __str__(self):
        return f"{self.code} - {self.title}"
    @property
    def is_full(self):
        if self.max_enrollments:
            return self.enrollment_count >= self.max_enrollments
        return False
