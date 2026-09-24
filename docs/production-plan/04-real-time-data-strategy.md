# 04 — Real-Time Data Strategy

← [Index](README.md) · Previous: [03 Research](03-market-and-tooling-research.md) · Next: [05 Target architecture](05-target-architecture.md)

**Position:** "real-time" means different things for each workflow. For this product, the aims are:

- **freshness that is honest and labelled**;
- **minute-level detection latency**;
- **near-real-time evidence** (filings and news).

The aim is not the lowest possible price latency. HFT-style infrastructure is out of scope. All targets are **proposals** until they are measured in Stage 3 ([08](08-implementation-roadmap.md)). Licensing evidence: [research/market-data.md](research/market-data.md) (accessed 2026-09-24).

---

## 1. Timestamps (the data model is required to carry all five)

| Field | Meaning | Source |
|---|---|---|
| `event_ts` | When the trade or quote happened at the venue or SIP (participant/SIP timestamp), or when EDGAR accepted a filing, or the wire publication time | Provider payload |
| `provider_ts` | When the vendor stamped or emitted it, if different | Provider payload |
| `ingest_ts` | When our ingestor received it | Our clock (NTP/chrony-synced host) |
| `process_ts` | When the detector or evidence step consumed it | Our clock |
| `display_ts` | When it was rendered or notified | Client or notification service |

All five are UTC and timezone-aware. The UI shows the relevant time in the market's local zone (America/New_York) and in the user's zone. The following are derived from these fields and monitored:

- **Source delay:** `ingest_ts − event_ts`.
- **Pipeline latency:** `process_ts − ingest_ts`.
- **Freshness age:** `now − event_ts` of the latest bar.

## 2. Real-time requirements per workflow

| Workflow | Acceptable source delay | Update frequency | End-to-end target (event → user) | Stale when | Behaviour when stale or unavailable |
|---|---|---|---|---|---|
| Abnormal-move alerts (pilot: delayed feed) | 15 min, labelled "Delayed 15 min" | 1-minute bars | p95 ≤ 90 s after the delayed bar is published, so ≈ 16.5 min after the trade | Latest bar older than delay + 3 min during market hours | No new alerts for that symbol. Watchlist shows ⚠ "data delayed/stale since HH:MM". A system banner appears if more than 5% of the universe is stale. |
| Abnormal-move alerts (upsell: real-time or indicative feed) | ≤ 5 s for actual prints; "indicative/FMV" feeds are labelled as modelled | 1-minute bars plus last-trade updates | p95 ≤ 60 s after bar close | Latest update older than 2 min for a liquid name while the market is open | Same as above. Never silently fall back to the delayed feed: switch the label to "Delayed" and record the switch. |
| Filing evidence (EDGAR) | Seconds to minutes (EDGAR acceptance → feed) | Poll the EDGAR "latest filings" feed every 30–60 s, within the 10 req/s fair-access limit | p95 ≤ 3 min from acceptance to appearing in the ledger | No successful poll for 5 min | Ledger shows "filings check incomplete since HH:MM". The LLM summary is suppressed; the deterministic alert is still shown. |
| News evidence (licensed or linked headlines) | Vendor-dependent, 0–5 min | Vendor stream or 1-min poll | p95 ≤ 3 min from publication | Feed silent for more than 10 min during market hours (vendor-specific heartbeat) | Same as filings. |
| Earnings calendar | Daily | 2× daily, plus on-demand refresh | Available before the open | Last refresh older than 24 h | Show "calendar may be outdated". |
| Daily digest | EOD official close | Once pre-open, once post-close | Post-close digest ≤ 30 min after the official close file is available | Close not final | Mark values "preliminary". |
| Corporate actions | Daily (ex-dates known in advance) | Daily, before the open | Adjustments applied before the first bar of the ex-date | Table not refreshed today | Block returns spanning unverified ex-dates; show "adjustment pending". |

