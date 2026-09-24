# Infrastructure & Quant-Tooling Research: Near-Real-Time US Equity/ETF Watchlist + Explainable Alerts

Research date / access date for all sources: **2026-09-24**. Target: Python 3.12 FastAPI, 1-3 devs, minute-level freshness, 500-5,000 symbols.

**Method.** Package versions and dates come from the PyPI JSON API (`pypi.org/pypi/<pkg>/json`). Repository activity and licenses come from the GitHub API (`gh api repos/...`). Both were queried on 2026-09-24. This data is marked **[PyPI]** / **[GH]**, confidence High. Web-page summaries produced several wrong dates, so none of their dates are used where API data exists.

**Confidence scale for prices and facts:**
- **High:** two or more independent sources agree, or the fact is a primary API or doc quote.
- **Med:** a single official page, fetched once.
- **Med-Low:** an aggregator or third-party blog only.
- **Est:** my own derivation.

---

## 0. Cross-cutting findings that drive the design (read first)

1. **US equities move to 23/5 trading on 2026-12-06.**
   - **Hours:** an overnight session runs 9pm-4am ET and a maintenance pause runs 8-9pm ET. The trading day is 9pm-8pm ET, futures-style, so "Monday" starts Sunday evening. Trades between 9pm and midnight ET count toward the next calendar date. [R40] (Massive blog, pub 2026-08-26, Med)
   - **NYSE Arca:** it filed SR-NYSEArca-2026-53 for extended hours, and its FAQ is v4.0 from Aug 2026. My fetch could not confirm the exact launch date from the primary PDF, and Arca is described as "subject to SEC approval". [R41] (Med-Low on the date)
   - **Implications:**
     - Partition and bucket by **session date**, not UTC or calendar date.
     - Make the session model explicit: overnight, pre, regular, post.
     - Size storage for up to 23 trading hours per day (1,380 min).
     - Neither calendar library models the overnight session yet (see §3).
2. **Market-data websockets allow one connection per key.**
   - Alpaca's market-data stream is commonly limited to 1 concurrent connection; opening more returns error 406. [R42] (Med)
   - Massive (formerly Polygon.io) allows 1 concurrent connection per asset class by default. [R43] (Med)
   - **Design consequence:** run exactly **one ingestor process** that owns the socket and fans out internally (via Postgres, Redis, or NATS). Web workers must never each open their own socket.
   - **Deploy overlap:** PaaS rolling/zero-downtime deploys start the new instance before stopping the old one, which can trip the 1-connection limit. The ingestor should (a) hold a Postgres **advisory lock** (leader election) before connecting, and (b) use a stop-before-start deploy strategy. (Fly/Render/Railway worker deploy-overlap behaviour: unverified.)
3. **Long-lived sockets rule out request-scoped serverless for the ingestor.** Cloud Run *services* cap a websocket at 60 min, bill it as instance-based, and require reconnect logic. [R30] (High, primary doc)
4. **Several managed Postgres providers do not offer TimescaleDB's TSL features** (compression, continuous aggregates, retention policies).

   | Provider | TimescaleDB status |
   |---|---|
   | Neon | Apache-only features, and an old 2.17.1 [R6] |
   | Supabase | Deprecated on PG17 [R7] |
   | RDS | Not supported [R8] |
   | Fly MPG | Not supported; only pgvector and PostGIS [R33] |

   Full TimescaleDB means **Tiger Cloud or self-hosting**.
5. **Windows dev machine.** Python's `zoneinfo` has no system IANA database on Windows. Pin `tzdata` (2026.4, 2026-09-12 [PyPI]) as a runtime dependency.

---

## 1. Time-series / analytical storage

**Sizing (Est).**

| Scenario | Rows/day | Rows/year | Raw size/year | Compressed |
|---|---|---|---|---|
| 5,000 symbols, regular session (5,000 × 390 min) | 1.95M | ~0.49B | **~55-65 GB** | 5-10x smaller (vendor claim; unverified for this schema) |
| 4am-8pm (960 min) | 4.8M | ~1.2B | ~140-160 GB | — |
| 23/5 upper bound (9pm-8pm = 1,380 min) | 6.9M | ~1.74B | ~200-225 GB | — |

- Assumptions: 252 sessions/yr. Per row in plain PG ≈ 24 B tuple header + 4 B line pointer + ~60-70 B data (int security_id, timestamptz, OHLC float8, volume, vwap, trade_count) + ~25-30 B for the `(security_id, ts)` PK index ≈ **110-130 B/row**.
- The 23/5 figure is an upper bound. Real counts are lower because illiquid names don't print every minute.
- At 500 symbols, every figure is 10x smaller (~6 GB/yr for regular hours).
- **At 5k symbols, plain PG crosses the ~50 GB upgrade trigger within the first year.**

| Candidate | Fit for this workflow | Py 3.12 client | Latest (date) | License | Hosting | Cost (managed) | Lock-in / alternatives | Conf | Ref |
|---|---|---|---|---|---|---|---|---|---|
| **PostgreSQL + TimescaleDB** | Best fit. SQL plus relational data (users, watchlists, alerts) in one DB. Hypertables, `time_bucket`, continuous aggregates (1m→5m/1h/1d), columnstore compression, retention | psycopg 3.3.6 (2026-09-18), asyncpg 0.31.0 (2025-11-24), SQLAlchemy 2.0.54 [PyPI] | 2.30.1 (2026-09-17). Supports PG 16/17/18; PG15 dropped in 2.29 | Apache-2.0 core, plus **Timescale License (TSL)** for the `tsl/` dir: compression, CAggs, policies. TSL is free to self-host and forbids offering it as a DBaaS | Self-host (Docker or VM), or Tiger Cloud | Tiger Cloud Performance from **$30/mo** compute plus storage (~$0.177/GB-mo per aggregator), Scale from $36/mo; 30-day free trial | Low: it's Postgres, and you can fall back to native partitioning. Managed choice is effectively Tiger Cloud only | High (license, version); High ($30); Med-Low (storage rate) | R1,R2,R3,R6-R8 |
| **Postgres alone + native partitioning (pg_partman optional)** | Fine for 500 symbols and early 5k. No compression or CAggs, so you roll your own rollup tables or materialized views | same | PG 18 current | PostgreSQL License | Any managed PG. pg_partman is on Neon, Supabase, Render and RDS, but not Fly MPG | See §8 | None | High | R8,R33,R70 |
| **ClickHouse** | Excellent for large scans or aggregates. Overkill at this size; needs a second DB for OLTP; updates and deletes are awkward | clickhouse-connect 1.9.0 (2026-09-22) [PyPI] | v26.9.2.8-stable / v26.8.11.7-lts (2026-09-22) | Apache-2.0 | Self-host or ClickHouse Cloud | Basic ~**$66.52/mo** at 6h/day, ~$186/mo at 24/7 (8 GiB/2 vCPU) | Med (SQL dialect) | High (release); Med-Low (price) | R4,R5 |
| **QuestDB** | Purpose-built for market ticks, with `SAMPLE BY` and ASOF joins. Fast ingest (ILP/QWP). Second DB needed for app data | questdb 5.0.0 (2026-07-27) [PyPI] | 10.0.1 (2026-08-24) [GH] | Apache-2.0 (OSS); Enterprise is commercial | Self-host; QuestDB Enterprise/BYOC | Not verified | Med (non-PG dialect; PG-wire partial) | High (version, license) | R9 |
| **DuckDB + Parquet** | Great for **offline research** and backtests over Parquet exports. Not a live store: one writer *process* at a time (MVCC within that process) | duckdb 1.5.5 (2026-07-22) [PyPI]; 1.4.x is LTS | 1.5.x stable, 1.4.5 LTS (2026-06-17) | MIT | Embedded, or MotherDuck | Free | None (Parquet is portable) | High | R10,R11 |

