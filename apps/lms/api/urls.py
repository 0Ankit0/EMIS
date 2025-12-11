"""API URLs for lms app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='course')
router.register(r'modules', views.ModuleViewSet, basename='module')
router.register(r'lessons', views.LessonViewSet, basename='lesson')
router.register(r'enrollments', views.EnrollmentViewSet, basename='enrollment')
router.register(r'lesson-progress', views.LessonProgressViewSet, basename='lesson-progress')
router.register(r'quizzes', views.QuizViewSet, basename='quiz')
router.register(r'quiz-attempts', views.QuizAttemptViewSet, basename='quiz-attempt')
router.register(r'assignments', views.AssignmentViewSet, basename='assignment')
router.register(r'assignment-submissions', views.AssignmentSubmissionViewSet, basename='assignment-submission')
router.register(r'discussions', views.DiscussionViewSet, basename='discussion')
router.register(r'discussion-replies', views.DiscussionReplyViewSet, basename='discussion-reply')
router.register(r'certificates', views.CertificateViewSet, basename='certificate')

urlpatterns = [
    path('', include(router.urls)),
]

