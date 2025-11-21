"""HR URL Configuration"""
from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<uuid:pk>/', views.employee_detail, name='employee_detail'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('leaves/', views.leave_list, name='leave_list'),
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('jobs/', views.job_list, name='job_list'),
    path('applications/', views.application_list, name='application_list'),
]
