"""Quarterly Report Service for EMIS"""
from datetime import datetime, date
from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from src.models.reports import QuarterlyReport, ReportType, ReportStatus
from src.models.accounting import Expense, Income
from src.models.billing import Bill, BillStatus
from src.services.accounting_service import AccountingService
from src.lib.logging import get_logger

logger = get_logger(__name__)


class QuarterlyReportService:
    """Service for generating quarterly financial reports"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.accounting_service = AccountingService(db)
    
    def get_quarter_dates(self, financial_year: str, quarter: int) -> tuple[date, date]:
        """Get start and end dates for a quarter"""
        # Financial year format: "2024-2025"
        start_year = int(financial_year.split('-')[0])
        
        quarter_months = {
            1: (4, 6),   # Apr-Jun
            2: (7, 9),   # Jul-Sep
            3: (10, 12), # Oct-Dec
            4: (1, 3),   # Jan-Mar
        }
        
        start_month, end_month = quarter_months[quarter]
        
        if quarter == 4:  # Jan-Mar of next year
            year = start_year + 1
        else:
            year = start_year
        
        start_date = date(year, start_month, 1)
        
        # Get last day of end month
        if end_month == 12:
            end_date = date(year, 12, 31)
        elif end_month in [4, 6, 9]:
            end_date = date(year, end_month, 30)
        elif end_month == 3:
            end_date = date(year, 3, 31)
        else:
            end_date = date(year, end_month, 31)
        
        return start_date, end_date
    
    async def generate_report_number(self, financial_year: str, quarter: int) -> str:
        """Generate unique report number"""
        fy_short = financial_year.replace('-', '')
        return f"QR{fy_short}Q{quarter}"
    
    async def generate_quarterly_report(
        self,
        financial_year: str,
        quarter: int,
        generated_by: Optional[int] = None
    ) -> QuarterlyReport:
        """Generate comprehensive quarterly report"""
        
        report_number = await self.generate_report_number(financial_year, quarter)
        start_date, end_date = self.get_quarter_dates(financial_year, quarter)
        
        # Check if report already exists
        result = await self.db.execute(
            select(QuarterlyReport).where(
                and_(
                    QuarterlyReport.financial_year == financial_year,
                    QuarterlyReport.quarter == quarter
                )
            )
        )
        existing_report = result.scalar_one_or_none()
        
        if existing_report:
            logger.info(f"Updating existing report {report_number}")
            report = existing_report
            report.status = ReportStatus.GENERATING
        else:
            report = QuarterlyReport(
                report_number=report_number,
                report_type=ReportType.QUARTERLY_FINANCIAL,
                financial_year=financial_year,
                quarter=quarter,
                start_date=start_date,
                end_date=end_date,
                status=ReportStatus.GENERATING
            )
            self.db.add(report)
        
        try:
            # Get all income for the quarter
            incomes = await self.accounting_service.get_income_by_quarter(
                financial_year, quarter
            )
            
            # Get all expenses for the quarter
            expenses = await self.accounting_service.get_expenses_by_quarter(
                financial_year, quarter
            )
            
            # Calculate income breakdown
            tuition_fee_income = 0.0
            admission_fee_income = 0.0
            exam_fee_income = 0.0
            library_fee_income = 0.0
            other_fee_income = 0.0
            miscellaneous_income = 0.0
            
            income_details = {}
            
            for income in incomes:
                # Categorize income
                if 'tuition' in income.title.lower():
                    tuition_fee_income += income.total_amount
                elif 'admission' in income.title.lower():
                    admission_fee_income += income.total_amount
                elif 'exam' in income.title.lower():
                    exam_fee_income += income.total_amount
                elif 'library' in income.title.lower():
                    library_fee_income += income.total_amount
                else:
                    miscellaneous_income += income.total_amount
                
                # Store details
                category_name = income.title
                if category_name in income_details:
                    income_details[category_name] += income.total_amount
                else:
                    income_details[category_name] = income.total_amount
            
            total_income = sum([
                tuition_fee_income, admission_fee_income, exam_fee_income,
                library_fee_income, other_fee_income, miscellaneous_income
            ])
            
            # Calculate expense breakdown
            salary_expenses = 0.0
            maintenance_expenses = 0.0
            utility_expenses = 0.0
            infrastructure_expenses = 0.0
            administrative_expenses = 0.0
            emergency_expenses = 0.0
            other_expenses = 0.0
            
            expense_details = {}
            
            for expense in expenses:
                # Categorize expenses
                title_lower = expense.title.lower()
                if 'salary' in title_lower or 'wage' in title_lower:
                    salary_expenses += expense.total_amount
                elif 'maintenance' in title_lower:
                    maintenance_expenses += expense.total_amount
                elif 'electricity' in title_lower or 'water' in title_lower or 'utility' in title_lower:
                    utility_expenses += expense.total_amount
                elif 'infrastructure' in title_lower or 'building' in title_lower:
                    infrastructure_expenses += expense.total_amount
                elif 'administrative' in title_lower or 'office' in title_lower:
                    administrative_expenses += expense.total_amount
                elif 'emergency' in title_lower:
                    emergency_expenses += expense.total_amount
                else:
                    other_expenses += expense.total_amount
                
                # Store details
                category_name = expense.title
                if category_name in expense_details:
                    expense_details[category_name] += expense.total_amount
                else:
                    expense_details[category_name] = expense.total_amount
            
            total_expenses = sum([
                salary_expenses, maintenance_expenses, utility_expenses,
                infrastructure_expenses, administrative_expenses,
                emergency_expenses, other_expenses
            ])
            
            # Calculate net profit/loss
            net_profit_loss = total_income - total_expenses
            
            # Get student and employee counts
            from src.models.student import Student
            from src.models.employee import Employee
            
            student_count_result = await self.db.execute(
                select(func.count(Student.id))
            )
            student_count = student_count_result.scalar() or 0
            
            employee_count_result = await self.db.execute(
                select(func.count(Employee.id))
            )
            employee_count = employee_count_result.scalar() or 0
            
            # Calculate average fee per student
            avg_fee_per_student = total_income / student_count if student_count > 0 else 0.0
            
            # Calculate fee collection rate
            bills_result = await self.db.execute(
                select(
                    func.sum(Bill.total_amount).label('total_bills'),
                    func.sum(Bill.amount_paid).label('total_paid')
                ).where(
                    and_(
                        Bill.bill_date >= start_date,
                        Bill.bill_date <= end_date
                    )
                )
            )
            bills_row = bills_result.first()
            total_bills = float(bills_row.total_bills or 0)
            total_paid = float(bills_row.total_paid or 0)
            fee_collection_rate = (total_paid / total_bills * 100) if total_bills > 0 else 0.0
            
            # Update report
            report.total_income = total_income
            report.total_expenses = total_expenses
            report.net_profit_loss = net_profit_loss
            
            report.tuition_fee_income = tuition_fee_income
            report.admission_fee_income = admission_fee_income
            report.exam_fee_income = exam_fee_income
            report.library_fee_income = library_fee_income
            report.other_fee_income = other_fee_income
            report.miscellaneous_income = miscellaneous_income
            
            report.salary_expenses = salary_expenses
            report.maintenance_expenses = maintenance_expenses
            report.utility_expenses = utility_expenses
            report.infrastructure_expenses = infrastructure_expenses
            report.administrative_expenses = administrative_expenses
            report.emergency_expenses = emergency_expenses
            report.other_expenses = other_expenses
            
            report.student_count = student_count
            report.employee_count = employee_count
            report.average_fee_per_student = avg_fee_per_student
            report.fee_collection_rate = fee_collection_rate
            
            report.income_details = income_details
            report.expense_details = expense_details
            
            report.status = ReportStatus.COMPLETED
            report.generated_by = generated_by
            report.generated_at = datetime.utcnow()
            
            await self.db.commit()
            await self.db.refresh(report)
            
            logger.info(f"Generated quarterly report {report_number}: Income ₹{total_income}, Expenses ₹{total_expenses}, Profit ₹{net_profit_loss}")
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate quarterly report: {str(e)}")
            report.status = ReportStatus.FAILED
            await self.db.commit()
            raise
    
    async def get_report_by_id(self, report_id: int) -> Optional[QuarterlyReport]:
        """Get report by ID"""
        result = await self.db.execute(
            select(QuarterlyReport).where(QuarterlyReport.id == report_id)
        )
        return result.scalar_one_or_none()
    
    async def get_report_by_period(
        self,
        financial_year: str,
        quarter: int
    ) -> Optional[QuarterlyReport]:
        """Get report for a specific period"""
        result = await self.db.execute(
            select(QuarterlyReport).where(
                and_(
                    QuarterlyReport.financial_year == financial_year,
                    QuarterlyReport.quarter == quarter
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all_reports(
        self,
        financial_year: Optional[str] = None
    ) -> List[QuarterlyReport]:
        """Get all reports, optionally filtered by financial year"""
        query = select(QuarterlyReport)
        
        if financial_year:
            query = query.where(QuarterlyReport.financial_year == financial_year)
        
        query = query.order_by(
            QuarterlyReport.financial_year.desc(),
            QuarterlyReport.quarter.desc()
        )
        
        result = await self.db.execute(query)
        return result.scalars().all()
