# Enhanced Financial Reporting Specification

## Overview

This specification extends the financial reporting system to provide comprehensive quarterly and annual reports with proper hierarchical organization for teachers/faculty and detailed financial breakdowns.

## 1. Teacher Hierarchy Enhancement

### 1.1 Teacher Hierarchy Levels

```
Institution Level
├── Department Head (HOD)
│   ├── Senior Faculty
│   │   ├── Assistant Professors
│   │   ├── Lecturers
│   │   └── Teaching Assistants
│   └── Junior Faculty
├── Program Coordinator
├── Subject Coordinators
└── Regular Faculty
```

### 1.2 Teacher Roles & Permissions

**Department Head (HOD):**
- View department-wise financial reports
- View faculty salary breakdowns
- Approve department expenses
- Access student enrollment reports
- View performance analytics

**Program Coordinator:**
- View program-specific reports
- Student performance tracking
- Course-wise analytics

**Subject Coordinator:**
- View subject-wise reports
- Student performance in subject
- Resource allocation

**Senior Faculty:**
- View own salary details
- Submit expense claims
- Access student reports for assigned classes

**Regular Faculty:**
- View own salary details
- Submit expense claims
- Basic student reports

### 1.3 Required Fields

```python
class TeacherHierarchy:
    teacher_id: int
    designation: str  # HOD, Professor, Associate Prof, Assistant Prof, Lecturer, TA
    department_id: int
    reports_to: Optional[int]  # Supervisor's teacher_id
    hierarchy_level: int  # 1=HOD, 2=Senior, 3=Regular, 4=Junior
    is_department_head: bool
    is_program_coordinator: bool
    subject_coordinator_for: List[int]  # subject_ids
    permissions: List[str]
```

## 2. Enhanced Quarterly Report

### 2.1 Report Structure

```
Quarterly Financial Report
├── Executive Summary
│   ├── Key Metrics
│   ├── Quarter Highlights
│   └── Variance Analysis
├── Income Statement
│   ├── Operating Income
│   │   ├── Student Fees (by category)
│   │   ├── Admission Fees
│   │   ├── Examination Fees
│   │   ├── Library Fees
│   │   └── Other Academic Fees
│   ├── Non-Operating Income
│   │   ├── Grants & Donations
│   │   ├── Interest Income
│   │   └── Miscellaneous
│   └── Total Income
├── Expense Statement
│   ├── Personnel Costs
│   │   ├── Faculty Salaries (by department)
│   │   ├── Administrative Staff Salaries
│   │   ├── Support Staff Salaries
│   │   ├── Benefits & Allowances
│   │   └── Professional Development
│   ├── Operating Expenses
│   │   ├── Utilities (Electricity, Water, Internet)
│   │   ├── Maintenance & Repairs
│   │   ├── Supplies & Materials
│   │   ├── Library Resources
│   │   └── IT Infrastructure
│   ├── Administrative Expenses
│   │   ├── Office Supplies
│   │   ├── Communication
│   │   ├── Travel & Transport
│   │   └── Legal & Professional Fees
│   ├── Emergency & Contingency
│   └── Total Expenses
├── Profit & Loss
│   ├── Net Income/Loss
│   ├── Margin Analysis
│   └── Trend Analysis
├── Balance Sheet Summary
│   ├── Assets
│   ├── Liabilities
│   └── Net Worth
├── Department-wise Analysis
│   ├── Income per Department
│   ├── Expenses per Department
│   └── Department Profitability
├── Student Metrics
│   ├── Enrollment Statistics
│   ├── Fee Collection Rate
│   ├── Outstanding Fees
│   └── Scholarship Disbursements
└── Comparative Analysis
    ├── Quarter-over-Quarter
    ├── Year-over-Year
    └── Budget vs Actual
```

### 2.2 Data Fields Required

