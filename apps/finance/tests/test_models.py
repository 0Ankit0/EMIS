"""Finance App Tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from apps.finance.models import FeeStructure, Invoice, Payment, ExpenseCategory, Expense, Budget, BudgetAllocation, Scholarship, ScholarshipApplication

User = get_user_model()


class FeeStructureTestCase(TestCase):
    """Test FeeStructure model"""
    
    def setUp(self):
        self.fee_structure = FeeStructure.objects.create(
            name='Computer Science BS Fee',
            code='CS-BS-2024',
            program='Computer Science BS',
            academic_year='2024-2025',
            components={'tuition': 5000, 'lab': 500, 'library': 100},
            total_amount=5600,
            valid_from=timezone.now().date(),
            valid_to=timezone.now().date() + timedelta(days=365)
        )
    
    def test_calculate_total(self):
        """Test total calculation from components"""
        calculated = self.fee_structure.calculate_total()
        self.assertEqual(calculated, 5600)
    
    def test_fee_structure_str(self):
        """Test string representation"""
        self.assertEqual(
            str(self.fee_structure),
            'CS-BS-2024 - Computer Science BS Fee'
        )


class InvoiceTestCase(TestCase):
    """Test Invoice model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpass123'
        )
        
        # Assuming Student model exists
        # self.student = Student.objects.create(user=self.user, ...)
    
    def test_invoice_number_generation(self):
        """Test automatic invoice number generation"""
        # Invoice creation test would go here
        pass
    
    def test_balance_calculation(self):
        """Test invoice balance calculation"""
        # Balance calculation test would go here
        pass


class PaymentTestCase(TestCase):
    """Test Payment model"""
    
    def test_receipt_number_generation(self):
        """Test automatic receipt number generation"""
        pass
    
    def test_invoice_update_on_payment(self):
        """Test that invoice is updated when payment is made"""
        pass


class ExpenseTestCase(TestCase):
    """Test Expense model"""
    
    def setUp(self):
        self.category = ExpenseCategory.objects.create(
            name='Office Supplies',
            code='OFFICE-SUP'
        )
        
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
    
    def test_expense_number_generation(self):
        """Test automatic expense number generation"""
        expense = Expense.objects.create(
            category=self.category,
            title='Printer Paper',
            description='A4 size paper',
            amount=100,
            tax_amount=18,
            requested_by=self.user
        )
        
        self.assertTrue(expense.expense_number.startswith('EXP-'))
    
    def test_total_amount_calculation(self):
        """Test total amount calculation"""
        expense = Expense.objects.create(
            category=self.category,
            title='Printer',
            description='Laser printer',
            amount=500,
            tax_amount=90,
            requested_by=self.user
        )
        
        self.assertEqual(expense.total_amount, Decimal('590.00'))


class BudgetTestCase(TestCase):
    """Test Budget model"""
    
    def test_balance_property(self):
        """Test budget balance calculation"""
        budget = Budget.objects.create(
            name='Annual Budget 2024',
            code='BUD-2024',
            fiscal_year='2024',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=365),
            total_allocated=100000,
            total_spent=25000
        )
        
        self.assertEqual(budget.balance, 75000)
    
    def test_utilization_percentage(self):
        """Test utilization percentage calculation"""
        budget = Budget.objects.create(
            name='Q1 Budget',
            code='BUD-Q1-2024',
            fiscal_year='2024',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=90),
            total_allocated=50000,
            total_spent=12500
        )
        
        self.assertEqual(budget.utilization_percentage, 25.0)


class ScholarshipTestCase(TestCase):
    """Test Scholarship model"""
    
    def setUp(self):
        self.scholarship = Scholarship.objects.create(
            name='Merit Scholarship',
            code='MERIT-2024',
            scholarship_type='merit',
            amount=5000,
            total_slots=10,
            filled_slots=3,
            valid_from=timezone.now().date(),
            valid_to=timezone.now().date() + timedelta(days=365),
            description='For top performers',
            eligibility_criteria='CGPA >= 3.5'
        )
    
    def test_available_slots(self):
        """Test available slots calculation"""
        self.assertEqual(self.scholarship.available_slots, 7)
    
    def test_is_open_for_application(self):
        """Test application period check"""
        self.scholarship.application_start_date = timezone.now().date()
        self.scholarship.application_end_date = timezone.now().date() + timedelta(days=30)
        self.scholarship.save()
        
        self.assertTrue(self.scholarship.is_open_for_application)
