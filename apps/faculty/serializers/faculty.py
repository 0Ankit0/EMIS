"""Faculty Serializers"""
from rest_framework import serializers
from ..models import Faculty
from .qualification import FacultyQualificationSerializer
from .experience import FacultyExperienceSerializer
from .publication import FacultyPublicationSerializer
from .award import FacultyAwardSerializer


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
