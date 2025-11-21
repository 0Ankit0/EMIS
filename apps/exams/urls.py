"""
Exams URL Configuration
Complete CRUD and additional operations
"""
from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Exam CRUD Operations
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/create/', views.exam_create, name='exam_create'),
    path('exams/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('exams/<int:pk>/update/', views.exam_update, name='exam_update'),
    path('exams/<int:pk>/delete/', views.exam_delete, name='exam_delete'),
    
    # Exam Results
    path('results/', views.result_list, name='result_list'),
    path('results/create/', views.result_create, name='result_create'),
    path('results/<int:pk>/update/', views.result_update, name='result_update'),
    path('exams/<int:exam_id>/grade-entry/', views.grade_entry, name='grade_entry'),
    
    # Exam Schedules
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/<int:pk>/', views.schedule_detail, name='schedule_detail'),
    
    # Export Operations
    path('export/exams/csv/', views.export_exams_csv, name='export_exams_csv'),
    path('export/results/csv/', views.export_results_csv_view, name='export_results_csv'),
    path('results/<int:student_id>/<int:exam_id>/pdf/', views.result_card_pdf, name='result_card_pdf'),
    
    # AJAX/API Operations
    path('api/exams/<int:pk>/data/', views.get_exam_data, name='get_exam_data'),
    path('api/exams/<int:pk>/status/', views.update_exam_status, name='update_exam_status'),
    
    # Analysis and Reports
    path('analysis/', views.analysis, name='analysis'),
    
    # Bulk Operations
    path('bulk/upload/', views.bulk_result_upload, name='bulk_result_upload'),
]
