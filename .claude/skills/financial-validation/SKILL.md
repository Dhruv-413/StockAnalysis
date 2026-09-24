---
name: financial-validation
description: Validate financial calculations and market-data pipeline changes (returns, abnormal returns, z-scores, relative volume, corporate-action adjustments, calendars/timestamps, entitlement labels) against the invariants in docs/production-plan/06-quantitative-validation.md. Use when calculation, ingestion, or data-model code changes.
argument-hint: "[path or module to focus on]"
---

Validate the financial and market-data correctness of: $ARGUMENTS. If no argument is given, validate the current `git diff`.

Delegate the review to the `financial-correctness-reviewer` subagent (`.claude/agents/financial-correctness-reviewer.md`) with the Agent tool. Pass it the scope and the checklist below. Then relay its findings together with your own verdict. If the subagent is unavailable, run the checklist yourself, read-only.

Use `docs/production-plan/06-quantitative-validation.md` §1–4 and the invariants in `CLAUDE.md` as the specification.

For each changed calculation or data path:

1. State the formula as implemented, then compare it to the spec. Check:
   - windows: estimation window ends before the event window;
   - annualization and intraday scaling;
   - benchmark;
   - adjusted vs. unadjusted inputs;
   - price return vs. total return.
2. Check timestamp handling:
   - all timestamps are tz-aware UTC;
   - XNYS calendar is used for sessions, half-days and DST;
   - `event_ts`, `ingest_ts` and `display_ts` are kept distinct;
   - point-in-time availability (EDGAR acceptance time, first-publication time).
3. Check data integrity:
   - no fabrication, zero-fill or interpolation of prices;
   - fallback sources change the entitlement label;
   - idempotent upserts on natural keys;
   - quarantine of invalid bars.
4. Check test coverage against the required fixture days: split, ex-dividend, half-day, halt, DST Monday, IPO with short history. Also check the property tests (symmetry, zero abnormal return when the stock equals the benchmark with β=1, idempotent adjustment). List the missing ones.
5. If feasible, compute one fixture case by hand in a short Python snippet and compare it with the code's output. Use local fixtures only; never call a live API.

Report each finding with `path:line`, severity, and the concrete input that produces a wrong number. End with a verdict and the tests that must be added.
