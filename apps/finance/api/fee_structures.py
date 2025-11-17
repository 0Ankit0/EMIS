"""Fee structure API endpoints"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from apps.finance.models.fee_structure import FeeStructure
from apps.finance.serializers.fee_structure import (
    FeeStructureCreateSerializer,
    FeeStructureUpdateSerializer,
    FeeStructureResponseSerializer,
)
from apps.finance.services.fee_structure_service import FeeStructureService
from apps.core.exceptions import EMISException
from apps.core.middleware.rbac import require_permission
from drf_spectacular.utils import extend_schema, OpenApiParameter


class FeeStructureViewSet(viewsets.ModelViewSet):
    """ViewSet for fee structure management"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = FeeStructureResponseSerializer
    
    def get_queryset(self):
        """Get queryset with filters"""
        queryset = FeeStructure.objects.all()
        
        # Filter parameters
        program = self.request.query_params.get('program')
        academic_year = self.request.query_params.get('academic_year')
        is_active = self.request.query_params.get('is_active')
        search = self.request.query_params.get('search')
        
        return FeeStructureService.list_fee_structures(
            program=program,
            academic_year=academic_year,
            is_active=is_active == 'true' if is_active else None,
            search=search
        )
    
    @extend_schema(
        request=FeeStructureCreateSerializer,
        responses={201: FeeStructureResponseSerializer}
    )
    @require_permission('finance', 'create')
    def create(self, request):
        """
        Create a new fee structure
        
        POST /fee-structures/
        """
        serializer = FeeStructureCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            fee_structure = FeeStructureService.create_fee_structure(
                serializer.validated_data
            )
            response_serializer = FeeStructureResponseSerializer(fee_structure)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        responses={200: FeeStructureResponseSerializer}
    )
    @require_permission('finance', 'read')
    def list(self, request):
        """
        Get list of fee structures
        
        GET /fee-structures/
        
        Query parameters:
        - program: Filter by program
        - academic_year: Filter by academic year
        - is_active: Filter by active status (true/false)
        - search: Search in name or code
        """
        queryset = self.get_queryset()
        
        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        responses={200: FeeStructureResponseSerializer}
    )
    @require_permission('finance', 'read')
    def retrieve(self, request, pk=None):
        """
        Get fee structure by ID
        
        GET /fee-structures/{id}/
        """
        try:
            fee_structure = FeeStructureService.get_fee_structure(pk)
            serializer = FeeStructureResponseSerializer(fee_structure)
            return Response(serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        request=FeeStructureUpdateSerializer,
        responses={200: FeeStructureResponseSerializer}
    )
    @require_permission('finance', 'update')
    def update(self, request, pk=None):
        """
        Update fee structure
        
        PUT /fee-structures/{id}/
        """
        serializer = FeeStructureUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            fee_structure = FeeStructureService.update_fee_structure(
                pk,
                serializer.validated_data
            )
            response_serializer = FeeStructureResponseSerializer(fee_structure)
            return Response(response_serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        request=FeeStructureUpdateSerializer,
        responses={200: FeeStructureResponseSerializer}
    )
    @require_permission('finance', 'update')
    def partial_update(self, request, pk=None):
        """
        Partially update fee structure
        
        PATCH /fee-structures/{id}/
        """
        serializer = FeeStructureUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            fee_structure = FeeStructureService.update_fee_structure(
                pk,
                serializer.validated_data
            )
            response_serializer = FeeStructureResponseSerializer(fee_structure)
            return Response(response_serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        responses={204: None}
    )
    @require_permission('finance', 'delete')
    def destroy(self, request, pk=None):
        """
        Delete fee structure (soft delete)
        
        DELETE /fee-structures/{id}/
        """
        try:
            FeeStructureService.delete_fee_structure(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
