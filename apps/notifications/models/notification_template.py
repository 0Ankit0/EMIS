from django.db import models
from apps.core.models import TimeStampedModel
from .notification_type import NotificationType
from ..managers import NotificationTemplateManager

class NotificationTemplate(TimeStampedModel):
    """
    Reusable notification templates
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    title_template = models.CharField(max_length=255)
    message_template = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO
    )
    default_channels = models.JSONField(
        default=list,
        help_text="Default delivery channels"
    )
    is_active = models.BooleanField(default=True)
    template_variables = models.JSONField(
        default=list,
        help_text="List of variables used in template"
    )
    objects = NotificationTemplateManager()
    class Meta:
        db_table = 'notification_templates'
        ordering = ['name']
        verbose_name = 'Notification Template'
        verbose_name_plural = 'Notification Templates'
    def __str__(self):
        return self.name
    def render(self, context):
        from django.template import Template, Context
        title = Template(self.title_template).render(Context(context))
        message = Template(self.message_template).render(Context(context))
        return {
            'title': title,
            'message': message,
            'notification_type': self.notification_type,
            'channels': self.default_channels,
        }
