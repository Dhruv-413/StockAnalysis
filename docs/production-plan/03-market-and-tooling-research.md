# 03 — Market and Tooling Research (synthesis)

← [Index](README.md) · Previous: [02 Product thesis](02-product-thesis.md) · Next: [04 Real-time data strategy](04-real-time-data-strategy.md)

This page summarises what the four research appendices found and what the plan does with it. The appendices carry the per-claim URLs, publication dates and confidence ratings (H = primary page read, M = secondary or summarised, L = single or conflicting source). All sources were accessed **2026-09-24**.

- [research/market-data.md](research/market-data.md): vendors, exchange licensing, reference data, news, Gemini
- [research/products.md](research/products.md): competitors, open-source licences, regulation
- [research/infrastructure.md](research/infrastructure.md): storage, queues, calendars, deployment, auth, notifications, LLM tooling, brokers
- [research/papers.md](research/papers.md): research papers and evaluation methods

**Software licence ≠ data rights.** Throughout, a tool's licence (MIT, Apache, AGPL, Commons Clause) governs its *code*. The right to display or store the *data* it retrieves comes from vendor terms and exchange agreements.

---

## A. Comparable commercial products

| Product | Relevant capability | Price (list, verified unless noted) | Implication |
|---|---|---|---|
| Robinhood Cortex Digests | "What may be driving" a stock; popular stocks only | Robinhood Gold, $5/mo (H) | Commoditised for retail, and tied to the broker |
| Schwab Portfolio Insights | AI summaries of the 5 biggest movers among a client's holdings | Free to self-directed clients since May 2026 (H) | No per-claim citations; carries a "may be hallucinated" disclaimer |
| Perplexity Finance | Cited answers; move alerts that trigger an AI query | Free; Pro $20 (H/M) | Closest free substitute. No audit ledger, export or multi-client workflow |
| Benzinga Pro / WIIM | Fast news; one-line "why is it moving" feed | $37–197/mo; WIIM sold wholesale (H) | Competes on speed, not on evidence |
| TradingView | Price and technical alerts; watchlist alerts only on Premium (2) and Ultimate (15) | $12.95–199.95/mo billed annually (H) | Alerts say what moved, not why |
| Koyfin | Research terminal; Advisor tiers | $39–299/mo (H) | Shows that pro-am and adviser users pay |
| Snowball Analytics | Portfolio tracker with "Why is it moving" | $14.99/mo (H) | The "why" feature is a low-price bundle add-on |
| Unusual Whales, Stocktwits, Finviz Elite, Seeking Alpha, Fiscal.ai, Yahoo Finance Plus, Morningstar Investor, Portfolio Visualizer, Composer, QuantConnect, TrendSpider, AInvest | See [products §1–5](research/products.md) | Various; some unverified (L) | Crowded outside the evidence-ledger niche |

**Conclusion:** the opening is **auditable, multi-name, broker-agnostic explanation with honest abstention**, for users who publish or advise ([02](02-product-thesis.md)). Re-check Perplexity's feature set every quarter; it is the main threat.

## B. Open-source projects and licences

