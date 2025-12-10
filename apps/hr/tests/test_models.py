"""HR App Tests"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta

from .models import Department, Designation, Employee, Attendance, Leave, Payroll
from .utils import calculate_leave_balance, generate_payroll_for_employee

User = get_user_model()


class DepartmentTestCase(TestCase):
    """Test Department model"""
    
    def setUp(self):
        self.dept = Department.objects.create(
            name='Information Technology',
            code='IT',
            description='IT Department'
        )
    
    def test_department_str(self):
        self.assertEqual(str(self.dept), 'IT - Information Technology')


class EmployeeTestCase(TestCase):
    """Test Employee model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testemployee',
            email='test@example.com',
            password='testpass123'
        )
        
        self.dept = Department.objects.create(name='HR', code='HR')
        self.designation = Designation.objects.create(
            title='HR Manager',
            code='HR-MGR',
            level='manager',
            min_salary=50000,
            max_salary=100000
        )
        
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 1, 1),
            gender='male',
            marital_status='single',
            phone='+919876543210',
            email='john@example.com',
            current_address='Test Address',
            city='Mumbai',
            state='Maharashtra',
            pincode='400001',
            department=self.dept,
            designation=self.designation,
            employment_type='full_time',
            date_of_joining=date.today(),
            basic_salary=Decimal('60000')
        )
    
    def test_employee_full_name(self):
        self.assertEqual(self.employee.get_full_name(), 'John Doe')
    
    def test_employee_age(self):
        age = self.employee.get_age()
        self.assertGreater(age, 0)
    
    def test_gross_salary(self):
        self.employee.hra = Decimal('15000')
        self.employee.da = Decimal('5000')
        self.assertEqual(self.employee.gross_salary, Decimal('80000'))


class LeaveTestCase(TestCase):
    """Test Leave model"""
    
    def setUp(self):
        user = User.objects.create_user(username='emp', email='emp@test.com', password='pass')
        dept = Department.objects.create(name='Test', code='TST')
        designation = Designation.objects.create(
            title='Test', code='TST', level='mid',
            min_salary=40000, max_salary=80000
        )
        
        self.employee = Employee.objects.create(
            user=user,
            employee_id='EMP002',
            first_name='Jane',
            last_name='Smith',
            date_of_birth=date(1985, 5, 15),
            gender='female',
            marital_status='married',
            phone='+919876543211',
            email='jane@example.com',
            current_address='Test',
            city='Delhi',
            state='Delhi',
            pincode='110001',
            department=dept,
            designation=designation,
            employment_type='full_time',
            date_of_joining=date.today(),
            basic_salary=Decimal('50000')
        )
    
    def test_leave_creation(self):
        leave = Leave.objects.create(
            employee=self.employee,
            leave_type='casual',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            reason='Personal work'
        )
        
        self.assertEqual(leave.number_of_days, 3)
    
    def test_leave_balance_calculation(self):
        # Create some approved leaves
        Leave.objects.create(
            employee=self.employee,
            leave_type='casual',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            status='approved',
            reason='Test'
        )
        
        balance = calculate_leave_balance(self.employee, 'casual', date.today().year)
        self.assertEqual(balance['taken'], 2)
        self.assertEqual(balance['balance'], 10)  # 12 - 2


class PayrollTestCase(TestCase):
    """Test Payroll model"""
    
    def test_payroll_calculations(self):
        user = User.objects.create_user(username='paytest', email='pay@test.com', password='pass')
        dept = Department.objects.create(name='Finance', code='FIN')
        designation = Designation.objects.create(
            title='Accountant', code='ACC', level='mid',
            min_salary=40000, max_salary=70000
        )
        
        employee = Employee.objects.create(
            user=user,
            employee_id='EMP003',
            first_name='Test',
            last_name='Employee',
            date_of_birth=date(1988, 3, 20),
            gender='male',
            marital_status='single',
            phone='+919876543212',
            email='test@example.com',
            current_address='Test Address',
            city='Bangalore',
            state='Karnataka',
            pincode='560001',
            department=dept,
            designation=designation,
            employment_type='full_time',
            date_of_joining=date.today(),
            basic_salary=Decimal('50000')
        )
        
        payroll = Payroll.objects.create(
            employee=employee,
            month=1,
            year=2024,
            basic_salary=Decimal('50000'),
            hra=Decimal('10000'),
            da=Decimal('5000'),
            pf=Decimal('6000'),
            esi=Decimal('500'),
            working_days=26,
            present_days=26
        )
        
        self.assertEqual(payroll.gross_salary, Decimal('65000'))
        self.assertEqual(payroll.total_deductions, Decimal('6500'))
        self.assertEqual(payroll.net_salary, Decimal('58500'))
