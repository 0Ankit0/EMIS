"""Student URL patterns"""
from django.urls import path
from apps.students.api import transcripts

app_name = 'students'

urlpatterns = [
    # Transcript endpoints (T180)
    path('transcripts/<uuid:student_id>/', transcripts.get_student_transcript, name='get_student_transcript'),
    path('transcripts/<uuid:student_id>/list/', transcripts.list_student_transcripts, name='list_student_transcripts'),
    path('transcripts/<uuid:student_id>/summary/', transcripts.get_transcript_summary, name='get_transcript_summary'),
    path('transcripts/<uuid:transcript_id>/certify/', transcripts.certify_transcript, name='certify_transcript'),
]
