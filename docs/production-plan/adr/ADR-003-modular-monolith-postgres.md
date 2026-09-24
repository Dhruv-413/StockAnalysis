# ADR-003: Modular monolith on Postgres, with three process types

- **Status:** Proposed (2026-09-24)
- **Deciders:** repository owner

## Context
- The team is 1–2 engineers.
- The workload is minute-bar monitoring for about 1,000–5,000 US symbols, plus event-driven evidence retrieval and notifications.
- Vendors allow a single market-data WebSocket per API key (Alpaca; Massive per asset class). The ingestor therefore has to be a singleton.
- Managed Postgres offerings (Fly, Render, Neon, RDS, Supabase on PG17) do not provide TimescaleDB compression or continuous aggregates. Tiger Cloud or self-hosting does.
- US equities are expected to move to 23/5 trading (an overnight session) around 2026-12-06. Neither calendar library models it yet.

Source: [research/infrastructure.md](../research/infrastructure.md).

## Decision
- One Python 3.12 codebase and container image, run as three process types:
  - `web` (FastAPI + Jinja/HTMX);
  - `ingestor` (exactly one, guarded by an advisory lock, deployed stop-before-start);
  - `worker` (Procrastinate jobs + APScheduler).
- A single managed Postgres holds everything:
  - `bars_1m` uses native monthly range partitions keyed on **trading-session date**;
  - jobs use a transactional outbox plus LISTEN/NOTIFY as a wake-up signal.
- No Redis, Kafka, or Kubernetes in the MVP.
- Host on Fly.io or Render in US-East. Not Cloud Run, which has a 60-minute WebSocket cap.
- Calendar = `exchange_calendars` XNYS + a `session_overrides` table. Pin `tzdata`.

## Consequences
- Cheap (infrastructure about $50–150/mo) and simple to run.
- The upgrade triggers are measured and documented in [05 §8](../05-target-architecture.md#8-when-to-add-infrastructure). Partitioned Postgres to TimescaleDB is a low-risk migration because both are Postgres.
- The single ingestor is a single point of failure. That is mitigated by fast restart, gap backfill, and degraded-mode signalling rather than by redundancy. Revisit if SLO breaches are traced to it.
