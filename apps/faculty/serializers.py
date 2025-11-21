"""
Faculty Serializers
"""
from rest_framework import serializers
from .models import (
    Department, Faculty, FacultyQualification, FacultyExperience,
    FacultyAttendance, FacultyLeave, FacultyPublication, FacultyAward
)


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department"""
    head_name = serializers.CharField(source='head.get_full_name', read_only=True)
    faculty_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = ['id', 'name', 'code', 'description', 'head', 'head_name', 
                  'is_active', 'faculty_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_faculty_count(self, obj):
        return obj.faculty_members.filter(status='active').count()


class FacultyQualificationSerializer(serializers.ModelSerializer):
    """Serializer for FacultyQualification"""
    
    class Meta:
        model = FacultyQualification
        fields = ['id', 'degree', 'degree_name', 'specialization', 'institution',
                  'university', 'year_of_passing', 'percentage_or_cgpa', 'grade_system',
                  'certificate', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at']


class FacultyExperienceSerializer(serializers.ModelSerializer):
    """Serializer for FacultyExperience"""
    duration_years = serializers.SerializerMethodField()
    
    class Meta:
        model = FacultyExperience
        fields = ['id', 'organization', 'designation', 'experience_type',
                  'start_date', 'end_date', 'is_current', 'responsibilities',
                  'location', 'certificate', 'duration_years', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_duration_years(self, obj):
        return round(obj.get_duration_years(), 2)


class FacultyPublicationSerializer(serializers.ModelSerializer):
    """Serializer for FacultyPublication"""
    
    class Meta:
        model = FacultyPublication
        fields = ['id', 'title', 'publication_type', 'authors', 'journal_or_conference',
                  'volume', 'issue', 'pages', 'year', 'doi', 'isbn_issn', 'url',
                  'abstract', 'keywords', 'citation_count', 'impact_factor',
                  'is_indexed', 'document', 'created_at']
        read_only_fields = ['id', 'created_at']


class FacultyAwardSerializer(serializers.ModelSerializer):
    """Serializer for FacultyAward"""
    
    class Meta:
        model = FacultyAward
        fields = ['id', 'title', 'awarding_body', 'date_received', 'description',
                  'category', 'certificate', 'created_at']
        read_only_fields = ['id', 'created_at']


class FacultyListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing faculty"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = Faculty
        fields = ['id', 'employee_id', 'full_name', 'official_email',
                  'department_name', 'designation', 'status', 'photo']
        read_only_fields = ['id']


class FacultyDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Faculty"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    experience_years = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    qualifications = FacultyQualificationSerializer(many=True, read_only=True)
    experiences = FacultyExperienceSerializer(many=True, read_only=True)
    publications = FacultyPublicationSerializer(many=True, read_only=True)
    awards = FacultyAwardSerializer(many=True, read_only=True)
    
    class Meta:
        model = Faculty
        fields = [
            'id', 'employee_id', 'first_name', 'middle_name', 'last_name', 'full_name',
            'phone', 'alternate_phone', 'personal_email', 'official_email',
            'date_of_birth', 'age', 'gender', 'blood_group', 'nationality', 'religion',
            'caste_category', 'aadhar_number', 'pan_number', 'passport_number',
            'current_address', 'permanent_address', 'city', 'state', 'pincode', 'country',
            'department', 'department_name', 'designation', 'specialization',
            'employment_type', 'date_of_joining', 'date_of_leaving', 'experience_years',
            'probation_period_months', 'is_probation_completed', 'confirmation_date',
            'status', 'is_teaching', 'is_research_active', 'is_hod',
            'basic_salary', 'grade_pay', 'pay_scale', 'bank_name', 
            'bank_account_number', 'ifsc_code',
            'max_weekly_hours', 'current_weekly_hours', 'research_interests',
            'publications_count', 'projects_count', 'photo', 'resume', 'id_proof',
            'linkedin_url', 'google_scholar_url', 'research_gate_url', 'orcid_id',
            'notes', 'qualifications', 'experiences', 'publications', 'awards',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'experience_years', 'age']
    
    def get_experience_years(self, obj):
        return round(obj.get_experience_years(), 2)
    
    def get_age(self, obj):
        return obj.get_age()


class FacultyCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Faculty"""
    
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
    
    def validate_employee_id(self, value):
        """Validate unique employee ID"""
        if self.instance:
            if Faculty.objects.exclude(pk=self.instance.pk).filter(employee_id=value).exists():
                raise serializers.ValidationError("Faculty with this employee ID already exists.")
        else:
            if Faculty.objects.filter(employee_id=value).exists():
                raise serializers.ValidationError("Faculty with this employee ID already exists.")
        return value
    
    def validate_official_email(self, value):
        """Validate unique official email"""
        if self.instance:
            if Faculty.objects.exclude(pk=self.instance.pk).filter(official_email=value).exists():
                raise serializers.ValidationError("Faculty with this official email already exists.")
        else:
            if Faculty.objects.filter(official_email=value).exists():
                raise serializers.ValidationError("Faculty with this official email already exists.")
        return value


class FacultyAttendanceSerializer(serializers.ModelSerializer):
    """Serializer for FacultyAttendance"""
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.get_full_name', read_only=True)
    
    class Meta:
        model = FacultyAttendance
        fields = ['id', 'faculty', 'faculty_name', 'date', 'status',
                  'check_in_time', 'check_out_time', 'working_hours', 'remarks',
                  'marked_by', 'marked_by_name', 'created_at']
        read_only_fields = ['id', 'created_at', 'marked_by']


class FacultyLeaveSerializer(serializers.ModelSerializer):
    """Serializer for FacultyLeave"""
    faculty_name = serializers.CharField(source='faculty.get_full_name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = FacultyLeave
        fields = ['id', 'faculty', 'faculty_name', 'leave_type', 'start_date',
                  'end_date', 'number_of_days', 'reason', 'status',
                  'approved_by', 'approved_by_name', 'approval_date',
                  'rejection_reason', 'supporting_document', 'created_at']
        read_only_fields = ['id', 'number_of_days', 'created_at', 'approved_by', 'approval_date']
    
    def validate(self, data):
        """Validate leave dates"""
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("End date must be after start date.")
        return data
