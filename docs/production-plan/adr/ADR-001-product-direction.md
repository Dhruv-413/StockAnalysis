# ADR-001: Primary product direction — explainable watchlist monitoring

- **Status:** Proposed (2026-09-24). It becomes Accepted once the Stage 0 validation gates in [08](../08-implementation-roadmap.md#stopgo-gates) pass.
- **Deciders:** repository owner

## Context
The prototype answers "why did stock X move?" for one ticker at a time. It is ungrounded (news never reaches the prompt), and it uses data sources that are not licensed for display ([01](../01-repository-assessment.md)). Five directions were compared in [02 §3](../02-product-thesis.md#3-directions-compared):

- research and screening;
- monitoring and alerts;
- portfolio and risk;
- backtesting;
- trading.

## Decision
Build a monitoring service for US equities and ETFs. It sends abnormal-move alerts, each with a timestamped evidence ledger and an optional grounded summary with explicit abstention. It targets independent equity researchers: newsletter writers, independent analysts, and small advisory shops.

## Consequences
- The existing question and adapter pattern are reused. Trading, backtesting, bonds, and chat are excluded from the MVP.
- Value rests on auditability and workflow, not speed. That makes delayed data viable ([ADR-002](ADR-002-delayed-first-market-data.md)).
- Main risks:
  - Brokers or Perplexity add evidence ledgers and export.
  - The audience turns out to want speed rather than evidence.
  - Both are tested in Stage 0 through interviews and a paid concierge pilot.
- Regulatory posture relies on the publisher's exclusion, which needs a counsel memo before launch.

## Alternatives rejected
- **All-in-one AI trading platform.** Licensing, regulatory, and correctness burden is multiplied, and incumbents give it away free.
- **Research and screening, or backtesting, as the primary direction.** Crowded, and free open-source tools dominate.
- **Paper trading and broker integration.** Needs a broker partnership and possible registration.
