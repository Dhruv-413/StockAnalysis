# 09 — Costs and Operating Model

← [Index](README.md) · Previous: [08 Roadmap](08-implementation-roadmap.md) · Next: [10 Claude Code setup](10-claude-code-setup.md)

**Every figure here is an estimate.** Estimates are built from list prices accessed on 2026-09-24 ([research/market-data.md §2](research/market-data.md), [research/infrastructure.md](research/infrastructure.md)). Formulas are shown so they can be recomputed. Items marked ⚠ depend on vendor answers that have not yet been confirmed ([11 §2](11-evidence-and-open-questions.md#2-open-questions)). Salaries are excluded because location and staffing model are unknown. People are the dominant cost at every stage.

---

## 1. Monthly run-rate by stage

| Line item | Dev (Stage 0–1) | Pilot (50–200 users, Stage 3–4) | Growth (~5,000 users) |
|---|---|---|---|
| **Market data** | $0–250. Free or dev tiers for internal use (Alpaca Basic, Massive Starter $29). Optionally a history tier such as Massive Advanced $199, internal use only | **$500–3,000** ⚠, $0 per user. For a feed that meets the [06 §1 data spec](06-quantitative-validation.md#required-data-specification-for-the-intraday-detector): Massive Full Market Delayed $499 (or $2,998 if the $2,499 base is required); Twelve Data Venture $499; Intrinio Enterprise $1,250+. Plus $0–250 UTP delayed-redistributor fee. The partial-venue fallback (Intrinio Startup $333→$999 plus Databento $199) is $530–1,450. The indicative real-time switch (G-LATENCY) is about $2,500 | **$2.5–5k** ⚠ fixed for delayed data plus an FMV or derived feed. The real-time upsell adds fees passed through (§3) |
| News licence | $0 (EDGAR; headline links) | $0 (EDGAR plus links), or Benzinga quote ⚠ | Benzinga or equivalent, quote ⚠ (placeholder $500–2,000) |
| Compute (Fly/Render, US-East) | $10–30 | $40–80 (2× web at 1 GB, 1 ingestor, 1–2 workers) | $300–600 |
| Postgres | $0–38 (Neon free or Fly MPG Basic) | $72–110 (Fly MPG Starter plus about 60 GB) | $150–500 (Tiger Cloud Timescale after the [05 §8](05-target-architecture.md#8-when-to-add-infrastructure) triggers) |
| Object storage and backups | ~$1 | ~$5 | $20–50 |
| Email (Postmark) | $0 (dev tier) | $15 | $300–450 (about 300k emails/mo) |
| Auth (Clerk) | $0 | $0 | $0 (below 50k monthly retained users) |
| Errors / observability (Sentry, Grafana Cloud) | $0 | $26 (Sentry Team) | $80–200 |
| LLM (paid tier, pinned flash-lite/flash model) | $5–20 | $10–200 | $50–800 (§2) |
| Payments (Stripe, 2.9% + $0.30) | — | ~3.5% of revenue | ~3.5% of revenue |
| **Total, excluding people and payments** | **≈ $20–400** | **≈ $650–3,500** | **≈ $3.5–9.5k** |

## 2. The LLM cost driver

- **Per-user design** (the market-data appendix's assumption): users × alerts per day × days × tokens. That gives 5,000 × 20 × 30 = 3M calls/mo. At about 1,500 input and 300 output tokens per call, this is about **$810/mo on `gemini-2.5-flash-lite`** or about **$3.6k/mo on `gemini-3.5-flash-lite`** ([market-data §2](research/market-data.md)).
- **This plan's design** is **one canonical explanation per (instrument, event)**, shared by every user who watches that instrument. Counsel prefers this too ([07 §7](07-security-and-production-readiness.md#7-regulatory-questions-to-resolve-counsel-required-not-legal-advice)).
  - Formula: universe × events per symbol per day × trading days. For example, 3,000 × 0.5 × 21 ≈ 31.5k calls/mo, which is **≈ $10–130/mo** depending on the model.
  - Cost now scales with the size of the universe, not the number of users.
- **Evaluation runs:** 800 cases × 3–5 model or prompt variants per iteration adds a few dollars per run.

## 3. Real-time upsell economics (for a Stage 6 decision)

| Feed | Fixed cost | Per non-pro user | Per pro user | Break-even example |
|---|---|---|---|---|
| Cboe One Summary | $5,000 + $1,000 consolidation | $0.25 | $10 | At a $20/mo upsell: (6,000) / (20 − 0.25) ≈ **304 non-pro upsell users** |
| Nasdaq Basic (via vendor) | $2,140 × 1.029 | $1.00 (3 markets) | $28.50 | At a $20/mo upsell: about **116 non-pro users**, but a pro user costs $28.50, so pros need a higher price. Non-display fees ⚠ not verified |
| SIP today (CTA+UTP) | ≈ $12k (redistribution + access + non-display) | $3 | $92 | ≈ 700 non-pro users at $20, or a pro tier priced above $92 |
| SIP under the CT Plan (from 2027-04-01) | ≈ $3.5k + access and non-display ⚠ | $0.90 × 3 (first 2,000 users) | $73 | Re-model once Exhibit F is confirmed. Agreement with DataCT required by 2027-03-01 |

Implication: real-time data belongs in a **separately priced tier**, gated by a non-professional attestation, once there are at least 150 paying users ([08 Stage 6](08-implementation-roadmap.md#stage-6--later-expansion-only-with-evidence)).

## 4. Unit economics at the pilot (illustrative)

- Assumed price is **$49/mo**, the midpoint of the $39–79 hypothesis; it needs validation.
- **Fixed costs:** $650–3,500/mo, depending on the T-06 data outcome.
- **Break-even on direct costs:** about $3,500 / ($49 × 0.965) ≈ **74 paying users** at the high end of costs, or about 14 at the low end.
- **At 200 users:** revenue ≈ $9,800/mo against $0.65–3.5k of direct costs, a **contribution margin of about 60–90%** after payment fees and before people costs.
- **G-PILOT** ([08](08-implementation-roadmap.md#stopgo-gates)) requires this to hold with the vendor's *confirmed* pricing.

## 5. One-time costs to production (estimates)

| Item | Estimate | Note |
|---|---|---|
| Legal: publisher's-exclusion memo, ToS/Privacy, vendor-contract review | $5–15k | Get quotes; depends on jurisdiction |
| External pentest (auth, IDOR, web) | $5–15k | Before GA (gate G6) |
| Gold-set annotation | 60–80 hours | Internal or contractor; financially literate annotators |
| Historical data for calibration (2 years of minute bars) | $0–1,000 | Depends on the vendor's history licence for internal use ⚠ |
| Design/UX (pilot polish, accessibility) | 0.3 FTE across Stages 2–4 | — |

## 6. Operating model

- **Team (pilot):**
  - 1 senior Python engineer, who owns the platform and on-call;
  - 0.3 FTE frontend/design;
  - the product owner, who handles support, interviews and vendor relations;
  - counsel on retainer or hourly.
- **Team (GA):** add a second engineer, so on-call is not a single person, and part-time data QA or annotation.
- **Market-hours coverage.** Alerting only matters 09:30–16:00 ET, plus pre-open jobs. On-call is **market hours plus the pre-open window** on weekdays, with automated paging on freshness and latency SLO burn. Nights and weekends get best-effort response unless 23/5 alerting is added.
- **Weekly rituals:**
  - alert-quality audit of 50 alerts;
  - review of calibration drift;
  - vendor-quota and cost review;
  - incident review.
- **Monthly:** secret-rotation checks; dependency updates; licence register review, including vendor terms changes; restore drill every quarter.
- **Cost controls:**
  - a daily LLM token cap;
  - per-provider request budgets;
  - storage tiering to Parquet;
  - billing alerts on every cloud account;
  - no auto-scaling beyond 2× without review.
