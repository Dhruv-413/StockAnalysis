# 06 — Quantitative and Financial Correctness

← [Index](README.md) · Previous: [05 Target architecture](05-target-architecture.md) · Next: [07 Security & readiness](07-security-and-production-readiness.md)

This document defines **what the product computes, how we make sure it is right, and what evidence has to exist before any number or claim is shown as meaningful**. Paper verdicts and citations are in [research/papers.md](research/papers.md), accessed 2026-09-24.

**Governing rule:** every number shown to a user comes from a deterministic, versioned calculation over stored, timestamped inputs. LLMs may *select and phrase* retrieved evidence. They never produce numbers, forecasts, or confidence scores.

---

## 1. What the MVP computes

The MVP makes descriptive claims only. See the [product thesis](02-product-thesis.md).

| Metric | Definition | Inputs | Notes |
|---|---|---|---|
| Session return | `last / prev_close_adj − 1` | Consolidated last trade, or IEX-only if that is the entitlement ([04](04-real-time-data-strategy.md)); previous official close adjusted for any corporate action effective today | Label the price source and timestamp. |
| Gap (overnight) return | `open_official / prev_close_adj − 1` | Official opening print | Treated as its own segment, because news explains far more overnight variance (Boudoukh et al. 2019, [papers §10](research/papers.md)). |
| Abnormal return (AR) | `r_i − (α̂ + β̂·r_benchmark)` over the event window | Market-model α, β estimated on a trailing **estimation window** (default 250 trading days, minimum 120). The window ends the day before the event window. Excludes the ±1 day around past earnings. | Benchmark: SPY by default, plus a sector SPDR ETF for the sector-adjusted variant (MacKinlay 1997; Brown & Warner 1985). |
| Standardised AR (z) | `AR / σ̂_resid`, scaled to the elapsed fraction of the session | Residual σ from the estimation window | Intraday scaling is approximate because volatility is U-shaped across the day. Use a time-of-day variance profile, not √t, once 1-minute history exists. |
| Relative volume (RVOL) | `cum_volume(t) / median cum_volume at the same minute-of-day over the prior 20 sessions` | Minute bars | Time-of-day matched. Half-days are excluded from the baseline. |
| Alert trigger | `|z| ≥ k` **and** `RVOL ≥ v` (plus user-defined price levels) | — | `k` and `v` are **calibrated to a target false-alert rate** per watchlist-day (§4). They are not read from a normal table. |
| Context decomposition | Market move, sector move, residual | Benchmark returns over the same window | Shown on every alert ("SPY −1.2%, XLK −2.0%, residual −3.1%"). |

### Required data specification for the intraday detector

The detector above needs **consolidated (all-venue), full-volume, 1-minute OHLCV bars**. Each bar needs a trade-based timestamp and must be displayable to paying users. They may be 15-minute delayed.

A single-venue or partial-venue feed does not meet this. Examples:
- Cboe One, which carries about 10–15% of volume;
- IEX;
- a modelled "FMV" price.

With such feeds, RVOL is meaningless, and the price z-score reflects only part of the market.

