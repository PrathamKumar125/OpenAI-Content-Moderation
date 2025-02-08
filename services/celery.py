from celery import Celery
from utils.config import get_settings

settings = get_settings()

# Create the Celery instance
celery = Celery(
    "content_moderation",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Configure Celery
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_pool_restarts=True
)

# Import tasks module to ensure tasks are registered
celery.autodiscover_tasks(['services'])

# Export the celery instance
__all__ = ['celery']