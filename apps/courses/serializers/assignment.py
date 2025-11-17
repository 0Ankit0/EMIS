from rest_framework import serializers
from apps.courses.models import Assignment


class AssignmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating an assignment"""
    
    class Meta:
        model = Assignment
        fields = [
            'course',
            'title',
            'description',
            'instructions',
            'max_score',
            'grading_rubric',
            'due_date',
            'available_from',
            'late_submission_allowed',
            'late_penalty_percentage',
            'assignment_type',
            'is_published',
        ]


class AssignmentResponseSerializer(serializers.ModelSerializer):
    """Serializer for assignment responses"""
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    submission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = [
            'id',
            'course',
            'course_code',
            'course_title',
            'title',
            'description',
            'instructions',
            'max_score',
            'grading_rubric',
            'due_date',
            'available_from',
            'late_submission_allowed',
            'late_penalty_percentage',
            'assignment_type',
            'is_published',
            'is_overdue',
            'submission_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_submission_count(self, obj):
        """Return the number of submissions for this assignment"""
        return obj.submissions.count()
