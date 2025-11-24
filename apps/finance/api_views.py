"""Finance API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone

from .models import (
    FeeStructure, Invoice, Payment,
)
from .serializers import (
    FeeStructureResponseSerializer, 
    InvoiceResponseSerializer, 
    PaymentResponseSerializer,
    FeeStructureCreateSerializer,
    FeeStructureUpdateSerializer,
    InvoiceCreateSerializer,
    InvoiceUpdateSerializer,
    PaymentCreateSerializer,
)


class FeeStructureViewSet(viewsets.ModelViewSet):
    """ViewSet for FeeStructure"""
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['program', 'academic_year', 'semester', 'is_active']
    search_fields = ['name', 'code', 'program']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return FeeStructureCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return FeeStructureUpdateSerializer
        return FeeStructureResponseSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Invoice"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'status', 'academic_year', 'semester']
    search_fields = ['invoice_number', 'student__user__email']
    ordering_fields = ['invoice_date', 'due_date', 'amount_due']
    ordering = ['-invoice_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return InvoiceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return InvoiceUpdateSerializer
        return InvoiceResponseSerializer
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get invoice statistics"""
        queryset = self.get_queryset()
        stats = {
            'total_invoices': queryset.count(),
            'total_amount': queryset.aggregate(Sum('amount_due'))['amount_due__sum'] or 0,
            'total_paid': queryset.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0,
            'by_status': {
                'pending': queryset.filter(status='pending').count(),
                'partial': queryset.filter(status='partial').count(),
                'paid': queryset.filter(status='paid').count(),
                'overdue': queryset.filter(status='overdue').count(),
            }
        }
        return Response(stats)


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment"""
    queryset = Payment.objects.all()
    serializer_class = PaymentResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice', 'student', 'method']
    search_fields = ['receipt_number', 'transaction_id']
    ordering_fields = ['payment_date', 'amount_paid']
    ordering = ['-payment_date']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentResponseSerializer
    
    def perform_create(self, serializer):
        serializer.save(processed_by=self.request.user)
