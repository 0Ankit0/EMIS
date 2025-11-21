from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.portal_home, name='home'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement_detail'),
    path('settings/profile/', views.profile_settings, name='profile_settings'),
    path('settings/dashboard/', views.dashboard_settings, name='dashboard_settings'),
    path('activity/', views.activity_log, name='activity_log'),
]
