from django.urls import path
from apps.courses.api import courses, assignments, submissions, grades

urlpatterns = [
    # Course endpoints (T169-T173)
    path('courses/', courses.list_courses, name='list_courses'),
    path('courses/create/', courses.create_course, name='create_course'),
    path('courses/<uuid:course_id>/', courses.get_course, name='get_course'),
    path('courses/<uuid:course_id>/update/', courses.update_course, name='update_course'),
    path('courses/<uuid:course_id>/modules/', courses.list_modules, name='list_modules'),
    path('courses/<uuid:course_id>/modules/create/', courses.create_module, name='create_module'),
    
    # Assignment endpoints (T174-T175)
    path('assignments/', assignments.list_assignments, name='list_assignments'),
    path('assignments/create/', assignments.create_assignment, name='create_assignment'),
    path('assignments/<uuid:assignment_id>/', assignments.get_assignment, name='get_assignment'),
    path('assignments/<uuid:assignment_id>/update/', assignments.update_assignment, name='update_assignment'),
    
    # Submission endpoints (T176-T177)
    path('submissions/', submissions.list_submissions, name='list_submissions'),
    path('submissions/create/', submissions.create_submission, name='create_submission'),
    path('submissions/<uuid:submission_id>/', submissions.get_submission, name='get_submission'),
    path('submissions/<uuid:submission_id>/grade/', submissions.grade_submission, name='grade_submission'),
    
    # Grade endpoints (T178-T179)
    path('grades/', grades.list_grades, name='list_grades'),
    path('grades/create/', grades.create_grade, name='create_grade'),
    path('grades/<uuid:grade_id>/', grades.get_grade, name='get_grade'),
    path('grades/<uuid:grade_id>/update/', grades.update_grade, name='update_grade'),
    path('grades/<uuid:grade_id>/finalize/', grades.finalize_grade, name='finalize_grade'),
]
