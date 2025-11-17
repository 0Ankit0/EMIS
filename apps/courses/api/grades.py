from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.courses.serializers import (
    GradeRecordCreateSerializer,
    GradeRecordResponseSerializer,
)
from apps.courses.services import GradingService
from apps.core.middleware.rbac import require_permission
from apps.core.middleware.audit import audit_action


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'create')
@audit_action(action='grade.create')
def create_grade(request):
    """Create a new grade record (T178) - Faculty only"""
    serializer = GradeRecordCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    grade_record = GradingService.create_grade_record(serializer.validated_data)
    
    response_serializer = GradeRecordResponseSerializer(grade_record)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def list_grades(request):
    """List grade records with optional filtering (T179)"""
    filters = {}
    
    # Extract filter parameters
    if request.query_params.get('course'):
        filters['course'] = request.query_params.get('course')
    if request.query_params.get('student'):
        filters['student'] = request.query_params.get('student')
    if request.query_params.get('finalized'):
        filters['finalized'] = request.query_params.get('finalized').lower() == 'true'
    if request.query_params.get('semester'):
        filters['semester'] = request.query_params.get('semester')
    if request.query_params.get('academic_year'):
        filters['academic_year'] = request.query_params.get('academic_year')
    
    # Pagination parameters
    limit = int(request.query_params.get('limit', 50))
    offset = int(request.query_params.get('offset', 0))
    
    grade_records, total = GradingService.list_grade_records(
        filters=filters,
        limit=limit,
        offset=offset
    )
    
    serializer = GradeRecordResponseSerializer(grade_records, many=True)
    
    return Response({
        'results': serializer.data,
        'total': total,
        'limit': limit,
        'offset': offset,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def get_grade(request, grade_id):
    """Get a single grade record by ID"""
    grade_record = GradingService.get_grade_record(grade_id)
    
    if not grade_record:
        return Response(
            {'error': 'Grade record not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = GradeRecordResponseSerializer(grade_record)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'update')
@audit_action(action='grade.update')
def update_grade(request, grade_id):
    """Update a grade record (only if not finalized)"""
    serializer = GradeRecordCreateSerializer(
        data=request.data,
        partial=request.method == 'PATCH'
    )
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    grade_record = GradingService.update_grade_record(
        grade_id,
        serializer.validated_data
    )
    
    if not grade_record:
        return Response(
            {'error': 'Grade record not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    response_serializer = GradeRecordResponseSerializer(grade_record)
    return Response(response_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'update')
@audit_action(action='grade.finalize')
def finalize_grade(request, grade_id):
    """Finalize a grade record (make it immutable)"""
    grade_record = GradingService.finalize_grade_record(
        grade_record_id=grade_id,
        finalized_by_id=request.user.id
    )
    
    if not grade_record:
        return Response(
            {'error': 'Grade record not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = GradeRecordResponseSerializer(grade_record)
    return Response(serializer.data)
