# ADR-006: Quick-response latency tier A (~1 s) on Python, with a layered deterministic decision engine

- **Status:** Proposed (2026-09-24)
- **Deciders:** repository owner
- **Evidence:** [13](../13-quick-response-system.md); research appendices [low-latency](../research/low-latency.md), [fast-fetch](../research/fast-fetch.md), [decision-engines](../research/decision-engines.md) and [reactive-and-jev](../research/reactive-and-jev.md)

## Context
The owner wants a system that fetches, decides and responds quickly, and is open to any language. The research found several constraints:

- Latency is set by network distance, the vendor, the data entitlement and the delivery channel.
  - The physical floor from AWS us-east-1 to NJ is about 2 ms one way.
  - Retail WebSockets have millisecond-scale medians.
  - Pilot prices are 15-minute delayed.
- Sub-millisecond latency requires colocation and direct feeds.
- The team is 1–3 people and the quant/ML ecosystem is in Python.
- Deterministic rule engines give microsecond decisions that can be replayed and audited: GoRules Zen (MIT, Rust core, Python binding) and CEL.

## Decision
1. **Target tier A (about 1 s).**
   - Evidence events: event arrival to in-app alert at p95 ≤ 1 s.
   - Price events: p95 ≤ 1 s after the bar or print becomes available under our entitlement.
2. **Runtime.** Python asyncio on Linux (uvloop + picows + msgspec). Develop in WSL2 on Windows, because uvloop does not support Windows.
3. **Decision layers:**
   - **L0:** deterministic detectors.
   - **L1:** Zen JDM rules kept as versioned JSON in git, plus CEL for user-defined conditions.
   - **L2:** an optional typed text-triage step that only enriches or prioritises, with a timeout ([ADR-007](ADR-007-jev-as-optional-triage-classifier.md)).
   - **L3:** an asynchronous grounded explanation ([ADR-004](ADR-004-llm-role-grounded-only.md)).

   Every decision record stores the input snapshot, the rule SHA, the engine version, the trace and the output, orchestrated durably with DBOS on Postgres.
4. **Changing language or runtime.**
   - Rust via PyO3 for a profiled hot spot.
   - Apache Pekko, not Akka (BSL), only with JVM skills and a clustering or event-sourcing need.
   - Tier B or C only with an approved use case, a benchmark on our own workload, and new entitlements.

## Consequences
- No language migration now; the existing FastAPI and pydantic skills carry over.
- Adds dependencies to vet in Q-03 and Q-04: `zen-engine`, `cel-python`, `dbos`, `picows`, `msgspec`, `uvloop`.
- Latency SLOs in [07 §3](../07-security-and-production-readiness.md#3-proposed-service-level-objectives) are tightened for evidence events once Q-01 has measured them.
- Delayed prices still limit how fast we can react to price moves. Evidence events (filings, news, halts) get the quick response.

## Alternatives rejected
- **A Rust or JVM rewrite now:** no measured bottleneck justifies it, and it slows a small team.
- **Deephaven or Flink as the core:** operational weight is unjustified at 1–5k symbols of minute bars. Deephaven stays under "Assess" for tier B.
- **An LLM or Jev as the primary decision maker:** not deterministic, cannot be replayed, and weak on numbers.

## Revisit when
- Q-01 shows compute is more than 20% of p95.
- Full-market tick ingestion exceeds about 10k msg/s.
- Automated execution or a paid sub-100 ms use case is approved.
