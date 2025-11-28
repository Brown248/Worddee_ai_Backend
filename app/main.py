from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import word, validate, summary
from app.config import settings

app = FastAPI(title=settings.app_name, version=settings.api_version)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(word.router, prefix="/api", tags=["Word"])
app.include_router(validate.router, prefix="/api", tags=["Validation"])
app.include_router(summary.router, prefix="/api", tags=["Summary"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Worddee.ai API",
        "version": settings.api_version,
        "endpoints": {
            "word": "/api/word",
            "validate": "/api/validate-sentence",
            "summary": "/api/summary"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}