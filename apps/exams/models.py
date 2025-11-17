"""
Exams models for EMIS
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel, AuditModel


class ExamType(models.TextChoices):
    """Exam type choices"""
    MIDTERM = 'midterm', 'Midterm'
    FINAL = 'final', 'Final'
    QUIZ = 'quiz', 'Quiz'
    ASSIGNMENT = 'assignment', 'Assignment'
    PRACTICAL = 'practical', 'Practical'
    PROJECT = 'project', 'Project'


class GradeScale(models.TextChoices):
    """Grade scale choices"""
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


class Exam(AuditModel):
    """Exam model"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    course = models.ForeignKey('lms.Course', on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    
    # Schedule
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    
    # Details
    total_marks = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Settings
    is_published = models.BooleanField(default=False)
    instructions = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'exams'
        ordering = ['-exam_date']
        indexes = [
            models.Index(fields=['exam_date']),
            models.Index(fields=['exam_type']),
            models.Index(fields=['code']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class ExamResult(AuditModel):
    """Exam result for a student"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='exam_results')
    
    # Scores
    marks_obtained = models.DecimalField(
        max_digits=6, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    grade = models.CharField(max_length=3, choices=GradeScale.choices, blank=True, null=True)
    
    # Status
    is_absent = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'exam_results'
        unique_together = [['exam', 'student']]
        ordering = ['-exam__exam_date']
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['exam']),
        ]
    
    def __str__(self):
        return f"{self.student.student_number} - {self.exam.code}: {self.marks_obtained}/{self.exam.total_marks}"
    
    def calculate_grade(self):
        """Calculate grade based on marks"""
        if self.is_absent or self.marks_obtained is None:
            return None
        
        percentage = (self.marks_obtained / self.exam.total_marks) * 100
        
        if percentage >= 90:
            return GradeScale.A_PLUS
        elif percentage >= 85:
            return GradeScale.A
        elif percentage >= 80:
            return GradeScale.A_MINUS
        elif percentage >= 75:
            return GradeScale.B_PLUS
        elif percentage >= 70:
            return GradeScale.B
        elif percentage >= 65:
            return GradeScale.B_MINUS
        elif percentage >= 60:
            return GradeScale.C_PLUS
        elif percentage >= 55:
            return GradeScale.C
        elif percentage >= 50:
            return GradeScale.C_MINUS
        elif percentage >= 40:
            return GradeScale.D
        else:
            return GradeScale.F
    
    def save(self, *args, **kwargs):
        """Auto-calculate grade and pass/fail status"""
        if self.marks_obtained is not None and not self.is_absent:
            self.grade = self.calculate_grade()
            self.is_passed = self.marks_obtained >= self.exam.passing_marks
        super().save(*args, **kwargs)