As of 2026-09-24, **no priced pilot option is confirmed to meet this spec** ([11 §2 Q1](11-evidence-and-open-questions.md#2-open-questions)). The plausible candidates are:
- Massive Full Market Delayed ($499/mo; it may require the $2,499 base plan);
- Twelve Data Venture ($499/mo; feed composition unverified);
- Intrinio Enterprise with SIP-delayed ($1,250+/mo);
- Databento `EQUS.SUMMARY`, if minute granularity and display are confirmed.

**Fallback mode.** If G-DATA ([08](08-implementation-roadmap.md#stopgo-gates)) finds nothing affordable that meets the spec, the intraday detector runs **price-only**: the z-score on a partial-venue delayed feed, labelled "partial-venue price". Full-volume RVOL is then computed **end of day** from consolidated summary data. Validation (§4) must be repeated for this mode.

Deferred until later stages: technical indicators, factor models, screening, portfolio risk, and backtests. Each gets its own validation section before it ships (§7).

## 2. Data correctness invariants

These are enforced in code and tested. They are summarised again in `CLAUDE.md` for contributors.

1. **Timestamps.** Store every observation with `event_ts` (exchange or SIP timestamp), `provider_ts` if different, `ingest_ts`, and `source`, all as timezone-aware UTC. Never use naive datetimes. The session calendar comes from `exchange_calendars` (XNYS), not from weekday arithmetic.
2. **Adjusted and unadjusted are separate.**
   - Raw prints are stored unadjusted.
   - Adjusted series are derived with a versioned corporate-action table: split ratio and cash dividend, with ex-date, record date and pay date.
   - A return spanning an ex-date uses total-return adjustment. It is labelled "price return" or "total return" explicitly.
   - Never mix a provider's pre-adjusted history with our own adjustments.
3. **Point-in-time.**
   - Reference data (symbol, name, listing, sector) is stored as validity intervals (`valid_from`, `valid_to`).
   - Filings use EDGAR *acceptance* time.
   - News uses first-publication time from the wire, not the crawl time.
4. **No silent substitution.**
   - A value from a fallback source carries that source's label and entitlement class (real-time, delayed-15, EOD).
   - Delayed data is never displayed as live ([04 §5](04-real-time-data-strategy.md#5-freshness-and-degraded-mode-semantics)).
5. **No fabrication.** Missing data renders as missing. The estimated-history code in `finnhub_adapter.py:340-366` is deleted, not ported.
6. **Symbology.** Keep an internal `instrument_id`, mapped to ticker (time-varying), FIGI, and CIK. Ticker changes and reuse must not merge histories.
7. **Survivorship.** Once history is stored, delisted instruments stay in the database. Any historical statistic uses the point-in-time universe.

## 3. Asset-class specifics

### ETFs (in MVP scope)

- **Price vs. NAV.** Alerts use the market price. Show the premium or discount to the most recent official NAV, which is end of day, where it is available. Intraday indicative value (IIV/iNAV) is only shown if licensed; it is often a 15-second value with known quality issues for international and bond ETFs.
- **Distributions.** Handle ETF distributions like dividends in the total-return adjustment.
- **Holdings.** Holdings are T+1 at best, and vary by issuer. Any exposure or look-through calculation (post-MVP) must show the holdings `as_of` date.
- **Tracking difference.** Calculate tracking difference over the period against the index only if index data is licensed. This is out of MVP scope.
- **Leveraged and inverse ETFs.** The daily-reset maths makes multi-day comparisons against the underlying misleading. Flag these products in the UI.

### Bonds (excluded from MVP; see [02 §5](02-product-thesis.md#5-explicit-mvp-exclusions))

If bonds are ever added, the minimum correct treatment is:
- clean vs. dirty price, with accrued interest under the correct day-count convention (30/360 for most US corporates, ACT/ACT for Treasuries);
- yield to maturity or yield to worst for callable bonds;
- modified and effective duration, and convexity;
- a credit-spread measure;
- trade data from FINRA TRACE, which is sparse, delayed and licensed, and for munis from MSRB EMMA.

Illiquidity means "last trade" is often stale by days. Evaluated pricing (vendor marks) is the norm and is expensive. This is the main reason bonds are excluded ([03 §D](03-market-and-tooling-research.md#d-reference-fundamentals-filings-bonds)).

## 4. Alert-engine validation (MVP)

Validation is gated on historical replay before the pilot.

- **Replay harness.** Run the detector over stored minute bars for the pilot universe (≈1,000 liquid US stocks and ETFs), across ≥ 12 months. This window must include earnings seasons, half-days, a daylight-saving transition, and at least one high-volatility episode.
- **False-alert calibration** (Harvey, Liu & Zhu 2016 logic; Roll 1988 fat tails).
  - Choose `k` and `v` so the median user watchlist of 30 names gets about 1–3 alerts per day. This target is a proposal; validate it with pilot users.
  - Report the empirical per-ticker exceedance rate, not the Gaussian one.
- **Correctness tests.**
  - Golden-file tests of AR, z and RVOL against hand-computed spreadsheets for about 20 fixture days. These fixtures include a split day, an ex-dividend day, a half-day, a trading halt, a DST Monday, and an IPO with less history than the estimation window, where the alert must say "insufficient history".
  - Property tests:
    - a symmetric price path gives a symmetric z;
    - AR is zero when the stock equals the benchmark and β = 1;
    - adjustment is idempotent.
- **Cross-source reconciliation.** Each day, compare our computed close-to-close returns with a second source for a sample of 100 symbols. Any `|diff| > 1 bp` that is not explained by a corporate action creates a data-quality incident ([07](07-security-and-production-readiness.md)).
- **Latency measurement.** For each alert, record `event_ts → detect_ts → notify_ts`. Targets are in [04](04-real-time-data-strategy.md#2-real-time-requirements-per-workflow).

## 5. LLM explanations: evaluation

The design follows [papers §(b)](research/papers.md#b-evaluation-plan-for-grounded-llm-alert-explanations).

**Role.**
1. Retrieval is deterministic. It collects news, 8-K filings and earnings-calendar entries for the instrument, published in the window `[move_start − lookback, move_start + small grace]`.
2. The LLM selects which retrieved items are relevant and writes 1–3 sentences.
3. Every sentence must cite evidence IDs. The output must validate against a JSON schema.
4. **Abstention is a first-class output.** Intraday, identified news explains only about 12% of idiosyncratic volatility (Boudoukh et al. 2019), so "No company-specific catalyst found; sector moved −2%" will be the most common honest answer.

**Hard gates, checked on every response at runtime; the response is rejected on failure:**
- Every cited ID exists in the retrieved set.
- Every number in the text matches the deterministic engine output or a cited span.
- Evidence timestamps are no later than `move_start + grace`, or the evidence is labelled "reported after the move began".
- No advice or forecast language, checked with a deny-list plus a classifier.

**Offline eval before pilot:**
- Build a gold set of about 800 historical alerts: half with news and half without. Stratify by overnight vs. intraday, large vs. small cap, and event type.
- Metrics:
  - ALCE-style citation precision and recall;
  - FActScore-style atomic-claim support;
  - false-attribution rate on no-news cases;
  - false-abstention rate;
  - parametric-leak rate: remove the evidence, and check whether the model still names a catalyst. Also test with entity masking, following Glasserman & Lin 2023.
- Human AIS rubric: two raters with ≥ 20% overlap, target κ ≥ 0.6.

**Proposed release gates** (to be confirmed once measured):

| Metric | Gate |
|---|---|
| Hard checks | 100% |
| Citation precision | ≥ 0.95 |
| Atomic-claim support | ≥ 0.95 |
| False attribution on no-news | ≤ 5%, with the upper 95% CI ≤ 8% |
| Parametric leak | ≤ 1% |
| Human "fully attributable" | ≥ 90% |

**In production:** sample about 50 alerts per week for human audit, and track drift in these metrics. Pin the model and version prompts; any model or prompt change re-runs the offline eval.

**Not claimed:** sentiment scores, "confidence" numbers, or price direction. The current `confidence_score` field is removed.

## 6. Reproducibility and lineage

- Every alert row stores:
  - the detector version (git SHA);
  - parameter set ID;
  - input bar range and source;
  - corporate-action table version;
  - evidence IDs;
  - LLM model ID, prompt version and raw output.

  An alert must be fully re-derivable from these for at least the retention period ([07](07-security-and-production-readiness.md)).
- Datasets for calibration and evaluation are frozen as Parquet snapshots, with a manifest giving source, pull date and licence class. Experiments log their parameters and results. A simple `experiments/` directory with a manifest is sufficient; an MLflow-class tool only becomes justified once there are more than 50 runs a month.
- Licence constraint: some vendors restrict retention and derived works. The snapshot manifest must record whether retention is permitted ([04 §6](04-real-time-data-strategy.md#6-licensing-and-entitlements)).

## 7. Evidence required before later features ship

| Feature | Minimum evidence before it is shown to users |
|---|---|
| Any signal, score, or "setup" | Point-in-time data including delisted names. Walk-forward with a purge gap, plus an untouched holdout. Every variant logged. Deflated Sharpe > 0.95 and PBO < 0.2 (Bailey & López de Prado 2014; Bailey et al. 2017). t > 3. Net of costs with a sensitivity curve at 5, 10, 20 and 50 bp. Multi-year, multi-regime data. Beats buy-and-hold, SPY and sector ETFs, and simple momentum. Reported with a Sharpe standard error. |
| LLM-derived features in any backtest | Use only data after the model's training cutoff, or point-in-time models (ChronoGPT, TiMaGPT, DatedGPT, Kelly et al. 2026). Run a Lookahead-Propensity or masking audit ([papers §3](research/papers.md)). |
| Backtesting module | Borrow cost, and financing for leverage. Taxes are *out of scope*, stated explicitly. FX for non-USD instruments. Slippage from spread plus an impact model (Almgren–Chriss or Frazzini, Israel & Moskowitz 2018). Delisting returns (Shumway 1997). |
| Portfolio risk metrics | Deterministic formulas with documented conventions: return frequency, annualisation, benchmark, and look-back. Golden tests against QuantStats or empyrical-reloaded outputs on fixed fixtures ([03 §H](03-market-and-tooling-research.md#h-research-backtesting-portfolio-later-stages)). |
| Broker or paper trading | See [05 §9](05-target-architecture.md#9-future-execution-separation-not-in-mvp). |

**Explicitly rejected as evidence:**
- TradingAgents-style results. Three tickers over three months give a Sharpe standard error of about 8.
- A raw LLM "sentiment alpha" such as Lopez-Lira & Tang's. The tradable part is fragile to costs of about 20 bp and decays as adoption rises.
- Any backtest on data from before the LLM's training cutoff.
