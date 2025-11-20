"""
Admissions Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_application_data(data):
    """
    Validate application data
    
    Args:
        data: Dictionary of data to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    required_fields = ['first_name', 'last_name', 'email', 'program']
    for field in required_fields:
        if not data.get(field):
            raise ValidationError(f"{field.replace('_', ' ').title()} is required")
    
    return True


def generate_admissions_report(queryset):
    """
    Generate report for applications
    
    Args:
        queryset: QuerySet of applications
    
    Returns:
        dict: Report data
    """
    from .models import Application
    
    report = {
        'total': queryset.count(),
        'by_status': {}
    }
    
    for status_code, status_name in Application.STATUS_CHOICES:
        report['by_status'][status_name] = queryset.filter(status=status_code).count()
    
    return report


def export_admissions_to_csv(queryset):
    """
    Export applications to CSV
    
    Args:
        queryset: QuerySet of applications to export
    
    Returns:
        str: CSV data
    """
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Application Number', 'First Name', 'Last Name', 'Email', 'Phone',
        'Program', 'Admission Year', 'Semester', 'Status', 'Submitted At', 'Merit Score'
    ])
    
    # Write data
    for app in queryset:
        writer.writerow([
            app.application_number,
            app.first_name,
            app.last_name,
            app.email,
            app.phone,
            app.program,
            app.admission_year,
            app.admission_semester,
            app.get_status_display(),
            app.submitted_at.strftime('%Y-%m-%d %H:%M') if app.submitted_at else '',
            app.merit_score or ''
        ])
    
    return output.getvalue()


def calculate_merit_score(application):
    """
    Calculate merit score for an application
    
    Args:
        application: Application instance
    
    Returns:
        float: Calculated merit score
    """
    score = 0.0
    
    # GPA contribution (40%)
    if application.gpa:
        score += (application.gpa / 4.0) * 40
    
    # Additional scoring logic can be added here
    
    return round(score, 2)
