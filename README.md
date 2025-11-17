# EMIS - Education Management Information System

A comprehensive Django-based management information system for educational institutions, providing complete solutions for admissions, academics, finance, and analytics.

## 🚀 Features

### Core Modules Implemented ✅

- **Authentication & Authorization**
  - JWT-based authentication with refresh tokens
  - Role-Based Access Control (RBAC)
  - 5 default roles (Student, Faculty, Staff, Admin, Management)
  - Password strength validation & secure hashing (bcrypt)
  - Comprehensive audit logging
  - Session management with auto-extension

- **Admissions Management**
  - Online application submission
  - Document verification workflow
  - Merit list generation with ranking
  - Application status tracking
  - Automated enrollment from accepted applications

- **Academic Management**
  - Course creation and management
  - Modular learning content delivery
  - Assignment submission and grading
  - Prerequisite validation
  - Grade records and transcripts
  - Attendance tracking

- **Finance Management**
  - Fee structure configuration
  - Invoice generation
  - Payment processing (multiple methods)
  - Late fee calculation
  - Installment support
  - Financial reports and exports (PDF, Excel, CSV)

- **Analytics & Reporting**
  - Management dashboard
  - Admissions funnel metrics
  - Attendance rate tracking
  - Fee collection analytics
  - Course completion statistics
  - Automated metric refresh (Celery)

- **System Features**
  - Full-text search (PostgreSQL tsvector)
  - Pagination and filtering
  - Internationalization (i18n) support
  - Redis caching for performance
  - Rate limiting
  - Security headers (HSTS, CSP, etc.)
  - Health and readiness checks
  - Prometheus metrics
  - OpenAPI/Swagger documentation

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 6+
- Podman (recommended) or Docker

## 🛠️ Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd EMIS
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/emis_db

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 5. Start Services with Podman

```bash
# Start PostgreSQL and Redis
podman-compose up -d db redis

# Or manually
podman run -d --name emis-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
podman run -d --name emis-redis -p 6379:6379 redis:7
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Seed initial data

```bash
# Seed authentication data (roles, permissions, resource groups)
python manage.py seed-auth
```

This creates:
- 5 Default Roles (Student, Faculty, Staff, Admin, Management)
- Resource groups and permissions for all modules
- Proper role-permission assignments

### 8. Create superuser

```bash
python manage.py createsuperuser
```

### 9. Run development server

```bash
# Django development server
python manage.py runserver

# Or with Gunicorn (production)
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### 10. Run Celery (for background tasks)

```bash
# Worker
celery -A config worker -l info

# Beat scheduler (in another terminal)
celery -A config beat -l info
```

The application will be available at `http://localhost:8000`

## 📚 Documentation

- **API Documentation**: http://localhost:8000/api/docs/ (Swagger UI)
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

- [Authentication Guide](docs/guides/auth.md)
- [API Reference](docs/api/README.md)
- [Deployment Guide](docs/deployment.md)

## 🧪 Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=apps --cov-report=html
```

Run specific test module:
```bash
pytest tests/authentication/ -v
pytest tests/admissions/ -v
pytest tests/courses/ -v
```

Run linting:
```bash
# Black formatter
black apps/ tests/

# isort imports
isort apps/ tests/

# flake8 linting
flake8 apps/ tests/

