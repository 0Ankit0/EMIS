#!/bin/bash

# Production Mode Startup Script
echo "🚀 Starting EMIS in Production Mode (Docker)..."

# Check if .env file exists, if not copy from .env.production
if [ ! -f .env ]; then
    echo "📋 Creating .env from .env.production..."
    cp .env.production .env
    echo "⚠️  WARNING: Update .env with production secrets!"
else
    echo "✅ Using existing .env file"
fi

# Check if using Docker or Podman
if command -v podman &> /dev/null; then
    CONTAINER_CMD="podman-compose"
    echo "🐳 Using Podman Compose"
elif command -v docker &> /dev/null; then
    CONTAINER_CMD="docker-compose"
    echo "🐳 Using Docker Compose"
else
    echo "❌ Error: Neither Docker nor Podman found!"
    echo "   Please install Docker or Podman to run in production mode."
    exit 1
fi

# Stop any running containers
echo "🛑 Stopping existing containers..."
$CONTAINER_CMD down 2>/dev/null || true

# Build and start containers
echo "🔨 Building containers..."
$CONTAINER_CMD build

echo "🚀 Starting all services..."
$CONTAINER_CMD up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check service status
echo ""
echo "📊 Service Status:"
$CONTAINER_CMD ps

echo ""
echo "✅ EMIS is running in production mode!"
echo "🎯 API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "🗄️  PostgreSQL: localhost:5433"
echo "🔴 Redis: localhost:6379"
echo ""
echo "📝 View logs: $CONTAINER_CMD logs -f"
echo "🛑 Stop services: $CONTAINER_CMD down"
echo "🔄 Restart services: $CONTAINER_CMD restart"
