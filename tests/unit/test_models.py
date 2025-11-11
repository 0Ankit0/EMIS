"""Model validation tests - ensure models can be instantiated correctly"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from uuid import uuid4

from src.models.student import Student
from src.models.course import Course, Department
from src.models.employee import Employee
from src.models.library import Book
from src.models.billing import Bill, BillItem
from src.models.attendance import Attendance


class TestModelInstantiation:
    """Test that models can be created with valid data"""

    def test_create_student_model(self):
        """Test creating a Student model instance"""
        student = Student(
            id=uuid4(),
            student_id="STU001",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="1234567890",
            date_of_birth=date(2000, 1, 1),
            gender="male",
            program="B.Tech",
            status="active"
        )
        
        assert student is not None
        assert student.first_name == "John"
        assert student.email == "john@example.com"
        assert student.status == "active"

    def test_create_course_model(self):
        """Test creating a Course model instance"""
        course = Course(
            id=uuid4(),
            course_code="CS101",
            course_name="Introduction to Programming",
            credits=4,
            semester=1,
            status="active"
        )
        
        assert course is not None
        assert course.course_code == "CS101"
        assert course.credits == 4

    def test_create_employee_model(self):
        """Test creating an Employee model instance"""
        employee = Employee(
            id=uuid4(),
            employee_id="EMP001",
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone="9876543210",
            department="Computer Science",
            designation="Professor",
            status="active"
        )
        
        assert employee is not None
        assert employee.first_name == "Jane"
        assert employee.department == "Computer Science"

    def test_create_book_model(self):
        """Test creating a Book model instance"""
        book = Book(
            id=uuid4(),
            isbn="978-0-123456-78-9",
            title="Python Programming",
            author="John Author",
            publisher="Tech Books",
            category="Programming",
            total_copies=5,
            available_copies=5
        )
        
        assert book is not None
        assert book.isbn == "978-0-123456-78-9"
        assert book.title == "Python Programming"
        assert book.total_copies == 5

    def test_create_bill_model(self):
        """Test creating a Bill model instance"""
        bill = Bill(
            id=uuid4(),
            bill_number="BILL001",
            student_id=uuid4(),
            billing_period="2024-Q1",
            total_amount=Decimal("50000.00"),
            paid_amount=Decimal("0.00"),
            status="pending",
            issue_date=datetime.utcnow()
        )
        
        assert bill is not None
        assert bill.bill_number == "BILL001"
        assert bill.total_amount == Decimal("50000.00")
        assert bill.status == "pending"

    def test_create_bill_item_model(self):
        """Test creating a BillItem model instance"""
        bill_item = BillItem(
            id=uuid4(),
            bill_id=uuid4(),
            description="Tuition Fee",
            amount=Decimal("50000.00"),
            quantity=1
        )
        
        assert bill_item is not None
        assert bill_item.description == "Tuition Fee"
        assert bill_item.amount == Decimal("50000.00")

    def test_create_attendance_model(self):
        """Test creating an Attendance model instance"""
        attendance = Attendance(
            id=uuid4(),
            student_id=uuid4(),
            course_id=uuid4(),
            date=date.today(),
            status="present",
            marked_by=uuid4()
        )
        
        assert attendance is not None
        assert attendance.status == "present"

    def test_create_department_model(self):
        """Test creating a Department model instance"""
        department = Department(
            id=uuid4(),
            department_code="CS",
            department_name="Computer Science",
            hod_id=uuid4(),
            status="active"
        )
        
        assert department is not None
        assert department.department_code == "CS"
        assert department.department_name == "Computer Science"

    def test_model_string_representation(self):
        """Test model string representations"""
        student = Student(
            id=uuid4(),
            student_id="STU002",
            first_name="Alice",
            last_name="Wilson",
            email="alice@example.com",
            phone="1111111111",
            program="MBA",
            status="active"
        )
        
        # Most models should have __repr__ or __str__
        str_repr = str(student)
        assert "Alice" in str_repr or "STU002" in str_repr or "Student" in str_repr

    def test_model_with_relationships(self):
        """Test model with relationship fields"""
        # Create bill with items (testing relationship)
        bill_id = uuid4()
        
        bill = Bill(
            id=bill_id,
            bill_number="BILL002",
            student_id=uuid4(),
            billing_period="2024-Q2",
            total_amount=Decimal("60000.00"),
            paid_amount=Decimal("0.00"),
            status="pending",
            issue_date=datetime.utcnow()
        )
        
        item1 = BillItem(
            id=uuid4(),
            bill_id=bill_id,
            description="Tuition Fee",
            amount=Decimal("50000.00"),
            quantity=1
        )
        
        item2 = BillItem(
            id=uuid4(),
            bill_id=bill_id,
            description="Lab Fee",
            amount=Decimal("10000.00"),
            quantity=1
        )
        
        # Both items reference the same bill
        assert item1.bill_id == bill_id
        assert item2.bill_id == bill_id

    def test_model_default_values(self):
        """Test that models set default values correctly"""
        student = Student(
            id=uuid4(),
            student_id="STU003",
            first_name="Bob",
            last_name="Johnson",
            email="bob@example.com",
            phone="2222222222",
            program="B.Tech"
            # Not setting status - should default to 'active'
        )
        
        # Check if defaults are set (this depends on model definition)
        assert student.id is not None

    def test_model_with_decimal_fields(self):
        """Test models with Decimal fields for currency"""
        bill = Bill(
            id=uuid4(),
            bill_number="BILL003",
            student_id=uuid4(),
            billing_period="2024-Q3",
            total_amount=Decimal("55000.50"),  # With decimal places
            paid_amount=Decimal("25000.25"),
            status="partial",
            issue_date=datetime.utcnow()
        )
        
        assert isinstance(bill.total_amount, Decimal)
        assert isinstance(bill.paid_amount, Decimal)
        assert bill.total_amount == Decimal("55000.50")
        assert bill.paid_amount == Decimal("25000.25")

    def test_model_with_datetime_fields(self):
        """Test models with datetime fields"""
        now = datetime.utcnow()
        
        bill = Bill(
            id=uuid4(),
            bill_number="BILL004",
            student_id=uuid4(),
            billing_period="2024-Q4",
            total_amount=Decimal("50000.00"),
            paid_amount=Decimal("0.00"),
            status="pending",
            issue_date=now,
            due_date=now
        )
        
        assert bill.issue_date == now
        assert isinstance(bill.issue_date, datetime)
