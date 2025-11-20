"""
Attendance Utility Functions
"""
from datetime import timedelta
from django.db.models import Count, Q


def calculate_attendance_percentage(student, course=None, start_date=None, end_date=None):
    """Calculate attendance percentage for a student"""
    from .models import AttendanceRecord
    
    records = AttendanceRecord.objects.filter(student=student)
    
    if course:
        records = records.filter(course=course)
    if start_date:
        records = records.filter(date__gte=start_date)
    if end_date:
        records = records.filter(date__lte=end_date)
    
    total = records.count()
    if total == 0:
        return 0
    
    present = records.filter(status='present').count()
    return round((present / total) * 100, 2)


def get_low_attendance_students(threshold=75, course=None):
    """Get students with attendance below threshold"""
    from .models import AttendanceRecord
    from apps.students.models import Student
    
    students = Student.objects.all()
    low_attendance = []
    
    for student in students:
        percentage = calculate_attendance_percentage(student, course)
        if percentage < threshold:
            low_attendance.append({
                'student': student,
                'percentage': percentage
            })
    
    return low_attendance


def generate_attendance_report_data(filters):
    """Generate attendance report data based on filters"""
    from .models import AttendanceRecord
    
    records = AttendanceRecord.objects.all()
    
    # Apply filters
    if 'course' in filters:
        records = records.filter(course_id=filters['course'])
    if 'start_date' in filters:
        records = records.filter(date__gte=filters['start_date'])
    if 'end_date' in filters:
        records = records.filter(date__lte=filters['end_date'])
    
    # Calculate statistics
    total = records.count()
    by_status = records.values('status').annotate(count=Count('id'))
    
    return {
        'total_records': total,
        'by_status': list(by_status),
        'records': list(records.values())
    }
