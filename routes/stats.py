from fastapi import APIRouter, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from models.moderation import ModerationStats
from services.metrics import moderation_requests, cached_requests, redis_client
from utils.logging import logger

router = APIRouter()

@router.get("/metrics")
async def metrics():
    """Endpoint to expose Prometheus metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@router.get("/stats", response_model=ModerationStats)
async def get_stats():
    """Get moderation service statistics"""
    try:
        total = int(moderation_requests._value.get())
        cached = int(redis_client.get("cached_requests") or 0)
        avg_time = float(redis_client.get("average_response_time") or 0.0)
        
        return ModerationStats(
            total_requests=total,
            cached_requests=cached,
            average_response_time=avg_time
        )
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail="Error fetching statistics")