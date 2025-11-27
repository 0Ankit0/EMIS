from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class TimeStampedModel(models.Model):
    """Abstract base class that provides self-updating
    ``created_at`` and ``updated_at`` fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Calendar(TimeStampedModel):
    """Model representing a calendar."""
    title = models.CharField(max_length=200)

    def __str__(self) -> str: # what to return when we print an object of this class
        return self.title
    
class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, blank=True, help_text="Hex color code")
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
    
class Event(TimeStampedModel):
    """Model representing an event in a calendar."""
    # Event types
    SINGLE_DAY = 'single'
    MULTI_DAY = 'multi'

    EVENT_TYPES = [
        (SINGLE_DAY, 'Single Day Event'),
        (MULTI_DAY, 'Multi-day Event'),
    ]

    # Event status
    EVENT_STATUS_DRAFT = 'draft'
    EVENT_STATUS_PUBLISHED = 'published'
    EVENT_STATUS = [
        (EVENT_STATUS_DRAFT, 'Draft'),
        (EVENT_STATUS_PUBLISHED, 'Published'),
    ]

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='events')
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organizer = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    type = models.CharField(max_length=10,
                            choices=EVENT_TYPES,
                            default=SINGLE_DAY)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    entry_form_required = models.BooleanField(default=False)
    reminder_enabled = models.BooleanField(default=False)
    status = models.CharField(max_length=20, 
                              choices=EVENT_STATUS, 
                              default=EVENT_STATUS_DRAFT)
    
    def clean(self):
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")
        elif not self.start_time or not self.end_time:
            raise ValidationError("Start time and end time are required.")
        
        if self.type == self.MULTI_DAY:
            if not self.start_date or not self.end_date:
                raise ValidationError("Start date and end date are required for multi-day events.")
            if self.start_date >= self.end_date:
                raise ValidationError("End date must be after start date.")
        elif self.type == self.SINGLE_DAY:
            if self.start_date or self.end_date:
                raise ValidationError("Start date and end date should be empty for single day events.")

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
       if self.type == 'single':
           return f"{self.title} from {self.start_time} to {self.end_time}"
       else:
           return f"{self.title} from {self.start_date} to {self.end_date} and {self.start_time} to {self.end_time}"