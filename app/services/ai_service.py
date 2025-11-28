import httpx
from app.config import settings
import random

class AIService:
    @staticmethod
    async def validate_sentence(word: str, sentence: str):
        """
        ส่งประโยคไปให้ AI ตรวจสอบผ่าน n8n webhook
        ในตัวอย่างนี้ใช้ mock data ถ้าต้องการเชื่อมต่อจริง
        ให้ uncomment ส่วน httpx และตั้งค่า n8n_webhook_url ใน .env
        """
        
        # Mock response (ใช้เมื่อยังไม่ได้เชื่อมต่อ n8n)
        score = round(random.uniform(7.0, 9.5), 1)
        
        feedback = {
            "score": score,
            "level": "Beginner" if score < 8.0 else "Intermediate",
            "suggestion": f"Try using adjectives to expand your sentence. Your use of '{word}' is good, but adding more context would improve it.",
            "corrected_sentence": sentence if score > 8.5 else f"The {word.lower()} is being used correctly in context."
        }
        
        return feedback
        
        # Uncomment below for actual n8n integration:
        """
        if not settings.n8n_webhook_url:
            raise ValueError("n8n webhook URL not configured")
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    settings.n8n_webhook_url,
                    json={"word": word, "sentence": sentence},
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise Exception(f"Error calling n8n webhook: {str(e)}")
        """