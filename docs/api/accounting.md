# Accounting API Documentation

## Overview

The Accounting API provides comprehensive double-entry bookkeeping, chart of accounts, general ledger, budget tracking, and bank reconciliation functionality.

## Base URL

```
/api/v1/accounting
```

## Authentication

All endpoints require authentication and appropriate permissions.

## Endpoints

### Expense Tracking

#### Record Expense

```http
POST /expenses
```

**Request Body:**

```json
{
  "title": "Office Supplies Purchase",
  "amount": 5000.00,
  "category_id": 1,
  "description": "Monthly stationery",
  "paid_to": "ABC Supplies",
  "payment_method": "bank_transfer"
}
```

### Income Tracking

#### Record Income

```http
POST /income
```

**Request Body:**

```json
{
  "title": "Tuition Fee Collection",
  "amount": 500000.00,
  "category_id": 1,
  "description": "Q1 fee collection",
  "received_from": "Students",
  "payment_method": "online"
}
```

### Chart of Accounts (T236)

#### Create Account

```http
POST /chart-of-accounts
```

**Request Body:**

```json
{
  "account_code": "1010",
  "account_name": "Cash",
  "account_type": "asset",
  "normal_balance": "debit",
  "description": "Cash on hand",
  "is_header": false
}
```

**Account Types:**
- `asset` - Assets
- `liability` - Liabilities
- `equity` - Owner's Equity
- `revenue` - Revenue/Income
- `expense` - Expenses

**Normal Balance:**
- `debit` - Assets, Expenses
- `credit` - Liabilities, Equity, Revenue

#### Get Chart of Accounts

```http
GET /chart-of-accounts?account_type=asset&active_only=true
```

**Response:**

```json
{
  "accounts": [
    {
      "id": 1,
      "account_code": "1010",
      "account_name": "Cash",
      "account_type": "asset",
      "current_balance": 500000.00,
      "normal_balance": "debit"
    }
  ]
}
```

---

### General Ledger (T237)

#### Get Ledger Entries

```http
GET /general-ledger?account_id=1&financial_year=2024-2025
```

**Response:**

```json
{
  "entries": [
    {
      "id": 1,
      "transaction_date": "2025-11-10",
      "description": "Tuition fee payment received",
      "debit_amount": 50000.00,
      "credit_amount": 0.00,
      "balance_after": 550000.00,
      "account_id": 1
    }
  ]
}
```

#### Get Trial Balance

```http
GET /trial-balance?financial_year=2024-2025
```

**Response:**

```json
{
  "financial_year": "2024-2025",
  "accounts": [
    {
      "account_code": "1010",
      "account_name": "Cash",
      "debit": 500000.00,
      "credit": 0.00
    },
    {
      "account_code": "4000",
      "account_name": "Tuition Fee Income",
      "debit": 0.00,
      "credit": 500000.00
    }
  ],
  "total_debit": 500000.00,
  "total_credit": 500000.00,
  "difference": 0.00,
  "balanced": true
}
```

**Permissions:** `accounting:read`

---

### Budget Tracking (T238)

#### Create Budget Allocation

```http
POST /budgets
```

**Request Body:**

```json
{
  "financial_year": "2024-2025",
  "allocated_amount": 1000000.00,
  "expense_category_id": 1,
  "department": "Computer Science",
  "quarter": 1
}
```

#### Get Budget Report

```http
GET /budgets/report?financial_year=2024-2025&quarter=1
```

**Response:**

```json
{
  "financial_year": "2024-2025",
  "quarter": 1,
  "total_allocated": 1000000.00,
  "total_spent": 450000.00,
  "total_remaining": 550000.00,
  "overall_utilization": 45.0,
  "budgets": [
    {
      "id": 1,
      "department": "Computer Science",
      "allocated": 500000.00,
      "spent": 225000.00,
      "remaining": 275000.00,
      "utilization": 45.0,
      "exceeded": false
    }
  ]
}
```

