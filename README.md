# EMIS - Educational Management Information System

A comprehensive backend API for educational institutions built with FastAPI, PostgreSQL, and modern Python.

## Features

### Core Modules ✅

- **Student Lifecycle Management**: Complete admission to alumni tracking
  - Admissions, enrollment, academic records, attendance
  - Marks entry, exams, results, transcripts
  - Class schedules, timetables
  - Graduation and alumni tracking
  
- **HR & Payroll**: Comprehensive staff management
  - Employee records, recruitment, onboarding
  - Payroll processing, tax calculations
  - Leave management (casual, sick, earned)
  - Performance reviews, appraisals
  - Teacher hierarchy (9 levels: Principal to TA)
  - Department structure and reporting relationships

- **Library Management**: Full-featured library system
  - Book cataloging (ISBN, categories, digital resources)
  - Circulation (issue, return, renew, reserve)
  - **Faculty borrowing** with different limits (10 books, 30 days)
  - **Lost book management** with automatic fine calculation
  - Configurable fines per member type (student/faculty/staff/alumni)
  - Investigation workflow for lost books
  - Payment tracking and fine waivers
  - Barcode/RFID integration ready
  
- **Learning Management System**: Complete LMS
  - Course creation and management
  - Assignments, quizzes, assessments
  - Content delivery (video, documents, presentations)
  - Plagiarism detection integration
  - Video conferencing (Zoom/Teams)
  - Discussion forums, collaboration tools
  
- **Financial Management**: Enterprise-grade accounting
  - **28 Bill Types**: Tuition, exam, hostel, transport, events, ID cards, and more
  - **Professional bill PDFs** with QR codes for online payment
  - Fee structure templates
  - Double-entry accounting system
  - Expense tracking with 15+ categories
  - Budget vs actual analysis
  - Journal entries, ledgers
  - **Quarterly reports** with income/expense analysis
  - **Annual reports** with financial statements
  - UGC/AICTE compliance reports
  
- **Analytics & Reporting**: Comprehensive insights
  - Real-time admin dashboard
  - Quarterly financial reports (PDF/Excel export)
  - Annual financial reports (balance sheet, cash flow, ratios)
  - Student performance analytics
  - Predictive analytics (scikit-learn, pandas)
  - Custom report builder
  - **Print and Save as PDF** for all reports
  - Comparative analysis (quarter-over-quarter, year-over-year)
  
- **Notifications**: Multi-channel communication
  - Email, SMS, in-app notifications
  - Bulk messaging
  - Opt-in/opt-out management
  - Delivery tracking
  - Scheduled notifications

### Advanced Features ✅

- **Authentication & Authorization**: Secure access control
  - JWT-based authentication
  - Role-based access control (RBAC)
  - Multi-level permissions
  - Audit logging for all sensitive operations
  
- **Compliance & Data Privacy**:
  - GDPR data export and deletion tools
  - Indian IT Act compliance
  - Data retention policies
  - Full audit trails
  
- **Monitoring & Observability**:
  - Prometheus metrics
  - Grafana dashboards
  - Centralized logging
  - Health check endpoints
  
- **Integration Ready**:
  - Payment gateways (Razorpay, PayU)
  - SMS gateways (Twilio, MSG91)
  - Email services (SMTP, SendGrid)
  - Document verification (DigiLocker)
  - Plagiarism detection (Turnitin)
  - Video conferencing (Zoom, Teams)

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL 15+ with async SQLAlchemy
- **Task Queue**: Celery with Redis
- **Authentication**: JWT-based auth with RBAC
- **Testing**: pytest with async support
- **Code Quality**: Black, isort, flake8, mypy
- **CI/CD**: GitHub Actions

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

## Architecture

The system follows a modular, service-oriented architecture:

```
src/
├── models/          # SQLAlchemy ORM models
├── services/        # Business logic layer
├── routes/          # FastAPI route handlers
├── middleware/      # Authentication, RBAC, error handling
├── lib/             # Shared utilities (logging, metrics, integrations)
├── cli/             # Command-line tools
└── tasks/           # Celery background tasks
```

## Getting Started

### Option 1: Docker Compose (Recommended)

```bash
# Start all services (PostgreSQL, Redis, API, Celery)
docker-compose up -d

# Check services are running
docker-compose ps

# View logs
docker-compose logs -f api

# API will be available at http://localhost:8000
```

### Option 2: Local Development

#### 1. Clone the repository

```bash
git clone <repository-url>
cd EMIS
```

#### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your database and service credentials
```

Required environment variables:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/emis
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60
```

#### 5. Start required services

```bash
# Option A: Using Docker Compose for dependencies only
docker-compose up -d postgres redis

# Option B: Install PostgreSQL and Redis locally
# See installation instructions for your OS
```

#### 6. Run database migrations

```bash
alembic upgrade head
```

#### 7. Initialize default data (optional)

```bash
# Initialize library settings
python -m src.cli.library_commands init-settings

# Create initial admin user
python -m src.cli.user_commands create-admin --email admin@example.com --password admin123
```

#### 8. Start the application

```bash
# Development server with auto-reload
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

# Production server
gunicorn src.app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The API will be available at `http://localhost:8000`

**Interactive API documentation**: `http://localhost:8000/docs` (Swagger UI)

