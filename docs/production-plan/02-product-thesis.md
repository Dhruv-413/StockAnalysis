# 02 — Product Thesis

← [Index](README.md) · Previous: [01 Repository assessment](01-repository-assessment.md) · Next: [03 Market & tooling research](03-market-and-tooling-research.md)

**Status: proposal.** This recommendation has to pass the validation gates in §7 before significant build spend. Competitive evidence and prices are in [research/products.md](research/products.md). Licensing evidence is in [research/market-data.md](research/market-data.md). Both were accessed 2026-09-24.

---

## 1. Recommendation in one paragraph

Build **"Move Ledger"** (working name). It is a watchlist-monitoring service for **US-listed equities and ETFs**. It detects statistically abnormal price and volume moves using deterministic, market- and sector-adjusted measures. For each move it attaches a **timestamped evidence ledger**:

- SEC filings;
- earnings-calendar events;
- licensed or linked headlines;
- sector and market context.

It then writes, optionally, a short summary **grounded only in that evidence**, with an explicit "no company-specific catalyst found" when the evidence is missing.

The first audience is **independent equity researchers**: newsletter and Substack writers, independent analysts, and 1–3 person advisory shops. Each covers 30–200 US names and must explain moves to *their own* readers or clients with sources they can cite.

The product sells **auditability, coverage and workflow** (digest, export, archive). It does not sell speed, forecasts or trade execution.

## 2. Why this direction

