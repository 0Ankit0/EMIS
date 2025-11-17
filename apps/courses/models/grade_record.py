from django.db import models
from apps.core.models import TimeStampedModel


class GradeRecord(TimeStampedModel):
    GRADE_LETTER_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('B-', 'B-'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('C-', 'C-'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
        ('W', 'Withdrawn'),
        ('P', 'Pass'),
        ('NP', 'No Pass'),
    ]

    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='grade_records'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='grade_records'
    )
    
    # Grading information
    grade_value = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Numeric grade (e.g., 85.50)"
    )
    grade_letter = models.CharField(
        max_length=2,
        choices=GRADE_LETTER_CHOICES,
        blank=True
    )
    grade_points = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text="Grade points for GPA calculation (e.g., 4.00)"
    )
    
    # Status
    finalized = models.BooleanField(default=False)
    finalized_at = models.DateTimeField(null=True, blank=True)
    finalized_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='finalized_grades'
    )
    
    # Additional details
    comments = models.TextField(blank=True)
    semester = models.CharField(max_length=50, blank=True)
    academic_year = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'grade_records'
        ordering = ['-created_at']
        unique_together = [['course', 'student', 'semester', 'academic_year']]
        indexes = [
            models.Index(fields=['course']),
            models.Index(fields=['student']),
            models.Index(fields=['finalized']),
        ]

    def __str__(self):
        return f"{self.student.user.email} - {self.course.code}: {self.grade_letter}"
    
    def calculate_grade_letter(self):
        """Calculate letter grade based on numeric value"""
        if self.grade_value >= 97:
            return 'A+'
        elif self.grade_value >= 93:
            return 'A'
        elif self.grade_value >= 90:
            return 'A-'
        elif self.grade_value >= 87:
            return 'B+'
        elif self.grade_value >= 83:
            return 'B'
        elif self.grade_value >= 80:
            return 'B-'
        elif self.grade_value >= 77:
            return 'C+'
        elif self.grade_value >= 73:
            return 'C'
        elif self.grade_value >= 70:
            return 'C-'
        elif self.grade_value >= 60:
            return 'D'
        else:
            return 'F'
    
    def calculate_grade_points(self):
        """Calculate grade points based on letter grade"""
        grade_point_map = {
            'A+': 4.00, 'A': 4.00, 'A-': 3.70,
            'B+': 3.30, 'B': 3.00, 'B-': 2.70,
            'C+': 2.30, 'C': 2.00, 'C-': 1.70,
            'D': 1.00, 'F': 0.00,
            'I': 0.00, 'W': 0.00, 'P': 0.00, 'NP': 0.00
        }
        return grade_point_map.get(self.grade_letter, 0.00)
