# Stock Analysis Multi-Agent System

A production-ready, AI-powered stock analysis platform built with FastAPI and Google Gemini. This system leverages a sophisticated multi-agent architecture to provide real-time stock insights, natural language query processing, and intelligent market analysis.

---

## 🚀 Key Features

- **🤖 Multi-Agent Architecture**: Specialized agents for ticker identification, price retrieval, news aggregation, historical analysis, and AI-powered insights
- **🗣️ Natural Language Processing**: Process queries like "Why did Tesla stock drop today?" or "How has Apple performed this week?"
- **📈 Real-Time Market Data**: Live stock prices, news, and historical data from Finnhub and Alpha Vantage APIs
- **🧠 AI-Driven Analysis**: Google Gemini integration for contextual stock movement analysis and sentiment evaluation
- **⚡ Production-Ready**: Built-in rate limiting, intelligent caching, comprehensive error handling, and health monitoring
- **🔧 Extensible Design**: Modular architecture for easy addition of new data sources and analysis capabilities

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                    │
├─────────────────────────────────────────────────────────────┤
│                    Main Orchestrator                       │
├─────────────────────────────────────────────────────────────┤
│                    Agent Layer                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐ │
│  │ Ticker ID Agent │ │ Price Agent     │ │ News Agent   │ │
│  └─────────────────┘ └─────────────────┘ └──────────────┘ │
│  ┌─────────────────┐ ┌─────────────────┐                  │
│  │Price Change Agt │ │ Analysis Agent  │                  │
│  └─────────────────┘ └─────────────────┘                  │
├─────────────────────────────────────────────────────────────┤
│                   Adapter Layer                            │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐ │
│  │ Finnhub Adapter │ │Alpha Vantage Adp│ │ Gemini Adp   │ │
│  └─────────────────┘ └─────────────────┘ └──────────────┘ │
│  ┌─────────────────┐                                      │
│  │TwelveData Adp   │                                      │
│  └─────────────────┘                                      │
├─────────────────────────────────────────────────────────────┤
│                   External APIs                            │
│    Finnhub API    Alpha Vantage API    Google Gemini      │
└─────────────────────────────────────────────────────────────┘
```

### Core Components

**Agents:**
- **TickerIdentificationAgent**: Identifies stock tickers from natural language queries
- **TickerPriceAgent**: Fetches real-time stock prices and market data
- **TickerNewsAgent**: Aggregates recent news and market sentiment
- **TickerPriceChangeAgent**: Calculates historical price movements and trends
- **TickerAnalysisAgent**: Performs AI-powered analysis using Gemini

**Adapters:**
- **FinnhubAdapter**: Real-time quotes, news, company profiles, financials
- **AlphaVantageAdapter**: Historical data, technical indicators, time series
- **GeminiAdapter**: Intent extraction and intelligent analysis
- **TwelveDataAdapter**: Technical indicators and advanced market data

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.8+
- pip package manager
- API keys for external services

### 1. Clone the Repository

```bash
git clone <repository-url>
cd StockAnalysis
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy example file if available
cp .env.example .env
```

Configure your `.env` file with the following variables:

```env
# Required API Keys
GOOGLE_API_KEY=your_google_gemini_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here

# Optional API Keys
TWELVE_DATA_API_KEY=your_twelve_data_api_key_here

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
CACHE_TTL=3600
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### 5. Run the Application

```bash
python main.py
```

