# StockAnalysis → Production Product: Thesis & Roadmap

_Research date: 2026-09-24. Star counts and prices are snapshots and change often. Items marked **[unverified]** come from a single secondary source; check them before relying on them._

---

## 1. TL;DR

**What it is today:** a FastAPI + Gemini demo, with a Google ADK wrapper. It turns a question like "why did TSLA drop?" into five steps: find the ticker, fetch the quote, fetch the news, compute the % change, and have the LLM write a summary. It covers US equities only. It is about 3.6k lines of Python, has no tests, and has several correctness bugs (§2.3).

**The problem:** that pipeline is now a commodity. TradingAgents (~108k★), ai-hedge-fund (~64k★), OpenBB (~73k★), Perplexity Finance ($0–20/mo) and every broker's MCP server already do "ticker → price → news → LLM paragraph" for free.

**The thesis:** turn it into an **auditable, multi-asset research copilot for stocks, ETFs and bonds**. The rule is: _LLMs plan and narrate; deterministic code computes every number; every number carries a source and an as-of timestamp._ It would ship with:

1. **A point-in-time data layer** (Parquet/DuckDB → TimescaleDB) fed by licensed providers, SEC EDGAR, FRED and Treasury.
2. **Deterministic analytics modules:**
   - Equity: fundamentals, valuation, technicals, factor scores.
   - ETF: holdings, overlap, cost, tracking.
   - Bonds: yield curve, duration, convexity, spread, via rateslib/QuantLib.
   - Portfolio: risk and optimization via skfolio/Riskfolio.
3. **An agent layer** that calls these tools, cites sources, and exposes everything as an **MCP server** and a REST API.
4. **Leakage-safe evaluation.** Test only on data after the model's knowledge cutoff, keep a public paper-trading track record, and trace every run in Langfuse.
5. **Compliance by design:** impersonal research by default, AI-use disclosure, full audit log, and execution only through regulated brokers (Alpaca / IBKR / Zerodha Kite).

**The wedge:** ETFs and bonds are badly served by open-source agents. Retail investors, especially in India, and small RIAs pay $20–80/mo for trustworthy, explainable, cited analysis. They do not pay for chat alone.

---

## 2. What the repository is today

### 2.1 Architecture (as built)

```
POST /api/v1/analyze {query}
  └─ MainOrchestrator
       1. GeminiAdapter.extract_intent_and_ticker      (LLM call #1; hard-coded 9-company dict first)
       2. TickerIdentificationAgent → Finnhub search/profile (+ word-by-word fallback)
       3. TickerPriceChangeAgent  → AlphaVantage → TwelveData → Yahoo   (sequential)
       4. TickerPriceAgent ∥ TickerNewsAgent
            price: Finnhub → Yahoo → TwelveData
            news : Finnhub + Marketaux + Yahoo, title-similarity dedupe, top 15
       5. TickerAnalysisAgent → GeminiAdapter.analyze_stock_movement  (LLM call #2)
  └─ AnalysisResult (summary, insights, sentiment, confidence, price, news)

adk_agents/  – same functions wrapped as Google ADK FunctionTools + root agent
```

The "agents" are deterministic async wrappers. Only two LLM calls happen. That is fine, but it means the "multi-agent" label is marketing.

### 2.2 Strengths worth keeping

- The adapter pattern with multi-provider fallback (`src/adapters/`), plus tenacity retries.
- A two-tier cache (in-process TTL + optional Redis).
- A clean agent contract: `BaseAgent.execute` → `AgentResponse` with timing.
- Parallel fan-out for news and price.
- An ADK wrapper that is an easy path to agent UIs and A2A.

### 2.3 Verified defects (fix before building anything on top)

