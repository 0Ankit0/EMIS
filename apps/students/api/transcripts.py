from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
from apps.students.models import Transcript
from apps.students.services import TranscriptService
from apps.core.middleware.rbac import require_permission
from apps.core.middleware.audit import audit_action


class TranscriptResponseSerializer(serializers.ModelSerializer):
    """Serializer for transcript responses"""
    student_email = serializers.EmailField(source='student.user.email', read_only=True)
    generated_by_email = serializers.EmailField(source='generated_by.email', read_only=True, allow_null=True)
    
    class Meta:
        model = Transcript
        fields = [
            'id',
            'student',
            'student_email',
            'grade_records_snapshot',
            'total_credits_attempted',
            'total_credits_earned',
            'cumulative_gpa',
            'generated_at',
            'generated_by',
            'generated_by_email',
            'transcript_type',
            'academic_year',
            'semester',
            'is_certified',
            'certification_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'generated_at', 'created_at', 'updated_at']


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('students', 'read')
def get_student_transcript(request, student_id):
    """Get or generate transcript for a student (T180)"""
    # Check if we should generate a new one or get the latest
    generate_new = request.query_params.get('generate', 'false').lower() == 'true'
    transcript_type = request.query_params.get('type', 'unofficial')
    semester = request.query_params.get('semester')
    academic_year = request.query_params.get('academic_year')
    
    if generate_new:
        # Generate a new transcript
        transcript = TranscriptService.generate_transcript(
            student_id=student_id,
            transcript_type=transcript_type,
            semester=semester,
            academic_year=academic_year,
            generated_by_id=request.user.id
        )
    else:
        # Get the latest transcript
        transcript = TranscriptService.get_latest_transcript(
            student_id=student_id,
            transcript_type=transcript_type
        )
        
        if not transcript:
            # If no transcript exists, generate one
            transcript = TranscriptService.generate_transcript(
                student_id=student_id,
                transcript_type=transcript_type,
                semester=semester,
                academic_year=academic_year,
                generated_by_id=request.user.id
            )
    
    serializer = TranscriptResponseSerializer(transcript)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('students', 'read')
def list_student_transcripts(request, student_id):
    """List all transcripts for a student"""
    transcripts = TranscriptService.list_student_transcripts(student_id)
    serializer = TranscriptResponseSerializer(transcripts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('students', 'read')
def get_transcript_summary(request, student_id):
    """Get academic summary for a student without generating full transcript"""
    summary = TranscriptService.get_transcript_summary(student_id)
    return Response(summary)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('students', 'update')
@audit_action(action='transcript.certify')
def certify_transcript(request, transcript_id):
    """Certify a transcript (make it official)"""
    transcript = TranscriptService.certify_transcript(
        transcript_id=transcript_id,
        certified_by_id=request.user.id
    )
    
    if not transcript:
        return Response(
            {'error': 'Transcript not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = TranscriptResponseSerializer(transcript)
    return Response(serializer.data)
