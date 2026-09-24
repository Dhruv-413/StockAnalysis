# 11 — Evidence Register and Open Questions

← [Index](README.md) · Previous: [10 Claude Code setup](10-claude-code-setup.md)

Research date and access date for all web sources: **2026-09-24**. Full source lists with URLs, publication dates and confidence ratings are in the research appendices:

| Appendix | Scope |
|---|---|
| [research/market-data.md](research/market-data.md) | Vendors, exchange/SIP licensing, EDGAR, FRED, OpenFIGI, TRACE, news licensing, Gemini status. About 70 sources. |
| [research/products.md](research/products.md) | Competitors, prices, open-source licences, regulation. 42 sources. |
| [research/papers.md](research/papers.md) | Research papers, with verdicts and evaluation design. |
| [research/infrastructure.md](research/infrastructure.md) | Storage, queues, calendars, deployment, auth, notifications, LLM tooling. |
| [research/low-latency.md](research/low-latency.md) · [fast-fetch.md](research/fast-fetch.md) · [decision-engines.md](research/decision-engines.md) · [reactive-and-jev.md](research/reactive-and-jev.md) | Quick-response system: latency tiers, feeds and protocols, rule and decision engines, Jev, Akka/Pekko and reactive alternatives. |
| [research/tech-radar.md](research/tech-radar.md) | Consolidated Adopt/Trial/Assess/Hold view. |

The appendices were produced by parallel research agents that were told to prefer primary sources, and then reconciled by the lead author. Claims marked **M** or **L** in the appendices have not been confirmed on a primary page. Treat them as leads to check, not as facts.

## 1. Classification of key statements

