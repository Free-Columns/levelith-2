# Root Makefile for Levelith-2 Project
.PHONY: help install test lint format clean build deploy ci setup

# Variables
BACKEND_DIR := backend
FRONTEND_DIR := frontend
DEV_DIR := dev
DOCKER_COMPOSE := docker-compose
DOCKER_COMPOSE_TEST := docker-compose -f docker-compose.test.yml

# Colors for terminal output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(GREEN)Levelith-2 Project Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

# === SETUP COMMANDS ===
setup: ## Initial project setup
	@echo "$(BLUE)Setting up Levelith-2 project...$(NC)"
	@make install
	@make setup-hooks
	@make generate-context-nodes
	@echo "$(GREEN)Setup complete!$(NC)"

install: ## Install all dependencies
	@echo "$(YELLOW)Installing backend dependencies...$(NC)"
	cd $(BACKEND_DIR) && make install
	@echo "$(YELLOW)Installing frontend dependencies...$(NC)"
	cd $(FRONTEND_DIR) && npm install
	@echo "$(GREEN)All dependencies installed!$(NC)"

setup-hooks: ## Setup git hooks
	pip install pre-commit
	pre-commit install
	@echo "$(GREEN)Git hooks installed!$(NC)"

# === CONTEXT NODE MANAGEMENT ===
generate-context-nodes: ## Generate context nodes for the project
	@echo "$(BLUE)Generating context nodes...$(NC)"
	python $(DEV_DIR)/cn-create.py

validate-context-nodes: ## Validate context nodes
	@echo "$(BLUE)Validating context nodes...$(NC)"
	python $(DEV_DIR)/cn-validate.py

update-context-nodes: ## Update context nodes completeness
	@echo "$(BLUE)Checking context node completeness...$(NC)"
	python $(DEV_DIR)/cn-validate.py --check-completeness

# === DEVELOPMENT COMMANDS ===
dev: ## Start development environment
	@echo "$(BLUE)Starting development environment...$(NC)"
	$(DOCKER_COMPOSE) up

dev-backend: ## Start backend development server
	cd $(BACKEND_DIR) && make run

dev-frontend: ## Start frontend development server
	cd $(FRONTEND_DIR) && npm run dev

build: ## Build all services
	@echo "$(BLUE)Building all services...$(NC)"
	$(DOCKER_COMPOSE) build

# === TESTING COMMANDS ===
test: ## Run all tests
	@echo "$(YELLOW)Running all tests...$(NC)"
	@make test-backend
	@make test-frontend
	@make test-integration
	@echo "$(GREEN)All tests passed!$(NC)"

test-backend: ## Run backend tests
	@echo "$(YELLOW)Running backend tests...$(NC)"
	cd $(BACKEND_DIR) && make test

test-frontend: ## Run frontend tests
	@echo "$(YELLOW)Running frontend tests...$(NC)"
	cd $(FRONTEND_DIR) && npm test

test-integration: ## Run integration tests
	@echo "$(YELLOW)Running integration tests...$(NC)"
	$(DOCKER_COMPOSE_TEST) up --abort-on-container-exit
	$(DOCKER_COMPOSE_TEST) down

test-e2e: ## Run E2E tests
	@echo "$(YELLOW)Running E2E tests...$(NC)"
	cd $(FRONTEND_DIR) && npm run test:e2e

test-ci: ## Run CI test suite
	@echo "$(YELLOW)Running CI test suite...$(NC)"
	$(DOCKER_COMPOSE_TEST) up --abort-on-container-exit --exit-code-from integration-test
	$(DOCKER_COMPOSE_TEST) down

# === CODE QUALITY ===
lint: ## Run linters on all code
	@echo "$(YELLOW)Linting code...$(NC)"
	cd $(BACKEND_DIR) && make lint
	cd $(FRONTEND_DIR) && npm run lint
	@echo "$(GREEN)Linting complete!$(NC)"

