---
name: standup
description: Team standup for StockAnalysis - summarise recent changes, progress against the roadmap tasks (T-xx) and stop/go gates, blockers and open questions, and propose today's assignments per role. Use at the start of a work session or when asked for status.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status *)
  - Bash(git log *)
  - Bash(git diff *)
---

Produce a standup. This skill is read-only.

1. Run `git log --since="7 days ago" --oneline` and `git status --short`, then group the changes by squad using the ownership table in `docs/production-plan/12-team-operating-model.md` §2.
2. Using `08-implementation-roadmap.md`, find which `T-xx` tasks are done, in progress or next. Check the code for evidence rather than trusting the docs. Report the status of each stop/go gate: G-DEMAND, G-LATENCY, G-DATA, G-CALIBRATION, G-EVAL and G-PILOT.
3. List blockers from `11-evidence-and-open-questions.md` §2 that gate the next task. Separate the items the user must act on (vendors, counsel, key rotation) from engineering items.
4. Propose today's plan: 1–3 tasks per role at most, only for the roles actually needed.
5. Scan agent memory (`.claude/agent-memory-local/*/`, or `.claude/agent-memory/*/` if a team opted into shared memory) and recent notes in `docs/production-plan/handoffs/` for decisions or risks worth surfacing.

Output 20 lines or fewer.
