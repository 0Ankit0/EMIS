import uuid
from django.db import models
from apps.authentication.models import User

class Slider(models.Model):
    """Homepage sliders/carousels"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='cms/sliders/')
    mobile_image = models.ImageField(upload_to='cms/sliders/', blank=True, null=True)
    link_text = models.CharField(max_length=100, blank=True)
    link_url = models.CharField(max_length=500, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='sliders'
    )
    class Meta:
        db_table = 'cms_sliders'
        ordering = ['order', '-created_at']
    def __str__(self):
        return self.title
