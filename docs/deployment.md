# EMIS Deployment Guide

## Overview

This guide covers deploying the EMIS (Education Management Information System) to production environments.

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 6+
- Podman or Docker
- Reverse proxy (Nginx/Apache)

## Environment Setup

### 1. Environment Variables

Create a `.env` file with the following variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=emis.yourdomain.com,www.emis.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/emis_db
USE_PGBOUNCER=True

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ALLOWED_ORIGINS=https://emis.yourdomain.com,https://www.emis.yourdomain.com

# Email (if using)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Monitoring
LOG_LEVEL=INFO
```

### 2. Generate Secret Key

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deployment Options

### Option 1: Podman Deployment (Recommended)

#### Build Image

```bash
podman build -t emis:latest .
```

#### Run with Podman Compose

```bash
# Use podman-compose instead of docker-compose
podman-compose up -d
```

#### Podman Compose File

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: emis_db
      POSTGRES_USER: emis_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  web:
    image: emis:latest
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/uploads
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://emis_user:secure_password@db:5432/emis_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery:
    image: emis:latest
    command: celery -A config worker -l info
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://emis_user:secure_password@db:5432/emis_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  celery-beat:
    image: emis:latest
    command: celery -A config beat -l info
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgresql://emis_user:secure_password@db:5432/emis_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
  static_volume:
  media_volume:
```

### Option 2: Manual Deployment

#### Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Database Setup

```bash
# Create database
sudo -u postgres createdb emis_db
sudo -u postgres createuser emis_user
sudo -u postgres psql -c "ALTER USER emis_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE emis_db TO emis_user;"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

#### Run Application

```bash
# Production server
gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --worker-class sync \
    --timeout 120 \
    --access-logfile logs/access.log \
    --error-logfile logs/error.log
```

#### Run Celery Workers

```bash
# Worker
celery -A config worker -l info --concurrency=4

# Beat scheduler
celery -A config beat -l info
```

## Web Server Configuration

### Nginx Configuration

```nginx
upstream emis_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name emis.yourdomain.com www.emis.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name emis.yourdomain.com www.emis.yourdomain.com;

    ssl_certificate /etc/ssl/certs/emis.crt;
    ssl_certificate_key /etc/ssl/private/emis.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 50M;

    location /static/ {
        alias /path/to/emis/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /path/to/emis/uploads/;
        expires 7d;
    }

    location / {
        proxy_pass http://emis_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

## Database Optimization

### PostgreSQL Configuration

Edit `/etc/postgresql/15/main/postgresql.conf`:

```ini
# Memory
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 16MB
maintenance_work_mem = 128MB

# Connections
max_connections = 100

# Write Ahead Log
wal_buffers = 16MB
checkpoint_completion_target = 0.9
```

### Connection Pooling with PgBouncer

```ini
[databases]
emis_db = host=localhost port=5432 dbname=emis_db

[pgbouncer]
listen_addr = 127.0.0.1
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction
max_client_conn = 100
default_pool_size = 20
```

## Monitoring

### Health Checks

```bash
# Basic health
curl http://localhost:8000/api/v1/health/

# Readiness (DB + Redis)
curl http://localhost:8000/api/v1/readiness/

# Metrics
curl http://localhost:8000/api/v1/metrics/
```

### Log Management

```bash
# View application logs
tail -f logs/emis.log

# View Gunicorn logs
tail -f logs/access.log
tail -f logs/error.log

# View Celery logs
tail -f logs/celery.log
```

## Backup & Recovery

### Database Backup

```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR=/backups/emis
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U emis_user emis_db | gzip > $BACKUP_DIR/emis_db_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "emis_db_*.sql.gz" -mtime +30 -delete
```

### Database Restore

```bash
gunzip < backup.sql.gz | psql -U emis_user emis_db
```

### Media Files Backup

```bash
# Backup uploads directory
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/
```

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure HTTPS/SSL certificates
- [ ] Set proper `ALLOWED_HOSTS`
- [ ] Enable security headers middleware
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Database access restrictions
- [ ] Regular backups
- [ ] Monitor logs for suspicious activity

## Performance Tuning

### Django Settings

```python
# Cache templates in production
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

# Use Redis for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### Gunicorn Workers

```bash
# Formula: (2 * CPU cores) + 1
gunicorn --workers 9  # For 4 CPU cores
```

## Troubleshooting

### Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
```

**Database connection errors:**
- Check DATABASE_URL
- Verify PostgreSQL is running
- Check firewall rules

**Celery tasks not running:**
- Verify Redis is accessible
- Check Celery worker logs
- Ensure beat scheduler is running

**High memory usage:**
- Reduce Gunicorn workers
- Optimize database queries
- Check for memory leaks in custom code

## Support

For deployment issues or questions:
- Email: devops@emis.example.com
- Documentation: https://docs.emis.example.com
