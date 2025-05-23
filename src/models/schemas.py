from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
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

class StructuredQuery(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol")
    action: str = Field(..., description="Action to perform")
    timeframe: Optional[str] = "1d"
    additional_params: Optional[Dict[str, Any]] = None

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
    high_price_today: Optional[float] = None # From quote
    low_price_today: Optional[float] = None # From quote
    open_price_today: Optional[float] = None # From quote

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

class FinancialReport(BaseModel):
    period_end_date: str
    filing_date: str
    report: Dict[str, Any] # Can be complex, so keeping as dict for now

class FinancialsData(BaseModel):
    annual_reports: List[FinancialReport] = []
    quarterly_reports: List[FinancialReport] = []

class EventData(BaseModel):
    event_type: str # e.g., earnings, dividend, split, IPO
    date: Optional[datetime] = None
    description: str
    details: Optional[Dict[str, Any]] = None

class InsiderTransaction(BaseModel):
    name: str
    share: int
    change: int # Number of shares transacted
    filing_date: datetime
    transaction_date: datetime
    transaction_price: float
    transaction_code: str # P-Purchase, S-Sale

class MarketNewsItem(NewsItem): # Inherits from NewsItem, can add more fields if needed
    category: Optional[str] = None

class TechnicalIndicator(BaseModel):
    name: str
    value: Any # Could be a float, dict, list of dicts depending on indicator
    parameters: Dict[str, Any]

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
    
    # New fields for additional agent data
    price_change_data: Optional[List[PriceChangeData]] = None
    financials: Optional[FinancialsData] = None
    upcoming_events: Optional[List[EventData]] = None
    insider_activity: Optional[List[InsiderTransaction]] = None
    # market_scan_results: Optional[List[MarketNewsItem]] = None # For market scanner, if applicable to single stock analysis
    technical_indicators: Optional[List[TechnicalIndicator]] = None

class AgentResponse(BaseModel):
    agent_name: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
