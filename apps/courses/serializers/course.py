from rest_framework import serializers
from apps.courses.models import Course


class CourseCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a course"""
    
    class Meta:
        model = Course
        fields = [
            'title',
            'code',
            'description',
            'syllabus',
            'credits',
            'prerequisites',
            'status',
            'department',
            'semester',
            'academic_year',
        ]
    
    def validate_code(self, value):
        """Ensure course code is uppercase"""
        return value.upper()


class CourseUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a course"""
    
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'syllabus',
            'credits',
            'prerequisites',
            'status',
            'department',
            'semester',
            'academic_year',
        ]


class CourseResponseSerializer(serializers.ModelSerializer):
    """Serializer for course responses"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True, allow_null=True)
    module_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'code',
            'description',
            'syllabus',
            'credits',
            'prerequisites',
            'status',
            'created_by',
            'created_by_email',
            'department',
            'semester',
            'academic_year',
            'module_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_module_count(self, obj):
        """Return the number of modules in this course"""
        return obj.modules.count()
