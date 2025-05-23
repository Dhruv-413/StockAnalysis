# Stock Analysis Multi-Agent System (Leveraging Google AI - Gemini)

A production-ready, AI-powered stock analysis system built with FastAPI, leveraging Google's Gemini models for core AI capabilities, and multiple data sources. The system uses a custom multi-agent architecture to provide comprehensive stock analysis.

## 🚀 Features

- **Multi-Agent Architecture**: Modular Python-based agents for ticker identification, price fetching, news retrieval, and AI-powered insights.
- **Natural Language Processing**: Accept queries like "Why did Tesla stock drop today?"
- **Structured Queries**: Support JSON-based queries for programmatic access
- **Real-time Data**: Live stock prices and recent news primarily from Finnhub.
- **AI Analysis**: Powered by Google Gemini for intelligent stock movement analysis.
- **Production Ready**: Rate limiting, caching, error handling, and monitoring.
- **Async Performance**: Built with FastAPI and async/await for high performance.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI API   │────│   Orchestrator   │────│   Agents Pool   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                │                        ├── Ticker ID Agent
                                │                        ├── Price Agent
                                │                        ├── News Agent
                                │                        └── Analysis Agent
                                │
                       ┌────────▼────────┐
                       │   Data Sources   │
                       ├─────────────────┤
                       │   • Finnhub     │
                       │   • Gemini AI   │
                       └─────────────────┘
```

## 📦 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd StockAnalysis
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application**:
```bash
python main.py
```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`.

## 🔑 API Keys Setup

You'll need the following API keys, configured in your `.env` file:

- **Google API Key**: For Gemini AI analysis (variable: `GOOGLE_API_KEY`).
- **Finnhub API Key**: For stock data and news (variable: `FINNHUB_API_KEY`).

## 🎯 Usage Examples

### Natural Language Queries

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Why did Tesla stock drop today?",
    "query_type": "natural_language"
  }'
```

### Structured Queries

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{\"ticker\": \"AAPL\", \"action\": \"news_and_price\"}",
    "query_type": "structured"
  }'
```

### Response Format

```json
{
  "ticker": "TSLA",
  "company_name": "Tesla Inc",
  "analysis_summary": "Tesla stock declined 3.2% today primarily due to...",
  "price_data": {
    "current_price": 248.50,
    "previous_close": 257.12,
    "change": -8.62,
    "change_percent": -3.35
  },
  "recent_news": [
    {
      "title": "Tesla Reports Q3 Earnings",
      "summary": "Tesla reported mixed Q3 results...",
      "source": "Reuters",
      "published_at": "2024-01-15T10:30:00Z"
    }
  ],
  "key_insights": [
    "Earnings miss expectations",
    "Supply chain concerns",
    "Market rotation from growth stocks"
  ],
  "sentiment": "negative",
  "confidence_score": 0.85,
  "timestamp": "2024-01-15T15:30:00Z"
}
```

## 🧪 Testing

Run the test suite:

```bash
pytest -v
```

## 📊 Monitoring & Performance

- **Rate Limiting**: 100 requests per minute per IP
- **Caching**: 5-minute cache for prices, 30-minute cache for analysis
- **Logging**: Structured logging with configurable levels
- **Health Checks**: Available at `/api/v1/health`

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production with Docker
```bash
docker build -t stock-analysis .
docker run -p 8000:8000 --env-file .env stock-analysis
```

### Clarification on "Google ADK" and Agent Development

**This project does NOT use a "Google Agent Development Kit (ADK)" or a managed Google Cloud agent platform (like Vertex AI Agent Builder or Dialogflow CX) for its core agent framework.**

Instead, it implements:
1.  A **custom multi-agent framework** built in Python. The "agents" are Python classes that perform specific tasks.
2.  Direct integration with **Google's Gemini models** using the `google-generativeai` Python SDK. This is used for AI-powered text analysis, summarization, and intent extraction.

The `google-adk` package found on PyPI is for Android/Assistant hardware development and is **not** used in this project.

While this project leverages Google's powerful AI (Gemini), its agent orchestration and structure are self-contained within this codebase.

**Potential Integration with Managed Google Cloud Agent Platforms:**
If you were to use a platform like Vertex AI Agent Builder:
*   You would define your agents and tools within the Google Cloud environment.
*   The Python logic from this project (e.g., specific agent functionalities) could potentially be adapted into "tools" or "fulfillments" that a Google Cloud-managed agent would call. This would be a different architectural approach.

This project serves as an example of building a sophisticated AI application by directly utilizing LLMs within a custom framework.

## 🛠️ Configuration

Key configuration options in `src/config.py`:

- `RATE_LIMIT_REQUESTS`: API rate limiting
- `REDIS_URL`: Cache backend (optional)
- `LOG_LEVEL`: Logging verbosity
- `GEMINI_MODEL`: AI model for analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support or questions:
- Check the `/docs` endpoint for API documentation
- Review this README, particularly the "Clarification on 'Google ADK' and Agent Development" section.
- Open an issue on GitHub

### Google Cloud Alignment
This project's modular agent design and its direct use of Google Gemini for AI capabilities align with the principles of building sophisticated AI systems. While it's a custom framework, the functionalities developed here could conceptually be exposed as tools if one were to integrate with broader Google Cloud AI services like Vertex AI Agent Builder in the future.
