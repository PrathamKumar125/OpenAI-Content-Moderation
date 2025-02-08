from services.celery import celery
from services.moderation import ModerationService
from services.metrics import moderation_latency, cached_requests, redis_client
from db.session import SessionLocal
from utils.logging import logger
from db.models import ModerationResult
import json
import time

moderation_service = ModerationService()

@celery.task
def moderate_text_task(text: str):
    db = SessionLocal()
    start_time = time.time()
    
    try:
        # Check cache
        cache_key = f"moderation:{text}"
        cached_result = redis_client.get(cache_key)
        
        if cached_result:
            logger.info(f"Cache hit for text: {text}")
            cached_requests.inc()
            return json.loads(cached_result)
        
        # Process moderation
        result = moderation_service.moderate_content(text)
        
        # Update metrics
        processing_time = time.time() - start_time
        moderation_latency.observe(processing_time)
        
        # Update average response time
        current_avg = float(redis_client.get("average_response_time") or 0.0)
        total_requests = int(redis_client.get("total_requests") or 0)
        new_avg = ((current_avg * total_requests) + processing_time) / (total_requests + 1)
        redis_client.set("average_response_time", new_avg)
        redis_client.incr("total_requests")
        
        # Cache result
        redis_client.setex(cache_key, 3600, json.dumps(result))
        
        # Store in database
        moderation_entry = ModerationResult(
            text=text,
            result=json.dumps(result)
        )
        db.add(moderation_entry)
        db.commit()
        
        return result
    except Exception as e:
        logger.error(f"Error moderating text: {str(e)}")
        return {"error": str(e)}
    finally:
        db.close()

@celery.task
def moderate_content_task(content_items):
    db = SessionLocal()
    
    try:
        result = moderation_service.moderate_content(content_items)
        
        # Store in database
        for item in content_items:
            content_text = item.get('text') or item.get('image_url')
            if content_text:
                moderation_entry = ModerationResult(
                    text=content_text,
                    result=json.dumps(result)
                )
                db.add(moderation_entry)
        
        db.commit()
        return result
    except Exception as e:
        logger.error(f"Error moderating content: {str(e)}")
        return {"error": str(e)}
    finally:
        db.close()