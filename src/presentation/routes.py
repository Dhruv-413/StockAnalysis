from fastapi import APIRouter, HTTPException, Request, Depends
from src.models.schemas import AnalysisRequest, AnalysisResult
from src.orchestrator.main_orchestrator import MainOrchestrator
from src.utils.rate_limiter import limiter
from src.utils.logger import setup_logger

router = APIRouter(prefix="/api/v1", tags=["Stock Analysis"])
logger = setup_logger("StockAnalysisAPI")

# Initialize orchestrator
orchestrator = MainOrchestrator()

@router.post("/analyze", response_model=AnalysisResult)
@limiter.limit("30/minute")
async def analyze_stock(request: Request, analysis_request: AnalysisRequest):
    """
    Analyze a stock based on natural language query or structured input.
    
    Example queries:
    - "Why did Tesla stock drop today?"
    - "What's happening with Palantir stock recently?"
    - "How has Nvidia stock changed in the last 7 days?"
    - {"ticker": "AAPL", "action": "news_and_price"}
    """
    try:
        logger.info(f"Processing analysis request: {analysis_request.query}")
        result = await orchestrator.process_request(analysis_request)
        return result
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Stock Analysis API"}

@router.get("/supported-queries")
async def get_supported_queries():
    """Get examples of supported query types"""
    return {
        "natural_language_examples": [
            "Why did Tesla stock drop today?",
            "What's happening with Apple stock recently?",
            "How has Microsoft performed this week?",
            "Tell me about GameStop stock movement",
            "What's driving Nvidia's stock price?"
        ],
        "structured_examples": [
            {"ticker": "AAPL", "action": "news_and_price"},
            {"ticker": "TSLA", "action": "analysis", "timeframe": "7d"},
            {"ticker": "MSFT", "action": "price_change", "timeframe": "1d"}
        ]
    }
