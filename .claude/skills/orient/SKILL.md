---
name: orient
description: Orient a new session in the StockAnalysis repo. Summarizes current code state versus the planned product, the current roadmap stage, and open blockers. Use at the start of a session or when asked "where are we / what is this repo".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status *)
  - Bash(git log *)
  - Bash(git diff *)
---

Produce a short orientation for this repository. Do not modify any files.

1. Read `CLAUDE.md` and `docs/production-plan/README.md`.
2. Run `git status --short` and `git log --oneline -10`. Note uncommitted work, but do not open `.env*` files.
3. From `docs/production-plan/08-implementation-roadmap.md`, find the first task (`T-xx`) whose acceptance criteria are not yet met in the code. Check the code rather than trusting the docs.
4. Read `docs/production-plan/11-evidence-and-open-questions.md` and list open questions that block that task.
5. Report in 10 lines or fewer:
   - what the code does today;
   - the current stage and next task;
   - blockers;
   - the verification commands that currently work, taken from `CLAUDE.md`.

   Label anything you inferred rather than verified.