- **Recommendation:**
  - **Phase 1 (≤500 symbols, regular hours):** plain managed Postgres, with a `bars_1m` table using **native declarative range partitioning by session date**, plus rollup tables.
    - Pre-create partitions from a scheduled job (Procrastinate or APScheduler).
    - Use **pg_partman where the provider offers it.** It is listed on the Neon, Supabase and Render extension pages [R70]. It is **not** available on Fly MPG, which supports only the default PG16 trusted extensions plus pgvector and PostGIS [R33].
  - **Phase 2 (toward 5,000 symbols, extended or 23/5 hours):** move to **Timescale** for compression and continuous aggregates, on **Tiger Cloud** or a self-hosted TimescaleDB container.
  - **Research:** DuckDB reading Parquet exports.
- **When to upgrade:**
  - **Plain PG → Timescale** when any of these holds: the bars table passes ~100-200M rows or ~50 GB; rollup refresh jobs exceed ~30 s per minute cycle; you ingest extended or 23/5 hours for more than 1,000 symbols (Est).
  - **Timescale → ClickHouse or QuestDB** when you store **tick/trade-level data for 5k symbols** (billions of rows per month), or dashboards need sub-second scans across the universe.

---

## 2. Event processing / queues / scheduling

| Candidate | Fit | Latest (date) | License | Hosting | Cost | Notes / lock-in | Conf | Ref |
|---|---|---|---|---|---|---|---|---|
| **Postgres LISTEN/NOTIFY + transactional outbox** | Best first choice: no new infra. Write the alert and the outbox row in the same transaction, NOTIFY as a wake-up, and consumers poll the outbox as the source of truth | PG core | PostgreSQL | Any PG | $0 | NOTIFY payload must be < **8000 bytes** (default). Delivered only on commit; identical notifications within a transaction are folded. **A listener that isn't connected at commit time never receives the notification** (during reconnects, deploys, worker restarts). So NOTIFY is only a wake-up signal, not a queue, and the outbox table is the source of truth. Poolers in transaction mode (PgBouncer) break LISTEN (general knowledge, Med) | High | R12 |
| **Procrastinate** (PG task queue) | Background jobs, retries, periodic tasks, locks, all on the same PG. Async-native, FastAPI-friendly | 3.10.0 (2026-09-23) [PyPI]; Py ≥3.10, PG ≥13 | MIT | Same PG | $0 | Low lock-in | High | R13 |
| **Redis Streams** | Fan-out with consumer groups, low latency, also a cache and pub/sub for websocket push to browsers | redis-py 8.1.0 (2026-07-30); Redis server 8.10.2 (2026-09-17) [GH] | Redis 8: **RSALv2 / SSPLv1 / AGPLv3 tri-license**. **Valkey** 9.1.2 (2026-09-01) is BSD-3 | Managed (Upstash, Render KV, Railway) or self-host | ~$0-10/mo small (Est) | AGPL is fine for internal use; use Valkey if license-averse | High | R14,R15 |
| **NATS JetStream** | Lightweight durable streams, KV, great for fan-out; single Go binary | nats-server v2.15.0 (2026-09-17) [GH]; nats-py 2.16.0 (2026-09-16) [PyPI] | Apache-2.0 | Self-host (tiny) or Synadia Cloud | Self-host ≈ VM cost | Extra moving part; low lock-in | High | R16 |
| **Kafka / Redpanda** | Overkill for 1-3 devs at minute resolution | aiokafka 0.14.0 (2026-04-29); confluent-kafka 2.15.1 (2026-09-10) [PyPI] | Kafka Apache-2.0; Redpanda source-available (BSL) (unverified) | Managed (Redpanda Serverless has a free start; usage-based) | Usage-based | Heavy ops | Med-Low | R17 |
| **arq** | asyncio + Redis jobs | 0.28.0 (2026-04-16) | MIT | Redis | — | **Maintenance-only mode** (README) | High | R18 |
| **Dramatiq** | Solid sync worker model (Redis/RabbitMQ) | 2.2.1 (2026-09-02) | **LGPL-3.0+** | Redis/RabbitMQ | — | Active | High | R19 |
| **Celery** | Mature but heavy; weak asyncio story | 5.6.3 (2026-03-26) [PyPI] | BSD-3 | Redis/RabbitMQ | — | Active | High | R20 |
| **APScheduler** | In-process cron and interval scheduling (e.g., market-open jobs) | Stable **3.11.3 (2026-06-28)**; 4.0 still pre-release (4.0.0a6) | MIT | In-process | $0 | **Don't use 4.x in production** (the project says so) | High | R21 |

- **Recommendation:**
  - One **ingestor** process owns the vendor socket and writes bars to PG.
  - An **evaluator** consumes new bars and writes `alerts` plus an `outbox` row in the same transaction, with NOTIFY as the wake-up.
  - **Procrastinate** handles delivery jobs (email, push, Telegram) with retries.
  - **APScheduler 3.11** (or Procrastinate periodic tasks) runs calendar-driven jobs.
  - Add **Redis/Valkey pub/sub** only when you need to fan live updates out to many web workers over SSE or websockets.
