from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import word, validate, summary
from app.config import settings
import logging
import time

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    debug=settings.debug
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"Response: {response.status_code} | "
            f"Time: {process_time:.3f}s | "
            f"Path: {request.url.path}"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred"
        }
    )

# Include routers
app.include_router(word.router, prefix="/api", tags=["Word"])
app.include_router(validate.router, prefix="/api", tags=["Validation"])
app.include_router(summary.router, prefix="/api", tags=["Summary"])

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.app_name} v{settings.api_version}")
    if settings.n8n_webhook_url:
        logger.info(f"n8n webhook configured: {settings.n8n_webhook_url}")
    else:
        logger.warning("n8n webhook URL not configured - using mock responses")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application")

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.api_version,
        "n8n_configured": bool(settings.n8n_webhook_url),
        "endpoints": {
            "word": "/api/word",
            "validate": "/api/validate-sentence",
            "summary": "/api/summary",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.api_version,
        "n8n_configured": bool(settings.n8n_webhook_url)
    }