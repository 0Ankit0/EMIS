# EMIS System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         EMIS - Full Stack System                        │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │               Streamlit Frontend (Port 8501)                     │  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │  • Dashboard        • Students       • Admissions               │  │
│  │  • Academics        • HR & Payroll   • Library                  │  │
│  │  • Finance          • Reports        • Settings                 │  │
│  │                                                                  │  │
│  │  Components:                                                     │  │
│  │  - UI Components    - API Client     - Helpers                  │  │
│  │  - Charts (Plotly)  - Forms          - Authentication           │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/REST API
                                    │ (JSON)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYER                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                FastAPI Backend (Port 8000)                       │  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │  API Routes:                                                     │  │
│  │  ┌────────────┬────────────┬────────────┬─────────────┐        │  │
│  │  │ Students   │ Admissions │ Academics  │ HR          │        │  │
│  │  │ Library    │ Finance    │ Reports    │ Auth        │        │  │
│  │  └────────────┴────────────┴────────────┴─────────────┘        │  │
│  │                                                                  │  │
│  │  Services:                                                       │  │
│  │  ┌────────────┬────────────┬────────────┬─────────────┐        │  │
│  │  │ Student    │ Admission  │ Exam       │ HR          │        │  │
│  │  │ Library    │ Billing    │ Dashboard  │ Notification│        │  │
│  │  └────────────┴────────────┴────────────┴─────────────┘        │  │
│  │                                                                  │  │
│  │  Middleware:                                                     │  │
│  │  • Authentication  • RBAC  • Logging  • Error Handling          │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ SQL (SQLAlchemy)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              PostgreSQL Database (Port 5432)                     │  │
│  ├──────────────────────────────────────────────────────────────────┤  │
│  │  Tables:                                                         │  │
│  │  ┌────────────┬────────────┬────────────┬─────────────┐        │  │
│  │  │ students   │ employees  │ books      │ courses     │        │  │
│  │  │ admissions │ payroll    │ exams      │ bills       │        │  │
│  │  │ attendance │ leaves     │ issues     │ reports     │        │  │
│  │  └────────────┴────────────┴────────────┴─────────────┘        │  │
│  │                                                                  │  │
│  │  Migrations: Alembic                                            │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        SUPPORTING SERVICES                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │    Redis     │  │    Celery    │  │  Prometheus  │               │
│  │  (Caching)   │  │   (Tasks)    │  │ (Monitoring) │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Request Flow

### User Login Flow

```
User → Streamlit → POST /api/auth/login → FastAPI
                                              ↓
                                         Validate
                                              ↓
                                         Query DB
                                              ↓
                                      Generate JWT
                                              ↓
                                     Return Token
         ← Store in Session ← JSON Response ←
```

### Data Retrieval Flow

```
User → Click "Students" → GET /api/students → FastAPI
                                                  ↓
                                            Check Auth
                                                  ↓
                                            Query DB
                                                  ↓
                                          Format JSON
                                                  ↓
         ← Display Table ← JSON Response ←
```

### Data Creation Flow

```
User → Fill Form → Submit → POST /api/students → FastAPI
                                                     ↓
                                               Validate
                                                     ↓
                                               Save DB
                                                     ↓
                                           Return Created
         ← Show Success ← JSON Response ←
```

## Technology Stack

### Frontend
```
┌─────────────────────────────────┐
│ Streamlit 1.29.0                │
│ ├── UI Framework                │
│ ├── Plotly (Charts)             │
│ ├── Pandas (Data)               │
│ └── Requests (API)              │
└─────────────────────────────────┘
```

### Backend
```
┌─────────────────────────────────┐
│ FastAPI (Python 3.11+)          │
│ ├── Pydantic (Validation)       │
│ ├── SQLAlchemy (ORM)            │
│ ├── Alembic (Migrations)        │
│ ├── JWT (Authentication)        │
│ └── Celery (Tasks)              │
└─────────────────────────────────┘
```

