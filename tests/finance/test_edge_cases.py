"""Additional edge case tests for finance"""
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
class TestFinanceEdgeCases:
    """Test edge cases for finance operations"""
    
    @pytest.fixture
    def setup_data(self):
        """Setup test data"""
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
            'name': 'Test Fee with Scholarship',
            'code': 'TEST-SCH-2024',
            'program': 'Test Program',
            'components': {
                'tuition': 5000,
                'lab': 500
            },
            'late_fee_policy': {
                'percentage': 5,
                'grace_days': 7,
                'flat_fee': 100
            },
            'installment_rules': {
                'enabled': True,
                'count': 3
            },
            'valid_from': date.today(),
            'valid_to': date.today() + timedelta(days=365),
            'is_active': True
        })
        
        return {'student': student, 'fee_structure': fee_structure}
    
    def test_partial_installment_with_scholarship(self, setup_data):
        """Test fee payment with partial installment and scholarship adjustment"""
        student = setup_data['student']
        fee_structure = setup_data['fee_structure']
        
        # Create invoice with scholarship discount
        original_amount = fee_structure.total_amount
        scholarship_amount = Decimal('1000.00')
        discounted_amount = original_amount - scholarship_amount
        
        invoice = InvoiceService.create_invoice({
            'student_id': student.id,
            'fee_structure_id': fee_structure.id,
            'fee_components': fee_structure.components,
            'amount_due': discounted_amount,
            'due_date': date.today() + timedelta(days=30),
            'description': f'Fee with ${scholarship_amount} scholarship'
        })
        
        # Make installment payment (1/3 of discounted amount)
        installment_amount = discounted_amount / 3
        
        payment1 = PaymentService.process_partial_payment(
            invoice_id=invoice.id,
            amount_paid=installment_amount,
            method='online',
            remarks='First installment'
        )
        
        assert payment1.amount_paid == installment_amount
        
        invoice.refresh_from_db()
        assert invoice.status == 'partial'
        assert invoice.balance == discounted_amount - installment_amount
    
    def test_multiple_payments_on_same_invoice(self, setup_data):
        """Test multiple partial payments on the same invoice"""
        student = setup_data['student']
        fee_structure = setup_data['fee_structure']
        
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() + timedelta(days=30)
        )
        
        # Make three partial payments
        payment1 = PaymentService.process_partial_payment(
            invoice_id=invoice.id,
            amount_paid=Decimal('2000.00'),
            method='cash'
        )
        
        payment2 = PaymentService.process_partial_payment(
            invoice_id=invoice.id,
            amount_paid=Decimal('2000.00'),
            method='card'
        )
        
        payment3 = PaymentService.process_partial_payment(
            invoice_id=invoice.id,
            amount_paid=Decimal('1500.00'),
            method='online'
        )
        
        invoice.refresh_from_db()
        
        assert invoice.amount_paid == Decimal('5500.00')
        assert invoice.status == 'paid'
        assert invoice.is_paid is True
    
    def test_late_fee_with_grace_period(self, setup_data):
        """Test late fee calculation respecting grace period"""
        student = setup_data['student']
        fee_structure = setup_data['fee_structure']
        
        # Create invoice with due date just past grace period
        grace_days = fee_structure.late_fee_policy['grace_days']
        due_date = date.today() - timedelta(days=grace_days + 1)
        
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=due_date
        )
        
        # Calculate late fee
        late_fee = PaymentService.calculate_late_fee(invoice)
        
        # Should apply 5% late fee
        expected_late_fee = invoice.amount_due * Decimal('0.05')
        assert late_fee == expected_late_fee
    
    def test_invoice_within_grace_period_no_late_fee(self, setup_data):
        """Test that no late fee is applied within grace period"""
        student = setup_data['student']
        fee_structure = setup_data['fee_structure']
        
        # Create invoice with due date within grace period
        grace_days = fee_structure.late_fee_policy['grace_days']
        due_date = date.today() - timedelta(days=grace_days - 1)
        
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=due_date
        )
        
        # Calculate late fee
        late_fee = PaymentService.calculate_late_fee(invoice)
        
        # Should not apply late fee
        assert late_fee == Decimal('0.00')
    
    def test_cannot_cancel_invoice_with_payments(self, setup_data):
        """Test that invoice with payments cannot be cancelled"""
        from apps.core.exceptions import EMISException
        
        student = setup_data['student']
        fee_structure = setup_data['fee_structure']
        
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() + timedelta(days=30)
        )
        
        # Make a payment
        PaymentService.process_partial_payment(
            invoice_id=invoice.id,
            amount_paid=Decimal('1000.00'),
            method='cash'
        )
        
        # Try to cancel
        with pytest.raises(EMISException) as exc_info:
            InvoiceService.cancel_invoice(invoice.id)
        
        assert 'Cannot cancel invoice with payments' in str(exc_info.value)
