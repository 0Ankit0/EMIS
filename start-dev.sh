#!/bin/bash

# Development Mode Startup Script
echo "🚀 Starting EMIS in Development Mode..."

# Check if .env file exists, if not copy from .env.development
if [ ! -f .env ]; then
    echo "📋 Creating .env from .env.development..."
    cp .env.development .env
else
    echo "⚠️  .env file already exists. Using existing configuration."
    echo "   To use development settings, run: cp .env.development .env"
fi

# Check if PostgreSQL is running
echo "🔍 Checking PostgreSQL..."
if ! sudo systemctl is-active --quiet postgresql; then
    echo "🔧 Starting PostgreSQL..."
    sudo systemctl start postgresql
else
    echo "✅ PostgreSQL is running"
fi

# Check if Redis is running
echo "🔍 Checking Redis..."
if ! sudo systemctl is-active --quiet redis-server && ! sudo systemctl is-active --quiet redis; then
    echo "🔧 Starting Redis..."
    sudo systemctl start redis-server 2>/dev/null || sudo systemctl start redis 2>/dev/null || echo "⚠️  Redis service not found. Please start it manually."
else
    echo "✅ Redis is running"
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Verify virtual environment setup
echo "✓ Verifying virtual environment..."
./check-venv.sh || exit 1

# Install/update dependencies (only in virtual environment)
echo "📚 Installing dependencies in virtual environment..."
pip install -r requirements.txt --quiet

# Run database migrations (in virtual environment)
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

# Start the application (in virtual environment)
echo "🎯 Starting Django server on http://localhost:8000"
echo "📖 Admin Panel: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"
python manage.py runserver 0.0.0.0:8000
