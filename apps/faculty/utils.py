"""
Faculty Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal


def validate_faculty_employee_id(employee_id):
    """
    Validate faculty employee ID format
    
    Args:
        employee_id: Employee ID to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    if not employee_id:
        raise ValidationError("Employee ID is required")
    
    if len(employee_id) < 3:
        raise ValidationError("Employee ID must be at least 3 characters")
    
    return True


def calculate_faculty_experience(date_of_joining, date_of_leaving=None):
    """
    Calculate years of experience
    
    Args:
        date_of_joining: Joining date
        date_of_leaving: Leaving date (optional, uses today if None)
    
    Returns:
        float: Years of experience
    """
    if date_of_leaving:
        end_date = date_of_leaving
    else:
        end_date = timezone.now().date()
    
    delta = end_date - date_of_joining
    return round(delta.days / 365.25, 2)


def generate_faculty_report(queryset):
    """
    Generate report for faculty
    
    Args:
        queryset: QuerySet of faculty members
    
    Returns:
        dict: Report data
    """
    return {
        'total': queryset.count(),
        'active': queryset.filter(status='active').count(),
        'on_leave': queryset.filter(status='on_leave').count(),
        'teaching': queryset.filter(is_teaching=True).count(),
        'research_active': queryset.filter(is_research_active=True).count(),
    }


def export_faculty_to_csv(queryset):
    """
    Export faculty to CSV
    
    Args:
        queryset: QuerySet of faculty to export
    
    Returns:
        str: CSV data
    """
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Employee ID', 'Name', 'Email', 'Phone', 'Department',
        'Designation', 'Status', 'Date of Joining'
    ])
    
    # Write data
    for faculty in queryset:
        writer.writerow([
            faculty.employee_id,
            faculty.get_full_name(),
            faculty.official_email,
            faculty.phone,
            faculty.department.name if faculty.department else '',
            faculty.get_designation_display(),
            faculty.get_status_display(),
            faculty.date_of_joining.strftime('%Y-%m-%d')
        ])
    
    return output.getvalue()


def calculate_leave_balance(faculty, leave_type, year=None):
    """
    Calculate leave balance for faculty
    
    Args:
        faculty: Faculty instance
        leave_type: Type of leave
        year: Year to calculate for (default current year)
    
    Returns:
        dict: Leave balance information
    """
    from .models import FacultyLeave
    
    if year is None:
        year = timezone.now().year
    
    # Get approved leaves for the year
    approved_leaves = FacultyLeave.objects.filter(
        faculty=faculty,
        leave_type=leave_type,
        status='approved',
        start_date__year=year
    )
    
    total_days_taken = sum(leave.number_of_days for leave in approved_leaves)
    
    # Default leave entitlements (can be customized)
    entitlements = {
        'casual': 12,
        'sick': 12,
        'earned': 30,
        'maternity': 180,
        'paternity': 15,
    }
    
    entitled = entitlements.get(leave_type, 0)
    balance = entitled - total_days_taken
    
    return {
        'entitled': entitled,
        'taken': total_days_taken,
        'balance': balance
    }
