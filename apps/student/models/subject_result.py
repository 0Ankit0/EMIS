from django.db import models
from django.core.exceptions import ValidationError
from . import Student
from . import BaseModel
class SubjectResult(BaseModel):
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
        ('I', 'Incomplete'),
        ('W', 'Withdrawn'),
    ]
    ATTEMPT_CHOICE_REGULAR = 'regular'
    ATTEMPT_CHOICE_REEXAM = 're_exam'
    ATTEMPT_CHOICES = [
        (ATTEMPT_CHOICE_REGULAR, 'Regular'),
        (ATTEMPT_CHOICE_REEXAM, 'Re-examination'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_results')
    subject_name = models.CharField(max_length=255)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    maximum_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    credit_hours = models.IntegerField(default=3)
    semester = models.CharField(max_length=20)
    attempt_type = models.CharField(max_length=10, choices=ATTEMPT_CHOICES, default='regular')
     
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