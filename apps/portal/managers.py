from django.db import models


class PortalQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def for_role(self, role):
        return self.filter(roles__contains=role)


class PortalManager(models.Manager):
    def get_queryset(self):
        return PortalQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def for_role(self, role):
        return self.get_queryset().for_role(role)


class AnnouncementQuerySet(models.QuerySet):
    def published(self):
        from django.utils import timezone
        now = timezone.now()
        return self.filter(
            is_published=True,
            publish_date__lte=now
        ).exclude(expiry_date__lt=now)
    
    def for_role(self, role):
        return self.filter(target_roles__contains=role)


class AnnouncementManager(models.Manager):
    def get_queryset(self):
        return AnnouncementQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def for_role(self, role):
        return self.get_queryset().for_role(role)
    
    def active_for_role(self, role):
        return self.published().for_role(role)
