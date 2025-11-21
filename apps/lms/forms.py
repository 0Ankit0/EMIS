"""
LMS Forms
"""
from django import forms
from .models import (
    Course, Module, Lesson, Enrollment, Quiz, Question,
    Assignment, AssignmentSubmission, Discussion, DiscussionReply
)


class CourseForm(forms.ModelForm):
    """Form for creating and updating courses"""
    
    class Meta:
        model = Course
        fields = [
            'title', 'code', 'description', 'short_description',
            'category', 'difficulty_level', 'instructor',
            'thumbnail', 'intro_video', 'duration_hours',
            'prerequisites', 'learning_objectives',
            'price', 'is_free', 'max_enrollments',
            'start_date', 'end_date', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'prerequisites': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'learning_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_free': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'max_enrollments': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ModuleForm(forms.ModelForm):
    """Form for creating and updating modules"""
    
    class Meta:
        model = Module
        fields = ['course', 'title', 'description', 'order', 'duration_minutes', 'is_published']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class LessonForm(forms.ModelForm):
    """Form for creating and updating lessons"""
    
    class Meta:
        model = Lesson
        fields = [
            'module', 'title', 'content_type', 'description',
            'order', 'duration_minutes', 'text_content',
            'video_url', 'video_file', 'pdf_file',
            'is_preview', 'is_published'
        ]
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'text_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'is_preview': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuizForm(forms.ModelForm):
    """Form for creating and updating quizzes"""
    
    class Meta:
        model = Quiz
        fields = [
            'lesson', 'title', 'description', 'passing_score',
            'max_attempts', 'time_limit_minutes', 'is_mandatory',
            'show_correct_answers', 'randomize_questions'
        ]
        widgets = {
            'lesson': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'passing_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_attempts': forms.NumberInput(attrs={'class': 'form-control'}),
            'time_limit_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_mandatory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_correct_answers': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'randomize_questions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class QuestionForm(forms.ModelForm):
    """Form for creating and updating questions"""
    
    class Meta:
        model = Question
        fields = ['quiz', 'question_text', 'question_type', 'points', 'order', 'options', 'correct_answer', 'explanation']
        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'correct_answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class AssignmentForm(forms.ModelForm):
    """Form for creating and updating assignments"""
    
    class Meta:
        model = Assignment
        fields = [
            'lesson', 'title', 'description', 'instructions',
            'max_points', 'due_date', 'allow_late_submission',
            'late_penalty_percentage', 'attachment'
        ]
        widgets = {
            'lesson': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'max_points': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'allow_late_submission': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'late_penalty_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AssignmentSubmissionForm(forms.ModelForm):
    """Form for student assignment submissions"""
    
    class Meta:
        model = AssignmentSubmission
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


class DiscussionForm(forms.ModelForm):
    """Form for creating discussions"""
    
    class Meta:
        model = Discussion
        fields = ['course', 'lesson', 'title', 'content']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'lesson': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class DiscussionReplyForm(forms.ModelForm):
    """Form for replying to discussions"""
    
    class Meta:
        model = DiscussionReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class EnrollmentForm(forms.ModelForm):
    """Form for course enrollment"""
    
    class Meta:
        model = Enrollment
        fields = ['course', 'student']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-control'}),
            'student': forms.Select(attrs={'class': 'form-control'}),
        }
