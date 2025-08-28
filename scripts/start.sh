#!/bin/bash

# Portfolio Website Startup Script
# This script helps you get started with the portfolio website quickly

set -e  # Exit on any error

echo "🚀 Portfolio Website Startup Script"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Docker and Docker Compose are installed"

# Check if .env file exists
if [ ! -f .env ]; then
    print_warning ".env file not found. Creating from template..."
    if [ -f env.example ]; then
        cp env.example .env
        print_status "Created .env file from env.example"
        print_warning "Please edit .env file with your configuration before proceeding"
        echo "Run: nano .env or vim .env"
        exit 1
    else
        print_error "env.example not found. Please create .env file manually."
        exit 1
    fi
fi

print_status ".env file exists"

# Create necessary directories
mkdir -p data
mkdir -p logs
print_status "Created necessary directories"

# Ask user which environment to start
echo ""
echo "Which environment would you like to start?"
echo "1) Development (SQLite, hot reload)"
echo "2) Production (PostgreSQL, optimized)"
read -p "Enter your choice (1-2): " choice

case $choice in
    1)
        echo ""
        print_status "Starting development environment..."
        docker-compose -f docker-compose.dev.yml up --build -d
        
        # Wait for the service to be ready
        echo "Waiting for the application to start..."
        sleep 10
        
        # Seed database with sample data
        echo ""
        print_status "Seeding database with sample data..."
        docker-compose -f docker-compose.dev.yml exec web python scripts/seed_data.py
        
        echo ""
        print_status "Development environment is ready!"
        echo "🌐 Website: http://localhost:8000"
        echo "📝 To view logs: docker-compose -f docker-compose.dev.yml logs -f"
        echo "🛑 To stop: docker-compose -f docker-compose.dev.yml down"
        ;;
    2)
        echo ""
        print_status "Starting production environment..."
        docker-compose up --build -d
        
        # Wait for the database to be ready
        echo "Waiting for database to be ready..."
        sleep 15
        
        # Run database migrations
        echo ""
        print_status "Running database migrations..."
        docker-compose exec web alembic upgrade head
        
        # Seed database with sample data
        echo ""
        print_status "Seeding database with sample data..."
        docker-compose exec web python scripts/seed_data.py
        
        echo ""
        print_status "Production environment is ready!"
        echo "🌐 Website: http://localhost:80"
        echo "🗄️  Database Admin: http://localhost:8080 (username: portfolio_user, password: portfolio_password)"
        echo "📝 To view logs: docker-compose logs -f"
        echo "🛑 To stop: docker-compose down"
        ;;
    *)
        print_error "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Enjoy your new portfolio website!"
echo ""
echo "Next steps:"
echo "1. Customize your personal information in the templates"
echo "2. Add your GitHub username to .env for repository integration"
echo "3. Configure email settings for the contact form"
echo "4. Add your own projects and content"
echo ""
echo "For more information, check the README.md file."
