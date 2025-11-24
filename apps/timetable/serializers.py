"""Timetable Serializers"""
from rest_framework import serializers
from .models import AcademicYear, Semester, TimeSlot, Room, TimetableEntry, TimetableException


class AcademicYearSerializer(serializers.ModelSerializer):
    """Serializer for AcademicYear"""
    class Meta:
        model = AcademicYear
        fields = '__all__'


class SemesterSerializer(serializers.ModelSerializer):
    """Serializer for Semester"""
    class Meta:
        model = Semester
        fields = '__all__'


class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer for TimeSlot"""
    class Meta:
        model = TimeSlot
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room"""
    class Meta:
        model = Room
        fields = '__all__'


class TimetableEntrySerializer(serializers.ModelSerializer):
    """Serializer for TimetableEntry"""
    class Meta:
        model = TimetableEntry
        fields = '__all__'


class TimetableExceptionSerializer(serializers.ModelSerializer):
    """Serializer for TimetableException"""
    class Meta:
        model = TimetableException
        fields = '__all__'
