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

**A. FastApi**
```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                    │
├─────────────────────────────────────────────────────────────┤
│                    Main Orchestrator                        │
├─────────────────────────────────────────────────────────────┤
│                    Agent Layer                              │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │ Ticker ID Agent │ │ Price Agent     │ │ News Agent   │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
│  ┌─────────────────┐ ┌─────────────────┐                    │
│  │Price Change Agt │ │ Analysis Agent  │                    │
│  └─────────────────┘ └─────────────────┘                    │
├─────────────────────────────────────────────────────────────┤
│                   Adapter Layer                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐   │
│  │ Finnhub Adapter │ │Alpha Vantage Adp│ │ Gemini Adp   │   │
│  └─────────────────┘ └─────────────────┘ └──────────────┘   │
│  ┌─────────────────┐                                        │
│  │TwelveData Adp   │                                        │
│  └─────────────────┘                                        │
├─────────────────────────────────────────────────────────────┤
│                   External APIs                             │
│    Finnhub API    Alpha Vantage API    Google Gemini        │  
└─────────────────────────────────────────────────────────────┘
```

**B. Agent Architecture in ADK**

```
┌─────────────────────────────────────────────────────────────────┐
│                     StockAnalysisAgent                          │
│                                                                 │
│  ┌────────────────┐ ┌───────────────────────────────────────┐   │
│  │IdentifyTickerA.│→│         ParallelFetchAgent            │   │
│  └────────────────┘ │  ┌─────────┐ ┌─────────┐ ┌─────────┐  │   │
│                     │  │ Price   │ │ News    │ │ Price   │  │   │
│                     │  │ Agent   │ │ Agent   │ │ Change  │  │→  │→┌───────────┐
│                     │  └─────────┘ └─────────┘ └─────────┘  │   │ │Analysis   │
│                     └───────────────────────────────────────┘   │ │Agent      │
└─────────────────────────────────────────────────────────────────┘ └───────────┘
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

- Python 3.10
- pip package manager
- Git (for cloning the repository)
- Node.js v16+ and npm (for ADK Web interface, optional)

### 1. Clone the Repository

```bash
git clone https://github.com/Dhruv-413/StockAnalysis.git
cd StockAnalysis
```

### 2. Create Virtual Environment (Required)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

Verify your virtual environment is active by checking for `(venv)` prefix in your terminal.

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt
```

### 4. Obtain API Keys (Required)

Before running the application, you must obtain API keys from the following services:

