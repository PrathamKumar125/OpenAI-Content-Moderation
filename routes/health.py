from fastapi import APIRouter, HTTPException
from models.health import HealthCheckResponse
from services.health import (
    check_database_health,
    check_redis_health,
    check_celery_health,
    check_api_health
)
from services.metrics import health_check_requests, health_check_failures
import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Quick health check endpoint"""
    health_check_requests.inc()
    return {"status": "healthy"}

@router.get("/health/ready", response_model=HealthCheckResponse)
async def readiness_check():
    """Detailed health check for all components"""
    health_check_requests.inc()
    
    db_health = await check_database_health()
    redis_health = await check_redis_health()
    celery_health = await check_celery_health()
    api_health = await check_api_health()
    
    # Determine overall status
    components = [db_health, redis_health, celery_health, api_health]
    overall_status = "healthy" if all(c.status == "healthy" for c in components) else "unhealthy"
    
    if overall_status == "unhealthy":
        health_check_failures.inc()
    
    return HealthCheckResponse(
        status=overall_status,
        database=db_health,
        redis=redis_health,
        celery=celery_health,
        api=api_health,
        last_checked=datetime.datetime.now().isoformat()
    )