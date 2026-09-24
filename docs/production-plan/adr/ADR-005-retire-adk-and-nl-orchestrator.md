# ADR-005: Retire the Google ADK wrapper and free-text orchestrator from the product path

- **Status:** Proposed (2026-09-24)
- **Deciders:** repository owner

## Context
Two components route requests using free text:

- `adk_agents/` exposes the agent classes as LLM tools. It leaves the choice of tool to the model, hard-codes a retired model, and defines five sub-agents that are never used ([01 finding 22](../01-repository-assessment.md#44-medium--security-and-operations)).
- `MainOrchestrator` parses timeframes with keyword heuristics ([01 §3](../01-repository-assessment.md#3-end-to-end-workflow-trace-post-apiv1analyze)).

The target product receives structured requests from a UI: a watchlist, an instrument, and a window.

## Decision
- Stop extending `adk_agents/`, `adk_main.py`, and the free-text `/api/v1/analyze` flow.
- Keep them runnable until Stage 2 replaces them, then delete them in a single commit, recorded in the changelog.
- Remove `google-adk` from runtime dependencies at that point.
- A future "ask about this alert" research feature, if it is validated, would work over our own event archive with the same grounding rules as [ADR-004](ADR-004-llm-role-grounded-only.md).

## Consequences
- Removes the non-deterministic routing layer and a large dependency tree.
- Contributors should not port ADK patterns into new code.
