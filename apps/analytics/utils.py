"""
Analytics Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_analytics_data(data):
    """
    Validate analytics data
    
    Args:
        data: Dictionary of data to validate
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    if not data.get('name'):
        raise ValidationError("Name is required")
    
    return True


def generate_analytics_report(queryset):
    """
    Generate report for analytics items
    
    Args:
        queryset: QuerySet of items
    
    Returns:
        dict: Report data
    """
    return {
        'total': queryset.count(),
        'active': queryset.filter(status='active').count(),
        'inactive': queryset.filter(status='inactive').count(),
        'pending': queryset.filter(status='pending').count(),
    }


def export_analytics_to_csv(queryset):
    """
    Export analytics items to CSV
    
    Args:
        queryset: QuerySet of items to export
    
    Returns:
        str: CSV data
    """
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Name', 'Description', 'Status', 'Created At'])
    
    # Write data
    for item in queryset:
        writer.writerow([
            item.name,
            item.description,
            item.status,
            item.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return output.getvalue()