| Project | Licence | Status / relevance |
|---|---|---|
| OpenBB ODP | **AGPL-3.0** | Useful data connectors. AGPL obligations apply if a modified version is run as a hosted service. Not adopted. |
| Ghostfolio | AGPL-3.0 | Portfolio tracker. Not adopted. |
| NautilusTrader | LGPL-3.0 | The candidate if execution is ever built ([05 §9](05-target-architecture.md#9-future-execution-separation-not-in-mvp)) |
| LEAN / QuantConnect | Apache-2.0 | Backtesting reference. Later only. |
| vectorbt | Apache-2.0 **+ Commons Clause** | Internal research only. Risky if backtesting becomes a paid feature. |
| backtrader | GPL; no release since 2023 | Avoid |
| Riskfolio-Lib (BSD-3), skfolio, QuantStats (Apache-2.0), empyrical-reloaded | Permissive | Candidates for later portfolio or risk views, as golden-test references |
| TradingAgents, FinRobot (Apache-2.0), FinGPT, ai-hedge-fund (MIT) | Permissive | Research demos. Their evaluations don't meet [06 §7](06-quantitative-validation.md#7-evidence-required-before-later-features-ship). Not adopted. |

## C. Market data providers and exchange connectivity

Main findings ([market-data §A–C](research/market-data.md)):

- **The repo's providers are unusable for a paid product.**
  - Finnhub: personal use even at $3,500/mo.
  - Alpha Vantage: 25 requests/day free; `outputsize=full` is premium.
  - Twelve Data: display rights start at the $499 Venture plan.
  - Marketaux: non-commercial.
  - yfinance and Yahoo: the terms forbid scraping and commercial use.
- **Candidates for display-licensed data:**
  - Intrinio Startup: commercial display rights; FMV real-time plus Cboe One delayed.
  - Databento: US Equities Mini is fee-free; `EQUS.SUMMARY` gives full-volume delayed or EOD data. Whether it allows display under the Standard plan is ⚠.
  - Massive (formerly Polygon.io, renamed 2025-10-30): Business plan $2,499 with FMV; add-ons ⚠.
  - Twelve Data Venture ($499; exchange-fee inclusion ⚠).
  - Proprietary feeds: Nasdaq Basic, Cboe One.
- **Exchange economics.**
  - Delayed (15 min) data has no per-user display fees.
  - Real-time SIP costs $1 per tape for non-pro users and about $92 for pro users, plus redistribution, access and non-display fees.
  - The CT Plan takes effect 2027-04-01, with the DataCT agreement due by 2027-03-01.
  - Pro-am users are often "professional".
- **Market-structure changes to track:**
  - new round-lot definition (live 2025-11-03);
  - expected 23/5 trading (~2026-12-06);
  - IEX Cloud shut down on 2024-08-31.
- **"Indicative/FMV" feeds are modelled, not trades.** Label them as such, or an alert may contradict the actual prints.

Decision: [ADR-002](adr/ADR-002-delayed-first-market-data.md). Detail: [04](04-real-time-data-strategy.md).

## D. Reference, fundamentals, filings, bonds

- **SEC EDGAR** (`data.sec.gov`):
  - no key needed;
  - ≤ 10 requests/second, with a declared User-Agent;
  - content is public and redistributable;
  - near-real-time.

  This is the **core evidence source** of the MVP.
- **OpenFIGI:** free symbology (25 mapping requests/minute without a key). This gives the internal instrument ID ↔ FIGI mapping.
- **FRED:** third-party series need the owner's permission for commercial use, so use government series only. Not needed for the MVP.
- **Corporate actions:** available from Massive, Databento, Intrinio and EODHD. Massive returns split-adjusted history by default, so backfills must request `adjusted=false` to keep the raw-bar table pure ([infrastructure §4](research/infrastructure.md)).
- **ETF holdings:** public N-PORT filings are quarterly with a lag of about 60 days. Monthly public N-PORT has been delayed to 2027-11-17. Issuer websites publish daily, but their terms vary.
- **Bonds:**
  - FINRA TRACE real-time costs $1,500/mo per data set; display to non-pro users is free.
  - MSRB subscriptions cost $5.5k–45k.

  Bonds are **excluded from the MVP**; [06 §3](06-quantitative-validation.md#3-asset-class-specifics) lists what they would require.

## E. News licensing

- Finnhub and Marketaux news need vendor approval before display.
- Benzinga explicitly licenses display (quote required). Massive's Benzinga add-on is for individual use; the business version is priced on request.
- **Pilot rule:** show headline, source, time and link. Summarise only from licensed text or from EDGAR.
- Whether an LLM summary of licensed news counts as permitted "derived data" is ⚠ and needs a written answer from the vendor.

## F. LLM provider status

- `gemini-1.5-flash`, which the repo uses, is **retired**: the -002 version was retired on 2025-09-24.
- `google-generativeai` is **archived**, with support ended on 2025-11-30. Migrate to `google-genai`.
- Current flash-tier models run from `gemini-2.5-flash-lite` ($0.10 input / $0.40 output per 1M tokens) up to `gemini-3.8-flash` ($0.75 / $3.75 until 2026-12-31). Only the 3.7/3.8 prices were read on a primary page.
- **The free tier uses submitted content to improve Google's products**, so use the paid tier for anything that touches users.
- Structured output is available on both candidates: Gemini `response_json_schema`, and Claude structured outputs (GA, `output_config.format`). The plan keeps a provider-agnostic interface and evaluates both on the gold set ([ADR-004](adr/ADR-004-llm-role-grounded-only.md)).
- **Evaluation tooling:**
  - DeepEval, in CI.
  - Ragas: the repo has moved and activity has slowed.
  - promptfoo: now owned by OpenAI, and a Node CLI.
  - The plan's primary metrics (ALCE-style citation precision and recall, FActScore-style claim support) are simple enough to implement directly ([06 §5](06-quantitative-validation.md#5-llm-explanations-evaluation)).

## G. Infrastructure tooling (selected)

| Need | Choice | Why | Alternative / upgrade trigger |
|---|---|---|---|
| Time-series storage | Managed Postgres, natively partitioned by session date | Simplest; relational and time-series data in one place | TimescaleDB (Tiger Cloud from $30/mo, or self-hosted) once past ~50 GB or 100–200M rows. Managed Fly/Neon/RDS/Supabase-PG17 lack Timescale's TSL features. |
| Queue / jobs | Outbox + LISTEN/NOTIFY + Procrastinate; APScheduler 3.11 | Uses Postgres only | Redis Streams or NATS JetStream above a few hundred events per second. arq is in maintenance mode. |
| Calendar | `exchange_calendars` 4.13.2 + an overrides table; pin `tzdata` | Correct 2026 early closes, tested locally | Neither library models 23/5 yet |
| Data quality | pandera + Postgres constraints | Lightweight | Great Expectations moved to Fivetran and GX Cloud shut down. Soda Core is now ELv2. |
| Observability | structlog, Sentry (free → Team $26), OpenTelemetry → Grafana Cloud free tier | Cheap and standard | FastAPI OTel instrumentation is still beta |
| Hosting | Fly.io (iad) or Render/Railway | Always-on workers; stop-before-start deploys for the singleton ingestor | Not Cloud Run (60-minute WebSocket cap); App Runner closed to new customers on 2026-04-30 |
| Auth | Clerk (free up to 50k monthly *retained* users) | $0 at pilot | Auth0 costs about $350/mo at 5k users; fastapi-users is in maintenance mode |
| Email / push | Postmark ($15/10k) or Resend; Web Push (VAPID) | Good transactional deliverability | SMS deferred because of US 10DLC registration |
| Cache / pub-sub | None in the MVP | — | Valkey (BSD) rather than Redis 8 (AGPL/RSAL/SSPL tri-licence) if needed |

## H. Research, backtesting, portfolio (later stages)

- **Event studies:** no maintained library exists. Implement the market model directly with statsmodels (MacKinlay 1997).
- **Backtesting:** only under the [06 §7](06-quantitative-validation.md#7-evidence-required-before-later-features-ship) standards. vectorbt for internal use, or LEAN. NautilusTrader if execution is ever added.
- **Portfolio and risk:** skfolio or Riskfolio-Lib, plus QuantStats as golden references.

## I. Broker APIs (later, only if execution is ever pursued)

| Broker | Constraint |
|---|---|
| Alpaca | Paper trading via OAuth is the easiest start. Market data cannot be redistributed. |
| IBKR | OAuth only for licensed organisations or approved vendors |
| Schwab Trader API | Needs a commercial review; refresh token lasts 7 days |
| Tradier | OAuth is partner-only; sandbox data is 15 minutes delayed |

## J. Research papers: what goes where

Full reviews are in [papers](research/papers.md).

| Verdict | Works |
|---|---|
| **MVP** | Event-study methods (MacKinlay 1997; Brown & Warner 1985). Multiple-testing logic for alert thresholds (Harvey, Liu & Zhu 2016). News vs. price-move base rates (Boudoukh et al. 2019; Roll 1988; Cutler, Poterba & Summers 1989; Jeon et al. 2022). Citation and faithfulness evaluation (ALCE, FActScore, AIS; RAGAS as a monitor). FinanceBench as a warning and template. Look-ahead and distraction principles (Glasserman & Lin; Sarkar & Vafa). Larger firms attract more hallucination (Shah et al., COLM 2025). FinBen: use LLMs for extraction, not forecasting. |
| **Later** | Deflated Sharpe ratio and probability of backtest overfitting. Point-in-time LLMs (ChronoGPT, TiMaGPT, DatedGPT, Kelly et al. 2026). Lookahead Propensity audit. LiveTradeBench's forward-only protocol. Survivorship and trading-cost references. |
| **Not in plan** | Lopez-Lira & Tang as a trading signal (fragile to costs of about 20 bp). BloombergGPT, FinGPT. TradingAgents: its Sharpe of 5.6 over 3 months has a standard error of about 8. INVESTORBENCH, Ploutos. |

**Gap:** there is no public benchmark for the faithfulness of "why is this stock moving" explanations, so the plan builds an in-house gold set.
