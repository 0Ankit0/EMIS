FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads staticfiles logs

# Collect static files
RUN python manage.py collectstatic --no-input || true

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate && \
    gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
