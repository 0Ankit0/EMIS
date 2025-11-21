"""
Timetable Models
"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel
from django.core.exceptions import ValidationError

User = get_user_model()


class AcademicYear(TimeStampedModel):
    """Academic Year model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True, help_text="e.g., 2024-2025")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        db_table = 'academic_years'
        ordering = ['-start_date']
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Set all other academic years to inactive
            AcademicYear.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class Semester(TimeStampedModel):
    """Semester model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=50, help_text="e.g., Fall 2024, Spring 2025")
    semester_number = models.IntegerField(help_text="1, 2, 3, etc.")
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        db_table = 'semesters'
        ordering = ['-start_date']
        unique_together = [['academic_year', 'semester_number']]
        
    def __str__(self):
        return f"{self.name} ({self.academic_year})"
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Set all other semesters to inactive
            Semester.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class TimeSlot(TimeStampedModel):
    """Time slot for classes"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text="e.g., Period 1, Morning Slot")
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.IntegerField(
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ],
        db_index=True
    )
    is_active = models.BooleanField(default=True, db_index=True)
    
    class Meta:
        db_table = 'time_slots'
        ordering = ['day_of_week', 'start_time']
        unique_together = [['day_of_week', 'start_time', 'end_time']]
        
    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")


class Room(TimeStampedModel):
    """Classroom or room model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Room 101, Lab A")
    room_number = models.CharField(max_length=50, blank=True)
    building = models.CharField(max_length=100, blank=True)
    capacity = models.IntegerField(default=0, help_text="Maximum number of students")
    room_type = models.CharField(
        max_length=50,
        choices=[
            ('classroom', 'Classroom'),
            ('lab', 'Laboratory'),
            ('lecture_hall', 'Lecture Hall'),
            ('seminar', 'Seminar Room'),
            ('auditorium', 'Auditorium'),
            ('other', 'Other'),
        ],
        default='classroom',
        db_index=True
    )
    facilities = models.TextField(blank=True, help_text="Available facilities (projector, computers, etc.)")
    is_active = models.BooleanField(default=True, db_index=True)
    
    class Meta:
        db_table = 'rooms'
        ordering = ['building', 'name']
        
    def __str__(self):
        if self.building:
            return f"{self.building} - {self.name}"
        return self.name


class TimetableEntry(TimeStampedModel):
    """Main timetable entry linking all components"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='timetable_entries')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='timetable_entries')
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='timetable_entries')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetable_entries')
    instructor = models.ForeignKey(
        'faculty.Faculty', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='timetable_entries'
    )
    
    # Optional: For section-specific classes
    section = models.CharField(max_length=10, blank=True, help_text="e.g., A, B, CS-1")
    batch = models.CharField(max_length=50, blank=True, help_text="e.g., 2024, 2024-Spring")
    
    # Session details
    session_type = models.CharField(
        max_length=50,
        choices=[
            ('lecture', 'Lecture'),
            ('tutorial', 'Tutorial'),
            ('lab', 'Laboratory'),
            ('seminar', 'Seminar'),
            ('practical', 'Practical'),
            ('other', 'Other'),
        ],
        default='lecture',
        db_index=True
    )
    
    # Recurrence settings
    is_recurring = models.BooleanField(default=True, help_text="Repeats weekly")
    start_date = models.DateField(help_text="When this entry starts")
    end_date = models.DateField(null=True, blank=True, help_text="When this entry ends (optional)")
    
    # Status
    is_active = models.BooleanField(default=True, db_index=True)
    notes = models.TextField(blank=True)
    
    # Metadata
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_timetable_entries'
    )
    
    class Meta:
        db_table = 'timetable_entries'
        ordering = ['time_slot__day_of_week', 'time_slot__start_time']
        indexes = [
            models.Index(fields=['semester', 'is_active']),
            models.Index(fields=['course', 'semester']),
            models.Index(fields=['instructor', 'semester']),
            models.Index(fields=['room', 'time_slot']),
        ]
        
    def __str__(self):
        return f"{self.course.code} - {self.time_slot} - {self.room}"
    
    def clean(self):
        """Validate timetable entry for conflicts"""
        if not self.pk:  # Only check for new entries
            # Check room conflict
            if self.room:
                room_conflict = TimetableEntry.objects.filter(
                    semester=self.semester,
                    time_slot=self.time_slot,
                    room=self.room,
                    is_active=True
                ).exclude(pk=self.pk).exists()
                
                if room_conflict:
                    raise ValidationError(f"Room {self.room} is already booked for this time slot")
            
            # Check instructor conflict
            if self.instructor:
                instructor_conflict = TimetableEntry.objects.filter(
                    semester=self.semester,
                    time_slot=self.time_slot,
                    instructor=self.instructor,
                    is_active=True
                ).exclude(pk=self.pk).exists()
                
                if instructor_conflict:
                    raise ValidationError(f"Instructor {self.instructor} already has a class at this time")


class TimetableException(TimeStampedModel):
    """Exceptions to regular timetable (holidays, makeup classes, etc.)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timetable_entry = models.ForeignKey(
        TimetableEntry, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='exceptions'
    )
    date = models.DateField(db_index=True)
    exception_type = models.CharField(
        max_length=50,
        choices=[
            ('cancelled', 'Class Cancelled'),
            ('rescheduled', 'Rescheduled'),
            ('makeup', 'Makeup Class'),
            ('holiday', 'Holiday'),
            ('exam', 'Examination'),
            ('event', 'Special Event'),
        ],
        db_index=True
    )
    reason = models.TextField(blank=True)
    
    # If rescheduled or makeup
    new_time_slot = models.ForeignKey(
        TimeSlot, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='exception_slots'
    )
    new_room = models.ForeignKey(
        Room, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='exception_rooms'
    )
    
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='created_timetable_exceptions'
    )
    
    class Meta:
        db_table = 'timetable_exceptions'
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.get_exception_type_display()} - {self.date}"
