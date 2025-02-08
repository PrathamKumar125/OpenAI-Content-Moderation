from prometheus_client import Counter, Histogram
from redis import Redis
from utils.config import get_settings

settings = get_settings()
redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

# Health check metrics
health_check_requests = Counter("health_check_requests", "Number of health check requests")
health_check_failures = Counter("health_check_failures", "Number of failed health checks")

# Moderation metrics
moderation_requests = Counter("moderation_requests", "Number of moderation requests")
moderation_failures = Counter("moderation_failures", "Number of failed moderation requests")
moderation_latency = Histogram("moderation_latency_seconds", "Time spent processing moderation requests")
cached_requests = Counter("cached_requests", "Number of cached moderation requests")