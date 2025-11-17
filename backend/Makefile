# Backend Makefile
.PHONY: help install dev-install test lint format clean run migrate docker-build docker-run

PYTHON := python3
PIP := $(PYTHON) -m pip
VENV := venv
APP_NAME := levelith-backend
PORT := 8000

# Colors for terminal output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install production dependencies
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt || $(PIP) install flask sqlalchemy psycopg2-binary redis gunicorn

dev-install: install ## Install development dependencies
	$(PIP) install -r requirements-dev.txt || $(PIP) install pytest pytest-cov pytest-asyncio black flake8 mypy pre-commit

venv: ## Create virtual environment
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)Virtual environment created. Activate with: source $(VENV)/bin/activate$(NC)"

test: ## Run all tests
	pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html

test-unit: ## Run unit tests only
	pytest tests/unit -v --cov=. --cov-report=term-missing

test-integration: ## Run integration tests only
	pytest tests/integration -v

test-watch: ## Run tests in watch mode
	ptw tests/ -- -v

lint: ## Run linting checks
	@echo "$(YELLOW)Running black...$(NC)"
	black --check .
	@echo "$(YELLOW)Running flake8...$(NC)"
	flake8 .
	@echo "$(YELLOW)Running mypy...$(NC)"
	mypy .

format: ## Auto-format code
	black .
	isort .

security: ## Run security checks
	bandit -r . -f json -o security-report.json
	safety check --json
	@echo "$(GREEN)Security scan complete. Check security-report.json$(NC)"

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf dist/
	rm -rf *.egg-info

migrate: ## Run database migrations
	$(PYTHON) manage.py db upgrade

migrate-create: ## Create a new migration
	@read -p "Enter migration message: " msg; \
	$(PYTHON) manage.py db migrate -m "$$msg"

db-reset: ## Reset database (WARNING: destroys all data)
	$(PYTHON) manage.py db downgrade base
	$(PYTHON) manage.py db upgrade

run: ## Run development server
	$(PYTHON) app.py || flask run --host=0.0.0.0 --port=$(PORT)

run-prod: ## Run production server with gunicorn
	gunicorn -w 4 -b 0.0.0.0:$(PORT) app:app

docker-build: ## Build Docker image
	docker build -t $(APP_NAME) .

docker-run: docker-build ## Run Docker container
	docker run -p $(PORT):$(PORT) \
		-e DATABASE_URL=$${DATABASE_URL:-postgresql://localhost/levelith} \
		-e REDIS_URL=$${REDIS_URL:-redis://localhost:6379} \
		$(APP_NAME)

docker-compose-up: ## Start all services with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop all services
	docker-compose down

ci-local: ## Run CI pipeline locally
	@echo "$(YELLOW)Running local CI pipeline...$(NC)"
	@make lint
	@make test
	@make security
	@echo "$(GREEN)Local CI pipeline complete!$(NC)"

setup-hooks: ## Setup git pre-commit hooks
	pre-commit install
	@echo "$(GREEN)Pre-commit hooks installed$(NC)"

api-docs: ## Generate API documentation
	python -m pdoc --html --output-dir docs/api .

requirements-update: ## Update requirements files
	pip-compile requirements.in
	pip-compile requirements-dev.in

shell: ## Open Python shell with app context
	$(PYTHON) manage.py shell || $(PYTHON) -i -c "from app import *"

.DEFAULT_GOAL := help
