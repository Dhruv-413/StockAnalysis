# 01 — Repository Assessment

**Scope:** the `v3` branch at commit `8e8dd33`, plus uncommitted `.serena/`. Assessed 2026-09-24.
**Evidence labels:** **[Verified]** means executed or read directly. **[Inferred]** means reasoned from code but not executed against live providers. **[Suspected]** means plausible but not confirmed.

← [Back to plan index](README.md) · Next: [02 Product thesis](02-product-thesis.md)

---

## 1. Summary

The repository is a **prototype of a natural-language "why did stock X move?" Q&A API**. For one US ticker per request it:

1. uses an LLM to guess the ticker, intent and timeframe;
2. fetches a quote, recent headlines and a period price change from free-tier providers, falling back from one provider to the next;
3. asks Gemini to write a summary.

It has no database, no users, no tests, no CI, no frontend of its own, no streaming and no persistent state. A second entry point exposes the same functions to Google ADK as LLM tools.

The README calls the system "production-ready" and "real-time", and it presents an example response containing news-driven insights. **The code does not support any of these claims.** The analysis prompt never includes the fetched news. Quotes are cached for up to 5 minutes and carry no timestamps. The app fails to start unless all five API keys are set. There are no tests. Keys were committed to the public GitHub history.

**What it is useful for:** a working map of which free APIs exist, a reasonable adapter/agent separation, and a demonstration of the target question ("why is this moving?"). Almost every layer needs a redesign before anyone relies on its numbers.

## 2. Inventory

### 2.1 Languages, frameworks, dependencies

