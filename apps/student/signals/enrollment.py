from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models import Enrollment, EnrollmentHistory
from apps.core.middleware import get_current_user

@receiver(post_save,sender=Enrollment)
def create_enrollment_history(sender,instance,created,**kwargs):
    if not created:
        previous = sender.objects.get(pk=instance.pk)
        user = get_current_user()
        changed_by = str(user) if user and user.is_authenticated else 'system'
        
        if previous.status != instance.status:
            EnrollmentHistory.objects.create(
                enrollment=instance,
                student=instance.student,
                semester=instance.semester,
                previous_status=previous.status,
                new_status=instance.status,
                changed_by=changed_by
            )
        else:
            EnrollmentHistory.objects.create(
                enrollment=instance,
                student=instance.student,
                semester=instance.semester,
                previous_status=previous.status,
                new_status=instance.status,
                changed_by=changed_by
            )
