"""Faculty Experience Serializer"""
from rest_framework import serializers
from ..models import FacultyExperience


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
