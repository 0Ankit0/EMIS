"""Faculty Qualification Serializer"""
from rest_framework import serializers
from ..models import FacultyQualification


class FacultyQualificationSerializer(serializers.ModelSerializer):
    """Serializer for FacultyQualification"""
    
    class Meta:
        model = FacultyQualification
        fields = ['id', 'degree', 'degree_name', 'specialization', 'institution',
                  'university', 'year_of_passing', 'percentage_or_cgpa', 'grade_system',
                  'certificate', 'is_verified', 'created_at']
        read_only_fields = ['id', 'created_at']
