"""HR Forms"""
from django import forms
from .models import (
    Department, Designation, Employee, Attendance, Leave, Payroll,
    JobPosting, JobApplication, PerformanceReview, Training, TrainingParticipant
)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head', 'parent_department', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = ['title', 'code', 'description', 'level', 'department',
                  'min_salary', 'max_salary', 'required_qualifications',
                  'responsibilities', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'required_qualifications': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'middle_name', 'last_name',
            'date_of_birth', 'gender', 'marital_status', 'blood_group',
            'phone', 'alternate_phone', 'email', 'personal_email',
            'current_address', 'permanent_address', 'city', 'state', 'pincode', 'country',
            'aadhar_number', 'pan_number', 'passport_number',
            'department', 'designation', 'employment_type',
            'date_of_joining', 'probation_period_months', 'reporting_manager',
            'basic_salary', 'hra', 'da', 'other_allowances',
            'bank_name', 'bank_account_number', 'ifsc_code',
            'photo', 'resume', 'id_proof',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'current_address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'check_in_time', 'check_out_time', 'working_hours', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason', 'supporting_document']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError("End date must be after start date")
        
        return cleaned_data


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee', 'month', 'year',
            'basic_salary', 'hra', 'da', 'other_allowances', 'overtime_pay', 'bonus',
            'pf', 'esi', 'professional_tax', 'tds', 'loan_deduction', 'other_deductions',
            'working_days', 'present_days', 'leave_days',
            'status', 'payment_date', 'payment_method', 'transaction_reference', 'remarks'
        ]
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title', 'job_code', 'department', 'designation', 'employment_type',
            'vacancies', 'description', 'requirements', 'responsibilities',
            'min_experience_years', 'max_experience_years',
            'min_salary', 'max_salary', 'location',
            'posted_date', 'closing_date', 'status'
        ]
        widgets = {
            'posted_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'closing_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'requirements': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'job_posting', 'first_name', 'last_name', 'email', 'phone',
            'current_location', 'total_experience_years',
            'current_company', 'current_designation', 'current_salary', 'expected_salary',
            'notice_period_days', 'resume', 'cover_letter'
        ]
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }


class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'review_type', 'review_period_start', 'review_period_end',
            'technical_skills', 'communication', 'teamwork', 'leadership',
            'punctuality', 'quality_of_work',
            'strengths', 'areas_of_improvement', 'achievements', 'goals_for_next_period',
            'comments', 'status'
        ]
        widgets = {
            'review_period_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'review_period_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'strengths': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'areas_of_improvement': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'achievements': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'goals_for_next_period': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = [
            'title', 'code', 'description', 'trainer_name', 'trainer_organization',
            'start_date', 'end_date', 'duration_hours', 'location', 'capacity',
            'cost_per_participant', 'status'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class TrainingParticipantForm(forms.ModelForm):
    class Meta:
        model = TrainingParticipant
        fields = ['training', 'employee', 'status', 'attendance_percentage', 'assessment_score', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
