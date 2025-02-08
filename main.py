from fastapi import FastAPI
import redis

from db.models import Base
from db.session import engine, test_db_connection
from routes import health, metrics, moderation,stats
from utils.config import get_settings
from utils.logging import logger
from services.celery import celery

settings = get_settings()

app = FastAPI(title="Content Moderation Service")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(stats.router, prefix="/api/v1", tags=["stats"])
app.include_router(metrics.router, prefix="/api/v1", tags=["metrics"])
app.include_router(moderation.router, prefix="/api/v1/moderate", tags=["moderation"])

# Configure Redis
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

@app.on_event("startup")
async def startup_event():
    test_db_connection()
    try:
        redis_client.ping()
        logger.info("Successfully connected to Redis")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)