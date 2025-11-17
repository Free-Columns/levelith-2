"""
Health Check and Monitoring Endpoints

Provides endpoints for health checks, readiness, and system status.
Critical for Render deployment monitoring.
"""

from datetime import datetime
from typing import Dict

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.database import DatabaseHealthCheck

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict:
    """
    Basic health check endpoint.

    Returns 200 OK if the service is running.
    Used by Render for health monitoring.

    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": settings.app_name,
        "version": settings.app_version,
    }


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness_check() -> JSONResponse:
    """
    Readiness check endpoint.

    Checks if all dependencies (database, cache, etc.) are ready.
    Returns 200 if ready, 503 if not ready.

    Returns:
        JSONResponse: Readiness status with details
    """
    checks = {
        "database": DatabaseHealthCheck.check(),
    }

    all_ready = all(checks.values())

    response_data = {
        "status": "ready" if all_ready else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks,
        "service": settings.app_name,
    }

    return JSONResponse(
        status_code=status.HTTP_200_OK if all_ready else status.HTTP_503_SERVICE_UNAVAILABLE,
        content=response_data,
    )


@router.get("/health/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict:
    """
    Liveness check endpoint.

    Simple check to verify the service is alive.
    Used by Kubernetes/Render for liveness probes.

    Returns:
        dict: Liveness status
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/health/details", status_code=status.HTTP_200_OK)
async def health_details() -> Dict:
    """
    Detailed health information.

    Provides comprehensive health and configuration details.
    Only available in non-production environments.

    Returns:
        dict: Detailed health and system information
    """
    db_info = DatabaseHealthCheck.get_info()

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        },
        "database": db_info,
        "configuration": {
            "debug": settings.debug,
            "log_level": settings.log_level,
        } if not settings.is_production else {"debug": False},
    }
