"""Unit tests for BillingService"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.billing_service import BillingService
from src.models.billing import Bill, BillItem
from src.models.student import Student


@pytest.fixture
def billing_service():
    """Create billing service instance"""
    return BillingService()


@pytest.fixture
async def sample_student(db_session: AsyncSession) -> Student:
    """Create a sample student for testing"""
    student = Student(
        id=uuid4(),
        student_id="STU001",
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="1234567890",
        program="B.Tech",
        status="active"
    )
    db_session.add(student)
    await db_session.commit()
    await db_session.refresh(student)
    return student


class TestBillingService:
    """Test cases for BillingService"""

    @pytest.mark.asyncio
    async def test_create_bill(
        self,
        db_session: AsyncSession,
        billing_service: BillingService,
        sample_student: Student
    ):
        """Test creating a new bill"""
        bill_data = {
            "student_id": sample_student.id,
            "billing_period": "2024-Q1",
            "items": [
                {"description": "Tuition Fee", "amount": Decimal("50000.00")},
                {"description": "Lab Fee", "amount": Decimal("5000.00")},
            ]
        }

        bill = await billing_service.create_bill(db_session, bill_data)

        assert bill is not None
        assert bill.student_id == sample_student.id
        assert bill.total_amount == Decimal("55000.00")
        assert bill.status == "pending"
        assert len(bill.items) == 2

    @pytest.mark.asyncio
    async def test_get_bill_by_id(
        self,
        db_session: AsyncSession,
        billing_service: BillingService,
        sample_student: Student
    ):
        """Test retrieving a bill by ID"""
        # Create a bill first
        bill_data = {
            "student_id": sample_student.id,
            "billing_period": "2024-Q1",
            "items": [
                {"description": "Tuition Fee", "amount": Decimal("50000.00")},
            ]
        }
        created_bill = await billing_service.create_bill(db_session, bill_data)

        # Retrieve it
        bill = await billing_service.get_bill_by_id(db_session, created_bill.id)

        assert bill is not None
        assert bill.id == created_bill.id
        assert bill.total_amount == Decimal("50000.00")

    @pytest.mark.asyncio
    async def test_process_payment(
        self,
        db_session: AsyncSession,
        billing_service: BillingService,
        sample_student: Student
    ):
        """Test processing a payment for a bill"""
        # Create a bill
        bill_data = {
            "student_id": sample_student.id,
            "billing_period": "2024-Q1",
            "items": [
                {"description": "Tuition Fee", "amount": Decimal("50000.00")},
            ]
        }
        bill = await billing_service.create_bill(db_session, bill_data)

        # Process payment
        payment_data = {
            "amount": Decimal("50000.00"),
            "payment_method": "upi",
            "transaction_id": "TXN123456"
        }
        updated_bill = await billing_service.process_payment(
            db_session, bill.id, payment_data
        )

        assert updated_bill is not None
        assert updated_bill.paid_amount == Decimal("50000.00")
        assert updated_bill.status == "paid"
        assert updated_bill.payment_date is not None

    @pytest.mark.asyncio
    async def test_partial_payment(
        self,
        db_session: AsyncSession,
        billing_service: BillingService,
        sample_student: Student
    ):
        """Test processing a partial payment"""
        # Create a bill
        bill_data = {
            "student_id": sample_student.id,
            "billing_period": "2024-Q1",
            "items": [
                {"description": "Tuition Fee", "amount": Decimal("50000.00")},
            ]
        }
        bill = await billing_service.create_bill(db_session, bill_data)

        # Process partial payment
        payment_data = {
            "amount": Decimal("30000.00"),
            "payment_method": "cash",
            "transaction_id": "TXN789"
        }
        updated_bill = await billing_service.process_payment(
            db_session, bill.id, payment_data
        )

        assert updated_bill.paid_amount == Decimal("30000.00")
        assert updated_bill.status == "partial"
        assert updated_bill.balance == Decimal("20000.00")

    @pytest.mark.asyncio
    async def test_get_student_bills(
        self,
        db_session: AsyncSession,
        billing_service: BillingService,
        sample_student: Student
    ):
        """Test getting all bills for a student"""
        # Create multiple bills
        for i in range(3):
            bill_data = {
                "student_id": sample_student.id,
                "billing_period": f"2024-Q{i+1}",
                "items": [
                    {"description": "Tuition Fee", "amount": Decimal("50000.00")},
                ]
            }
            await billing_service.create_bill(db_session, bill_data)

        bills = await billing_service.get_student_bills(
            db_session, sample_student.id
        )

        assert len(bills) == 3
        assert all(b.student_id == sample_student.id for b in bills)

    @pytest.mark.asyncio
    async def test_get_pending_bills(
        self,
        db_session: AsyncSession,
        billing_service: BillingService,
        sample_student: Student
    ):
        """Test getting pending bills"""
        # Create pending bill
        bill_data = {
            "student_id": sample_student.id,
            "billing_period": "2024-Q1",
            "items": [
                {"description": "Tuition Fee", "amount": Decimal("50000.00")},
            ]
        }
        await billing_service.create_bill(db_session, bill_data)

        pending_bills = await billing_service.get_pending_bills(db_session)

        assert len(pending_bills) >= 1
        assert all(b.status == "pending" for b in pending_bills)

    @pytest.mark.asyncio
    async def test_calculate_bill_total(
        self,
        db_session: AsyncSession,
        billing_service: BillingService
    ):
        """Test calculating bill total from items"""
        items = [
            {"description": "Tuition Fee", "amount": Decimal("50000.00")},
            {"description": "Lab Fee", "amount": Decimal("5000.00")},
            {"description": "Library Fee", "amount": Decimal("1000.00")},
        ]

        total = billing_service.calculate_total(items)

        assert total == Decimal("56000.00")

    @pytest.mark.asyncio
    async def test_apply_discount(
        self,
        db_session: AsyncSession,
        billing_service: BillingService,
        sample_student: Student
    ):
        """Test applying discount to a bill"""
        # Create a bill
        bill_data = {
            "student_id": sample_student.id,
            "billing_period": "2024-Q1",
            "items": [
                {"description": "Tuition Fee", "amount": Decimal("50000.00")},
            ]
        }
        bill = await billing_service.create_bill(db_session, bill_data)

        # Apply discount
        updated_bill = await billing_service.apply_discount(
            db_session,
            bill_id=bill.id,
            discount_percentage=Decimal("10.0")
        )

        assert updated_bill.discount == Decimal("5000.00")
        assert updated_bill.total_amount == Decimal("45000.00")

    @pytest.mark.asyncio
    async def test_cancel_bill(
        self,
        db_session: AsyncSession,
        billing_service: BillingService,
        sample_student: Student
    ):
        """Test canceling a bill"""
        # Create a bill
        bill_data = {
            "student_id": sample_student.id,
            "billing_period": "2024-Q1",
            "items": [
                {"description": "Tuition Fee", "amount": Decimal("50000.00")},
            ]
        }
        bill = await billing_service.create_bill(db_session, bill_data)

        # Cancel it
        canceled_bill = await billing_service.cancel_bill(db_session, bill.id)

        assert canceled_bill.status == "canceled"
        assert canceled_bill.canceled_at is not None

    @pytest.mark.asyncio
    async def test_generate_invoice_number(
        self,
        db_session: AsyncSession,
        billing_service: BillingService
    ):
        """Test generating invoice number"""
        invoice_number = await billing_service.generate_invoice_number(db_session)

        assert invoice_number is not None
        assert invoice_number.startswith("INV")
        assert len(invoice_number) > 3
