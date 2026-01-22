#!/bin/bash

# 🚀 AI Worker Productivity Dashboard - One-Click Startup Script
# This script starts the entire application with a single command

echo "🏭 Starting AI Worker Productivity Dashboard..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Stop any existing containers
echo "🧹 Cleaning up existing containers..."
docker compose down > /dev/null 2>&1

# Build and start containers
echo "🔨 Building containers (this may take a few minutes on first run)..."
docker compose up --build -d

# Wait for backend to be healthy
echo ""
echo "⏳ Waiting for backend to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy!"
        break
    fi
    
    attempt=$((attempt + 1))
    echo "   Attempt $attempt/$max_attempts..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Backend failed to start. Check logs with: docker compose logs backend"
    exit 1
fi

# Seed the database
echo ""
echo "🌱 Seeding database with sample data..."
if curl -X POST "http://localhost:8000/api/admin/seed?clear_existing=true" > /dev/null 2>&1; then
    echo "✅ Database seeded successfully!"
else
    echo "⚠️  Warning: Failed to seed database. You can do this manually later."
fi

# Final status
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✨ Application is running!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "📊 Dashboard:   http://localhost:3000"
echo "🔧 API Docs:    http://localhost:8000/docs"
echo "❤️  Health:      http://localhost:8000/health"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "To stop the application, run: docker compose down"
echo "To view logs, run: docker compose logs -f"
echo ""
