"""Enhanced Accounting Models for EMIS"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Float, Boolean, Enum, Text, JSON
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class TransactionType(str, enum.Enum):
    """Enumeration for transaction types"""
    DEBIT = "debit"
    CREDIT = "credit"


class ExpenseCategory(Base):
    """Expense Category model for classification"""
    __tablename__ = "expense_categories"

    id = Column(Integer, primary_key=True, index=True)
    
    # Category details
    name = Column(String(200), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Hierarchy
    parent_id = Column(Integer, ForeignKey("expense_categories.id", ondelete="SET NULL"), nullable=True)
    
    # Budget tracking
    monthly_budget = Column(Float, nullable=True)
    quarterly_budget = Column(Float, nullable=True)
    annual_budget = Column(Float, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    parent = relationship("ExpenseCategory", remote_side=[id], back_populates="children")
    children = relationship("ExpenseCategory", back_populates="parent")
    expenses = relationship("Expense", back_populates="category")
    
    def __repr__(self):
        return f"<ExpenseCategory(id={self.id}, name={self.name}, code={self.code})>"


class IncomeCategory(Base):
    """Income Category model for classification"""
    __tablename__ = "income_categories"

    id = Column(Integer, primary_key=True, index=True)
    
    # Category details
    name = Column(String(200), unique=True, nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Hierarchy
    parent_id = Column(Integer, ForeignKey("income_categories.id", ondelete="SET NULL"), nullable=True)
    
    # Target tracking
    monthly_target = Column(Float, nullable=True)
    quarterly_target = Column(Float, nullable=True)
    annual_target = Column(Float, nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    parent = relationship("IncomeCategory", remote_side=[id], back_populates="children")
    children = relationship("IncomeCategory", back_populates="parent")
    incomes = relationship("Income", back_populates="category")
    
    def __repr__(self):
        return f"<IncomeCategory(id={self.id}, name={self.name}, code={self.code})>"


class JournalEntry(Base):
    """Enhanced Journal Entry model for double-entry accounting"""
    __tablename__ = "journal_entries"

    id = Column(Integer, primary_key=True, index=True)
    
    # Entry identification
    entry_number = Column(String(50), unique=True, nullable=False, index=True)
    entry_date = Column(Date, default=date.today, nullable=False)
    
    # Transaction details
    transaction_type = Column(Enum(TransactionType), nullable=False)
    
    # Account details
    account_code = Column(String(50), nullable=False, index=True)
    account_name = Column(String(200), nullable=False)
    
    # Amount
    debit_amount = Column(Float, default=0.0, nullable=False)
    credit_amount = Column(Float, default=0.0, nullable=False)
    
    # Description
    description = Column(Text, nullable=False)
    reference_number = Column(String(100), nullable=True)
    
    # Categorization
    category_id = Column(Integer, nullable=True)  # Could be expense or income category
    category_type = Column(String(20), nullable=True)  # 'expense' or 'income'
    
    # Period
    financial_year = Column(String(20), nullable=False)
    quarter = Column(Integer, nullable=True)  # 1, 2, 3, 4
    month = Column(Integer, nullable=True)  # 1-12
    
    # Source tracking
    source_type = Column(String(50), nullable=True)  # 'bill', 'payment', 'expense', 'income', etc.
    source_id = Column(Integer, nullable=True)
    
    # Approval workflow
    is_approved = Column(Boolean, default=False, nullable=False)
    approved_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    approver = relationship("Employee", foreign_keys=[approved_by])
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<JournalEntry(id={self.id}, number={self.entry_number}, type={self.transaction_type}, amount={self.debit_amount or self.credit_amount})>"


class Expense(Base):
    """Expense model for tracking all institutional expenses"""
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    
    # Expense details
    expense_number = Column(String(50), unique=True, nullable=False, index=True)
    expense_date = Column(Date, default=date.today, nullable=False)
    
    # Category
    category_id = Column(Integer, ForeignKey("expense_categories.id", ondelete="SET NULL"), nullable=True)
    
    # Description
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    
    # Amount
    amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Payment
    payment_method = Column(String(50), nullable=True)
    payment_reference = Column(String(100), nullable=True)
    paid_to = Column(String(200), nullable=True)
    
    # Documentation
    invoice_number = Column(String(100), nullable=True)
    supporting_documents = Column(JSON, nullable=True)
    
    # Accounting
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id", ondelete="SET NULL"), nullable=True)
    
    # Period
    financial_year = Column(String(20), nullable=False)
    quarter = Column(Integer, nullable=True)
    
    # Approval
    approved_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    category = relationship("ExpenseCategory", back_populates="expenses")
    approver = relationship("Employee", foreign_keys=[approved_by])
    creator = relationship("User", foreign_keys=[created_by])
    journal_entry = relationship("JournalEntry", foreign_keys=[journal_entry_id])
    
    def __repr__(self):
        return f"<Expense(id={self.id}, number={self.expense_number}, amount={self.total_amount})>"


class Income(Base):
    """Income model for tracking all institutional income"""
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    
    # Income details
    income_number = Column(String(50), unique=True, nullable=False, index=True)
    income_date = Column(Date, default=date.today, nullable=False)
    
    # Category
    category_id = Column(Integer, ForeignKey("income_categories.id", ondelete="SET NULL"), nullable=True)
    
    # Description
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    
    # Amount
    amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0, nullable=False)
    total_amount = Column(Float, nullable=False)
    
    # Payment
    payment_method = Column(String(50), nullable=True)
    payment_reference = Column(String(100), nullable=True)
    received_from = Column(String(200), nullable=True)
    
    # Documentation
    receipt_number = Column(String(100), nullable=True)
    supporting_documents = Column(JSON, nullable=True)
    
    # Accounting
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id", ondelete="SET NULL"), nullable=True)
    
    # Period
    financial_year = Column(String(20), nullable=False)
    quarter = Column(Integer, nullable=True)
    
    # Recording
    recorded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    category = relationship("IncomeCategory", back_populates="incomes")
    recorder = relationship("User", foreign_keys=[recorded_by])
    journal_entry = relationship("JournalEntry", foreign_keys=[journal_entry_id])
    
    def __repr__(self):
        return f"<Income(id={self.id}, number={self.income_number}, amount={self.total_amount})>"


# T236: Chart of Accounts
class ChartOfAccounts(Base):
    """Chart of Accounts model for accounting structure"""
    __tablename__ = "chart_of_accounts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Account details
    account_code = Column(String(50), unique=True, nullable=False, index=True)
    account_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Account type
    account_type = Column(String(50), nullable=False)  # asset, liability, equity, revenue, expense
    account_category = Column(String(100), nullable=True)
    
    # Hierarchy
    parent_account_id = Column(Integer, ForeignKey("chart_of_accounts.id", ondelete="SET NULL"), nullable=True)
    
    # Balance tracking
    current_balance = Column(Float, default=0.0, nullable=False)
    normal_balance = Column(String(10), nullable=False)  # debit or credit
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_header = Column(Boolean, default=False, nullable=False)  # Header account (no transactions)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    parent_account = relationship("ChartOfAccounts", remote_side=[id], back_populates="sub_accounts")
    sub_accounts = relationship("ChartOfAccounts", back_populates="parent_account")
    
    def __repr__(self):
        return f"<ChartOfAccounts(code={self.account_code}, name={self.account_name})>"


# T237: General Ledger
class GeneralLedger(Base):
    """General Ledger model for complete transaction history"""
    __tablename__ = "general_ledger"

    id = Column(Integer, primary_key=True, index=True)
    
    # Transaction reference
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(Integer, ForeignKey("chart_of_accounts.id", ondelete="CASCADE"), nullable=False)
    
    # Transaction details
    transaction_date = Column(Date, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Amounts
    debit_amount = Column(Float, default=0.0, nullable=False)
    credit_amount = Column(Float, default=0.0, nullable=False)
    balance_after = Column(Float, nullable=False)  # Running balance
    
    # References
    source_type = Column(String(50), nullable=True)  # payment, expense, income, etc.
    source_id = Column(Integer, nullable=True)
    
    # Financial period
    financial_year = Column(String(20), nullable=False)
    quarter = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    journal_entry = relationship("JournalEntry")
    account = relationship("ChartOfAccounts")
    
    def __repr__(self):
        return f"<GeneralLedger(id={self.id}, account={self.account_id}, date={self.transaction_date})>"


# T239: Bank Reconciliation
class BankReconciliation(Base):
    """Bank Reconciliation model for matching bank statements"""
    __tablename__ = "bank_reconciliations"

    id = Column(Integer, primary_key=True, index=True)
    
    # Reconciliation period
    reconciliation_number = Column(String(50), unique=True, nullable=False, index=True)
    bank_account_id = Column(Integer, ForeignKey("chart_of_accounts.id", ondelete="CASCADE"), nullable=False)
    
    # Period details
    statement_date = Column(Date, nullable=False)
    reconciliation_date = Column(Date, default=date.today, nullable=False)
    period_from = Column(Date, nullable=False)
    period_to = Column(Date, nullable=False)
    
    # Bank statement details
    statement_opening_balance = Column(Float, nullable=False)
    statement_closing_balance = Column(Float, nullable=False)
    
    # Book balance
    book_opening_balance = Column(Float, nullable=False)
    book_closing_balance = Column(Float, nullable=False)
    
    # Reconciliation adjustments
    outstanding_deposits = Column(Float, default=0.0, nullable=False)
    outstanding_checks = Column(Float, default=0.0, nullable=False)
    bank_charges = Column(Float, default=0.0, nullable=False)
    bank_interest = Column(Float, default=0.0, nullable=False)
    other_adjustments = Column(Float, default=0.0, nullable=False)
    
    # Reconciled balance
    reconciled_balance = Column(Float, nullable=False)
    difference = Column(Float, default=0.0, nullable=False)
    
    # Status
    is_reconciled = Column(Boolean, default=False, nullable=False)
    reconciled_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    unmatched_items = Column(JSON, nullable=True)  # Array of unmatched transactions
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    bank_account = relationship("ChartOfAccounts")
    reconciler = relationship("User", foreign_keys=[reconciled_by])
    
    def __repr__(self):
        return f"<BankReconciliation(number={self.reconciliation_number}, date={self.statement_date})>"


class BudgetAllocation(Base):
    """Budget Allocation model for T238"""
    __tablename__ = "budget_allocations"

    id = Column(Integer, primary_key=True, index=True)
    
    # Budget period
    financial_year = Column(String(20), nullable=False)
    quarter = Column(Integer, nullable=True)  # NULL means annual
    
    # Account/Category
    account_id = Column(Integer, ForeignKey("chart_of_accounts.id", ondelete="CASCADE"), nullable=True)
    expense_category_id = Column(Integer, ForeignKey("expense_categories.id", ondelete="CASCADE"), nullable=True)
    department = Column(String(100), nullable=True)
    
    # Budget amounts
    allocated_amount = Column(Float, nullable=False)
    spent_amount = Column(Float, default=0.0, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    
    # Tracking
    utilization_percentage = Column(Float, default=0.0, nullable=False)
    is_exceeded = Column(Boolean, default=False, nullable=False)
    
    # Approval
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approval_date = Column(DateTime, nullable=True)
    
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    account = relationship("ChartOfAccounts")
    expense_category = relationship("ExpenseCategory")
    approver = relationship("User", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<BudgetAllocation(year={self.financial_year}, allocated={self.allocated_amount})>"
