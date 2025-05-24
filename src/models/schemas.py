from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class QueryType(str, Enum):
    NATURAL_LANGUAGE = "natural_language"
    STRUCTURED = "structured"

class AnalysisRequest(BaseModel):
    query: str = Field(..., description="Natural language query or JSON structure")
    query_type: QueryType = QueryType.NATURAL_LANGUAGE
    include_fundamentals: bool = False
    include_insider_activity: bool = False

class NewsItem(BaseModel):
    title: str
    summary: Optional[str] = None
    source: str
    published_at: datetime
    sentiment: Optional[str] = None
    url: Optional[str] = None

class PriceData(BaseModel):
    ticker: str
    current_price: float
    previous_close: float
    change: float
    change_percent: float
    volume: Optional[int] = None
    market_cap: Optional[float] = None
    high_price_today: Optional[float] = None
    low_price_today: Optional[float] = None
    open_price_today: Optional[float] = None

class StockCandle(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: int
    timestamp: datetime

class PriceChangeData(BaseModel):
    period: str
    open: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    candles: Optional[List[StockCandle]] = None
    meta: Optional[Dict[str, Any]] = None

class AnalysisResult(BaseModel):
    ticker: str
    company_name: Optional[str] = None
    analysis_summary: str
    price_data: Optional[PriceData] = None
    recent_news: List[NewsItem] = []
    key_insights: List[str] = []
    sentiment: Optional[str] = None
    confidence_score: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    price_change_data: Optional[List[PriceChangeData]] = None

class AgentResponse(BaseModel):
    agent_name: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
