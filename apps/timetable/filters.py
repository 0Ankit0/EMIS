"""
Timetable Filters
"""
import django_filters
from .models import TimetableEntry, Room, TimeSlot


class TimetableEntryFilter(django_filters.FilterSet):
    """Filter for Timetable Entry"""
    course_code = django_filters.CharFilter(field_name='course__code', lookup_expr='icontains')
    course_title = django_filters.CharFilter(field_name='course__title', lookup_expr='icontains')
    section = django_filters.CharFilter(lookup_expr='icontains')
    batch = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = TimetableEntry
        fields = ['semester', 'session_type', 'room', 'instructor', 'is_active', 'is_recurring']


class RoomFilter(django_filters.FilterSet):
    """Filter for Room"""
    name = django_filters.CharFilter(lookup_expr='icontains')
    building = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Room
        fields = ['room_type', 'is_active', 'building']


class TimeSlotFilter(django_filters.FilterSet):
    """Filter for Time Slot"""
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = TimeSlot
        fields = ['day_of_week', 'is_active']
