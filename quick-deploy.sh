#!/bin/bash

# ================================================
# BTEC Platform - Quick Deploy Script
# ================================================

set -e

echo "🚀 BTEC Smart Platform - Quick Deploy"
echo "======================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Copying from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created. Please edit it before continuing.${NC}"
    exit 1
fi

# Function to check if a command exists in PATH
# Usage: command_exists <command_name>  
# Returns: 0 if exists, 1 if not
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo ""
echo "📋 Checking prerequisites..."

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.11+${NC}"
    exit 1
fi

if ! command_exists flutter; then
    echo -e "${RED}❌ Flutter not found. Please install Flutter 3.0+${NC}"
    exit 1
fi

if ! command_exists docker; then
    echo -e "${YELLOW}⚠️  Docker not found. Docker deployment won't be available.${NC}"
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Ask deployment type
echo ""
echo "📦 Select deployment type:"
echo "1) Local Development"
echo "2) Docker Deployment"
echo "3) Production Build Only"
read -p "Enter choice [1-3]: " deploy_choice

case $deploy_choice in
    1)
        echo ""
        echo "🔧 Setting up Local Development..."
        
        # Backend setup
        echo ""
        echo "📦 Setting up Backend..."
        cd backend
        
        if ! command_exists uv; then
            echo "Installing UV..."
            pip install uv
        fi
        
        echo "Syncing dependencies..."
        uv sync
        
        echo -e "${GREEN}✅ Backend setup complete${NC}"
        
        # Frontend setup
        echo ""
        echo "📱 Setting up Frontend..."
        cd ../Flutter
        
        echo "Getting Flutter dependencies..."
        flutter pub get
        
        echo -e "${GREEN}✅ Frontend setup complete${NC}"
        
        # Instructions
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}✅ Setup Complete!${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo "To start development:"
        echo ""
        echo "Terminal 1 (Backend):"
        echo "  cd backend"
        echo "  uv run fastapi dev app/main.py"
        echo ""
        echo "Terminal 2 (Frontend):"
        echo "  cd Flutter"
        echo "  flutter run -d chrome"
        echo ""
        ;;
        
    2)
        echo ""
        echo "🐳 Deploying with Docker..."
        
        if ! command_exists docker; then
            echo -e "${RED}❌ Docker is required for this option${NC}"
            exit 1
        fi
        
        echo "Building and starting containers..."
        docker-compose -f docker-compose.prod.yml up --build -d
        
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}✅ Docker Deployment Complete!${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo "Services running:"
        echo "  - Frontend: http://localhost"
        echo "  - Backend:  http://localhost:8000"
        echo "  - Database: localhost:5432"
        echo ""
        echo "To view logs:"
        echo "  docker-compose -f docker-compose.prod.yml logs -f"
        echo ""
        echo "To stop:"
        echo "  docker-compose -f docker-compose.prod.yml down"
        echo ""
        ;;
        
    3)
        echo ""
        echo "🏗️  Building for Production..."
        
        # Build Backend
        echo ""
        echo "📦 Building Backend..."
        cd backend
        uv sync
        echo -e "${GREEN}✅ Backend built${NC}"
        
        # Build Frontend
        echo ""
        echo "📱 Building Flutter Web..."
        cd ../Flutter
        flutter build web --release
        echo -e "${GREEN}✅ Flutter Web built → build/web/${NC}"
        
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}✅ Production Build Complete!${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        echo "Build artifacts:"
        echo "  - Flutter Web: Flutter/build/web/"
        echo ""
        echo "Next steps:"
        echo "  1. Deploy backend to Render/Railway/Azure"
        echo "  2. Deploy frontend (build/web/) to Netlify/Vercel"
        echo "  3. Configure environment variables"
        echo "  4. Test end-to-end"
        echo ""
        ;;
        
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Done!${NC}"
