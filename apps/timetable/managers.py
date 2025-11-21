"""
Timetable Custom Managers and QuerySets
"""
from django.db import models


class TimetableEntryQuerySet(models.QuerySet):
    """Custom queryset for TimetableEntry"""
    
    def active(self):
        """Get only active entries"""
        return self.filter(is_active=True)
    
    def for_semester(self, semester):
        """Get entries for specific semester"""
        return self.filter(semester=semester, is_active=True)
    
    def for_course(self, course):
        """Get entries for specific course"""
        return self.filter(course=course, is_active=True)
    
    def for_instructor(self, instructor):
        """Get entries for specific instructor"""
        return self.filter(instructor=instructor, is_active=True)
    
    def for_room(self, room):
        """Get entries for specific room"""
        return self.filter(room=room, is_active=True)
    
    def for_day(self, day_of_week):
        """Get entries for specific day"""
        return self.filter(time_slot__day_of_week=day_of_week, is_active=True)


class TimetableEntryManager(models.Manager):
    """Custom manager for TimetableEntry"""
    
    def get_queryset(self):
        return TimetableEntryQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def for_semester(self, semester):
        return self.get_queryset().for_semester(semester)
    
    def for_course(self, course):
        return self.get_queryset().for_course(course)
    
    def for_instructor(self, instructor):
        return self.get_queryset().for_instructor(instructor)
    
    def for_room(self, room):
        return self.get_queryset().for_room(room)
    
    def for_day(self, day_of_week):
        return self.get_queryset().for_day(day_of_week)
