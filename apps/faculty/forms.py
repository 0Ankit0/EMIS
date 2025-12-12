"""
Faculty Forms
"""
from django import forms
from .models import (
    Department, Faculty, FacultyQualification, FacultyExperience,
    FacultyAttendance, FacultyLeave, FacultyPublication, FacultyAward
)


class DepartmentForm(forms.ModelForm):
    """Form for Department"""
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter department name'
            }),
            'code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter department code'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter description',
                'rows': 4
            }),
            'head': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
        }


class FacultyForm(forms.ModelForm):
    """Form for Faculty"""
    class Meta:
        model = Faculty
        fields = [
            'employee_id', 'first_name', 'middle_name', 'last_name',
            'phone', 'alternate_phone', 'personal_email', 'official_email',
            'date_of_birth', 'gender', 'blood_group', 'nationality', 'religion',
            'caste_category', 'aadhar_number', 'pan_number', 'passport_number',
            'current_address', 'permanent_address', 'city', 'state', 'pincode', 'country',
            'department', 'designation', 'specialization', 'employment_type',
            'date_of_joining', 'date_of_leaving', 'probation_period_months',
            'is_probation_completed', 'confirmation_date', 'status', 'is_teaching',
            'is_research_active', 'is_hod', 'basic_salary', 'grade_pay', 'pay_scale',
            'bank_name', 'bank_account_number', 'ifsc_code', 'max_weekly_hours',
            'research_interests', 'photo', 'resume', 'id_proof',
            'linkedin_url', 'google_scholar_url', 'research_gate_url', 'orcid_id', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_of_leaving': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'confirmation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'current_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'permanent_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'research_interests': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class FacultyQualificationForm(forms.ModelForm):
    """Form for Faculty Qualification"""
    class Meta:
        model = FacultyQualification
        fields = ['faculty', 'degree', 'degree_name', 'specialization', 'institution',
                  'university', 'year_of_passing', 'percentage_or_cgpa', 'grade_system',
                  'certificate', 'is_verified']
        widgets = {
            'degree_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'institution': forms.TextInput(attrs={'class': 'form-control'}),
            'university': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FacultyExperienceForm(forms.ModelForm):
    """Form for Faculty Experience"""
    class Meta:
        model = FacultyExperience
        fields = ['faculty', 'organization', 'designation', 'experience_type',
                  'start_date', 'end_date', 'is_current', 'responsibilities',
                  'location', 'certificate']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'responsibilities': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class FacultyAttendanceForm(forms.ModelForm):
    """Form for Faculty Attendance"""
    class Meta:
        model = FacultyAttendance
        fields = ['faculty', 'date', 'status', 'check_in_time', 'check_out_time',
                  'working_hours', 'remarks']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_in_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


class FacultyLeaveForm(forms.ModelForm):
    """Form for Faculty Leave"""
    class Meta:
        model = FacultyLeave
        fields = ['faculty', 'leave_type', 'start_date', 'end_date', 'reason',
                  'supporting_document']
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
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data


class FacultyPublicationForm(forms.ModelForm):
    """Form for Faculty Publication"""
    class Meta:
        model = FacultyPublication
        fields = ['faculty', 'title', 'publication_type', 'authors', 'journal_or_conference',
                  'volume', 'issue', 'pages', 'year', 'doi', 'isbn_issn', 'url',
                  'abstract', 'keywords', 'citation_count', 'impact_factor',
                  'is_indexed', 'document']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'authors': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'abstract': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class FacultyAwardForm(forms.ModelForm):
    """Form for Faculty Award"""
    class Meta:
        model = FacultyAward
        fields = ['faculty', 'title', 'awarding_body', 'date_received',
                  'description', 'category', 'certificate']
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


class BulkAttendanceForm(forms.Form):
    """Form for marking bulk attendance"""
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    status = forms.ChoiceField(
        choices=FacultyAttendance.Status.choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    faculty_ids = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['faculty_ids'].choices = [
            (f.id, f.get_full_name()) 
            for f in Faculty.objects.filter(status='active')
        ]

