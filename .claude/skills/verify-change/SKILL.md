---
name: verify-change
description: Run focused verification and a review pass on the current uncommitted change in StockAnalysis, choosing checks by change type (adapter, calculation, LLM, API/auth, migration, docs). Use before declaring a change done or before committing.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status *)
  - Bash(git diff *)
  - Bash(git log *)
  - Bash(python -m pytest *)
  - Bash(python -m pytest)
  - Bash(python -m compileall *)
---

Verify the current change. Report evidence, not assurances.

1. Run `git status --short` and `git diff --stat`, then read the full diff. Classify each changed file using the "Verification by change type" table in `CLAUDE.md`.
2. Run the checks that apply. Always run `python -m compileall -q src adk_agents main.py adk_main.py` and `python -m pytest -q`.
   - Exit code 5, "no tests ran", means the change is **unverified**. It is not a pass.
   - If a `pyproject.toml` defines ruff or mypy (task T-02), run exactly those commands.
3. Review the diff for the following. Cite `path:line` for each finding.
   - **Invariant violations:** naive datetimes; missing `source` or entitlement fields; fabricated, zero-filled or interpolated prices; silent provider fallback; LLM-generated numbers.
   - **Error handling:** errors swallowed into `None` or `[]`; exception text returned to clients.
   - **Tests:** live network calls in tests.
   - **Secrets:** secrets or `.env` access.
   - **Licensing:** dev-only or unlicensed data sources (yfinance) used in product paths.
4. If calculation code changed, recommend running `/financial-validation`.
5. Check whether docs need updating: `docs/production-plan/*` and `CLAUDE.md` commands and invariants. List the stale statements.
6. Output three things:
   - the checks you ran, with the exact commands and results;
   - findings, most severe first;
   - an explicit verdict: `verified`, `partially verified (why)` or `not verified (why)`.
