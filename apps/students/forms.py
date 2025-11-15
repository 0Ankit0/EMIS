"""
Student forms
"""
from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

from .models import Student, Gender


class StudentCreateForm(forms.ModelForm):
    """Form for creating a new student"""
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'nationality',
            'address', 'city', 'state', 'postal_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        """Ensure email is unique"""
        email = self.cleaned_data.get('email')
        if Student.objects.filter(email=email).exists():
            raise ValidationError("A student with this email already exists")
        return email
    
    def clean_date_of_birth(self):
        """Validate date of birth"""
        dob = self.cleaned_data.get('date_of_birth')
        if not dob:
            raise ValidationError("Date of birth is required")
        
        today = date.today()
        age = relativedelta(today, dob).years
        
        if age < 5:
            raise ValidationError("Student must be at least 5 years old")
        if age > 100:
            raise ValidationError("Invalid date of birth")
        
        return dob


class StudentUpdateForm(forms.ModelForm):
    """Form for updating student information"""
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'phone',
            'gender', 'nationality',
            'address', 'city', 'state', 'postal_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'current_gpa'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'current_gpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '4'}),
        }
    
    def clean_current_gpa(self):
        """Validate GPA"""
        gpa = self.cleaned_data.get('current_gpa')
        if gpa is not None and (gpa < 0 or gpa > 4.0):
            raise ValidationError("GPA must be between 0.0 and 4.0")
        return gpa
