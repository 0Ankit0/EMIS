from rest_framework import serializers
from ..models import Enrollment, EnrollmentStatus
from .student import StudentResponseSerializer

class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'student', 'program', 'batch', 'section', 'semester', 'enrollment_date'
        ]

class EnrollmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'program', 'batch', 'section', 'semester', 'status', 'updated_by'
        ]
        extra_kwargs = {field: {'required': False} for field in fields}

class EnrollmentResponseSerializer(serializers.ModelSerializer):
    student = StudentResponseSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'ukid', 'student', 'program', 'batch', 'section', 'semester', 
            'enrollment_date', 'status', 'status_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['ukid', 'created_at', 'updated_at']