## 3. Ingestion design: streaming versus polling

- **Prices (1-minute bars):**
  - **Streaming** over the vendor WebSocket or TCP, where the plan allows it, subscribed to the union of all watchlist symbols plus the benchmark ETFs.
  - A small ingestor process keeps one connection per vendor.
  - **Polling** of minute-bar endpoints is the fallback for vendors that lack streaming. Budget requests against the plan's rate limit, sized as symbols × 1/min.
- **Snapshot plus incremental:**
  - On connect or reconnect, fetch a REST snapshot (today's bars so far and the previous close).
  - Then apply stream updates keyed by `(instrument_id, bar_start)`.
- **Gaps and replay:**
  - Detect a gap when a subscribed liquid symbol has no bar for a minute in which its benchmark had one, or when a vendor sequence number jumps.
  - Backfill the missing window from REST.
  - Detector runs over backfilled windows are marked `backfilled=true` and **do not send push notifications** for moves older than 10 min. They appear in the archive only.
- **Idempotency and duplicates:**
  - Bars are upserted on the natural key.
  - Alerts have a deterministic key `(instrument_id, detector_version, window_start, rule_id)`, so a re-run never double-notifies.
  - Out-of-order bars are accepted up to a lateness bound (5 min for real-time, 20 min for delayed). Later corrections update the stored bar and emit an audit event, not a new alert.
- **Rate limits, backpressure and retries:**
  - Each provider has a token-bucket budget.
  - Retries use exponential back-off with jitter and a **total deadline**, unlike the current 30 s × 3 retries per call ([01 finding 13](01-repository-assessment.md#43-high--reliability-and-performance)).
  - The detector consumes from a bounded queue. Under backpressure it drops to "latest bar per symbol" semantics and logs the dropped count.
- **Reconnection:** exponential back-off from 1 s to a maximum of 60 s. An alarm is raised if the connection is down for more than 2 min during market hours.

## 4. Sessions, calendars and time

- Use the `exchange_calendars` XNYS calendar ([03 §G](03-market-and-tooling-research.md#g-infrastructure-tooling-selected)) for:
  - regular session 09:30–16:00 ET;
  - half-days at 13:00 ET;
  - holidays.
- A unit test pins the 2026–2027 holiday list and checks it against the published NYSE calendar.
- **DST:**
  - Store UTC and convert with `zoneinfo`.
  - Intraday baselines are keyed by *minutes since the session open*, not by wall-clock time, so DST transitions do not shift RVOL baselines.
- **Extended hours:**
  - Pre-market and after-hours moves are shown but are **not** alertable in the MVP. Liquidity is thin and the prints are noisy.
  - Earnings reactions after the close are handled as a *gap* at the next open (with evidence attached).
  - **23/5 trading.** Extended SIP hours and an overnight session (roughly a 21:00–20:00 ET trading day) are expected from about 2026-12-06. Secondary sources give that date; the primary NYSE Arca document shows none and says SEC approval is still pending ([market-data §C4](research/market-data.md), [infrastructure §0](research/infrastructure.md)). A local test found that neither `exchange_calendars` 4.13.2 nor `pandas_market_calendars` 5.4.0 models the overnight session. Consequences:
    - bars are keyed and partitioned by **trading-session date**, not UTC date;
    - a `session_overrides` table covers the new session and ad-hoc closures;
    - the MVP keeps alerting to the regular session.
- **Halts:**
  - Treat LULD and regulatory halts as a state: no bars while a halt is in force.
  - After a halt, the first bar is compared to the pre-halt price and the alert notes "resumed from halt".
  - Halt status comes from the vendor feed if available, otherwise from Nasdaq Trader halt RSS (verify terms before production use).
- **Round lots and odd lots:** the new round-lot definition has been live since 2025-11-03, and quote sizes are now in shares ([market-data §C4](research/market-data.md)). The MVP uses trades and bars only, not quote sizes, so the change does not affect it. Note it for any later quote-based feature.

## 5. Freshness and degraded-mode semantics

1. **Every price the UI shows carries three things:**
   - a source badge (vendor name);
   - an entitlement label: `Real-time`, `Indicative (modelled)`, `Delayed 15 min`, or `End of day`;
   - an "as of" time.

   A "Delayed" label must be conspicuous, as the CTA/UTP delayed-display conditions require.
2. **No silent substitution.** If the primary feed fails and a secondary feed with a different entitlement is used, the label changes to the secondary feed's entitlement, and an incident is recorded. Delayed data is never displayed as real-time.
3. **Missing data is shown as missing.** No interpolation, estimation or zero-fill for prices. The fabricated-history code path is deleted ([01 finding 3](01-repository-assessment.md#41-critical)).
4. **Degraded modes** (a system status indicator is visible in the UI):

   | Mode | Trigger | Behaviour |
   |---|---|---|
   | `normal` | All health checks green | Everything runs normally. |
   | `prices-degraded` | Stale-symbol share above 5%, or the primary feed disconnected for more than 2 min | Alerts for affected symbols are paused. A banner is shown. Digest values are marked. |
   | `evidence-degraded` | EDGAR or news poller failing | Alerts still fire, with "evidence incomplete". LLM summaries are suppressed. |
   | `llm-unavailable` | LLM errors, timeouts, or eval-gate breaches | Alerts carry the deterministic ledger only. |
   | `maintenance` | Deploys and migrations outside market hours | Scheduled and announced. |

## 6. Licensing and entitlements

**Software licence ≠ data rights.** MIT, Apache-2.0 or AGPL covers code only. Data rights come from vendor terms and, underneath those, from exchange agreements ([market-data key findings](research/market-data.md)).

| Question | Finding | Consequence |
|---|---|---|
| Can current repo providers be displayed to paying users? | No. Finnhub (even the $3,500/mo plan) is "Personal Use", and redistribution needs written approval. Alpha Vantage is personal; `outputsize=full` is premium-only. Twelve Data individual plans are non-commercial; display starts at Venture, $499/mo. Marketaux is personal/non-commercial. Yahoo terms prohibit scraping and commercial use ([market-data §A](research/market-data.md)). | Current adapters are **dev-only**. yfinance is removed from every product path. |
| Delayed display | CTA and UTP charge no per-user display fees for data delayed 15 min or more. The redistributor signs the NYSE agreement. UTP charges a $250/mo delayed redistributor fee plus a $250/yr admin fee. A conspicuous delay notice is required. | Pilot uses **delayed full-volume data**, which has $0 per-user exchange fees. |
| Real-time display (today) | Non-pro users pay $1 per tape per month. Pro users pay about $92/mo across three tapes. Redistributor fee is $1,000 per tape. Non-display applies if algorithms (e.g. alert rules) consume the real-time data. Estimated ≈ $12.6k/mo at 200 users. | Not viable for the pilot. |
| CT Plan (new SIP fee regime) | SEC approved 2026-06-26. Operative date **2027-04-01**. All subscribers must sign with **DataCT by 2027-03-01**. Non-pro fee is $0.90 down to $0.25 per tape; pro fees are $26/$23/$24. | Roadmap checkpoint: re-price the real-time upsell before 2027-03-01. |
| Fee-free alternatives | "Indicative/FMV" and derived feeds: Intrinio EquitiesEdge, Massive Business FMV, Databento US Equities Mini. IEX TOPS costs $500/mo flat but covers only a small share of volume. | Possible *labelled* real-time indication. Volume-based alerts need full-market volume, not a single venue's. |
| Professional vs non-professional | Anyone acting for an entity, or serving third parties for compensation, is a **professional**. Unknown status defaults to professional under the CT Plan safe harbour. | Signup requires a non-professional attestation. Newsletter writers and advisers are likely **pro**. This favours delayed data for the core product. |
| Storage and retention | Vendor-specific; frequently limited for derived-data and redistribution rights. | Record licence class and retention rights per dataset ([06 §6](06-quantitative-validation.md#6-reproducibility-and-lineage)). Get vendor answers in writing. |
| Filings and news | EDGAR content is public and redistributable (User-Agent required, ≤ 10 req/s). Finnhub and Marketaux news need approval to display. Benzinga licenses display (quote required). | Pilot ledger shows EDGAR in full. Third-party news is shown as headline + source + time + link only, until licensed. |

**Cost envelopes** (estimates, from [market-data §2](research/market-data.md); detail in [09](09-costs-and-operating-model.md)):

| Stage | Data cost |
|---|---|
| Development | ≈ $0–50/mo (internal use only) |
| Pilot (delayed consolidated 1-minute bars meeting the [06 §1 data spec](06-quantitative-validation.md#required-data-specification-for-the-intraday-detector), plus optional indicative) | ≈ $500–3,000/mo, $0 per user. **Unconfirmed:** which vendor meets the spec, and whether a base plan is required. A partial-venue fallback costs about $530–1,450. |
| Real-time SIP pilot | ≈ $12.6k/mo |
| Growth, 5,000 users on delayed + upsell | ≈ $2.5–5k/mo fixed, plus upsell fees that scale with upsell revenue |

**Blocking unknowns** (tracked in [11](11-evidence-and-open-questions.md)):
- Which vendor delivers **consolidated full-volume delayed 1-minute bars with display rights**, and at what price.
- Whether Databento Standard + Mini, Massive expansions without the $2,499 base plan, and Twelve Data Venture include external display rights and exchange fees.
- Who counts as "vendor" for delayed CTA/UTP display.
- Whether **user exports** are allowed. Newsletter writers republishing ledgers to their readers counts as third-party redistribution.

These need **written vendor confirmation** before the pilot contract.

## 7. Asset-class differences

- **Equities:** consolidated trade data from many venues; tight intraday cadence; corporate actions frequent.
- **ETFs:**
  - Same tape as equities, but NAV and holdings are separate datasets with separate licences and cadences (daily NAV, T+1 holdings; SEC N-PORT is public only quarterly with about a 60-day lag).
  - Leveraged and inverse ETFs need flagging.
- **Bonds (excluded):**
  - Sparse OTC trades via TRACE.
  - Real-time vendor feed is $1,500/mo per dataset; non-pro display is free.
  - MSRB subscriptions cost $5.5k–45k.
  - Stale "last price" is normal; evaluated pricing is needed.

  None of the equity pipeline carries over unchanged ([06 §3](06-quantitative-validation.md#3-asset-class-specifics)).

## 8. Recommended architecture and upgrade path

- **Stage 0 (dev):**
  - EOD and delayed bars from a dev-tier vendor (internal use only).
  - EDGAR poller.
  - Replay harness over stored bars.
  - No live users.
- **Pilot:**
  - One delayed full-volume bar vendor with **confirmed display rights**.
  - Optional indicative real-time feed, labelled "Indicative".
  - EDGAR in real time.
  - Headline links.
  - A single ingestor process writing to Postgres/Timescale ([05](05-target-architecture.md)).
- **Upgrade triggers:**
  - ≥ 150 paying users **and** survey demand ≥ 40% → add a real-time proprietary feed (Cboe One Summary or Nasdaq Basic) as an upsell tier, gated by attestation, with per-user fees passed through in the price.
  - Detector lag p95 > target at peak → separate the ingestor and detector processes, and add a queue ([05 §8](05-target-architecture.md#8-when-to-add-infrastructure)).
  - More than 5,000 symbols → move bar storage to ClickHouse and keep Postgres for OLTP.
  - Never: co-location, kernel bypass, or tick-by-tick order-book processing. Nothing in this product needs sub-second latency.
