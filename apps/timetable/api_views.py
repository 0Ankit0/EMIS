"""Timetable API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import AcademicYear, Semester, TimeSlot, Room, TimetableEntry, TimetableException
from .serializers import (
    AcademicYearSerializer, SemesterSerializer, TimeSlotSerializer,
    RoomSerializer, TimetableEntrySerializer, TimetableExceptionSerializer
)


class AcademicYearViewSet(viewsets.ModelViewSet):
    """ViewSet for Academic Years"""
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-start_date']


class SemesterViewSet(viewsets.ModelViewSet):
    """ViewSet for Semesters"""
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['academic_year', 'is_active']
    ordering = ['-start_date']


class TimeSlotViewSet(viewsets.ModelViewSet):
    """ViewSet for Time Slots"""
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['start_time']


class RoomViewSet(viewsets.ModelViewSet):
    """ViewSet for Rooms"""
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_available']
    search_fields = ['room_number', 'building']


class TimetableEntryViewSet(viewsets.ModelViewSet):
    """ViewSet for Timetable Entries"""
    queryset = TimetableEntry.objects.all()
    serializer_class = TimetableEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course', 'faculty', 'day_of_week', 'room']
    search_fields = ['course__name', 'faculty__user__first_name']
    ordering = ['day_of_week', 'time_slot__start_time']


class TimetableExceptionViewSet(viewsets.ModelViewSet):
    """ViewSet for Timetable Exceptions"""
    queryset = TimetableException.objects.all()
    serializer_class = TimetableExceptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['date', 'is_cancelled']
    ordering = ['-date']
