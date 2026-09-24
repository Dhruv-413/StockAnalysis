# ADR-004: The LLM only selects and phrases retrieved evidence

- **Status:** Proposed (2026-09-24)
- **Deciders:** repository owner

## Context
The prototype asks Gemini to explain price moves without passing it the news it fetched. It also passes an LLM-invented "confidence" through as a number ([01 §3](../01-repository-assessment.md#3-end-to-end-workflow-trace-post-apiv1analyze)). The research points the same way:

- LLMs are good at extracting and labelling text, but weak at forecasting (FinBen).
- They hallucinate more about large, recent companies (Shah et al., COLM 2025).
- Look-ahead bias and distraction effects are real (Glasserman & Lin 2023; Sarkar & Vafa 2024).
- Intraday moves usually have no identifiable news (Boudoukh et al., RFS 2019).

Sources: [research/papers.md](../research/papers.md).

## Decision
- Numbers come only from deterministic code.
- Retrieval is deterministic and time-bounded.
- The LLM:
  - receives only the evidence set, as untrusted delimited data;
  - must cite evidence IDs;
  - must abstain when the evidence is insufficient;
  - returns schema-validated JSON.
- Runtime hard gates check:
  - that each citation exists;
  - that numbers match the deterministic outputs;
  - that evidence timestamps precede the move;
  - that there is no advice language.

  Any failure falls back to the deterministic ledger only.
- The model ID is pinned, prompts are versioned, and any change reruns the offline evaluation ([06 §5](../06-quantitative-validation.md#5-llm-explanations-evaluation)).
- No free-text chat and no tool-using agent in the MVP.
- Migrate from the deprecated `google-generativeai` SDK and the retired `gemini-1.5-flash` model to `google-genai` with a current model, on a paid tier. Keep a provider-agnostic interface so a second provider can be compared.

## Consequences
- More "no catalyst found" outputs, which is honest, and hypothesis H3 tests how users receive them.
- An evaluation harness and a gold set of about 800 cases are required before summaries are shown in the pilot.
- LLM cost is small: roughly $810–3,600 per month at 5,000 users ([09](../09-costs-and-operating-model.md)).
