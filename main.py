from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.routes import router
from src.utils.rate_limiter import limiter, rate_limit_handler
from slowapi.errors import RateLimitExceeded
from src.utils.logger import setup_logger
from src.config import settings

# Initialize logger
logger = setup_logger("StockAnalysisApp")

# Create FastAPI app
app = FastAPI(
    title="Stock Analysis Multi-Agent System",
    description="AI-powered stock analysis leveraging Google Gemini models within a custom FastAPI framework.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("Stock Analysis API starting up...")
    logger.info(f"Environment: {settings.environment}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Stock Analysis API shutting down...")

@app.get("/")
async def root():
    return {
        "message": "Stock Analysis Multi-Agent System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )
