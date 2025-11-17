"""Tests for fee collection reports"""
import pytest
from decimal import Decimal
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from apps.finance.services.fee_structure_service import FeeStructureService
from apps.finance.services.invoice_service import InvoiceService
from apps.finance.services.payment_service import PaymentService
from apps.finance.services.report_service import ReportService
from apps.students.models.student import Student

User = get_user_model()


@pytest.mark.django_db
class TestReports:
    """Test report generation"""
    
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
            'name': 'Test Fee',
            'code': 'TEST-2024',
            'program': 'Test Program',
            'academic_year': '2024',
            'semester': 'Fall',
            'components': {'tuition': 5000},
            'valid_from': date.today(),
            'valid_to': date.today() + timedelta(days=365),
            'is_active': True
        })
        
        invoice = InvoiceService.generate_invoice_from_fee_structure(
            student_id=student.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() + timedelta(days=30),
            academic_year='2024',
            semester='Fall'
        )
        
        # Make a payment
        PaymentService.process_payment({
            'invoice_id': invoice.id,
            'amount_paid': Decimal('5000.00'),
            'method': 'cash'
        })
        
        return {'student': student, 'invoice': invoice}
    
    def test_fee_collection_summary(self, setup_data):
        """Test fee collection summary generation"""
        summary = ReportService.generate_fee_collection_summary(
            academic_year='2024',
            semester='Fall'
        )
        
        assert summary['summary']['total_invoiced'] == 5000.00
        assert summary['summary']['total_collected'] == 5000.00
        assert summary['summary']['collection_rate'] == 100.00
    
    def test_student_fee_report(self, setup_data):
        """Test student-specific fee report"""
        student = setup_data['student']
        
        report = ReportService.generate_student_fee_report(student.id)
        
        assert report['summary']['total_invoiced'] == 5000.00
        assert report['summary']['total_paid'] == 5000.00
        assert report['invoices']['paid'] == 1
    
    def test_outstanding_fees_report(self, setup_data):
        """Test outstanding fees report"""
        # Create another unpaid invoice
        user = User.objects.create_user(
            email='student2@test.com',
            password='student123',
            first_name='Test2',
            last_name='Student2'
        )
        student2 = Student.objects.create(
            user=user,
            student_id='ST2024002',
            date_of_birth=date(2000, 1, 1)
        )
        
        fee_structure = FeeStructureService.create_fee_structure({
            'name': 'Test Fee 2',
            'code': 'TEST-2024-2',
            'program': 'Test Program',
            'academic_year': '2024',
            'semester': 'Fall',
            'components': {'tuition': 3000},
            'valid_from': date.today(),
            'valid_to': date.today() + timedelta(days=365),
            'is_active': True
        })
        
        InvoiceService.generate_invoice_from_fee_structure(
            student_id=student2.id,
            fee_structure_id=fee_structure.id,
            due_date=date.today() + timedelta(days=30)
        )
        
        report = ReportService.get_outstanding_fees_report(
            academic_year='2024',
            semester='Fall'
        )
        
        # Should have one outstanding invoice (student2's)
        assert len(report) >= 1
        outstanding = [r for r in report if r['student_id'] == student2.id]
        assert len(outstanding) == 1
    
    def test_export_csv_report(self, setup_data):
        """Test CSV export functionality"""
        csv_content = ReportService.export_collection_report_csv(
            academic_year='2024',
            semester='Fall'
        )
        
        assert csv_content is not None
        assert 'Receipt Number' in csv_content
        assert 'Amount Paid' in csv_content
