from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.core.models import TimeStampedModel
from ..managers import ExamManager

class Exam(TimeStampedModel):
    """
    Exams model with comprehensive fields
    """
    class Semester(models.TextChoices):
        FALL = 'fall', 'Fall'
        SPRING = 'spring', 'Spring'
        SUMMER = 'summer', 'Summer'
    
    class ExamType(models.TextChoices):
        MIDTERM = 'midterm', 'Midterm'
        FINAL = 'final', 'Final'
        QUIZ = 'quiz', 'Quiz'
        PRACTICAL = 'practical', 'Practical'
    
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', 'Scheduled'
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
    
    exam_code = models.CharField(max_length=20, unique=True)
    exam_name = models.CharField(max_length=200)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='exams'
    )
    academic_year = models.CharField(max_length=20, help_text="e.g., 2023-2024")
    semester = models.CharField(max_length=20, choices=Semester.choices)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    total_marks = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    passing_marks = models.IntegerField(default=40, validators=[MinValueValidator(0)])
    exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    room_number = models.CharField(max_length=20, blank=True)
    invigilator = models.ForeignKey(
        'faculty.Faculty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invigilated_exams'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED
    )
    instructions = models.TextField(blank=True, help_text="Special instructions for students")
    is_published = models.BooleanField(default=False, help_text="Whether results are published")
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='created_exams')
    
    objects = ExamManager()
    
    def clean(self):
        if self.passing_marks > self.total_marks:
            raise ValidationError("Passing marks cannot be greater than total marks")
    
    def is_passed(self, marks):
        return marks >= self.passing_marks
    
    def start_exam(self):
        self.status = Status.ONGOING
        self.save()
    
    def complete_exam(self):
        self.status = Status.COMPLETED
        self.save()
    
    def get_pass_percentage(self):
        results = self.results.all()
        if not results.exists():
            return 0
        passed = results.filter(marks_obtained__gte=self.passing_marks).count()
        return (passed / results.count()) * 100
    
    class Meta:
        db_table = 'exams'
        ordering = ['-exam_date', '-start_time']
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
        indexes = [
            models.Index(fields=['exam_code']),
            models.Index(fields=['status']),
            models.Index(fields=['exam_date']),
            models.Index(fields=['academic_year', 'semester']),
        ]
    
    def __str__(self):
        return f"{self.exam_code} - {self.exam_name}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('exams:detail', kwargs={'pk': self.pk})

