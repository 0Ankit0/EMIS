from django.db import models
from django.core.exceptions import ValidationError
from . import Student
from . import BaseModel

class AttemptType(models.TextChoices):
    REGULAR = 'regular', 'Regular'
    RE_EXAM = 're_exam', 'Re-examination'

class GradeChoices(models.TextChoices):
    A_PLUS = 'A+', 'A+'
    A = 'A', 'A'
    B_PLUS = 'B+', 'B+'
    B = 'B', 'B'
    C_PLUS = 'C+', 'C+'
    C = 'C', 'C'
    D = 'D', 'D'
    F = 'F', 'F'
    I = 'I', 'Incomplete'

class SubjectResult(BaseModel):
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_results')
    subject_name = models.CharField(max_length=255)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    maximum_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=2, choices=GradeChoices.choices, blank=True, null=True)
    credit_hours = models.IntegerField(default=3)
    semester = models.CharField(max_length=20)
    attempt_type = models.CharField(max_length=10, choices=AttemptType.choices, default=AttemptType.REGULAR)
     
    def clean(self):
        if self.marks_obtained is not None and self.marks_obtained < 0:
            raise ValidationError('Marks obtained cannot be negative.')
        
        if self.maximum_marks is not None and self.maximum_marks <= 0:
            raise ValidationError('Maximum marks must be greater than zero.')
        
        if self.marks_obtained is not None and self.maximum_marks is not None:
            if self.marks_obtained > self.maximum_marks:
                raise ValidationError('Marks obtained cannot exceed maximum marks.')
        
        if self.credit_hours < 0:
            raise ValidationError('Credit hours cannot be negative.')

    def __str__(self):
        return f"{self.subject_name} Result for {self.student.first_name} {self.student.last_name}"

    class Meta: # type: ignore
        db_table = 'subject_results'
        ordering = ['-semester', 'subject_name']