- **When to upgrade:**
  - Move to **Redis Streams** or **NATS JetStream** when outbox throughput exceeds a few hundred events per second, or when you need multiple independent consumers that replay history.
  - Move to **Kafka/Redpanda** only for multi-team, tick-level, multi-day replay needs.

---

## 3. Market calendars and time

| Candidate | Fit | Latest (date) | License | Coverage tested (2026-09-24, local venv) | Conf | Ref |
|---|---|---|---|---|---|---|
| **exchange_calendars** | Authoritative session and minute logic (`XNYS`), `is_session`, `minutes_in_range`, early closes | 4.13.2 (2026-03-10) [PyPI]; repo active (pushed 2026-09-24) [GH]; Py ≥3.10 | Apache-2.0 | 2026-11-27 and 2026-12-24 close at 18:00 UTC (1pm ET); 2026-07-03 is a holiday; the 2025-01-09 Carter mourning closure is handled. **Default calendar ends 1 year out** (last session 2027-09-24), so pass `end=` explicitly for later dates. **No overnight or 23/5 session model** | High (test) | R22,R24 |
| **pandas_market_calendars** | Adds pre/post schedule columns (`start="pre", end="post"`); **depends on exchange_calendars** | 5.4.0 (2026-05-27) [PyPI]; repo pushed 2026-07-12 | MIT | Schedule has pre/market_open/market_close/post only. **No overnight session** | High (test) | R23 |
| **zoneinfo + tzdata** | Always store UTC `timestamptz`; convert via `ZoneInfo("America/New_York")` | tzdata 2026.4 (2026-09-12) | Apache-2.0 | Needed on Windows | High | [PyPI] |

**Official NYSE dates:**
- **2026 holidays:** Jan 1, Jan 19, Feb 16, Apr 3 (Good Friday), May 25, Jun 19, Jul 3 (observed), Sep 7, Nov 26, Dec 25.
- **2026 early closes (1:00pm ET):** Nov 27 and Dec 24.
- **2027 early closes:** Nov 26 (the day after Thanksgiving). [R25]
- **2028:** NYSE has also published its 2028 calendar. [R25b]

- **Recommendation:**
  - Use `exchange_calendars` as the source of truth, wrapped in your own `market_calendar` service.
  - Keep a small DB table, `session_overrides(date, kind, open, close, source)`, for:
    - ad-hoc closures (mourning days, emergencies)
    - the **23/5 overnight session from 2026-12-06**
  - Compute a `session_date` for every bar: it is the trading day on which the 8pm-ET boundary closes.
  - Do all arithmetic in UTC, with display in ET.
  - Unit-test DST transitions: 2026-11-01 and 2027-03-14.
- **When to upgrade:** once exchange_calendars or pandas_market_calendars ships an overnight-session model, drop that part of your overrides.

---

## 4. Symbology and corporate actions

| Item | What it gives you | Terms / limits | Conf | Ref |
|---|---|---|---|---|
| **OpenFIGI API v3** (`/v3/mapping`) | Maps ticker, ISIN, or CUSIP to **FIGI**, a free, open, permanent identifier. Use the share-class FIGI as the internal security key; treat ticker as a time-varying attribute | Free. **No key:** 25 req/min, 10 jobs/req. **With free key:** 25 req per 6 s, 100 jobs/req. HTTP 429 when exceeded | Med (official doc) | R26 |
| **Massive (formerly Polygon.io)** | Splits and Dividends endpoints now include a **`historical_adjustment_factor`**, a cumulative multiplier to the current share basis. Aggregates are **split-adjusted by default**; `adjusted=false` returns raw. **Trap:** if you store raw bars, REST backfills must pass `adjusted=false`. Otherwise adjusted history mixes with raw live bars and corrupts the table at the next split | Python SDK renamed: `massive` 2.8.0 (2026-05-26) supersedes `polygon-api-client` 1.16.3 (2025-10-30) [PyPI] | Med | R27,R28 |
| **Databento** | Corporate actions dataset (310k+ securities, 61 event types, point-in-time), plus an **adjustment factors** dataset that combines all events into one daily ratio, via the reference API | `databento` 0.87.0 (2026-09-22) [PyPI]; pricing not verified | Med | R29 |

- **Recommendation:**
  - Store **raw (unadjusted) bars** plus a `corporate_actions` table (ex_date, type, ratio or amount, source).
  - Keep a derived `adj_factor(security_id, date)` table. Apply adjustments at query time (`price × cumulative factor`) or in materialized adjusted views.
  - Key everything by an internal `security_id` mapped to FIGI, with a `ticker_history(security_id, ticker, valid_from, valid_to)` table.
  - Alert thresholds that compare against history (for example, a 52-week high) **must use adjusted series**. Intraday alerts use raw.
- **When to upgrade:** move to a paid reference-data feed (Databento reference or vendor corporate actions) when you backtest over delisted names or need point-in-time universes, to avoid survivorship bias.

---

## 5. Backtesting / research, portfolio / risk

All rows: version and date from [PyPI]; activity and license from [GH] unless noted.

