from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from . import BaseModel
class Student(BaseModel):
    registration_number = models.BigIntegerField(unique=True)
    roll_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    enrollment_date = models.DateField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.CharField(max_length=100, null=True, blank=True)

    def clean(self):
        if self.date_of_birth:
            age = (date.today() - self.date_of_birth).days / 365.25
            if age < 3:
                raise ValidationError('Student must be at least 3 years old.')
            if age > 100:
                raise ValidationError('Invalid date of birth.')
        
        if self.enrollment_date and self.enrollment_date > date.today():
            raise ValidationError('Enrollment date cannot be in the future.')

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Reg No: {self.registration_number})"

    class Meta: # type: ignore
        db_table = 'students'
        ordering = [ 'first_name', 'last_name' ]
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['registration_number']),
            models.Index(fields=['is_active', 'enrollment_date']),
            models.Index(fields=['is_deleted']),
        ]