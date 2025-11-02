#!/bin/bash

# Local development - Start REDIS + CELERY (Worker + Beat)

echo "⚙️ Starting Redis and Celery Services (Local Mode)..."

if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

echo "🔧 Activating virtual environment..."
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting services..."
echo "===================="

if ! command -v redis-server &> /dev/null; then
    echo "❌ Redis is not installed!"
    echo ""
    echo "Please install Redis first:"
    echo "  macOS:   brew install redis"
    echo "  Ubuntu:  sudo apt-get install redis-server"
    echo "  Windows: Download from https://redis.io/download"
    exit 1
fi

echo "🔴 Starting Redis..."
redis-server --daemonize yes --port 6379
sleep 2

if redis-cli ping &> /dev/null; then
    echo "✅ Redis is running"
else
    echo "❌ Failed to start Redis"
    exit 1
fi

echo "📅 Starting Celery Beat..."
celery -A celery_tasks.celery beat -l info &
BEAT_PID=$!

echo "⚙️ Starting Celery Worker..."
echo ""
celery -A celery_tasks.celery worker -l info -Q celery

echo ""
echo "🛑 Stopping services..."
kill $BEAT_PID 2>/dev/null

# Stop Redis
echo "🔴 Stopping Redis..."
redis-cli shutdown 2>/dev/null

wait
echo "✅ All services stopped"
