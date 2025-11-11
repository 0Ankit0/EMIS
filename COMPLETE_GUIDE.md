# EMIS - Complete System Guide

## 🎓 Education Management Information System

### Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [System Architecture](#system-architecture)
4. [Features](#features)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage Guide](#usage-guide)
8. [API Reference](#api-reference)
9. [Development](#development)
10. [Deployment](#deployment)
11. [Troubleshooting](#troubleshooting)

---

## Introduction

EMIS is a comprehensive Education Management Information System built with:
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Streamlit
- **Database**: PostgreSQL
- **Cache**: Redis
- **Tasks**: Celery

### Key Features

✅ Student Information System (SIS)
✅ Admissions & Enrollment Management
✅ Academic Management (Courses, Exams, Results)
✅ HR & Payroll System
✅ Library Management
✅ Finance & Billing
✅ Reports & Analytics
✅ Multi-user with RBAC

---

## Quick Start

### Prerequisites

```bash
- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (optional)
- Git
```

### 5-Minute Setup

```bash
# 1. Clone repository
git clone <repo-url>
cd EMIS

# 2. Checkout frontend branch
git checkout frontend-streamlit

# 3. Start backend (Terminal 1)
./setup.sh
./start-dev.sh

# 4. Start frontend (Terminal 2)
cd frontend
./start-frontend.sh

# 5. Open browser
# Frontend: http://localhost:8501
# Backend: http://localhost:8000/docs
```

### Default Credentials

```
Username: admin
Password: admin123
```

---

## System Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Streamlit  │─────▶│   FastAPI   │─────▶│ PostgreSQL  │
│  Frontend   │      │   Backend   │      │  Database   │
│  :8501      │      │   :8000     │      │  :5432      │
└─────────────┘      └─────────────┘      └─────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture.

---

## Features

### 📊 Dashboard
- Real-time KPIs
- Enrollment statistics
- Financial overview
- Attendance trends
- Recent activities

### 👨‍🎓 Student Management
- Student registration
- Profile management
- Attendance tracking
- Academic records
- Document management

### 📝 Admissions
- Online applications
- Document verification
- Merit list generation
- Admission processing
- Fee collection

### 📚 Academics
- Course management
- Timetable scheduling
- Exam management
- Result publication
- Assignment tracking

### 💼 HR & Payroll
- Employee management
- Payroll processing
- Leave management
- Performance reviews
- Recruitment tracking

### 📖 Library
- Book catalog
- Circulation management
- Fine calculation
- Digital resources
- Reports

### 💰 Finance
- Fee structure management
- Bill generation
- Payment tracking
- Accounting
- Budget management

### 📊 Reports
- Custom report builder
- Quarterly reports
- Annual reports
- Analytics dashboard
- Data export

---

## Installation

### Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup database
docker-compose up -d postgres redis

# Run migrations
alembic upgrade head

# Start server
uvicorn src.app:app --reload
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start Streamlit
streamlit run app.py
```

---

## Configuration

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://emis:emis@localhost:5432/emis

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://localhost:6379

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
```

### Frontend (.env)

```bash
# API Configuration
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30

# Session
SESSION_TIMEOUT=3600
TOKEN_REFRESH_INTERVAL=1800
```

---

## Usage Guide

### Adding a Student

1. **Navigate to Students module**
   - Click "Students" in sidebar

2. **Fill student form**
   - First Name, Last Name
   - Email, Phone
   - Date of Birth
   - Program, Admission Year

3. **Submit**
   - Click "Add Student"
   - View success message

### Processing Admission

1. **Go to Admissions**
   - View pending applications

2. **Review application**
   - Check documents
   - Verify details

3. **Approve/Reject**
   - Make decision
   - Generate offer letter

### Library Book Issue

1. **Go to Library → Circulation**

2. **Select book and member**

3. **Set issue date and due date**

4. **Click Issue Book**

### Generate Financial Report

1. **Navigate to Reports**

2. **Select report type**
   - Quarterly/Annual
   - Custom date range

3. **Choose filters**
   - Department, Program, etc.

4. **Generate and download**

---

## API Reference

### Authentication

```bash
POST /api/auth/login
{
  "username": "admin",
  "password": "admin123"
}

Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {...}
}
```

### Students

```bash
# List students
GET /api/students?page=1&limit=20

# Get student
GET /api/students/{id}

# Create student
POST /api/students
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}

# Update student
PUT /api/students/{id}
{...}

# Delete student
DELETE /api/students/{id}
```

Full API documentation: http://localhost:8000/docs

---

## Development

### Project Structure

```
EMIS/
├── src/                    # Backend source
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   ├── models/            # Database models
│   └── middleware/        # Middleware
├── frontend/              # Streamlit frontend
│   ├── pages/            # UI pages
│   ├── components/       # UI components
│   └── utils/            # Utilities
├── tests/                # Test suite
├── alembic/              # Migrations
└── docs/                 # Documentation
```

### Running Tests

```bash
# Backend tests
pytest

# Integration tests
./test-integration.sh

# Frontend tests
cd frontend
python -m pytest
```

### Adding New Features

1. **Backend**: Create route, service, model
2. **Frontend**: Create page, integrate API
3. **Test**: Write tests
4. **Document**: Update docs

---

## Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Check status
docker-compose ps
```

### Production Setup

```bash
# Backend with Gunicorn
gunicorn src.app:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend with production settings
streamlit run frontend/app.py --server.port=80 --server.headless=true
```

### Environment Variables

Production .env should include:
- Strong SECRET_KEY
- Production DATABASE_URL
- HTTPS configuration
- Email credentials
- API keys

---

## Troubleshooting

### Backend won't start

```bash
# Check PostgreSQL
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Frontend connection error

```bash
# Verify backend is running
curl http://localhost:8000/health

# Check API URL in frontend/.env
cat frontend/.env | grep API_BASE_URL

# Test API connection
./test-integration.sh
```

### Database errors

```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres

# Run migrations
alembic upgrade head

# Create admin user
python -m src.cli.user_commands create-admin
```

### Port conflicts

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

---

## Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Frontend README**: [frontend/README.md](frontend/README.md)
- **Integration Guide**: [frontend/INTEGRATION.md](frontend/INTEGRATION.md)
- **Quick Start**: [FRONTEND_QUICKSTART.md](FRONTEND_QUICKSTART.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Support

For issues and questions:
- **GitHub Issues**: [Create an issue](https://github.com/yourorg/emis/issues)
- **Documentation**: Check docs/ folder
- **Email**: support@emis.com

---

## License

Copyright © 2024 EMIS. All rights reserved.

---

## Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the list of contributors.

---

**Built with ❤️ using FastAPI and Streamlit**