| Statement | Type | Basis |
|---|---|---|
| Analysis prompt omits fetched news | **Verified fact** | Offline harness ([01 §3](01-repository-assessment.md#3-end-to-end-workflow-trace-post-apiv1analyze)) |
| App fails to start without the Twelve Data, Alpha Vantage or Marketaux key | **Verified fact** | Import run ([01 §5](01-repository-assessment.md#5-checks-performed)) |
| Keys exposed in public git history | **Verified fact** | `git show` (values redacted); `gh repo view` reports `PUBLIC` |
| Current providers don't license display to paying users | **Verified (vendor terms, H)** | [market-data §A](research/market-data.md) |
| Delayed (15 min) display carries no per-user CTA/UTP fees | **Verified (H)** | CTA and UTP schedules |
| CT Plan fees start 2027-04-01; DataCT agreement needed by 2027-03-01 | **Verified (H)**; fee amounts **M** | SEC order; CT Plan notices |
| Retail "why is it moving" features are commoditised | **Verified (H)** for Robinhood, Schwab, Perplexity, Snowball | [products §2](research/products.md) |
| Independent researchers will pay $39–79/mo for evidence ledgers | **Hypothesis** | Adjacent price points only. To be validated (H5) |
| Intraday moves mostly lack identifiable news (about 12% of idiosyncratic volatility is news-explained) | **Published finding** (Boudoukh et al., RFS 2019) | [papers §10](research/papers.md) |
| Delayed prices are acceptable to the target users | **Assumption** | To be validated (H4) |
| Pilot data cost about $500–3,000/mo | **Estimate** | Vendor list prices (H/M). It is not confirmed which option meets the detector data spec, or what its display rights are |
| Effort 33–47 engineer-weeks | **Estimate** | Author judgement from task decomposition |
| US equities/ETFs as the market | **Assumption** | Inferred from the repo's providers and examples |
| Watchlist alerts fall within the publisher's exclusion | **Unresolved, legal** | *Lowe v. SEC*; *Seeking Alpha* (S.D.N.Y. 2024) is supportive but not binding |

## 2. Open questions

### Blocking before the pilot contract (owner and vendors)

1. **Data spec and display rights.** Which vendor delivers **consolidated, full-volume, 1-minute OHLCV, 15-minute delayed, displayable to paying users**, and at what price ([06 §1](06-quantitative-validation.md#required-data-specification-for-the-intraday-detector))? Intrinio Startup's delayed feed is Cboe One, only about 10–15% of volume, so it does **not** meet the spec. Answers are also needed on three vendor configurations:
   - Does Databento Standard plus US Equities Mini permit display to paying external users? What does it cost today? (The $199 figure comes from a January 2025 blog.)
   - Do Massive's "Full Market Delayed" add-ons require the $2,499 Business base plan? The pilot cost differs about 6× depending on the answer.
   - Does Twelve Data Venture include exchange fees?
2. **Vendor of record.** For delayed CTA/UTP display, are we or our vendor the "vendor"? This decides who signs the NYSE/UTP agreements and who pays the $250/mo UTP delayed-redistributor fee.
3. **Storage and derived-data rights.** Can we store bars and computed alerts indefinitely? Can we show LLM summaries written from licensed news text? Every vendor must answer in writing.
4. **User exports and republication.** Newsletter writers republishing exported ledgers to their own readers is third-party redistribution. What does each vendor permit? Until answered, exports are limited to derived statistics, EDGAR content, and headline links ([02 §4](02-product-thesis.md#core-workflows-mvp)).
5. **Non-display classification.** Does running alert rules on *delayed* data count as non-display use? On real-time data it does, which adds fees.

### Blocking before public launch (owner and counsel)

6. **Operating entity, jurisdiction and user geography.** The plan assumes US users. The owner's location and whether non-US users (EU/UK GDPR, India SEBI, etc.) are served are **unknown**.
7. **Publisher's exclusion.** Does it cover per-watchlist alerts and LLM summaries? Is a single canonical explanation per event required? What disclaimers are needed?
8. **Professional status.** How do we attest professional vs. non-professional status, and what records must we keep under vendor and exchange agreements?

### Product (resolved in Stage 0 interviews)

9. Is the primary persona newsletter writers, small RIAs or active pro-am investors? This changes pricing, the need for team features, and exposure to professional-user fees.
10. How many alerts per watchlist per day is useful, and how much is too many? The current target is 1–3 per 30 names.
11. Is web push required for the pilot, or is email enough?

### Technical (resolved in Stage 1)

12. Is TimescaleDB needed, or is plain partitioned Postgres enough at 3,000 symbols × 390 minutes × 2 years (about 585M rows)? See [ADR-003](adr/ADR-003-modular-monolith-postgres.md).
13. What is the quality of intraday relative volume from a delayed, full-volume feed compared with a single-venue real-time feed?
14. **Jev (TypeSafe AI).** We need its terms and AUP (financial or automated-decision use, retention, training on inputs), its serving region, SLA and rate limits, and whether licensed news text may be sent to it. These block Q-05 and production use ([ADR-007](adr/ADR-007-jev-as-optional-triage-classifier.md)).
15. **Real-time evidence feeds.** We need confirmed latency and terms for sec-api.io, RTPR and the Benzinga WebSocket. The vendors' latency claims are unverified ([fast-fetch](research/fast-fetch.md)).
16. Which Gemini model and version to pin? Should a second provider (for example Claude) be evaluated for citation faithfulness on the gold set?

## 3. Evidence that was unavailable

These items were searched for but not confirmed. See the "could not verify" section of each appendix.

- Finnhub's candle premium badge (the docs page renders with JavaScript) and Finnhub/Marketaux commercial pricing.
- Exhibit F of the CT Plan approval order (final fees). UTP non-display and access fee amounts.
- Whether any competing consolidator is operating.
- Pricing for Fiscal.ai, QuantConnect, AInvest and Stocktwits monthly plans. Whether Benzinga WIIM is written by people or by AI.
- A public benchmark for faithfulness of "why is this stock moving" explanations. The search found **none**, so we must build our own gold set.
- Lopez-Lira & Tang journal status and version date: conflicting.
- Anything requiring live API calls against this repository's providers. None were made, by design.

## 4. Change log

| Date | Change |
|---|---|
| 2026-09-24 | Initial assessment, thesis, research and plan |
