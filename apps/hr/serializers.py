"""HR Serializers"""
from rest_framework import serializers
from .models import (
    Department, Designation, Employee, Attendance, Leave, Payroll,
    JobPosting, JobApplication, PerformanceReview, Training, TrainingParticipant
)


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department"""
    head_name = serializers.CharField(source='head.get_full_name', read_only=True)
    employee_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_employee_count(self, obj):
        return obj.employees.filter(status='active').count()


class DesignationSerializer(serializers.ModelSerializer):
    """Serializer for Designation"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Designation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing employees"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_title = serializers.CharField(source='designation.title', read_only=True)
    
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'phone',
                  'department_name', 'designation_title', 'status', 'photo']
        read_only_fields = ['id']


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Employee"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_title = serializers.CharField(source='designation.title', read_only=True)
    age = serializers.IntegerField(source='get_age', read_only=True)
    gross_salary = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    experience_years = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Employee"""
    
    class Meta:
        model = Employee
        exclude = ['created_at', 'updated_at', 'created_by']
    
    def validate_employee_id(self, value):
        """Validate unique employee ID"""
        if self.instance:
            if Employee.objects.exclude(pk=self.instance.pk).filter(employee_id=value).exists():
                raise serializers.ValidationError("Employee with this ID already exists.")
        else:
            if Employee.objects.filter(employee_id=value).exists():
                raise serializers.ValidationError("Employee with this ID already exists.")
        return value


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance"""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    marked_by_name = serializers.CharField(source='marked_by.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LeaveSerializer(serializers.ModelSerializer):
    """Serializer for Leave"""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    
    class Meta:
        model = Leave
        fields = '__all__'
        read_only_fields = ['id', 'number_of_days', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate leave dates"""
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError("End date must be after start date")
        return data


class PayrollSerializer(serializers.ModelSerializer):
    """Serializer for Payroll"""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True)
    
    class Meta:
        model = Payroll
        fields = '__all__'
        read_only_fields = ['id', 'gross_salary', 'total_deductions', 'net_salary', 'created_at', 'updated_at']


class JobPostingSerializer(serializers.ModelSerializer):
    """Serializer for JobPosting"""
    department_name = serializers.CharField(source='department.name', read_only=True)
    designation_title = serializers.CharField(source='designation.title', read_only=True)
    posted_by_name = serializers.CharField(source='posted_by.get_full_name', read_only=True)
    applications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = JobPosting
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_applications_count(self, obj):
        return obj.applications.count()


class JobApplicationSerializer(serializers.ModelSerializer):
    """Serializer for JobApplication"""
    job_title = serializers.CharField(source='job_posting.title', read_only=True)
    job_code = serializers.CharField(source='job_posting.job_code', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['id', 'application_date', 'created_at', 'updated_at']


class PerformanceReviewSerializer(serializers.ModelSerializer):
    """Serializer for PerformanceReview"""
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    
    class Meta:
        model = PerformanceReview
        fields = '__all__'
        read_only_fields = ['id', 'overall_rating', 'created_at', 'updated_at']


class TrainingSerializer(serializers.ModelSerializer):
    """Serializer for Training"""
    organized_by_name = serializers.CharField(source='organized_by.get_full_name', read_only=True)
    participants_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Training
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_participants_count(self, obj):
        return obj.participants.count()


class TrainingParticipantSerializer(serializers.ModelSerializer):
    """Serializer for TrainingParticipant"""
    training_title = serializers.CharField(source='training.title', read_only=True)
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    
    class Meta:
        model = TrainingParticipant
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
