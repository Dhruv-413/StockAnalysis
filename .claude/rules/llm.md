---
paths:
  - "src/adapters/gemini_adapter.py"
  - "summarizer/**"
  - "evals/**"
  - "prompts/**"
---

# LLM code rules

The owner is `ml-llm-engineer`. The governing decision is ADR-004.

- The LLM may only select and phrase retrieved evidence, with evidence-ID citations. It must abstain when the evidence is insufficient.
- The LLM must never produce numbers, forecasts, confidence scores, sentiment scores or advice.
- Retrieved text is untrusted. Put it in delimited sections. Never give the LLM tools or secrets.
- Output must follow the JSON schema and pass the hard gates: citations exist, numbers match, evidence timestamps are no later than the move start plus grace, and there is no advice language.
- Pin the model ID and version the prompts. Any change reruns the offline eval (`06` §5).
- Use the paid tier only. `google-generativeai` and `gemini-1.5-*` are retired; use `google-genai`.
