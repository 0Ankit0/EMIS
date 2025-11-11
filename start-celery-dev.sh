#!/bin/bash

# Celery Worker for Development Mode
echo "🔧 Starting Celery Worker in Development Mode..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "�� Creating .env from .env.development..."
    cp .env.development .env
fi

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./start-dev.sh first!"
    exit 1
fi

source venv/bin/activate

# Start Celery worker
echo "🚀 Starting Celery worker..."
celery -A src.tasks.worker worker --loglevel=info
