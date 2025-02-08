from openai import OpenAI
from typing import Union, List, Dict
from models.moderation import ContentItem  
from utils.config import get_settings
from utils.logging import logger

settings = get_settings()

class ModerationService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def moderate_content(self, content: Union[str, List[Dict]]):
        try:
            if isinstance(content, str):
                input_data = content
            else:
                input_data = []
                for item in content:
                    if item.get('type') == "text":
                        input_data.append(item.get('text'))
                    elif item.get('type') == "image_url":
                        input_data.append(item.get('image_url'))

            response = self.client.moderations.create(
                model="text-moderation-latest",
                input=input_data
            )
            return response.model_dump()
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise