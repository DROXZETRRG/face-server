# Scripts for development and testing

# Start development server
dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start all services with Docker Compose
up:
	docker-compose up -d

# Build and start services
up-build:
	docker-compose up -d --build

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Run database migrations
migrate:
	alembic upgrade head

# Create a new migration
migration:
	alembic revision --autogenerate -m "$(message)"

# Rollback last migration
rollback:
	alembic downgrade -1

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-coverage:
	pytest tests/ -v --cov=app --cov-report=html

# Format code
format:
	black app/ tests/
	isort app/ tests/

# Lint code
lint:
	ruff app/ tests/

# Clean up Python cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Install dependencies
install:
	uv pip install -e .

# Install with development dependencies
install-dev:
	uv pip install -e ".[dev]"

# Setup development environment
setup:
	python setup_dev.py

# Help
help:
	@echo "Available commands:"
	@echo "  make dev           - Start development server (local, uses uv)"
	@echo "  make up            - Start Docker services (uses pip)"
	@echo "  make up-build      - Build and start Docker services"
	@echo "  make down          - Stop Docker services"
	@echo "  make logs          - View Docker logs"
	@echo "  make install       - Install dependencies with uv (local dev)"
	@echo "  make install-dev   - Install with dev dependencies"
	@echo "  make test          - Run tests"
	@echo "  make migrate       - Run database migrations"
	@echo "  make clean         - Clean Python cache files"

.PHONY: dev up up-build down logs migrate migration rollback test test-coverage format lint clean install install-dev setup help
