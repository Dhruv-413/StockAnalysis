# 10 — Claude Code Setup

← [Index](README.md) · Previous: [09 Costs](09-costs-and-operating-model.md) · Next: [11 Evidence & open questions](11-evidence-and-open-questions.md)

Date: 2026-09-24. Claude Code CLI version on this machine: 2.1.281. Syntax was checked against the official docs ([memory](https://code.claude.com/docs/en/memory.md), [settings](https://code.claude.com/docs/en/settings.md), [hooks guide](https://code.claude.com/docs/en/hooks-guide.md), [skills](https://code.claude.com/docs/en/skills.md), [sub-agents](https://code.claude.com/docs/en/sub-agents.md), [mcp](https://code.claude.com/docs/en/mcp.md)) and against the SchemaStore settings schema (`https://json.schemastore.org/claude-code-settings.json`, which redirects to `www.schemastore.org`).

## 1. What existed before

| Item | State |
|---|---|
| Project `CLAUDE.md`, `.claude/`, `.mcp.json`, `AGENTS.md` | None |
| `docs/` | Git-ignored (`.gitignore`, added in `7e71439` with no stated reason) |
| `.serena/` (untracked) | Serena MCP project config. **Left untouched.** |
| `.remember/` | Local tool state. **Left untouched.** |
| User-global `~/.claude/settings.json` | Read to avoid duplicating rules and hooks; not modified. It has no deny rules for env files. |
| User-global `~/.claude/CLAUDE.md` | Not modified. |

## 2. What was changed

| File | Purpose |
|---|---|
| `CLAUDE.md` (49 lines) | Product and state summary, **verified** commands, hard rules, financial and data invariants, verification per change type, and a docs map. Kept short; details live in these docs. |
| `.claude/settings.json` | Project permissions and the secrets-guard hook (see §3). |
| `.claude/hooks/guard_secrets.py` | A `PreToolUse` hook that blocks Bash commands referencing real `.env*` files and blocks Write/Edit/MultiEdit when the content contains credential-shaped strings or targets `.env*`. Uses only the Python standard library. |
| `.claude/skills/orient/SKILL.md` | `/orient`: repo orientation, current stage, blockers. Read-only. |
| `.claude/skills/plan-task/SKILL.md` | `/plan-task T-xx`: an implementation plan grounded in the roadmap, invariants and ADRs. Writes no code. |
| `.claude/skills/verify-change/SKILL.md` | `/verify-change`: checks chosen by change type, a diff review against the invariants, and an explicit verdict. |
| `.claude/skills/financial-validation/SKILL.md` | `/financial-validation`: delegates to the `financial-correctness-reviewer` subagent through the Agent tool, checking against [06](06-quantitative-validation.md). The docs don't clearly say whether `context: fork` + `agent:` can point to a *custom* subagent, so the skill uses explicit delegation instead. |
| `.claude/skills/readiness-review/SKILL.md` | `/readiness-review`: assesses gates G1–G10 and the drills in [07](07-security-and-production-readiness.md). `disable-model-invocation: true`, so it runs only when a person invokes it. |
| `.claude/agents/financial-correctness-reviewer.md` | A read-only quant reviewer subagent. |
| `.gitignore` | `docs/` became `docs/*` plus `!docs/production-plan/`, so these docs are tracked and any other `docs/` content stays ignored. Added `.claude/settings.local.json` and `CLAUDE.local.md`. Line endings kept as CRLF. |

### Rationale for the choices

- **Deny rules rather than hooks where possible.**
  - `Read(**/.env*)` and `Edit(**/.env*)` are denied for the exact filenames in `.gitignore`.
  - `.env.example` is deliberately **not** denied, so contributors can read variable names.
  - Force-push is denied. Ordinary push, PR creation and merge, releases and `git filter-repo` are set to **ask**.
- **One hook only.** The docs note that Read/Edit deny rules do not cover Bash subprocesses (for example `cat .env`), so a small hook closes that gap. It also stops key literals from being written into any file. That risk is real here: keys already leaked through a commit ([01 finding 1](01-repository-assessment.md#41-critical)).
- **Allow list kept minimal.** Broad allow rules add little for this workflow. Only the verified read-only test and git commands are listed.
- **No MCP servers added.** None is needed for the current work, and each adds credentials and attack surface (see §5).
- **No `.claude/commands/`.** Skills are the current mechanism.

## 3. Validation performed

| Check | Result |
|---|---|
| `.claude/settings.json` validated against the SchemaStore schema (draft-07) with `jsonschema` | **Valid** |
| YAML frontmatter of the 5 skills and 1 agent parsed with PyYAML; `name` matches the directory or file | **OK**. `allowed-tools` is written as a YAML list, which the docs accept. That avoids any ambiguity with space-separated entries such as `Bash(git status *)`. |
| `argument-hint` field | **Not confirmed** in the skills frontmatter reference that was retrieved. It is harmless if ignored. |
| Hook unit tests: 18 synthetic payloads covering Bash `.env` reads, `.env.example`, `.venv` paths, `os.environ`, `python-dotenv`, Windows and POSIX `.env` writes, Google key, provider-key literal, placeholder values, PEM block, malformed stdin, other tools | **All matched expectations** after one test-harness quoting fix. Malformed input is allowed through on purpose (fail-open) so a broken payload never locks the session. |
| **Live integration in this session:** a Bash command containing `.env` | **Blocked by the hook**, which ran through Git Bash with `python3` and `$CLAUDE_PROJECT_DIR` |
| **Live:** `Read` of `./.env` | **Denied by the permission rules** |
| Skills appearing in the `/` menu | **Not verified.** Skills load when a session starts; confirm by running `/orient` in a new session. |

## 3b. Team setup (added 2026-09-24, second pass)

Roles, ownership, RACI and workflow are in [12](12-team-operating-model.md).

| Added | Details |
|---|---|
| 14 role subagents in `.claude/agents/` | tech-lead, product-manager, tech-scout, market-data-researcher, quant-researcher, data-engineer, realtime-engineer, backend-engineer, frontend-engineer, ml-llm-engineer, qa-engineer, sre-engineer, security-engineer, compliance-analyst. Plus the existing financial-correctness-reviewer, for 15 in total. Each has `memory: local` (ignored by git, because the repository is public) and a `color`. Builders use `isolation: worktree`. **Every agent has an explicit `tools` list**, so none inherits the session's MCP tools, some of which are destructive (database, email, commerce, computer use). Researchers and reviewers have restricted tool lists. security-engineer has no Write or Edit. compliance-analyst, market-data-researcher and tech-scout have Write (for reports) but no Edit. These are tool restrictions, not path sandboxes; their briefs limit them to docs. |
| Path-scoped rules in `.claude/rules/` | `market-data.md`, `realtime-decision.md`, `llm.md`, `tests.md` and `docs.md`, each with a `paths:` frontmatter field |
| Team skills | `/team-kickoff`, `/research-sprint`, `/adr`, `/standup`, `/handoff` |
| Saved workflow | `.claude/workflows/research-sprint.js`: one scout per front, two skeptics per critical claim, then synthesis. Invoke it by name with `args: {question, fronts?, constraints?}`. It spawns up to about 67 agents at the defaults, so use it for broad sweeps only. It is capped at 5 candidates per front and logs what it drops. Its prompts forbid installing or running packages. |
| `.gitignore` | `.claude/agent-memory-local/` is ignored. Shared `agent-memory/` would be tracked if a private team opts into `memory: project`. |
| Agent teams | **Not enabled in shared settings.** The feature is experimental and its cost scales with teammate count. Opt in personally with `.claude/settings.local.json` → `{"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}}`. On Windows it runs in-process only. A teammate receives a role's tools, model and body, but not its skills or memory ([docs](https://code.claude.com/docs/en/agent-teams.md)). |

**Validation performed on the team setup:**
- The YAML frontmatter of all agents, skills and rules parses.
- Agent `name` values match their file names.
- Rules have a `paths` list.
- The workflow script passes `node --check` once its body is wrapped the way the runtime runs it. A top-level `return` is valid in the workflow runtime.
- `settings.json` is unchanged and still validates against the schema.

**Not yet verified:** registration of the 14 new agents.
- A probe in this session (`Agent` with `subagent_type: tech-lead`) returned "agent type not found". Only `financial-correctness-reviewer`, created earlier, was registered.
- Expected cause: agent definitions load at session start.
- To check, start a new session and look in `/agents`, or run `/standup`.

Also unverified: whether saved workflows in `.claude/workflows/` are discovered by name.

## 4. Known limitations

- The hook calls `python3`. On Windows this resolves to the WindowsApps launcher (Python 3.14 here). If a contributor has no `python3` on PATH, the hook fails with a non-blocking error: the action is **not** blocked, and a hook error is shown. Fix by installing Python or by editing the command locally in `.claude/settings.local.json`.
- The hook's pattern matching is a best-effort safety net. It is not a secret scanner. Keep GitHub secret scanning and push protection (S0.3 in [07](07-security-and-production-readiness.md#1-immediate-security-actions-before-any-other-work)).
- Commands listed in `CLAUDE.md` reflect the repo **as it is now**, with no tests and no lint config. Tasks T-02 and T-03 must update `CLAUDE.md` when they add `pyproject.toml`, ruff/mypy and pytest suites. `/verify-change` checks for this drift.

## 5. Optional integrations (not configured; each needs a decision or credentials)

| Integration | Value | Why not added now |
|---|---|---|
| GitHub MCP / `gh` CLI | PR and issue workflows | Needs an owner token; `gh` already works via the CLI. |
| Postgres MCP (read-only role) | Schema-aware queries once the DB exists (Stage 1) | No database exists yet; needs a least-privilege role. |
| Sentry or observability MCP | Incident triage | No deployment yet. |
| Serena MCP (`.serena/` exists, untracked) | Symbol-level navigation | Already set up by the owner outside git. Whether to commit `.serena/project.yml` is the owner's call. |
| A PostToolUse formatter hook (ruff format) | Consistent formatting | Add after T-02 introduces ruff, so it is not run against an unconfigured tool. |
| A Stop hook that runs tests | Automatic verification | Would be noisy while the suite is empty. Reconsider once the suite runs in under 30 seconds. |
