"""
Courses Forms
"""
from django import forms
from .models import Course, Module, Assignment


class CourseForm(forms.ModelForm):
    """
    Form for creating and updating courses
    """
    class Meta:
        model = Course
        fields = ['title', 'code', 'description', 'syllabus', 'credits', 'department', 'semester', 'academic_year', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter course title'
            }),
            'code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter course code'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter description',
                'rows': 3
            }),
            'syllabus': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter syllabus',
                'rows': 5
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'department': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'academic_year': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
        }
    
    def clean_code(self):
        """Validate code field"""
        code = self.cleaned_data.get('code')
        if code:
            code = code.strip().upper()
            if len(code) < 3:
                raise forms.ValidationError("Code must be at least 3 characters long")
        return code


class ModuleForm(forms.ModelForm):
    """Form for creating and updating modules"""
    class Meta:
        model = Module
        fields = ['course', 'title', 'description', 'sequence_order', 'content', 'content_type', 'duration_minutes', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'sequence_order': forms.NumberInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5}),
            'content_type': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-input'}),
        }


class AssignmentForm(forms.ModelForm):
    """Form for creating and updating assignments"""
    class Meta:
        model = Assignment
        fields = ['course', 'title', 'description', 'instructions', 'due_date', 'max_score', 
                  'assignment_type', 'late_submission_allowed', 'late_penalty_percentage', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'instructions': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-input', 'type': 'datetime-local'}),
            'max_score': forms.NumberInput(attrs={'class': 'form-input'}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'late_penalty_percentage': forms.NumberInput(attrs={'class': 'form-input'}),
        }

