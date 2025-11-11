"""Accounting Service for EMIS"""
from datetime import datetime, date
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, extract

from src.models.accounting import (
    JournalEntry, TransactionType, ExpenseCategory, IncomeCategory,
    Expense, Income
)
from src.lib.logging import get_logger

logger = get_logger(__name__)


class AccountingService:
    """Service for double-entry accounting operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def get_current_financial_year(self) -> str:
        """Get current financial year (Apr-Mar)"""
        today = date.today()
        if today.month >= 4:
            return f"{today.year}-{today.year + 1}"
        else:
            return f"{today.year - 1}-{today.year}"
    
    def get_quarter(self, date_obj: date) -> int:
        """Get quarter number (1-4) for a date"""
        # Financial year: Apr-Mar
        # Q1: Apr-Jun, Q2: Jul-Sep, Q3: Oct-Dec, Q4: Jan-Mar
        month = date_obj.month
        if month >= 4 and month <= 6:
            return 1
        elif month >= 7 and month <= 9:
            return 2
        elif month >= 10 and month <= 12:
            return 3
        else:  # Jan-Mar
            return 4
    
    async def generate_entry_number(self) -> str:
        """Generate unique journal entry number"""
        today = date.today()
        year_month = today.strftime("%Y%m")
        
        result = await self.db.execute(
            select(func.count(JournalEntry.id)).where(
                JournalEntry.entry_number.like(f"JE{year_month}%")
            )
        )
        count = result.scalar() or 0
        sequence = str(count + 1).zfill(4)
        
        return f"JE{year_month}{sequence}"
    
    async def create_journal_entry(
        self,
        transaction_type: TransactionType,
        account_code: str,
        account_name: str,
        debit_amount: float = 0.0,
        credit_amount: float = 0.0,
        description: str = "",
        reference_number: Optional[str] = None,
        source_type: Optional[str] = None,
        source_id: Optional[int] = None,
        created_by: Optional[int] = None
    ) -> JournalEntry:
        """Create a journal entry"""
        
        entry_number = await self.generate_entry_number()
        entry_date = date.today()
        financial_year = self.get_current_financial_year()
        quarter = self.get_quarter(entry_date)
        
        entry = JournalEntry(
            entry_number=entry_number,
            entry_date=entry_date,
            transaction_type=transaction_type,
            account_code=account_code,
            account_name=account_name,
            debit_amount=debit_amount,
            credit_amount=credit_amount,
            description=description,
            reference_number=reference_number,
            financial_year=financial_year,
            quarter=quarter,
            month=entry_date.month,
            source_type=source_type,
            source_id=source_id,
            created_by=created_by
        )
        
        self.db.add(entry)
        await self.db.commit()
        await self.db.refresh(entry)
        
        logger.info(f"Created journal entry {entry_number}: {account_name} Dr:{debit_amount} Cr:{credit_amount}")
        
        return entry
    
    async def record_expense(
        self,
        title: str,
        amount: float,
        category_id: Optional[int] = None,
        description: Optional[str] = None,
        paid_to: Optional[str] = None,
        payment_method: Optional[str] = None,
        created_by: Optional[int] = None
    ) -> Expense:
        """Record an expense with journal entry"""
        
        # Generate expense number
        today = date.today()
        year_month = today.strftime("%Y%m")
        result = await self.db.execute(
            select(func.count(Expense.id)).where(
                Expense.expense_number.like(f"EXP{year_month}%")
            )
        )
        count = result.scalar() or 0
        expense_number = f"EXP{year_month}{str(count + 1).zfill(4)}"
        
        # Create expense
        expense = Expense(
            expense_number=expense_number,
            expense_date=today,
            category_id=category_id,
            title=title,
            description=description,
            amount=amount,
            total_amount=amount,
            payment_method=payment_method,
            paid_to=paid_to,
            financial_year=self.get_current_financial_year(),
            quarter=self.get_quarter(today),
            created_by=created_by
        )
        
        self.db.add(expense)
        await self.db.commit()
        await self.db.refresh(expense)
        
        # Create journal entry (Debit: Expense, Credit: Cash/Bank)
        journal_entry = await self.create_journal_entry(
            transaction_type=TransactionType.DEBIT,
            account_code="6000",  # Expense account
            account_name=title,
            debit_amount=amount,
            credit_amount=0.0,
            description=f"Expense: {title}",
            source_type="expense",
            source_id=expense.id,
            created_by=created_by
        )
        
        expense.journal_entry_id = journal_entry.id
        await self.db.commit()
        
        logger.info(f"Recorded expense {expense_number}: {title} ₹{amount}")
        
        return expense
    
    async def record_income(
        self,
        title: str,
        amount: float,
        category_id: Optional[int] = None,
        description: Optional[str] = None,
        received_from: Optional[str] = None,
        payment_method: Optional[str] = None,
        recorded_by: Optional[int] = None
    ) -> Income:
        """Record income with journal entry"""
        
        # Generate income number
        today = date.today()
        year_month = today.strftime("%Y%m")
        result = await self.db.execute(
            select(func.count(Income.id)).where(
                Income.income_number.like(f"INC{year_month}%")
            )
        )
        count = result.scalar() or 0
        income_number = f"INC{year_month}{str(count + 1).zfill(4)}"
        
        # Create income
        income = Income(
            income_number=income_number,
            income_date=today,
            category_id=category_id,
            title=title,
            description=description,
            amount=amount,
            total_amount=amount,
            payment_method=payment_method,
            received_from=received_from,
            financial_year=self.get_current_financial_year(),
            quarter=self.get_quarter(today),
            recorded_by=recorded_by
        )
        
        self.db.add(income)
        await self.db.commit()
        await self.db.refresh(income)
        
        # Create journal entry (Debit: Cash/Bank, Credit: Income)
        journal_entry = await self.create_journal_entry(
            transaction_type=TransactionType.CREDIT,
            account_code="4000",  # Income account
            account_name=title,
            debit_amount=0.0,
            credit_amount=amount,
            description=f"Income: {title}",
            source_type="income",
            source_id=income.id,
            created_by=recorded_by
        )
        
        income.journal_entry_id = journal_entry.id
        await self.db.commit()
        
        logger.info(f"Recorded income {income_number}: {title} ₹{amount}")
        
        return income
    
    async def get_balance(
        self,
        financial_year: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, float]:
        """Get total debits and credits"""
        
        query = select(
            func.sum(JournalEntry.debit_amount).label('total_debit'),
            func.sum(JournalEntry.credit_amount).label('total_credit')
        )
        
        if financial_year:
            query = query.where(JournalEntry.financial_year == financial_year)
        
        if start_date and end_date:
            query = query.where(
                and_(
                    JournalEntry.entry_date >= start_date,
                    JournalEntry.entry_date <= end_date
                )
            )
        
        result = await self.db.execute(query)
        row = result.first()
        
        total_debit = float(row.total_debit or 0)
        total_credit = float(row.total_credit or 0)
        
        return {
            "total_debit": total_debit,
            "total_credit": total_credit,
            "balance": total_credit - total_debit  # Net income
        }
    
    async def create_expense_category(
        self,
        name: str,
        code: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None
    ) -> ExpenseCategory:
        """Create expense category"""
        
        category = ExpenseCategory(
            name=name,
            code=code,
            description=description,
            parent_id=parent_id
        )
        
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        
        return category
    
    async def create_income_category(
        self,
        name: str,
        code: str,
        description: Optional[str] = None,
        parent_id: Optional[int] = None
    ) -> IncomeCategory:
        """Create income category"""
        
        category = IncomeCategory(
            name=name,
            code=code,
            description=description,
            parent_id=parent_id
        )
        
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        
        return category
    
    async def get_expenses_by_quarter(
        self,
        financial_year: str,
        quarter: int
    ) -> List[Expense]:
        """Get expenses for a quarter"""
        
        result = await self.db.execute(
            select(Expense).where(
                and_(
                    Expense.financial_year == financial_year,
                    Expense.quarter == quarter
                )
            ).order_by(Expense.expense_date.desc())
        )
        return result.scalars().all()
    
    async def get_income_by_quarter(
        self,
        financial_year: str,
        quarter: int
    ) -> List[Income]:
        """Get income for a quarter"""
        
        result = await self.db.execute(
            select(Income).where(
                and_(
                    Income.financial_year == financial_year,
                    Income.quarter == quarter
                )
            ).order_by(Income.income_date.desc())
        )
        return result.scalars().all()
    
    # T236: Chart of Accounts Management
    async def create_account(
        self,
        account_code: str,
        account_name: str,
        account_type: str,
        normal_balance: str,
        description: Optional[str] = None,
        parent_account_id: Optional[int] = None,
        is_header: bool = False
    ):
        """Create new account in chart of accounts"""
        from src.models.accounting import ChartOfAccounts
        
        account = ChartOfAccounts(
            account_code=account_code,
            account_name=account_name,
            description=description,
            account_type=account_type,
            normal_balance=normal_balance,
            parent_account_id=parent_account_id,
            is_header=is_header
        )
        
        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)
        
        logger.info(f"Created account: {account_code} - {account_name}")
        
        return account
    
    async def get_chart_of_accounts(
        self,
        account_type: Optional[str] = None,
        active_only: bool = True
    ):
        """Get chart of accounts"""
        from src.models.accounting import ChartOfAccounts
        
        query = select(ChartOfAccounts)
        
        if account_type:
            query = query.where(ChartOfAccounts.account_type == account_type)
        
        if active_only:
            query = query.where(ChartOfAccounts.is_active == True)
        
        query = query.order_by(ChartOfAccounts.account_code)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_account_balance(
        self,
        account_id: int,
        amount: float,
        is_debit: bool
    ):
        """Update account balance"""
        from src.models.accounting import ChartOfAccounts
        
        result = await self.db.execute(
            select(ChartOfAccounts).where(ChartOfAccounts.id == account_id)
        )
        account = result.scalar_one_or_none()
        
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Update based on normal balance
        if account.normal_balance == "debit":
            if is_debit:
                account.current_balance += amount
            else:
                account.current_balance -= amount
        else:  # credit
            if is_debit:
                account.current_balance -= amount
            else:
                account.current_balance += amount
        
        await self.db.commit()
        await self.db.refresh(account)
        
        return account
    
    # T237: General Ledger Functionality
    async def post_to_ledger(
        self,
        journal_entry_id: int,
        account_id: int,
        debit_amount: float,
        credit_amount: float,
        description: str,
        source_type: Optional[str] = None,
        source_id: Optional[int] = None
    ):
        """Post entry to general ledger"""
        from src.models.accounting import GeneralLedger, ChartOfAccounts
        
        # Get current account balance
        result = await self.db.execute(
            select(ChartOfAccounts).where(ChartOfAccounts.id == account_id)
        )
        account = result.scalar_one_or_none()
        
        if not account:
            raise ValueError(f"Account {account_id} not found")
        
        # Calculate new balance
        if account.normal_balance == "debit":
            balance_after = account.current_balance + debit_amount - credit_amount
        else:
            balance_after = account.current_balance + credit_amount - debit_amount
        
        # Create ledger entry
        financial_year = self.get_current_financial_year()
        transaction_date = date.today()
        
        ledger_entry = GeneralLedger(
            journal_entry_id=journal_entry_id,
            account_id=account_id,
            transaction_date=transaction_date,
            description=description,
            debit_amount=debit_amount,
            credit_amount=credit_amount,
            balance_after=balance_after,
            source_type=source_type,
            source_id=source_id,
            financial_year=financial_year,
            quarter=self.get_quarter(transaction_date)
        )
        
        self.db.add(ledger_entry)
        
        # Update account balance
        await self.update_account_balance(account_id, abs(debit_amount - credit_amount), debit_amount > 0)
        
        await self.db.commit()
        await self.db.refresh(ledger_entry)
        
        return ledger_entry
    
    async def get_ledger_entries(
        self,
        account_id: Optional[int] = None,
        financial_year: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ):
        """Get general ledger entries"""
        from src.models.accounting import GeneralLedger
        
        query = select(GeneralLedger)
        
        if account_id:
            query = query.where(GeneralLedger.account_id == account_id)
        
        if financial_year:
            query = query.where(GeneralLedger.financial_year == financial_year)
        
        if start_date:
            query = query.where(GeneralLedger.transaction_date >= start_date)
        
        if end_date:
            query = query.where(GeneralLedger.transaction_date <= end_date)
        
        query = query.order_by(GeneralLedger.transaction_date.desc())
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_trial_balance(
        self,
        financial_year: Optional[str] = None
    ) -> Dict:
        """Generate trial balance"""
        from src.models.accounting import ChartOfAccounts
        
        if not financial_year:
            financial_year = self.get_current_financial_year()
        
        # Get all active accounts with balances
        result = await self.db.execute(
            select(ChartOfAccounts).where(
                and_(
                    ChartOfAccounts.is_active == True,
                    ChartOfAccounts.is_header == False
                )
            ).order_by(ChartOfAccounts.account_code)
        )
        accounts = result.scalars().all()
        
        total_debit = 0.0
        total_credit = 0.0
        accounts_data = []
        
        for account in accounts:
            balance = abs(account.current_balance)
            if balance > 0:
                account_data = {
                    'account_code': account.account_code,
                    'account_name': account.account_name,
                    'debit': balance if account.normal_balance == "debit" else 0.0,
                    'credit': balance if account.normal_balance == "credit" else 0.0
                }
                accounts_data.append(account_data)
                
                if account.normal_balance == "debit":
                    total_debit += balance
                else:
                    total_credit += balance
        
        return {
            'financial_year': financial_year,
            'accounts': accounts_data,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'difference': abs(total_debit - total_credit),
            'balanced': abs(total_debit - total_credit) < 0.01
        }
    
    # T238: Budget Tracking
    async def create_budget(
        self,
        financial_year: str,
        allocated_amount: float,
        account_id: Optional[int] = None,
        expense_category_id: Optional[int] = None,
        department: Optional[str] = None,
        quarter: Optional[int] = None,
        approver_id: Optional[int] = None
    ):
        """Create budget allocation"""
        from src.models.accounting import BudgetAllocation
        
        budget = BudgetAllocation(
            financial_year=financial_year,
            quarter=quarter,
            account_id=account_id,
            expense_category_id=expense_category_id,
            department=department,
            allocated_amount=allocated_amount,
            remaining_amount=allocated_amount,
            approved_by=approver_id,
            approval_date=datetime.utcnow() if approver_id else None
        )
        
        self.db.add(budget)
        await self.db.commit()
        await self.db.refresh(budget)
        
        logger.info(f"Created budget allocation for {financial_year}: ₹{allocated_amount}")
        
        return budget
    
    async def track_budget_utilization(
        self,
        budget_id: int,
        expense_amount: float
    ):
        """Track budget utilization when expense is recorded"""
        from src.models.accounting import BudgetAllocation
        
        result = await self.db.execute(
            select(BudgetAllocation).where(BudgetAllocation.id == budget_id)
        )
        budget = result.scalar_one_or_none()
        
        if not budget:
            raise ValueError(f"Budget allocation {budget_id} not found")
        
        budget.spent_amount += expense_amount
        budget.remaining_amount = budget.allocated_amount - budget.spent_amount
        budget.utilization_percentage = (budget.spent_amount / budget.allocated_amount) * 100
        budget.is_exceeded = budget.spent_amount > budget.allocated_amount
        
        await self.db.commit()
        await self.db.refresh(budget)
        
        if budget.is_exceeded:
            logger.warning(f"Budget {budget_id} exceeded! Allocated: ₹{budget.allocated_amount}, Spent: ₹{budget.spent_amount}")
        
        return budget
    
    async def get_budget_report(
        self,
        financial_year: str,
        quarter: Optional[int] = None
    ) -> Dict:
        """Get budget vs actual report"""
        from src.models.accounting import BudgetAllocation
        
        query = select(BudgetAllocation).where(
            BudgetAllocation.financial_year == financial_year
        )
        
        if quarter:
            query = query.where(BudgetAllocation.quarter == quarter)
        
        result = await self.db.execute(query)
        budgets = result.scalars().all()
        
        total_allocated = sum(b.allocated_amount for b in budgets)
        total_spent = sum(b.spent_amount for b in budgets)
        
        return {
            'financial_year': financial_year,
            'quarter': quarter,
            'total_allocated': total_allocated,
            'total_spent': total_spent,
            'total_remaining': total_allocated - total_spent,
            'overall_utilization': (total_spent / total_allocated * 100) if total_allocated > 0 else 0,
            'budgets': [
                {
                    'id': b.id,
                    'department': b.department,
                    'allocated': b.allocated_amount,
                    'spent': b.spent_amount,
                    'remaining': b.remaining_amount,
                    'utilization': b.utilization_percentage,
                    'exceeded': b.is_exceeded
                }
                for b in budgets
            ]
        }
    
    # T239: Bank Reconciliation
    async def create_bank_reconciliation(
        self,
        bank_account_id: int,
        statement_date: date,
        period_from: date,
        period_to: date,
        statement_opening_balance: float,
        statement_closing_balance: float,
        book_opening_balance: float,
        book_closing_balance: float
    ):
        """Create bank reconciliation record"""
        from src.models.accounting import BankReconciliation
        
        # Generate reconciliation number
        recon_number = f"BR{statement_date.strftime('%Y%m%d')}{bank_account_id}"
        
        reconciliation = BankReconciliation(
            reconciliation_number=recon_number,
            bank_account_id=bank_account_id,
            statement_date=statement_date,
            period_from=period_from,
            period_to=period_to,
            statement_opening_balance=statement_opening_balance,
            statement_closing_balance=statement_closing_balance,
            book_opening_balance=book_opening_balance,
            book_closing_balance=book_closing_balance,
            reconciled_balance=book_closing_balance
        )
        
        self.db.add(reconciliation)
        await self.db.commit()
        await self.db.refresh(reconciliation)
        
        logger.info(f"Created bank reconciliation {recon_number}")
        
        return reconciliation
    
    async def perform_bank_reconciliation(
        self,
        reconciliation_id: int,
        outstanding_deposits: float = 0.0,
        outstanding_checks: float = 0.0,
        bank_charges: float = 0.0,
        bank_interest: float = 0.0,
        other_adjustments: float = 0.0,
        reconciler_id: Optional[int] = None
    ):
        """Perform bank reconciliation"""
        from src.models.accounting import BankReconciliation
        
        result = await self.db.execute(
            select(BankReconciliation).where(BankReconciliation.id == reconciliation_id)
        )
        reconciliation = result.scalar_one_or_none()
        
        if not reconciliation:
            raise ValueError(f"Bank reconciliation {reconciliation_id} not found")
        
        # Update adjustments
        reconciliation.outstanding_deposits = outstanding_deposits
        reconciliation.outstanding_checks = outstanding_checks
        reconciliation.bank_charges = bank_charges
        reconciliation.bank_interest = bank_interest
        reconciliation.other_adjustments = other_adjustments
        
        # Calculate reconciled balance
        # Book balance + Outstanding deposits - Outstanding checks - Bank charges + Bank interest + Other adjustments
        reconciliation.reconciled_balance = (
            reconciliation.book_closing_balance
            + outstanding_deposits
            - outstanding_checks
            - bank_charges
            + bank_interest
            + other_adjustments
        )
        
        # Calculate difference
        reconciliation.difference = abs(reconciliation.reconciled_balance - reconciliation.statement_closing_balance)
        
        # Mark as reconciled if difference is negligible (less than ₹1)
        reconciliation.is_reconciled = reconciliation.difference < 1.0
        reconciliation.reconciled_by = reconciler_id
        
        await self.db.commit()
        await self.db.refresh(reconciliation)
        
        logger.info(f"Bank reconciliation {reconciliation.reconciliation_number}: Difference ₹{reconciliation.difference}")
        
        return reconciliation
    
    async def get_unreconciled_items(
        self,
        bank_account_id: int,
        period_from: date,
        period_to: date
    ) -> Dict:
        """Get unreconciled bank transactions"""
        from src.models.accounting import GeneralLedger
        
        # Get all ledger entries for bank account in period
        result = await self.db.execute(
            select(GeneralLedger).where(
                and_(
                    GeneralLedger.account_id == bank_account_id,
                    GeneralLedger.transaction_date >= period_from,
                    GeneralLedger.transaction_date <= period_to
                )
            ).order_by(GeneralLedger.transaction_date)
        )
        entries = result.scalars().all()
        
        # Categorize
        deposits = []
        withdrawals = []
        
        for entry in entries:
            if entry.debit_amount > 0:
                deposits.append({
                    'date': entry.transaction_date,
                    'description': entry.description,
                    'amount': entry.debit_amount,
                    'balance': entry.balance_after
                })
            elif entry.credit_amount > 0:
                withdrawals.append({
                    'date': entry.transaction_date,
                    'description': entry.description,
                    'amount': entry.credit_amount,
                    'balance': entry.balance_after
                })
        
        return {
            'deposits': deposits,
            'withdrawals': withdrawals,
            'total_deposits': sum(d['amount'] for d in deposits),
            'total_withdrawals': sum(w['amount'] for w in withdrawals)
        }
