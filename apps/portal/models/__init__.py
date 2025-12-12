from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from apps.students.models import Student
from apps.faculty.models import Faculty
from apps.courses.models import Course
from apps.lms.models import Enrollment

User = get_user_model()


class Dashboard(models.Model):
    """Base dashboard configuration"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
        ('parent', 'Parent'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='portal_dashboard')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    layout_config = models.JSONField(default=dict, blank=True)
    theme_settings = models.JSONField(default=dict, blank=True)
    widget_preferences = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portal_dashboards'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.role} Dashboard"


class Widget(models.Model):
    """Dashboard widgets"""
    WIDGET_TYPE_CHOICES = [
        ('attendance', 'Attendance Summary'),
        ('grades', 'Grades Overview'),
        ('announcements', 'Announcements'),
        ('schedule', 'Class Schedule'),
        ('assignments', 'Assignments'),
        ('fees', 'Fee Status'),
        ('notifications', 'Notifications'),
        ('calendar', 'Calendar'),
        ('performance', 'Performance Chart'),
        ('quick_links', 'Quick Links'),
    ]
    
    name = models.CharField(max_length=100)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPE_CHOICES)
    description = models.TextField(blank=True)
    roles = models.JSONField(default=list)
    default_config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portal_widgets'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class QuickLink(models.Model):
    """Quick access links for portal"""
    CATEGORY_CHOICES = [
        ('academic', 'Academic'),
        ('administrative', 'Administrative'),
        ('services', 'Services'),
        ('resources', 'Resources'),
    ]
    
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    roles = models.JSONField(default=list)
    is_external = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portal_quick_links'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Announcement(models.Model):
    """Portal announcements"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='portal_announcements')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    target_roles = models.JSONField(default=list)
    target_users = models.ManyToManyField(User, blank=True, related_name='targeted_announcements')
    attachments = models.JSONField(default=list, blank=True)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portal_announcements'
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title

    def is_active(self):
        now = timezone.now()
        if not self.is_published:
            return False
        if self.publish_date and self.publish_date > now:
            return False
        if self.expiry_date and self.expiry_date < now:
            return False
        return True


class AnnouncementView(models.Model):
    """Track announcement views"""
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portal_announcement_views'
        unique_together = ['announcement', 'user']

    def __str__(self):
        return f"{self.user.username} viewed {self.announcement.title}"


class StudentPortalProfile(models.Model):
    """Extended student portal profile"""
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='portal_profile')
    profile_picture = models.ImageField(upload_to='portal/students/', null=True, blank=True)
    bio = models.TextField(blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    emergency_contacts = models.JSONField(default=list, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portal_student_profiles'

    def __str__(self):
        return f"Portal Profile - {self.student}"


class FacultyPortalProfile(models.Model):
    """Extended faculty portal profile"""
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE, related_name='portal_profile')
    profile_picture = models.ImageField(upload_to='portal/faculty/', null=True, blank=True)
    bio = models.TextField(blank=True)
    office_hours = models.JSONField(default=list, blank=True)
    consultation_settings = models.JSONField(default=dict, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    login_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portal_faculty_profiles'

    def __str__(self):
        return f"Portal Profile - {self.faculty}"


class PortalActivity(models.Model):
    """Track user portal activities"""
    ACTIVITY_TYPE_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view_page', 'View Page'),
        ('download', 'Download'),
        ('upload', 'Upload'),
        ('submit', 'Submit'),
        ('update', 'Update'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portal_activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'portal_activities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['activity_type']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.created_at}"


class PortalSettings(models.Model):
    """Global portal settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'portal_settings'
        verbose_name_plural = 'Portal Settings'

    def __str__(self):
        return self.key
