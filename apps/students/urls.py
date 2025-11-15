"""
Student frontend URLs
"""
from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list, name='list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.student_create, name='create'),
    path('<uuid:pk>/', views.student_detail, name='detail'),
    path('<uuid:pk>/update/', views.student_update, name='update'),
    path('<uuid:pk>/admit/', views.student_admit, name='admit'),
    path('<uuid:pk>/graduate/', views.student_graduate, name='graduate'),
    path('stats/', views.statistics, name='statistics'),
]
