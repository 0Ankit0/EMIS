"""Tests for invoice flow"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from apps.finance.models.fee_structure import FeeStructure
from apps.finance.models.invoice import Invoice
from apps.finance.services.invoice_service import InvoiceService
from apps.finance.services.fee_structure_service import FeeStructureService
from apps.students.models.student import Student
from apps.students.models.enrollment import Enrollment

User = get_user_model()


@pytest.mark.django_db
class TestInvoiceFlow:
    """Test invoice generation and management"""
    
    @pytest.fixture
    def student(self):
        """Create test student"""
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
        return student
    
    @pytest.fixture
    def fee_structure(self):
        """Create test fee structure"""
        return FeeStructureService.create_fee_structure({
            'name': 'Test Fee Structure',
            'code': 'TEST-2024',
            'program': 'Test Program',
            'components': {
                'tuition': 5000,
                'lab': 500
            },
            'late_fee_policy': {
                'percentage': 5,
                'grace_days': 7
            },
            'valid_from': date.today(),
            'valid_to': date.today() + timedelta(days=365),
            'is_active': True
        })
    
    def test_create_invoice(self, student, fee_structure):
        """Test creating an invoice"""
        invoice_data = {
            'student_id': student.id,
            'fee_structure_id': fee_structure.id,
            'fee_components': fee_structure.components,
            'amount_due': fee_structure.total_amount,
            'due_date': date.today() + timedelta(days=30)
        }
        
        invoice = InvoiceService.create_invoice(invoice_data)
        
        assert invoice.student == student
        assert invoice.fee_structure == fee_structure
        assert invoice.amount_due == fee_structure.total_amount
        assert invoice.status == 'pending'
        assert invoice.invoice_number is not None
    
    def test_generate_invoice_from_fee_structure(self, student, fee_structure):
        """Test generating invoice from fee structure"""
        due_date = date.today() + timedelta(days=30)
        
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=due_date,
            academic_year='2024',
            semester='Fall'
        )
        
        assert invoice.student == student
        assert invoice.amount_due == fee_structure.total_amount
        assert invoice.due_date == due_date
    
    def test_invoice_balance_calculation(self, student, fee_structure):
        """Test invoice balance calculation"""
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() + timedelta(days=30)
        )
        
        # Initial balance should equal amount_due
        assert invoice.balance == invoice.amount_due
        
        # Simulate partial payment
        invoice.amount_paid = Decimal('2000.00')
        invoice.save()
        
        expected_balance = invoice.amount_due - invoice.amount_paid
        assert invoice.balance == expected_balance
    
    def test_invoice_overdue_status(self, student, fee_structure):
        """Test invoice overdue status"""
        # Create invoice with past due date
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() - timedelta(days=10)
        )
        
        assert invoice.is_overdue is True
    
    def test_apply_late_fee(self, student, fee_structure):
        """Test applying late fee to overdue invoice"""
        # Create overdue invoice
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() - timedelta(days=10)
        )
        
        # Apply late fee
        updated_invoice = InvoiceService.apply_late_fee(invoice.id)
        
        # Should have late fee applied (5% of amount_due)
        expected_late_fee = invoice.amount_due * Decimal('0.05')
        assert updated_invoice.late_fee == expected_late_fee
    
    def test_list_invoices_with_filters(self, student, fee_structure):
        """Test listing invoices with filters"""
        # Create multiple invoices
        for i in range(3):
            InvoiceService.generate_invoice_from_fee_structure(
                student_id=student.id,
                fee_structure_id=fee_structure.id,
                due_date=date.today() + timedelta(days=30 + i)
            )
        
        # Filter by student
        invoices = InvoiceService.list_invoices(student_id=student.id)
        assert invoices.count() == 3
    
    def test_cancel_invoice(self, student, fee_structure):
        """Test cancelling an invoice"""
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() + timedelta(days=30)
        )
        
        cancelled = InvoiceService.cancel_invoice(invoice.id, reason='Test cancellation')
        
        assert cancelled.status == 'cancelled'
        assert 'Test cancellation' in cancelled.notes
    
    def test_get_student_balance(self, student, fee_structure):
        """Test getting student's total outstanding balance"""
        # Create multiple invoices
        for i in range(2):
            InvoiceService.generate_invoice_from_fee_structure(
                student_id=student.id,
                fee_structure_id=fee_structure.id,
                due_date=date.today() + timedelta(days=30)
            )
        
        balance = InvoiceService.get_student_balance(student.id)
        
        # Should be 2 * fee_structure.total_amount
        expected_balance = fee_structure.total_amount * 2
        assert balance == expected_balance
