"""
Admissions Serializers
"""
from rest_framework import serializers
from .models import Application, MeritList


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for Application
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'application_number', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'address_line1', 'address_line2', 'city',
            'state', 'postal_code', 'country', 'previous_school', 'previous_grade',
            'gpa', 'program', 'admission_year', 'admission_semester', 'status',
            'status_display', 'submitted_at', 'merit_score', 'rank',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'application_number', 'created_at', 'updated_at']
    
    def validate_email(self, value):
        """Validate email field"""
        if value:
            value = value.lower().strip()
        return value
    
    def validate_gpa(self, value):
        """Validate GPA field"""
        if value and (value < 0 or value > 4.0):
            raise serializers.ValidationError("GPA must be between 0.0 and 4.0")
        return value


class ApplicationListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing applications
    """
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Application
        fields = ['id', 'application_number', 'first_name', 'last_name', 'program', 'status', 'status_display', 'submitted_at']


class MeritListSerializer(serializers.ModelSerializer):
    """
    Serializer for MeritList
    """
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    
    class Meta:
        model = MeritList
        fields = [
            'id', 'name', 'program', 'admission_year', 'admission_semester',
            'generation_timestamp', 'generated_by', 'generated_by_name',
            'criteria', 'ranked_applications', 'total_applications',
            'version', 'is_published', 'published_at', 'cutoff_rank', 'cutoff_score',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'generation_timestamp', 'created_at', 'updated_at']
