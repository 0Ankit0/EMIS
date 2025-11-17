from rest_framework import serializers
from apps.courses.models import Submission


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a submission"""
    
    class Meta:
        model = Submission
        fields = [
            'assignment',
            'student',
            'content',
            'files',
        ]


class SubmissionResponseSerializer(serializers.ModelSerializer):
    """Serializer for submission responses"""
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    student_email = serializers.EmailField(source='student.user.email', read_only=True)
    student_name = serializers.SerializerMethodField()
    graded_by_email = serializers.EmailField(source='graded_by.email', read_only=True, allow_null=True)
    
    class Meta:
        model = Submission
        fields = [
            'id',
            'assignment',
            'assignment_title',
            'student',
            'student_email',
            'student_name',
            'submitted_at',
            'content',
            'files',
            'grade_status',
            'score',
            'feedback',
            'graded_at',
            'graded_by',
            'graded_by_email',
            'is_late',
            'late_penalty_applied',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'submitted_at',
            'is_late',
            'late_penalty_applied',
            'created_at',
            'updated_at',
        ]
    
    def get_student_name(self, obj):
        """Return student's full name if available"""
        if hasattr(obj.student.user, 'first_name') and hasattr(obj.student.user, 'last_name'):
            return f"{obj.student.user.first_name} {obj.student.user.last_name}".strip() or obj.student.user.email
        return obj.student.user.email
