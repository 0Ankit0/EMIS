"""Payment API endpoints"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.finance.models.payment import Payment
from apps.finance.serializers.payment import (
    PaymentCreateSerializer,
    PaymentResponseSerializer,
)
from apps.finance.services.payment_service import PaymentService
from apps.core.exceptions import EMISException
from apps.core.middleware.rbac import require_permission
from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import datetime


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for payment management"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentResponseSerializer
    http_method_names = ['get', 'post', 'head', 'options']  # No PUT/PATCH/DELETE for payments
    
    def get_queryset(self):
        """Get queryset with filters"""
        student_id = self.request.query_params.get('student_id')
        invoice_id = self.request.query_params.get('invoice_id')
        method = self.request.query_params.get('method')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        # Parse dates
        date_from_obj = None
        date_to_obj = None
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            except ValueError:
                pass
        
        return PaymentService.list_payments(
            student_id=int(student_id) if student_id else None,
            invoice_id=int(invoice_id) if invoice_id else None,
            method=method,
            date_from=date_from_obj,
            date_to=date_to_obj
        )
    
    @extend_schema(
        request=PaymentCreateSerializer,
        responses={201: PaymentResponseSerializer}
    )
    @require_permission('finance', 'create')
    def create(self, request):
        """
        Process a payment
        
        POST /payments/
        """
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Add processed_by from request user
            data = serializer.validated_data.copy()
            if not data.get('processed_by_id'):
                data['processed_by_id'] = request.user.id
            
            payment = PaymentService.process_payment(data)
            response_serializer = PaymentResponseSerializer(payment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        responses={200: PaymentResponseSerializer}
    )
    @require_permission('finance', 'read')
    def list(self, request):
        """
        Get list of payments
        
        GET /payments/
        
        Query parameters:
        - student_id: Filter by student
        - invoice_id: Filter by invoice
        - method: Filter by payment method
        - date_from: Filter payments from date (YYYY-MM-DD)
        - date_to: Filter payments to date (YYYY-MM-DD)
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
        responses={200: PaymentResponseSerializer}
    )
    @require_permission('finance', 'read')
    def retrieve(self, request, pk=None):
        """
        Get payment by ID
        
        GET /payments/{id}/
        """
        try:
            payment = PaymentService.get_payment(pk)
            serializer = PaymentResponseSerializer(payment)
            return Response(serializer.data)
        except EMISException as e:
            return Response(
                {'error': str(e), 'code': e.code},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        responses={200: dict}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @require_permission('finance', 'read')
    def summary(self, request):
        """
        Get payment summary for a student
        
        GET /payments/summary/?student_id=123
        """
        student_id = request.query_params.get('student_id')
        
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            summary = PaymentService.get_payment_summary(int(student_id))
            return Response(summary)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