| # | Issue | Where | Impact |
|---|---|---|---|
| 1 | `news_items` is passed to `analyze_stock_movement` but **never put into the prompt** | `src/adapters/gemini_adapter.py` | "Why did X drop?" answers are ungrounded. The model guesses causes. |
| 2 | Alpha Vantage, Twelve Data and Marketaux adapters call `self.logger` **before** `super().__init__()` | `alpha_vantage_adapter.py`, `twelve_data_adapter.py`, `marketaux_adapter.py` | If one key is missing, the app raises `AttributeError` at import. This defeats the "graceful fallback" design. |
| 3 | Deprecated `google-generativeai` SDK; `gemini-1.5-flash` is retired | `config.py`, `adk_agents/agent.py` | Will break. Migrate to `google-genai` and a current model. |
| 4 | yfinance is called synchronously inside `async` functions | `yahoo_finance_adapter.py` | Blocks the event loop under load. |
| 5 | Yahoo `regularMarketChangePercent * 100` | `yahoo_finance_adapter.py` | Likely 100× wrong. yfinance already returns a percent. **[verify]** |
| 6 | The general intent path calls `json.loads(response.text)` without stripping code fences | `gemini_adapter.py` | This often fails and drops to the word-guess heuristic. |
| 7 | The cache key is `hash(str(args))`, which includes `self` repr and Python's per-process hash seed | `utils/cache.py` | Redis entries are never shared across workers. `_generate_key` (md5) is unused. |
| 8 | The LLM invents `confidence_score` and `sentiment` | `gemini_adapter.py` | Numbers look precise but have no basis. |
| 9 | No tests, CI, Dockerfile, auth or disclaimers; CORS is `*` with credentials; httpx clients are never closed | repo-wide | Not production-ready despite the README claim. |
| 10 | US equities only; `TwelveData.get_technical_indicator` and Finnhub financials, insider and earnings endpoints are unused | adapters | Much of the value is already wired in but not used. |
| 11 | Alpha Vantage `outputsize=full` is premium on the free tier **[verify]**; the free tiers of Yahoo, Alpha Vantage, Finnhub and Marketaux forbid commercial redistribution | adapters | Legal blocker for a paid product (§7). |

---

## 3. Landscape: who already does this

### 3.1 Open source

