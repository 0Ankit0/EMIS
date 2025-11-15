# EMIS - Educational Management Information System

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive full-stack web application for educational institutions built with **Django 4.2+**, PostgreSQL, and modern Python.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd EMIS
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.development .env
# Edit .env with your database credentials

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Start development server
./start-dev.sh
```

**Access:**
- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- API: http://localhost:8000/api/v1/

📖 **Full documentation**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)

## ✨ Features

### 🎓 Student Management
- Admissions, enrollment, academic records
- Attendance tracking and reporting
- Marks entry, exams, results, transcripts
- Class schedules and timetables
- Graduation and alumni tracking

### 👥 HR & Payroll
- Employee management and recruitment
- Payroll processing with tax calculations
- Leave management (casual, sick, earned)
- Performance reviews and appraisals
- 9-level teacher hierarchy (Principal to TA)

### 📚 Library Management
- Book cataloging with ISBN
- Circulation: issue, return, renew, reserve
- Faculty/student borrowing with different limits
- Lost book management with auto fines
- Barcode/RFID ready

### 🎯 Learning Management System (LMS)
- Course creation and content delivery
- Assignments, quizzes, assessments
- Video conferencing integration (Zoom/Teams)
- Discussion forums and collaboration

### 💰 Financial Management
- 28+ bill types (tuition, hostel, transport, etc.)
- Professional PDF bills with QR codes
- Double-entry accounting
- Quarterly and annual reports
- Budget analysis and tracking

### 📊 Analytics & Reporting
- Real-time dashboards
- Student performance analytics
- Financial reports (PDF/Excel export)
- Custom report builder
- Predictive analytics

### 🔔 Notifications
- Multi-channel (email, SMS, in-app)
- Bulk messaging
- Delivery tracking

### 🔒 Security & Compliance
- JWT + Session authentication
- Role-based access control (RBAC)
- Audit logging
- GDPR data tools
- Indian IT Act compliance

## 🛠️ Tech Stack

- **Framework**: Django 4.2+
- **API**: Django REST Framework
- **Database**: PostgreSQL 15+
- **Frontend**: Bootstrap 5, HTMX, Chart.js
- **Cache/Queue**: Redis + Celery
- **Server**: Gunicorn
- **Testing**: pytest-django

## 📁 Project Structure

```
EMIS/
├── config/              # Django configuration
├── apps/                # 18 Django applications
│   ├── authentication/  # User & auth
│   ├── students/       # Student portal
│   ├── faculty/        # Faculty portal
│   ├── hr/             # HR management
│   ├── finance/        # Finance
│   └── ...             # 13 more apps
├── templates/          # HTML templates
├── static/             # CSS, JS, images
└── manage.py           # Django CLI
```

## 📚 Documentation

- **[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)** - Complete setup and development guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Common commands
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide

## 🐳 Docker Deployment

```bash
# Start all services (PostgreSQL, Redis, Django, Celery)
./start-prod.sh

# Or manually
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# With pytest
pytest

# With coverage
pytest --cov=apps --cov-report=html
```

## 📝 License

[Your License Here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📧 Support

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ using Django**
