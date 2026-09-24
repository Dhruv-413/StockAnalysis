---
paths:
  - "tests/**"
  - "**/test_*.py"
  - "**/*_test.py"
---

# Test rules

The owner is `qa-engineer`.

- Tests never call live market-data or LLM APIs. Use recorded fixtures, stubs and fake models.
- Use dummy env values set by the test harness. Never read `.env`.
- Each financial test states its expected value and how it was derived (hand calculation or spreadsheet).
- A characterisation test for a known defect uses `xfail(strict=True)` with a reference to the finding ID in `01-repository-assessment.md`.
- Exit code 5 ("no tests ran") is not a pass.