**Alternative API docs**: `http://localhost:8000/redoc` (ReDoc)

## CLI Commands

The system provides CLI commands for common administrative tasks:

### Database Management

```bash
# Run migrations
python -m src.cli.db_commands migrate

# Rollback migration
python -m src.cli.db_commands rollback

# Reset database (WARNING: destroys all data)
python -m src.cli.db_commands reset
```

### User Management

```bash
# Create admin user
python -m src.cli.user_commands create-admin --email admin@example.com

# Create regular user
python -m src.cli.user_commands create-user --email user@example.com --role student

# List all users
python -m src.cli.user_commands list
```

### Library Management

```bash
# Initialize default library settings
python -m src.cli.library_commands init-settings

# Update settings for member type
python -m src.cli.library_commands update-settings student --fine 10 --period 21

# Calculate fine
python -m src.cli.library_commands calculate-fine student 2024-01-15 --return-date 2024-01-25

# Show all settings
python -m src.cli.library_commands show-settings
```

### Exam Management

```bash
# Create exam
python -m src.cli.exam_commands create --course-id 1 --name "Midterm Math" --code MATH-MT-2024 --date 2024-03-15

# Show exam details
python -m src.cli.exam_commands show 1

# List upcoming exams
python -m src.cli.exam_commands upcoming --days 30

# Add marks for student
python -m src.cli.exam_commands add-marks 1 10 --enrollment-id 5 --marks 85.5

# Publish all marks for exam
python -m src.cli.exam_commands publish-all-marks 1

# Generate result sheet
python -m src.cli.exam_commands generate-result --student-id 10 --enrollment-id 5 --type semester --year 2023-2024 --semester 1
```

## Development

### Run tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test file
pytest tests/unit/test_schedule_service.py

# Run tests matching pattern
pytest -k "test_fine"

# Run tests with verbose output
pytest -v

# View coverage report
open htmlcov/index.html  # macOS/Linux
# or
start htmlcov/index.html  # Windows
```

### Code Quality

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
black src/ tests/ && isort src/ tests/ && flake8 src/ tests/ && mypy src/
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

## Project Structure

```
.
├── src/
│   ├── models/          # SQLAlchemy ORM models
│   │   ├── auth.py      # User, Role, Permission models
│   │   ├── student.py   # Student lifecycle models
│   │   ├── employee.py  # HR and staff models
│   │   ├── library.py   # Library management models
│   │   ├── course.py    # Course and LMS models
│   │   └── ...
│   ├── services/        # Business logic layer
│   │   ├── student_service.py
│   │   ├── library_service.py
│   │   ├── exam_service.py
│   │   └── ...
│   ├── routes/          # FastAPI route handlers
│   │   ├── students.py
│   │   ├── library.py
│   │   ├── exams.py
│   │   └── ...
│   ├── middleware/      # Custom middleware
│   │   ├── rbac.py      # Role-based access control
│   │   └── errors.py    # Error handling
│   ├── lib/             # Shared utilities
│   │   ├── logging.py   # Centralized logging
│   │   ├── audit.py     # Audit trail
│   │   └── ...
│   ├── cli/             # CLI commands
│   │   ├── db_commands.py
│   │   ├── user_commands.py
│   │   ├── library_commands.py
│   │   └── exam_commands.py
│   ├── tasks/           # Celery background tasks
│   ├── app.py           # FastAPI application
│   ├── config.py        # Configuration
│   └── database.py      # Database connection
├── tests/
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   ├── contract/        # Contract tests
│   └── conftest.py      # Pytest fixtures
├── alembic/             # Database migrations
│   └── versions/
├── docs/                # Documentation
│   ├── api/             # API documentation
│   └── deployment.md
├── monitoring/          # Monitoring configs
│   └── grafana/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pyproject.toml
└── README.md
```
│   ├── middleware/    # Custom middleware
│   ├── cli/           # CLI commands
│   ├── lib/           # Utility libraries
│   └── tasks/         # Celery tasks
├── tests/
│   ├── contract/      # Contract tests
│   ├── integration/   # Integration tests
│   └── unit/          # Unit tests
├── alembic/           # Database migrations
├── docs/              # Documentation
└── monitoring/        # Monitoring configs
```

## Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[Quick Start Guide](docs/QUICK_START.md)** - Get up and running in 5 minutes
- **[Frontend Quick Start](docs/FRONTEND_QUICKSTART.md)** - Frontend setup guide
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture and design
- **[Development Guide](docs/DEVELOPMENT.md)** - Development setup and workflows
- **[Complete Guide](docs/COMPLETE_GUIDE.md)** - Comprehensive system documentation
- **[API Documentation](docs/API_DOCUMENTATION.md)** - REST API reference
- **[Services Documentation](docs/SERVICES_DOCUMENTATION.md)** - Business logic layer
- **[Calendar Usage Guide](docs/CALENDAR_USAGE_GUIDE.md)** - Calendar system guide
- **[Frontend Navigation](docs/NAVIGATION.md)** - Frontend navigation structure
- **[Frontend Integration](docs/INTEGRATION.md)** - Frontend-backend integration
- **[Frontend Quick Reference](docs/QUICK_REFERENCE.md)** - Quick reference guide
- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)** - Implementation details

## License

Copyright © 2025 EMIS Team
