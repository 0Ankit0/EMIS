"""Finance models for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class FeeType(str, Enum):
    """Fee type enumeration."""
    TUITION = "tuition"
    LIBRARY = "library"
    SPORTS = "sports"
    EXAM = "exam"
    LAB = "lab"
    HOSTEL = "hostel"
    TRANSPORT = "transport"
    OTHER = "other"


class FeeStructure(Base):
    """Fee structure model for programs."""
    
    __tablename__ = "fee_structures"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    program_id: Mapped[UUID] = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    semester: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Fee components
    tuition_fee: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    library_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    sports_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    exam_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    lab_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    hostel_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    transport_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    other_fees: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    
    # Dates
    effective_from: Mapped[date] = mapped_column(Date, nullable=False)
    effective_to: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    program: Mapped["Program"] = relationship("Program", lazy="selectin")
    
    @property
    def total_fee(self) -> float:
        """Calculate total fee."""
        return (
            float(self.tuition_fee or 0) +
            float(self.library_fee or 0) +
            float(self.sports_fee or 0) +
            float(self.exam_fee or 0) +
            float(self.lab_fee or 0) +
            float(self.hostel_fee or 0) +
            float(self.transport_fee or 0) +
            float(self.other_fees or 0)
        )
    
    def __repr__(self) -> str:
        return f"<FeeStructure(id={self.id}, program_id={self.program_id}, year={self.academic_year})>"


class PaymentMethod(str, Enum):
    """Payment method enumeration."""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    NET_BANKING = "net_banking"
    OTHER = "other"


class PaymentStatus(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class Payment(Base):
    """Payment model for fee payments."""
    
    __tablename__ = "payments"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    
    # Payment details
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    payment_method: Mapped[PaymentMethod] = mapped_column(String(30), nullable=False)
    payment_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    
    # Transaction details
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    reference_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    
    # Fee breakdown
    fee_type: Mapped[FeeType] = mapped_column(String(20), nullable=False, index=True)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    semester: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Status
    status: Mapped[PaymentStatus] = mapped_column(
        String(20), default=PaymentStatus.PENDING, index=True
    )
    
    # Receipt
    receipt_number: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True)
    receipt_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Processing
    processed_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    processed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", lazy="selectin")
    processor: Mapped[Optional["Employee"]] = relationship("Employee", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, amount={self.amount}, status={self.status})>"


class ScholarshipType(str, Enum):
    """Scholarship type enumeration."""
    MERIT = "merit"
    NEED_BASED = "need_based"
    SPORTS = "sports"
    MINORITY = "minority"
    SC_ST = "sc_st"
    GOVERNMENT = "government"
    INSTITUTIONAL = "institutional"
    EXTERNAL = "external"


class ScholarshipStatus(str, Enum):
    """Scholarship status enumeration."""
    APPLIED = "applied"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Scholarship(Base):
    """Scholarship model for student scholarships."""
    
    __tablename__ = "scholarships"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # Scholarship details
    scholarship_name: Mapped[str] = mapped_column(String(200), nullable=False)
    scholarship_type: Mapped[ScholarshipType] = mapped_column(
        String(30), nullable=False, index=True
    )
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Academic period
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Eligibility
    criteria: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status
    status: Mapped[ScholarshipStatus] = mapped_column(
        String(20), default=ScholarshipStatus.APPLIED, index=True
    )
    
    # Approval
    approved_by: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
    )
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    # Disbursement
    disbursement_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    disbursed_amount: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    student: Mapped["Student"] = relationship("Student", lazy="selectin")
    approver: Mapped[Optional["Employee"]] = relationship("Employee", lazy="selectin")
    
    def __repr__(self) -> str:
        return f"<Scholarship(id={self.id}, name={self.scholarship_name}, amount={self.amount})>"


class Program(Base):
    """Program/Degree model."""
    
    __tablename__ = "programs"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    program_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    program_name: Mapped[str] = mapped_column(String(200), nullable=False)
    degree: Mapped[str] = mapped_column(String(100), nullable=False)  # BSc, MSc, PhD
    department: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    duration_years: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<Program(id={self.id}, code={self.program_code}, name={self.program_name})>"
