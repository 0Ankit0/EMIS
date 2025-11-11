from typing import Dict, Any
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from src.database import get_db
from src.config import settings


router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "healthy", "service": settings.APP_NAME, "version": settings.APP_VERSION}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Readiness check - verifies all dependencies are available.

    Returns:
        Dict with status of each dependency
    """
    checks = {
        "database": "unknown",
        "redis": "unknown",
    }

    # Check database
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Check Redis
    try:
        redis = Redis.from_url(settings.REDIS_URL, decode_responses=True)
        await redis.ping()
        checks["redis"] = "healthy"
        await redis.aclose()
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"

    # Determine overall status
    all_healthy = all(status == "healthy" for status in checks.values())
    overall_status = "ready" if all_healthy else "not_ready"

    return {
        "status": overall_status,
        "checks": checks,
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check() -> Dict[str, str]:
    """Liveness check - application is running."""
    return {"status": "alive", "service": settings.APP_NAME}
