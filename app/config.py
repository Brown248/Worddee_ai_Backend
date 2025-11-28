from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Worddee.ai API"
    api_version: str = "v1"
    n8n_webhook_url: str = ""  # URL สำหรับเชื่อมต่อ n8n
    
    class Config:
        env_file = ".env"

settings = Settings()