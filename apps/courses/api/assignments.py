from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.courses.serializers import (
    AssignmentCreateSerializer,
    AssignmentResponseSerializer,
)
from apps.courses.services import AssignmentService
from apps.core.middleware.rbac import require_permission
from apps.core.middleware.audit import audit_action


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'create')
@audit_action(action='assignment.create')
def create_assignment(request):
    """Create a new assignment (T174)"""
    serializer = AssignmentCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    assignment = AssignmentService.create_assignment(serializer.validated_data)
    
    response_serializer = AssignmentResponseSerializer(assignment)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def list_assignments(request):
    """List assignments with optional filtering (T175)"""
    filters = {}
    
    # Extract filter parameters
    if request.query_params.get('course'):
        filters['course'] = request.query_params.get('course')
    if request.query_params.get('assignment_type'):
        filters['assignment_type'] = request.query_params.get('assignment_type')
    if request.query_params.get('is_published'):
        filters['is_published'] = request.query_params.get('is_published').lower() == 'true'
    if request.query_params.get('overdue_only'):
        filters['overdue_only'] = request.query_params.get('overdue_only').lower() == 'true'
    
    # Pagination parameters
    limit = int(request.query_params.get('limit', 50))
    offset = int(request.query_params.get('offset', 0))
    
    assignments, total = AssignmentService.list_assignments(
        filters=filters,
        limit=limit,
        offset=offset
    )
    
    serializer = AssignmentResponseSerializer(assignments, many=True)
    
    return Response({
        'results': serializer.data,
        'total': total,
        'limit': limit,
        'offset': offset,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def get_assignment(request, assignment_id):
    """Get a single assignment by ID"""
    assignment = AssignmentService.get_assignment(assignment_id)
    
    if not assignment:
        return Response(
            {'error': 'Assignment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = AssignmentResponseSerializer(assignment)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'update')
@audit_action(action='assignment.update')
def update_assignment(request, assignment_id):
    """Update an assignment"""
    serializer = AssignmentCreateSerializer(
        data=request.data,
        partial=request.method == 'PATCH'
    )
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    assignment = AssignmentService.update_assignment(
        assignment_id,
        serializer.validated_data
    )
    
    if not assignment:
        return Response(
            {'error': 'Assignment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    response_serializer = AssignmentResponseSerializer(assignment)
    return Response(response_serializer.data)
