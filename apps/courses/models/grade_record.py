from django.db import models
from apps.core.models import TimeStampedModel


class GradeRecord(TimeStampedModel):
    class GradeLetter(models.TextChoices):
        A_PLUS = 'A+', 'A+'
        A = 'A', 'A'
        A_MINUS = 'A-', 'A-'
        B_PLUS = 'B+', 'B+'
        B = 'B', 'B'
        B_MINUS = 'B-', 'B-'
        C_PLUS = 'C+', 'C+'
        C = 'C', 'C'
        C_MINUS = 'C-', 'C-'
        D = 'D', 'D'
        F = 'F', 'F'
        INCOMPLETE = 'I', 'Incomplete'
        WITHDRAWN = 'W', 'Withdrawn'
        PASS = 'P', 'Pass'
        NO_PASS = 'NP', 'No Pass'

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
        choices=GradeLetter.choices,
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
        unique_together = (('course', 'student', 'semester', 'academic_year'),)
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
            return GradeLetter.A_PLUS
        elif self.grade_value >= 93:
            return GradeLetter.A
        elif self.grade_value >= 90:
            return GradeLetter.A_MINUS
        elif self.grade_value >= 87:
            return GradeLetter.B_PLUS
        elif self.grade_value >= 83:
            return GradeLetter.B
        elif self.grade_value >= 80:
            return GradeLetter.B_MINUS
        elif self.grade_value >= 77:
            return GradeLetter.C_PLUS
        elif self.grade_value >= 73:
            return GradeLetter.C
        elif self.grade_value >= 70:
            return GradeLetter.C_MINUS
        elif self.grade_value >= 60:
            return GradeLetter.D
        else:
            return GradeLetter.F
    
    def calculate_grade_points(self):
        """Calculate grade points based on letter grade"""
        grade_point_map = {
            GradeLetter.A_PLUS: 4.00, GradeLetter.A: 4.00, GradeLetter.A_MINUS: 3.70,
            GradeLetter.B_PLUS: 3.30, GradeLetter.B: 3.00, GradeLetter.B_MINUS: 2.70,
            GradeLetter.C_PLUS: 2.30, GradeLetter.C: 2.00, GradeLetter.C_MINUS: 1.70,
            GradeLetter.D: 1.00, GradeLetter.F: 0.00,
            GradeLetter.INCOMPLETE: 0.00, GradeLetter.WITHDRAWN: 0.00, 
            GradeLetter.PASS: 0.00, GradeLetter.NO_PASS: 0.00
        }
        return grade_point_map.get(self.grade_letter, 0.00)

