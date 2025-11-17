from rest_framework import serializers
from apps.courses.models import GradeRecord


class GradeRecordCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a grade record"""
    
    class Meta:
        model = GradeRecord
        fields = [
            'course',
            'student',
            'grade_value',
            'comments',
            'semester',
            'academic_year',
        ]
    
    def validate_grade_value(self, value):
        """Ensure grade value is between 0 and 100"""
        if value < 0 or value > 100:
            raise serializers.ValidationError("Grade value must be between 0 and 100")
        return value


class GradeRecordResponseSerializer(serializers.ModelSerializer):
    """Serializer for grade record responses"""
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    student_email = serializers.EmailField(source='student.user.email', read_only=True)
    student_name = serializers.SerializerMethodField()
    finalized_by_email = serializers.EmailField(source='finalized_by.email', read_only=True, allow_null=True)
    
    class Meta:
        model = GradeRecord
        fields = [
            'id',
            'course',
            'course_code',
            'course_title',
            'student',
            'student_email',
            'student_name',
            'grade_value',
            'grade_letter',
            'grade_points',
            'finalized',
            'finalized_at',
            'finalized_by',
            'finalized_by_email',
            'comments',
            'semester',
            'academic_year',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'grade_letter',
            'grade_points',
            'created_at',
            'updated_at',
        ]
    
    def get_student_name(self, obj):
        """Return student's full name if available"""
        if hasattr(obj.student.user, 'first_name') and hasattr(obj.student.user, 'last_name'):
            return f"{obj.student.user.first_name} {obj.student.user.last_name}".strip() or obj.student.user.email
        return obj.student.user.email
