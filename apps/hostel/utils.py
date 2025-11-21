"""Hostel Utility Functions"""
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
import csv
from io import StringIO


def get_hostel_occupancy_stats(hostel):
    """Get detailed occupancy statistics for a hostel"""
    stats = {
        'total_capacity': hostel.total_capacity,
        'occupied': hostel.occupied_capacity,
        'available': hostel.available_capacity,
        'occupancy_rate': hostel.occupancy_percentage,
        'rooms': {
            'total': hostel.rooms.count(),
            'available': hostel.rooms.filter(status='available').count(),
            'occupied': hostel.rooms.filter(status='occupied').count(),
            'full': hostel.rooms.filter(status='full').count(),
            'maintenance': hostel.rooms.filter(status='maintenance').count(),
        },
        'by_room_type': {}
    }
    
    # Occupancy by room type
    from .models import Room
    for room_type, _ in Room.ROOM_TYPE_CHOICES:
        rooms = hostel.rooms.filter(room_type=room_type)
        total_capacity = rooms.aggregate(Sum('capacity'))['capacity__sum'] or 0
        occupied_beds = rooms.aggregate(Sum('occupied_beds'))['occupied_beds__sum'] or 0
        
        stats['by_room_type'][room_type] = {
            'total_capacity': total_capacity,
            'occupied': occupied_beds,
            'available': total_capacity - occupied_beds,
            'occupancy_rate': (occupied_beds / total_capacity * 100) if total_capacity > 0 else 0
        }
    
    return stats


def find_available_rooms(hostel, room_type=None, has_ac=None):
    """Find available rooms with optional filters"""
    from .models import Room
    
    rooms = Room.objects.filter(
        hostel=hostel,
        status='available',
        occupied_beds__lt=models.F('capacity')
    )
    
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    
    if has_ac is not None:
        rooms = rooms.filter(has_ac=has_ac)
    
    return rooms


def calculate_hostel_revenue(hostel, start_date=None, end_date=None):
    """Calculate hostel revenue from room allocations"""
    from .models import RoomAllocation
    
    allocations = RoomAllocation.objects.filter(
        room__hostel=hostel,
        status='active'
    )
    
    if start_date:
        allocations = allocations.filter(allocation_date__gte=start_date)
    if end_date:
        allocations = allocations.filter(allocation_date__lte=end_date)
    
    monthly_revenue = allocations.aggregate(Sum('monthly_rent'))['monthly_rent__sum'] or 0
    security_deposits = allocations.aggregate(Sum('security_deposit'))['security_deposit__sum'] or 0
    
    return {
        'monthly_rent_total': monthly_revenue,
        'security_deposits_total': security_deposits,
        'total_allocations': allocations.count(),
    }


def get_complaint_statistics(hostel=None, start_date=None, end_date=None):
    """Get complaint statistics"""
    from .models import Complaint
    
    complaints = Complaint.objects.all()
    
    if hostel:
        complaints = complaints.filter(hostel=hostel)
    
    if start_date:
        complaints = complaints.filter(submitted_date__gte=start_date)
    if end_date:
        complaints = complaints.filter(submitted_date__lte=end_date)
    
    stats = {
        'total': complaints.count(),
        'by_status': {},
        'by_category': {},
        'by_priority': {},
        'average_resolution_time': None,
    }
    
    # By status
    for status, _ in Complaint.STATUS_CHOICES:
        stats['by_status'][status] = complaints.filter(status=status).count()
    
    # By category
    for category, _ in Complaint.CATEGORY_CHOICES:
        stats['by_category'][category] = complaints.filter(category=category).count()
    
    # By priority
    for priority, _ in Complaint.PRIORITY_CHOICES:
        stats['by_priority'][priority] = complaints.filter(priority=priority).count()
    
    # Average resolution time
    resolved = complaints.filter(status='resolved', resolved_date__isnull=False)
    if resolved.exists():
        total_days = 0
        count = 0
        for complaint in resolved:
            if complaint.submitted_date and complaint.resolved_date:
                delta = complaint.resolved_date.date() - complaint.submitted_date.date()
                total_days += delta.days
                count += 1
        
        if count > 0:
            stats['average_resolution_time'] = total_days / count
    
    return stats


