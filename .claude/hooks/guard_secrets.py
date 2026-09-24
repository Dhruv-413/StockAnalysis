#!/usr/bin/env python3
"""PreToolUse guard: keep API keys out of Claude's context and out of the repo.

Blocks (exit 2, reason on stderr):
  * Bash commands that read or copy real env files (.env, .env.local, ...).
    `.env.example` / `.env.sample` / `.env.template` are allowed.
  * Write/Edit/MultiEdit whose new content contains a credential-shaped string.

This repository has already leaked provider keys through a committed .env
(see docs/production-plan/01-repository-assessment.md, finding 1), hence the guard.
Stdlib only; reads the hook payload as JSON on stdin.
"""
import json
import re
import sys

ENV_FILE = re.compile(r"(?<![\w.-])\.env(?:\.(?!example\b|sample\b|template\b)[\w-]+)?(?![\w.-])")
SECRET_PATTERNS = [
    ("Google API key", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Anthropic API key", re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("OpenAI-style secret key", re.compile(r"\bsk-[A-Za-z0-9]{32,}")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    # KEY=<long literal> assignments for this project's provider variables
    ("provider key assignment", re.compile(
        r"(?i)\b(FINNHUB|ALPHA_VANTAGE|TWELVE_DATA|MARKETAUX|GOOGLE|POLYGON|MASSIVE|DATABENTO|ALPACA|TIINGO)"
        r"_(API_)?(KEY|SECRET|TOKEN)\s*[=:]\s*['\"]?(?!your_|<|\$\{|changeme|dummy|test|example)[A-Za-z0-9_\-]{16,}")),
]


def block(reason: str) -> None:
    sys.stderr.write(f"Blocked by .claude/hooks/guard_secrets.py: {reason}\n")
    sys.exit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # not our business; never break the session on malformed input

    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}

    if tool == "Bash":
        command = tool_input.get("command", "")
        if ENV_FILE.search(command):
            block("command references a real .env file. Secrets must stay out of the "
                  "session; use .env.example for variable names, or ask the user.")

    if tool in ("Write", "Edit", "MultiEdit"):
        path = str(tool_input.get("file_path", ""))
        if ENV_FILE.search(path.replace("\\", "/").split("/")[-1]):
            block(f"writing to a real env file ({path}) is not allowed; edit .env.example instead.")
        texts = [tool_input.get("content", ""), tool_input.get("new_string", "")]
        texts += [e.get("new_string", "") for e in tool_input.get("edits", []) or []]
        blob = "\n".join(t for t in texts if isinstance(t, str))
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(blob):
                block(f"new content contains a {label}. Never write credentials to files; "
                      "reference an environment variable instead.")

    sys.exit(0)


if __name__ == "__main__":
    main()
