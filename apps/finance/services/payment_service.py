"""Payment service for processing payments"""
from typing import List, Optional, Dict, Any
from django.db.models import Q, QuerySet, Sum
from django.utils import timezone
from apps.finance.models.payment import Payment
from apps.finance.models.invoice import Invoice
from apps.students.models.student import Student
from django.contrib.auth import get_user_model
from apps.core.exceptions import EMISException

User = get_user_model()
from decimal import Decimal
from datetime import date, datetime


class PaymentService:
    """Service for payment processing and late fee calculation"""
    
    @staticmethod
    def process_payment(data: Dict[str, Any]) -> Payment:
        """
        Process a payment
        
        Args:
            data: Payment data including invoice, amount, method
        
        Returns:
            Created payment
        
        Raises:
            EMISException: If validation fails
        """
        invoice_id = data.get('invoice_id')
        amount_paid = data.get('amount_paid')
        
        # Validate invoice
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise EMISException(
                code="FINANCE_202",
                message=f"Invoice with id {invoice_id} not found"
            )
        
        # Validate amount
        if amount_paid <= 0:
            raise EMISException(
                code="FINANCE_301",
                message="Payment amount must be greater than zero"
            )
        
        # Check if payment exceeds balance
        balance = invoice.balance
        if amount_paid > balance:
            raise EMISException(
                code="FINANCE_302",
                message=f"Payment amount (${amount_paid}) exceeds invoice balance (${balance})"
            )
        
        # Calculate late fee if invoice is overdue
        late_fee_applied = Decimal('0.00')
        if invoice.is_overdue and invoice.late_fee > 0:
            # Apply late fee from invoice
            late_fee_applied = data.get('late_fee_applied', invoice.late_fee)
        
        # Get processed_by user
        processed_by = None
        if data.get('processed_by_id'):
            try:
                processed_by = User.objects.get(id=data['processed_by_id'])
            except User.DoesNotExist:
                pass
        
        # Create payment
        payment = Payment.objects.create(
            invoice=invoice,
            student=invoice.student,
            amount_paid=amount_paid,
            late_fee_applied=late_fee_applied,
            method=data.get('method'),
            payment_date=data.get('payment_date', timezone.now()),
            reference_number=data.get('reference_number', ''),
            remarks=data.get('remarks', ''),
            processed_by=processed_by,
            transaction_id=data.get('transaction_id', ''),
        )
        
        return payment
    
    @staticmethod
    def get_payment(payment_id: int) -> Payment:
        """
        Get payment by ID
        
        Args:
            payment_id: Payment ID
        
        Returns:
            Payment
        
        Raises:
            EMISException: If payment not found
        """
        try:
            return Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            raise EMISException(
                code="FINANCE_303",
                message=f"Payment with id {payment_id} not found"
            )
    
    @staticmethod
    def list_payments(
        student_id: Optional[int] = None,
        invoice_id: Optional[int] = None,
        method: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> QuerySet[Payment]:
        """
        List payments with optional filters
        
        Args:
            student_id: Filter by student
            invoice_id: Filter by invoice
            method: Filter by payment method
            date_from: Filter payments from date
            date_to: Filter payments to date
        
        Returns:
            QuerySet of payments
        """
        queryset = Payment.objects.all()
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)
        
        if method:
            queryset = queryset.filter(method=method)
        
        if date_from:
            queryset = queryset.filter(payment_date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(payment_date__lte=date_to)
        
        return queryset.order_by('-payment_date')
    
    @staticmethod
    def get_student_payment_history(student_id: int) -> QuerySet[Payment]:
        """
        Get payment history for a student
        
        Args:
            student_id: Student ID
        
        Returns:
            QuerySet of payments
        """
        return Payment.objects.filter(student_id=student_id).order_by('-payment_date')
    
    @staticmethod
    def calculate_late_fee(invoice: Invoice) -> Decimal:
        """
        Calculate late fee for an invoice
        
        Args:
            invoice: Invoice object
        
        Returns:
            Late fee amount
        """
        if not invoice.is_overdue:
            return Decimal('0.00')
        
        late_fee = Decimal('0.00')
        
        if invoice.fee_structure and invoice.fee_structure.late_fee_policy:
            policy = invoice.fee_structure.late_fee_policy
            
            # Check grace period
            grace_days = policy.get('grace_days', 0)
            days_overdue = (date.today() - invoice.due_date).days
            
            if days_overdue > grace_days:
                # Calculate based on percentage or flat fee
                if 'percentage' in policy:
                    percentage = Decimal(str(policy['percentage'])) / 100
                    late_fee = invoice.amount_due * percentage
                elif 'flat_fee' in policy:
                    late_fee = Decimal(str(policy['flat_fee']))
                
                # Apply daily accumulation if configured
                if policy.get('daily_accumulation', False):
                    days_to_charge = days_overdue - grace_days
                    if 'daily_rate' in policy:
                        daily_rate = Decimal(str(policy['daily_rate']))
                        late_fee += daily_rate * days_to_charge
        
        return late_fee
    
    @staticmethod
    def process_partial_payment(
        invoice_id: int,
        amount_paid: Decimal,
        method: str,
        processed_by_id: Optional[int] = None,
        reference_number: str = '',
        remarks: str = ''
    ) -> Payment:
        """
        Process a partial payment
        
        Args:
            invoice_id: Invoice ID
            amount_paid: Amount being paid
            method: Payment method
            processed_by_id: ID of user processing payment
            reference_number: Payment reference
            remarks: Additional remarks
        
        Returns:
            Created payment
        
        Raises:
            EMISException: If validation fails
        """
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise EMISException(
                code="FINANCE_202",
                message=f"Invoice with id {invoice_id} not found"
            )
        
        # Validate amount
        balance = invoice.balance
        if amount_paid > balance:
            raise EMISException(
                code="FINANCE_302",
                message=f"Payment amount (${amount_paid}) exceeds invoice balance (${balance})"
            )
        
        # Calculate late fee if applicable
        late_fee_applied = Decimal('0.00')
        if invoice.is_overdue:
            late_fee_applied = PaymentService.calculate_late_fee(invoice)
            # Update invoice late fee
            invoice.late_fee = late_fee_applied
            invoice.save()
        
        # Get processed_by user
        processed_by = None
        if processed_by_id:
            try:
                processed_by = User.objects.get(id=processed_by_id)
            except User.DoesNotExist:
                pass
        
        # Create payment
        payment = Payment.objects.create(
            invoice=invoice,
            student=invoice.student,
            amount_paid=amount_paid,
            late_fee_applied=late_fee_applied,
            method=method,
            reference_number=reference_number,
            remarks=f"Partial payment. {remarks}".strip(),
            processed_by=processed_by,
        )
        
        return payment
    
    @staticmethod
    def get_payment_summary(student_id: int) -> Dict[str, Any]:
        """
        Get payment summary for a student
        
        Args:
            student_id: Student ID
        
        Returns:
            Dictionary with payment summary
        """
        payments = Payment.objects.filter(student_id=student_id)
        
        total_paid = payments.aggregate(
            total=Sum('amount_paid')
        )['total'] or Decimal('0.00')
        
        total_late_fees = payments.aggregate(
            total=Sum('late_fee_applied')
        )['total'] or Decimal('0.00')
        
        # Get pending invoices
        from apps.finance.services.invoice_service import InvoiceService
        outstanding_balance = InvoiceService.get_student_balance(student_id)
        
        return {
            'total_paid': total_paid,
            'total_late_fees': total_late_fees,
            'outstanding_balance': outstanding_balance,
            'payment_count': payments.count(),
        }
