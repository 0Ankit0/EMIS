# Dashboard API Documentation

## Overview

The Dashboard API provides real-time financial metrics, KPIs, and insights for institutional decision-making.

## Base URL

```
/api/v1/dashboard
```

## Authentication

All endpoints require authentication and `dashboard:read` permission.

## Endpoints

### Dashboard Metrics

#### Get Latest Metrics

```http
GET /metrics
```

Get comprehensive dashboard metrics for today.

**Response:**

```json
{
  "metric_date": "2025-11-10",
  "daily_revenue": 125000.00,
  "monthly_revenue": 2500000.00,
  "daily_expenses": 50000.00,
  "monthly_expenses": 1000000.00,
  "daily_profit": 75000.00,
  "monthly_profit": 1500000.00,
  "total_students": 1500,
  "new_admissions_today": 5,
  "fees_collected_today": 125000.00,
  "fees_pending": 500000.00,
  "fee_collection_rate": 83.33
}
```

#### Refresh Metrics

```http
POST /metrics/refresh
```

Manually trigger metrics recalculation.

**Permissions:** `dashboard:admin`

---

### Financial Summary

#### Get Financial Summary

```http
GET /financial-summary
```

Get comprehensive financial overview.

**Response:**

```json
{
  "current_month": {
    "revenue": 2500000.00,
    "expenses": 1000000.00,
    "profit": 1500000.00,
    "profit_margin": 60.0
  },
  "current_quarter": {
    "revenue": 7000000.00,
    "expenses": 2800000.00,
    "profit": 4200000.00
  },
  "current_year": {
    "revenue": 20000000.00,
    "expenses": 8000000.00,
    "profit": 12000000.00
  },
  "outstanding_fees": 1500000.00,
  "collection_efficiency": 92.5
}
```

---

### Student Summary

#### Get Student Summary

```http
GET /student-summary
```

**Response:**

```json
{
  "total_students": 1500,
  "active_students": 1480,
  "new_admissions_this_month": 50,
  "students_by_program": {
    "B.Tech": 800,
    "M.Tech": 300,
    "MBA": 400
  },
  "attendance_average": 87.5,
  "low_attendance_count": 25
}
```

---

### Library Summary

#### Get Library Summary

```http
GET /library-summary
```

**Response:**

```json
{
  "total_books": 15000,
  "books_issued": 1200,
  "books_available": 13800,
  "overdue_books": 45,
  "fines_pending": 4500.00,
  "active_members": 1350,
  "popular_books": [...]
}
```

---

### Real-Time Metrics (T270)

#### Real-Time Financial

```http
GET /real-time/financial
```

Get live financial metrics with auto-refresh support.

**Response:**

```json
{
  "timestamp": "2025-11-10",
  "metrics": {
    "daily_revenue": 125000.00,
    "monthly_revenue": 2500000.00,
    "daily_expenses": 50000.00,
    "monthly_expenses": 1000000.00,
    "daily_profit": 75000.00,
    "monthly_profit": 1500000.00,
    "collection_efficiency": 92.5
  },
  "trends": {
    "revenue_trend": "increasing",
    "expense_trend": "stable",
    "profit_trend": "increasing"
  }
}
```

**Features:**
- Real-time data calculation
- Auto-refresh every 30 seconds (client-side)
- Trending indicators
- Live collection efficiency

#### Real-Time Students

```http
GET /real-time/students
```

Live student metrics including today's admissions, active students.

#### Real-Time Attendance

```http
GET /real-time/attendance
```

Live attendance metrics for today.

---

### KPI Overview

#### Get KPI Overview

```http
GET /kpi/overview
```

Get Key Performance Indicators summary.

**Response:**

```json
{
  "financial_kpis": {
    "revenue_growth": 15.5,
    "expense_ratio": 40.0,
    "profit_margin": 60.0,
    "collection_efficiency": 92.5
  },
  "academic_kpis": {
    "student_retention": 95.0,
    "average_attendance": 87.5,
    "pass_percentage": 92.0,
    "placement_rate": 85.0
  },
  "operational_kpis": {
    "staff_utilization": 88.0,
    "library_utilization": 75.0,
    "hostel_occupancy": 90.0
  }
}
```

---

## Metrics Calculation

### Revenue
- Sum of all fee payments received
- Includes tuition, hostel, transport, library, events

### Expenses
- All operational expenses recorded
- Includes salaries, maintenance, utilities, purchases

### Profit
```
Profit = Revenue - Expenses
Profit Margin = (Profit / Revenue) × 100
```

### Collection Efficiency
```
Collection Efficiency = (Fees Collected / Total Fees Due) × 100
```

### Fee Collection Rate
```
Fee Collection Rate = (Amount Paid / Total Amount) × 100
```

---

## Auto-Refresh Guidelines

For real-time dashboards:

1. **Financial Metrics**: Refresh every 30 seconds
2. **Student Metrics**: Refresh every 1 minute  
3. **Attendance Metrics**: Refresh every 2 minutes
4. **KPI Overview**: Refresh every 5 minutes

**WebSocket Support**: Coming soon for push-based updates

---

## Use Cases

### Executive Dashboard

```javascript
// Frontend implementation example
setInterval(async () => {
  const financial = await fetch('/api/v1/dashboard/real-time/financial');
  const students = await fetch('/api/v1/dashboard/real-time/students');
  updateDashboard(financial, students);
}, 30000); // 30 seconds
```

### Mobile App

```javascript
// Lightweight metrics for mobile
const kpis = await fetch('/api/v1/dashboard/kpi/overview');
displayKPIs(kpis);
```

### Reporting

```javascript
// Daily summary for reports
const metrics = await fetch('/api/v1/dashboard/metrics');
generateDailyReport(metrics);
```

---

## Permissions

- `dashboard:read` - View dashboard metrics
- `dashboard:admin` - Refresh and manage dashboard

---

## Performance

- Metrics are cached for 5 minutes
- Real-time endpoints bypass cache
- Background jobs update metrics every hour
- Manual refresh available for admins

---

## Trends

Trend indicators:
- `increasing` - Metric growing >5%
- `stable` - Metric within ±5%
- `decreasing` - Metric falling >5%

---

## Implementation Status

✅ All endpoints implemented (T269-T271)
- [X] T269 - Dashboard endpoints
- [X] T270 - Real-time data refresh
- [X] T271 - API documentation
