from models.health import ComponentHealth
from db.session import engine
from utils.config import get_settings
from sqlalchemy import text
from celery.app.control import Control
from utils.celeryconfig import celery_app
import redis

settings = get_settings()
redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def check_database_health() -> ComponentHealth:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return ComponentHealth(status="healthy")
    except Exception as e:
        return ComponentHealth(status="unhealthy", details=str(e))

async def check_redis_health() -> ComponentHealth:
    try:
        redis_client.ping()
        return ComponentHealth(status="healthy")
    except Exception as e:
        return ComponentHealth(status="unhealthy", details=str(e))

async def check_celery_health() -> ComponentHealth:
    try:
        i = celery_app.control.inspect()
        if not i.active():
            return ComponentHealth(status="unhealthy", details="No active Celery workers")
        return ComponentHealth(status="healthy")
    except Exception as e:
        return ComponentHealth(status="unhealthy", details=str(e))

async def check_api_health() -> ComponentHealth:
    try:
        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-api-key":
            return ComponentHealth(status="unhealthy", details="OpenAI API key not configured")
        return ComponentHealth(status="healthy")
    except Exception as e:
        return ComponentHealth(status="unhealthy", details=str(e))