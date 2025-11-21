from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Dashboard, Widget, QuickLink, Announcement, AnnouncementView,
    StudentPortalProfile, FacultyPortalProfile, PortalActivity, PortalSettings
)

User = get_user_model()


class DashboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Dashboard
        fields = [
            'id', 'user', 'username', 'role', 'layout_config', 'theme_settings',
            'widget_preferences', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = [
            'id', 'name', 'widget_type', 'description', 'roles', 'default_config',
            'is_active', 'order', 'created_at'
        ]
        read_only_fields = ['created_at']


class QuickLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = [
            'id', 'title', 'url', 'description', 'icon', 'category', 'roles',
            'is_external', 'is_active', 'order', 'created_at'
        ]
        read_only_fields = ['created_at']


class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    is_active_now = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'author', 'author_name', 'priority',
            'target_roles', 'target_users', 'attachments', 'is_published',
            'publish_date', 'expiry_date', 'views_count', 'is_active_now',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['views_count', 'created_at', 'updated_at']
    
    def get_is_active_now(self, obj):
        return obj.is_active()


class AnnouncementViewSerializer(serializers.ModelSerializer):
    announcement_title = serializers.CharField(source='announcement.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = AnnouncementView
        fields = ['id', 'announcement', 'announcement_title', 'user', 'username', 'viewed_at']
        read_only_fields = ['viewed_at']


class StudentPortalProfileSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    registration_number = serializers.CharField(source='student.registration_number', read_only=True)
    
    class Meta:
        model = StudentPortalProfile
        fields = [
            'id', 'student', 'student_name', 'registration_number',
            'profile_picture', 'bio', 'preferences', 'emergency_contacts',
            'last_login', 'login_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['last_login', 'login_count', 'created_at', 'updated_at']


class FacultyPortalProfileSerializer(serializers.ModelSerializer):
    faculty_name = serializers.CharField(source='faculty.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='faculty.employee_id', read_only=True)
    
    class Meta:
        model = FacultyPortalProfile
        fields = [
            'id', 'faculty', 'faculty_name', 'employee_id',
            'profile_picture', 'bio', 'office_hours', 'consultation_settings',
            'preferences', 'last_login', 'login_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['last_login', 'login_count', 'created_at', 'updated_at']


class PortalActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = PortalActivity
        fields = [
            'id', 'user', 'username', 'activity_type', 'description',
            'metadata', 'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['created_at']


class PortalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalSettings
        fields = ['id', 'key', 'value', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
