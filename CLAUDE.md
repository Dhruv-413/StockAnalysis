# StockAnalysis — contributor guide for Claude Code

## What this repo is (read first)
- **Today:** a prototype FastAPI + Gemini "why did stock X move?" Q&A API (`main.py`, `src/`), plus a Google ADK wrapper (`adk_main.py`, `adk_agents/`). No DB, no tests, no CI, no frontend. The README overstates it ("real-time", "production-ready"). The verified state is in `docs/production-plan/01-repository-assessment.md`.
- **Planned:** a watchlist monitoring service for US equities/ETFs. It sends explainable abnormal-move alerts with a timestamped evidence ledger. The **redesign is planned, not implemented.** Start at `docs/production-plan/README.md`. Work is sequenced in `08-implementation-roadmap.md` (task IDs `T-xx`).

## Setup and commands (verified 2026-09-24 on Windows, Python 3.12)
- `py -3.12 -m venv .venv` then `.venv\Scripts\python -m pip install -r requirements.txt`
  - Requirements are unpinned.
  - If a Windows MAX_PATH error appears, use a short venv path.
  - Python 3.14 (the machine default) is untested.
- The app **crashes at import unless all five keys are set**: `GOOGLE_API_KEY`, `FINNHUB_API_KEY`, `ALPHA_VANTAGE_API_KEY`, `TWELVE_DATA_API_KEY`, `MARKETAUX_API_KEY`. Dummy values are fine for offline work.
- Run: `python main.py` → http://localhost:8001 (`/docs`, `/api/v1/health`).
- Tests: `python -m pytest -q`. There are **no tests yet** (exit code 5). Adding the first tests is task T-03.
- Sanity: `python -m compileall -q src adk_agents main.py adk_main.py`.
- No lint or typecheck config exists yet. Once T-02 lands, use the ruff/mypy commands it adds to `pyproject.toml`. Do not invent flags.

## Hard rules
- **Secrets:**
  - Never read, print, copy or write `.env*` files (except `.env.example`), and never write key literals anywhere.
  - `.claude/hooks/guard_secrets.py` enforces this.
  - Keys were already leaked in public git history (assessment finding 1).
- **No external side effects without explicit user approval:** no `git push`, deploys, paid-API sign-ups, or live provider/LLM calls in tests.
- **Tests use stubs and fixtures, never live market-data or LLM APIs.**
- Never execute trades or add order-placing code. Execution is out of scope ([05 §9](docs/production-plan/05-target-architecture.md)).

## Financial and market-data invariants (details: docs/production-plan/06-quantitative-validation.md)
1. Every price or bar carries `source`, entitlement (`real-time | indicative | delayed-15 | eod`), and UTC tz-aware `event_ts` and `ingest_ts`. No naive datetimes.
2. **Never fabricate or silently substitute data.** Missing data is shown as missing. A fallback source must change the label. Delayed data is never shown as live. (`finnhub_adapter.py:340-366` fabricates data: delete it, never reuse it.)
3. Keep raw unadjusted prints. Derive adjusted series from a versioned corporate-action table, and say whether a figure is price return or total return.
4. Use `exchange_calendars` (XNYS) for sessions, holidays, half-days and DST. No weekday arithmetic.
5. Numbers shown to users come from deterministic code. LLMs only select and phrase retrieved evidence, cite evidence IDs, and must abstain when evidence is missing. No LLM "confidence", sentiment scores or forecasts.
6. Point-in-time: filings use EDGAR acceptance time; news uses first-publication time. Evidence published after a move began must be labelled that way.
7. Respect data licences: dev-tier vendor data is internal-only. yfinance is never used in product code paths ([04 §6](docs/production-plan/04-real-time-data-strategy.md)).

## Verification by change type
| Change | Minimum verification |
|---|---|
| Adapter / ingestion | Unit tests with recorded fixtures; timezone and entitlement fields asserted; error paths return typed errors, not `None`/`[]` |
| Calculations (returns, AR, z, RVOL, adjustments) | Golden-fixture and property tests; run `/financial-validation` |
| LLM prompt or model | Offline eval harness against the gold set ([06 §5](docs/production-plan/06-quantitative-validation.md)); pin the model id |
| API / auth | Endpoint tests including tenant-isolation cases; generic error bodies |
| Schema / migration | Expand/contract migration; test on a restored snapshot |
| Docs-only | Links resolve; claims match code |

## Team (see docs/production-plan/12-team-operating-model.md)
You act as the **tech-lead** unless the user says otherwise. Delegate to role subagents in `.claude/agents/`:

| Squad | Roles |
|---|---|
| Product | `product-manager` |
| Research | `tech-scout`, `market-data-researcher`, `quant-researcher` |
| Platform | `data-engineer`, `realtime-engineer` |
| Application | `backend-engineer`, `frontend-engineer`, `ml-llm-engineer` |
| Quality & Ops | `qa-engineer`, `sre-engineer`, `security-engineer` |
| Governance | `compliance-analyst`, `financial-correctness-reviewer` |

- Use the fewest roles that cover the work.
- Research runs in parallel; each builder works on its own paths.
- Calculation or data changes always go to `financial-correctness-reviewer`.
- Auth, secrets or input changes go to `security-engineer`.
- Money, vendor, licence and language decisions are the user's to accept, recorded as an ADR.

Path-scoped rules in `.claude/rules/` load automatically for their areas.

## Where things are
- Plan and ADRs: `docs/production-plan/` (index `README.md`; ADRs in `adr/`; raw research evidence in `research/`).
- Quick-response (fast fetch → decide → notify) design: `docs/production-plan/13-quick-response-system.md`.
- Skills:
  - team: `/team-kickoff`, `/research-sprint`, `/standup`, `/handoff`, `/adr`
  - engineering: `/orient`, `/plan-task`, `/verify-change`, `/financial-validation`, `/readiness-review`
- Saved workflow: `research-sprint` (multi-front research with adversarial verification; costly, use it for broad sweeps).
- Claude Code setup rationale: `docs/production-plan/10-claude-code-setup.md`.
