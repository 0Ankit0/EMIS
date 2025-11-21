"""
Exams Models
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.core.models import TimeStampedModel
from .managers import ExamManager, ExamResultManager

User = get_user_model()


class Exam(TimeStampedModel):
    """
    Exams model with comprehensive fields
    """

    # Exam Information
    exam_code = models.CharField(max_length=20, unique=True)
    exam_name = models.CharField(max_length=200)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='exams'
    )
    academic_year = models.CharField(max_length=20, help_text="e.g., 2023-2024")
    semester = models.CharField(
        max_length=20,
        choices=[
            ('fall', 'Fall'),
            ('spring', 'Spring'),
            ('summer', 'Summer'),
        ]
    )
    
    # Schedule
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Details
    total_marks = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    passing_marks = models.IntegerField(default=40, validators=[MinValueValidator(0)])
    exam_type = models.CharField(
        max_length=20,
        choices=[
            ('midterm', 'Midterm'),
            ('final', 'Final'),
            ('quiz', 'Quiz'),
            ('practical', 'Practical'),
        ]
    )
    
    # Location
    room_number = models.CharField(max_length=20, blank=True)
    invigilator = models.ForeignKey(
        'faculty.Faculty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='invigilated_exams'
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('ongoing', 'Ongoing'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='scheduled'
    )
    
    # Additional fields
    instructions = models.TextField(blank=True, help_text="Special instructions for students")
    is_published = models.BooleanField(default=False, help_text="Whether results are published")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_exams')
    
    objects = ExamManager()
    
    def clean(self):
        if self.passing_marks > self.total_marks:
            raise ValidationError("Passing marks cannot be greater than total marks")
    
    def is_passed(self, marks):
        return marks >= self.passing_marks
    
    def start_exam(self):
        self.status = 'ongoing'
        self.save()
    
    def complete_exam(self):
        self.status = 'completed'
        self.save()
    
    def get_pass_percentage(self):
        """Calculate pass percentage for this exam"""
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


class ExamResult(TimeStampedModel):
    """
    Individual exam results for students
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    grade = models.CharField(
        max_length=2,
        choices=[
            ('A+', 'A+'),
            ('A', 'A'),
            ('B+', 'B+'),
            ('B', 'B'),
            ('C+', 'C+'),
            ('C', 'C'),
            ('D', 'D'),
            ('F', 'F'),
        ],
        blank=True
    )
    remarks = models.TextField(blank=True)
    is_absent = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)
    evaluated_by = models.ForeignKey(
        'faculty.Faculty',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluated_results'
    )
    evaluated_at = models.DateTimeField(null=True, blank=True)
    
    objects = ExamResultManager()
    
    class Meta:
        db_table = 'exam_results'
        ordering = ['-exam__exam_date', 'student__first_name']
        verbose_name = 'Exam Result'
        verbose_name_plural = 'Exam Results'
        unique_together = ['exam', 'student']
        indexes = [
            models.Index(fields=['exam', 'student']),
            models.Index(fields=['grade']),
            models.Index(fields=['is_passed']),
        ]
    
    def __str__(self):
        return f"{self.student} - {self.exam.exam_code} - {self.marks_obtained}/{self.exam.total_marks}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate grade and pass status
        if not self.is_absent:
            self.is_passed = self.marks_obtained >= self.exam.passing_marks
            self.grade = self.calculate_grade()
        super().save(*args, **kwargs)
    
    def calculate_grade(self):
        """Calculate grade based on marks obtained"""
        percentage = (float(self.marks_obtained) / self.exam.total_marks) * 100
        
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B+'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C+'
        elif percentage >= 40:
            return 'C'
        elif percentage >= 33:
            return 'D'
        else:
            return 'F'
    
    def get_percentage(self):
        """Get percentage scored"""
        if self.is_absent:
            return 0
        return (float(self.marks_obtained) / self.exam.total_marks) * 100


class ExamSchedule(TimeStampedModel):
    """
    Exam schedule for organizing multiple exams
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    academic_year = models.CharField(max_length=20)
    semester = models.CharField(
        max_length=20,
        choices=[
            ('fall', 'Fall'),
            ('spring', 'Spring'),
            ('summer', 'Summer'),
        ]
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'exam_schedules'
        ordering = ['-start_date']
        verbose_name = 'Exam Schedule'
        verbose_name_plural = 'Exam Schedules'
    
    def __str__(self):
        return f"{self.name} - {self.academic_year} ({self.semester})"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('exams:schedule_detail', kwargs={'pk': self.pk})
