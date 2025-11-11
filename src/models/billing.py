"""Billing Models for EMIS"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Float, Boolean, Enum, Text, JSON
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class BillType(str, enum.Enum):
    """Enumeration for bill types"""
    TUITION_FEE = "tuition_fee"
    ADMISSION_FEE = "admission_fee"
    EXAM_FEE = "exam_fee"
    INTERNAL_EXAM_FEE = "internal_exam_fee"
    EXTERNAL_EXAM_FEE = "external_exam_fee"
    REVALUATION_FEE = "revaluation_fee"
    LIBRARY_FEE = "library_fee"
    LIBRARY_SECURITY_DEPOSIT = "library_security_deposit"
    LABORATORY_FEE = "laboratory_fee"
    SPORTS_FEE = "sports_fee"
    MAINTENANCE_FEE = "maintenance_fee"
    EMERGENCY_EXPENSE = "emergency_expense"
    TRANSPORT_FEE = "transport_fee"
    HOSTEL_FEE = "hostel_fee"
    HOSTEL_MESS_FEE = "hostel_mess_fee"
    EVENT_FEE = "event_fee"
    CULTURAL_EVENT_FEE = "cultural_event_fee"
    TECHNICAL_EVENT_FEE = "technical_event_fee"
    SPORTS_EVENT_FEE = "sports_event_fee"
    ID_CARD_FEE = "id_card_fee"
    CERTIFICATE_FEE = "certificate_fee"
    DOCUMENT_FEE = "document_fee"
    DEVELOPMENT_FEE = "development_fee"
    ALUMNI_FEE = "alumni_fee"
    PLACEMENT_FEE = "placement_fee"
    MISCELLANEOUS = "miscellaneous"
    FINE = "fine"
    CAUTION_DEPOSIT = "caution_deposit"


class BillStatus(str, enum.Enum):
    """Enumeration for bill status"""
    DRAFT = "draft"
    GENERATED = "generated"
    SENT = "sent"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(str, enum.Enum):
    """Enumeration for payment methods"""
    CASH = "cash"
    CHEQUE = "cheque"
    BANK_TRANSFER = "bank_transfer"
    UPI = "upi"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    NET_BANKING = "net_banking"
    ONLINE_GATEWAY = "online_gateway"


class Bill(Base):
    """Bill model for student/staff billing"""
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    bill_number = Column(String(50), unique=True, nullable=False, index=True)
    
    # Billable entity (Student or Employee)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=True)
    
    # Bill details
    bill_type = Column(Enum(BillType), nullable=False)
    bill_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Financial details
    subtotal = Column(Float, nullable=False, default=0.0)
    tax_amount = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0, nullable=False)
    amount_due = Column(Float, nullable=False)
    
    status = Column(Enum(BillStatus), default=BillStatus.DRAFT, nullable=False)
    
    # Academic context
    academic_year = Column(String(20), nullable=True)
    semester = Column(Integer, nullable=True)
    quarter = Column(Integer, nullable=True)
    
    # Payment details
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    payment_date = Column(DateTime, nullable=True)
    
    # Installment support (T209)
    has_installments = Column(Boolean, default=False, nullable=False)
    installments = Column(JSON, nullable=True)  # Array of installment details
    
    # Late fee tracking (T208)
    late_fee_applied = Column(Boolean, default=False, nullable=False)
    late_fee_amount = Column(Float, default=0.0, nullable=False)
    
    # Email tracking (T213)
    email_sent = Column(Boolean, default=False, nullable=False)
    email_sent_date = Column(DateTime, nullable=True)
    email_recipient = Column(String(255), nullable=True)
    
    # Notes and description
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    terms_and_conditions = Column(Text, nullable=True)
    
    # File storage
    pdf_path = Column(String(500), nullable=True)
    
    # Metadata
    generated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    sent_to_email = Column(String(255), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="bills")
    employee = relationship("Employee", back_populates="bills")
    items = relationship("BillItem", back_populates="bill", cascade="all, delete-orphan")
    generator = relationship("User", foreign_keys=[generated_by])
    
    def __repr__(self):
        return f"<Bill(id={self.id}, number={self.bill_number}, type={self.bill_type}, amount={self.total_amount}, status={self.status})>"


class BillItem(Base):
    """Bill Item model for line items in a bill"""
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id", ondelete="CASCADE"), nullable=False)
    
    # Item details
    item_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Pricing
    quantity = Column(Float, default=1.0, nullable=False)
    unit_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)  # quantity * unit_price
    
    # Tax and discount
    tax_percentage = Column(Float, default=0.0, nullable=False)
    discount_percentage = Column(Float, default=0.0, nullable=False)
    
    # Categorization
    category = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    bill = relationship("Bill", back_populates="items")
    
    def __repr__(self):
        return f"<BillItem(id={self.id}, name={self.item_name}, amount={self.amount})>"


class MaintenanceFee(Base):
    """Maintenance Fee model for school/college infrastructure"""
    __tablename__ = "maintenance_fees"

    id = Column(Integer, primary_key=True, index=True)
    
    # Fee structure
    fee_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Float, nullable=False)
    
    # Applicability
    applies_to_students = Column(Boolean, default=True, nullable=False)
    applies_to_employees = Column(Boolean, default=False, nullable=False)
    
    # Frequency
    frequency = Column(String(50), default="yearly", nullable=False)  # yearly, semester, quarterly, monthly
    
    # Active period
    academic_year = Column(String(20), nullable=True)
    effective_from = Column(Date, nullable=False)
    effective_to = Column(Date, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<MaintenanceFee(id={self.id}, name={self.fee_name}, amount={self.amount})>"


class EmergencyExpense(Base):
    """Emergency Expense model for tracking urgent institutional expenses"""
    __tablename__ = "emergency_expenses"

    id = Column(Integer, primary_key=True, index=True)
    
    # Expense details
    expense_title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    
    # Financial details
    amount = Column(Float, nullable=False)
    approved_amount = Column(Float, nullable=True)
    
    # Priority and urgency
    priority = Column(String(20), default="medium", nullable=False)  # low, medium, high, critical
    is_emergency = Column(Boolean, default=True, nullable=False)
    
    # Approval workflow
    requested_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    approved_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    # Payment tracking
    is_paid = Column(Boolean, default=False, nullable=False)
    paid_amount = Column(Float, default=0.0, nullable=False)
    paid_date = Column(DateTime, nullable=True)
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    
    # Documentation
    justification = Column(Text, nullable=True)
    supporting_documents = Column(JSON, nullable=True)  # Array of file paths
    
    # Accounting
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id", ondelete="SET NULL"), nullable=True)
    expense_category_id = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    requester = relationship("Employee", foreign_keys=[requested_by])
    approver = relationship("Employee", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<EmergencyExpense(id={self.id}, title={self.expense_title}, amount={self.amount}, priority={self.priority})>"