1. **Google Gemini API** (Required)
   - Visit [Google AI Studio](https://makersuite.google.com/)
   - Create an account or sign in
   - Generate an API key from the API keys section

2. **Finnhub API** (Required)
   - Visit [Finnhub.io](https://finnhub.io/)
   - Register for a free account
   - Copy your API key from the dashboard

3. **Alpha Vantage API** (Required)
   - Visit [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
   - Get a free API key by completing the form
   - Copy your API key from the email or dashboard

4. **Twelve Data API**
   - Visit [Twelve Data](https://twelvedata.com/)
   - Register for a free account
   - Copy your API key from the dashboard

5. **Marketaux API**
   - Visit [Marketaux](https://marketaux.com/)  
   - Register for a free account  
   - Copy your API key from the dashboard  

### 5. Environment Configuration (Required)

Create a `.env` file in the project root with the following content:

```env
# Required API Keys (Replace with your actual keys)
GOOGLE_API_KEY=your_google_gemini_api_key_here
FINNHUB_API_KEY=your_finnhub_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
TWELVE_DATA_API_KEY=your_twelve_data_api_key_here
MARKETAUX_API_KEY=your_marketaux_api_key_here

# Application Settings (Adjust as needed)
ENVIRONMENT=development
LOG_LEVEL=INFO
CACHE_TTL=3600
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

**Important**: Without proper API keys, the application will not function correctly.

### 6. Run the Application

There are two ways to run the application:

#### A. Standard FastAPI Server)

```bash
# Make sure your virtual environment is activated
python main.py
```

This will start the REST API server on [http://localhost:8001](http://localhost:8001).

#### B. Google ADK Integration

```bash
# First, ensure the ADK module is installed
pip install google-adk

#Second, clone adk-web repository
git clone https://github.com/google/adk-web.git
cd adk-web
npm install

#Run the ADK-Web server
npm run serve --backend=http://localhost:8000

# Run the ADK server
adk api_server --allow_origins=http://localhost:4200 --host=0.0.0.0
```

The ADK server will run on [http://localhost:8000](http://localhost:8000).\
Visit http://localhost:4200 in your browser to access the ADK Web interface.

---

## 🔧 Project Structure

```
StockAnalysis/
├── src/                       # Source code
│   ├── agents/                # Multi-agent system
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
├── adk_agents/                # Google ADK integration
│   ├── agent.py               # Root agent definition
│   ├── identify_ticker.py     # Ticker identification
│   ├── ticker_price.py        # Price data retrieval
│   ├── ticker_news.py         # News retrieval
│   ├── ticker_price_change.py # Historical data analysis
│   ├── ticker_analysis.py     # AI analysis
│   └── main.py                # Agent workflow definitions
├── main.py                    # FastAPI application entry point
├── adk_main.py                # Google ADK entry point
├── requirements.txt           # Dependencies
├── .env                       # Environment variables
└── README.md                  # Documentation
```

---

## 🔑 API Keys & Data Sources

### Required Services

| Service | Purpose | Free Tier Limits | Get API Key |
|---------|---------|------------------|-------------|
| **Google Gemini** | AI Analysis & Intent Extraction | 60 queries/minute | [Google AI Studio](https://makersuite.google.com/) |
| **Finnhub** | Real-time prices, news, profiles | 60 calls/minute | [Finnhub.io](https://finnhub.io/) |
| **Alpha Vantage** | Historical data, time series | 5 calls/minute, 500/day | [Alpha Vantage](https://www.alphavantage.co/) |
| **Twelve Data** | Technical indicators | 8 calls/minute, 800/day | [Twelve Data](https://twelvedata.com/) |
| **Marketaux** | Financial news | 100 calls/day | [Marketaux](https://www.marketaux.com/) |

**Note**: The system implements automatic fallback between data providers. If one source fails or reaches its rate limit, others will be attempted.

---

## 🎯 Usage Examples

### Testing the API

Once the server is running, you can interact with it through:

1. **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
2. **ReDoc**: [http://localhost:8001/redoc](http://localhost:8001/redoc)
3. **cURL Commands** (examples below)

### Basic Natural Language Queries

```bash
# Current stock status
curl -X POST "http://localhost:8001/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Apple stock price today?"}'

# Historical analysis
curl -X POST "http://localhost:8001/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "How has Tesla performed in the last 7 days?"}'

# Market sentiment
curl -X POST "http://localhost:8001/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"query": "Why did Microsoft stock drop today?"}'
```

### Using Python Client

```python
import requests
import json

url = "http://localhost:8001/api/v1/analyze"
headers = {"Content-Type": "application/json"}
data = {"query": "What's happening with NVIDIA stock?"}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(json.dumps(result, indent=2))
```

### Health Check

```bash
curl "http://localhost:8001/api/v1/health"
```

Expected response:
```json
{"status": "healthy", "service": "Stock Analysis API"}
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
| `TWELVE_DATA_API_KEY` | Twelve Data API key | - | ✅ |
| `MARKETAUX_API_KEY` | Marketaux news API key | - | ✅ |
| `ENVIRONMENT` | Runtime environment (development/production) | development | ❌ |
| `LOG_LEVEL` | Logging verbosity (DEBUG/INFO/WARNING/ERROR) | INFO | ❌ |
| `CACHE_TTL` | Cache duration in seconds | 3600 | ❌ |
| `RATE_LIMIT_REQUESTS` | Rate limit per window | 100 | ❌ |
| `RATE_LIMIT_WINDOW` | Rate limit window in seconds | 60 | ❌ |
| `REDIS_URL` | Redis connection string (for distributed cache) | None | ❌ |


## 🔍 API Reference

### Analysis Endpoint

**POST** `/api/v1/analyze`

Analyze stocks using natural language queries.

**Request Body:**
```json
{
  "query": "string",
}
```

**Parameters:**

| Field | Type | Description |
|-------|------|-------------|
| query | string | Natural language query or ticker symbol |
| query_type | string | Either "natural_language" or "structured" |
| include_fundamentals | boolean | Include fundamental data in response |
| include_insider_activity | boolean | Include insider trading data |

**Response**: `AnalysisResult` object (see example above)

### Health Check

**GET** `/api/v1/health`

Check system health and status.

**Response:**
```json
{
  "status": "healthy",
  "service": "Stock Analysis API"
}
```

### Supported Queries

**GET** `/api/v1/supported-queries`

Get examples of supported query patterns.

**Response:**
```json
{
  "natural_language_examples": [
    "Why did Tesla stock drop today?",
    "What's happening with Apple stock recently?",
    "How has Microsoft performed this week?",
    "What's driving Nvidia's stock price?"
  ],
  "structured_examples": [
    {"ticker": "AAPL", "action": "news_and_price"},
    {"ticker": "TSLA", "action": "analysis", "timeframe": "7d"}
  ]
}
```


## 🔒 Security & Rate Limiting

- **Rate Limiting**: 30 requests/minute per IP (configurable)
- **API Key Security**: All external API keys are stored securely in environment variables
- **Input Validation**: All requests are validated using Pydantic models
- **CORS**: Configurable cross-origin resource sharing
- **Exception Handling**: Comprehensive error handling prevents exposing system details

To adjust rate limits, modify the following environment variables:
- `RATE_LIMIT_REQUESTS`: Maximum requests per window
- `RATE_LIMIT_WINDOW`: Time window in seconds

---

## 📊 Performance & Monitoring

### Caching Strategy

The system implements multi-level caching to optimize performance:

- **Price Data**: 5-minute cache (TTL=300)
- **News Data**: 30-minute cache (TTL=1800)
- **Historical Data**: 1-hour cache (TTL=3600)
- **Company Profiles**: 24-hour cache (TTL=86400)

The caching system automatically falls back to memory cache if Redis is not configured.

### Monitoring Endpoints

- **Health Check**: `/api/v1/health`
- **Metrics**: Available through logging
- **Rate Limit Status**: Headers in API responses

### Logs

By default, logs are written to the console.
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python main.py
```

---


## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** for AI analysis capabilities
- **Finnhub** for real-time market data
- **Alpha Vantage** for historical data
- **FastAPI** for the robust web framework
- **Google ADK** for agent development toolkit
