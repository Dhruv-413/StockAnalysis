---
paths:
  - "ingestor/**"
  - "detector/**"
  - "decision/**"
  - "rules/**"
  - "notify/**"
---

# Quick-response path rules

The owner is `realtime-engineer`.

- Latency claims need measurements: p50, p95 and p99 per stage, derived from the timestamps `event_ts`, `provider_ts`, `ingest_ts`, `process_ts` and `display_ts`.
- Decisions are deterministic and versioned. Persist inputs, the rule or model version, and the output for every decision (audit trail). Alert and decision keys are idempotent.
- Handle reconnects, gaps (backfill; archive-only for old moves), duplicates, late events and backpressure explicitly.
- The ingestor is a singleton. It takes an advisory lock and is deployed stop-before-start.
- No order placement, broker calls, or code paths from alerts or LLM output to execution.
- Runtime or language changes need an ADR plus a benchmark on our workload (see `docs/production-plan/13-quick-response-system.md`).
