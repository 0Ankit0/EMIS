from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.students.models import Student
from apps.faculty.models import Faculty
from .models import Dashboard, StudentPortalProfile, FacultyPortalProfile

User = get_user_model()


@receiver(post_save, sender=Student)
def create_student_portal_profile(sender, instance, created, **kwargs):
    """Create portal profile when student is created"""
    if created:
        StudentPortalProfile.objects.get_or_create(student=instance)
        Dashboard.objects.get_or_create(
            user=instance.user,
            defaults={'role': 'student'}
        )


@receiver(post_save, sender=Faculty)
def create_faculty_portal_profile(sender, instance, created, **kwargs):
    """Create portal profile when faculty is created"""
    if created:
        FacultyPortalProfile.objects.get_or_create(faculty=instance)
        Dashboard.objects.get_or_create(
            user=instance.user,
            defaults={'role': 'faculty'}
        )
