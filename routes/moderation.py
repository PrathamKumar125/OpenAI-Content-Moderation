from fastapi import APIRouter, HTTPException
from models.moderation import ModerationRequest, ImageModerationRequest, ContentItem
from services.tasks import moderate_text_task, moderate_content_task
from services.celery import celery
from services.metrics import moderation_requests

router = APIRouter()

@router.post("/text")
async def moderate_text(request: ModerationRequest):
    moderation_requests.inc()
    task = moderate_text_task.delay(request.text)
    return {"id": task.id, "status": "processing"}

@router.post("/image")
async def moderate_image(request: ImageModerationRequest):
    if not (request.image_url or request.image_base64):
        raise HTTPException(
            status_code=400,
            detail="Either image_url or image_base64 must be provided"
        )
    
    image_url = request.image_url or request.image_base64
    if not image_url.startswith(('http://', 'https://', 'data:image/')):
        raise HTTPException(
            status_code=400,
            detail="Invalid image URL format"
        )
    
    content_item = ContentItem(
        type="image_url",
        image_url=image_url
    ).dict()
    
    moderation_requests.inc()
    task = moderate_content_task.delay([content_item])
    return {"id": task.id, "status": "processing"}

@router.get("/{task_id}")
async def get_moderation_result(task_id: str):
    result = celery.AsyncResult(task_id)
    if result.ready():
        return {"status": "completed", "result": result.get()}
    return {"status": "processing"}