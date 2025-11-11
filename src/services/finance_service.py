"""Finance service for EMIS."""
from datetime import datetime, date
from typing import Optional, List
from uuid import UUID
from decimal import Decimal

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.finance import Program, FeeStructure, Payment, Scholarship, PaymentStatus
from src.models.student import Student
from src.lib.audit import log_audit, AuditAction
from src.lib.logging import get_logger

logger = get_logger(__name__)


class FinanceService:
    """Service for managing finance operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_program(
        self,
        program_code: str,
        program_name: str,
        degree_level: str,
        duration_years: int,
        department: str,
        description: Optional[str] = None,
    ) -> Program:
        """Create a new academic program."""
        program = Program(
            program_code=program_code,
            program_name=program_name,
            degree_level=degree_level,
            duration_years=duration_years,
            department=department,
            description=description,
            status="active"
        )

        self.db.add(program)
        await self.db.commit()
        await self.db.refresh(program)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="Program",
            entity_id=program.id,
            details={"program_code": program_code, "program_name": program_name}
        )

        logger.info(f"Program created: {program_code}")
        return program

    async def create_fee_structure(
        self,
        program_id: UUID,
        academic_year: str,
        semester: str,
        tuition_fee: Decimal,
        lab_fee: Optional[Decimal] = None,
        library_fee: Optional[Decimal] = None,
        sports_fee: Optional[Decimal] = None,
        other_fees: Optional[Decimal] = None,
    ) -> FeeStructure:
        """Create fee structure for a program."""
        # Verify program exists
        result = await self.db.execute(
            select(Program).where(Program.id == program_id)
        )
        if not result.scalar_one_or_none():
            raise ValueError(f"Program {program_id} not found")

        total_fee = tuition_fee
        if lab_fee:
            total_fee += lab_fee
        if library_fee:
            total_fee += library_fee
        if sports_fee:
            total_fee += sports_fee
        if other_fees:
            total_fee += other_fees

        fee_structure = FeeStructure(
            program_id=program_id,
            academic_year=academic_year,
            semester=semester,
            tuition_fee=tuition_fee,
            lab_fee=lab_fee,
            library_fee=library_fee,
            sports_fee=sports_fee,
            other_fees=other_fees,
            total_fee=total_fee,
        )

        self.db.add(fee_structure)
        await self.db.commit()
        await self.db.refresh(fee_structure)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="FeeStructure",
            entity_id=fee_structure.id,
            details={
                "program_id": str(program_id),
                "academic_year": academic_year,
                "total_fee": str(total_fee)
            }
        )

        logger.info(f"Fee structure created for program {program_id}")
        return fee_structure

    async def record_payment(
        self,
        student_id: UUID,
        fee_structure_id: UUID,
        amount: Decimal,
        payment_method: str,
        transaction_id: Optional[str] = None,
        payment_date: Optional[date] = None,
    ) -> Payment:
        """Record a fee payment."""
        # Verify student exists
        student_result = await self.db.execute(
            select(Student).where(Student.id == student_id)
        )
        student = student_result.scalar_one_or_none()
        if not student:
            raise ValueError(f"Student {student_id} not found")

        # Verify fee structure exists
        fee_result = await self.db.execute(
            select(FeeStructure).where(FeeStructure.id == fee_structure_id)
        )
        fee_structure = fee_result.scalar_one_or_none()
        if not fee_structure:
            raise ValueError(f"Fee structure {fee_structure_id} not found")

        if not payment_date:
            payment_date = date.today()

        payment = Payment(
            student_id=student_id,
            fee_structure_id=fee_structure_id,
            amount=amount,
            payment_date=payment_date,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status=PaymentStatus.COMPLETED,
        )

        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="Payment",
            entity_id=payment.id,
            user_id=student.user_id,
            details={
                "student_id": str(student_id),
                "amount": str(amount),
                "payment_method": payment_method
            }
        )

        logger.info(f"Payment recorded: {amount} for student {student.student_number}")
        return payment

    async def award_scholarship(
        self,
        student_id: UUID,
        scholarship_name: str,
        amount: Decimal,
        academic_year: str,
        award_date: Optional[date] = None,
        description: Optional[str] = None,
    ) -> Scholarship:
        """Award a scholarship to a student."""
        # Verify student exists
        result = await self.db.execute(
            select(Student).where(Student.id == student_id)
        )
        student = result.scalar_one_or_none()
        if not student:
            raise ValueError(f"Student {student_id} not found")

        if not award_date:
            award_date = date.today()

        scholarship = Scholarship(
            student_id=student_id,
            scholarship_name=scholarship_name,
            amount=amount,
            academic_year=academic_year,
            award_date=award_date,
            description=description,
            status="active"
        )

        self.db.add(scholarship)
        await self.db.commit()
        await self.db.refresh(scholarship)

        await log_audit(
            self.db,
            action=AuditAction.CREATE,
            entity_type="Scholarship",
            entity_id=scholarship.id,
            user_id=student.user_id,
            details={
                "student_id": str(student_id),
                "scholarship_name": scholarship_name,
                "amount": str(amount)
            }
        )

        logger.info(f"Scholarship awarded: {scholarship_name} to {student.student_number}")
        return scholarship

    async def get_student_fee_status(
        self,
        student_id: UUID,
        academic_year: str,
        semester: Optional[str] = None
    ) -> dict:
        """Get fee payment status for a student."""
        student_result = await self.db.execute(
            select(Student).where(Student.id == student_id)
        )
        student = student_result.scalar_one_or_none()
        if not student:
            raise ValueError(f"Student {student_id} not found")

        # Get applicable fee structure (from student's program)
        fee_query = (
            select(FeeStructure)
            .where(
                and_(
                    FeeStructure.program_id == student.program_id,
                    FeeStructure.academic_year == academic_year
                )
            )
        )
        
        if semester:
            fee_query = fee_query.where(FeeStructure.semester == semester)

        fee_result = await self.db.execute(fee_query)
        fee_structures = list(fee_result.scalars().all())

        # Get total payments
        payment_query = (
            select(func.sum(Payment.amount))
            .join(FeeStructure)
            .where(
                and_(
                    Payment.student_id == student_id,
                    FeeStructure.academic_year == academic_year,
                    Payment.status == PaymentStatus.COMPLETED
                )
            )
        )

        if semester:
            payment_query = payment_query.where(FeeStructure.semester == semester)

        payment_result = await self.db.execute(payment_query)
        total_paid = payment_result.scalar() or Decimal(0)

        # Get scholarships
        scholarship_query = (
            select(func.sum(Scholarship.amount))
            .where(
                and_(
                    Scholarship.student_id == student_id,
                    Scholarship.academic_year == academic_year,
                    Scholarship.status == "active"
                )
            )
        )
        scholarship_result = await self.db.execute(scholarship_query)
        total_scholarship = scholarship_result.scalar() or Decimal(0)

        # Calculate total fee
        total_fee = sum(fs.total_fee for fs in fee_structures)

        # Calculate balance
        balance = total_fee - total_paid - total_scholarship

        return {
            "student_id": str(student_id),
            "student_number": student.student_number,
            "academic_year": academic_year,
            "semester": semester,
            "total_fee": float(total_fee),
            "total_paid": float(total_paid),
            "total_scholarship": float(total_scholarship),
            "balance": float(balance),
            "fee_structures": [
                {
                    "id": str(fs.id),
                    "semester": fs.semester,
                    "total_fee": float(fs.total_fee)
                }
                for fs in fee_structures
            ]
        }

    async def get_payment_history(
        self,
        student_id: UUID,
        academic_year: Optional[str] = None
    ) -> List[Payment]:
        """Get payment history for a student."""
        query = select(Payment).where(Payment.student_id == student_id)

        if academic_year:
            query = (
                query
                .join(FeeStructure)
                .where(FeeStructure.academic_year == academic_year)
            )

        query = query.order_by(Payment.payment_date.desc())

        result = await self.db.execute(query)
        return list(result.scalars().all())
