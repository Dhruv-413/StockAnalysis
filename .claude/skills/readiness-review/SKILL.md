---
name: readiness-review
description: Assess StockAnalysis against the production-readiness release gates (G1–G10) and failure-scenario drills in docs/production-plan/07-security-and-production-readiness.md, using evidence from the repo. Use before a pilot or release decision, or when asked "is this production-ready?".
disable-model-invocation: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status *)
  - Bash(git log *)
  - Bash(python -m pytest *)
  - Bash(python -m pytest)
---

Run a production-readiness review. Default to "not ready" unless evidence exists.

1. Read the release gates table (§4), the SLOs (§3) and the failure scenarios (§5) in `docs/production-plan/07-security-and-production-readiness.md`.
2. For each gate G1–G10, search the repo for the required evidence: test suites, CI workflow files, eval reports, runbooks, load-test reports, signed-licence records referenced in docs, and ADRs. Run `python -m pytest -q` to see the current test state.
3. Mark each gate `met` (link the evidence), `partial` (say what is missing) or `not met`. A green build or passing unit tests alone never satisfies G2–G10.
4. For each failure scenario in §5, check that a runbook and a drill record exist.
5. Also check the immediate security actions in §1 (S0.1–S0.4). Key rotation can only be confirmed by the owner, so list it as "owner confirmation required".
6. Output:
   - a gate table;
   - the top 5 blockers, in order;
   - the stop/go status from `08-implementation-roadmap.md`.

   Do not edit files unless the user asks you to record the review.
