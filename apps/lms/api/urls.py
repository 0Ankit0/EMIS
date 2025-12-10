"""API URLs for lms app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'courses', api_views.CourseViewSet, basename='course')
router.register(r'modules', api_views.ModuleViewSet, basename='module')
router.register(r'lessons', api_views.LessonViewSet, basename='lesson')
router.register(r'enrollments', api_views.EnrollmentViewSet, basename='enrollment')
router.register(r'lesson-progress', api_views.LessonProgressViewSet, basename='lesson-progress')
router.register(r'quizzes', api_views.QuizViewSet, basename='quiz')
router.register(r'quiz-attempts', api_views.QuizAttemptViewSet, basename='quiz-attempt')
router.register(r'assignments', api_views.AssignmentViewSet, basename='assignment')
router.register(r'assignment-submissions', api_views.AssignmentSubmissionViewSet, basename='assignment-submission')
router.register(r'discussions', api_views.DiscussionViewSet, basename='discussion')
router.register(r'discussion-replies', api_views.DiscussionReplyViewSet, basename='discussion-reply')
router.register(r'certificates', api_views.CertificateViewSet, basename='certificate')

urlpatterns = [
    path('', include(router.urls)),
]

