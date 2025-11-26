import os 
from dotenv import load_dotenv

load_dotenv()

class Setting:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL" , 
        "postgresql://postgres:pass@localhost:5432/worddee"
    )

    N8N_WEBHOOK_URL: str = os.getenv(
        "N8N_WEBHOOK_URL",
        "http://localhost:5678/webhook/worddee-validate"
    )

Setting = Setting()