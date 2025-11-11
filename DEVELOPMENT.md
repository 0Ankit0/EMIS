# EMIS Development Guide

This guide explains how to run the EMIS backend in different modes.

## Prerequisites

### Development Mode
- Python 3.11+
- PostgreSQL 15+ (installed locally)
- Redis (installed locally)

### Production Mode
- Docker or Podman
- Docker Compose or Podman Compose

## Quick Start

### Development Mode (Local)

Development mode uses your local PostgreSQL and Redis installations.

```bash
# Start the backend server
./start-dev.sh
```

This will:
1. Check if PostgreSQL and Redis are running (start them if needed)
2. Create a virtual environment (if it doesn't exist)
3. Install dependencies
4. Run database migrations
5. Start the FastAPI server with hot reload on http://localhost:8000

**To run Celery workers** (in a separate terminal):
```bash
./start-celery-dev.sh
```

### Production Mode (Docker)

Production mode runs everything in Docker/Podman containers.

```bash
# Start all services in Docker
./start-prod.sh
```

This will:
1. Build Docker images
2. Start PostgreSQL, Redis, Celery workers, and the FastAPI app
3. Run all services in containers

## Environment Files

- `.env.development` - Development configuration (local services)
- `.env.production` - Production configuration (Docker services)
- `.env` - Active configuration (created from above files)

## Database Setup (Development Mode)

### Create PostgreSQL Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE emis_db;
CREATE USER emis_user WITH PASSWORD 'emis_password';
GRANT ALL PRIVILEGES ON DATABASE emis_db TO emis_user;
\q
```

### Install Redis

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Check if Redis is running
redis-cli ping
# Should return: PONG
```

## Available Scripts

| Script | Purpose |
|--------|---------|
| `./start-dev.sh` | Start backend in development mode (local PostgreSQL/Redis) |
| `./start-prod.sh` | Start backend in production mode (Docker containers) |
| `./start-celery-dev.sh` | Start Celery worker in development mode |

## Accessing Services

### Development Mode
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Production Mode
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- PostgreSQL: localhost:5433 (mapped from container)
- Redis: localhost:6379

## Useful Commands

### Development Mode

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description"

# Start server manually
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# Run tests
pytest
```

### Production Mode

```bash
# View logs
podman-compose logs -f        # or docker-compose logs -f

# Stop services
podman-compose down           # or docker-compose down

# Restart services
podman-compose restart        # or docker-compose restart

# Rebuild containers
podman-compose build          # or docker-compose build

# Run migrations in container
podman-compose exec app alembic upgrade head
```

## Switching Between Modes

To switch from development to production:
```bash
cp .env.production .env
./start-prod.sh
```

To switch from production to development:
```bash
cp .env.development .env
./start-dev.sh
```

## Troubleshooting

### Development Mode

**PostgreSQL not starting:**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

**Redis not starting:**
```bash
sudo systemctl status redis-server
sudo systemctl start redis-server
```

**Port already in use:**
```bash
# Find process using port 8000
sudo lsof -i :8000
# Kill the process
kill -9 <PID>
```

### Production Mode

**Containers not starting:**
```bash
# Check container status
podman ps -a  # or docker ps -a

# View container logs
podman logs emis-app  # or docker logs emis-app
```

**Port conflicts:**
```bash
# Change ports in docker-compose.yml
# PostgreSQL: 5433 (host) -> 5432 (container)
# Redis: 6379 (host) -> 6379 (container)
# API: 8000 (host) -> 8000 (container)
```

## Security Notes

- **NEVER** commit `.env` files to git
- Change default passwords in production
- Update `SECRET_KEY` and `JWT_SECRET_KEY` in `.env.production`
- Use strong passwords for PostgreSQL
- Enable SSL/TLS in production
