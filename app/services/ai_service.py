import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    async def validate_sentence(word: str, sentence: str):
        """
        ส่งประโยคไปให้ AI ตรวจสอบผ่าน n8n webhook
        """
        
        if not settings.n8n_webhook_url:
            logger.warning("n8n webhook URL not configured, using mock response")
            return AIService._get_mock_response(word, sentence)
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                logger.info(f"Sending request to n8n: word={word}, sentence={sentence}")
                
                response = await client.post(
                    settings.n8n_webhook_url,
                    json={
                        "word": word,
                        "sentence": sentence
                    },
                    headers={
                        "Content-Type": "application/json"
                    }
                )
                
                response.raise_for_status()
                data = response.json()
                
                logger.info(f"Received response from n8n: {data}")
                
                # Validate response structure
                required_fields = ["score", "level", "suggestion", "corrected_sentence"]
                for field in required_fields:
                    if field not in data:
                        raise ValueError(f"Missing required field: {field}")
                
                # Ensure score is float
                data["score"] = float(data["score"])
                
                # Validate score range
                if not 0 <= data["score"] <= 10:
                    raise ValueError(f"Score out of range: {data['score']}")
                
                return data
                
        except httpx.TimeoutException:
            logger.error("n8n webhook timeout")
            raise Exception("AI service timeout. Please try again.")
            
        except httpx.HTTPStatusError as e:
            logger.error(f"n8n webhook HTTP error: {e.response.status_code}")
            raise Exception(f"AI service error: {e.response.status_code}")
            
        except ValueError as e:
            logger.error(f"Invalid response from n8n: {str(e)}")
            raise Exception("Invalid response from AI service")
            
        except Exception as e:
            logger.error(f"Unexpected error calling n8n: {str(e)}")
            raise Exception("Failed to validate sentence. Please try again.")
    
    @staticmethod
    def _get_mock_response(word: str, sentence: str):
        """
        Mock response สำหรับการทดสอบเมื่อยังไม่ได้เชื่อมต่อ n8n
        """
        import random
        
        score = round(random.uniform(7.0, 9.5), 1)
        
        return {
            "score": score,
            "level": "Beginner" if score < 6.0 else "Intermediate" if score < 8.5 else "Advanced",
            "suggestion": f"Good use of the word '{word}'! Try adding more descriptive adjectives to make your sentence more vivid and engaging.",
            "corrected_sentence": sentence if score > 8.5 else f"The {word.lower()} was clearly visible from a distance."
        }