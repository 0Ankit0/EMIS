from django.db import models

class Student(models.Model):
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
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (Reg No: {self.registration_number})"

    class Meta:
        db_table = 'students'
        ordering = [ 'first_name', 'last_name' ]
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['registration_number']),
            models.Index(fields=['is_active', 'enrollment_date']),
            models.Index(fields=['is_deleted']),
        ]