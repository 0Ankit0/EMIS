"""Comprehensive tests for Accounting Service"""
import pytest
from datetime import datetime
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.accounting_service import AccountingService


@pytest.fixture
def accounting_service():
    return AccountingService()


@pytest.mark.asyncio
async def test_record_transaction(db_session: AsyncSession, accounting_service: AccountingService):
    """Test recording financial transaction"""
    transaction_data = {
        "transaction_type": "income",
        "amount": Decimal("50000.00"),
        "category": "tuition_fee",
        "description": "Semester fee payment",
        "reference_id": str(uuid4())
    }
    
    transaction = await accounting_service.record_transaction(db_session, transaction_data)
    
    assert transaction is not None
    assert transaction.amount == Decimal("50000.00")
    assert transaction.transaction_type == "income"


@pytest.mark.asyncio
async def test_calculate_balance(accounting_service: AccountingService):
    """Test balance calculation"""
    income = Decimal("100000.00")
    expenses = Decimal("60000.00")
    
    balance = accounting_service.calculate_balance(income, expenses)
    
    assert balance == Decimal("40000.00")


@pytest.mark.asyncio
async def test_generate_ledger(db_session: AsyncSession, accounting_service: AccountingService):
    """Test ledger generation"""
    ledger = await accounting_service.generate_ledger(
        db_session,
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31)
    )
    
    assert ledger is not None
    assert "transactions" in ledger or isinstance(ledger, list)


@pytest.mark.asyncio
async def test_calculate_profit_loss(db_session: AsyncSession, accounting_service: AccountingService):
    """Test profit/loss calculation"""
    # Record income
    await accounting_service.record_transaction(db_session, {
        "transaction_type": "income",
        "amount": Decimal("100000.00"),
        "category": "fees"
    })
    
    # Record expense
    await accounting_service.record_transaction(db_session, {
        "transaction_type": "expense",
        "amount": Decimal("60000.00"),
        "category": "salaries"
    })
    
    pl_statement = await accounting_service.calculate_profit_loss(
        db_session,
        period="monthly"
    )
    
    assert pl_statement is not None


@pytest.mark.asyncio
async def test_generate_balance_sheet(db_session: AsyncSession, accounting_service: AccountingService):
    """Test balance sheet generation"""
    balance_sheet = await accounting_service.generate_balance_sheet(
        db_session,
        as_of_date=datetime(2024, 12, 31)
    )
    
    assert balance_sheet is not None
    assert "assets" in balance_sheet or "liabilities" in balance_sheet


@pytest.mark.asyncio
async def test_record_expense(db_session: AsyncSession, accounting_service: AccountingService):
    """Test expense recording"""
    expense_data = {
        "amount": Decimal("25000.00"),
        "category": "utilities",
        "description": "Electricity bill",
        "paid_by": uuid4()
    }
    
    expense = await accounting_service.record_expense(db_session, expense_data)
    
    assert expense is not None
    assert expense.amount == Decimal("25000.00")


@pytest.mark.asyncio
async def test_reconcile_accounts(db_session: AsyncSession, accounting_service: AccountingService):
    """Test account reconciliation"""
    reconciliation = await accounting_service.reconcile_accounts(
        db_session,
        account_id=uuid4(),
        statement_balance=Decimal("50000.00")
    )
    
    assert reconciliation is not None


@pytest.mark.asyncio
async def test_generate_financial_report(db_session: AsyncSession, accounting_service: AccountingService):
    """Test financial report generation"""
    report = await accounting_service.generate_financial_report(
        db_session,
        report_type="monthly",
        month=1,
        year=2024
    )
    
    assert report is not None


@pytest.mark.asyncio
async def test_get_account_balance(db_session: AsyncSession, accounting_service: AccountingService):
    """Test getting account balance"""
    balance = await accounting_service.get_account_balance(
        db_session,
        account_id=uuid4()
    )
    
    assert balance is not None or balance == Decimal("0.00")


@pytest.mark.asyncio
async def test_categorize_transaction(accounting_service: AccountingService):
    """Test transaction categorization"""
    category = accounting_service.categorize_transaction(
        description="Student fee payment"
    )
    
    assert category in ["tuition", "fees", "other"]
