#!/bin/bash

# Local development - Start BOT only + Redis

echo "🤖 Starting Telegram Bot (Local Mode)..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Virtual environment not found. Creating..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Start Redis
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

echo ""
echo "🚀 Starting Telegram Bot..."
echo "===================="
python -m telegram.main
