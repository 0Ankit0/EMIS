from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel

class MessMenu(TimeStampedModel):
    """Mess Menu"""
    class MealType(models.TextChoices):
        BREAKFAST = 'breakfast', 'Breakfast'
        LUNCH = 'lunch', 'Lunch'
        SNACKS = 'snacks', 'Snacks'
        DINNER = 'dinner', 'Dinner'
    
    class DayOfWeek(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'
    
    hostel = models.ForeignKey('hostel.Hostel', on_delete=models.CASCADE, related_name='mess_menus')
    day_of_week = models.CharField(max_length=20, choices=DayOfWeek.choices)
    meal_type = models.CharField(max_length=20, choices=MealType.choices)
    menu_items = models.JSONField(
        default=list,
        help_text="List of menu items"
    )
    timing = models.CharField(max_length=50, help_text="e.g., '7:00 AM - 9:00 AM'")
    is_active = models.BooleanField(default=True)
    effective_from = models.DateField(default=timezone.now)
    class Meta:
        db_table = 'hostel_mess_menus'
        unique_together = ['hostel', 'day_of_week', 'meal_type']
        ordering = ['hostel', 'day_of_week', 'meal_type']
        verbose_name = 'Mess Menu'
        verbose_name_plural = 'Mess Menus'
    def __str__(self):
        return f"{self.hostel.name} - {self.day_of_week} {self.meal_type}"
