from django import forms
from django.contrib.auth import get_user_model
from .models import (
    Dashboard, Widget, QuickLink, Announcement,
    StudentPortalProfile, FacultyPortalProfile
)

User = get_user_model()


class DashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['role', 'layout_config', 'theme_settings', 'widget_preferences', 'is_active']
        widgets = {
            'layout_config': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'theme_settings': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'widget_preferences': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class WidgetForm(forms.ModelForm):
    class Meta:
        model = Widget
        fields = ['name', 'widget_type', 'description', 'roles', 'default_config', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'widget_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'roles': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': '["student", "faculty"]'}),
            'default_config': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class QuickLinkForm(forms.ModelForm):
    class Meta:
        model = QuickLink
        fields = ['title', 'url', 'description', 'icon', 'category', 'roles', 'is_external', 'is_active', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fa-home'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'roles': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': '["student"]'}),
            'is_external': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'title', 'content', 'priority', 'target_roles', 'target_users',
            'attachments', 'is_published', 'publish_date', 'expiry_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'target_roles': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': '["student", "faculty"]'}),
            'target_users': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'attachments': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'publish_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'expiry_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target_users'].required = False


class StudentPortalProfileForm(forms.ModelForm):
    class Meta:
        model = StudentPortalProfile
        fields = ['profile_picture', 'bio', 'preferences', 'emergency_contacts']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'preferences': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'emergency_contacts': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class FacultyPortalProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyPortalProfile
        fields = ['profile_picture', 'bio', 'office_hours', 'consultation_settings', 'preferences']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'office_hours': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'consultation_settings': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'preferences': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class ProfilePictureUploadForm(forms.Form):
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )


class ThemeSettingsForm(forms.Form):
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto'),
    ]
    
    theme = forms.ChoiceField(
        choices=THEME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    primary_color = forms.CharField(
        max_length=7,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'color'})
    )
