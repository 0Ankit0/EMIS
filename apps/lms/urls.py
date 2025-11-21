"""
LMS URL Configuration
"""
from django.urls import path
from . import views

app_name = 'lms'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Courses
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/<int:pk>/enroll/', views.course_enroll, name='course_enroll'),
    
    # My Learning
    path('my-learning/', views.my_learning, name='my_learning'),
    
    # Lessons
    path('lessons/<int:pk>/', views.lesson_view, name='lesson_view'),
    path('lessons/<int:pk>/complete/', views.lesson_complete, name='lesson_complete'),
    
    # Quizzes
    path('quizzes/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quizzes/<int:pk>/start/', views.quiz_start, name='quiz_start'),
    path('quiz-attempts/<int:attempt_id>/', views.quiz_take, name='quiz_take'),
    path('quiz-attempts/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
    
    # Assignments
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:pk>/submit/', views.assignment_submit, name='assignment_submit'),
    
    # Discussions
    path('courses/<int:course_id>/discussions/', views.discussion_list, name='discussion_list'),
    path('courses/<int:course_id>/discussions/create/', views.discussion_create, name='discussion_create'),
    path('discussions/<int:pk>/', views.discussion_detail, name='discussion_detail'),
    
    # Certificates
    path('my-certificates/', views.my_certificates, name='my_certificates'),
    path('certificates/<int:pk>/', views.certificate_view, name='certificate_view'),
    
    # Legacy URLs (for compatibility)
    path('list/', views.item_list, name='list'),
    path('create/', views.item_create, name='create'),
    path('<int:pk>/', views.item_detail, name='detail'),
    path('<int:pk>/update/', views.item_update, name='update'),
    path('<int:pk>/delete/', views.item_delete, name='delete'),
    
    # Bulk Operations
    path('bulk-delete/', views.bulk_delete, name='bulk_delete'),
    path('bulk-update-status/', views.bulk_update_status, name='bulk_update_status'),
    
    # Export Operations
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    
    # AJAX/API Operations
    path('<int:pk>/data/', views.get_item_data, name='get_data'),
    path('<int:pk>/toggle-status/', views.toggle_status, name='toggle_status'),
    
    # Statistics and Reports
    path('statistics/', views.statistics, name='statistics'),
    path('search/', views.search, name='search'),
]
