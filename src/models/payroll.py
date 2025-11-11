"""Payroll model for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.models.employee import Employee


class PayrollStatus(str, Enum):
    """Payroll status enumeration."""

    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    PROCESSED = "processed"
    PAID = "paid"
    REJECTED = "rejected"


class Payroll(Base):
    """Payroll model for employee salary payments."""

    __tablename__ = "payroll"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    employee_id: Mapped[UUID] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # Period
    month: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    pay_period_start: Mapped[date] = mapped_column(Date, nullable=False)
    pay_period_end: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Salary components
    basic_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    hra: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True, default=0)
    transport_allowance: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), nullable=True, default=0
    )
    medical_allowance: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), nullable=True, default=0
    )
    special_allowance: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), nullable=True, default=0
    )
    other_allowances: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), nullable=True, default=0
    )
    
    # Deductions
    provident_fund: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), nullable=True, default=0
    )
    professional_tax: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), nullable=True, default=0
    )
    income_tax: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), nullable=True, default=0
    )
    other_deductions: Mapped[Optional[float]] = mapped_column(
        Numeric(12, 2), nullable=True, default=0
    )
    
    # Totals
    gross_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    total_deductions: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    net_salary: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    
    # Payment details
    payment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Status
    status: Mapped[PayrollStatus] = mapped_column(
        String(20), default=PayrollStatus.DRAFT, index=True
    )
    
    # Approval tracking
    approved_by: Mapped[Optional[UUID]] = mapped_column(nullable=True)
    approved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    employee: Mapped["Employee"] = relationship("Employee", back_populates="payrolls")
    
    def __repr__(self) -> str:
        return f"<Payroll(id={self.id}, employee_id={self.employee_id}, period={self.month}/{self.year})>"
    
    def calculate_gross_salary(self) -> float:
        """Calculate gross salary from all allowances."""
        return float(
            self.basic_salary
            + (self.hra or 0)
            + (self.transport_allowance or 0)
            + (self.medical_allowance or 0)
            + (self.special_allowance or 0)
            + (self.other_allowances or 0)
        )
    
    def calculate_total_deductions(self) -> float:
        """Calculate total deductions."""
        return float(
            (self.provident_fund or 0)
            + (self.professional_tax or 0)
            + (self.income_tax or 0)
            + (self.other_deductions or 0)
        )
    
    def calculate_net_salary(self) -> float:
        """Calculate net salary."""
        return self.calculate_gross_salary() - self.calculate_total_deductions()
