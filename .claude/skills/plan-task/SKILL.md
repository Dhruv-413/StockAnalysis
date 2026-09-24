---
name: plan-task
description: Turn a roadmap task (T-xx) or feature request into a concrete implementation plan for this repo, grounded in the production plan docs, invariants, and verification rules. Use before implementing any non-trivial change.
argument-hint: "<T-xx or short description>"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status *)
  - Bash(git log *)
---

Plan the work for: $ARGUMENTS

1. Find the task in `docs/production-plan/08-implementation-roadmap.md`. If it is not there, say which stage it belongs to. Also say whether it is in the MVP scope defined in `02-product-thesis.md` §4–5. Stop and ask the user if the request is an explicit MVP exclusion.
2. Read the design sections that govern it:
   - architecture: `05-target-architecture.md`;
   - data and real-time semantics: `04-real-time-data-strategy.md`;
   - calculations and evaluations: `06-quantitative-validation.md`;
   - gates: `07-security-and-production-readiness.md`.
3. Inspect the code it touches and cite `path:line`. Check the ADRs in `docs/production-plan/adr/` for decisions you must respect.
4. Write the plan:
   - goal and acceptance criteria, copied or refined from the roadmap;
   - files to add or change;
   - data model and migration impact;
   - the invariants from `CLAUDE.md` it touches and how each is preserved;
   - tests to write first (fixtures only, no live APIs);
   - verification commands;
   - docs to update;
   - risks and open questions.
5. Flag anything that needs user approval: new paid vendors, external calls, schema changes that drop data, or new dependencies with non-permissive licences (AGPL, Commons Clause).

Do not write code in this skill.
