#!/bin/bash

# MetaLearn Pro Quick Start Script
# This script helps you get started with the MetaLearn Pro platform

set -e

echo "🎓 MetaLearn Pro - Quick Start"
echo "=============================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your configuration (especially OPENAI_API_KEY)"
    echo "   Then run this script again."
    exit 1
fi

# Check for required environment variables
if ! grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "⚠️  Warning: OPENAI_API_KEY not configured in .env"
    echo "   AI features will not work without a valid OpenAI API key"
fi

echo "🐳 Starting services with Docker Compose..."
echo ""

# Start services
docker-compose -f docker-compose.metalearn.yml up -d

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📍 Service URLs:"
echo "   Backend API:          http://localhost:8000"
echo "   API Documentation:    http://localhost:8000/docs"
echo "   AI Tutor Service:     http://localhost:8001"
echo "   Learning Companion:   http://localhost:8002"
echo "   Gamification Engine:  http://localhost:8003"
echo "   Virtual Campus:       http://localhost:8004"
echo "   Analytics:            http://localhost:8005"
echo "   Simulations:          http://localhost:8006"
echo "   Blockchain:           http://localhost:8007"
echo ""
echo "🔍 View logs:"
echo "   docker-compose -f docker-compose.metalearn.yml logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose -f docker-compose.metalearn.yml down"
echo ""
echo "🎉 Happy Learning!"
