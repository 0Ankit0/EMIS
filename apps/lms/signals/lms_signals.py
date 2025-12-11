"""
LMS Signals
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from ..models import Enrollment, LessonProgress, QuizAttempt, Certificate
from ..utils import calculate_progress, generate_certificate_number

@receiver(post_save, sender=LessonProgress)
def update_enrollment_progress(sender, instance, created, **kwargs):
    """
    Update enrollment progress when lesson progress changes
    """
    if instance.is_completed:
        enrollment = instance.enrollment
        enrollment.progress_percentage = calculate_progress(enrollment)
        # Check if course is completed
        if enrollment.progress_percentage >= 100:
            enrollment.status = 'completed'
            enrollment.completion_date = timezone.now()
            # Issue certificate if not already issued
            if not enrollment.certificate_issued:
                certificate_number = generate_certificate_number(enrollment)
                Certificate.objects.get_or_create(
                    enrollment=enrollment,
                    defaults={'certificate_number': certificate_number}
                )
                enrollment.certificate_issued = True
                enrollment.certificate_number = certificate_number
        enrollment.save()

@receiver(post_save, sender=QuizAttempt)
def quiz_attempt_graded(sender, instance, created, **kwargs):
    """
    Handle quiz attempt grading
    """
    if not created and instance.status == 'graded':
        # Update lesson progress if quiz is mandatory and passed
        if instance.quiz.is_mandatory and instance.passed:
            lesson = instance.quiz.lesson
            progress, created = LessonProgress.objects.get_or_create(
                enrollment=instance.enrollment,
                lesson=lesson
            )
            if not progress.is_completed:
                progress.is_completed = True
                progress.completion_date = timezone.now()
                progress.save()

@receiver(post_save, sender=Enrollment)
def enrollment_created(sender, instance, created, **kwargs):
    """
    Handle new enrollment
    """
    if created:
        # You can add logic here like sending welcome email
        pass
