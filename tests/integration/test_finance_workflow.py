"""Integration tests for Finance workflow"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.student import Student
from src.models.billing import Bill, BillItem
from src.models.finance import Payment


@pytest.mark.asyncio
async def test_complete_billing_workflow(db_session: AsyncSession):
    """Test complete billing workflow from bill creation to payment"""
    # Step 1: Create a student
    student = Student(
        id=uuid4(),
        student_id="STU20240001",
        first_name="Alice",
        last_name="Johnson",
        email="alice.johnson@example.com",
        phone="9876543210",
        program="B.Tech",
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)
    
    # Step 2: Create a bill for the student
    bill = Bill(
        id=uuid4(),
        bill_number="BILL20240001",
        student_id=student.id,
        billing_period="2024-Q1",
        total_amount=Decimal("55000.00"),
        paid_amount=Decimal("0.00"),
        status="pending",
        issue_date=datetime.utcnow()
    )
    db_session.add(bill)
    
    # Step 3: Add bill items
    items = [
        BillItem(
            id=uuid4(),
            bill_id=bill.id,
            description="Tuition Fee",
            amount=Decimal("50000.00"),
            quantity=1
        ),
        BillItem(
            id=uuid4(),
            bill_id=bill.id,
            description="Lab Fee",
            amount=Decimal("5000.00"),
            quantity=1
        )
    ]
    for item in items:
        db_session.add(item)
    
    await db_session.commit()
    await db_session.refresh(bill)
    
    # Step 4: Process payment
    payment = Payment(
        id=uuid4(),
        bill_id=bill.id,
        amount=Decimal("55000.00"),
        payment_method="upi",
        transaction_id="TXN123456",
        payment_date=datetime.utcnow(),
        status="completed"
    )
    db_session.add(payment)
    
    # Update bill status
    bill.paid_amount = Decimal("55000.00")
    bill.status = "paid"
    bill.payment_date = datetime.utcnow()
    
    await db_session.commit()
    await db_session.refresh(bill)
    
    # Assertions
    assert bill.status == "paid"
    assert bill.paid_amount == Decimal("55000.00")
    assert bill.total_amount == Decimal("55000.00")
    assert len(bill.items) == 2


@pytest.mark.asyncio
async def test_partial_payment_workflow(db_session: AsyncSession):
    """Test partial payment workflow"""
    # Create student
    student = Student(
        id=uuid4(),
        student_id="STU20240002",
        first_name="Bob",
        last_name="Smith",
        email="bob.smith@example.com",
        phone="9876543211",
        program="MBA",
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    
    # Create bill
    bill = Bill(
        id=uuid4(),
        bill_number="BILL20240002",
        student_id=student.id,
        billing_period="2024-Q1",
        total_amount=Decimal("100000.00"),
        paid_amount=Decimal("0.00"),
        status="pending",
        issue_date=datetime.utcnow()
    )
    db_session.add(bill)
    await db_session.commit()
    
    # First partial payment
    payment1 = Payment(
        id=uuid4(),
        bill_id=bill.id,
        amount=Decimal("60000.00"),
        payment_method="cash",
        transaction_id="TXN789",
        payment_date=datetime.utcnow(),
        status="completed"
    )
    db_session.add(payment1)
    
    bill.paid_amount = Decimal("60000.00")
    bill.status = "partial"
    
    await db_session.commit()
    await db_session.refresh(bill)
    
    # Verify partial payment
    assert bill.status == "partial"
    assert bill.paid_amount == Decimal("60000.00")
    balance = bill.total_amount - bill.paid_amount
    assert balance == Decimal("40000.00")
    
    # Second payment (complete)
    payment2 = Payment(
        id=uuid4(),
        bill_id=bill.id,
        amount=Decimal("40000.00"),
        payment_method="card",
        transaction_id="TXN790",
        payment_date=datetime.utcnow(),
        status="completed"
    )
    db_session.add(payment2)
    
    bill.paid_amount = Decimal("100000.00")
    bill.status = "paid"
    bill.payment_date = datetime.utcnow()
    
    await db_session.commit()
    await db_session.refresh(bill)
    
    # Verify full payment
    assert bill.status == "paid"
    assert bill.paid_amount == Decimal("100000.00")


@pytest.mark.asyncio
async def test_bill_with_discount(db_session: AsyncSession):
    """Test bill with discount applied"""
    # Create student
    student = Student(
        id=uuid4(),
        student_id="STU20240003",
        first_name="Charlie",
        last_name="Brown",
        email="charlie.brown@example.com",
        phone="9876543212",
        program="M.Tech",
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    
    # Create bill with discount
    original_amount = Decimal("50000.00")
    discount = Decimal("5000.00")  # 10% discount
    final_amount = original_amount - discount
    
    bill = Bill(
        id=uuid4(),
        bill_number="BILL20240003",
        student_id=student.id,
        billing_period="2024-Q1",
        total_amount=final_amount,
        discount=discount,
        paid_amount=Decimal("0.00"),
        status="pending",
        issue_date=datetime.utcnow()
    )
    db_session.add(bill)
    await db_session.commit()
    await db_session.refresh(bill)
    
    # Verify discount applied
    assert bill.discount == Decimal("5000.00")
    assert bill.total_amount == Decimal("45000.00")


@pytest.mark.asyncio
async def test_multiple_students_billing(db_session: AsyncSession):
    """Test creating bills for multiple students"""
    # Create multiple students
    students = []
    for i in range(3):
        student = Student(
            id=uuid4(),
            student_id=f"STU2024000{i+4}",
            first_name=f"Student{i+1}",
            last_name="Test",
            email=f"student{i+1}@example.com",
            phone=f"987654321{i}",
            program="B.Tech",
            status="active"
        )
        db_session.add(student)
        students.append(student)
    
    await db_session.commit()
    
    # Create bills for all students
    bills = []
    for i, student in enumerate(students):
        bill = Bill(
            id=uuid4(),
            bill_number=f"BILL2024000{i+4}",
            student_id=student.id,
            billing_period="2024-Q1",
            total_amount=Decimal("50000.00"),
            paid_amount=Decimal("0.00"),
            status="pending",
            issue_date=datetime.utcnow()
        )
        db_session.add(bill)
        bills.append(bill)
    
    await db_session.commit()
    
    # Verify all bills created
    assert len(bills) == 3
    assert all(b.status == "pending" for b in bills)
    assert all(b.total_amount == Decimal("50000.00") for b in bills)
