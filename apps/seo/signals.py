"""SEO Signals"""
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import SEOMetadata


@receiver(post_delete)
def delete_seo_metadata_on_object_delete(sender, instance, **kwargs):
    """Delete SEO metadata when the related object is deleted"""
    # Skip if sender is SEOMetadata itself
    if sender == SEOMetadata:
        return
    
    try:
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(sender)
        SEOMetadata.objects.filter(
            content_type=content_type,
            object_id=instance.pk
        ).delete()
    except Exception:
        pass