| Project | ★ (Sep 2026) | Core idea | Lesson for us |
|---|---|---|---|
| [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) | ~108k | LangGraph "trading firm": analysts, then a bull/bear debate, then trader, risk and PM | The debate pattern is popular, but costs many tokens. They only recently added look-ahead filtering. |
| [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) | ~64k | About 19 investor-persona agents; **FastAPI + LangGraph + React canvas**; backtester | Almost our stack. Its moat is UX, not analysis. |
| [virattt/dexter](https://github.com/virattt/dexter) | ~28k | Plan → tool → self-validate deep research over filings | Iterative research beats one-shot prompting. |
| [OpenBB](https://github.com/OpenBB-finance/OpenBB) | ~73k | Unified multi-asset data platform + **MCP server** | Use it as a data layer instead of competing with it (check the license **[unverified: AGPL]**). |
| [FinRobot](https://github.com/ai4finance-foundation/finrobot) | ~8k | Equity research; **numbers from deterministic Python, the LLM only narrates** | This is the design principle to adopt. |
| [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) | ~21k | LoRA financial LLMs | Frontier model + tools has mostly overtaken this. Use FinBERT-class models only as cheap sentiment baselines. |
| FinMem / FinAgent / FinCon | papers | Layered memory, multimodal charts, manager–analyst hierarchy | Ideas for later memory and critique loops. |
| [Kronos](https://github.com/shiyu-coder/Kronos) | ~39k | Foundation model for OHLCV candles | Useful for volatility and range priors, not alpha (§5). |

**Finance MCP servers are now table stakes:**
- Alpha Vantage (official)
- FMP
- OpenBB
- Fiscal.ai
- Alpaca (official, trading)
- IBKR (first-party)
- Zerodha Kite (free, hosted)
- Morningstar
- Anthropic's financial-services connectors (FactSet, S&P, Morningstar)

### 3.2 Commercial comparables

| Product | Price | What users pay for |
|---|---|---|
| Perplexity Finance | Free / $20 / $200 **[Max pricing conflicting]** | Cited answers, earnings hub, NL screener (US + **India**) |
| Fiscal.ai (formerly FinChat) | Free / $39–49 / $79–99 | Clean fundamentals and segment KPIs, cited AI chat, API + MCP |
| Koyfin | Free / $39 / $79 / $209–299 advisor | Dashboards, **ETF holdings & screening**, model portfolios |
| Seeking Alpha | ~$299/yr; Pro $2,400/yr | **Quant Ratings** (factor grades) |
| TipRanks | ~$360–600/yr | Analyst and insider track records, Smart Score |
| Danelfin | ~$22–99/mo | **Explainable** 1–10 AI score |
| Composer | $40/mo | Plain-English strategy → backtest → **auto-execute** |
| Bloomberg ASKB | Terminal | Agentic workflows over proprietary data (Feb 2026) |

**What people pay for:**
1. Trustworthy, sourced data.
2. Explainable scores **with a track record**.
3. Watchlist alerts and briefings.
4. Screeners.
5. Idea → execution.

"Chat about a stock" alone is worth $0.

---

## 4. The thesis

### 4.1 Positioning

> **An open-core, auditable research copilot for stocks, ETFs and bonds, where every number is computed, sourced and time-stamped, and every AI claim is cited.**

Three things set it apart, and none of the big OSS agents does all three:

1. **Deterministic numbers, cited narrative.** The LLM never produces a price, ratio, yield or score. It calls tools that return typed values with `{value, unit, source, as_of}`, and it must cite them. A post-check rejects any number in the text that did not come from a tool result.
2. **Multi-asset depth where others are thin:**
   - **ETFs**: look-through holdings, overlap between two ETFs, expense and tracking difference, factor and sector exposure, premium/discount to NAV.
   - **Bonds**: Treasury curve, YTM, duration, convexity, spread to curve, ladder builder, rate-shock scenarios (rateslib/QuantLib).
3. **Honest evaluation.** A point-in-time store plus leakage-safe backtests: evaluate only after the model's cutoff, use counterfactual tests, and keep a public paper-trading ledger. Following the "Profit Mirage" (2025) and Look-Ahead-Bench (2026) work, this is a real credibility moat.

### 4.2 Target users (in order)

1. **Self-directed retail investors (US + India)** who hold ETFs and some bonds or bond ETFs. Jobs: "Explain what moved my watchlist today, with sources." "Compare these 3 ETFs." "Build me a 5-year Treasury ladder."
2. **Small RIAs and research analysts.** Jobs: client-ready research notes, portfolio risk tear sheets, audit trail. In India, registered research analysts must disclose AI use, so the built-in provenance log helps them comply.
3. **Developers and quants** who use the MCP server / API as a clean, point-in-time, multi-asset tool layer for their own agents. This is the open-core funnel.

### 4.3 Product surfaces

- **Ask**: cited Q&A (what the repo does today, done correctly).
- **Watchlist brief**: a daily or intraday digest of movers with attributed causes (news, earnings, macro, sector move, ex-dividend), pushed by email, Telegram or Slack.
- **Screener**: natural language → structured filter over factor and fundamental tables. Show the SQL; never let the LLM pick stocks directly.
- **Compare / X-ray**: stock vs. stock, ETF overlap, fund look-through.
- **Bond desk**: curve viewer, bond calculator, ladder builder, rate-shock P&L.
- **Portfolio**: import CSV or broker (read-only first), then exposures, risk (VaR/CVaR, drawdown), optimization suggestions labeled as hypothetical.
- **Strategy lab** (later): plain-language rule → backtest (vectorbt) → paper trade (Alpaca) → public track record.
- **MCP server + REST API**: every capability above, as tools.

---

## 5. Research to build on (and what not to believe)

- **Agent patterns:**
  - TradingAgents ([2412.20138](https://arxiv.org/abs/2412.20138)) for debate and risk review.
  - FinRobot ([2405.14767](https://arxiv.org/abs/2405.14767)) for deterministic numbers.
  - FinCon (NeurIPS 2024) for manager–analyst hierarchy with self-critique.
  - FinMem for layered memory in watchlist context.
  - Survey: [2605.19337](https://arxiv.org/pdf/2605.19337).
- **Look-ahead bias is the #1 risk:**
  - Glasserman & Lin ([2309.17322](https://arxiv.org/abs/2309.17322)).
  - **Profit Mirage** ([2510.07920](https://arxiv.org/abs/2510.07920)): LLM-agent returns "evaporate" after the knowledge cutoff.
  - Look-Ahead-Bench ([2601.13770](https://arxiv.org/pdf/2601.13770)).
  - Bias via weights *and* RAG context ([2602.14233](https://arxiv.org/html/2602.14233v1)).
  - Mitigation ([2605.24564](https://arxiv.org/html/2605.24564)).

  → Every stored document and price gets `available_at`, and every backtest query filters on it.
- **Benchmarks to run in CI / nightly:**
  - FinanceBench (QA over filings).
  - FinBen.
  - InvestorBench ([2412.18174](https://arxiv.org/abs/2412.18174)): stocks, crypto, **ETFs**.
  - StockBench ([2510.02209](https://arxiv.org/pdf/2510.02209)): contamination-free.
  - Live: Agent Market Arena ([2510.11695](https://arxiv.org/abs/2510.11695)), LiveTradeBench ([2511.03628](https://arxiv.org/abs/2511.03628)).
- **Time-series foundation models:**
  - Kronos ([2508.02739](https://arxiv.org/abs/2508.02739)), TimesFM 2.5, Chronos-2, Moirai, Lag-Llama.
  - Independent evaluations find **negative out-of-sample R² on daily returns and ~50% direction accuracy**.
  - Use them only for **volatility and range bands and scenarios**, shown as uncertainty, never as "the price will be X".
- **Sentiment:** FinBERT as a cheap, deterministic baseline score per headline. Use the LLM for *event classification* (earnings, guidance, M&A, litigation, macro) rather than a vague "sentiment".

---

## 6. Target architecture

```
                ┌──────────── Clients ────────────┐
                │ Web (Next.js) · Telegram/Slack  │
                │ MCP clients (Claude, ADK, IDEs) │
                └──────┬───────────────┬──────────┘
                  REST/SSE          MCP server (FastMCP)
                ┌──────┴───────────────┴──────────┐
                │ API gateway: FastAPI, auth (JWT/ │
                │ API keys), quotas, audit log     │
                ├──────────────────────────────────┤
                │ Agent layer (ADK or LangGraph)   │
                │  planner → tool calls → verifier │
                │  (number-provenance check,       │
                │   citation check, disclaimers)   │
                ├──────────────────────────────────┤
                │ Deterministic analytics (pure py)│
                │  equity · etf · bonds · portfolio│
                │  technicals · factors · events   │
                ├──────────────────────────────────┤
                │ Point-in-time data layer         │
                │  Parquet/DuckDB → Timescale/PG   │
                │  pgvector for filings/news RAG   │
                │  every row: source, as_of,       │
                │  available_at                    │
                ├──────────────────────────────────┤
                │ Ingestion (Prefect/Dagster)      │
                │  provider adapters (existing     │
                │  pattern) + symbology (OpenFIGI) │
                └──────────────────────────────────┘
   Observability: Langfuse (LLM traces/evals) · OpenTelemetry · Sentry
   Execution (opt-in, later): Alpaca paper → Alpaca/IBKR/Kite live via their MCP/APIs
```

**Key design decisions:**
- **Keep the adapter + fallback pattern**, but put it behind a normalized `Instrument` model (FIGI/ISIN/CUSIP + exchange + asset class) instead of bare US tickers.
- **Ingest, don't proxy.** Load data on a schedule into the store, and have agents read the store. This gives determinism, speed, point-in-time replay, and lower vendor cost.
- **Structured output everywhere.** Use schema-constrained generation with Pydantic models. Drop the regex JSON parsing.
- **The LLM is replaceable.** Put Gemini, Claude and GPT behind one interface; ADK and LangGraph both support this. Choose per task (cheap model for routing, strong model for synthesis).
- **The verifier step is mandatory.** Extract every number in the draft and match it to a tool output within a tolerance, or the answer is regenerated. This is cheap to build and is the main trust feature.

---

## 7. Integration catalog (what to plug in, by priority)

### 7.1 Data

| Need | Recommended | Notes |
|---|---|---|
| US equities/ETFs EOD + intraday | **Massive (formerly Polygon)**, Tiingo, Alpaca data | Replace yfinance before charging money. Yahoo's ToS forbids commercial use. |
| Fundamentals / estimates | **FMP**, EODHD, Fiscal.ai API | FMP also offers an MCP server |
| Filings (10-K/Q, 8-K, Form 4, 13F, N-PORT) | **SEC EDGAR + `edgartools`** | Free. Send a User-Agent and respect ~10 req/s. N-PORT gives fund holdings **[verify edgartools N-PORT support]**. |
| Macro | **FRED**, BLS, BEA | Free. Check restrictions on third-party FRED series. |
| Treasury curve & auctions | **Treasury daily par-yield feed**, Fiscal Data API, TreasuryDirect API | Free. The backbone of the bond module. |
| Corporate bonds | FINRA TRACE (licensed), EODHD, Open Source Bond Asset Pricing (academic) | Start with Treasuries and bond ETFs; add corporate bonds when licensed. |
| ETF holdings | Issuer CSVs, N-PORT, FMP/EODHD | Look-through, overlap and exposure |
| Symbology | **OpenFIGI** | Free. Maps ticker ↔ FIGI ↔ ISIN/CUSIP. |
| India | Zerodha Kite Connect / Kite MCP, NSE/BSE via licensed vendors | Exchange data fees apply |
| News | Keep Finnhub/Marketaux; add Benzinga or Massive news | Store `published_at` / `available_at` |

### 7.2 Analytics

- **Technicals**: TA-Lib (or pandas-ta; check maintenance).
- **Portfolio & risk**: **skfolio** (sklearn-style, cross-validated), Riskfolio-Lib (CVaR, risk parity), PyPortfolioOpt, **QuantStats** (tear sheets). Use empyrical forks only.
- **Fixed income**: **rateslib** (curves, bonds, AD greeks); **QuantLib** for breadth.
- **Backtesting**: **vectorbt** for fast research; **NautilusTrader** or **LEAN** when the same code must run backtest → live.
- **Forecast bands**: Chronos-2 / TimesFM / Kronos, served offline and batched. Show them only as uncertainty ranges.
- **Sentiment/events**: FinBERT baseline plus an LLM event classifier.

### 7.3 Platform

- **Storage**: DuckDB + Parquet (phase 1) → TimescaleDB/Postgres + pgvector (phase 2). QuestDB only if we ever handle ticks.
- **Orchestration**: Prefect (simple) or Dagster (asset lineage and data-freshness checks).
- **LLM ops**: **Langfuse** (traces, prompt versions, eval datasets); golden-question regression suite in CI.
- **App**: FastAPI (keep), SSE streaming, Redis (fix the key scheme), Postgres for users and watchlists, Docker + GitHub Actions, OpenTelemetry + Sentry.
- **Agent interop**: **FastMCP** to expose our tools; consume the Alpaca, IBKR and Kite MCP servers for execution; ADK A2A optional.

---

## 8. Trust, evaluation & compliance

### 8.1 Evaluation harness (a product feature, not an afterthought)

1. **Golden Q&A set**: about 200 questions with ground-truth numbers from the store. Score numeric exactness, citation validity and refusal correctness on every PR.
2. **Provenance check rate**: % of answer numbers matched to tool outputs. Target 100%, and block the answer otherwise.
3. **Leakage tests**: evaluate signals only on dates after the model's cutoff; run counterfactual perturbation (FactFin-style); log the model version with every signal.
4. **Public track record**: every score or signal is logged at issue time (immutable) and scored later. Show hit rate and calibration openly, as TipRanks and Danelfin do.

### 8.2 Compliance (get counsel; this is orientation, not legal advice)

- **US:**
  - Stay inside the **publisher's exclusion** (*Lowe v. SEC*): impersonal, regularly published and non-personalized content. Portfolio-specific "buy X" advice or auto-execution likely requires RIA or broker-dealer status, or a regulated partner.
  - The SEC's predictive-analytics rule was **withdrawn in June 2025**, but anti-fraud, Marketing Rule and "AI-washing" enforcement still apply.
  - FINRA RN 24-09 and the 2026 oversight report: chatbot output may count as a communication, so supervise and retain it.
  - Hypothetical-performance disclaimers are required on backtests.
- **India:**
  - SEBI Research Analyst rules (2024 amendment) require **AI-use disclosure**; recommendations offered as a business need RA registration.
  - **Retail algo framework is fully mandatory from 2026-04-01**: broker as principal, empanelled algo provider, exchange algo-ID, static IP. Any auto-trade must go through that path.
  - Finfluencer restrictions apply.
- **Data licensing:**
  - Free tiers (Yahoo, Alpha Vantage, Finnhub, Twelve Data, Marketaux) generally prohibit commercial display or redistribution.
  - Budget for display licenses and exchange non-pro/pro fees.
  - EDGAR, FRED, Treasury and OpenFIGI are free.
- **Built in by default:**
  - Disclaimers on every answer.
  - Source and as-of shown on every number.
  - Immutable audit log of prompt, tools, data and output.
  - No personalization in the free tier.
  - Execution strictly opt-in, paper trading first.

---

## 9. Roadmap

| Phase | Scope | Exit criteria |
|---|---|---|
| **0. Stabilize (1–2 wks)** | Fix §2.3 defects #1–8. Migrate to `google-genai`. Add pytest with recorded HTTP fixtures (respx/vcrpy). Add Dockerfile, GitHub Actions (ruff, mypy, tests), `.env.example`, disclaimers. | CI green. App boots with any subset of keys. News actually grounds answers. |
| **1. Trustworthy core (3–5 wks)** | `Instrument` model + OpenFIGI. DuckDB/Parquet point-in-time store with ingestion jobs (EOD prices, EDGAR fundamentals, FRED, Treasury curve). Typed tool layer with `{value, source, as_of}`. Verifier step. Langfuse. Golden eval set. | 100% number provenance on golden set; p95 latency under 6 s |
| **2. Multi-asset (4–6 wks)** | ETF X-ray (holdings, overlap, costs). Bond desk (curve, calculator, ladder, shocks via rateslib). Equity factor scores. Technicals via TA-Lib. NL screener → SQL. | Cited Compare/X-ray/Bond pages; eval coverage per module |
| **3. Product surfaces (4–6 wks)** | Auth, watchlists, daily brief (email/Telegram), streaming UI, **MCP server**, portfolio import + risk tear sheet (skfolio/QuantStats). Swap in licensed data providers. | First paying users; MCP listed in registries |
| **4. Strategy lab & execution (later)** | vectorbt backtests with leakage guards, Alpaca paper trading, public signal ledger. Live execution only via regulated broker APIs/MCPs (Alpaca, IBKR, Kite with the SEBI algo framework). | 6+ months of post-cutoff live track record before any marketing of performance |

### Monetization sketch

- **Open-core**: MIT/Apache engine + MCP server (the developer funnel).
- **Hosted Pro**: $15–30/mo, with watchlist briefs, ETF/bond tools, portfolio risk, higher limits.
- **Advisor/RA tier**: $100–300/mo, with white-label notes, audit export, AI-disclosure reports.
- **API/MCP usage pricing** for developers.

---

## 10. What *not* to do

- Don't sell "AI picks stocks and beats the market". The research (Profit Mirage, TSFM re-evaluations) says this rarely survives out of sample, and regulators treat it as AI-washing.
- Don't build ever more persona or debate agents. The token cost rises without a measurable accuracy gain, and TradingAgents and ai-hedge-fund already own that niche.
- Don't ship yfinance or free-tier data in a paid product.
- Don't let the LLM output numbers, scores or "confidence" that it did not get from a tool.

---

## 11. Immediate next steps (concrete)

1. Put `news_items` (title, source, time, summary) into the analysis prompt and require citations `[n]`.
2. Move the `self.logger` usage after `super().__init__()` in three adapters (or set the logger first).
3. Wrap yfinance calls in `asyncio.to_thread`; verify the % scaling.
4. Migrate to `google-genai` with `response_schema` Pydantic models; remove the hard-coded company dict in favor of OpenFIGI/Finnhub search.
5. Fix the cache keys (stable md5 of the function's qualified name + args excluding `self`).
6. Add `tests/` with recorded fixtures, a Dockerfile and a CI workflow.
7. Prototype the `Instrument` + DuckDB store + Treasury curve ingestion as the first multi-asset slice.
