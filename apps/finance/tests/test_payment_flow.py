"""Tests for payment processing"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from apps.finance.services.fee_structure_service import FeeStructureService
from apps.finance.services.invoice_service import InvoiceService
from apps.finance.services.payment_service import PaymentService
from apps.students.models.student import Student

User = get_user_model()


@pytest.mark.django_db
class TestPaymentFlow:
    """Test payment processing"""
    
    @pytest.fixture
    def setup_data(self):
        """Setup student, fee structure, and invoice"""
        user = User.objects.create_user(
            email='student@test.com',
            password='student123',
            first_name='Test',
            last_name='Student'
        )
        student = Student.objects.create(
            user=user,
            student_id='ST2024001',
            date_of_birth=date(2000, 1, 1)
        )
        
        fee_structure = FeeStructureService.create_fee_structure({
            'name': 'Test Fee',
            'code': 'TEST-2024',
            'program': 'Test Program',
            'components': {'tuition': 5000},
            'late_fee_policy': {'percentage': 5, 'grace_days': 7},
            'valid_from': date.today(),
            'valid_to': date.today() + timedelta(days=365),
            'is_active': True
        })
        
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() + timedelta(days=30)
        )
        
        return {'student': student, 'fee_structure': fee_structure, 'invoice': invoice}
    
    def test_process_payment(self, setup_data):
        """Test processing a payment"""
        invoice = setup_data['invoice']
        
        payment_data = {
            'invoice_id': invoice.id,
            'amount_paid': Decimal('5000.00'),
            'method': 'cash'
        }
        
        payment = PaymentService.process_payment(payment_data)
        
        assert payment.amount_paid == Decimal('5000.00')
        assert payment.invoice == invoice
        assert payment.receipt_number is not None
    
    def test_process_partial_payment(self, setup_data):
        """Test processing partial payment"""
        invoice = setup_data['invoice']
        
        payment = PaymentService.process_partial_payment(
            invoice_id=invoice.id,
            amount_paid=Decimal('2000.00'),
            method='card'
        )
        
        assert payment.amount_paid == Decimal('2000.00')
        
        # Check invoice was updated
        invoice.refresh_from_db()
        assert invoice.amount_paid == Decimal('2000.00')
        assert invoice.status == 'partial'
    
    def test_payment_with_late_fee(self, setup_data):
        """Test payment processing with late fee calculation"""
        invoice = setup_data['invoice']
        
        # Make invoice overdue
        invoice.due_date = date.today() - timedelta(days=10)
        invoice.save()
        
        payment = PaymentService.process_partial_payment(
            invoice_id=invoice.id,
            amount_paid=Decimal('5000.00'),
            method='online'
        )
        
        # Late fee should be applied
        assert payment.late_fee_applied > 0
    
    def test_payment_summary(self, setup_data):
        """Test payment summary generation"""
        student = setup_data['student']
        invoice = setup_data['invoice']
        
        # Make payment
        PaymentService.process_payment({
            'invoice_id': invoice.id,
            'amount_paid': Decimal('5000.00'),
            'method': 'cash'
        })
        
        summary = PaymentService.get_payment_summary(student.id)
        
        assert summary['total_paid'] == Decimal('5000.00')
        assert summary['payment_count'] == 1


@pytest.mark.django_db
class TestEdgeCases:
    """Test edge cases for finance module"""
    
    @pytest.fixture
    def setup_data(self):
        """Setup data"""
        user = User.objects.create_user(
            email='student@test.com',
            password='student123',
            first_name='Test',
            last_name='Student'
        )
        student = Student.objects.create(
            user=user,
            student_id='ST2024001',
            date_of_birth=date(2000, 1, 1)
        )
        
        fee_structure = FeeStructureService.create_fee_structure({
            'name': 'Test Fee',
            'code': 'TEST-2024',
            'program': 'Test Program',
            'components': {'tuition': 5000},
            'valid_from': date.today(),
            'valid_to': date.today() + timedelta(days=365),
            'is_active': True
        })
        
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() + timedelta(days=30)
        )
        
        return {'student': student, 'fee_structure': fee_structure, 'invoice': invoice}
    
    def test_payment_exceeding_balance(self, setup_data):
        """Test payment amount exceeding invoice balance"""
        from apps.core.exceptions import EMISException
        
        invoice = setup_data['invoice']
        
        # Try to pay more than balance
        with pytest.raises(EMISException) as exc_info:
            PaymentService.process_payment({
                'invoice_id': invoice.id,
                'amount_paid': Decimal('10000.00'),
                'method': 'cash'
            })
        
        assert 'exceeds invoice balance' in str(exc_info.value)
    
    def test_overdue_fee_payment_reversal(self, setup_data):
        """Test handling of overdue fee payment scenarios"""
        invoice = setup_data['invoice']
        
        # Make invoice overdue
        invoice.due_date = date.today() - timedelta(days=10)
        invoice.save()
        
        # Apply late fee
        InvoiceService.apply_late_fee(invoice.id)
        invoice.refresh_from_db()
        
        # Payment should cover amount_due + late_fee
        total_due = invoice.amount_due + invoice.late_fee
        
        payment = PaymentService.process_payment({
            'invoice_id': invoice.id,
            'amount_paid': total_due,
            'method': 'online'
        })
        
        invoice.refresh_from_db()
        assert invoice.is_paid is True
