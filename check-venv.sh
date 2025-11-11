#!/bin/bash

# Check Virtual Environment Setup
echo "🔍 Checking Virtual Environment Setup..."

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment 'venv' not found!"
    echo "   Run: python3 -m venv venv"
    exit 1
fi

# Check if venv is activated
if [[ "$VIRTUAL_ENV" != *"/venv" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "   Run: source venv/bin/activate"
    exit 1
fi

# Check Python executable
PYTHON_PATH=$(which python)
if [[ "$PYTHON_PATH" != *"/venv/bin/python"* ]]; then
    echo "❌ ERROR: Not using virtual environment Python!"
    echo "   Current Python: $PYTHON_PATH"
    exit 1
fi

# Check pip executable
PIP_PATH=$(which pip)
if [[ "$PIP_PATH" != *"/venv/bin/pip"* ]]; then
    echo "❌ ERROR: Not using virtual environment pip!"
    echo "   Current pip: $PIP_PATH"
    exit 1
fi

# Check installed packages location
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")
if [[ "$SITE_PACKAGES" != *"/venv"* ]]; then
    echo "❌ ERROR: Packages not installing in virtual environment!"
    echo "   Site packages: $SITE_PACKAGES"
    exit 1
fi

echo "✅ Virtual environment is properly configured!"
echo "   Python: $PYTHON_PATH"
echo "   Pip: $PIP_PATH"
echo "   Site packages: $SITE_PACKAGES"