| Item | Evidence | Notes |
|---|---|---|
| Python only; README says 3.10 | `README.md` §Prerequisites | Checks here ran on **3.12.10** in a scratch venv. The machine default is 3.14, which was not tested. |
| No lock file; `requirements.txt` has 18 **unpinned** names | `requirements.txt:1-18` | A fresh install on 2026-09-24 resolved fastapi 0.141.1, starlette 1.7.0, pydantic 2.13.5, pydantic-settings 2.15.0, httpx 0.28.1, google-generativeai 0.8.6, google-genai 2.25.0 (transitive), google-adk 2.9.2, yfinance 1.7.0, pandas 3.0.6, redis 8.1.0, slowapi 0.1.10, tenacity 9.1.4. Builds are not reproducible. |
| Declared but unused | `aiofiles`, `python-multipart`, `colorama`, `limits` (used only via slowapi) | Minor clean-up. |
| `pandas` is used but not declared | `yahoo_finance_adapter.py:3` | Arrives only transitively through yfinance. |
| LLM SDK | `google-generativeai` (`gemini_adapter.py:1`), model `gemini-1.5-flash` (`config.py:12`, `adk_agents/agent.py:17`) | Google has deprecated this SDK and retired this model. See [03 §F](03-market-and-tooling-research.md#f-llm-provider-status). |
| License | MIT (`LICENSE`) | This covers the code only. It gives no rights to data obtained through the APIs. See [04 §6](04-real-time-data-strategy.md#6-licensing-and-entitlements). |
| Package manager | pip + venv (README) | No pyproject, no tooling config (ruff, mypy, pytest), no pre-commit. |

### 2.2 Entry points, services, APIs

| Entry point | What it does | Evidence |
|---|---|---|
| `python main.py` → FastAPI on port 8001 | `POST /api/v1/analyze`, `GET /api/v1/health`, `GET /api/v1/supported-queries`, `/docs`, `/redoc` | `main.py:12-62`, `src/presentation/routes.py:13-46` |
| `adk api_server` (ADK web UI on port 4200 from an external `adk-web` checkout) | An LLM agent whose tools wrap the same agent classes | `adk_main.py`, `adk_agents/agent.py:11-30` |
| Background jobs, queues, schedulers, websockets | **None** | Confirmed by a full-tree read. |
| Database, migrations | **None** | — |
| Cache | Per-process `TTLCache` plus optional Redis (`REDIS_URL`) | `src/utils/cache.py:10-50` |
| Frontend | **None** first-party. The ADK web UI is a separate Google project. | README §B |

### 2.3 Module map

```
main.py ── routes.py ── MainOrchestrator (src/orchestrator/main_orchestrator.py)
                          ├─ GeminiAdapter.extract_intent_and_ticker     (LLM)
                          ├─ TickerIdentificationAgent → Finnhub search/profile (+ LLM hint)
                          ├─ TickerPriceChangeAgent → AlphaVantage → TwelveData → yfinance
                          ├─ TickerPriceAgent       → Finnhub → yfinance → TwelveData
                          ├─ TickerNewsAgent        → Finnhub + Marketaux + yfinance (parallel)
                          └─ TickerAnalysisAgent    → GeminiAdapter.analyze_stock_movement (LLM)
adk_main.py ── adk_agents/* ── same src/agents classes exposed as ADK FunctionTools
```

"Agents" here are plain async classes with an `execute()` wrapper (`src/agents/base_agent.py:12-31`). They are not autonomous agents. The only LLM decisions are intent extraction and summary writing. In the ADK path, tool choice is also left to the LLM.

### 2.4 Market-data sources actually called

| Provider | Endpoints used on the request path | Cache TTL | Evidence |
|---|---|---|---|
| Finnhub | `/search`, `/stock/profile2`, `/quote`, `/company-news` | 1 h / 1 h / **5 min** / 30 min | `finnhub_adapter.py:18-98` |
| Alpha Vantage | `TIME_SERIES_DAILY` (compact/full), `TIME_SERIES_WEEKLY`, `TIME_SERIES_MONTHLY` — **unadjusted** | 1–4 h | `alpha_vantage_adapter.py:64-161` |
| Twelve Data | `/quote`, `/time_series` | 5 min / 1 h | `twelve_data_adapter.py:55-216` |
| Marketaux | `/news/all` | 30 min | `marketaux_adapter.py:31-81` |
| Yahoo via `yfinance` (unofficial scraping) | `Ticker.info`, `.history`, `.news` | 5 min – 1 h | `yahoo_finance_adapter.py:20-137` |
| Google Gemini | `generate_content_async` | 5 min (intent only) | `gemini_adapter.py:15-261` |

Many adapter methods are defined but **never called**: Finnhub financials, candles, earnings, IPO, dividends, splits, insider and general-news methods, plus `get_price_change_over_period` and `get_comprehensive_historical_data`; Alpha Vantage `get_global_quote`, intraday and comprehensive methods; Twelve Data `get_technical_indicator`. The request fields `include_fundamentals`, `include_insider_activity` and `query_type` are accepted but ignored (`schemas.py:17-21`). "Structured" queries advertised by `/supported-queries` (`routes.py:42-45`) are not implemented.

### 2.5 Indicators, models, backtesting, portfolio, trading

**None implemented.** The only calculations are:
- the percent change between two closes;
- period high and low (`alpha_vantage_adapter.py:255-280`, `twelve_data_adapter.py:130-140`, `yahoo_finance_adapter.py:74-81`);
- a "today" change built from the quote (`main_orchestrator.py:166-194`).

There are no screeners, indicators, backtests, portfolios or broker integrations.

### 2.6 AI/ML components

| Component | Behaviour | Evaluation |
|---|---|---|
| Intent/ticker extraction | A hard-coded dictionary of 9 companies (`gemini_adapter.py:20-30`), otherwise a free-form LLM JSON parse | None |
| Analysis | One of three prompt templates, chosen by keyword (`"today"`, `"how … changed"`) (`gemini_adapter.py:140-189`) | None |
| `confidence_score` | Either invented by the LLM and rescaled (`gemini_adapter.py:208-220`) or hard-coded to 0.6/0.8 (`:242`, `:250`) | Has no statistical meaning, but is presented to users as a number |
| Sentiment | An LLM label, or the sign of the price change (`:240`, `:248`) | None |

### 2.7 Tests, CI/CD, infrastructure, observability, security

| Area | State |
|---|---|
| Tests | **0**. `pytest` exits 5 with "no tests ran" (see §5). `pytest` and `pytest-asyncio` are in requirements anyway. |
| CI/CD, containers, IaC | None: no `.github/`, Dockerfile, compose file or deploy scripts. |
| Logging | stdout `logging` with DEBUG-style f-strings at INFO level, which dump full provider payloads (`ticker_price_change_agent.py:21,40,64,88`, `finnhub_adapter.py:262`). Raw user queries are logged (`routes.py:20`). |
| Metrics, tracing, alerting | None. `/health` always returns "healthy" without checking dependencies (`routes.py:27-30`). |
| AuthN/AuthZ | None. |
| Rate limiting | slowapi in-memory, keyed per IP, 30/min on `/analyze` (`routes.py:14`). This does not work across multiple workers or behind a proxy unless the real client IP is forwarded. |
| CORS | `allow_origins=["*"]` with `allow_credentials=True` (`main.py:26-32`). |
| Secrets | `.env` via pydantic-settings. **Real keys were committed** (see §4.1). |

### 2.8 Documentation and developer setup

A single `README.md` of 528 lines. It is accurate on setup steps and inaccurate on capabilities: "real-time", "production-ready", "comprehensive error handling prevents exposing system details" (contradicted by `routes.py:25` and `main_orchestrator.py:238`), and an example response whose news-driven insights the code cannot produce. There was no `CLAUDE.md`, no `.claude/` directory and no `docs/`, and `docs/` was git-ignored (fixed narrowly; see [10](10-claude-code-setup.md)).

## 3. End-to-end workflow trace (`POST /api/v1/analyze`)

Traced by reading the code and by an **offline harness**. The harness stubbed every provider method and replaced the Gemini model with a fake that records prompts; no network calls were made. Query: *"Why did Tesla stock drop today?"*

| Step | Code | Observed / verified behaviour |
|---|---|---|
| 1. Intent | `gemini_adapter.py:32-79` | "tesla" hits the hard-coded map, so the ticker is TSLA without any lookup. The LLM is asked only for intent and timeframe. |
| 2. Ticker validation | `ticker_identification_agent.py:20-35` | Finnhub profile name is compared by substring. |
| 3. Timeframe | `main_orchestrator.py:26-103` | "today" parses to `duration_days = 1`, so the historical chain runs for 1 day. **[Verified]** All three providers return None in the stub; in live use they would compare the last close with the one before it. |
| 4. Quote and news | `main_orchestrator.py:128-163` | Run in parallel; the quote comes from Finnhub first. |
| 5. Synthetic "1 day" change | `main_orchestrator.py:166-194` | **[Verified]** The response reports `open = previous_close` (210.0), labelled as the period open. |
| 6. LLM analysis | `gemini_adapter.py:140-155` | **[Verified]** The captured prompt contains only price, change and range. **The fetched headline is absent from the prompt.** The model is asked to explain a drop without any evidence, so any cause it names is unsupported. |
| 7. Response | `main_orchestrator.py:222-232` | **[Verified]** The fake model's "87" became `confidence_score: 0.87`. `price_data` has **no timestamp and no source field**, so freshness cannot be shown. |
| Error path | `main_orchestrator.py:234-240` | **[Verified]** Internal exception text is returned in `analysis_summary` with **HTTP 200** and `ticker: "ERROR"`. |

## 4. Findings by severity

### 4.1 Critical

1. **Secrets in public git history.** `.env` with real-looking `GOOGLE_API_KEY`, `FINNHUB_API_KEY`, `TWELVE_DATA_API_KEY` and `ALPHA_VANTAGE_API_KEY` values was committed in `9a6f32a` and `c79b38a` (2025-05-23/24) and deleted in `b931726`. The GitHub repository is **public**: `gh repo view` reports `PUBLIC`, and the unauthenticated API returns 200. A regex scan finds 4 Google-key-shaped strings in history. Values are deliberately not reproduced here.
   **Action for the owner:** rotate or revoke all four keys now. Optionally purge history with `git filter-repo`, which requires a force-push, so it is the owner's decision. Enable GitHub secret scanning and push protection.
2. **The explanation feature is ungrounded.** News is fetched and returned but never passed to the LLM (`gemini_adapter.py:140-189`; §3 step 6). "Why did X move" answers are therefore invented.
3. **Fabricated market data exists in code.** `FinnhubAdapter.get_price_change_over_period` returns an invented −2.5% move and ±5% range, labelled `"resolution_used": "estimated"` (`finnhub_adapter.py:340-366`). It is currently reachable only through `get_comprehensive_historical_data`, which has no callers, so it is dead code. It must be deleted, not revived.
4. **Startup crash when any optional key is missing.** `AlphaVantageAdapter`, `TwelveDataAdapter` and `MarketauxAdapter` call `self.logger` before `super().__init__()` (`alpha_vantage_adapter.py:13-14`, `twelve_data_adapter.py:10-11`, `marketaux_adapter.py:15-16`). Because `routes.py:11` builds the orchestrator at import time, the whole app fails to start. **[Verified]** `AttributeError: 'TwelveDataAdapter' object has no attribute 'logger'`.

### 4.2 High — financial and data correctness

5. **No timestamps or provenance on prices.** The Finnhub quote's `t` field is discarded (`finnhub_adapter.py:38-46`), and `PriceData` has no `as_of` or `source` (`schemas.py:36-46`). Yet the README advertises "real-time". With a 5-minute cache (`finnhub_adapter.py:33`), a price can be over 5 minutes old, or from a previous session, with nothing to show it.
6. **Silent cross-provider fallback.** Price falls back Finnhub → Yahoo → Twelve Data (`ticker_price_agent.py:20-57`). History falls back Alpha Vantage → Twelve Data → Yahoo (`ticker_price_change_agent.py:34-62`). These sources differ in delay, adjustment and session conventions, and the user is never told which one was used (`data_source` is dropped before the response).
7. **Unadjusted prices.** Alpha Vantage `TIME_SERIES_DAILY` is split- and dividend-unadjusted, while Yahoo `history()` auto-adjusts by default. So the same query can return different percentages depending on which fallback fired, and periods spanning a split are wrong. **[Inferred]**
8. **Unit errors in period selection.** `days_ago` is converted to weeks (`alpha_vantage_adapter.py:193`) or months (`:199`), then reused as calendar days (`:220`) and in the period label (`:283`). Twelve Data and Yahoo index trading-day rows as if they were calendar days (`twelve_data_adapter.py:118-124`, `yahoo_finance_adapter.py:64-70`). Alpha Vantage results carry no `data_source` (`:282-293`).
9. **News step fails on mixed timestamp types.** Finnhub and Marketaux return `datetime` objects while Yahoo returns ISO strings. Sorting them together raises `TypeError`, and the entire news result is discarded (`ticker_news_agent.py:66-70`). **[Verified]** with stubs. Whether it triggers live depends on whether yfinance returns news in the expected shape. **[Suspected]** yfinance ≥0.2.5x changed the news payload structure.
10. **Fake freshness in news.** A failed Marketaux timestamp parse sets `published_at = now()` (`marketaux_adapter.py:62-65`). A missing Yahoo publish time becomes the Unix epoch (`yahoo_finance_adapter.py:117`). Timestamps are naive, and they mix local time with UTC.
11. **The "today" change is mislabelled.** The period "open" is actually the previous close (`main_orchestrator.py:174-177`). The Yahoo quote computes `change` with 0 defaults and multiplies `regularMarketChangePercent` by 100 (`yahoo_finance_adapter.py:33-34`). **[Suspected]** Yahoo already reports that field in percent units.
12. **Meaningless confidence and sentiment** (§2.6).

### 4.3 High — reliability and performance

13. **Worst-case latency is minutes.** Every call has a 30 s timeout with 3 tenacity attempts and 4–10 s back-off (`base_adapter.py:13-15`), multiplied across sequential three-provider fallbacks and two LLM calls. There is no overall request deadline.
14. **Blocking I/O on the event loop.** `yfinance` is synchronous but is called inside `async` functions (`yahoo_finance_adapter.py:24-27, 53-55, 108-109`). One slow Yahoo call stalls every request on that worker.
15. **The cache is incorrect for production use.**
    - Keys use Python's salted `hash()` plus the adapter instance's `repr` (`cache.py:61`), so keys differ per process and per restart. **[Verified]** Two runs gave different `hash('AAPL')`. Redis entries are therefore never reused across workers.
    - Failure results such as `[]` are cached for up to 30 minutes.
    - The local cache ignores the requested TTL and always uses 300 s (`cache.py:12`).
16. **Leaked HTTP clients.** Each adapter instance creates an `httpx.AsyncClient` that is never closed. Several methods also open a second ad-hoc client per call (for example `alpha_vantage_adapter.py:40`).
17. **Errors are swallowed.** Errors turn into `None` or `[]` at every layer. Callers cannot tell "no data" from "provider down" from "quota exceeded".

### 4.4 Medium — security and operations

18. **Error details leak** to clients (`routes.py:25`, `main_orchestrator.py:238`).
19. **Wildcard CORS with credentials** (`main.py:26-32`).
20. **Prompt injection surface.** The raw user query is interpolated into prompts (`gemini_adapter.py:36, 83, 147`). This is low impact today because no tools run and no secrets sit in the prompt, but it matters once summaries are shown to other users or tools are added.
21. **Deprecated APIs.** `@app.on_event` (`main.py:37-44`), `datetime.utcnow` (`schemas.py:76`), pydantic v1 `validator` and `class Config` (`schemas.py:1,31`, `config.py:21`).
22. **ADK layer issues.** It builds five sub-`Agent` objects that are never used (`adk_agents/*.py`). `root_agent: ClassVar[bool]` has no effect (`agent.py:12`). The model is hard-coded to a retired Gemini version.

## 5. Checks performed

All checks ran against a scratch venv outside the repo (Python 3.12.10, `%TEMP%\sav312`). No provider or LLM calls were made.

| Command | Outcome |
|---|---|
| `pip install -r requirements.txt` in a long-path scratchpad venv | **Failed**: Windows MAX_PATH limit on an lxml resource file. This is an environment blocker, not a repo defect. |
| Same, in the short-path venv `%TEMP%\sav312` | Succeeded; resolved versions listed in §2.1. |
| `python -m pip check` | "No broken requirements found." |
| `python -m compileall -q src adk_agents main.py adk_main.py` | OK |
| `python -c "import main"` with no API keys in the environment | **Failed**: `AttributeError` at `twelve_data_adapter.py:11` (finding 4). |
| `import main` with dummy keys, then TestClient `GET /`, `/api/v1/health`, `/api/v1/supported-queries`, `/openapi.json` | All returned 200. |
| `python -c "import adk_main"` with dummy keys | OK; the root agent class is `StockAnalysisAgent`. |
| `python -m pytest -q` | "no tests ran", **exit 5**. |
| Offline end-to-end harness (scratchpad `trace_e2e.py`) | Results in §3. |
| Offline news-merge harness | `TypeError` reproduced (finding 9). |
| Lint and type check | Not run. The repo has no lint or typecheck configuration, so any result would reflect tool defaults rather than repo conventions. |

Side effect: importing the app created `__pycache__/` directories, which are git-ignored and were removed after the checks.

## 6. Reuse vs. redesign

| Component | Verdict | Reason |
|---|---|---|
| Adapter-per-provider pattern (`base_adapter.py`) | **Refactor** | The idea is right. It needs typed return models with `source`, `as_of` and `received_at`; explicit error types; one shared client; per-provider quota budgets; and no silent fallback. |
| Finnhub, Twelve Data and Alpha Vantage adapters | **Mostly replace** | Free tiers do not permit commercial display (see [03](03-market-and-tooling-research.md)). Keep them as dev-only adapters behind the same interface. |
| yfinance adapter | **Retire from the product path** | Unofficial scraping with personal-use terms. Keep it for local exploration only. |
| Marketaux adapter | **Replace** with a news source licensed for display | [03 §E](03-market-and-tooling-research.md). |
| `MainOrchestrator` keyword and timeframe parsing | **Retire** | Replaced by explicit, structured requests from a UI (ticker plus window), not free-text parsing. |
| Gemini adapter and prompts | **Replace** | Use a grounded-summary component with a strict JSON schema, citations to evidence IDs, abstention and evals ([06 §5](06-quantitative-validation.md#5-llm-explanations-evaluation)). |
| `TickerNewsAgent` dedup idea | **Refactor** | Keep the idea; use normalised UTC timestamps and URL- or ID-based dedup. |
| FastAPI app, pydantic models | **Keep and refactor** | A good base. Modernise: lifespan, settings, auth, error handling. |
| Cache utility | **Replace** | Deterministic keys, a TTL per data class, never caching failures, and explicit staleness. |
| ADK layer | **Retire for the MVP** | Adds LLM tool-routing nondeterminism with no product need. Revisit only as a separate "research chat" experiment. |
| `README.md` capability claims | **Rewrite** in the implementation phase | Claims must match verified behaviour. |

## 7. Inspection coverage and exclusions

- **Read in full:** all 39 tracked files (35 Python files; 3,618 lines per `wc -l`). This covers every `.py` file, `README.md`, `requirements.txt`, `.gitignore`, `LICENSE`, plus the git history of `.gitignore` and `.env`.
- **Inventoried, not reviewed as product code:**
  - `.serena/` (untracked; Serena MCP project config, left untouched);
  - `.remember/` (local tool state, untracked, left untouched);
  - `.git/`;
  - the installed site-packages in the scratch venv.
- **Not present:** datasets, binaries, generated code, vendored dependencies and build outputs.
- **Not done:** calls to live providers or the LLM (by design: it avoids spending quota and sending data externally); load testing.
