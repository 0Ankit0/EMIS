"""Faculty Award Serializer"""
from rest_framework import serializers
from ..models import FacultyAward


class FacultyAwardSerializer(serializers.ModelSerializer):
    """Serializer for FacultyAward"""
    
    class Meta:
        model = FacultyAward
        fields = ['id', 'title', 'awarding_body', 'date_received', 'description',
                  'category', 'certificate', 'created_at']
        read_only_fields = ['id', 'created_at']
