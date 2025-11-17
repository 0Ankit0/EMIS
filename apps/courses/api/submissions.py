from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.courses.serializers import (
    SubmissionCreateSerializer,
    SubmissionResponseSerializer,
)
from apps.courses.services import SubmissionService
from apps.core.middleware.rbac import require_permission
from apps.core.middleware.audit import audit_action


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'create')
@audit_action(action='submission.create')
def create_submission(request):
    """Create a new submission (T176)"""
    serializer = SubmissionCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    submission = SubmissionService.create_submission(serializer.validated_data)
    
    response_serializer = SubmissionResponseSerializer(submission)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def list_submissions(request):
    """List submissions with optional filtering (T177)"""
    filters = {}
    
    # Extract filter parameters
    if request.query_params.get('assignment'):
        filters['assignment'] = request.query_params.get('assignment')
    if request.query_params.get('student'):
        filters['student'] = request.query_params.get('student')
    if request.query_params.get('grade_status'):
        filters['grade_status'] = request.query_params.get('grade_status')
    if request.query_params.get('is_late'):
        filters['is_late'] = request.query_params.get('is_late').lower() == 'true'
    
    # Pagination parameters
    limit = int(request.query_params.get('limit', 50))
    offset = int(request.query_params.get('offset', 0))
    
    submissions, total = SubmissionService.list_submissions(
        filters=filters,
        limit=limit,
        offset=offset
    )
    
    serializer = SubmissionResponseSerializer(submissions, many=True)
    
    return Response({
        'results': serializer.data,
        'total': total,
        'limit': limit,
        'offset': offset,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def get_submission(request, submission_id):
    """Get a single submission by ID"""
    submission = SubmissionService.get_submission(submission_id)
    
    if not submission:
        return Response(
            {'error': 'Submission not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = SubmissionResponseSerializer(submission)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'update')
@audit_action(action='submission.grade')
def grade_submission(request, submission_id):
    """Grade a submission"""
    score = request.data.get('score')
    feedback = request.data.get('feedback', '')
    
    if score is None:
        return Response(
            {'error': 'Score is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        score = float(score)
    except (ValueError, TypeError):
        return Response(
            {'error': 'Invalid score value'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    submission = SubmissionService.grade_submission(
        submission_id=submission_id,
        score=score,
        feedback=feedback,
        graded_by_id=request.user.id
    )
    
    if not submission:
        return Response(
            {'error': 'Submission not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = SubmissionResponseSerializer(submission)
    return Response(serializer.data)
