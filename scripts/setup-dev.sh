#!/bin/bash

# HabitFlow Development Setup Script
# This script sets up the development environment for HabitFlow

set -e

echo "🚀 Setting up HabitFlow development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create environment file for backend if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend environment file..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env from example. Please update the values as needed."
fi

# Create environment file for frontend if it doesn't exist
if [ ! -f frontend/.env ]; then
    echo "📝 Creating frontend environment file..."
    cat > frontend/.env << EOF
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=HabitFlow
VITE_APP_VERSION=1.0.0
EOF
    echo "✅ Created frontend/.env"
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
if command -v pnpm &> /dev/null; then
    pnpm install
else
    npm install
fi
cd ..

# Start development services
echo "🐳 Starting development services with Docker Compose..."
docker-compose -f infra/docker-compose.yml up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Run database migrations
echo "🗄️ Running database migrations..."
cd backend
source venv/bin/activate
python -c "
from app.core.database import create_tables
import asyncio
asyncio.run(create_tables())
print('Database tables created successfully!')
"
cd ..

echo "✅ Development environment setup complete!"
echo ""
echo "🎉 You can now start the development servers:"
echo "   Backend:  cd backend && source venv/bin/activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"
echo "   Frontend: cd frontend && pnpm run dev"
echo ""
echo "📱 Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔧 To stop services: docker-compose -f infra/docker-compose.yml down"

