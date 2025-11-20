"""
Attendance Forms
"""
from django import forms
from .models import AttendanceRecord, AttendanceSession, AttendancePolicy, AttendanceReport


class AttendanceRecordForm(forms.ModelForm):
    """
    Form for creating and updating attendance records
    """
    class Meta:
        model = AttendanceRecord
        fields = ['student', 'course', 'session', 'date', 'status', 'time_in', 'time_out', 'remarks', 'leave_document']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'course': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'session': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'time_in': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'time_out': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Additional notes...'
            }),
            'leave_document': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
        }


class AttendanceSessionForm(forms.ModelForm):
    """
    Form for creating and updating attendance sessions
    """
    class Meta:
        model = AttendanceSession
        fields = [
            'course', 'title', 'session_type', 'date', 'start_time', 'end_time',
            'status', 'instructor', 'room', 'building', 'notes'
        ]
        widgets = {
            'course': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Session Title'
            }),
            'session_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'instructor': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'room': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Room Number'
            }),
            'building': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Building Name'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Session notes...'
            }),
        }


class AttendancePolicyForm(forms.ModelForm):
    """
    Form for managing attendance policies
    """
    class Meta:
        model = AttendancePolicy
        fields = [
            'name', 'description', 'minimum_percentage', 'grace_period_days',
            'warning_threshold', 'penalty_threshold', 'applies_to_program',
            'applies_to_year', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Policy Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'rows': 3
            }),
            'minimum_percentage': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '75.00',
                'step': '0.01'
            }),
            'grace_period_days': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '0'
            }),
            'warning_threshold': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '80.00',
                'step': '0.01'
            }),
            'penalty_threshold': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '70.00',
                'step': '0.01'
            }),
            'applies_to_program': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Program Name'
            }),
            'applies_to_year': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Year'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 rounded focus:ring-blue-500'
            }),
        }


class BulkAttendanceForm(forms.Form):
    """
    Form for bulk marking attendance
    """
    def __init__(self, *args, **kwargs):
        self.session = kwargs.pop('session', None)
        students = kwargs.pop('students', [])
        super().__init__(*args, **kwargs)
        
        # Create a field for each student
        for student in students:
            field_name = f'student_{student.id}'
            self.fields[field_name] = forms.ChoiceField(
                choices=AttendanceRecord.STATUS_CHOICES,
                initial='present',
                widget=forms.Select(attrs={
                    'class': 'px-3 py-1 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
                }),
                label=str(student)
            )
    
    def clean(self):
        cleaned_data = super().clean()
        attendance_data = {}
        
        for field_name, value in cleaned_data.items():
            if field_name.startswith('student_'):
                student_id = field_name.replace('student_', '')
                attendance_data[student_id] = value
        
        cleaned_data['attendance_data'] = attendance_data
        return cleaned_data


class AttendanceReportForm(forms.ModelForm):
    """
    Form for generating attendance reports
    """
    class Meta:
        model = AttendanceReport
        fields = ['title', 'report_type', 'format', 'start_date', 'end_date', 'filters']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Report Title'
            }),
            'report_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'format': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'filters': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 font-mono',
                'rows': 4,
                'placeholder': '{"program": "Computer Science", "status": "present"}'
            }),
        }