### Database
```
┌─────────────────────────────────┐
│ PostgreSQL 15+                  │
│ ├── JSONB Support               │
│ ├── Full-text Search            │
│ └── Advanced Indexing           │
└─────────────────────────────────┘
```

## Module Architecture

### Frontend Modules
```
frontend/
├── app.py (Entry Point)
├── pages/
│   ├── dashboard.py     → GET /api/dashboard/metrics
│   ├── students.py      → GET/POST/PUT/DELETE /api/students
│   ├── admissions.py    → GET/POST /api/admissions
│   ├── academics.py     → GET /api/courses, /api/exams
│   ├── hr.py            → GET /api/hr/employees
│   ├── library.py       → GET /api/library/books
│   ├── finance.py       → GET /api/finance/bills
│   ├── reports.py       → GET /api/reports
│   └── settings.py      → PUT /api/users/profile
└── utils/
    └── api_client.py    → HTTP Communication
```

### Backend Modules
```
src/
├── routes/              → API Endpoints
│   ├── students.py      → Student CRUD
│   ├── admissions.py    → Admission processing
│   ├── library.py       → Library operations
│   └── ...
├── services/            → Business Logic
│   ├── student_service.py
│   ├── library_service.py
│   └── ...
├── models/              → Database Models
│   ├── student.py
│   ├── book.py
│   └── ...
└── middleware/          → Cross-cutting
    ├── auth.py
    ├── rbac.py
    └── errors.py
```

## Security Architecture

```
┌─────────────────────────────────────────────┐
│          Security Layers                    │
├─────────────────────────────────────────────┤
│  1. HTTPS (Production)                      │
│  2. JWT Authentication                      │
│  3. RBAC (Role-Based Access)               │
│  4. Input Validation (Pydantic)            │
│  5. SQL Injection Prevention (ORM)         │
│  6. CSRF Protection                         │
│  7. Rate Limiting                           │
│  8. Audit Logging                           │
└─────────────────────────────────────────────┘
```

## Deployment Architecture

### Development
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Streamlit   │────▶│   FastAPI    │────▶│ PostgreSQL   │
│  localhost   │     │  localhost   │     │  Docker      │
│  :8501       │     │  :8000       │     │  :5432       │
└──────────────┘     └──────────────┘     └──────────────┘
```

### Production
```
┌───────────┐      ┌───────────┐      ┌──────────────┐
│  Nginx    │─────▶│ Streamlit │      │   FastAPI    │
│  :80/443  │      │ Gunicorn  │─────▶│  Gunicorn    │
└───────────┘      └───────────┘      └──────────────┘
                                              │
                                              ▼
                                      ┌──────────────┐
                                      │ PostgreSQL   │
                                      │ (Managed)    │
                                      └──────────────┘
```

## Data Flow Diagram

```
┌────────────────────────────────────────────────────────────┐
│                      User Actions                          │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                  Streamlit Frontend                        │
│  • Render UI                                              │
│  • Handle Events                                          │
│  • Manage State                                           │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                    API Client Layer                        │
│  • Format Requests                                        │
│  • Add Headers                                            │
│  • Handle Errors                                          │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                   FastAPI Routing                          │
│  • Route Matching                                         │
│  • Middleware Execution                                   │
│  • Request Validation                                     │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                  Service Layer                             │
│  • Business Logic                                         │
│  • Data Processing                                        │
│  • Validation                                             │
└────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────┐
│                   Database Layer                           │
│  • Query Execution                                        │
│  • Transaction Management                                 │
│  • Data Persistence                                       │
└────────────────────────────────────────────────────────────┘
```

## Conclusion

This architecture provides:
- ✅ Separation of Concerns
- ✅ Scalability
- ✅ Maintainability
- ✅ Security
- ✅ Performance
- ✅ Testability

The system is designed to be modular, extensible, and production-ready.
