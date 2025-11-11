"""Dashboard Service for EMIS"""
from datetime import datetime, date, timedelta
from typing import Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from src.models.reports import DashboardMetrics
from src.models.student import Student
from src.models.employee import Employee
from src.models.billing import Bill
from src.models.accounting import Income, Expense
from src.lib.logging import get_logger

logger = get_logger(__name__)


class DashboardService:
    """Service for calculating dashboard metrics"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def calculate_today_metrics(self) -> DashboardMetrics:
        """Calculate and store metrics for today"""
        
        today = date.today()
        
        # Check if metrics already exist for today
        result = await self.db.execute(
            select(DashboardMetrics).where(DashboardMetrics.metric_date == today)
        )
        metrics = result.scalar_one_or_none()
        
        if not metrics:
            metrics = DashboardMetrics(
                metric_date=today,
                metric_month=today.month,
                metric_year=today.year
            )
            self.db.add(metrics)
        
        # Financial metrics - Today
        today_income_result = await self.db.execute(
            select(func.sum(Income.total_amount)).where(
                Income.income_date == today
            )
        )
        metrics.daily_revenue = float(today_income_result.scalar() or 0)
        
        today_expense_result = await self.db.execute(
            select(func.sum(Expense.total_amount)).where(
                Expense.expense_date == today
            )
        )
        metrics.daily_expenses = float(today_expense_result.scalar() or 0)
        
        metrics.daily_profit = metrics.daily_revenue - metrics.daily_expenses
        
        # Financial metrics - This month
        month_start = today.replace(day=1)
        
        month_income_result = await self.db.execute(
            select(func.sum(Income.total_amount)).where(
                and_(
                    Income.income_date >= month_start,
                    Income.income_date <= today
                )
            )
        )
        metrics.monthly_revenue = float(month_income_result.scalar() or 0)
        
        month_expense_result = await self.db.execute(
            select(func.sum(Expense.total_amount)).where(
                and_(
                    Expense.expense_date >= month_start,
                    Expense.expense_date <= today
                )
            )
        )
        metrics.monthly_expenses = float(month_expense_result.scalar() or 0)
        
        metrics.monthly_profit = metrics.monthly_revenue - metrics.monthly_expenses
        
        # Student metrics
        total_students_result = await self.db.execute(
            select(func.count(Student.id))
        )
        metrics.total_students = total_students_result.scalar() or 0
        
        # New admissions today
        new_today_result = await self.db.execute(
            select(func.count(Student.id)).where(
                func.date(Student.created_at) == today
            )
        )
        metrics.new_admissions_today = new_today_result.scalar() or 0
        
        # New admissions this month
        new_month_result = await self.db.execute(
            select(func.count(Student.id)).where(
                and_(
                    func.date(Student.created_at) >= month_start,
                    func.date(Student.created_at) <= today
                )
            )
        )
        metrics.new_admissions_month = new_month_result.scalar() or 0
        
        # Fee collection metrics
        fees_today_result = await self.db.execute(
            select(func.sum(Bill.amount_paid)).where(
                func.date(Bill.payment_date) == today
            )
        )
        metrics.fees_collected_today = float(fees_today_result.scalar() or 0)
        
        fees_month_result = await self.db.execute(
            select(func.sum(Bill.amount_paid)).where(
                and_(
                    func.date(Bill.payment_date) >= month_start,
                    func.date(Bill.payment_date) <= today
                )
            )
        )
        metrics.fees_collected_month = float(fees_month_result.scalar() or 0)
        
        # Pending fees
        pending_result = await self.db.execute(
            select(func.sum(Bill.amount_due)).where(Bill.amount_due > 0)
        )
        metrics.fees_pending = float(pending_result.scalar() or 0)
        
        # Fee collection rate
        total_billed_result = await self.db.execute(
            select(
                func.sum(Bill.total_amount).label('total'),
                func.sum(Bill.amount_paid).label('paid')
            )
        )
        billed_row = total_billed_result.first()
        total_billed = float(billed_row.total or 0)
        total_paid = float(billed_row.paid or 0)
        metrics.fee_collection_rate = (total_paid / total_billed * 100) if total_billed > 0 else 0.0
        
        # Library metrics (would need library models)
        # Placeholder values for now
        metrics.books_issued_today = 0
        metrics.books_returned_today = 0
        metrics.overdue_books_count = 0
        metrics.fines_collected_today = 0.0
        metrics.lost_books_count = 0
        
        # HR metrics
        total_employees_result = await self.db.execute(
            select(func.count(Employee.id))
        )
        metrics.total_employees = total_employees_result.scalar() or 0
        
        metrics.employees_on_leave = 0  # Would need leave records
        metrics.pending_leave_requests = 0
        
        # Exam metrics (would need exam models)
        metrics.upcoming_exams_count = 0
        metrics.pending_results_count = 0
        
        # Detailed breakdowns
        # Revenue breakdown by source
        revenue_breakdown = {}
        income_by_category = await self.db.execute(
            select(
                Income.title,
                func.sum(Income.total_amount)
            ).where(
                and_(
                    Income.income_date >= month_start,
                    Income.income_date <= today
                )
            ).group_by(Income.title)
        )
        for title, amount in income_by_category:
            revenue_breakdown[title] = float(amount)
        
        metrics.revenue_breakdown = revenue_breakdown
        
        # Expense breakdown by category
        expense_breakdown = {}
        expense_by_category = await self.db.execute(
            select(
                Expense.title,
                func.sum(Expense.total_amount)
            ).where(
                and_(
                    Expense.expense_date >= month_start,
                    Expense.expense_date <= today
                )
            ).group_by(Expense.title)
        )
        for title, amount in expense_by_category:
            expense_breakdown[title] = float(amount)
        
        metrics.expense_breakdown = expense_breakdown
        
        metrics.last_calculated_at = datetime.utcnow()
        
        await self.db.commit()
        await self.db.refresh(metrics)
        
        logger.info(f"Updated dashboard metrics for {today}: Revenue ₹{metrics.daily_revenue}, Students {metrics.total_students}")
        
        return metrics
    
    async def get_latest_metrics(self) -> Optional[DashboardMetrics]:
        """Get latest calculated metrics"""
        result = await self.db.execute(
            select(DashboardMetrics).order_by(
                DashboardMetrics.metric_date.desc()
            ).limit(1)
        )
        return result.scalar_one_or_none()
    
    async def get_metrics_for_date(self, metric_date: date) -> Optional[DashboardMetrics]:
        """Get metrics for a specific date"""
        result = await self.db.execute(
            select(DashboardMetrics).where(
                DashboardMetrics.metric_date == metric_date
            )
        )
        return result.scalar_one_or_none()
    
    async def get_financial_summary(self) -> Dict:
        """Get comprehensive financial summary"""
        
        today = date.today()
        month_start = today.replace(day=1)
        
        # Get current month data
        month_income = await self.db.execute(
            select(func.sum(Income.total_amount)).where(
                and_(
                    Income.income_date >= month_start,
                    Income.income_date <= today
                )
            )
        )
        
        month_expense = await self.db.execute(
            select(func.sum(Expense.total_amount)).where(
                and_(
                    Expense.expense_date >= month_start,
                    Expense.expense_date <= today
                )
            )
        )
        
        total_income = float(month_income.scalar() or 0)
        total_expense = float(month_expense.scalar() or 0)
        
        return {
            "current_month": {
                "income": total_income,
                "expense": total_expense,
                "profit": total_income - total_expense
            },
            "summary": {
                "total_income": total_income,
                "total_expense": total_expense,
                "net_profit": total_income - total_expense,
                "profit_margin": ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0
            }
        }
    
    async def get_student_summary(self) -> Dict:
        """Get student enrollment summary"""
        
        total = await self.db.execute(select(func.count(Student.id)))
        
        return {
            "total_students": total.scalar() or 0,
            "active_students": total.scalar() or 0,  # Would need enrollment status
        }
    
    async def get_library_summary(self) -> Dict:
        """Get library activity summary"""
        
        # Placeholder - would need actual library models
        return {
            "total_books": 0,
            "books_issued": 0,
            "books_available": 0,
            "overdue_books": 0,
            "total_fines": 0.0
        }
