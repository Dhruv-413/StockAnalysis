---
paths:
  - "src/adapters/**"
  - "src/agents/**"
  - "marketdata/**"
  - "ingestor/**"
  - "calendar/**"
  - "evidence/**"
  - "domain/**"
  - "migrations/**"
---

# Market-data code rules

The owner is `data-engineer`; the reviewer is `financial-correctness-reviewer`.

- Every price, bar or event carries `source`, an `entitlement` value (`real-time | indicative | delayed-15 | eod`) and timezone-aware UTC `event_ts` and `ingest_ts`. Naive datetimes, `datetime.now()` without tz, and `utcnow()` are not allowed.
- Never fabricate, estimate, interpolate or zero-fill prices. Missing data stays missing. A fallback source must change the entitlement label and be logged.
- Keep raw prints unadjusted. Adjusted series come from the versioned corporate-action table.
- Sessions, half-days and DST come from `exchange_calendars` XNYS plus `session_overrides`. Key bars by trading-session date.
- Errors are typed exceptions. Do not return `None` or `[]` to mean "failed". Never cache failures.
- Dev-tier vendor adapters are `internal_only`. yfinance must never be imported in product code.
- Tests use recorded fixtures. No live vendor calls.
