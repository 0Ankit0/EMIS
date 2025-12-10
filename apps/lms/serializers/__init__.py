"""
LMS Serializers
"""
from rest_framework import serializers
from .models import (
    Course, Module, Lesson, Enrollment, LessonProgress,
    Quiz, Question, QuizAttempt, QuizAnswer,
    Assignment, AssignmentSubmission, Discussion, DiscussionReply, Certificate
)


class CourseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for course listing"""
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'code', 'title', 'short_description', 'category',
            'difficulty_level', 'instructor_name', 'duration_hours',
            'price', 'is_free', 'status', 'enrollment_count', 'thumbnail'
        ]


class CourseDetailSerializer(serializers.ModelSerializer):
    """Detailed course serializer"""
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    modules_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
    
    def get_modules_count(self, obj):
        return obj.modules.count()


class ModuleSerializer(serializers.ModelSerializer):
    """Module serializer"""
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Module
        fields = '__all__'
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    """Lesson serializer"""
    
    class Meta:
        model = Lesson
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    """Enrollment serializer"""
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ['enrollment_date', 'completion_date', 'progress_percentage']


class LessonProgressSerializer(serializers.ModelSerializer):
    """Lesson progress serializer"""
    
    class Meta:
        model = LessonProgress
        fields = '__all__'


class QuizSerializer(serializers.ModelSerializer):
    """Quiz serializer"""
    questions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = '__all__'
    
    def get_questions_count(self, obj):
        return obj.questions.count()


class QuestionSerializer(serializers.ModelSerializer):
    """Question serializer"""
    
    class Meta:
        model = Question
        fields = '__all__'


class QuizAttemptSerializer(serializers.ModelSerializer):
    """Quiz attempt serializer"""
    
    class Meta:
        model = QuizAttempt
        fields = '__all__'
        read_only_fields = ['started_at', 'submitted_at', 'score', 'passed']


class QuizAnswerSerializer(serializers.ModelSerializer):
    """Quiz answer serializer"""
    
    class Meta:
        model = QuizAnswer
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    """Assignment serializer"""
    
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    """Assignment submission serializer"""
    student_name = serializers.CharField(source='enrollment.student.user.get_full_name', read_only=True)
    
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'
        read_only_fields = ['submission_date', 'is_late', 'graded_by', 'graded_at']


class DiscussionSerializer(serializers.ModelSerializer):
    """Discussion serializer"""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Discussion
        fields = '__all__'
    
    def get_replies_count(self, obj):
        return obj.replies.count()


class DiscussionReplySerializer(serializers.ModelSerializer):
    """Discussion reply serializer"""
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = DiscussionReply
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):
    """Certificate serializer"""
    student_name = serializers.CharField(source='enrollment.student.user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='enrollment.course.title', read_only=True)
    
    class Meta:
        model = Certificate
        fields = '__all__'
