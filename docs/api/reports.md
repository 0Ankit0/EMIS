# Reports API Documentation

## Base URL
`/api/reports`

## Overview
The Reports API provides comprehensive financial and operational reporting capabilities.

## Authentication
All endpoints require authentication with appropriate permissions.

---

## Endpoints

### Quarterly Reports

#### Generate Quarterly Report
```http
POST /api/reports/quarterly
```

**Request Body:**
```json
{
  "year": 2024,
  "quarter": 1,
  "academic_year_id": 1
}
```

**Response:**
```json
{
  "message": "Quarterly report generated",
  "report_id": 1
}
```

#### Get Quarterly Report
```http
GET /api/reports/quarterly/{report_id}
```

**Response:**
```json
{
  "id": 1,
  "year": 2024,
  "quarter": 1,
  "total_income": 5000000.00,
  "total_expenses": 4000000.00,
  "net_profit": 1000000.00,
  "income_breakdown": {
    "tuition_fees": 3500000.00,
    "lab_fees": 800000.00,
    "other": 700000.00
  },
  "expense_breakdown": {
    "salaries": 2500000.00,
    "utilities": 500000.00,
    "maintenance": 1000000.00
  }
}
```

### Annual Reports

#### Generate Annual Report
```http
POST /api/reports/annual
```

**Request Body:**
```json
{
  "year": 2024,
  "academic_year_id": 1
}
```

#### Get Annual Report
```http
GET /api/reports/annual/{year}
```

**Response:**
```json
{
  "year": 2024,
  "total_revenue": 20000000.00,
  "total_expenses": 16000000.00,
  "net_profit": 4000000.00,
  "assets": 50000000.00,
  "liabilities": 10000000.00,
  "equity": 40000000.00,
  "quarterly_breakdown": []
}
```

### Compliance Reports

#### Generate Compliance Report
```http
POST /api/reports/compliance
```

**Request Body:**
```json
{
  "report_type": "UGC",
  "year": 2024
}
```

#### Get Compliance Report
```http
GET /api/reports/compliance/{report_id}
```

### Export Reports

#### Export Report as PDF
```http
GET /api/reports/{report_id}/export/pdf
```

**Response:** PDF file download

#### Export Report as Excel
```http
GET /api/reports/{report_id}/export/excel
```

**Response:** Excel file download

### Financial Dashboards

#### Get Financial Dashboard
```http
GET /api/reports/dashboard/financial?period=month
```

**Response:**
```json
{
  "total_revenue": 1500000.00,
  "total_expenses": 1200000.00,
  "net_income": 300000.00,
  "collection_rate": 85.5,
  "outstanding_dues": 500000.00,
  "revenue_trend": [],
  "expense_trend": []
}
```

### Custom Reports

#### Generate Custom Report
```http
POST /api/reports/custom
```

**Request Body:**
```json
{
  "report_name": "Department-wise Fee Collection",
  "start_date": "2024-01-01",
  "end_date": "2024-03-31",
  "filters": {
    "department_id": 1,
    "payment_status": "paid"
  }
}
```

---

## Data Models

### Quarterly Report
```json
{
  "id": 1,
  "year": 2024,
  "quarter": 1,
  "total_income": 5000000.00,
  "total_expenses": 4000000.00,
  "net_profit": 1000000.00,
  "generated_date": "2024-04-01T10:00:00",
  "generated_by": 1
}
```

### Annual Report
```json
{
  "id": 1,
  "year": 2024,
  "total_revenue": 20000000.00,
  "total_expenses": 16000000.00,
  "net_profit": 4000000.00,
  "generated_date": "2024-12-31T10:00:00"
}
```

---

## Report Types

- `quarterly` - Quarterly financial reports
- `annual` - Annual financial reports
- `compliance` - Regulatory compliance reports
- `ugc` - UGC reports
- `aicte` - AICTE reports
- `custom` - Custom reports

## Export Formats

- `pdf` - PDF document
- `excel` - Excel spreadsheet
- `csv` - CSV file
- `json` - JSON data
