#!/bin/bash

echo "🚀 Starting Flight Booking System..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "✅ Flight Booking System is ready!"
echo ""
echo "📍 Access Points:"
echo "   - Client:         http://localhost:5173"
echo "   - Server API:     http://localhost:5000"
echo "   - Flight Service: http://localhost:5001"
echo "   - MySQL DB1:      localhost:3306"
echo "   - MySQL DB2:      localhost:3307"
echo "   - Redis:          localhost:6379"
echo ""
echo "📝 To view logs: docker-compose logs -f"
echo "🛑 To stop: docker-compose down"