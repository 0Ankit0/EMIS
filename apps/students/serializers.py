"""
Student serializers for API
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, StudentStatus, Gender

User = get_user_model()


class StudentListSerializer(serializers.ModelSerializer):
    """Serializer for student list view (lightweight)"""
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_number', 'full_name', 'email', 
            'status', 'status_display', 'age', 'created_at'
        ]
        read_only_fields = ['id', 'student_number', 'created_at']


class StudentDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed student view"""
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_graduated = serializers.BooleanField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    updated_by_name = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_number', 'first_name', 'middle_name', 'last_name',
            'full_name', 'email', 'phone', 'date_of_birth', 'age',
            'gender', 'gender_display', 'nationality',
            'address', 'city', 'state', 'postal_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone', 
            'emergency_contact_relationship',
            'status', 'status_display', 'is_active', 'is_graduated',
            'admission_date', 'graduation_date', 'degree_earned', 'honors',
            'current_gpa', 'user',
            'created_at', 'updated_at', 'created_by', 'updated_by',
            'created_by_name', 'updated_by_name'
        ]
        read_only_fields = [
            'id', 'student_number', 'created_at', 'updated_at',
            'created_by', 'updated_by'
        ]


class StudentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new student"""
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'nationality',
            'address', 'city', 'state', 'postal_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship'
        ]
    
    def validate_email(self, value):
        """Ensure email is unique"""
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("Student with this email already exists")
        return value
    
    def validate_date_of_birth(self, value):
        """Validate date of birth"""
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        today = date.today()
        age = relativedelta(today, value).years
        
        if age < 5:
            raise serializers.ValidationError("Student must be at least 5 years old")
        if age > 100:
            raise serializers.ValidationError("Invalid date of birth")
        
        return value


class StudentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating student information"""
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'middle_name', 'last_name', 'phone',
            'gender', 'nationality',
            'address', 'city', 'state', 'postal_code', 'country',
            'emergency_contact_name', 'emergency_contact_phone',
            'emergency_contact_relationship', 'current_gpa'
        ]
    
    def validate_current_gpa(self, value):
        """Validate GPA is between 0 and 4.0"""
        if value is not None and (value < 0 or value > 4.0):
            raise serializers.ValidationError("GPA must be between 0.0 and 4.0")
        return value


class AdmissionSerializer(serializers.Serializer):
    """Serializer for student admission"""
    admission_date = serializers.DateTimeField(required=False, allow_null=True)
    
    def validate(self, data):
        """Validate admission request"""
        student = self.context.get('student')
        if student.status != StudentStatus.APPLICANT:
            raise serializers.ValidationError("Only applicants can be admitted")
        return data


class GraduationSerializer(serializers.Serializer):
    """Serializer for student graduation"""
    graduation_date = serializers.DateTimeField(required=False, allow_null=True)
    degree_earned = serializers.CharField(max_length=200, required=False)
    honors = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    def validate(self, data):
        """Validate graduation request"""
        student = self.context.get('student')
        if student.status != StudentStatus.ACTIVE:
            raise serializers.ValidationError("Only active students can graduate")
        return data


class StatusChangeSerializer(serializers.Serializer):
    """Serializer for status changes (suspend, withdraw)"""
    action = serializers.ChoiceField(
        choices=['suspend', 'withdraw', 'make_alumni']
    )
    reason = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate(self, data):
        """Validate status change"""
        student = self.context.get('student')
        action = data['action']
        
        if action == 'suspend' and student.status != StudentStatus.ACTIVE:
            raise serializers.ValidationError("Only active students can be suspended")
        
        if action == 'withdraw' and student.status not in [StudentStatus.ACTIVE, StudentStatus.SUSPENDED]:
            raise serializers.ValidationError("Only active or suspended students can be withdrawn")
        
        if action == 'make_alumni' and student.status != StudentStatus.GRADUATED:
            raise serializers.ValidationError("Only graduated students can become alumni")
        
        return data


class StudentBulkUploadSerializer(serializers.Serializer):
    """Serializer for bulk student upload"""
    file = serializers.FileField()
    
    def validate_file(self, value):
        """Validate uploaded file"""
        if not value.name.endswith(('.csv', '.xlsx', '.xls')):
            raise serializers.ValidationError(
                "Invalid file format. Please upload CSV or Excel file."
            )
        return value
