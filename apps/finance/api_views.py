"""Finance API Views"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Q
from django.utils import timezone

from .models import (
    FeeStructure, Invoice, Payment, ExpenseCategory, Expense,
    Budget, BudgetAllocation, Scholarship, ScholarshipApplication
)
from .serializers import (
    FeeStructureSerializer, InvoiceSerializer, PaymentSerializer,
    ExpenseCategorySerializer, ExpenseSerializer, BudgetSerializer,
    BudgetAllocationSerializer, ScholarshipSerializer, ScholarshipApplicationSerializer
)


class FeeStructureViewSet(viewsets.ModelViewSet):
    """ViewSet for FeeStructure"""
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['program', 'academic_year', 'semester', 'is_active']
    search_fields = ['name', 'code', 'program']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Invoice"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'status', 'academic_year', 'semester']
    search_fields = ['invoice_number', 'student__user__email']
    ordering_fields = ['invoice_date', 'due_date', 'amount_due']
    ordering = ['-invoice_date']
    
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
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['invoice', 'student', 'method']
    search_fields = ['receipt_number', 'transaction_id']
    ordering_fields = ['payment_date', 'amount_paid']
    ordering = ['-payment_date']
    
    def perform_create(self, serializer):
        serializer.save(processed_by=self.request.user)


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for ExpenseCategory"""
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering = ['name']


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for Expense"""
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'priority']
    search_fields = ['expense_number', 'title', 'vendor_name']
    ordering_fields = ['expense_date', 'total_amount']
    ordering = ['-expense_date']
    
    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve an expense"""
        expense = self.get_object()
        if expense.status != 'pending':
            return Response({'error': 'Only pending expenses can be approved'}, status=status.HTTP_400_BAD_REQUEST)
        
        expense.status = 'approved'
        expense.approved_by = request.user
        expense.approval_date = timezone.now()
        expense.save()
        
        return Response({'message': 'Expense approved successfully'})


class BudgetViewSet(viewsets.ModelViewSet):
    """ViewSet for Budget"""
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['fiscal_year', 'status', 'department']
    search_fields = ['name', 'code']
    ordering_fields = ['fiscal_year', 'start_date']
    ordering = ['-fiscal_year']


class BudgetAllocationViewSet(viewsets.ModelViewSet):
    """ViewSet for BudgetAllocation"""
    queryset = BudgetAllocation.objects.all()
    serializer_class = BudgetAllocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['budget', 'category']


class ScholarshipViewSet(viewsets.ModelViewSet):
    """ViewSet for Scholarship"""
    queryset = Scholarship.objects.all()
    serializer_class = ScholarshipSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['scholarship_type', 'status']
    search_fields = ['name', 'code']
    ordering = ['-created_at']


class ScholarshipApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for ScholarshipApplication"""
    queryset = ScholarshipApplication.objects.all()
    serializer_class = ScholarshipApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['scholarship', 'student', 'status']
    ordering = ['-application_date']
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve scholarship application"""
        application = self.get_object()
        if application.status != 'under_review':
            return Response({'error': 'Only applications under review can be approved'}, status=status.HTTP_400_BAD_REQUEST)
        
        awarded_amount = request.data.get('awarded_amount')
        if not awarded_amount:
            return Response({'error': 'awarded_amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        application.status = 'approved'
        application.awarded_amount = awarded_amount
        application.reviewed_by = request.user
        application.review_date = timezone.now()
        application.save()
        
        return Response({'message': 'Application approved successfully'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject scholarship application"""
        application = self.get_object()
        
        application.status = 'rejected'
        application.reviewed_by = request.user
        application.review_date = timezone.now()
        application.review_comments = request.data.get('review_comments', '')
        application.save()
        
        return Response({'message': 'Application rejected'})
