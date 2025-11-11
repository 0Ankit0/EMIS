#!/bin/bash
# EMIS Setup Script
# This script helps set up the EMIS development environment

set -e

echo "🚀 EMIS Setup Script"
echo "===================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3.11+ required"; exit 1; }

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📥 Installing dependencies..."
CC=gcc pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start services: podman-compose up -d postgres redis"
echo "2. Run migrations: alembic upgrade head"
echo "3. Start app: uvicorn src.app:app --reload"
echo ""
echo "Always activate venv first: source venv/bin/activate"
