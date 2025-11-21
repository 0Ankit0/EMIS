"""
Timetable URL Configuration
"""
from django.urls import path
from . import views

app_name = 'timetable'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Timetable Entries
    path('list/', views.timetable_list, name='list'),
    path('create/', views.timetable_create, name='create'),
    path('<uuid:pk>/update/', views.timetable_update, name='update'),
    path('<uuid:pk>/delete/', views.timetable_delete, name='delete'),
    
    # View Schedules
    path('class-schedule/', views.class_schedule, name='class_schedule'),
    path('teacher-schedule/', views.teacher_schedule, name='teacher_schedule'),
    path('room-allocation/', views.room_allocation, name='room_allocation'),
    
    # Rooms
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/create/', views.room_create, name='room_create'),
    
    # Time Slots
    path('timeslots/', views.timeslot_list, name='timeslot_list'),
    
    # Export
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    
    # AJAX
    path('check-conflict/', views.check_conflict, name='check_conflict'),
]