| Library | Fit | Latest (date) [PyPI] | License | Maintenance | Conf |
|---|---|---|---|---|---|
| **vectorbt** (OSS) | Fast vectorized signal research; ideal for "would this alert rule have worked" | 1.1.0 (2026-07-05); Py 3.11-3.14 | **Apache-2.0 + Commons Clause**: you may not *sell* a product or service whose value derives substantially from it [R71] | Active (pushed 2026-09-17) | High |
| vectorbt PRO | Closed source, more features | ~$20-25/mo membership [R72] | Proprietary | Active | Med-Low |
| **bt** | Portfolio-level strategy backtests | 1.2.3 (2026-09-12) | MIT | Active | High |
| **NautilusTrader** | Event-driven, production-grade, research-to-live parity (Rust core) | 1.231.0 (2026-08-02); **Py ≥3.12** | LGPL-3.0+ | Very active | High |
| **LEAN / QuantConnect** | Full engine (C#) with Python; local CLI `lean` 1.0.229 (2026-08-28) | — | Apache-2.0 (engine) | Active | High (engine); cloud pricing unverified |
| **zipline-reloaded** | Legacy Quantopian API | 3.1.1 (2025-07-19); last push 2026-01-06 | Apache-2.0 | Slow | High |
| **backtrader** | Popular but stale | 1.9.78.123 (**2023-04-19**); repo last push 2024-08-19 | **GPL-3.0** | **Effectively unmaintained** | High |
| Event studies | No maintained dedicated library; `eventstudy` 0.1a12 was last released in **2021** | — | — | Dead | High |
| → statsmodels | Build market-model event studies yourself: OLS on an estimation window, then abnormal and cumulative abnormal returns | 0.15.0 (2026-08-27) | BSD-3 | Active | High |
| **Riskfolio-Lib** | Broad portfolio optimization (CVaR, risk parity, HRP) | 7.3.0 (2026-05-31) | BSD-3 | Active | High |
| **PyPortfolioOpt** | Simple MVO/HRP/Black-Litterman; repo moved to the `PyPortfolio` org | 1.6.0 (2026-02-26) | MIT | Active | High |
| **skfolio** | scikit-learn-style portfolio optimization with CV | 1.3.1 (2026-09-23) | BSD-3 | Very active | High |
| **QuantStats** | Tear sheets and metrics | 0.0.81 (2026-01-13) | Apache-2.0 | Active | High |
| **empyrical-reloaded** | Metric primitives | 0.5.12 (2025-06-01) | Apache-2.0 | Slow | High |

- **Recommendation:**
  - Use **vectorbt (OSS)** for internal alert-rule research, and don't expose it as a paid feature (Commons Clause).
  - Use **statsmodels** for event studies (earnings or news reaction).
  - Use **skfolio** or **Riskfolio-Lib** plus **QuantStats** for portfolio and risk views.
  - Avoid backtrader.
- **When to upgrade:** move to **NautilusTrader** (LGPL, Py 3.12 native) when you add paper or live execution and need research-to-live parity. Buy vectorbt PRO only if your internal research velocity justifies it.

---

## 6. Data quality

| Tool | Fit | Latest (date) [PyPI] | License | Notes | Conf |
|---|---|---|---|---|---|
| **pandera** | In-process DataFrame and Polars schema checks. Ideal for per-batch OHLCV validation in the ingestor | 0.33.1 (2026-09-01) | MIT | Lightweight; works with Pydantic | High |
| **Great Expectations (GX Core)** | Heavier suite-based validation and data docs | 1.23.1 (2026-09-18) | Apache-2.0 | **Fivetran became steward on 2026-05-13**; repo now `fivetran/great_expectations`; **GX Cloud discontinued from June 1** | High [R31] |
| **Soda Core** | YAML data contracts against SQL sources | 4.25.0 (2026-09-23) | **Elastic License 2.0** (not Apache) | Soda Cloud upsell | High |

**OHLCV validation patterns** (implement as pandera checks plus SQL constraints):
- `low ≤ min(open, close) ≤ max(open, close) ≤ high`
- `volume ≥ 0`, prices `> 0`
- Unique `(security_id, ts)`
- `ts` aligned to the minute
- `ts` lies within a session per the calendar, with extended and overnight sessions allowed
- Gap detection: expected versus received minutes per session, tolerating illiquid names
- Staleness: last bar age during an open session
- Spike filter: `|ret_1m| > k·σ_rolling` quarantines the bar; it does not drop it
- Split sanity: a jump close to the ratio on an ex-date should match a `corporate_actions` row
- Cross-vendor spot-check: sample of daily closes against a second source

- **Recommendation:** **pandera** in the pipeline, plus Postgres `CHECK` and unique constraints. Skip GX and Soda at this size.
- **When to upgrade:** adopt GX Core when a separate data or analytics consumer needs published validation reports.

---

## 7. Observability

| Tool | Fit | Latest / price | License | Conf | Ref |
|---|---|---|---|---|---|
| **OpenTelemetry Python** | Traces and metrics; FastAPI auto-instrumentation | sdk 1.44.0; `opentelemetry-instrumentation-fastapi` **0.65b0 (beta)** (2026-07-16) [PyPI] | Apache-2.0 | High | [PyPI] |
| **structlog** | JSON structured logs with contextvars (request, alert, and symbol IDs) | 26.1.0 (2026-06-06) | MIT or Apache-2.0 | High | [PyPI] |
| **prometheus-client** | `/metrics` for Prometheus or Grafana scraping | 0.26.0 (2026-07-24) | Apache-2.0 + BSD-2 | High | [PyPI] |
| **Grafana Cloud** | Hosted metrics, logs, and traces | **Free:** 10k active series, 50 GB logs, 50 GB traces, 14-day retention, 3 users. **Pro:** $19/mo platform fee + usage | SaaS | Med | R32 |
| **Sentry** | Errors and performance; also offers uptime and cron monitors | sentry-sdk 2.70.0 (2026-09-22). **Developer free** (1 user), **Team $26/mo**, **Business $80/mo** (annual billing) | SaaS (SDK MIT) | Med | R34 |
| **Uptime** | External HTTP checks | UptimeRobot free: 50 monitors at 5-min checks, but sources conflict on commercial use. Better Stack free: 10 monitors (aggregator) | SaaS | Med-Low | R35 |

- **Recommendation:**
  - **structlog** for JSON logs to stdout.
  - **Sentry** (free, then Team) for errors.
  - **OTel** traces and metrics exported to **Grafana Cloud free**.
  - Domain-specific checks, because a generic HTTP uptime check will *not* catch a stalled feed:
    - A calendar-aware gauge `feed_last_bar_age_seconds{session}` that alerts when it exceeds 180 s during an open session.
    - `alerts_eval_lag_seconds`.
    - `outbox_pending`.
    - Notification delivery failure rate.
    - A **heartbeat/cron monitor** (Sentry Crons, or UptimeRobot/Better Stack heartbeat) pinged by the evaluator each minute during sessions.
- **When to upgrade:** move to paid Grafana Pro or self-hosted Prometheus when metrics pass 10k active series, typically from per-symbol labels. Avoid per-symbol labels anyway.

---

## 8. Deployment (tiny team) and managed Postgres

| Platform | Suitability for long-lived websocket ingestor | Price data (verify before buying) | Conf | Ref |
|---|---|---|---|---|
| **Fly.io Machines** | Good: always-on VMs, regions near NY (iad/ewr) | shared-cpu-1x: 256 MB = $0.00000078/s (**~$2.02 per 30-day month, Est**), 512 MB ~$3.32, 1 GB ~$5.91. Volumes $0.15/GB-mo. Egress $0.02/GB (NA/EU). Pricing update effective 2026-10-01 says machine CPU pricing is unchanged | High (per-second rates from the docs page source); Est (monthly) | R36,R37 |
| Fly **Managed Postgres** | No TimescaleDB (only pgvector and PostGIS as third-party extensions) | Basic (shared-2x, 1 GB) **$38/mo**, Starter (2 GB) $72, storage $0.28/GB-mo | High | R33 |
| **Render** | Good: "Background Worker" service type suits the ingestor | Worker/web Starter ~$7/mo (512 MB), Postgres Basic-256mb ~$6, Basic-1gb ~$19. New workspace plans since 2026-04-23. Primary pricing page fetch failed | Med-Low | R38 |
| **Railway** | Good: always-on services, usage-based | Hobby $5/mo (includes $5 credit), Pro $20/mo (includes $20). ~$20/vCPU-mo, ~$10/GB-RAM-mo, volumes ~$0.15/GB-mo, egress $0.05/GB. Has a TimescaleDB template (self-managed) | Med | R39 |
| **AWS ECS Fargate / ECS Express Mode** | Good but more ops | Fargate ARM ~$0.03238/vCPU-h, ~$0.00356/GB-h. **App Runner closed to new customers (from 2026-04-30)**; AWS recommends **ECS Express Mode**, which has no extra charge but provisions an ALB (~$16+/mo, Est) | High (App Runner); Med-Low (Fargate rates) | R44,R45 |
| **GCP Cloud Run services** | **Poor for the ingestor**: websocket requests max 60 min and need reconnects; fine for the FastAPI web tier | Instance-based billing while sockets are open | High | R30 |
| **GCP Cloud Run worker pools** | OK for a pull-based ingestor (non-HTTP, always-on) | ~$18-24/mo for 2 small instances (blog, Med-Low) | Med-Low | R46 |
| **Hetzner Cloud** | Cheapest VM **in the EU**. Minute-level data tolerates transatlantic latency | After the **2026-06-15** repricing: **CX23 €5.49 / $6.49/mo** (EU only); CAX11 $6.99; **US (Ashburn/Hillsboro) CPX11 $20.49/mo** | High (primary doc) | R47 |

**Managed Postgres (approximate prices):**

| Provider | Price | TimescaleDB | Conf | Ref |
|---|---|---|---|---|
| **Neon** | Free (0.5 GB, 100 CU-h, scale-to-zero). Launch $0.106/CU-h + $0.35/GB-mo | Apache-only | Med | R48, R6 |
| **Supabase** | Free (500 MB DB, pauses after 1 week idle). Pro $25/mo (8 GB DB, $10 compute credit) | Deprecated on PG17 | Med | R49, R7 |
| **RDS** db.t4g.micro | ~$11.68/mo single-AZ + storage | No TimescaleDB | Med-Low | R50, R8 |
| **Tiger Cloud** | From $30/mo | Full TimescaleDB | High | R2 |

Note that scale-to-zero (Neon) is at odds with a DB written every minute during sessions of up to 23 hours, so expect it to be always on.

- **Recommendation:**
  - **Start:** one PaaS (Fly.io or Render/Railway) with three processes: `web` (FastAPI), `ingestor` (singleton), `worker` (evaluator plus Procrastinate). Managed PG to begin with.
  - **Timescale needed:** Tiger Cloud (~$30+/mo), or TimescaleDB self-hosted on a Hetzner EU CX23 (~$6.49/mo) with backups you own (pgBackRest to object storage).
  - **Estimated all-in MVP:** ~$20-60/mo (Est).
- **When to upgrade:**
  - Move to AWS or GCP (ECS Express Mode, Cloud Run web plus a worker pool) when you need VPC compliance, SSO, or multi-region.
  - Split the ingestor onto dedicated compute when you run more than one vendor feed, or the socket drops correlate with web deploys.

---

## 9. Broker / paper-trading APIs (later phase)

| Broker | Paper / sandbox | Can a third-party app act for users? | Constraints | Conf | Ref |
|---|---|---|---|---|---|
| **Alpaca** | Paper account for anyone by email, globally, no funding. Default $100k. Real-time IEX data. **Does not simulate** dividends, slippage, queue position, borrow or regulatory fees | **Yes: OAuth 2.0** on the Trading API. You can request `env=paper` or live. **Broker API** is for building your own brokerage (you own the users) | Market-data websocket commonly limited to 1 connection | High | R51,R52,R42 |
| **Interactive Brokers** | Paper accounts exist | **OAuth 2.0 only for licensed orgs, FAs, and IBrokers, not individuals.** Third-party vendors must apply (currently OAuth 1.0a) via an onboarding form. Individuals use the **Client Portal Gateway** (a local Java app with manual login) | Heavy onboarding; TWS/Gateway session management | Med | R53 |
| **Tradier** | Sandbox is paper with **15-min delayed** data | OAuth 2.0 authorization code flow **for partners**. Personal users get API tokens (OAuth not enabled for personal use). Refresh tokens can be enabled for partners | Partner approval | Med | R54 |
| **Schwab Trader API** | No public sandbox (unverified) | **Individual access ≠ commercial.** Offering the app to other Schwab clients needs a **separate commercial review**, which weighs user control of orders and AI or automation | **Refresh token expires every 7 days**, forcing a full re-auth. Access token lasts 30 min | Med | R55,R56 |

- **Recommendation:** start alerts-only. For paper trading, integrate **Alpaca OAuth (paper env)** first. Treat IBKR and Schwab as "user brings own credentials and runs locally" until you are a registered vendor.
- **When to upgrade:** pursue IBKR vendor onboarding or Schwab commercial approval once there is real user demand for execution. Evaluate aggregators such as SnapTrade (unverified) to avoid per-broker approvals.
- **Compliance:** order routing, or an "AI suggests trades" feature, may trigger regulatory review. That is out of scope here, so get counsel.

---

## 10. Notifications

| Channel | Option | Cost | Deliverability / limits | Conf | Ref |
|---|---|---|---|---|---|
| Email | **Postmark** | Free dev tier 100/mo. 10k/mo: Basic $15, Pro $16.50, Platform $18. Overage $1.20-1.80 per 1k | Transactional-focused, strong reputation. Separate "message streams" for transactional vs broadcast | Med | R57 |
| Email | **Resend** | Free 3,000/mo (100/day, 3 domains). Pro $20/mo for 50k | Modern API; Python SDK 2.47.0 (2026-09-18) | Med | R58 |
| Email | **Amazon SES** | À la carte **$0.10 per 1k**. New plan tiers (Essentials $0.16/1k, etc.) seen on the pricing page | Cheapest; you own sandbox exit, bounces, and complaints | Med (plan tiers unverified) | R59 |
| Web push | VAPID + `pywebpush` 2.5.0 (MPL-2.0) | Free | **iOS/iPadOS needs the site installed to the Home Screen** (16.4+). Safari 18.4 adds Declarative Web Push | Med | R60 |
| Telegram | Bot API (`python-telegram-bot` 22.8, LGPL-3.0) | Free | ~30 msg/s overall, ~1 msg/s per chat, 20/min per group (**unofficial**, community figures) | Med-Low | R61 |
| Discord | Webhooks | Free | 5 requests per 2 s per webhook; handle 429 and Retry-After | Med | R62 |
| SMS | **Twilio** | US $0.0083/segment + carrier fees $0.0035-0.0045. Number ~$1.15/mo. **A2P 10DLC brand and campaign registration required** (fees unverified) | Registration delays of weeks; opt-in and STOP handling are mandatory | Med | R63 |

For all email providers, set up SPF, DKIM, and DMARC on the sending domain. Gmail and Yahoo bulk-sender requirements (one-click unsubscribe for non-transactional mail) likely apply; this is general knowledge, not verified this session (see Unverified).

- **Recommendation:**
  - **Email:** Postmark or Resend (transactional).
  - **Primary real-time channel:** web push, plus Telegram and Discord (free, instant).
  - **SMS:** defer (10DLC friction and cost).
  - Enforce per-user rate limits, quiet hours, and dedupe or cooldown per `(user, rule, security)` in the evaluator.
- **When to upgrade:** move to SES at more than ~50k emails per month. Add SMS only for premium users once 10DLC is approved.

---

## 11. Auth (cost for fewer than 5k users)

| Option | Free tier | Paid | Notes | Conf | Ref |
|---|---|---|---|---|---|
| **Clerk** | 50,000 **MRU** (monthly *retained* users) per app | Pro $25/mo ($20 annual), $0.02 per MRU above 50k | Hosted UI; verify JWTs in FastAPI via JWKS | Med | R64 |
| **Auth0** | 25,000 MAU free | B2C Essentials **$70/mo at 1k MAU, $350/mo at 5k**; Professional $240 / $1,000 | Most expensive at this scale | Med | R65 |
| **Supabase Auth** | 50,000 MAU (free project pauses after a week idle) | Pro $25/mo (100k MAU, then $0.00325/MAU) | Couples you to Supabase; server repo `supabase/auth` MIT, v2.197.0 (2026-09-09) [GH] | Med | R49 |
| **FastAPI-Users** | Self-hosted library | $0 | **Maintenance mode** (security fixes only); v15.0.5 (2026-03-27), MIT | High | [GH] |
| **Keycloak** | Self-hosted IdP | $0 + ~1-2 GB RAM VM (Est) | 26.7.4 (2026-09-16), Apache-2.0; heavy ops for 1-3 devs | High | [GH] |

- **Recommendation:** **Clerk free tier**, costing $0 below 50k MRU. FastAPI only verifies JWTs, and internal user IDs map to `clerk_user_id` to limit lock-in.
- **Alternatives:**
  - Supabase Auth if you're already on Supabase.
  - Self-rolled auth (FastAPI-Users is maintenance-only) only if avoiding vendors is a hard requirement.
- **When to upgrade:** re-evaluate at ~50k MRU, or when enterprise SSO/SAML is needed (Clerk Pro add-ons or Auth0).

---

## 12. LLM tooling for grounded, explainable alert summaries

| Tool | Status | Latest (date) | License | Notes | Conf | Ref |
|---|---|---|---|---|---|---|
| **Anthropic Claude API: structured outputs** | **GA**. `output_config.format = {type: "json_schema", schema}` plus `strict: true` on tools. Beta header no longer needed (`output_format` moved to `output_config.format`) | `anthropic` 1.8.0 (2026-09-22) [PyPI] | MIT (SDK) | Constrained decoding. **Unsupported:** recursive schemas; numeric (min/max) and string-length constraints; `minItems` other than 0 or 1. Grammar is cached for 24 h | High (primary doc) | R66 |
| **Gemini `google-genai` SDK** | `GenerateContentConfig(response_mime_type="application/json", response_schema=PydanticModel)` or `response_json_schema=Model.model_json_schema()`. Current docs also show a newer **Interactions API** (`client.interactions.create(..., response_format={...})`) | `google-genai` 2.25.0 (2026-09-22) [PyPI] | Apache-2.0 | "Not all JSON Schema features are supported"; deeply nested schemas may be rejected; historical nested-`$defs` issues | Med | R67,R68 |
| **instructor** / **pydantic-ai** | Provider-agnostic Pydantic validation and retry wrappers | 1.17.0 (2026-09-09) / 2.49.0 (2026-09-24) | MIT | Useful for a multi-provider fallback | High | [PyPI] |
| **promptfoo** | Evals and red-teaming; **Node CLI** (the PyPI `promptfoo` 0.2.0 is a wrapper, not the tool) | GitHub 0.123.1 (2026-09-18) | MIT | **Acquired by OpenAI (announced 2026-03-09)**; says it will stay open source under MIT | High | R69 |
| **DeepEval** | pytest-style LLM evals (faithfulness, G-Eval) | 4.2.6 (2026-09-24) | Apache-2.0 | Very active | High | [PyPI/GH] |
| **Ragas** | RAG metrics (faithfulness, context precision) | 0.4.3 (2026-01-13) | Apache-2.0 | Repo moved to `vibrantlabsai/ragas`; **last push 2026-02-24 (slowing)** | High | [GH] |
| **Inspect (UK AISI)** | Rigorous eval framework | inspect-ai 0.3.268 (2026-09-22) | MIT | Very active; more research-oriented | High | [PyPI/GH] |

**Grounding pattern for explainable alerts:**
1. The deterministic rule engine computes the facts: rule ID, thresholds, observed values, windows, bar timestamps, and data source.
2. The LLM receives *only* that fact payload (plus optional vetted news snippets with IDs).
3. The output schema forces the model to cite `evidence_ids` for every claim, plus `confidence`.
4. A post-validator checks that every number in the summary appears in the fact payload. On failure it falls back to a template summary.
5. Evals run in CI with DeepEval or promptfoo over a golden set of alert payloads, checking faithfulness, the no-new-numbers rule, and schema validity.

- **Recommendation:**
  - **Claude structured outputs (GA)**, or Gemini `response_json_schema`, behind a thin provider interface.
  - Keep schemas flat: enums and required fields; no numeric constraints, enforced in Pydantic post-validation instead.
  - **DeepEval** in pytest for CI.
  - **promptfoo** optional, for prompt A/B tests and red-teaming (a Node dependency).
- **When to upgrade:** add Inspect when evals become a research discipline, meaning many models, agents, or sandboxed tools.

---

## Recommended MVP stack (summary)

| Layer | Choice |
|---|---|
| Storage | Managed Postgres with native declarative partitions by **session date** (job-created; pg_partman where available, i.e. not on Fly MPG), then TimescaleDB (Tiger Cloud or self-hosted) at the trigger. At 5k symbols the trigger arrives within year 1 |
| Ingestion | Single `ingestor` process holding the vendor websocket (1-connection limit), guarded by a PG advisory lock and deployed stop-before-start, writing raw bars (REST backfill with `adjusted=false`) |
| Events | Transactional outbox + LISTEN/NOTIFY, with **Procrastinate** for delivery jobs and APScheduler 3.11 for calendar jobs; Redis/Valkey only for live UI fan-out |
| Calendars | exchange_calendars (pass `end=`) + `session_overrides` table (23/5 from 2026-12-06) + tzdata pinned |
| Symbology | Internal `security_id` ↔ FIGI (OpenFIGI), ticker history, raw bars + adjustment-factor table |
| Data quality | pandera + PG constraints + staleness and gap metrics |
| Observability | structlog, Sentry, OTel to Grafana Cloud free, feed-staleness heartbeat |
| Deploy | Fly.io or Render/Railway (web / ingestor / worker); Cloud Run services only for the web tier |
| Auth | Clerk (free below 50k MRU) |
| Notify | Postmark or Resend + web push + Telegram/Discord; SMS later |
| LLM | Claude or Gemini structured outputs, fact-only grounding, DeepEval in CI |
| Research | vectorbt OSS (internal only), statsmodels event studies, skfolio/Riskfolio + QuantStats |

---

## Unverified / low-confidence items (explicit)

1. **Redpanda:** license (believed BSL) and Serverless unit prices were not verified from a primary source.
2. **Twilio A2P 10DLC:** registration fees (brand and campaign) not captured.
3. **QuantConnect:** cloud pricing not checked.
4. **OpenTelemetry Python logs signal:** stability status not confirmed (believed still experimental or unstable in 2026). FastAPI instrumentation is confirmed beta (0.65b0).
5. **UptimeRobot:** free-plan commercial use is conflicting. A June 2026 help page reportedly allows it; earlier ToS reportedly banned it.
6. **Telegram rate limits:** community figures, not official.
7. **Render:** the primary pricing page fetch failed. Figures ($7 worker, $6/$19 PG) are from aggregators.
8. **Amazon SES:** the new "Essentials/Pro/Enterprise" plan tiers were seen in a single fetch. À la carte $0.10/1k is long-standing.
9. **Gemini:** relationship between the newer Interactions API (`response_format`) and `generate_content` (`response_schema` / `response_json_schema`) was not confirmed. Both appear in current material.
10. **ClickHouse Cloud ($66.52/mo), RDS t4g.micro ($11.68), Fargate ARM rates, Cloud Run worker-pool cost, VectorBT PRO price ($20-25/mo), Better Stack free tier:** aggregator-sourced only.
11. **Tiger Cloud storage rate:** $0.177/GB-mo is aggregator-sourced; the $30/$36 plan floors are official.
12. **NYSE Arca 23/5 launch date:** only secondary sources give Dec 6, 2026; the primary FAQ fetch didn't expose the date. Nasdaq's date is also from secondary sources. Confirm with your data vendor's notice before building the overnight session.
13. **Alpaca 1-connection limit:** from forum and GitHub issue reports plus the docs search snippet. Limits may differ on paid data plans.
14. **Schwab:** whether a paper or sandbox environment exists was not verified.
15. **QuestDB Enterprise and Databento:** pricing not captured.
16. **Neon TimescaleDB 2.17.1:** reported by a search snippet of Neon docs; may since have been upgraded.
17. **PaaS deploy overlap:** whether worker deploys on Fly, Render and Railway overlap old and new instances was not checked. Assume they do, and guard with an advisory lock.
18. **Gmail/Yahoo bulk-sender rules** (one-click unsubscribe, DMARC): not re-verified this session.
19. **Fly pricing update effective 2026-10-01:** read only through a page summary ("machine CPU pricing unchanged"). Re-check after Oct 1.
20. **pg_partman on Neon, Supabase and Render:** confirmed only by string matches on their extension pages, not by version or compatibility.
21. **Compression ratio 5-10x:** a vendor-typical figure, not measured for this schema.

---

## References (all accessed 2026-09-24)

| # | URL | Pub / release date | Conf |
|---|---|---|---|
| R1 | https://github.com/timescale/timescaledb/releases (2.30.1) | 2026-09-17 | High |
| R2 | https://www.tigerdata.com/pricing | current | High |
| R3 | https://github.com/timescale/timescaledb/blob/main/LICENSE ; https://www.tigerdata.com/legal/licenses | current | High |
| R4 | https://github.com/ClickHouse/ClickHouse/releases | 2026-09-22 | High |
| R5 | https://clickhouse.com/pricing ; https://selfhost.dev/blog/clickhouse-pricing-real-cost-of-running-it/ | 2026 | Med-Low |
| R6 | https://neon.com/docs/extensions/timescaledb | current | Med |
| R7 | https://supabase.com/docs/guides/database/extensions/timescaledb | current | Med |
| R8 | https://1bench.dev/extensions/postgresql/on-aws-rds ; https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html | 2026 | Med |
| R9 | https://github.com/questdb/questdb/releases (10.0.1) | 2026-08-24 | High |
| R10 | https://duckdb.org/2026/06/17/announcing-duckdb-145 ; https://pypi.org/project/duckdb/ | 2026-06-17 / 2026-07-22 | High |
| R11 | https://duckdb.org/docs/current/connect/concurrency | current | High |
| R12 | https://www.postgresql.org/docs/current/sql-notify.html | current | High |
| R13 | https://pypi.org/project/procrastinate/ | 2026-09-23 | High |
| R14 | https://redis.io/legal/licenses/ ; https://github.com/redis/redis/releases | 2026-09-17 | High |
| R15 | https://github.com/valkey-io/valkey/releases | 2026-09-01 | High |
| R16 | https://github.com/nats-io/nats-server/releases ; https://pypi.org/project/nats-py/ | 2026-09-17 / 2026-09-16 | High |
| R17 | https://www.redpanda.com/data-streaming/serverless | current | Med-Low |
| R18 | https://github.com/python-arq/arq | 2026-04-16 | High |
| R19 | https://pypi.org/project/dramatiq/ | 2026-09-02 | High |
| R20 | https://pypi.org/project/celery/ | 2026-03-26 | High |
| R21 | https://pypi.org/project/APScheduler/ | 2026-06-28 | High |
| R22 | https://pypi.org/project/exchange-calendars/ ; https://github.com/gerrymanoim/exchange_calendars | 2026-03-10 | High |
| R23 | https://pypi.org/project/pandas-market-calendars/ | 2026-05-27 | High |
| R24 | Local test: exchange_calendars 4.13.2 / pandas_market_calendars 5.4.0 in a scratch venv | 2026-09-24 | High |
| R25 | https://ir.theice.com/press/news-details/2024/NYSE-Group-Announces-2025-2026-and-2027-Holiday-and-Early-Closings-Calendar/default.aspx | 2024-11-08 | High |
| R25b | https://ir.theice.com/press/news-details/2025/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar/default.aspx | 2025 | Med |
| R26 | https://www.openfigi.com/api/documentation | current | Med |
| R27 | https://massive.com/blog/new-splits-and-dividends-endpoints | 2026 (undated in fetch) | Med |
| R28 | https://massive.com/knowledge-base/article/is-massives-stock-data-adjusted-for-splits-or-dividends | current | Med |
| R29 | https://databento.com/docs/venues-and-datasets/adjustment-factors ; https://databento.com/blog/corporate-actions | current | Med |
| R30 | https://docs.cloud.google.com/run/docs/triggering/websockets | current | High |
| R31 | https://www.businesswire.com/news/home/20260513083026/en/ ; https://github.com/fivetran/great_expectations | 2026-05-13 | High |
| R32 | https://grafana.com/pricing/ | current | Med |
| R33 | https://docs.fly.io/mpg/ | current | High |
| R34 | https://sentry.io/pricing/ | current | Med |
| R35 | https://help.uptimerobot.com/en/articles/11604710-who-should-use-uptimerobot-s-free-plan ; https://stillup.org/blog/uptimerobot-free-plan-limits | 2026 | Med-Low |
| R36 | https://docs.fly.io/about/pricing/ (page source: per-second rates) | current | High |
| R37 | https://fly.io/pricing-update/ | effective 2026-10-01 | Med |
| R38 | https://render.com/pricing (fetch failed) ; https://kuberns.com/blogs/render-pricing/ | 2026 | Med-Low |
| R39 | https://railway.com/pricing | current | Med |
| R40 | https://massive.com/blog/us-equities-move-to-23-5-trading | 2026-08-26 | Med |
| R41 | https://www.nyse.com/publicdocs/nyse/NYSE_Extended_Hours_Trading_FAQ.pdf | v4.0, Aug 2026 | Med-Low |
| R42 | https://docs.alpaca.markets/us/docs/streaming-market-data ; https://github.com/alpacahq/alpaca-py/issues/248 | current | Med |
| R43 | https://massive.com/knowledge-base/article/how-many-massive-websocket-connections-can-i-use-at-one-time | current | Med |
| R44 | https://docs.aws.amazon.com/apprunner/latest/dg/apprunner-availability-change.html | 2026 (closed 2026-04-30) | High |
| R45 | https://aws.amazon.com/fargate/pricing/ (via aggregator figures) | 2026 | Med-Low |
| R46 | https://docs.cloud.google.com/run/docs/deploy-worker-pools ; https://innfactory.de/en/cloud/gcp/products/cloud-run-worker-pools/ | 2026 | Med-Low |
| R47 | https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ | effective 2026-06-15 | High |
| R48 | https://neon.com/pricing | current | Med |
| R49 | https://supabase.com/pricing | current | Med |
| R50 | https://cloudprice.net/aws/rds/instances/db.t4g.micro | 2026 | Med-Low |
| R51 | https://docs.alpaca.markets/us/docs/paper-trading | current | High |
| R52 | https://docs.alpaca.markets/us/docs/using-oauth2-and-trading-api ; https://alpaca.markets/support/difference-between-oauth-and-broker-api | current | High |
| R53 | https://www.interactivebrokers.com/docs/web-api/authentication/oauth-2/register ; https://www.interactivebrokers.com/campus/ibkr-api-page/webapi-doc/ | current | Med |
| R54 | https://docs.tradier.com/docs/faq ; https://docs.tradier.com/docs/authentication | current | Med |
| R55 | https://developer.schwab.com/ ; https://mylinedchart.com/resources/articles/schwab-trader-api-commercial-approval-what-the-review-evaluates | 2026 | Med |
| R56 | https://schwab-py.readthedocs.io/en/latest/auth.html | current | Med |
| R57 | https://postmarkapp.com/pricing | current | Med |
| R58 | https://resend.com/pricing | current | Med |
| R59 | https://aws.amazon.com/ses/pricing/ | current | Med |
| R60 | https://pushpad.xyz/blog/ios-special-requirements-for-web-push-notifications ; https://www.magicbell.com/blog/pwa-ios-limitations-safari-support-complete-guide | 2026 | Med |
| R61 | https://core.telegram.org/bots/faq | current | Med-Low |
| R62 | https://docs.discord.com/developers/topics/rate-limits ; https://birdie0.github.io/discord-webhooks-guide/other/rate_limits.html | current | Med |
| R63 | https://www.twilio.com/en-us/sms/pricing/us | current | Med |
| R64 | https://clerk.com/pricing | current | Med |
| R65 | https://auth0.com/pricing | current | Med |
| R66 | https://platform.claude.com/docs/en/build-with-claude/structured-outputs | current | High |
| R67 | https://ai.google.dev/gemini-api/docs/structured-output | current | Med |
| R68 | https://googleapis.github.io/python-genai/ ; https://github.com/googleapis/python-genai/issues/60 | current | Med |
| R69 | https://openai.com/index/openai-to-acquire-promptfoo/ ; https://www.promptfoo.dev/blog/promptfoo-joining-openai/ | 2026-03-09 | High |
| [PyPI] | https://pypi.org/project/<package>/ (JSON API) | per row | High |
| [GH] | https://github.com/<owner>/<repo> (GitHub API) | per row | High |
| R70 | https://neon.com/docs/extensions/pg-extensions ; https://supabase.com/docs/guides/database/extensions ; https://render.com/docs/postgresql-extensions (pg_partman listed) | current | Med |
| R71 | https://github.com/polakowo/vectorbt/blob/master/LICENSE.md | current | High |
| R72 | https://vectorbt.pro/become-a-member/ ; https://ko-fi.com/vectorbtpro/tiers | current | Med-Low |
