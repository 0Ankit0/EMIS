# 🚀 EMIS Quick Start Guide

## Choose Your Mode

### Development Mode (Local)

Development mode uses your local PostgreSQL and Redis installations.

```bash
# Start the backend server
./start-dev.sh
```

**Important:** All Python packages are installed only in a virtual environment (`venv/`) to avoid conflicts with system packages.

**Features:**
- ✅ Hot reload enabled
- ✅ Debug mode on
- ✅ Uses local database
- ✅ Fast startup
- ✅ Easy debugging
- ✅ Isolated virtual environment

---

### �� Production Mode (Docker/Podman)
Runs everything in containers - isolated and production-ready.

```bash
./start-prod.sh
```

**Features:**
- ✅ Fully containerized
- ✅ Production settings
- ✅ Isolated environment
- ✅ Easy deployment
- ✅ Includes all services (PostgreSQL, Redis, Celery)

---

## First Time Setup

### Development Mode Setup

1. **Install PostgreSQL:**
   ```bash
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

2. **Create Database:**
   ```bash
   sudo -u postgres psql
   ```
   
   In PostgreSQL shell:
   ```sql
   CREATE DATABASE emis_db;
   CREATE USER emis_user WITH PASSWORD 'emis_password';
   GRANT ALL PRIVILEGES ON DATABASE emis_db TO emis_user;
   \q
   ```

3. **Install Redis:**
   ```bash
   sudo apt install redis-server
   sudo systemctl start redis-server
   sudo systemctl enable redis-server
   ```

4. **Start the application:**
   ```bash
   ./start-dev.sh
   ```

### Production Mode Setup

1. **Install Docker/Podman:**
   ```bash
   # For Podman (already installed on your system)
   sudo apt install podman-compose
   
   # OR for Docker
   sudo apt install docker.io docker-compose
   ```

2. **Start the application:**
   ```bash
   ./start-prod.sh
   ```

---

## Accessing the Application

Once started, access:
- 🌐 **API**: http://localhost:8000
- 📖 **API Documentation**: http://localhost:8000/docs
- 🔍 **ReDoc**: http://localhost:8000/redoc

---

## Additional Services

### Run Celery Worker (Development Mode)
In a **new terminal**:
```bash
./start-celery-dev.sh
```

---

## Stopping the Application

### Development Mode
Press `Ctrl+C` in the terminal

### Production Mode
```bash
podman-compose down
# or
docker-compose down
```

---

## Need Help?

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed documentation.

---

## File Structure

```
.
├── start-dev.sh              # Start in development mode
├── start-prod.sh             # Start in production mode (Docker)
├── start-celery-dev.sh       # Start Celery worker (dev)
├── .env.development          # Development environment config
├── .env.production           # Production environment config
├── .env                      # Active config (auto-generated)
└── DEVELOPMENT.md            # Detailed documentation
```