| Factor | Evidence |
|---|---|
| Closest to the existing repo | The repo already frames the question ("why did X move?") and has multi-provider fetch plus LLM summary plumbing ([01 §6](01-repository-assessment.md#6-reuse-vs-redesign)). |
| The retail version is commoditised | Robinhood Cortex Digests come with Gold at $5/mo, popular stocks only. Schwab Portfolio Insights is free, with a disclaimer that it "may be… hallucinated". Perplexity Finance is free with cited answers. Snowball includes "Why is it moving" at $14.99/mo. Benzinga WIIM is sold wholesale ([products §0, §2](research/products.md)). |
| The gap is auditability and multi-name workflow | None of those products exposes a per-claim evidence ledger with timestamps relative to the move, calibrated abstention, small and mid-cap coverage, export of cited notes, or a searchable event archive ([products §0](research/products.md)). |
| Research supports abstention as a core feature | Identified news explains about 49.6% of overnight but only about 12.4% of intraday idiosyncratic volatility (Boudoukh et al., RFS 2019; [papers §10](research/papers.md)). An honest product must often say "no catalyst found", and competitors do not advertise this. |
| Data economics fit the audience | Newsletter writers and advisers are often **"professional" subscribers** under exchange rules. Real-time SIP display then costs about $92 per user per month, plus about $12k/mo fixed at pilot scale. **15-minute delayed display carries no per-user exchange fees** ([market-data §C](research/market-data.md)). The value of this product is evidence, not milliseconds, so a delayed-plus-indicative design is commercially viable where a real-time terminal is not. |
| Regulatory posture | Impersonal, general-circulation publishing that is not tailored to any user's portfolio fits the publisher's exclusion (*Lowe v. SEC*, 1985) ([products §regulation](research/products.md)). Watchlist-triggered alerts are *probably* consistent with it (*Seeking Alpha* S.D.N.Y. 2024, one district court). **Counsel review is required before launch** ([11](11-evidence-and-open-questions.md)). |
| Willingness to pay | Pro-am and adviser tools sell at $39–299/mo: Finviz Elite $39.50, Koyfin Premium $79, Koyfin Advisor $209–299, Benzinga Pro $37–197 ([products §1–2](research/products.md)). |

## 3. Directions compared

| Direction | Target user and recurring problem | Existing alternatives | Distinctive value we could add | Repo fit | Data and permissions | Build/ops complexity | Business model / WTP | Main failure reasons |
|---|---|---|---|---|---|---|---|---|
| **(b) Monitoring + explainable alerts** ✅ | Independent researcher covering 30–200 names: "which of my names moved abnormally, and is there a documented reason?" Recurs every trading day. | Benzinga Pro/WIIM, Perplexity alerts, Robinhood/Schwab AI, TradingView alerts (watchlist alerts only on Premium+) | Evidence ledger with timestamps; calibrated alerts; honest abstention; export and archive; broker-agnostic | **High**: same question, reusable adapters | Delayed full-volume bars + EDGAR (free) + calendar + headline links; LLM API | Medium: streaming ingestion, scheduler, calibration | $39–79/mo individual; team tier later | Perplexity/brokers add ledgers and export; users want speed, not evidence; licensing costs rise |
| (a) Research & screening | Idea generation, fundamentals | Koyfin, Finviz, Fiscal.ai, Seeking Alpha, free Perplexity | Little on its own | Low: no screener or fundamentals pipeline | Fundamentals licence with display rights | Medium-high | Crowded at $0–79 | Commodity; hard to differentiate |
| (c) Portfolio / exposure / risk | "What am I exposed to?" | Portfolio Visualizer ($0–55), Sharesight, Snowball, broker tools | Event-aware exposure | None (no portfolio code) | Holdings import, ETF look-through data | Medium | $7–25/mo trackers | Personalised output edges towards advice; cheap incumbents |
| (d) Strategy research / backtesting | Quant hobbyists | QuantConnect/LEAN, NautilusTrader, vectorbt (Commons Clause), free OSS | Little | None | Point-in-time survivorship-free data (expensive) | High (correctness burden, [06 §7](06-quantitative-validation.md)) | Low WTP; free OSS dominates | Overfitting, data cost, crowded |
| (e) Paper / broker-connected trading | Active traders | Brokers themselves (Public AI Agents, Robinhood Cortex), Composer | None defensible | None | Broker partnership; possibly BD/RIA registration | Very high (risk controls, reconciliation) | Brokerage economics we don't own | Regulatory load; liability; incumbents |

**Ranking:** (b) ≫ (a) as a later supporting layer (Q&A over our own event archive) > (c) as impersonal watchlist exposure views only > (d) > (e).

## 4. Scope of the first release

- **Geography and market:** US-listed securities only (NYSE, Nasdaq, NYSE American, NYSE Arca, Cboe listings). US is assumed because the repo and its providers are US-centric. Other markets are an open question ([11](11-evidence-and-open-questions.md)).
- **Asset classes:** common stocks and ETFs. ETFs get NAV-premium context and leveraged/inverse flags ([06 §3](06-quantitative-validation.md#3-asset-class-specifics)).
- **Universe:** about 1,000–3,000 liquid names initially (Russell 1000 plus the top ~500 ETFs by ADV). A user's watchlist may add other US listings, which get "limited history" handling.
- **Freshness:** see [04](04-real-time-data-strategy.md). In short:
  - pilot prices are 15-minute delayed, or labelled *indicative* real-time, never unlabelled;
  - filings and news are ingested in near-real-time;
  - alerts fire within about 1–2 minutes of the (delayed or indicative) bar that triggers them.

### Core workflows (MVP)

1. **Watchlists.** Create or import (CSV or paste) up to 200 symbols per list, with up to 5 lists. Symbols resolve to internal instruments (FIGI/CIK), with warnings for ambiguous tickers.
2. **Abnormal-move alerts.**
   - Detection: market- and sector-adjusted abnormal return z-score plus time-of-day relative volume, calibrated to a target alert rate, plus simple price-level rules the user sets.
   - Delivery: in-app, email and web push.
   - Every alert shows its data source, delay class and timestamps.
3. **Evidence ledger per alert.**
   - SEC filings (8-K items, Forms 4, 10-Q/K, S-1, SC 13D/G) with acceptance time.
   - Earnings date and time.
   - Headlines (link-and-headline only unless licensed).
   - Market and sector move decomposition.
   - Each item is marked *before*, *during* or *after* the move started.
   - An optional grounded summary with citations, or an explicit abstention.
4. **Daily digest.** A pre-open, post-close summary across all watchlists: the top abnormal moves, new filings and upcoming earnings.
5. **Export and archive.** A searchable history of alerts and ledgers. Copy or export as Markdown or CSV with source links, for newsletters and client notes. Users can give feedback ("useful / not useful / wrong catalyst"), which feeds calibration.
   - When a subscriber republishes an export to *their* readers, that is third-party redistribution, and display licences usually forbid it.
   - Until vendors confirm otherwise (T-06), exports contain only:
     - our derived statistics (percent moves, z-scores, market/sector context), with no raw vendor price series;
     - EDGAR content;
     - headline + source + link;
     - our own summary text.

## 5. Explicit MVP exclusions

- Bonds, munis, options, futures, crypto, FX, and non-US listings. For bonds, TRACE/MSRB licensing and pricing methodology are a separate product ([06 §3](06-quantitative-validation.md#3-asset-class-specifics); [market-data §D](research/market-data.md)).
- Order entry, broker connections, paper trading, and portfolio or position import.
- Buy/sell ratings, price targets, forecasts, "signals", sentiment scores, and "confidence" numbers.
- Backtesting UI, screeners, fundamentals tables, and charting beyond a simple intraday sparkline.
- Free-form chat or agentic tool use. The Google ADK path is retired ([01 §6](01-repository-assessment.md#6-reuse-vs-redesign)).
- Consolidated real-time (SIP) quotes in the pilot, which is a paid upsell later ([04 §6](04-real-time-data-strategy.md#6-licensing-and-entitlements)).
- Native mobile apps. The web app is responsive, with web push.
- Multi-tenant organisations, SSO and team billing. A team tier comes after pilot evidence.

## 6. Product hypotheses and how to validate them

| # | Hypothesis | Validation method (before or during Stage 0–1) | Pass threshold (proposal) |
|---|---|---|---|
| H1 | Independent researchers spend ≥ 20 min per trading day working out why names moved, and they value cited sources | 12–15 structured interviews (newsletter writers from Substack investing, small RIAs, active pro-am investors), plus a diary study of 5 users for 1 week | ≥ 60% report the problem weekly; median ≥ 20 min per day |
| H2 | An evidence ledger with timestamps is preferred over a one-line "why" | Show 20 real historical alerts in two formats, WIIM-style line vs. ledger, blind | ≥ 70% prefer the ledger; ≥ 50% say they would cite it |
| H3 | "No catalyst found" increases trust rather than reducing perceived value | Include honest abstentions in the H2 test set | Trust rating not lower than for explained moves; ≤ 20% call it "useless" |
| H4 | 15-minute delayed prices are acceptable when alerts are about explanation, not execution | Ask directly; watch concierge-pilot behaviour | ≥ 60% accept delayed with an optional real-time upsell |
| H5 | Willingness to pay is $39–79/mo | Fake-door pricing page, then a paid concierge pilot | ≥ 10 paying users at ≥ $39/mo within 8 weeks of pilot start |
| H6 | Calibrated alerts are not noisy | Replay calibration ([06 §4](06-quantitative-validation.md#4-alert-engine-validation-mvp)), then pilot feedback | ≤ 3 alerts per 30-name watchlist per day; ≥ 50% rated "useful" |
| H7 | Grounded summaries are faithful enough to show | Offline eval gates ([06 §5](06-quantitative-validation.md#5-llm-explanations-evaluation)) | Meets all proposed release gates |

## 7. Stop/go gates tied to this thesis

(Detailed in [08](08-implementation-roadmap.md#stopgo-gates).)

- **After interviews (H1–H3):** if fewer than 60% report the problem weekly, or the ledger isn't preferred, **stop**. Reconsider (a) or (c) as impersonal watchlist exposure views.
- **If demand passes but H4 fails** (users reject delayed prices), **switch the pilot to labelled indicative real-time**. This is a fee-free, modelled FMV feed at about $2.5k/mo fixed, with no per-user fees even for professionals. Re-run the unit economics at that cost (G-LATENCY in [08](08-implementation-roadmap.md#stopgo-gates)).
- **After data quotes (G-DATA):** if no vendor confirms display rights for consolidated full-volume delayed 1-minute bars at about $3,000/mo or less, run the **price-only partial-venue fallback** ([06 §1](06-quantitative-validation.md#required-data-specification-for-the-intraday-detector)). If there is no displayable feed at all, fall back to EOD alerts plus real-time EDGAR filings.
- **After the paid pilot (H5–H7):** fewer than 10 paying users, or failing the evaluation gates, means **no production investment**.

## 8. Why not an "all-in-one AI trading platform"

- Every added capability multiplies licensing (display, non-display and professional fees), regulatory exposure (advice and brokerage) and correctness burden (backtests, [06 §7](06-quantitative-validation.md#7-evidence-required-before-later-features-ship)).
- Brokers already ship AI features free or bundled with trading ([products §2](research/products.md)).
- The repo's reusable asset is a narrow explanation workflow, not a platform.
- A small team can make *one* workflow trustworthy. It cannot make five trustworthy.
