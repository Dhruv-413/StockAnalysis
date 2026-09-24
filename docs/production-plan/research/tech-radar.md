# Tech Radar — StockAnalysis

Owner: `tech-scout`. Refresh monthly with `/research-sprint`. Last update: **2026-09-24**. Evidence and licences are in the research appendices.

**Rings**

| Ring | Meaning |
|---|---|
| **Adopt** | Default choice |
| **Trial** | Use in a spike behind an interface |
| **Assess** | Worth learning; no build yet |
| **Hold** | Avoid for new work |

| Area | Adopt | Trial | Assess | Hold |
|---|---|---|---|---|
| Runtime / language | Python 3.12 asyncio (Linux; uvloop) | Rust via PyO3 for profiled hot spots | Apache Pekko (JVM); Elixir OTP + Broadway; Mojo 1.0 | Akka 3 for this team (BSL licence key); a full rewrite without a benchmark |
| Networking / parsing | msgspec; httpx (REST) | picows; niquests (HTTP/3) | WebTransport | ― |
| Market-data clients | Vendor official SDKs (`databento`, `massive`, Alpaca) | `ib_async` (IBKR, later) | Databento Live (TCP/DBN) for tier B | `yfinance` in product; `polygon-api-client` (superseded by `massive`) |
| Filings / news | EDGAR Atom poller (≤ 10 req/s, User-Agent) | sec-api.io stream; Benzinga WebSocket | RTPR (press-wire aggregate; claims unverified) | Scraping sites whose terms forbid it |
| Decision / rules | Deterministic detectors + **GoRules Zen JDM**; CEL (user conditions) | ― | Drools/KIE (if JVM); OPA/Cedar (policy only) | durable_rules; Siddhi; Esper (GPLv2) in closed product |
| Fast text decisions | Structured-output LLM (Haiku 4.5 / Flash-Lite) | **TypeSafe Jev**, for background tagging only (ADR-007/008). **Hold on the India live path**: US-West hosting, English-first, no SLA | Groq / Cerebras open models; local fine-tuned classifier | LLM as primary decision maker |
| Streaming analytics | In-process state + Polars/DuckDB per bar | ― | Deephaven; Materialize CE; RisingWave; Feldera | Bytewax (company stopped); ksqlDB for new work |
| Storage | Postgres (partitioned) | TimescaleDB (Tiger Cloud) at trigger | ClickHouse / QuestDB (ticks); KDB-X Community | ArcticDB (BSL) without agreement |
| Assistant answer path | Card-first: exact-key cache (Valkey) + deterministic router + template stream | model2vec local router; Gemini 2.5 Flash-Lite narrative; Turbopuffer (Mumbai) | AnyJev (self-hosted, Apache-2.0, 0.0.2) | GPTCache (no release since 2024-08); semantic cache across symbols or time |
| Indicators | TA-Lib 0.8.x (reference) | talipp (streaming) | polars-ta | pandas-ta (repo 404; last release a 2025 beta) |
| Messaging / fan-out | Postgres outbox + LISTEN/NOTIFY; SSE | Centrifugo | NATS JetStream; Redis Streams/Valkey | Kafka for this team size |
| Durable workflows / audit | DBOS (Postgres) | ― | Temporal; Restate (BSL server) | ― |
| ML | LightGBM/CatBoost; River (drift) | lleaves / Treelite / ONNX Runtime | Chronos-2 / TimesFM 2.5 (Apache weights) for volume/vol only (see finance-model rows) | TS foundation models for return forecasts; non-commercial weights (TimesFM 3.0, Moirai 2.0) |
| Finance models: volatility and regime ([15](../15-finance-model-layer.md)) | HAR / Log-HAR, EWMA, GARCH(1,1)-t; exchange_calendars | IBM TTM r2, equal-weighted with Log-HAR (challenger) | **Kronos-small/base** (volatility challenger only; evaluated only from 2024-07; training data of unknown origin); FinCast; FinText checkpoints (for evaluation) | Any time-series FM for user-facing forecasts; Kronos-large (closed); MarS / TRADES / LOBS5 (need order-level data) |
| Finance NLP and LLMs | ― | FinBERT family (finbert-tone; ProsusAI as an internal baseline only, its training data is non-commercial) for **internal** tagging | Our own English + Hindi finance encoder; Fin-R1 / DianJin-R1 for filing QA; IndiaFinBench, FinQA and BizBench as evaluations | Palmyra-Fin (non-commercial); FinGPT-Forecaster; FinanceBench as training data (non-commercial); "Indian FinBERT" community models (mislabelled) |
| Quant research toolkits | TA-Lib (see Indicators) | `pyqlib` (research only); skfolio | RD-Agent 1.0; TradingAgents (reference only; integrates Jev) | OpenBB (AGPL) in product; vectorbt (Commons Clause) in product; PyPI look-alikes `qlib`, `kronos`, `tradingagents` |
| Backtest → live (later) | ― | ― | NautilusTrader 1.x + IBKR; LEAN + Alpaca | vectorbt PRO / PyBroker / Backtesting.py in product (licences) |
| Agents (research only) | Claude Code subagents (this repo) | Pydantic AI; Claude Agent SDK | LangGraph; OpenBB MCP | Agents with trading tools (e.g. Alpaca MCP order tools) |
