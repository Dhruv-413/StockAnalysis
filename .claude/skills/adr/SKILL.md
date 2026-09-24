---
name: adr
description: Draft an Architecture Decision Record in docs/production-plan/adr/ using the repo's format (Status/Context/Decision/Consequences/Alternatives) with evidence links. Use when a durable technical, vendor, licensing, or product decision is being made or changed.
argument-hint: "<decision title>"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
---

Draft an ADR for: $ARGUMENTS

1. List `docs/production-plan/adr/` and take the next number, `ADR-NNN`. Read any related ADRs. If this decision supersedes one, say so in both files.
2. Create `docs/production-plan/adr/ADR-NNN-<kebab-title>.md` with these sections:
   - **Status:** `Proposed (<today's date>)`. Only the user moves it to `Accepted`.
   - **Deciders**
   - **Context:** the facts, with links to research appendices and to findings in `01`.
   - **Decision**
   - **Consequences:** cost, risk, and what becomes easier or harder.
   - **Alternatives rejected:** each with the reason.
   - **Revisit when:** the measurable triggers that would reopen the decision.
3. Add the ADR to the ADR row of `docs/production-plan/README.md`, and link it from the doc it affects.
4. Label every claim as verified, estimate or assumption. Never include secrets or local paths.
