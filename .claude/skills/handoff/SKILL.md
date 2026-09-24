---
name: handoff
description: Write a structured handoff note from one role to the next (or for the next session) - what was done, evidence, decisions, open risks, and exact next steps. Use when finishing a chunk of work, switching roles, or before ending a session.
argument-hint: "[to-role]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash(git status *)
  - Bash(git diff *)
  - Bash(git log *)
---

Write a handoff note addressed to: $ARGUMENTS. If no role is given, address it to the next session.

Use the format from `docs/production-plan/12-team-operating-model.md` §5:

```
## Handoff — <date> — <from role> → <to role>
Task: T-xx / <short name>
Done: <bullets, with file paths>
Evidence: <commands run + results; tests added>
Not verified: <explicit list>
Decisions: <links to ADRs or reasoning>
Risks / open questions: <bullets>
Next steps: <numbered, concrete, each with the owning role>
```

Save the note to `docs/production-plan/handoffs/<YYYY-MM-DD>-<kebab-task>.md` (create the directory if it doesn't exist). Also append a two-line summary to the receiving role's agent memory, under `.claude/agent-memory-local/<role>/` (or `.claude/agent-memory/<role>/` if shared memory is enabled), if that directory exists. The repo is public: handoff docs must not contain vendor pricing negotiations, personal data or local paths.

Never include secrets or `.env` contents.