**Features:**
- Track budget vs actual spending
- Department-wise allocation
- Quarterly and annual budgets
- Automatic utilization calculation
- Overspend alerts

**Permissions:** `accounting:admin`

---

### Bank Reconciliation (T239)

#### Create Reconciliation

```http
POST /bank-reconciliation
```

**Request Body:**

```json
{
  "bank_account_id": 1,
  "statement_date": "2025-11-30",
  "period_from": "2025-11-01",
  "period_to": "2025-11-30",
  "statement_opening_balance": 500000.00,
  "statement_closing_balance": 750000.00,
  "book_opening_balance": 500000.00,
  "book_closing_balance": 745000.00
}
```

#### Perform Reconciliation

```http
POST /bank-reconciliation/{reconciliation_id}/perform
```

**Request Body:**

```json
{
  "outstanding_deposits": 10000.00,
  "outstanding_checks": 5000.00,
  "bank_charges": 500.00,
  "bank_interest": 1500.00,
  "other_adjustments": 0.00
}
```

**Response:**

```json
{
  "id": 1,
  "reconciliation_number": "BR202511301",
  "reconciled_balance": 751000.00,
  "statement_closing_balance": 750000.00,
  "difference": 1000.00,
  "is_reconciled": false
}
```

**Reconciliation Formula:**

```
Reconciled Balance = Book Balance
  + Outstanding Deposits
  - Outstanding Checks  
  - Bank Charges
  + Bank Interest
  + Other Adjustments

Difference = |Reconciled Balance - Statement Closing Balance|
Is Reconciled = Difference < ₹1.00
```

#### Get Unreconciled Items

```http
GET /bank-reconciliation/{bank_account_id}/unreconciled?period_from=2025-11-01&period_to=2025-11-30
```

**Response:**

```json
{
  "deposits": [
    {
      "date": "2025-11-29",
      "description": "Student payment",
      "amount": 10000.00,
      "balance": 755000.00
    }
  ],
  "withdrawals": [
    {
      "date": "2025-11-28",
      "description": "Salary payment",
      "amount": 5000.00,
      "balance": 750000.00
    }
  ],
  "total_deposits": 10000.00,
  "total_withdrawals": 5000.00
}
```

---

### Account Balance

#### Get Balance

```http
GET /balance?financial_year=2024-2025
```

Get overall financial balance for a period.

---

### Categories

#### Create Expense Category

```http
POST /expense-categories
```

#### Create Income Category

```http
POST /income-categories
```

---

## Permissions

- `accounting:read` - View accounting data
- `accounting:write` - Record expenses and income
- `accounting:admin` - Full accounting administration

## Financial Reporting

### Available Reports

1. **Balance Sheet** - Assets, Liabilities, Equity
2. **Income Statement** - Revenue vs Expenses
3. **Cash Flow Statement** - Cash inflows and outflows
4. **Trial Balance** - Verify double-entry balances
5. **Budget vs Actual** - Compare budget with actual spending
6. **General Ledger** - Complete transaction history

### Financial Year

- Runs from April 1 to March 31
- Quarters:
  - Q1: Apr-Jun
  - Q2: Jul-Sep
  - Q3: Oct-Dec
  - Q4: Jan-Mar

## Double-Entry Bookkeeping

Every transaction creates two entries:
- Debit entry in one account
- Credit entry in another account
- Total debits must equal total credits

**Example - Fee Payment Received:**

```
Debit: Cash (Asset) +₹50,000
Credit: Fee Income (Revenue) +₹50,000
```

## Implementation Status

✅ All endpoints implemented (T236-T243)
- [X] T236 - Chart of Accounts management
- [X] T237 - General Ledger functionality
- [X] T238 - Budget tracking
- [X] T239 - Bank reconciliation
- [X] T240 - Accounting endpoints
- [X] T241 - Expense tracking endpoints
- [X] T242 - Income tracking endpoints
- [X] T243 - API documentation
