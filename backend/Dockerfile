# Multi-stage Dockerfile for Python backend

# Base stage
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Development stage
FROM base as development

# Copy requirements files
COPY requirements*.txt ./

# Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install flask sqlalchemy psycopg2-binary redis gunicorn
RUN pip install --no-cache-dir -r requirements-dev.txt || \
    pip install pytest pytest-cov black flake8 mypy

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Development command
CMD ["python", "app.py"]

# Test stage
FROM development as test

# Run tests
RUN python -m pytest tests/ --cov=. --cov-report=xml

# Production build stage
FROM base as production-build

# Copy requirements
COPY requirements.txt ./

# Install production dependencies only
RUN pip install --no-cache-dir -r requirements.txt || \
    pip install flask sqlalchemy psycopg2-binary redis gunicorn

# Production stage
FROM python:3.11-slim as production

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from build stage
COPY --from=production-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=production-build /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Production command
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "120", "app:app"]
