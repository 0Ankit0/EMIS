from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.courses.models import Course
from apps.courses.serializers import (
    CourseCreateSerializer,
    CourseUpdateSerializer,
    CourseResponseSerializer,
    ModuleCreateSerializer,
    ModuleResponseSerializer,
)
from apps.courses.services import CourseService, ModuleService
from apps.core.middleware.rbac import require_permission
from apps.core.middleware.audit import audit_action


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'create')
@audit_action(action='course.create')
def create_course(request):
    """Create a new course (T169)"""
    serializer = CourseCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    course = CourseService.create_course(
        data=serializer.validated_data,
        created_by_id=request.user.id
    )
    
    response_serializer = CourseResponseSerializer(course)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def list_courses(request):
    """List courses with optional filtering and search (T170)"""
    filters = {}
    
    # Extract filter parameters
    if request.query_params.get('status'):
        filters['status'] = request.query_params.get('status')
    if request.query_params.get('department'):
        filters['department'] = request.query_params.get('department')
    if request.query_params.get('semester'):
        filters['semester'] = request.query_params.get('semester')
    if request.query_params.get('academic_year'):
        filters['academic_year'] = request.query_params.get('academic_year')
    if request.query_params.get('created_by'):
        filters['created_by'] = request.query_params.get('created_by')
    
    # Pagination parameters
    limit = int(request.query_params.get('limit', 50))
    offset = int(request.query_params.get('offset', 0))
    
    # Search parameter
    search = request.query_params.get('search')
    
    courses, total = CourseService.list_courses(
        filters=filters,
        search=search,
        limit=limit,
        offset=offset
    )
    
    serializer = CourseResponseSerializer(courses, many=True)
    
    return Response({
        'results': serializer.data,
        'total': total,
        'limit': limit,
        'offset': offset,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def get_course(request, course_id):
    """Get a single course by ID (T171)"""
    course = CourseService.get_course(course_id)
    
    if not course:
        return Response(
            {'error': 'Course not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = CourseResponseSerializer(course)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'update')
@audit_action(action='course.update')
def update_course(request, course_id):
    """Update a course (T172)"""
    serializer = CourseUpdateSerializer(data=request.data, partial=request.method == 'PATCH')
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    course = CourseService.update_course(course_id, serializer.validated_data)
    
    if not course:
        return Response(
            {'error': 'Course not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    response_serializer = CourseResponseSerializer(course)
    return Response(response_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'update')
@audit_action(action='course.module.create')
def create_module(request, course_id):
    """Create a module for a course (T173)"""
    # Add course_id to the request data
    data = request.data.copy()
    data['course'] = course_id
    
    serializer = ModuleCreateSerializer(data=data)
    if not serializer.is_valid():
        return Response(
            {'errors': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    module = ModuleService.create_module(serializer.validated_data)
    
    response_serializer = ModuleResponseSerializer(module)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('courses', 'read')
def list_modules(request, course_id):
    """List modules for a course"""
    published_only = request.query_params.get('published_only', 'false').lower() == 'true'
    
    modules = ModuleService.list_modules_for_course(
        course_id=course_id,
        published_only=published_only
    )
    
    serializer = ModuleResponseSerializer(modules, many=True)
    return Response(serializer.data)
