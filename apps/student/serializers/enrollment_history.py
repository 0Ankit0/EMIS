from rest_framework import serializers
from ..models import EnrollmentHistory, EnrollmentStatus
from .student import StudentResponseSerializer
from .enrollment import EnrollmentResponseSerializer

class EnrollmentHistoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentHistory
        fields = ['enrollment', 'student', 'semester', 'previous_status', 'new_status']

class EnrollmentHistoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentHistory
        fields = ['semester', 'previous_status', 'new_status', 'updated_by']
        extra_kwargs = {field: {'required': False} for field in fields}

class EnrollmentHistoryResponseSerializer(serializers.ModelSerializer):
    student = StudentResponseSerializer(read_only=True)
    enrollment = EnrollmentResponseSerializer(read_only=True)
    previous_status_display = serializers.CharField(source='get_previous_status_display', read_only=True)
    new_status_display = serializers.CharField(source='get_new_status_display', read_only=True)
    
    class Meta:
        model = EnrollmentHistory
        fields = [
            'ukid', 'enrollment', 'student', 'semester', 'previous_status', 
            'previous_status_display', 'new_status', 'new_status_display', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['ukid', 'created_at', 'updated_at']