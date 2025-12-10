"""
Exams Serializers
"""
from rest_framework import serializers
from .models import Exam, ExamResult, ExamSchedule


class ExamSerializer(serializers.ModelSerializer):
    """
    Serializer for Exam
    """
    course_name = serializers.CharField(source='course.course_name', read_only=True)
    invigilator_name = serializers.CharField(source='invigilator.get_full_name', read_only=True)
    pass_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = [
            'id', 'exam_code', 'exam_name', 'course', 'course_name',
            'academic_year', 'semester', 'exam_date', 'start_time', 'end_time',
            'duration_minutes', 'total_marks', 'passing_marks', 'exam_type',
            'room_number', 'invigilator', 'invigilator_name', 'status',
            'instructions', 'is_published', 'pass_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_pass_percentage(self, obj):
        return obj.get_pass_percentage()
    
    def validate(self, data):
        if data.get('passing_marks', 0) > data.get('total_marks', 100):
            raise serializers.ValidationError("Passing marks cannot be greater than total marks")
        return data


class ExamListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing exams
    """
    course_name = serializers.CharField(source='course.course_name', read_only=True)
    
    class Meta:
        model = Exam
        fields = [
            'id', 'exam_code', 'exam_name', 'course_name',
            'exam_date', 'start_time', 'exam_type', 'status'
        ]


class ExamResultSerializer(serializers.ModelSerializer):
    """
    Serializer for ExamResult
    """
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    exam_code = serializers.CharField(source='exam.exam_code', read_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    student_roll_number = serializers.CharField(source='student.roll_number', read_only=True)
    percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = ExamResult
        fields = [
            'id', 'exam', 'exam_name', 'exam_code', 'student', 'student_name',
            'student_roll_number', 'marks_obtained', 'grade', 'percentage',
            'remarks', 'is_absent', 'is_passed', 'evaluated_by', 'evaluated_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'grade', 'is_passed', 'created_at', 'updated_at']
    
    def get_percentage(self, obj):
        return obj.get_percentage()
    
    def validate(self, data):
        exam = data.get('exam')
        marks_obtained = data.get('marks_obtained')
        is_absent = data.get('is_absent', False)
        
        if not is_absent and marks_obtained is not None and exam:
            if marks_obtained > exam.total_marks:
                raise serializers.ValidationError(
                    f"Marks obtained cannot be greater than total marks ({exam.total_marks})"
                )
        
        return data


class ExamResultListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing exam results
    """
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = ExamResult
        fields = ['id', 'student_name', 'marks_obtained', 'grade', 'is_passed']


class ExamScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for ExamSchedule
    """
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = ExamSchedule
        fields = [
            'id', 'name', 'description', 'academic_year', 'semester',
            'start_date', 'end_date', 'is_published',
            'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("End date must be after start date")
        return data
