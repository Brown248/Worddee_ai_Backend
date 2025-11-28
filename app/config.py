from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    app_name: str = "Worddee.ai API"
    api_version: str = "v1"
    debug: bool = False
    
    # n8n Settings
    n8n_webhook_url: Optional[str] = None
    n8n_timeout: int = 30  # seconds
    
    # CORS Settings
    cors_origins: list = ["http://localhost:3000", "http://localhost:3001"]
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()