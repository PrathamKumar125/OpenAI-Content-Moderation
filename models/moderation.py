from pydantic import BaseModel
from typing import Optional, List

class ModerationRequest(BaseModel):
    text: str

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a sample text to moderate"
            }
        }

class ImageModerationRequest(BaseModel):
    text: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a sample text to moderate",
                "image_url": "https://example.com/image.jpg"
            }
        }

class ContentItem(BaseModel):
    type: str
    text: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "type": "text",
                "text": "Sample text content"
            },
            "examples": [
                {
                    "type": "text",
                    "text": "Sample text content"
                },
                {
                    "type": "image_url",
                    "image_url": "https://example.com/image.jpg"
                }
            ]
        }

    def dict(self, *args, **kwargs):
        return super().dict(exclude_none=True, *args, **kwargs)

class ModerationStats(BaseModel):
    total_requests: int
    cached_requests: int
    average_response_time: float

    class Config:
        json_schema_extra = {
            "example": {
                "total_requests": 100,
                "cached_requests": 25,
                "average_response_time": 0.45
            }
        }