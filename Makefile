# Makefile for Gujarati News Translator

.PHONY: help install build start stop clean test lint format

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies for both backend and frontend"
	@echo "  build       - Build Docker containers"
	@echo "  start       - Start the application with Docker Compose"
	@echo "  stop        - Stop the application"
	@echo "  clean       - Clean up containers and volumes"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  dev         - Start development environment"
	@echo "  prod        - Start production environment"

# Install dependencies
install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Build Docker containers
build:
	docker-compose build

# Start development environment
dev:
	docker-compose up --build

# Start production environment
prod:
	docker-compose -f docker-compose.prod.yml up --build -d

# Start the application
start:
	docker-compose up -d

# Stop the application
stop:
	docker-compose down

# Clean up containers and volumes
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Run tests
test:
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v
	@echo "Running frontend tests..."
	cd frontend && npm test -- --coverage --watchAll=false

# Run linting
lint:
	@echo "Linting backend code..."
	cd backend && python -m flake8 app/
	@echo "Linting frontend code..."
	cd frontend && npm run lint

# Format code
format:
	@echo "Formatting backend code..."
	cd backend && python -m black app/
	@echo "Formatting frontend code..."
	cd frontend && npm run format

# Check application health
health:
	@echo "Checking backend health..."
	curl -f http://localhost:8000/health || echo "Backend is not responding"
	@echo "Checking frontend..."
	curl -f http://localhost/ || echo "Frontend is not responding"

# View logs
logs:
	docker-compose logs -f

# Restart services
restart: stop start

# Setup development environment
setup-dev:
	@echo "Setting up development environment..."
	cp backend/.env.example backend/.env
	cp frontend/.env.example frontend/.env
	@echo "Please edit the .env files with your configurations"
	make install

# Deploy to production
deploy:
	@echo "Deploying to production..."
	git pull origin main
	docker-compose -f docker-compose.prod.yml down
	docker-compose -f docker-compose.prod.yml up --build -d
	@echo "Deployment complete!"