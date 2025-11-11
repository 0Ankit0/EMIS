"""Annual Financial Report Service"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract
from typing import List, Optional, Dict
from datetime import date, datetime
from decimal import Decimal

from src.models.reports import AnnualFinancialReport, QuarterlyReport, ReportStatus, ReportType
from src.models.accounting import JournalEntry, Expense, Income
from src.models.billing import Bill, BillStatus
from src.services.accounting_service import AccountingService


class AnnualReportService:
    """Service for generating comprehensive annual financial reports"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.accounting_service = AccountingService(db)
    
    async def generate_annual_report(
        self,
        financial_year: str,
        generated_by: Optional[int] = None
    ) -> AnnualFinancialReport:
        """Generate comprehensive annual financial report"""
        
        # Parse financial year (e.g., "2024-2025")
        start_year, end_year = financial_year.split("-")
        start_date = date(int(start_year), 4, 1)  # April 1
        end_date = date(int(end_year), 3, 31)  # March 31
        
        # Generate report number
        report_number = f"AR{start_year}{end_year}"
        
        report = AnnualFinancialReport(
            report_number=report_number,
            financial_year=financial_year,
            start_date=start_date,
            end_date=end_date,
            generated_by=generated_by,
            status=ReportStatus.GENERATING
        )
        
        # Calculate all metrics
        await self._calculate_annual_income(report, start_date, end_date)
        await self._calculate_annual_expenses(report, start_date, end_date)
        await self._calculate_quarterly_breakdown(report, financial_year)
        await self._calculate_monthly_breakdown(report, start_date, end_date)
        await self._calculate_salary_analysis(report, start_date, end_date)
        await self._calculate_department_performance(report, start_date, end_date)
        await self._calculate_student_metrics(report, start_date, end_date)
        await self._calculate_faculty_metrics(report)
        await self._calculate_balance_sheet(report, end_date)
        await self._calculate_cash_flow(report, start_date, end_date)
        await self._calculate_comparative_analysis(report, start_year)
        
        # Calculate derived metrics
        report.net_annual_profit_loss = report.total_annual_revenue - report.total_annual_expenses
        if report.total_annual_revenue > 0:
            report.annual_profit_margin = (report.net_annual_profit_loss / report.total_annual_revenue) * 100
        
        # Calculate financial ratios
        report.calculate_ratios()
        
        report.status = ReportStatus.COMPLETED
        report.generated_at = datetime.utcnow()
        
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        
        return report
    
    async def _calculate_annual_income(self, report: AnnualFinancialReport, start_date: date, end_date: date):
        """Calculate total annual income"""
        stmt = select(func.sum(Income.total_amount)).where(
            and_(
                Income.income_date >= start_date,
                Income.income_date <= end_date
            )
        )
        result = await self.db.execute(stmt)
        total = result.scalar_one_or_none() or 0.0
        report.total_annual_revenue = float(total)
        
        # Income by category
        stmt = select(
            Income.category_id,
            func.sum(Income.total_amount)
        ).where(
            and_(
                Income.income_date >= start_date,
                Income.income_date <= end_date
            )
        ).group_by(Income.category_id)
        
        result = await self.db.execute(stmt)
        income_by_cat = {str(cat_id): float(amount) for cat_id, amount in result.all() if cat_id}
        report.income_by_category = income_by_cat
    
    async def _calculate_annual_expenses(self, report: AnnualFinancialReport, start_date: date, end_date: date):
        """Calculate total annual expenses"""
        stmt = select(func.sum(Expense.total_amount)).where(
            and_(
                Expense.expense_date >= start_date,
                Expense.expense_date <= end_date
            )
        )
        result = await self.db.execute(stmt)
        total = result.scalar_one_or_none() or 0.0
        report.total_annual_expenses = float(total)
        
        # Expenses by category
        stmt = select(
            Expense.category_id,
            func.sum(Expense.total_amount)
        ).where(
            and_(
                Expense.expense_date >= start_date,
                Expense.expense_date <= end_date
            )
        ).group_by(Expense.category_id)
        
        result = await self.db.execute(stmt)
        expenses_by_cat = {str(cat_id): float(amount) for cat_id, amount in result.all() if cat_id}
        report.expenses_by_category = expenses_by_cat
    
    async def _calculate_quarterly_breakdown(self, report: AnnualFinancialReport, financial_year: str):
        """Get quarterly breakdown from quarterly reports"""
        for quarter in range(1, 5):
            stmt = select(QuarterlyReport).where(
                and_(
                    QuarterlyReport.financial_year == financial_year,
                    QuarterlyReport.quarter == quarter
                )
            )
            result = await self.db.execute(stmt)
            q_report = result.scalar_one_or_none()
            
            if q_report:
                if quarter == 1:
                    report.q1_income = q_report.total_income
                    report.q1_expenses = q_report.total_expenses
                elif quarter == 2:
                    report.q2_income = q_report.total_income
                    report.q2_expenses = q_report.total_expenses
                elif quarter == 3:
                    report.q3_income = q_report.total_income
                    report.q3_expenses = q_report.total_expenses
                elif quarter == 4:
                    report.q4_income = q_report.total_income
                    report.q4_expenses = q_report.total_expenses
    
    async def _calculate_monthly_breakdown(self, report: AnnualFinancialReport, start_date: date, end_date: date):
        """Calculate month-wise income and expense breakdown"""
        monthly_income = {}
        monthly_expenses = {}
        
        for month in range(1, 13):
            # Determine year (FY starts in April)
            if month >= 4:
                year = start_date.year
            else:
                year = end_date.year
            
            # Income for month
            stmt = select(func.sum(Income.total_amount)).where(
                and_(
                    extract('month', Income.income_date) == month,
                    extract('year', Income.income_date) == year
                )
            )
            result = await self.db.execute(stmt)
            income = result.scalar_one_or_none() or 0.0
            monthly_income[str(month)] = float(income)
            
            # Expenses for month
            stmt = select(func.sum(Expense.total_amount)).where(
                and_(
                    extract('month', Expense.expense_date) == month,
                    extract('year', Expense.expense_date) == year
                )
            )
            result = await self.db.execute(stmt)
            expense = result.scalar_one_or_none() or 0.0
            monthly_expenses[str(month)] = float(expense)
        
        report.monthly_income_breakdown = monthly_income
        report.monthly_expense_breakdown = monthly_expenses
    
    async def _calculate_salary_analysis(self, report: AnnualFinancialReport, start_date: date, end_date: date):
        """Calculate salary-related expenses"""
        # Get salary expenses (assuming category codes like 'SAL-*')
        stmt = select(func.sum(Expense.total_amount)).where(
            and_(
                Expense.expense_date >= start_date,
                Expense.expense_date <= end_date,
                Expense.title.like('%salary%')
            )
        )
        result = await self.db.execute(stmt)
        total_salary = result.scalar_one_or_none() or 0.0
        report.total_salary_expenses = float(total_salary)
        
        # Faculty vs Staff breakdown (placeholder - would need more detailed categorization)
        report.faculty_salary_total = float(total_salary * 0.7)  # Assuming 70% faculty
        report.staff_salary_total = float(total_salary * 0.3)  # Assuming 30% staff
    
    async def _calculate_department_performance(self, report: AnnualFinancialReport, start_date: date, end_date: date):
        """Calculate department-wise performance"""
        # This would require department tracking in bills and expenses
        # Placeholder implementation
        report.department_income = {}
        report.department_expenses = {}
        report.department_profitability = {}
    
    async def _calculate_student_metrics(self, report: AnnualFinancialReport, start_date: date, end_date: date):
        """Calculate student-related metrics"""
        # Total fees collected
        stmt = select(func.sum(Bill.amount_paid)).where(
            and_(
                Bill.bill_date >= start_date,
                Bill.bill_date <= end_date,
                Bill.status != BillStatus.CANCELLED
            )
        )
        result = await self.db.execute(stmt)
        fees_collected = result.scalar_one_or_none() or 0.0
        report.annual_fees_collected = float(fees_collected)
        
        # Outstanding fees
        stmt = select(func.sum(Bill.amount_due)).where(
            and_(
                Bill.bill_date >= start_date,
                Bill.bill_date <= end_date,
                Bill.status.in_([BillStatus.GENERATED, BillStatus.PARTIALLY_PAID, BillStatus.OVERDUE])
            )
        )
        result = await self.db.execute(stmt)
        fees_outstanding = result.scalar_one_or_none() or 0.0
        report.annual_fees_outstanding = float(fees_outstanding)
        
        # Collection rate
        total_billed = fees_collected + fees_outstanding
        if total_billed > 0:
            report.collection_rate = (fees_collected / total_billed) * 100
    
    async def _calculate_faculty_metrics(self, report: AnnualFinancialReport):
        """Calculate faculty-related metrics"""
        # This would query the teacher hierarchy and employee tables
        # Placeholder values
        report.total_faculty_count = 0
        report.department_faculty_count = {}
        report.faculty_student_ratio = 0.0
    
    async def _calculate_balance_sheet(self, report: AnnualFinancialReport, end_date: date):
        """Calculate balance sheet items"""
        # This would aggregate from accounting system
        # Placeholder implementation
        report.total_assets = 0.0
        report.current_assets = 0.0
        report.fixed_assets = 0.0
        report.total_liabilities = 0.0
        report.current_liabilities = 0.0
        report.long_term_liabilities = 0.0
        report.total_equity = report.total_assets - report.total_liabilities
    
    async def _calculate_cash_flow(self, report: AnnualFinancialReport, start_date: date, end_date: date):
        """Calculate cash flow statement"""
        # Operating cash flow ≈ Net Income
        report.operating_cash_flow = report.net_annual_profit_loss
        report.investing_cash_flow = 0.0
        report.financing_cash_flow = 0.0
        report.net_cash_flow = report.operating_cash_flow
    
    async def _calculate_comparative_analysis(self, report: AnnualFinancialReport, start_year: str):
        """Calculate year-over-year comparison"""
        previous_fy = f"{int(start_year) - 1}-{start_year}"
        
        stmt = select(AnnualFinancialReport).where(
            AnnualFinancialReport.financial_year == previous_fy
        )
        result = await self.db.execute(stmt)
        prev_report = result.scalar_one_or_none()
        
        if prev_report:
            report.previous_year_comparison = {
                "revenue": float(prev_report.total_annual_revenue),
                "expenses": float(prev_report.total_annual_expenses),
                "profit": float(prev_report.net_annual_profit_loss)
            }
            
            # Growth rates
            revenue_growth = ((report.total_annual_revenue - prev_report.total_annual_revenue) / 
                            prev_report.total_annual_revenue * 100) if prev_report.total_annual_revenue > 0 else 0
            
            report.year_over_year_growth = {
                "revenue_growth": round(revenue_growth, 2),
                "expense_growth": 0,  # Calculate similarly
                "profit_growth": 0
            }
    
    async def get_report_by_id(self, report_id: int) -> Optional[AnnualFinancialReport]:
        """Get annual report by ID"""
        stmt = select(AnnualFinancialReport).where(AnnualFinancialReport.id == report_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all_reports(self, financial_year: Optional[str] = None) -> List[AnnualFinancialReport]:
        """Get all annual reports, optionally filtered by FY"""
        stmt = select(AnnualFinancialReport)
        
        if financial_year:
            stmt = stmt.where(AnnualFinancialReport.financial_year == financial_year)
        
        stmt = stmt.order_by(AnnualFinancialReport.financial_year.desc())
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    async def approve_report(self, report_id: int, approved_by: int) -> AnnualFinancialReport:
        """Approve an annual report"""
        report = await self.get_report_by_id(report_id)
        if not report:
            raise ValueError(f"Report {report_id} not found")
        
        report.approved_by = approved_by
        report.approved_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(report)
        
        return report