```python
class EnhancedQuarterlyReport:
    # Basic Info
    report_id: int
    report_number: str
    financial_year: str
    quarter: int  # 1-4
    start_date: date
    end_date: date
    
    # Executive Summary
    total_revenue: Decimal
    total_expenses: Decimal
    net_profit_loss: Decimal
    profit_margin: float
    key_highlights: List[str]
    major_concerns: List[str]
    
    # Income Breakdown
    income_by_category: Dict[str, Decimal]
    fee_income_breakdown: Dict[str, Decimal]
    grant_income: Decimal
    other_income: Decimal
    
    # Expense Breakdown
    salary_expenses_by_department: Dict[str, Decimal]
    salary_expenses_by_designation: Dict[str, Decimal]
    operating_expenses_breakdown: Dict[str, Decimal]
    utility_expenses: Dict[str, Decimal]
    maintenance_expenses: Decimal
    administrative_expenses: Dict[str, Decimal]
    emergency_expenses: Decimal
    
    # Department Analysis
    department_wise_income: Dict[str, Decimal]
    department_wise_expenses: Dict[str, Decimal]
    department_profitability: Dict[str, Decimal]
    
    # Student Metrics
    total_students: int
    new_admissions: int
    student_by_program: Dict[str, int]
    fees_collected: Decimal
    fees_outstanding: Decimal
    collection_rate: float
    scholarship_amount: Decimal
    
    # Comparative Data
    previous_quarter_comparison: Dict
    year_over_year_comparison: Dict
    budget_variance: Dict
    
    # Charts & Graphs Data
    income_trend: List[Dict]
    expense_trend: List[Dict]
    enrollment_trend: List[Dict]
```

## 3. Annual Report

### 3.1 Annual Report Structure

```
Annual Financial Report
├── Cover & Introduction
│   ├── Institution Overview
│   ├── Vision & Mission
│   └── Academic Year Highlights
├── Executive Summary
│   ├── Financial Performance Overview
│   ├── Key Achievements
│   ├── Major Initiatives
│   └── Future Outlook
├── Comprehensive Income Statement (12 months)
│   ├── Quarter-wise Income
│   ├── Month-wise Income Trend
│   ├── Income Category Analysis
│   └── Income Growth Analysis
├── Comprehensive Expense Statement (12 months)
│   ├── Quarter-wise Expenses
│   ├── Month-wise Expense Trend
│   ├── Category-wise Analysis
│   └── Expense Optimization Insights
├── Annual Profit & Loss
│   ├── Quarterly P&L Summary
│   ├── Annual Net Profit/Loss
│   ├── Profitability Ratios
│   └── Financial Health Indicators
├── Balance Sheet (Year End)
│   ├── Assets
│   │   ├── Current Assets
│   │   └── Fixed Assets
│   ├── Liabilities
│   │   ├── Current Liabilities
│   │   └── Long-term Liabilities
│   └── Equity
├── Cash Flow Statement
│   ├── Operating Activities
│   ├── Investing Activities
│   └── Financing Activities
├── Department Performance
│   ├── Department-wise Revenue
│   ├── Department-wise Costs
│   ├── Department-wise Profitability
│   └── Resource Utilization
├── Academic Metrics
│   ├── Student Enrollment Trends
│   ├── Program-wise Performance
│   ├── Faculty Statistics
│   ├── Academic Achievements
│   └── Examination Results
├── HR Analytics
│   ├── Faculty Count & Distribution
│   ├── Staff Count & Distribution
│   ├── Salary Distribution
│   ├── Department-wise Headcount
│   └── Attrition Analysis
├── Infrastructure & Assets
│   ├── Library Resources
│   ├── IT Infrastructure
│   ├── Laboratory Equipment
│   └── Building & Facilities
├── Financial Ratios & KPIs
│   ├── Liquidity Ratios
│   ├── Profitability Ratios
│   ├── Efficiency Ratios
│   └── Growth Metrics
└── Appendices
    ├── Detailed Schedules
    ├── Notes to Accounts
    ├── Audit Report
    └── Compliance Certificates
```

## 4. Database Schema

