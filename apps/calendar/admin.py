"""Calendar Admin"""
from django.contrib import admin
from .models import EventCategory, Calendar, Event, EventReminder


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_code', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active']


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'calendar_type', 'visibility', 'is_active']
    search_fields = ['name', 'owner__username']
    list_filter = ['calendar_type', 'visibility', 'is_active']
    filter_horizontal = ['shared_with']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_datetime', 'end_datetime', 'category', 'priority', 'created_by']
    search_fields = ['title', 'description', 'location']
    list_filter = ['category', 'priority', 'is_all_day', 'recurrence', 'start_datetime']
    filter_horizontal = ['calendars', 'attendees']
    date_hierarchy = 'start_datetime'


@admin.register(EventReminder)
class EventReminderAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'time_value', 'time_unit', 'reminder_type', 'is_sent']
    search_fields = ['event__title', 'user__username']
    list_filter = ['reminder_type', 'is_sent', 'time_unit']
