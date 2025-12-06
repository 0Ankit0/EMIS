from django.db import models
from .student import Student
from .base import BaseModel

class Guardian(BaseModel):
    student = models.ManyToManyField(Student, related_name='guardians')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} is the {self.relationship} of {', '.join([student.first_name + ' ' + student.last_name for student in self.student.all()])}"

    class Meta: # type: ignore
        db_table = 'guardians'
        ordering = ['first_name', 'last_name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]