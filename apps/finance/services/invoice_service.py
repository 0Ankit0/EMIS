"""Invoice service for managing invoices"""
from typing import List, Optional, Dict, Any
from django.db.models import Q, QuerySet, Sum
from django.utils import timezone
from apps.finance.models.invoice import Invoice
from apps.finance.models.fee_structure import FeeStructure
from apps.students.models.student import Student
from apps.core.exceptions import EMISException
from decimal import Decimal
from datetime import date, datetime, timedelta


class InvoiceService:
    """Service for invoice generation and balance tracking"""
    
    @staticmethod
    def create_invoice(data: Dict[str, Any]) -> Invoice:
        """
        Create a new invoice
        
        Args:
            data: Invoice data including student, fee components, amounts
        
        Returns:
            Created invoice
        
        Raises:
            EMISException: If validation fails
        """
        student_id = data.get('student_id')
        fee_structure_id = data.get('fee_structure_id')
        
        # Validate student
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise EMISException(
                code="FINANCE_201",
                message=f"Student with id {student_id} not found"
            )
        
        # Get fee structure if provided
        fee_structure = None
        if fee_structure_id:
            try:
                fee_structure = FeeStructure.objects.get(id=fee_structure_id)
            except FeeStructure.DoesNotExist:
                raise EMISException(
                    code="FINANCE_101",
                    message=f"Fee structure with id {fee_structure_id} not found"
                )
        
        invoice = Invoice.objects.create(
            student=student,
            fee_structure=fee_structure,
            fee_components=data.get('fee_components', {}),
            amount_due=data.get('amount_due'),
            due_date=data.get('due_date'),
            description=data.get('description', ''),
            notes=data.get('notes', ''),
            academic_year=data.get('academic_year', ''),
            semester=data.get('semester', ''),
        )
        
        return invoice
    
    @staticmethod
    def generate_invoice_from_fee_structure(
        student_id: int,
        fee_structure_id: int,
        due_date: date,
        academic_year: str = '',
        semester: str = ''
    ) -> Invoice:
        """
        Generate invoice from fee structure
        
        Args:
            student_id: Student ID
            fee_structure_id: Fee structure ID
            due_date: Payment due date
            academic_year: Academic year
            semester: Semester
        
        Returns:
            Created invoice
        
        Raises:
            EMISException: If student or fee structure not found
        """
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            raise EMISException(
                code="FINANCE_201",
                message=f"Student with id {student_id} not found"
            )
        
        try:
            fee_structure = FeeStructure.objects.get(id=fee_structure_id)
        except FeeStructure.DoesNotExist:
            raise EMISException(
                code="FINANCE_101",
                message=f"Fee structure with id {fee_structure_id} not found"
            )
        
        # Create invoice from fee structure
        invoice = Invoice.objects.create(
            student=student,
            fee_structure=fee_structure,
            fee_components=fee_structure.components,
            amount_due=fee_structure.total_amount,
            due_date=due_date,
            description=f"Fee invoice for {fee_structure.name}",
            academic_year=academic_year or fee_structure.academic_year,
            semester=semester or fee_structure.semester,
        )
        
        return invoice
    
    @staticmethod
    def update_invoice(
        invoice_id: int,
        data: Dict[str, Any]
    ) -> Invoice:
        """
        Update invoice
        
        Args:
            invoice_id: Invoice ID
            data: Updated data
        
        Returns:
            Updated invoice
        
        Raises:
            EMISException: If invoice not found
        """
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise EMISException(
                code="FINANCE_202",
                message=f"Invoice with id {invoice_id} not found"
            )
        
        for key, value in data.items():
            setattr(invoice, key, value)
        
        invoice.save()
        return invoice
    
    @staticmethod
    def get_invoice(invoice_id: int) -> Invoice:
        """
        Get invoice by ID
        
        Args:
            invoice_id: Invoice ID
        
        Returns:
            Invoice
        
        Raises:
            EMISException: If invoice not found
        """
        try:
            return Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise EMISException(
                code="FINANCE_202",
                message=f"Invoice with id {invoice_id} not found"
            )
    
    @staticmethod
    def list_invoices(
        student_id: Optional[int] = None,
        status: Optional[str] = None,
        academic_year: Optional[str] = None,
        semester: Optional[str] = None,
        overdue_only: bool = False
    ) -> QuerySet[Invoice]:
        """
        List invoices with optional filters
        
        Args:
            student_id: Filter by student
            status: Filter by status
            academic_year: Filter by academic year
            semester: Filter by semester
            overdue_only: Filter overdue invoices
        
        Returns:
            QuerySet of invoices
        """
        queryset = Invoice.objects.all()
        
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        if status:
            queryset = queryset.filter(status=status)
        
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        if semester:
            queryset = queryset.filter(semester=semester)
        
        if overdue_only:
            queryset = queryset.filter(
                due_date__lt=date.today(),
                status__in=['pending', 'partial', 'overdue']
            )
        
        return queryset.order_by('-invoice_date')
    
    @staticmethod
    def get_student_balance(student_id: int) -> Decimal:
        """
        Get total outstanding balance for a student
        
        Args:
            student_id: Student ID
        
        Returns:
            Total balance
        """
        invoices = Invoice.objects.filter(
            student_id=student_id,
            status__in=['pending', 'partial', 'overdue']
        )
        
        total_balance = Decimal('0.00')
        for invoice in invoices:
            total_balance += invoice.balance
        
        return total_balance
    
    @staticmethod
    def apply_late_fee(invoice_id: int) -> Invoice:
        """
        Apply late fee to overdue invoice based on fee structure policy
        
        Args:
            invoice_id: Invoice ID
        
        Returns:
            Updated invoice
        
        Raises:
            EMISException: If invoice not found or not overdue
        """
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise EMISException(
                code="FINANCE_202",
                message=f"Invoice with id {invoice_id} not found"
            )
        
        if not invoice.is_overdue:
            raise EMISException(
                code="FINANCE_203",
                message="Invoice is not overdue"
            )
        
        # Calculate late fee from policy
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
        
        invoice.late_fee = late_fee
        invoice.save()
        
        return invoice
    
    @staticmethod
    def cancel_invoice(invoice_id: int, reason: str = '') -> Invoice:
        """
        Cancel an invoice
        
        Args:
            invoice_id: Invoice ID
            reason: Cancellation reason
        
        Returns:
            Updated invoice
        
        Raises:
            EMISException: If invoice not found or already paid
        """
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            raise EMISException(
                code="FINANCE_202",
                message=f"Invoice with id {invoice_id} not found"
            )
        
        if invoice.amount_paid > 0:
            raise EMISException(
                code="FINANCE_204",
                message="Cannot cancel invoice with payments"
            )
        
        invoice.status = 'cancelled'
        if reason:
            invoice.notes = f"{invoice.notes}\nCancellation reason: {reason}"
        invoice.save()
        
        return invoice