def get_student_attendance_summary(student, start_date=None, end_date=None):
    """Get attendance summary for a student"""
    from .models import Attendance
    
    attendance = Attendance.objects.filter(student=student)
    
    if start_date:
        attendance = attendance.filter(date__gte=start_date)
    if end_date:
        attendance = attendance.filter(date__lte=end_date)
    
    total_days = attendance.count()
    
    return {
        'total_days': total_days,
        'present': attendance.filter(status='present').count(),
        'absent': attendance.filter(status='absent').count(),
        'on_leave': attendance.filter(status='on_leave').count(),
        'attendance_percentage': (
            attendance.filter(status='present').count() / total_days * 100
            if total_days > 0 else 0
        )
    }


def check_room_availability(room):
    """Check if room has available beds"""
    return room.available_beds > 0 and room.status in ['available', 'occupied']


def generate_complaint_number():
    """Generate unique complaint number"""
    from .models import Complaint
    year = timezone.now().year
    count = Complaint.objects.filter(created_at__year=year).count() + 1
    return f"COMP-{year}-{count:06d}"


def export_hostel_data_csv(hostel):
    """Export hostel data to CSV"""
    output = StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Room Number', 'Room Type', 'Capacity', 'Occupied', 
                     'Available', 'Monthly Rent', 'Status'])
    
    # Rooms data
    for room in hostel.rooms.all():
        writer.writerow([
            room.room_number,
            room.get_room_type_display(),
            room.capacity,
            room.occupied_beds,
            room.available_beds,
            room.monthly_rent,
            room.get_status_display()
        ])
    
    return output.getvalue()


def export_allocations_csv(hostel=None):
    """Export room allocations to CSV"""
    from .models import RoomAllocation
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Student Email', 'Room Number', 'Hostel', 'Bed Number',
                     'Allocation Date', 'Monthly Rent', 'Status'])
    
    allocations = RoomAllocation.objects.filter(status='active')
    
    if hostel:
        allocations = allocations.filter(room__hostel=hostel)
    
    for allocation in allocations:
        writer.writerow([
            allocation.student.user.email,
            allocation.room.room_number,
            allocation.room.hostel.name,
            allocation.bed_number,
            allocation.allocation_date,
            allocation.monthly_rent,
            allocation.get_status_display()
        ])
    
    return output.getvalue()


def get_overdue_outing_requests():
    """Get outing requests that are overdue (student hasn't returned)"""
    from .models import OutingRequest
    
    today = timezone.now().date()
    
    overdue = OutingRequest.objects.filter(
        status='approved',
        expected_return_date__lt=today,
        actual_return_date__isnull=True
    )
    
    return overdue


def validate_room_allocation(student, room):
    """Validate if a room can be allocated to a student"""
    from .models import RoomAllocation
    
    # Check if student already has active allocation
    existing = RoomAllocation.objects.filter(
        student=student,
        status='active'
    ).exists()
    
    if existing:
        return False, "Student already has an active room allocation"
    
    # Check if room has availability
    if not check_room_availability(room):
        return False, "Room is not available"
    
    # Check gender compatibility (if hostel is gender-specific)
    hostel = room.hostel
    if hostel.hostel_type in ['boys', 'girls']:
        student_gender = student.gender if hasattr(student, 'gender') else None
        if hostel.hostel_type == 'boys' and student_gender != 'male':
            return False, "This is a boys' hostel"
        if hostel.hostel_type == 'girls' and student_gender != 'female':
            return False, "This is a girls' hostel"
    
    return True, None


from django.db import models

def send_complaint_notification(complaint):
    """Send notification for complaint status update"""
    # TODO: Implement email/SMS notification
    pass


def send_outing_approval_notification(outing_request):
    """Send notification for outing request approval/rejection"""
    # TODO: Implement email/SMS notification
    pass
