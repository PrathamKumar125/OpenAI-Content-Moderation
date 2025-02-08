from pydantic import BaseModel
from typing import Optional

class ComponentHealth(BaseModel):
    status: str
    details: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "details": "Connection successful"
            }
        }

class HealthCheckResponse(BaseModel):
    status: str
    database: ComponentHealth
    redis: ComponentHealth
    celery: ComponentHealth
    api: ComponentHealth
    last_checked: str

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "database": {
                    "status": "healthy",
                    "details": "Connected to PostgreSQL"
                },
                "redis": {
                    "status": "healthy",
                    "details": "Redis connection OK"
                },
                "celery": {
                    "status": "healthy",
                    "details": "Workers active"
                },
                "api": {
                    "status": "healthy",
                    "details": "OpenAI API responsive"
                },
                "last_checked": "2025-02-08T20:15:30.123456"
            }
        }