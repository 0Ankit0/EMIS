"""
Notifications Forms
"""
from django import forms
from django.contrib.auth import get_user_model
from .models import (
    Notification, NotificationTemplate, NotificationPreference,
    ScheduledNotification, NotificationType, NotificationChannel
)

User = get_user_model()


class NotificationForm(forms.ModelForm):
    """Form for creating notifications"""
    
    class Meta:
        model = Notification
        fields = [
            'recipient', 'title', 'message', 'notification_type',
            'action_url', 'channels', 'expires_at'
        ]
        widgets = {
            'recipient': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Notification title'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Notification message',
                'rows': 4
            }),
            'notification_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'action_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'https://example.com/action'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'datetime-local'
            }),
        }


class BulkNotificationForm(forms.Form):
    """Form for sending bulk notifications"""
    
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600'
        }),
        required=True
    )
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Notification title'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Notification message',
            'rows': 4
        })
    )
    
    notification_type = forms.ChoiceField(
        choices=NotificationType.choices,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
        })
    )
    
    channels = forms.MultipleChoiceField(
        choices=NotificationChannel.choices,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600'
        }),
        initial=['in_app']
    )
    
    action_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
            'placeholder': 'https://example.com/action'
        })
    )


class NotificationTemplateForm(forms.ModelForm):
    """Form for notification templates"""
    
    class Meta:
        model = NotificationTemplate
        fields = [
            'name', 'code', 'description', 'title_template',
            'message_template', 'notification_type', 'default_channels',
            'is_active', 'template_variables'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Template name'
            }),
            'code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'template-code'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 2
            }),
            'title_template': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Hello {{ user.first_name }}'
            }),
            'message_template': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Your {{ item }} is ready.',
                'rows': 4
            }),
            'notification_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
        }


class NotificationPreferenceForm(forms.ModelForm):
    """Form for user notification preferences"""
    
    class Meta:
        model = NotificationPreference
        fields = [
            'enable_email', 'enable_sms', 'enable_push', 'enable_in_app',
            'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end',
            'enable_daily_digest', 'daily_digest_time'
        ]
        widgets = {
            'enable_email': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
            'enable_sms': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
            'enable_push': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
            'enable_in_app': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
            'quiet_hours_enabled': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
            'quiet_hours_start': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'time'
            }),
            'quiet_hours_end': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'time'
            }),
            'enable_daily_digest': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
            'daily_digest_time': forms.TimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'time'
            }),
        }


class ScheduledNotificationForm(forms.ModelForm):
    """Form for scheduled notifications"""
    
    class Meta:
        model = ScheduledNotification
        fields = [
            'title', 'message', 'notification_type', 'recipients',
            'scheduled_for', 'channels', 'action_url', 'template',
            'is_recurring', 'recurrence_pattern', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Notification title'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 4
            }),
            'notification_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'recipients': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
            'scheduled_for': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'type': 'datetime-local'
            }),
            'action_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'template': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'is_recurring': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
            'recurrence_pattern': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-blue-600'
            }),
        }
