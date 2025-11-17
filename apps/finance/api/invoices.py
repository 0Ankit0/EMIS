"""Invoice API endpoints"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.finance.models.invoice import Invoice
from apps.finance.serializers.invoice import (
    InvoiceCreateSerializer,
    InvoiceUpdateSerializer,
    InvoiceResponseSerializer,
)
from apps.finance.services.invoice_service import InvoiceService
from apps.core.exceptions import EMISException
from apps.core.middleware.rbac import require_permission
from drf_spectacular.utils import extend_schema, OpenApiParameter


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for invoice management"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = InvoiceResponseSerializer
    
    def get_queryset(self):
        """Get queryset with filters"""
        student_id = self.request.query_params.get('student_id')
        status_filter = self.request.query_params.get('status')
        academic_year = self.request.query_params.get('academic_year')
        semester = self.request.query_params.get('semester')
        overdue_only = self.request.query_params.get('overdue_only') == 'true'
        
        return InvoiceService.list_invoices(
            student_id=int(student_id) if student_id else None,
            status=status_filter,
            academic_year=academic_year,
            semester=semester,
            overdue_only=overdue_only
        )
    
    @extend_schema(
        request=InvoiceCreateSerializer,
        responses={201: InvoiceResponseSerializer}
    )
    @require_permission('finance', 'create')
    def create(self, request):
        """
        Create a new invoice
        
        POST /invoices/
        """
        serializer = InvoiceCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            invoice = InvoiceService.create_invoice(serializer.validated_data)
            response_serializer = InvoiceResponseSerializer(invoice)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        responses={200: InvoiceResponseSerializer}
    )
    @require_permission('finance', 'read')
    def list(self, request):
        """
        Get list of invoices
        
        GET /invoices/
        
        Query parameters:
        - student_id: Filter by student
        - status: Filter by status (pending, partial, paid, overdue, cancelled)
        - academic_year: Filter by academic year
        - semester: Filter by semester
        - overdue_only: Filter overdue invoices (true/false)
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
        responses={200: InvoiceResponseSerializer}
    )
    @require_permission('finance', 'read')
    def retrieve(self, request, pk=None):
        """
        Get invoice by ID
        
        GET /invoices/{id}/
        """
        try:
            invoice = InvoiceService.get_invoice(pk)
            serializer = InvoiceResponseSerializer(invoice)
            return Response(serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        request=InvoiceUpdateSerializer,
        responses={200: InvoiceResponseSerializer}
    )
    @require_permission('finance', 'update')
    def update(self, request, pk=None):
        """
        Update invoice
        
        PUT /invoices/{id}/
        """
        serializer = InvoiceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            invoice = InvoiceService.update_invoice(pk, serializer.validated_data)
            response_serializer = InvoiceResponseSerializer(invoice)
            return Response(response_serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        request=InvoiceUpdateSerializer,
        responses={200: InvoiceResponseSerializer}
    )
    @require_permission('finance', 'update')
    def partial_update(self, request, pk=None):
        """
        Partially update invoice
        
        PATCH /invoices/{id}/
        """
        serializer = InvoiceUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        try:
            invoice = InvoiceService.update_invoice(pk, serializer.validated_data)
            response_serializer = InvoiceResponseSerializer(invoice)
            return Response(response_serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        responses={200: InvoiceResponseSerializer}
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    @require_permission('finance', 'update')
    def apply_late_fee(self, request, pk=None):
        """
        Apply late fee to invoice
        
        POST /invoices/{id}/apply-late-fee/
        """
        try:
            invoice = InvoiceService.apply_late_fee(pk)
            serializer = InvoiceResponseSerializer(invoice)
            return Response(serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        responses={200: InvoiceResponseSerializer}
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    @require_permission('finance', 'update')
    def cancel(self, request, pk=None):
        """
        Cancel invoice
        
        POST /invoices/{id}/cancel/
        """
        reason = request.data.get('reason', '')
        
        try:
            invoice = InvoiceService.cancel_invoice(pk, reason)
            serializer = InvoiceResponseSerializer(invoice)
            return Response(serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
