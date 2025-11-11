"""Employee model for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import String, Date, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class EmploymentType(str, Enum):
    """Employment type enumeration."""

    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    INTERN = "intern"


class EmployeeStatus(str, Enum):
    """Employee status enumeration."""

    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    RESIGNED = "resigned"
    RETIRED = "retired"


class Employee(Base):
    """Employee model for faculty and staff."""

    __tablename__ = "employees"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    employee_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    
    # Employment details
    date_of_joining: Mapped[date] = mapped_column(Date, nullable=False)
    date_of_termination: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    department: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    designation: Mapped[str] = mapped_column(String(100), nullable=False)
    employment_type: Mapped[EmploymentType] = mapped_column(String(20), nullable=False)
    status: Mapped[EmployeeStatus] = mapped_column(
        String(20), default=EmployeeStatus.ACTIVE, index=True
    )
    
    # Compensation
    basic_salary: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(10), default="INR")
    
    # Contact & Address
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Emergency contact
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    emergency_contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # Reporting
    manager_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True, index=True
    )
    
    # User account reference
    user_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    manager: Mapped[Optional["Employee"]] = relationship(
        "Employee", remote_side=[id], back_populates="subordinates"
    )
    subordinates: Mapped[List["Employee"]] = relationship(
        "Employee", back_populates="manager"
    )
    payrolls: Mapped[List["Payroll"]] = relationship(
        "Payroll", back_populates="employee", lazy="selectin"
    )
    leave_requests: Mapped[List["Leave"]] = relationship(
        "Leave", back_populates="employee", foreign_keys="Leave.employee_id"
    )
    
    def __repr__(self) -> str:
        return f"<Employee(id={self.id}, number={self.employee_number}, name={self.first_name} {self.last_name})>"
    
    @property
    def full_name(self) -> str:
        """Get employee's full name."""
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts)
