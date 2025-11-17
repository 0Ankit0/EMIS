from rest_framework import serializers
from apps.courses.models import Module


class ModuleCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a module"""
    
    class Meta:
        model = Module
        fields = [
            'course',
            'title',
            'description',
            'sequence_order',
            'content',
            'content_type',
            'duration_minutes',
            'is_published',
        ]


class ModuleResponseSerializer(serializers.ModelSerializer):
    """Serializer for module responses"""
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Module
        fields = [
            'id',
            'course',
            'course_code',
            'course_title',
            'title',
            'description',
            'sequence_order',
            'content',
            'content_type',
            'duration_minutes',
            'is_published',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
