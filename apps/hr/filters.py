"""HR Filters"""
import django_filters
from .models import Employee, Attendance, Leave, Payroll, JobPosting, JobApplication


class EmployeeFilter(django_filters.FilterSet):
    employment_type = django_filters.ChoiceFilter(choices=Employee.EMPLOYMENT_TYPE_CHOICES)
    status = django_filters.ChoiceFilter(choices=Employee.STATUS_CHOICES)
    date_of_joining = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Employee
        fields = ['department', 'designation', 'employment_type', 'status']


class AttendanceFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Attendance.STATUS_CHOICES)
    date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Attendance
        fields = ['employee', 'status', 'date']


class LeaveFilter(django_filters.FilterSet):
    leave_type = django_filters.ChoiceFilter(choices=Leave.LEAVE_TYPE_CHOICES)
    status = django_filters.ChoiceFilter(choices=Leave.STATUS_CHOICES)
    start_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Leave
        fields = ['employee', 'leave_type', 'status']


class PayrollFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Payroll.STATUS_CHOICES)
    
    class Meta:
        model = Payroll
        fields = ['employee', 'month', 'year', 'status']


class JobPostingFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=JobPosting.STATUS_CHOICES)
    employment_type = django_filters.ChoiceFilter(choices=JobPosting.EMPLOYMENT_TYPE_CHOICES)
    
    class Meta:
        model = JobPosting
        fields = ['department', 'designation', 'employment_type', 'status']


class JobApplicationFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=JobApplication.STATUS_CHOICES)
    
    class Meta:
        model = JobApplication
        fields = ['job_posting', 'status']
