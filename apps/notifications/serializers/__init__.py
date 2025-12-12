"""
Notifications Serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import (
    Notification, NotificationTemplate, NotificationPreference,
    ScheduledNotification, NotificationLog
)

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification
    """
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    time_ago = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_name', 'sender', 'sender_name',
            'title', 'message', 'notification_type', 'action_url',
            'is_read', 'read_at', 'channels', 'metadata',
            'email_sent', 'sms_sent', 'push_sent',
            'expires_at', 'created_at', 'updated_at', 'time_ago'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'read_at']
    
    def get_time_ago(self, obj):
        """Get human readable time since creation"""
        from django.utils.timesince import timesince
        return timesince(obj.created_at)


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing notifications
    """
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_name', 'title',
            'notification_type', 'is_read', 'created_at'
        ]


class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating notifications
    """
    class Meta:
        model = Notification
        fields = [
            'recipient', 'sender', 'title', 'message',
            'notification_type', 'action_url', 'channels',
            'metadata', 'expires_at'
        ]
    
    def validate(self, attrs):
        """Validate notification data"""
        if not attrs.get('channels'):
            attrs['channels'] = ['in_app']
        return attrs


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationTemplate
    """
    class Meta:
        model = NotificationTemplate
        fields = [
            'id', 'name', 'code', 'description',
            'title_template', 'message_template',
            'notification_type', 'default_channels',
            'is_active', 'template_variables',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationPreference
    """
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'user', 'enable_email', 'enable_sms',
            'enable_push', 'enable_in_app', 'notification_types',
            'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end',
            'enable_daily_digest', 'daily_digest_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ScheduledNotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for ScheduledNotification
    """
    recipients_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = ScheduledNotification
        fields = [
            'id', 'title', 'message', 'notification_type',
            'recipients', 'recipients_count', 'recipient_groups',
            'scheduled_for', 'is_sent', 'sent_at',
            'channels', 'action_url', 'template', 'template_context',
            'is_recurring', 'recurrence_pattern', 'is_active',
            'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_sent', 'sent_at', 'created_at', 'updated_at']
    
    def get_recipients_count(self, obj):
        """Get count of recipients"""
        return obj.recipients.count()


class NotificationLogSerializer(serializers.ModelSerializer):
    """
    Serializer for NotificationLog
    """
    notification_title = serializers.CharField(source='notification.title', read_only=True)
    
    class Meta:
        model = NotificationLog
        fields = [
            'id', 'notification', 'notification_title', 'channel',
            'is_successful', 'error_message', 'metadata',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class BulkNotificationSerializer(serializers.Serializer):
    """
    Serializer for creating bulk notifications
    """
    recipients = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of user IDs"
    )
    title = serializers.CharField(max_length=255)
    message = serializers.CharField(style={'base_template': 'textarea.html'})
    notification_type = serializers.ChoiceField(
        choices=['info', 'success', 'warning', 'error', 'announcement', 'reminder'],
        default='info'
    )
    channels = serializers.ListField(
        child=serializers.CharField(),
        default=['in_app']
    )
    action_url = serializers.URLField(required=False, allow_blank=True)
    
    def validate_recipients(self, value):
        """Validate recipients exist"""
        users = User.objects.filter(id__in=value)
        if users.count() != len(value):
            raise serializers.ValidationError("Some users do not exist")
        return value