# mypy type checking
mypy apps/
```

## 🌐 API Endpoints

### Health & Monitoring
- `GET /api/v1/health/` - Basic health check
- `GET /api/v1/readiness/` - Readiness check (DB + Redis)
- `GET /api/v1/liveness/` - Liveness check
- `GET /api/v1/metrics/` - Prometheus metrics

### Authentication
- `POST /api/v1/auth/register/` - Register new user
- `POST /api/v1/auth/login/` - Login and get tokens
- `POST /api/v1/auth/logout/` - Logout
- `POST /api/v1/auth/refresh/` - Refresh access token

### Users
- `GET /api/v1/users/` - List users (paginated, searchable)
- `GET /api/v1/users/{id}/` - Get user details
- `PUT /api/v1/users/{id}/` - Update user
- `DELETE /api/v1/users/{id}/` - Delete user

### Admissions
- `POST /api/v1/admissions/applications/` - Submit application
- `GET /api/v1/admissions/applications/` - List applications
- `PATCH /api/v1/admissions/applications/{id}/status` - Update status
- `POST /api/v1/admissions/merit-lists/` - Generate merit list

### Courses
- `POST /api/v1/courses/` - Create course
- `GET /api/v1/courses/` - List courses (searchable)
- `POST /api/v1/assignments/` - Create assignment
- `POST /api/v1/submissions/` - Submit assignment
- `POST /api/v1/grades/` - Record grade

### Finance
- `POST /api/v1/finance/fee-structures/` - Create fee structure
- `POST /api/v1/finance/invoices/` - Generate invoice
- `POST /api/v1/finance/payments/` - Record payment
- `GET /api/v1/finance/reports/fee-collection` - Fee collection report

### Analytics
- `GET /api/v1/dashboard/` - Get all dashboard metrics
- `GET /api/v1/dashboard/admissions` - Admissions funnel
- `GET /api/v1/dashboard/finance` - Fee collection metrics

For complete API documentation with examples, visit:
- Swagger UI: http://localhost:8000/api/docs/
- ReDoc: http://localhost:8000/api/redoc/

## 🏗️ Architecture

### Project Structure

```
EMIS/
├── apps/
│   ├── core/              # Core utilities, middleware, base models
│   ├── authentication/    # User management, RBAC, audit
│   ├── admissions/        # Application processing, merit lists
│   ├── students/          # Student records, enrollment
│   ├── courses/           # Course management, assignments
│   ├── faculty/           # Faculty management
│   ├── finance/           # Fee management, payments
│   ├── analytics/         # Dashboard, metrics, reports
│   └── ...
├── config/                # Django settings, URLs
├── docs/                  # Documentation
├── tests/                 # Test suite
├── static/                # Static files
├── templates/             # Django templates
└── requirements.txt       # Python dependencies
```

### Tech Stack

- **Backend**: Django 4.2+, Django REST Framework
- **Database**: PostgreSQL 15+
- **Cache**: Redis 6+
- **Task Queue**: Celery with Redis broker
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Deployment**: Podman/Docker, Gunicorn

## 🔒 Security Features

- JWT-based stateless authentication
- Role-Based Access Control (RBAC)
- Password hashing with bcrypt
- Rate limiting on authentication endpoints
- Security headers (HSTS, CSP, X-Frame-Options)
- CORS configuration
- Audit logging for sensitive actions
- SQL injection protection (Django ORM)
- XSS protection

## 🚀 Deployment

See [Deployment Guide](docs/deployment.md) for detailed instructions on deploying to production.

Quick deployment with Podman:

```bash
# Build image
podman build -t emis:latest .

# Run with podman-compose
podman-compose up -d
```

## 📊 Performance Features

- PostgreSQL full-text search (tsvector)
- Redis caching for frequently accessed data
- Database connection pooling
- Query optimization (select_related, prefetch_related)
- Database indexes on frequently queried fields
- Pagination for list endpoints
- Celery for background tasks

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options.

Key settings:
- `DEBUG`: Enable/disable debug mode
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `ALLOWED_HOSTS`: Allowed hostnames
- `CORS_ALLOWED_ORIGINS`: CORS configuration

### Django Settings

Located in `config/settings.py`:
- Database configuration with connection pooling
- Redis cache configuration
- Celery configuration
- REST Framework settings
- JWT token settings
- Logging configuration

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 📧 Support

For questions or support:
- Email: support@emis.example.com
- Documentation: [docs/](docs/)
- Issues: GitHub Issues
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJh..."
}
```

#### Get Current User
```http
GET /api/v1/auth/me/
Authorization: Bearer <access_token>
```

### User Management Endpoints

#### List Users
```http
GET /api/v1/auth/users/?page=1&page_size=20&search=john
Authorization: Bearer <access_token>
```

#### Get User
```http
GET /api/v1/auth/users/{user_id}/
Authorization: Bearer <access_token>
```

#### Update User
```http
PUT /api/v1/auth/users/{user_id}/update/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "newemail@example.com"
}
```

### Role Management Endpoints

#### List Roles
```http
GET /api/v1/auth/roles/
Authorization: Bearer <access_token>
```

#### Create Role
```http
POST /api/v1/auth/roles/create/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Teacher",
  "description": "Teaching staff role"
}
```

#### Assign Permissions to Role
```http
POST /api/v1/auth/roles/{role_id}/permissions/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "permission_ids": [
    "uuid1",
    "uuid2"
  ]
}
```

#### Assign Role to User
```http
POST /api/v1/auth/users/{user_id}/roles/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "role_id": "uuid"
}
```

### Audit Log Endpoints

#### List Audit Logs
```http
GET /api/v1/auth/audit/logs/?page=1&action=login
Authorization: Bearer <access_token>
```

#### Get User Activity
```http
GET /api/v1/auth/audit/users/{user_id}/activity/?days=30
Authorization: Bearer <access_token>
```

#### Get Security Events
```http
GET /api/v1/auth/audit/security-events/?hours=24
Authorization: Bearer <access_token>
```

## 🏗️ Architecture

### Project Structure

