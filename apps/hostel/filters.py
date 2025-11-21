"""Hostel Filters"""
import django_filters
from .models import (
    Hostel, Room, RoomAllocation, Complaint, OutingRequest, Attendance
)


class HostelFilter(django_filters.FilterSet):
    hostel_type = django_filters.ChoiceFilter(choices=Hostel.HOSTEL_TYPE_CHOICES)
    status = django_filters.ChoiceFilter(choices=Hostel.STATUS_CHOICES)
    
    class Meta:
        model = Hostel
        fields = ['hostel_type', 'status', 'is_active']


class RoomFilter(django_filters.FilterSet):
    room_type = django_filters.ChoiceFilter(choices=Room.ROOM_TYPE_CHOICES)
    status = django_filters.ChoiceFilter(choices=Room.STATUS_CHOICES)
    monthly_rent = django_filters.RangeFilter()
    
    class Meta:
        model = Room
        fields = ['hostel', 'floor', 'room_type', 'status', 'has_ac']


class RoomAllocationFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=RoomAllocation.STATUS_CHOICES)
    allocation_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = RoomAllocation
        fields = ['student', 'room', 'status', 'academic_year']


class ComplaintFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(choices=Complaint.CATEGORY_CHOICES)
    priority = django_filters.ChoiceFilter(choices=Complaint.PRIORITY_CHOICES)
    status = django_filters.ChoiceFilter(choices=Complaint.STATUS_CHOICES)
    submitted_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Complaint
        fields = ['hostel', 'student', 'category', 'priority', 'status']


class OutingRequestFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=OutingRequest.STATUS_CHOICES)
    out_date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = OutingRequest
        fields = ['student', 'hostel', 'status']


class AttendanceFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Attendance.STATUS_CHOICES)
    date = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = Attendance
        fields = ['hostel', 'student', 'status', 'date']
