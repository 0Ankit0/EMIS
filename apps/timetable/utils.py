"""
Timetable Utility Functions
"""
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, timedelta


def validate_time_slot(start_time, end_time):
    """
    Validate time slot
    
    Args:
        start_time: Start time
        end_time: End time
    
    Returns:
        bool: True if valid
    
    Raises:
        ValidationError: If validation fails
    """
    if start_time >= end_time:
        raise ValidationError("End time must be after start time")
    
    return True


def check_room_availability(room, time_slot, semester, exclude_entry=None):
    """
    Check if a room is available for a specific time slot
    
    Args:
        room: Room object
        time_slot: TimeSlot object
        semester: Semester object
        exclude_entry: TimetableEntry to exclude from check
    
    Returns:
        bool: True if available
    """
    from .models import TimetableEntry
    
    query = TimetableEntry.objects.filter(
        room=room,
        time_slot=time_slot,
        semester=semester,
        is_active=True
    )
    
    if exclude_entry:
        query = query.exclude(pk=exclude_entry.pk)
    
    return not query.exists()


def check_instructor_availability(instructor, time_slot, semester, exclude_entry=None):
    """
    Check if an instructor is available for a specific time slot
    
    Args:
        instructor: Faculty object
        time_slot: TimeSlot object
        semester: Semester object
        exclude_entry: TimetableEntry to exclude from check
    
    Returns:
        bool: True if available
    """
    from .models import TimetableEntry
    
    query = TimetableEntry.objects.filter(
        instructor=instructor,
        time_slot=time_slot,
        semester=semester,
        is_active=True
    )
    
    if exclude_entry:
        query = query.exclude(pk=exclude_entry.pk)
    
    return not query.exists()


def generate_timetable_report(entries_queryset):
    """
    Generate report for timetable entries
    
    Args:
        entries_queryset: QuerySet of TimetableEntry objects
    
    Returns:
        dict: Report data
    """
    total = entries_queryset.count()
    by_session_type = {}
    
    for entry in entries_queryset:
        session_type = entry.get_session_type_display()
        by_session_type[session_type] = by_session_type.get(session_type, 0) + 1
    
    return {
        'total': total,
        'by_session_type': by_session_type,
        'by_day': _count_by_day(entries_queryset),
    }


def _count_by_day(entries_queryset):
    """Count entries by day of week"""
    by_day = {}
    
    for i in range(7):
        day_name = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][i]
        count = entries_queryset.filter(time_slot__day_of_week=i).count()
        by_day[day_name] = count
    
    return by_day


def export_timetable_to_csv(entries_queryset):
    """
    Export timetable entries to CSV
    
    Args:
        entries_queryset: QuerySet of entries to export
    
    Returns:
        str: CSV data
    """
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Course Code', 'Course Title', 'Day', 'Time', 
        'Room', 'Instructor', 'Section', 'Type'
    ])
    
    # Write data
    for entry in entries_queryset:
        writer.writerow([
            entry.course.code,
            entry.course.title,
            entry.time_slot.get_day_of_week_display(),
            f"{entry.time_slot.start_time} - {entry.time_slot.end_time}",
            entry.room.name if entry.room else 'N/A',
            entry.instructor.get_full_name() if entry.instructor else 'N/A',
            entry.section or 'N/A',
            entry.get_session_type_display(),
        ])
    
    return output.getvalue()


def get_conflicts_for_entry(entry):
    """
    Get all conflicts for a timetable entry
    
    Args:
        entry: TimetableEntry object
    
    Returns:
        dict: Dictionary of conflicts
    """
    conflicts = {
        'room': [],
        'instructor': [],
    }
    
    # Check room conflicts
    if entry.room:
        room_available = check_room_availability(
            entry.room, entry.time_slot, entry.semester, exclude_entry=entry
        )
        if not room_available:
            conflicts['room'].append(f"Room {entry.room} is already booked")
    
    # Check instructor conflicts
    if entry.instructor:
        instructor_available = check_instructor_availability(
            entry.instructor, entry.time_slot, entry.semester, exclude_entry=entry
        )
        if not instructor_available:
            conflicts['instructor'].append(f"Instructor already has a class")
    
    return conflicts