```
EMIS/
├── apps/
│   ├── authentication/
│   │   ├── models.py          # User, Role, Permission, AuditLog
│   │   ├── serializers/       # DRF serializers
│   │   ├── services/          # Business logic layer
│   │   ├── api/               # API views
│   │   ├── api_views.py       # Auth endpoints
│   │   └── management/        # Management commands
│   ├── core/
│   │   ├── models.py          # Base models
│   │   ├── exceptions.py      # Custom exceptions
│   │   ├── error_codes.py     # Error code registry
│   │   ├── middleware/        # Custom middleware
│   │   ├── serializers/       # Base serializers
│   │   └── utils/             # Utilities
│   ├── students/
│   ├── finance/
│   ├── exams/
│   └── lms/
├── config/
│   ├── settings.py           # Django settings
│   ├── urls.py               # URL configuration
│   └── celery.py             # Celery configuration
├── tests/                    # Test suite
├── static/                   # Static files
├── templates/                # Django templates
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
└── manage.py                # Django management script
```

### Architecture Layers

1. **Models Layer**: Database models and business entities
2. **Service Layer**: Business logic and operations
3. **Serializer Layer**: Data validation and transformation
4. **API Layer**: RESTful endpoints
5. **Middleware Layer**: Cross-cutting concerns (auth, audit, etc.)

## 🔐 Security

### Implemented Security Features

- **Password Security**
  - Bcrypt hashing
  - Minimum 8 characters
  - Complexity requirements
  - Password history (planned)

- **Authentication**
  - JWT tokens with expiration
  - Refresh token rotation
  - Token blacklisting support

- **Authorization**
  - Role-based access control (RBAC)
  - Permission-based endpoint protection
  - Resource-level permissions

- **Audit Trail**
  - All sensitive operations logged
  - IP address tracking
  - User agent logging
  - Failed login monitoring

- **API Security**
  - CORS configuration
  - Rate limiting (planned)
  - Request validation
  - SQL injection prevention

## 📊 Default Roles & Permissions

### Roles Created by `seed_auth`

1. **Super Admin** (114 permissions)
   - Full system access

2. **Admin** (107 permissions)
   - Most features except sensitive HR/payroll

3. **Management** (42 permissions)
   - View and export across all modules

4. **Faculty** (19 permissions)
   - Course, assignment, and grade management

5. **Admissions Officer** (18 permissions)
   - Application and enrollment management

6. **Finance Officer** (18 permissions)
   - Fee and payment management

7. **Librarian** (12 permissions)
   - Library management

8. **Staff** (7 permissions)
   - Basic operational access

9. **Student** (0 permissions - to be configured)
10. **Parent** (0 permissions - to be configured)

### Resource Groups

- Authentication (users, roles, permissions, audit)
- Students (records, enrollment)
- Admissions (applications, merit lists)
- Courses (content, assignments, grades)
- Finance (fees, payments, invoices)
- Library (books, circulation)
- HR (employees, attendance, payroll)
- Analytics (reports, dashboards)

## 🚧 Development

### Running in Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Seed data
python manage.py seed_auth

# Run development server
python manage.py runserver
```

### Running with Docker

```bash
# Start services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Seed data
docker-compose exec web python manage.py seed_auth
```

### Code Style

This project uses:
- **black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run formatters:
```bash
black apps/
isort apps/
flake8 apps/
mypy apps/
```

## 📈 Performance

### Optimization Implemented

- Database query optimization with select_related/prefetch_related
- Pagination for large datasets
- Redis caching (configured)
- Celery for background tasks (configured)

### Performance Targets

- API response time: < 200ms (average)
- Login time: < 3 seconds
- Page load time: < 2 seconds

## 🐛 Troubleshooting

### Common Issues

**Issue: Database connection error**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check DATABASE_URL in .env
echo $DATABASE_URL
```

**Issue: Migration errors**
```bash
# Reset migrations (development only!)
python manage.py migrate --fake-initial

# Or drop and recreate database
dropdb emis_db
createdb emis_db
python manage.py migrate
```

**Issue: Permission denied errors**
```bash
# Re-seed authentication data
python manage.py seed_auth --reset
```

## 📄 License

This project is proprietary software. All rights reserved.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support, email support@emis.edu or create an issue in the repository.

## 🗺️ Roadmap

### Phase 4: Admissions (Planned)
- Application submission
- Document verification
- Merit list generation
- Enrollment workflow

### Phase 5: Course Management (Planned)
- Course creation and management
- Assignment submission
- Grade management
- Attendance tracking

### Phase 6: Finance (Planned)
- Fee structure management
- Payment processing
- Invoice generation
- Financial reports

### Phase 7: Analytics (Planned)
- Dashboard
- Custom reports
- Data export
- Visualizations

---

**Version**: 1.0.0  
**Last Updated**: November 16, 2024  
**Status**: Production Ready ✅
