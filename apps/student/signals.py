from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Enrollment, EnrollmentHistory


@receiver(pre_save, sender=Enrollment)
def track_enrollment_status_changes(sender, instance, **kwargs):
    """
    Automatically create EnrollmentHistory record when enrollment status changes.
    """
    if instance.pk:
        try:
            old_enrollment = Enrollment.objects.get(pk=instance.pk)
            if old_enrollment.status != instance.status:
                EnrollmentHistory.objects.create(
                    enrollment=instance,
                    student=instance.student,
                    semester=instance.semester,
                    previous_status=old_enrollment.status,
                    new_status=instance.status,
                    changed_by='system'
                )
        except Enrollment.DoesNotExist:
            pass
