import uuid
from django.db import models
from apps.core.models import TimeStampedModel

class AttendanceSession(TimeStampedModel):
    """
    Attendance session for a specific class/course
    """
    class SessionType(models.TextChoices):
        LECTURE = 'lecture', 'Lecture'
        LAB = 'lab', 'Laboratory'
        TUTORIAL = 'tutorial', 'Tutorial'
        SEMINAR = 'seminar', 'Seminar'
        EXAM = 'exam', 'Examination'
        OTHER = 'other', 'Other'
    
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='attendance_sessions'
    )
    title = models.CharField(max_length=255)
    session_type = models.CharField(
        max_length=20,
        choices=SessionType.choices,
        default=SessionType.LECTURE
    )
    date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        db_index=True
    )
    instructor = models.ForeignKey(
        'faculty.Faculty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_sessions'
    )
    room = models.CharField(max_length=100, blank=True)
    building = models.CharField(max_length=100, blank=True)
    total_students = models.IntegerField(default=0)
    present_count = models.IntegerField(default=0)
    absent_count = models.IntegerField(default=0)
    late_count = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    class Meta:
        db_table = 'attendance_sessions'
        ordering = ['-date', '-start_time']
        verbose_name = 'Attendance Session'
        verbose_name_plural = 'Attendance Sessions'
        indexes = [
            models.Index(fields=['course', 'date']),
            models.Index(fields=['date', 'status']),
        ]
    def __str__(self):
        return f"{self.course} - {self.title} ({self.date})"
    def update_counts(self):
        records = self.records.all()
        self.total_students = records.count()
        self.present_count = records.filter(status='present').count()
        self.absent_count = records.filter(status__in=['absent', 'sick_leave']).count()
        self.late_count = records.filter(status='late').count()
        self.save(update_fields=['total_students', 'present_count', 'absent_count', 'late_count'])
    def get_attendance_rate(self):
        if self.total_students == 0:
            return 0
        return round((self.present_count / self.total_students) * 100, 2)
