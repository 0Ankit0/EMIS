"""
Portal API Serializers
"""
from rest_framework import serializers
from ..models import (
    Dashboard, Widget, QuickLink, Announcement, AnnouncementView,
    StudentPortalProfile, FacultyPortalProfile, PortalActivity, PortalSettings
)


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = '__all__'


class QuickLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuickLink
        fields = '__all__'


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementView
        fields = '__all__'


class StudentPortalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPortalProfile
        fields = '__all__'


class FacultyPortalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyPortalProfile
        fields = '__all__'


class PortalActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalActivity
        fields = '__all__'


class PortalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortalSettings
        fields = '__all__'
