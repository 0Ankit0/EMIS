# Financial Core - Specification

## Overview

The Financial Core handles all monetary transactions, billing, accounting, and financial reporting for the college.

## Modules

### 1. Fee Management & Billing
**Purpose**: A critical module for colleges. Handles complex fee structures, generates invoices, tracks payments, and manages outstanding balances.

**Features**:
- Fee structure definition
- Multiple fee types (tuition, lab, hostel, transport, library, event, etc.)
- Bill generation
- Payment processing
- Payment gateway integration (Razorpay, PayU)
- Outstanding balance tracking
- Payment history
- Late fee calculation
- Installment management
- Bulk bill generation
- Bill printing with QR codes
- Email bills to students/parents
- Fee receipts

### 2. Financial Aid Management
**Purpose**: Tracks student scholarships, grants, and other forms of financial aid, applying them to the student's ledger.

**Features**:
- Scholarship management
- Grant tracking
- Financial aid application
- Eligibility verification
- Aid disbursement
- Aid adjustment in student bills
- Reporting to funding agencies

### 3. Accounting System
**Purpose**: Complete accounting system with double-entry bookkeeping, expense tracking, and financial reporting.

**Features**:
- Double-entry accounting
- Chart of accounts
- Journal entries
- General ledger
- Income tracking
- Expense tracking
- Budget management
- Vendor payments
- Expense categories
- Income categories
- Bank reconciliation

### 4. Financial Reporting
**Purpose**: Generates comprehensive financial reports for management and regulatory compliance.

**Features**:
- Quarterly financial reports
- Annual financial reports
- Balance sheet
- Cash flow statement
- Income statement
- Profit & loss statement
- Financial ratios
- Budget vs actual reports
- Comparative analysis
- Trend analysis
- UGC/AICTE compliance reports
- Tax reporting

### 5. Dashboard & Analytics
**Purpose**: Provides real-time financial metrics and insights for decision-making.

**Features**:
- Financial KPIs dashboard
- Revenue tracking
- Expense tracking
- Profit margins
- Collection efficiency
- Outstanding fees summary
- Fee collection trends
- Department-wise financial analysis
- Real-time data refresh

## Database Models

- FeeStructure
- Bill
- BillItem
- Payment
- Scholarship
- FinancialAid
- JournalEntry
- Expense
- Income
- ExpenseCategory
- IncomeCategory
- Budget
- QuarterlyReport
- AnnualFinancialReport
- DashboardMetrics
- MaintenanceFee
- EmergencyExpense

## API Endpoints

See `tasks.md` for detailed endpoint specifications.

## Integration Points

- **Academic Core**: Student fee tracking, course fees
- **Administrative Core**: Employee payroll, vendor payments, hostel/transport fees
- **Library**: Fine collection
- **Events**: Event fee collection
- **Payment Gateways**: Razorpay, PayU, other payment providers

## Compliance

- Income Tax Act compliance
- Goods and Services Tax (GST) compliance
- UGC/AICTE reporting requirements
- Audit trail maintenance
- GDPR/Data protection compliance
