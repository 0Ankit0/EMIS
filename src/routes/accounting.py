"""Accounting API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from pydantic import BaseModel

from src.database import get_db
from src.services.accounting_service import AccountingService
from src.models.accounting import TransactionType
from src.middleware.rbac import require_permissions

router = APIRouter(prefix="/accounting", tags=["accounting"])


class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category_id: Optional[int] = None
    description: Optional[str] = None
    paid_to: Optional[str] = None
    payment_method: Optional[str] = None


class IncomeCreate(BaseModel):
    title: str
    amount: float
    category_id: Optional[int] = None
    description: Optional[str] = None
    received_from: Optional[str] = None
    payment_method: Optional[str] = None


class ExpenseCategoryCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class IncomeCategoryCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


@router.post("/expenses", status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:write"]))
):
    """Record a new expense"""
    service = AccountingService(db)
    
    expense = await service.record_expense(
        **expense_data.dict(),
        created_by=current_user.get("id")
    )
    
    return {
        "id": expense.id,
        "expense_number": expense.expense_number,
        "title": expense.title,
        "amount": expense.total_amount,
        "journal_entry_id": expense.journal_entry_id
    }


@router.post("/income", status_code=status.HTTP_201_CREATED)
async def create_income(
    income_data: IncomeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:write"]))
):
    """Record new income"""
    service = AccountingService(db)
    
    income = await service.record_income(
        **income_data.dict(),
        recorded_by=current_user.get("id")
    )
    
    return {
        "id": income.id,
        "income_number": income.income_number,
        "title": income.title,
        "amount": income.total_amount,
        "journal_entry_id": income.journal_entry_id
    }


@router.get("/balance")
async def get_balance(
    financial_year: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:read"]))
):
    """Get account balance"""
    service = AccountingService(db)
    balance = await service.get_balance(financial_year, start_date, end_date)
    return balance


@router.post("/expense-categories", status_code=status.HTTP_201_CREATED)
async def create_expense_category(
    category_data: ExpenseCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:admin"]))
):
    """Create expense category"""
    service = AccountingService(db)
    category = await service.create_expense_category(**category_data.dict())
    return {"id": category.id, "name": category.name, "code": category.code}


@router.post("/income-categories", status_code=status.HTTP_201_CREATED)
async def create_income_category(
    category_data: IncomeCategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:admin"]))
):
    """Create income category"""
    service = AccountingService(db)
    category = await service.create_income_category(**category_data.dict())
    return {"id": category.id, "name": category.name, "code": category.code}

# T236: Chart of Accounts endpoints
class AccountCreate(BaseModel):
    account_code: str
    account_name: str
    account_type: str
    normal_balance: str
    description: Optional[str] = None
    parent_account_id: Optional[int] = None
    is_header: bool = False


@router.post("/chart-of-accounts", status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:admin"]))
):
    """Create account in chart of accounts (T236)"""
    service = AccountingService(db)
    account = await service.create_account(**account_data.dict())
    return {
        "id": account.id,
        "account_code": account.account_code,
        "account_name": account.account_name,
        "account_type": account.account_type
    }


@router.get("/chart-of-accounts")
async def get_chart_of_accounts(
    account_type: Optional[str] = None,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:read"]))
):
    """Get chart of accounts (T236)"""
    service = AccountingService(db)
    accounts = await service.get_chart_of_accounts(account_type, active_only)
    return {
        "accounts": [
            {
                "id": a.id,
                "account_code": a.account_code,
                "account_name": a.account_name,
                "account_type": a.account_type,
                "current_balance": a.current_balance,
                "normal_balance": a.normal_balance
            }
            for a in accounts
        ]
    }


# T237: General Ledger endpoints
@router.get("/general-ledger")
async def get_general_ledger(
    account_id: Optional[int] = None,
    financial_year: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:read"]))
):
    """Get general ledger entries (T237)"""
    service = AccountingService(db)
    entries = await service.get_ledger_entries(account_id, financial_year, start_date, end_date)
    return {
        "entries": [
            {
                "id": e.id,
                "transaction_date": e.transaction_date,
                "description": e.description,
                "debit_amount": e.debit_amount,
                "credit_amount": e.credit_amount,
                "balance_after": e.balance_after,
                "account_id": e.account_id
            }
            for e in entries
        ]
    }


@router.get("/trial-balance")
async def get_trial_balance(
    financial_year: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:read"]))
):
    """Get trial balance report (T237)"""
    service = AccountingService(db)
    trial_balance = await service.get_trial_balance(financial_year)
    return trial_balance


# T238: Budget Tracking endpoints
class BudgetCreate(BaseModel):
    financial_year: str
    allocated_amount: float
    account_id: Optional[int] = None
    expense_category_id: Optional[int] = None
    department: Optional[str] = None
    quarter: Optional[int] = None


@router.post("/budgets", status_code=status.HTTP_201_CREATED)
async def create_budget(
    budget_data: BudgetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:admin"]))
):
    """Create budget allocation (T238)"""
    service = AccountingService(db)
    budget = await service.create_budget(
        **budget_data.dict(),
        approver_id=current_user.get("id")
    )
    return {
        "id": budget.id,
        "financial_year": budget.financial_year,
        "allocated_amount": budget.allocated_amount,
        "remaining_amount": budget.remaining_amount
    }


@router.get("/budgets/report")
async def get_budget_report(
    financial_year: str,
    quarter: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:read"]))
):
    """Get budget vs actual report (T238)"""
    service = AccountingService(db)
    report = await service.get_budget_report(financial_year, quarter)
    return report


# T239: Bank Reconciliation endpoints
class BankReconciliationCreate(BaseModel):
    bank_account_id: int
    statement_date: date
    period_from: date
    period_to: date
    statement_opening_balance: float
    statement_closing_balance: float
    book_opening_balance: float
    book_closing_balance: float


class BankReconciliationPerform(BaseModel):
    outstanding_deposits: float = 0.0
    outstanding_checks: float = 0.0
    bank_charges: float = 0.0
    bank_interest: float = 0.0
    other_adjustments: float = 0.0


@router.post("/bank-reconciliation", status_code=status.HTTP_201_CREATED)
async def create_bank_reconciliation(
    recon_data: BankReconciliationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:admin"]))
):
    """Create bank reconciliation (T239)"""
    service = AccountingService(db)
    reconciliation = await service.create_bank_reconciliation(**recon_data.dict())
    return {
        "id": reconciliation.id,
        "reconciliation_number": reconciliation.reconciliation_number,
        "statement_date": reconciliation.statement_date,
        "difference": reconciliation.difference
    }


@router.post("/bank-reconciliation/{reconciliation_id}/perform")
async def perform_bank_reconciliation(
    reconciliation_id: int,
    recon_data: BankReconciliationPerform,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:admin"]))
):
    """Perform bank reconciliation (T239)"""
    service = AccountingService(db)
    reconciliation = await service.perform_bank_reconciliation(
        reconciliation_id=reconciliation_id,
        **recon_data.dict(),
        reconciler_id=current_user.get("id")
    )
    return {
        "id": reconciliation.id,
        "reconciliation_number": reconciliation.reconciliation_number,
        "reconciled_balance": reconciliation.reconciled_balance,
        "statement_closing_balance": reconciliation.statement_closing_balance,
        "difference": reconciliation.difference,
        "is_reconciled": reconciliation.is_reconciled
    }


@router.get("/bank-reconciliation/{bank_account_id}/unreconciled")
async def get_unreconciled_items(
    bank_account_id: int,
    period_from: date,
    period_to: date,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_permissions(["accounting:read"]))
):
    """Get unreconciled bank items (T239)"""
    service = AccountingService(db)
    items = await service.get_unreconciled_items(bank_account_id, period_from, period_to)
    return items