The API will be available at:
- **Main API**: [http://localhost:8000](http://localhost:8000)
- **Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔑 API Keys & Data Sources

### Required Services

| Service | Purpose | Free Tier | Get API Key |
|---------|---------|-----------|-------------|
| **Google Gemini** | AI Analysis & Intent Extraction | Yes | [Google AI Studio](https://makersuite.google.com/) |
| **Finnhub** | Real-time prices, news, profiles | Yes (60 calls/min) | [Finnhub.io](https://finnhub.io/) |
| **Alpha Vantage** | Historical data, time series | Yes (5 calls/min) | [Alpha Vantage](https://www.alphavantage.co/) |

### Optional Services

| Service | Purpose | Free Tier | Get API Key |
|---------|---------|-----------|-------------|
| **Twelve Data** | Technical indicators, advanced data | Yes (8 calls/min) | [Twelve Data](https://twelvedata.com/) |

---

## 🎯 Usage Examples

### Basic Natural Language Queries

```bash
# Current stock status
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Apple stock price today?"}'

# Historical analysis
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "How has Tesla performed in the last 7 days?"}'

# Market sentiment
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why did Microsoft stock drop today?"}'
```

### Supported Query Types

The system understands various natural language patterns:

- **Price Queries**: "What's Apple's current price?", "AAPL stock price"
- **Performance Analysis**: "How has Tesla performed this week?", "TSLA 30 day performance"
- **Market Events**: "Why did Google stock drop?", "What's happening with NVDA?"
- **Historical Trends**: "Apple stock history last month", "Microsoft 7 day trend"

### Example Response

```json
{
  "ticker": "AAPL",
  "company_name": "Apple Inc.",
  "analysis_summary": "Apple stock declined 2.3% over the past 7 days, primarily driven by concerns over iPhone sales in China and broader market volatility. The decline follows mixed earnings results and analyst downgrades.",
  "price_data": {
    "ticker": "AAPL",
    "current_price": 195.27,
    "previous_close": 201.45,
    "change": -6.18,
    "change_percent": -3.07,
    "volume": 45230000,
    "market_cap": 3000000000000,
    "high_price_today": 197.50,
    "low_price_today": 194.80,
    "open_price_today": 196.20
  },
  "recent_news": [
    {
      "title": "Apple Reports Mixed Q4 Results Amid China Concerns",
      "summary": "Apple's latest quarterly results show...",
      "source": "Reuters",
      "published_at": "2024-01-15T10:30:00Z",
      "url": "https://...",
      "sentiment": "negative"
    }
  ],
  "key_insights": [
    "iPhone sales declined 5% in China market",
    "Services revenue grew 8% year-over-year", 
    "Stock trading below 50-day moving average"
  ],
  "sentiment": "negative",
  "confidence_score": 0.87,
  "timestamp": "2024-01-15T14:30:00Z",
  "price_change_data": [
    {
      "period": "7 days",
      "open": 210.00,
      "close": 195.27,
      "change": -14.73,
      "change_percent": -7.02,
      "high": 212.50,
      "low": 194.80,
      "meta": {
        "start_date_used": "2024-01-08",
        "end_date_used": "2024-01-15",
        "data_points": 7,
        "data_source": "alpha_vantage"
      }
    }
  ]
}
```

---

## 🛠️ Configuration & Customization

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GOOGLE_API_KEY` | Google Gemini API key | - | ✅ |
| `FINNHUB_API_KEY` | Finnhub API key | - | ✅ |
| `ALPHA_VANTAGE_API_KEY` | Alpha Vantage API key | - | ✅ |
| `TWELVE_DATA_API_KEY` | Twelve Data API key | - | ❌ |
| `ENVIRONMENT` | Runtime environment | development | ❌ |
| `LOG_LEVEL` | Logging verbosity | INFO | ❌ |
| `CACHE_TTL` | Cache duration (seconds) | 3600 | ❌ |
| `RATE_LIMIT_REQUESTS` | Rate limit per window | 100 | ❌ |
| `RATE_LIMIT_WINDOW` | Rate limit window (seconds) | 60 | ❌ |

### Customizing Analysis

Modify `src/adapters/gemini_adapter.py` to customize:
- Analysis prompts and context
- Intent extraction logic
- Response formatting
- Confidence scoring

### Adding New Data Sources

1. Create a new adapter in `src/adapters/`
2. Extend `BaseAdapter` class
3. Implement required methods
4. Register in relevant agents

---

## 🧪 Testing

### Run All Tests

```bash
pytest -v
```

### Test Coverage

```bash
pytest --cov=src tests/
```

### Manual Testing

Use the interactive documentation at `/docs` to test endpoints manually.

---

## 🔍 API Endpoints

### Analysis Endpoint

**POST** `/api/v1/analyze`

Analyze stocks using natural language queries.

**Request Body:**
```json
{
  "query": "string",
}
```

### Health Check

**GET** `/api/v1/health`

Check system health and status.

### Supported Queries

**GET** `/api/v1/supported-queries`

Get examples of supported query patterns.

---

## 🔧 Project Structure

```
StockAnalysis/
├── src/
│   ├── agents/                 # Multi-agent system
│   │   ├── base_agent.py      # Base agent class
│   │   ├── ticker_identification_agent.py
│   │   ├── ticker_price_agent.py
│   │   ├── ticker_news_agent.py
│   │   ├── ticker_price_change_agent.py
│   │   └── ticker_analysis_agent.py
│   ├── adapters/              # External API integrations
│   │   ├── base_adapter.py
│   │   ├── finnhub_adapter.py
│   │   ├── alpha_vantage_adapter.py
│   │   ├── gemini_adapter.py
│   │   └── twelve_data_adapter.py
│   ├── models/                # Data models and schemas
│   │   └── schemas.py
│   ├── orchestrator/          # Request orchestration
│   │   └── main_orchestrator.py
│   ├── presentation/          # API layer
│   │   └── routes.py
│   ├── utils/                 # Utilities
│   │   ├── logger.py
│   │   ├── cache.py
│   │   └── rate_limiter.py
│   └── config.py              # Configuration settings
├── tests/                     # Test suite
├── main.py                    # Application entry point
├── requirements.txt           # Dependencies
├── .env                       # Environment
└── README.md                  # Documentation
```

---

## 🚀 Deployment

### Local Development

```bash
python main.py
```


## 🔒 Security & Rate Limiting

- **Rate Limiting**: 30 requests/minute per IP (configurable)
- **API Key Validation**: All external APIs require valid keys
- **CORS**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic models for request validation

---


## 📊 Performance & Monitoring

### Caching Strategy

- **Price Data**: 5-minute cache
- **News Data**: 30-minute cache
- **Historical Data**: 1-hour cache
- **Company Profiles**: 24-hour cache

### Monitoring Endpoints

- **Health Check**: `/api/v1/health`
- **Metrics**: Available through logging
- **Rate Limit Status**: Headers in API responses

---

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify all required API keys are set in `.env`
   - Check API key quotas and limits

2. **Rate Limiting**
   - Implement appropriate delays between requests
   - Consider upgrading API plans for higher limits

3. **Cache Issues**
   - Clear cache by restarting the application
   - Check Redis configuration if using external cache

### Debug Mode

Set `LOG_LEVEL=DEBUG` for detailed logging.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** for AI analysis capabilities
- **Finnhub** for real-time market data
- **Alpha Vantage** for historical data
- **FastAPI** for the robust web framework

---