### 4.1 Teacher Hierarchy

```sql
CREATE TABLE teacher_hierarchy (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES employees(id),
    designation VARCHAR(100),
    department_id INTEGER REFERENCES departments(id),
    reports_to INTEGER REFERENCES employees(id),
    hierarchy_level INTEGER,
    is_department_head BOOLEAN DEFAULT FALSE,
    is_program_coordinator BOOLEAN DEFAULT FALSE,
    program_id INTEGER,
    subject_coordinator_ids INTEGER[],
    effective_from DATE,
    effective_to DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2 Annual Reports

```sql
CREATE TABLE annual_financial_reports (
    id SERIAL PRIMARY KEY,
    report_number VARCHAR(50) UNIQUE NOT NULL,
    financial_year VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    -- Summary
    total_annual_revenue DECIMAL(15,2),
    total_annual_expenses DECIMAL(15,2),
    net_annual_profit_loss DECIMAL(15,2),
    annual_profit_margin FLOAT,
    
    -- Quarterly breakdown
    q1_income DECIMAL(15,2),
    q2_income DECIMAL(15,2),
    q3_income DECIMAL(15,2),
    q4_income DECIMAL(15,2),
    q1_expenses DECIMAL(15,2),
    q2_expenses DECIMAL(15,2),
    q3_expenses DECIMAL(15,2),
    q4_expenses DECIMAL(15,2),
    
    -- Detailed JSON data
    monthly_income_breakdown JSONB,
    monthly_expense_breakdown JSONB,
    income_by_category JSONB,
    expenses_by_category JSONB,
    department_income JSONB,
    department_expenses JSONB,
    salary_analysis JSONB,
    
    -- Student metrics
    year_start_enrollment INTEGER,
    year_end_enrollment INTEGER,
    total_admissions INTEGER,
    total_graduations INTEGER,
    annual_fees_collected DECIMAL(15,2),
    annual_collection_rate FLOAT,
    
    -- Balance sheet
    total_assets DECIMAL(15,2),
    total_liabilities DECIMAL(15,2),
    total_equity DECIMAL(15,2),
    
    -- Metadata
    status VARCHAR(50),
    generated_by INTEGER,
    approved_by INTEGER,
    approved_at TIMESTAMP,
    pdf_path VARCHAR(500),
    excel_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 5. API Endpoints

```
# Teacher Hierarchy
POST   /hr/teachers/{id}/hierarchy
GET    /hr/teachers/{id}/hierarchy
GET    /hr/departments/{id}/hierarchy
GET    /hr/hierarchy/tree

# Annual Reports
POST   /reports/annual/generate
GET    /reports/annual
GET    /reports/annual/{id}
GET    /reports/annual/{id}/pdf
GET    /reports/annual/{id}/excel
GET    /reports/annual/{id}/print

# Enhanced Quarterly
PATCH  /reports/quarterly/{id}/enhance

# Comparative
GET    /reports/compare/quarters
GET    /reports/compare/years
GET    /reports/trend/income
GET    /reports/trend/expenses
```

## 6. Implementation Tasks

**T177 [HIER]** - Create teacher hierarchy model
**T178 [HIER]** - Implement hierarchy service  
**T179 [HIER]** - Create hierarchy API endpoints
**T180 [RPT]** - Create annual report model
**T181 [RPT]** - Implement annual report service
**T182 [RPT]** - Enhance quarterly report fields
**T183 [RPT]** - Create comparative analysis service
**T184 [RPT]** - Enhance PDF generator
**T185 [RPT]** - Enhance Excel exporter
**T186 [RPT]** - Create annual report API endpoints
**T187 [RPT]** - Add financial ratio calculations
**T188 [RPT]** - Create balance sheet generator
**T189 [RPT]** - Create cash flow generator
**T190 [DB]** - Create migration for new tables
**T191 [TEST]** - Write hierarchy tests
**T192 [TEST]** - Write annual report tests
**T193 [DOC]** - Update API documentation
