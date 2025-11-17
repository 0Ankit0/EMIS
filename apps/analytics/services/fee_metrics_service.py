"""Fee metrics service"""
from typing import Dict, Any
from decimal import Decimal
from django.db.models import Sum, Count, Q
from apps.finance.models import Invoice, Payment


class FeeMetricsService:
    """Service for calculating fee collection metrics"""
    
    @staticmethod
    def calculate_collection() -> Dict[str, Any]:
        """Calculate fee collection metrics"""
        invoices = Invoice.objects.all()
        payments = Payment.objects.all()
        
        total_invoiced = invoices.aggregate(total=Sum('amount_due'))['total'] or Decimal('0.00')
        total_collected = payments.aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
        
        pending = invoices.filter(status__in=['pending', 'partial', 'overdue']).count()
        paid = invoices.filter(status='paid').count()
        
        collection_rate = round((float(total_collected) / float(total_invoiced) * 100) if total_invoiced > 0 else 0, 2)
        
        return {
            'total_invoiced': float(total_invoiced),
            'total_collected': float(total_collected),
            'pending_invoices': pending,
            'paid_invoices': paid,
            'collection_rate': collection_rate,
        }
