from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import TimeStampedModel
from .exam import Exam
from ..managers import ExamResultManager

class ExamResult(TimeStampedModel):
    """
    Individual exam results for students
    """
    class Grade(models.TextChoices):
        A_PLUS = 'A+', 'A+'
        A = 'A', 'A'
        B_PLUS = 'B+', 'B+'
        B = 'B', 'B'
        C_PLUS = 'C+', 'C+'
        C = 'C', 'C'
        D = 'D', 'D'
        F = 'F', 'F'
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='exam_results')
    marks_obtained = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    grade = models.CharField(max_length=2, choices=Grade.choices, blank=True)
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
        if not self.is_absent:
            self.is_passed = self.marks_obtained >= self.exam.passing_marks
            self.grade = self.calculate_grade()
        super().save(*args, **kwargs)
    
    def calculate_grade(self):
        percentage = (float(self.marks_obtained) / self.exam.total_marks) * 100
        if percentage >= 90:
            return Grade.A_PLUS
        elif percentage >= 80:
            return Grade.A
        elif percentage >= 70:
            return Grade.B_PLUS
        elif percentage >= 60:
            return Grade.B
        elif percentage >= 50:
            return Grade.C_PLUS
        elif percentage >= 40:
            return Grade.C
        elif percentage >= 35:
            return Grade.D
        else:
            return Grade.F

