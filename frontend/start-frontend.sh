#!/bin/bash
# Startup script for EMIS Frontend

echo "🎓 Starting EMIS Frontend Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please configure .env file with your settings"
fi

# Start Streamlit application
echo "🚀 Starting Streamlit application..."
streamlit run app.py
