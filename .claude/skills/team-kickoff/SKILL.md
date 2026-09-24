---
name: team-kickoff
description: Run a request through the StockAnalysis team - the tech lead triages it, picks the right members (research, product, platform, application, quality, governance), runs independent work in parallel, integrates handoffs, and verifies. Use for any multi-step feature, investigation or decision that spans more than one role.
argument-hint: "<request>"
---

Run this request as the team: $ARGUMENTS

The operating model is in `docs/production-plan/12-team-operating-model.md`. Roles are defined in `.claude/agents/`.

1. **Triage (you act as the tech lead).**
   - Map the request to the roadmap (`08-implementation-roadmap.md`, task `T-xx`) and to MVP scope (`02` §4–5).
   - If it hits an MVP exclusion or contradicts an ADR, stop and ask the user.
2. **Staff it.** Choose the fewest roles, usually 2–4, using the RACI table in `12` §3. Write a one-line brief per role with:
   - the goal;
   - the files or paths in scope;
   - the constraints;
   - the expected output.
3. **Phase the work.** Use the Agent tool with the role's agent type.
   - **Discover:** research roles run in parallel, each on a separate front.
   - **Decide:** summarise the options. If the decision is durable, draft an ADR with `/adr`, then ask the user when it involves cost, a vendor, a licence or a language choice.
   - **Build:** implementation roles work in parallel only on disjoint paths. Their agents run with `isolation: worktree`.
   - **Verify:** `qa-engineer` adds or runs tests. `financial-correctness-reviewer` reviews calculation and data changes. `security-engineer` reviews auth, secrets and input handling. Finish with `/verify-change`.
4. **Integrate.**
   - Collect each handoff in the format from `12` §5.
   - Resolve conflicts between handoffs.
   - List what was verified and what was not.
5. **Report.** Give the user:
   - the outcome;
   - the files changed;
   - evidence (commands and results);
   - open questions;
   - the next task.

Never push, deploy, spend money or contact vendors. Those actions are the user's.

**Optional:** if agent teams are enabled (see `12` §6), you may instead spawn 3–5 teammates using these agent types, with a shared task list.
