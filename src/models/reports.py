"""Reporting and Dashboard Models for EMIS"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Float, Boolean, Enum, Text, JSON
from sqlalchemy.orm import relationship
import enum
from src.database import Base


class ReportType(str, enum.Enum):
    """Enumeration for report types"""
    QUARTERLY_FINANCIAL = "quarterly_financial"
    ANNUAL_FINANCIAL = "annual_financial"
    INCOME_STATEMENT = "income_statement"
    BALANCE_SHEET = "balance_sheet"
    CASH_FLOW = "cash_flow"
    STUDENT_ENROLLMENT = "student_enrollment"
    FEE_COLLECTION = "fee_collection"
    EXPENSE_ANALYSIS = "expense_analysis"
    BUDGET_VARIANCE = "budget_variance"
    DEPARTMENT_PERFORMANCE = "department_performance"
    COMPARATIVE_ANALYSIS = "comparative_analysis"
    CUSTOM = "custom"


class ReportStatus(str, enum.Enum):
    """Enumeration for report status"""
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class QuarterlyReport(Base):
    """Quarterly Report model for financial reporting"""
    __tablename__ = "quarterly_reports"

    id = Column(Integer, primary_key=True, index=True)
    
    # Report identification
    report_number = Column(String(50), unique=True, nullable=False, index=True)
    report_type = Column(Enum(ReportType), nullable=False)
    
    # Period
    financial_year = Column(String(20), nullable=False, index=True)
    quarter = Column(Integer, nullable=False)  # 1, 2, 3, 4
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Financial summary
    total_income = Column(Float, default=0.0, nullable=False)
    total_expenses = Column(Float, default=0.0, nullable=False)
    net_profit_loss = Column(Float, default=0.0, nullable=False)
    
    # Income breakdown
    tuition_fee_income = Column(Float, default=0.0)
    admission_fee_income = Column(Float, default=0.0)
    exam_fee_income = Column(Float, default=0.0)
    library_fee_income = Column(Float, default=0.0)
    other_fee_income = Column(Float, default=0.0)
    miscellaneous_income = Column(Float, default=0.0)
    
    # Expense breakdown
    salary_expenses = Column(Float, default=0.0)
    maintenance_expenses = Column(Float, default=0.0)
    utility_expenses = Column(Float, default=0.0)
    infrastructure_expenses = Column(Float, default=0.0)
    administrative_expenses = Column(Float, default=0.0)
    emergency_expenses = Column(Float, default=0.0)
    other_expenses = Column(Float, default=0.0)
    
    # Additional metrics
    student_count = Column(Integer, default=0)
    employee_count = Column(Integer, default=0)
    average_fee_per_student = Column(Float, default=0.0)
    fee_collection_rate = Column(Float, default=0.0)  # Percentage
    
    # Detailed data (JSON)
    income_details = Column(JSON, nullable=True)  # Detailed breakdown
    expense_details = Column(JSON, nullable=True)  # Detailed breakdown
    category_wise_analysis = Column(JSON, nullable=True)
    
    # Report status
    status = Column(Enum(ReportStatus), default=ReportStatus.GENERATING, nullable=False)
    
    # File paths
    pdf_path = Column(String(500), nullable=True)
    excel_path = Column(String(500), nullable=True)
    
    # Metadata
    generated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    generated_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    generator = relationship("User", foreign_keys=[generated_by])
    
    def __repr__(self):
        return f"<QuarterlyReport(id={self.id}, fy={self.financial_year}, q={self.quarter}, profit={self.net_profit_loss})>"


class ReportTemplate(Base):
    """Report Template model for custom report generation"""
    __tablename__ = "report_templates"

    id = Column(Integer, primary_key=True, index=True)
    
    # Template details
    template_name = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    report_type = Column(Enum(ReportType), nullable=False)
    
    # Configuration
    fields = Column(JSON, nullable=False)  # List of fields to include
    filters = Column(JSON, nullable=True)  # Default filters
    grouping = Column(JSON, nullable=True)  # Grouping configuration
    sorting = Column(JSON, nullable=True)  # Sorting configuration
    
    # Formatting
    chart_types = Column(JSON, nullable=True)  # Chart configurations
    layout_config = Column(JSON, nullable=True)  # Layout settings
    
    # Access control
    is_public = Column(Boolean, default=False, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    
    def __repr__(self):
        return f"<ReportTemplate(id={self.id}, name={self.template_name}, type={self.report_type})>"


class DashboardMetrics(Base):
    """Dashboard Metrics model for storing aggregated metrics"""
    __tablename__ = "dashboard_metrics"

    id = Column(Integer, primary_key=True, index=True)
    
    # Time period
    metric_date = Column(Date, default=date.today, nullable=False, index=True)
    metric_month = Column(Integer, nullable=False)  # 1-12
    metric_year = Column(Integer, nullable=False)
    
    # Financial metrics
    daily_revenue = Column(Float, default=0.0)
    monthly_revenue = Column(Float, default=0.0)
    daily_expenses = Column(Float, default=0.0)
    monthly_expenses = Column(Float, default=0.0)
    daily_profit = Column(Float, default=0.0)
    monthly_profit = Column(Float, default=0.0)
    
    # Student metrics
    total_students = Column(Integer, default=0)
    new_admissions_today = Column(Integer, default=0)
    new_admissions_month = Column(Integer, default=0)
    attendance_percentage = Column(Float, default=0.0)
    
    # Fee collection metrics
    fees_collected_today = Column(Float, default=0.0)
    fees_collected_month = Column(Float, default=0.0)
    fees_pending = Column(Float, default=0.0)
    fee_collection_rate = Column(Float, default=0.0)
    
    # Library metrics
    books_issued_today = Column(Integer, default=0)
    books_returned_today = Column(Integer, default=0)
    overdue_books_count = Column(Integer, default=0)
    fines_collected_today = Column(Float, default=0.0)
    lost_books_count = Column(Integer, default=0)
    
    # HR metrics
    total_employees = Column(Integer, default=0)
    employees_on_leave = Column(Integer, default=0)
    pending_leave_requests = Column(Integer, default=0)
    
    # Exam metrics
    upcoming_exams_count = Column(Integer, default=0)
    pending_results_count = Column(Integer, default=0)
    
    # Detailed breakdowns (JSON)
    revenue_breakdown = Column(JSON, nullable=True)
    expense_breakdown = Column(JSON, nullable=True)
    student_breakdown = Column(JSON, nullable=True)
    
    # Metadata
    last_calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<DashboardMetrics(date={self.metric_date}, revenue={self.daily_revenue}, students={self.total_students})>"


class AnnualFinancialReport(Base):
    """Annual Financial Report model - comprehensive yearly financial statements"""
    __tablename__ = "annual_financial_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Report identification
    report_number = Column(String(50), unique=True, nullable=False, index=True)
    report_type = Column(Enum(ReportType), default=ReportType.ANNUAL_FINANCIAL, nullable=False)
    
    # Period
    financial_year = Column(String(20), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Executive Summary
    total_annual_revenue = Column(Float, default=0.0, nullable=False)
    total_annual_expenses = Column(Float, default=0.0, nullable=False)
    net_annual_profit_loss = Column(Float, default=0.0, nullable=False)
    annual_profit_margin = Column(Float, default=0.0)
    
    # Quarterly breakdown
    q1_income = Column(Float, default=0.0)
    q2_income = Column(Float, default=0.0)
    q3_income = Column(Float, default=0.0)
    q4_income = Column(Float, default=0.0)
    q1_expenses = Column(Float, default=0.0)
    q2_expenses = Column(Float, default=0.0)
    q3_expenses = Column(Float, default=0.0)
    q4_expenses = Column(Float, default=0.0)
    
    # Detailed breakdown (JSON)
    monthly_income_breakdown = Column(JSON, nullable=True)  # 12 months
    monthly_expense_breakdown = Column(JSON, nullable=True)  # 12 months
    income_by_category = Column(JSON, nullable=True)
    expenses_by_category = Column(JSON, nullable=True)
    
    # Salary analysis
    total_salary_expenses = Column(Float, default=0.0)
    faculty_salary_total = Column(Float, default=0.0)
    staff_salary_total = Column(Float, default=0.0)
    department_wise_salary = Column(JSON, nullable=True)
    designation_wise_salary = Column(JSON, nullable=True)
    
    # Department performance
    department_income = Column(JSON, nullable=True)
    department_expenses = Column(JSON, nullable=True)
    department_profitability = Column(JSON, nullable=True)
    
    # Student metrics
    year_start_enrollment = Column(Integer, default=0)
    year_end_enrollment = Column(Integer, default=0)
    total_admissions = Column(Integer, default=0)
    total_graduations = Column(Integer, default=0)
    program_enrollment = Column(JSON, nullable=True)
    annual_fees_collected = Column(Float, default=0.0)
    annual_fees_outstanding = Column(Float, default=0.0)
    collection_rate = Column(Float, default=0.0)
    
    # Faculty metrics
    total_faculty_count = Column(Integer, default=0)
    department_faculty_count = Column(JSON, nullable=True)
    faculty_student_ratio = Column(Float, default=0.0)
    
    # Balance sheet (Year End)
    total_assets = Column(Float, default=0.0)
    current_assets = Column(Float, default=0.0)
    fixed_assets = Column(Float, default=0.0)
    total_liabilities = Column(Float, default=0.0)
    current_liabilities = Column(Float, default=0.0)
    long_term_liabilities = Column(Float, default=0.0)
    total_equity = Column(Float, default=0.0)
    
    # Cash flow
    operating_cash_flow = Column(Float, default=0.0)
    investing_cash_flow = Column(Float, default=0.0)
    financing_cash_flow = Column(Float, default=0.0)
    net_cash_flow = Column(Float, default=0.0)
    
    # Financial ratios
    current_ratio = Column(Float, default=0.0)
    quick_ratio = Column(Float, default=0.0)
    debt_to_equity = Column(Float, default=0.0)
    return_on_assets = Column(Float, default=0.0)
    operating_margin = Column(Float, default=0.0)
    
    # Comparative analysis
    previous_year_comparison = Column(JSON, nullable=True)
    year_over_year_growth = Column(JSON, nullable=True)
    
    # Charts and trends
    income_trend = Column(JSON, nullable=True)
    expense_trend = Column(JSON, nullable=True)
    enrollment_trend = Column(JSON, nullable=True)
    
    # Metadata
    status = Column(Enum(ReportStatus), default=ReportStatus.GENERATING, nullable=False)
    pdf_path = Column(String(500), nullable=True)
    excel_path = Column(String(500), nullable=True)
    
    generated_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    generated_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    generator = relationship("User", foreign_keys=[generated_by])
    approver = relationship("User", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<AnnualFinancialReport(id={self.id}, fy={self.financial_year}, profit={self.net_annual_profit_loss})>"
    
    def calculate_ratios(self):
        """Calculate financial ratios"""
        # Current ratio = Current Assets / Current Liabilities
        if self.current_liabilities > 0:
            self.current_ratio = round(self.current_assets / self.current_liabilities, 2)
        
        # Quick ratio = (Current Assets - Inventory) / Current Liabilities
        # Assuming inventory is negligible for educational institutions
        self.quick_ratio = self.current_ratio
        
        # Debt to Equity
        if self.total_equity > 0:
            self.debt_to_equity = round(self.total_liabilities / self.total_equity, 2)
        
        # Return on Assets
        if self.total_assets > 0:
            self.return_on_assets = round((self.net_annual_profit_loss / self.total_assets) * 100, 2)
        
        # Operating Margin
        if self.total_annual_revenue > 0:
            self.operating_margin = round((self.net_annual_profit_loss / self.total_annual_revenue) * 100, 2)
    
    def get_quarter_data(self, quarter: int) -> dict:
        """Get data for specific quarter"""
        quarters = {
            1: {"income": self.q1_income, "expenses": self.q1_expenses},
            2: {"income": self.q2_income, "expenses": self.q2_expenses},
            3: {"income": self.q3_income, "expenses": self.q3_expenses},
            4: {"income": self.q4_income, "expenses": self.q4_expenses}
        }
        return quarters.get(quarter, {})

