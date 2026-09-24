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
| Fast text decisions | Structured-output LLM (Haiku 4.5 / Flash-Lite) | **TypeSafe Jev** (ADR-007 bake-off) | Groq / Cerebras open models; local fine-tuned classifier | LLM as primary decision maker |
| Streaming analytics | In-process state + Polars/DuckDB per bar | ― | Deephaven; Materialize CE; RisingWave; Feldera | Bytewax (company stopped); ksqlDB for new work |
| Storage | Postgres (partitioned) | TimescaleDB (Tiger Cloud) at trigger | ClickHouse / QuestDB (ticks); KDB-X Community | ArcticDB (BSL) without agreement |
| Messaging / fan-out | Postgres outbox + LISTEN/NOTIFY; SSE | Centrifugo | NATS JetStream; Redis Streams/Valkey | Kafka for this team size |
| Durable workflows / audit | DBOS (Postgres) | ― | Temporal; Restate (BSL server) | ― |
| ML | LightGBM/CatBoost; River (drift) | lleaves / Treelite / ONNX Runtime | Chronos-2 / TimesFM 2.5 (Apache weights) for volume/vol only | TS foundation models for return forecasts; non-commercial weights (TimesFM 3.0, Moirai 2.0) |
| Backtest → live (later) | ― | ― | NautilusTrader 1.x + IBKR; LEAN + Alpaca | vectorbt PRO / PyBroker / Backtesting.py in product (licences) |
| Agents (research only) | Claude Code subagents (this repo) | Pydantic AI; Claude Agent SDK | LangGraph; OpenBB MCP | Agents with trading tools (e.g. Alpaca MCP order tools) |
