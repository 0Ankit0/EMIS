"""Courses API URLs"""
from django.urls import path
from . import courses, assignments, submissions, grades

urlpatterns = [
    # Course endpoints
    path('courses/', courses.list_courses, name='course-list'),
    path('courses/create/', courses.create_course, name='course-create'),
    path('courses/<uuid:pk>/', courses.get_course, name='course-detail'),
    path('courses/<uuid:pk>/update/', courses.update_course, name='course-update'),
    
    # Module endpoints
    path('courses/<uuid:course_pk>/modules/', courses.list_modules, name='module-list'),
    path('courses/<uuid:course_pk>/modules/create/', courses.create_module, name='module-create'),
    
    # Assignment endpoints
    path('assignments/', assignments.list_assignments, name='assignment-list'),
    path('assignments/create/', assignments.create_assignment, name='assignment-create'),
    path('assignments/<uuid:pk>/', assignments.get_assignment, name='assignment-detail'),
    path('assignments/<uuid:pk>/update/', assignments.update_assignment, name='assignment-update'),
    
    # Submission endpoints
    path('submissions/', submissions.list_submissions, name='submission-list'),
    path('submissions/create/', submissions.create_submission, name='submission-create'),
    path('submissions/<uuid:pk>/', submissions.get_submission, name='submission-detail'),
    path('submissions/<uuid:pk>/grade/', submissions.grade_submission, name='submission-grade'),
    
    # Grade endpoints
    path('grades/', grades.list_grades, name='grade-list'),
    path('grades/create/', grades.create_grade, name='grade-create'),
    path('grades/<uuid:pk>/', grades.get_grade, name='grade-detail'),
    path('grades/<uuid:pk>/update/', grades.update_grade, name='grade-update'),
    path('grades/<uuid:pk>/finalize/', grades.finalize_grade, name='grade-finalize'),
]
