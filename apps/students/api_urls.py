"""API URLs for students app"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.enrollments import EnrollmentViewSet
from .api import transcripts

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')

urlpatterns = router.urls + [
    # Transcript endpoints
    path('transcripts/<uuid:student_id>/', transcripts.get_student_transcript, name='get_student_transcript'),
    path('transcripts/<uuid:student_id>/list/', transcripts.list_student_transcripts, name='list_student_transcripts'),
    path('transcripts/<uuid:student_id>/summary/', transcripts.get_transcript_summary, name='get_transcript_summary'),
    path('transcripts/<uuid:transcript_id>/certify/', transcripts.certify_transcript, name='certify_transcript'),
]
