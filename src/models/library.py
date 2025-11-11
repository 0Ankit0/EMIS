"""Library models for EMIS."""
from datetime import datetime, date
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import String, Integer, Date, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class BookStatus(str, Enum):
    """Book status enumeration."""
    AVAILABLE = "available"
    ISSUED = "issued"
    RESERVED = "reserved"
    LOST = "lost"
    DAMAGED = "damaged"
    UNDER_REPAIR = "under_repair"


class Book(Base):
    """Book model for library catalog."""
    
    __tablename__ = "books"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    publisher: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    publication_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    edition: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Classification
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    subject: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    language: Mapped[str] = mapped_column(String(50), default="English")
    
    # Inventory
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    available_quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Location
    shelf_location: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Pricing
    price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    
    # Additional info
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cover_image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Relationships
    transactions: Mapped[List["BookTransaction"]] = relationship(
        "BookTransaction", back_populates="book", lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<Book(id={self.id}, isbn={self.isbn}, title={self.title})>"


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    ISSUE = "issue"
    RETURN = "return"
    RENEW = "renew"
    RESERVE = "reserve"


class TransactionStatus(str, Enum):
    """Transaction status enumeration."""
    ACTIVE = "active"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class BookTransaction(Base):
    """Book transaction model for issue/return records."""
    
    __tablename__ = "book_transactions"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    book_id: Mapped[UUID] = mapped_column(
        ForeignKey("books.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    member_id: Mapped[UUID] = mapped_column(
        ForeignKey("students.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    
    # Transaction details
    transaction_type: Mapped[TransactionType] = mapped_column(
        String(20), nullable=False, index=True
    )
    status: Mapped[TransactionStatus] = mapped_column(
        String(20), default=TransactionStatus.ACTIVE, index=True
    )
    
    # Dates
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    
    # Renewal
    renewal_count: Mapped[int] = mapped_column(Integer, default=0)
    max_renewals: Mapped[int] = mapped_column(Integer, default=2)
    
    # Fines
    fine_amount: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    fine_paid: Mapped[bool] = mapped_column(default=False)
    
    # Book condition
    issue_condition: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    return_condition: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Staff
    issued_by: Mapped[UUID] = mapped_column(
        ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False
    )
    returned_to: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("employees.id", ondelete="SET NULL"), nullable=True
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
    book: Mapped["Book"] = relationship("Book", back_populates="transactions")
    member: Mapped["Student"] = relationship("Student", lazy="selectin")
    issuer: Mapped["Employee"] = relationship(
        "Employee", foreign_keys=[issued_by], lazy="selectin"
    )
    returner: Mapped[Optional["Employee"]] = relationship(
        "Employee", foreign_keys=[returned_to], lazy="selectin"
    )
    
    def __repr__(self) -> str:
        return f"<BookTransaction(id={self.id}, type={self.transaction_type}, status={self.status})>"