format: ## Format all code
	@echo "$(YELLOW)Formatting code...$(NC)"
	cd $(BACKEND_DIR) && make format
	cd $(FRONTEND_DIR) && npm run format
	@echo "$(GREEN)Formatting complete!$(NC)"

security: ## Run security scans
	@echo "$(YELLOW)Running security scans...$(NC)"
	cd $(BACKEND_DIR) && make security
	cd $(FRONTEND_DIR) && npm audit
	@echo "$(GREEN)Security scan complete!$(NC)"

# === CI/CD COMMANDS ===
ci: ## Run full CI pipeline locally
	@echo "$(BLUE)Running CI pipeline...$(NC)"
	@make validate-context-nodes
	@make lint
	@make test
	@make security
	@make build
	@echo "$(GREEN)CI pipeline complete!$(NC)"

ci-backend: ## Run backend CI
	cd $(BACKEND_DIR) && make ci-local

ci-frontend: ## Run frontend CI
	cd $(FRONTEND_DIR) && npm run ci

# === DOCKER COMMANDS ===
docker-build: ## Build Docker images
	$(DOCKER_COMPOSE) build

docker-up: ## Start Docker containers
	$(DOCKER_COMPOSE) up -d

docker-down: ## Stop Docker containers
	$(DOCKER_COMPOSE) down

docker-logs: ## Show Docker logs
	$(DOCKER_COMPOSE) logs -f

docker-clean: ## Clean Docker resources
	$(DOCKER_COMPOSE) down -v
	docker system prune -f

# === DATABASE COMMANDS ===
db-migrate: ## Run database migrations
	cd $(BACKEND_DIR) && make migrate

db-reset: ## Reset database
	cd $(BACKEND_DIR) && make db-reset

db-shell: ## Open database shell
	$(DOCKER_COMPOSE) exec db psql -U postgres -d levelith

# === DEPLOYMENT ===
deploy-staging: ## Deploy to staging
	@echo "$(BLUE)Deploying to staging...$(NC)"
	# Add staging deployment commands
	@echo "$(GREEN)Deployed to staging!$(NC)"

deploy-production: ## Deploy to production
	@echo "$(RED)Deploying to production...$(NC)"
	@echo "$(YELLOW)Are you sure? [y/N]$(NC)"
	@read -r response; \
	if [ "$$response" = "y" ]; then \
		echo "$(BLUE)Deploying...$(NC)"; \
		# Add production deployment commands; \
		echo "$(GREEN)Deployed to production!$(NC)"; \
	else \
		echo "$(YELLOW)Deployment cancelled$(NC)"; \
	fi

# === UTILITIES ===
clean: ## Clean all generated files
	@echo "$(YELLOW)Cleaning project...$(NC)"
	cd $(BACKEND_DIR) && make clean
	cd $(FRONTEND_DIR) && npm run clean
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov/ .coverage .pytest_cache/
	@echo "$(GREEN)Project cleaned!$(NC)"

logs: ## Show application logs
	$(DOCKER_COMPOSE) logs -f backend frontend

shell-backend: ## Open backend shell
	$(DOCKER_COMPOSE) exec backend /bin/sh

shell-frontend: ## Open frontend shell
	$(DOCKER_COMPOSE) exec frontend /bin/sh

status: ## Show project status
	@echo "$(BLUE)Project Status:$(NC)"
	@echo "$(YELLOW)Docker Status:$(NC)"
	@$(DOCKER_COMPOSE) ps
	@echo "\n$(YELLOW)Git Status:$(NC)"
	@git status --short
	@echo "\n$(YELLOW)Context Nodes:$(NC)"
	@python $(DEV_DIR)/cn-validate.py --check-completeness

version: ## Show versions
	@echo "$(BLUE)Component Versions:$(NC)"
	@echo "Python: $$(python --version)"
	@echo "Node: $$(node --version)"
	@echo "Docker: $$(docker --version)"
	@echo "Docker Compose: $$(docker-compose --version)"

.DEFAULT_GOAL := help
