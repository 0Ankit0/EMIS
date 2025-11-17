"""Report service for fee collection summaries"""
from typing import List, Optional, Dict, Any
from django.db.models import Q, QuerySet, Sum, Count, Avg
from django.utils import timezone
from apps.finance.models.invoice import Invoice
from apps.finance.models.payment import Payment
from apps.finance.models.fee_structure import FeeStructure
from decimal import Decimal
from datetime import date, datetime, timedelta
import csv
import io


class ReportService:
    """Service for fee collection summary generation"""
    
    @staticmethod
    def generate_fee_collection_summary(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        academic_year: Optional[str] = None,
        semester: Optional[str] = None,
        program: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate fee collection summary report
        
        Args:
            date_from: Start date for report
            date_to: End date for report
            academic_year: Filter by academic year
            semester: Filter by semester
            program: Filter by program
        
        Returns:
            Dictionary with fee collection summary
        """
        # Build invoice queryset
        invoice_queryset = Invoice.objects.all()
        
        if date_from:
            invoice_queryset = invoice_queryset.filter(invoice_date__gte=date_from)
        
        if date_to:
            invoice_queryset = invoice_queryset.filter(invoice_date__lte=date_to)
        
        if academic_year:
            invoice_queryset = invoice_queryset.filter(academic_year=academic_year)
        
        if semester:
            invoice_queryset = invoice_queryset.filter(semester=semester)
        
        # Build payment queryset
        payment_queryset = Payment.objects.all()
        
        if date_from:
            payment_queryset = payment_queryset.filter(payment_date__gte=date_from)
        
        if date_to:
            payment_queryset = payment_queryset.filter(payment_date__lte=date_to)
        
        # Calculate totals
        total_invoiced = invoice_queryset.aggregate(
            total=Sum('amount_due')
        )['total'] or Decimal('0.00')
        
        total_collected = payment_queryset.aggregate(
            total=Sum('amount_paid')
        )['total'] or Decimal('0.00')
        
        total_late_fees = payment_queryset.aggregate(
            total=Sum('late_fee_applied')
        )['total'] or Decimal('0.00')
        
        # Count invoices by status
        invoice_counts = invoice_queryset.values('status').annotate(
            count=Count('id')
        )
        
        status_breakdown = {item['status']: item['count'] for item in invoice_counts}
        
        # Calculate outstanding balance
        outstanding_invoices = invoice_queryset.filter(
            status__in=['pending', 'partial', 'overdue']
        )
        
        total_outstanding = Decimal('0.00')
        for invoice in outstanding_invoices:
            total_outstanding += invoice.balance
        
        # Payment method breakdown
        payment_method_breakdown = payment_queryset.values('method').annotate(
            total=Sum('amount_paid'),
            count=Count('id')
        )
        
        method_breakdown = {
            item['method']: {
                'total': item['total'],
                'count': item['count']
            }
            for item in payment_method_breakdown
        }
        
        # Collection rate
        collection_rate = 0
        if total_invoiced > 0:
            collection_rate = float((total_collected / total_invoiced) * 100)
        
        return {
            'period': {
                'from': date_from.isoformat() if date_from else None,
                'to': date_to.isoformat() if date_to else None,
            },
            'filters': {
                'academic_year': academic_year,
                'semester': semester,
                'program': program,
            },
            'summary': {
                'total_invoiced': float(total_invoiced),
                'total_collected': float(total_collected),
                'total_late_fees': float(total_late_fees),
                'total_outstanding': float(total_outstanding),
                'collection_rate': round(collection_rate, 2),
            },
            'invoice_status_breakdown': status_breakdown,
            'payment_method_breakdown': method_breakdown,
            'totals': {
                'invoice_count': invoice_queryset.count(),
                'payment_count': payment_queryset.count(),
            }
        }
    
    @staticmethod
    def generate_student_fee_report(student_id: int) -> Dict[str, Any]:
        """
        Generate fee report for a specific student
        
        Args:
            student_id: Student ID
        
        Returns:
            Dictionary with student fee report
        """
        invoices = Invoice.objects.filter(student_id=student_id)
        payments = Payment.objects.filter(student_id=student_id)
        
        total_invoiced = invoices.aggregate(
            total=Sum('amount_due')
        )['total'] or Decimal('0.00')
        
        total_paid = payments.aggregate(
            total=Sum('amount_paid')
        )['total'] or Decimal('0.00')
        
        total_late_fees = payments.aggregate(
            total=Sum('late_fee_applied')
        )['total'] or Decimal('0.00')
        
        # Calculate outstanding balance
        outstanding_balance = Decimal('0.00')
        for invoice in invoices.filter(status__in=['pending', 'partial', 'overdue']):
            outstanding_balance += invoice.balance
        
        # Get overdue invoices
        overdue_invoices = invoices.filter(
            due_date__lt=date.today(),
            status__in=['pending', 'partial', 'overdue']
        )
        
        return {
            'student_id': student_id,
            'summary': {
                'total_invoiced': float(total_invoiced),
                'total_paid': float(total_paid),
                'total_late_fees': float(total_late_fees),
                'outstanding_balance': float(outstanding_balance),
            },
            'invoices': {
                'total': invoices.count(),
                'paid': invoices.filter(status='paid').count(),
                'pending': invoices.filter(status='pending').count(),
                'partial': invoices.filter(status='partial').count(),
                'overdue': overdue_invoices.count(),
            },
            'payments': {
                'total': payments.count(),
            }
        }
    
    @staticmethod
    def export_collection_report_csv(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        academic_year: Optional[str] = None,
        semester: Optional[str] = None
    ) -> str:
        """
        Export fee collection report as CSV
        
        Args:
            date_from: Start date
            date_to: End date
            academic_year: Academic year filter
            semester: Semester filter
        
        Returns:
            CSV content as string
        """
        # Build payment queryset
        queryset = Payment.objects.all()
        
        if date_from:
            queryset = queryset.filter(payment_date__gte=date_from)
        
        if date_to:
            queryset = queryset.filter(payment_date__lte=date_to)
        
        if academic_year or semester:
            invoice_filters = {}
            if academic_year:
                invoice_filters['invoice__academic_year'] = academic_year
            if semester:
                invoice_filters['invoice__semester'] = semester
            queryset = queryset.filter(**invoice_filters)
        
        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'Receipt Number',
            'Date',
            'Student ID',
            'Student Name',
            'Invoice Number',
            'Amount Paid',
            'Late Fee',
            'Payment Method',
            'Reference Number',
        ])
        
        # Write data
        for payment in queryset.select_related('student', 'invoice', 'student__user'):
            writer.writerow([
                payment.receipt_number,
                payment.payment_date.strftime('%Y-%m-%d'),
                payment.student_id,
                payment.student.user.get_full_name(),
                payment.invoice.invoice_number,
                float(payment.amount_paid),
                float(payment.late_fee_applied),
                payment.method,
                payment.reference_number,
            ])
        
        return output.getvalue()
    
    @staticmethod
    def get_outstanding_fees_report(
        academic_year: Optional[str] = None,
        semester: Optional[str] = None,
        overdue_only: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get report of outstanding fees
        
        Args:
            academic_year: Filter by academic year
            semester: Filter by semester
            overdue_only: Only show overdue invoices
        
        Returns:
            List of outstanding fee records
        """
        queryset = Invoice.objects.filter(
            status__in=['pending', 'partial', 'overdue']
        ).select_related('student', 'student__user')
        
        if academic_year:
            queryset = queryset.filter(academic_year=academic_year)
        
        if semester:
            queryset = queryset.filter(semester=semester)
        
        if overdue_only:
            queryset = queryset.filter(due_date__lt=date.today())
        
        outstanding_fees = []
        for invoice in queryset:
            outstanding_fees.append({
                'student_id': invoice.student_id,
                'student_name': invoice.student.user.get_full_name(),
                'student_email': invoice.student.user.email,
                'invoice_number': invoice.invoice_number,
                'invoice_date': invoice.invoice_date.isoformat(),
                'due_date': invoice.due_date.isoformat(),
                'amount_due': float(invoice.amount_due),
                'amount_paid': float(invoice.amount_paid),
                'late_fee': float(invoice.late_fee),
                'balance': float(invoice.balance),
                'status': invoice.status,
                'is_overdue': invoice.is_overdue,
                'days_overdue': (date.today() - invoice.due_date).days if invoice.is_overdue else 0,
            })
        
        return outstanding_fees
