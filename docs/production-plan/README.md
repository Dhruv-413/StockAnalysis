# StockAnalysis → Production Plan

*Prepared 2026-09-24 on branch `v3` at commit `8e8dd33`. This is a plan, not an implementation. No product code was changed.*

> **Scope update (2026-09-24): owner decision pending.**
>
> The owner has since asked for a fast daily market assistant that is **India-first plus global**, for users of Zerodha, Groww, Angel One, TradingView and Bloomberg, answering in about 300 ms. [14](14-global-market-assistant.md) and [ADR-008](adr/ADR-008-india-first-market-assistant-scope.md) propose an **information-only India evidence assistant** with **card-first 300 ms answers**, reusing this plan's engine. The US plan below becomes the second leg.
>
> Four choices are open: scope, signals, what "300 ms" measures, and whether prices are real-time or delayed ([14 §9](14-global-market-assistant.md#9-decisions-needed-from-the-owner)).
>
> **Finance-specialised models (2026-09-24):** [15](15-finance-model-layer.md) and [ADR-009](adr/ADR-009-finance-model-layer.md). The deterministic finance engines (TA-Lib, HAR, EWMA, GARCH) are Adopt. Kronos and similar models are gated, offline challengers only. [15 §9](15-finance-model-layer.md#9-decisions-needed-from-the-owner) adds four more decisions for the owner.
>
> **India research round 3 (2026-09-24):** [16](16-india-research-round-3.md) covers Zerodha Kite and the other broker APIs, India papers, case studies and official sources. Kite can't be the data feed; it is a user-side MCP companion. It adds four more owner decisions.

## Executive overview

**What the repository is today.** A prototype FastAPI + Gemini API that answers free-text questions such as "why did Tesla drop today?". For one ticker it fetches a quote, headlines, and a period change from free-tier APIs, then asks an LLM for a summary. The README describes it as real-time and production-ready. It is neither:

- The analysis prompt **never receives the fetched news**, so the causes it gives are unsupported. This was verified with an offline harness.
- The app **fails to start** unless all five API keys are set.
- There are **no tests, CI, database, or users**.
- The data sources are **not licensed for display to paying users**.
- **Provider keys are in the public git history** and must be rotated.

Details: [01](01-repository-assessment.md).

**Recommendation.** Narrow the product to **Move Ledger** (working name). It is a watchlist-monitoring service for **US equities and ETFs** that:

- detects statistically abnormal moves deterministically, adjusted for market and sector, and calibrated to a target alert rate;
- attaches a **timestamped evidence ledger** built from SEC filings, earnings dates, and licensed or linked headlines, plus market and sector context;
- adds an optional **grounded summary that must cite that evidence or say "no company-specific catalyst found"**.

The first audience is **independent equity researchers**: newsletter writers, independent analysts, and small advisory shops. They cover 30–200 names and need citable explanations. The product sells auditability, coverage, and workflow (digest, export, archive). It does not sell speed, forecasts, or trading. See [02](02-product-thesis.md) and [ADR-001](adr/ADR-001-product-direction.md).

**Why this and not an AI trading platform:**
- Retail "why is it moving" features are free or bundled, from Robinhood, Schwab, Perplexity, and Snowball.
- Nobody offers an auditable, multi-name ledger with honest abstention.
- Research shows most intraday moves have no identifiable news, so abstention has to be a first-class feature.
- Trading, backtesting, and bonds each add licensing, regulatory, and correctness burdens that a small team cannot carry credibly ([03](03-market-and-tooling-research.md)).

**How to handle "real-time".**
- Define freshness per workflow and label every price with source, entitlement (`real-time`, `indicative`, `delayed-15`, `eod`), and as-of time.
- Never substitute delayed data silently. Show degraded modes explicitly.
- The pilot **deliberately does not show unlabelled real-time prices**.
  - It runs on **15-minute delayed, consolidated, full-volume 1-minute bars**, which carry no per-user exchange fees.
  - A **modelled "indicative" real-time** feed is optional and must be labelled.
  - The reason is that the target users are likely "professional" subscribers under exchange rules, and the product's value is evidence, not speed.
  - Hypothesis H4 tests whether users accept this. If they don't, the pilot switches to a labelled indicative real-time feed at about $2.5k/mo fixed (gate G-LATENCY).
  - It is **not yet confirmed** which vendor delivers the required consolidated delayed minute bars with display rights. If none does affordably, the detector degrades to a price-only mode.
- Filings from EDGAR arrive in near real time at no cost.
- Alerts target p95 ≤ 90 s after the bar is available.
- True real-time exchange data would cost about $12.6k/mo at 200 users on the SIP, and professional users cost about $92 each per month. It becomes a later paid upsell tier.
- Details: [04](04-real-time-data-strategy.md) and [ADR-002](adr/ADR-002-delayed-first-market-data.md).

**Architecture.**
- One Python 3.12 codebase running three process types: web, a single ingestor, and workers.
- One managed Postgres, natively partitioned and keyed by trading-session date, with an outbox and Postgres-backed jobs.
- Server-rendered UI; Clerk for auth; Postmark for email.
- No Redis, Kafka, or Kubernetes until measured triggers are hit.
- See [05](05-target-architecture.md) and [ADR-003](adr/ADR-003-modular-monolith-postgres.md).

## Key tradeoffs

| Choice | Gain | Cost / risk |
|---|---|---|
| Delayed-first data | $0 per-user exchange fees; viable for "professional" users | Alerts arrive about 16 min after the trade. Hypothesis H4 tests whether users accept this. |
| Evidence ledger + abstention | Trust, auditability, differentiation | More "no catalyst" answers, which may feel less magical (H3) |
| Narrow audience (independent researchers) | Clear willingness to pay ($39–299 comparables) and a clear workflow | A smaller market. The team tier and adviser features come later. |
| Modular monolith on Postgres | Cheap and simple for 1–2 engineers | A single ingestor is a single point of failure, mitigated by backfill and degraded modes |
| One canonical explanation per event | LLM cost scales with the universe, not with users; safer under the publisher's exclusion | Less personalisation |

## Major blockers

1. **Key rotation** for the leaked Google, Finnhub, Twelve Data, and Alpha Vantage keys. The owner must do this now ([07 §1](07-security-and-production-readiness.md#1-immediate-security-actions-before-any-other-work)).
2. **Written vendor confirmation of display rights.** It must cover a feed that meets the detector's data spec (consolidated, full-volume, 1-minute, delayed) and user exports. It must also clarify who is vendor of record ([11 §2](11-evidence-and-open-questions.md#2-open-questions)).
3. **Demand validation** through interviews and a blind ledger test before significant build spend (G-DEMAND).
4. **Counsel review** of the publisher's exclusion, jurisdiction, and user geography. The owner's location and target geography are unknown.
5. **Gold-set creation** (about 800 labelled alerts) before LLM summaries can be shown.

## Cost drivers

The main costs, all estimates:

- people;
- market-data licensing: pilot about $500–3,000/mo (unconfirmed until vendors answer T-06); growth about $2.5–5k/mo fixed;
- one-time legal and pentest: about $10–30k.

Infrastructure is about $100–250/mo at pilot. LLM cost is small under the per-event design. See [09](09-costs-and-operating-model.md).

## First milestone

**Stage 0: baseline and validation, 3–5 weeks.**

- Rotate keys (T-01).
- Add tooling and CI (T-02).
- Add characterisation tests (T-03).
- Apply prototype quick fixes (T-04).
- In parallel: customer interviews (T-05) and vendor due diligence (T-06).

It ends at the **G-DEMAND**, **G-LATENCY**, and **G-DATA** stop/go gates ([08](08-implementation-roadmap.md#stopgo-gates)).

## Documents

| # | Document | For |
|---|---|---|
| 01 | [Repository assessment](01-repository-assessment.md) | Developers: inventory, workflow trace, findings with `file:line`, checks run |
| 02 | [Product thesis](02-product-thesis.md) | Product owner: directions compared, scope, exclusions, hypotheses |
| 03 | [Market & tooling research](03-market-and-tooling-research.md) | Both: synthesis of the research appendices |
| 04 | [Real-time data strategy](04-real-time-data-strategy.md) | Developers: freshness semantics, ingestion, licensing |
| 05 | [Target architecture](05-target-architecture.md) | Developers: diagrams, modules, deployment, upgrade triggers |
| 06 | [Quantitative validation](06-quantitative-validation.md) | Developers and quants: formulas, invariants, evaluation gates |
| 07 | [Security & production readiness](07-security-and-production-readiness.md) | Both: security, SLOs, release gates, failure drills |
| 08 | [Implementation roadmap](08-implementation-roadmap.md) | Both: stages, first ten tasks, stop/go gates |
| 09 | [Costs & operating model](09-costs-and-operating-model.md) | Product owner: run-rate, unit economics, team |
| 10 | [Claude Code setup](10-claude-code-setup.md) | Contributors: config changes and validation |
| 11 | [Evidence & open questions](11-evidence-and-open-questions.md) | Both: fact vs. assumption register, blockers |
| 12 | [Team operating model](12-team-operating-model.md) | Everyone: roles, ownership, RACI, workflow, handoffs, agent teams |
| 13 | [Quick-response system](13-quick-response-system.md) | Both: fast fetch → decide → respond, latency tiers, Jev and similar tools |
| 14 | [Global & India market assistant](14-global-market-assistant.md) | Both: the owner's 300 ms daily-assistant ask; India data and SEBI; card-first architecture; options needing a decision |
| 15 | [Finance-specialised model layer](15-finance-model-layer.md) | Both: Kronos and its peers; evidence; simple vs layered architecture; model selection and gates |
| 16 | [India research round 3](16-india-research-round-3.md) | Both: Zerodha Kite and broker APIs, India papers, case studies, official sources; corrections; decisions |
| ADR | [001](adr/ADR-001-product-direction.md) · [002](adr/ADR-002-delayed-first-market-data.md) · [003](adr/ADR-003-modular-monolith-postgres.md) · [004](adr/ADR-004-llm-role-grounded-only.md) · [005](adr/ADR-005-retire-adk-and-nl-orchestrator.md) · [006](adr/ADR-006-quick-response-tier-and-runtime.md) · [007](adr/ADR-007-jev-as-optional-triage-classifier.md) · [008](adr/ADR-008-india-first-market-assistant-scope.md) · [009](adr/ADR-009-finance-model-layer.md) | Durable decisions (all *Proposed*) |
| Research | [market-data](research/market-data.md) · [products](research/products.md) · [infrastructure](research/infrastructure.md) · [papers](research/papers.md) · [low-latency](research/low-latency.md) · [fast-fetch](research/fast-fetch.md) · [decision-engines](research/decision-engines.md) · [reactive-and-jev](research/reactive-and-jev.md) · [india-market-data-and-sebi](research/india-market-data-and-sebi.md) · [global-news-and-data](research/global-news-and-data.md) · [assistant-300ms-and-jev](research/assistant-300ms-and-jev.md) · [distribution-and-competitors-india](research/distribution-and-competitors-india.md) · [accuracy-indicators-algos](research/accuracy-indicators-algos.md) · [finance-models-catalogue](research/finance-models-catalogue.md) · [finance-models-evidence](research/finance-models-evidence.md) · [kite-and-broker-apis](research/kite-and-broker-apis.md) · [papers-india](research/papers-india.md) · [case-studies](research/case-studies.md) · [official-sources-and-tools](research/official-sources-and-tools.md) · [tech-radar](research/tech-radar.md) | Raw evidence with sources |

**Evidence conventions:**
- **[Verified]** means executed or read directly.
- **Estimates** and **proposals** are labelled as such.
- Web sources were accessed 2026-09-24.
- Confidence is H, M, or L per claim, as recorded in the research appendices.
