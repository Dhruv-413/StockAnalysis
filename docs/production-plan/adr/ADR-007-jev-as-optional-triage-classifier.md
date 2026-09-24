# ADR-007: Evaluate TypeSafe AI "Jev" as an optional L2 text-triage classifier

- **Status:** Proposed (2026-09-24). Evaluation only; not approved for production.
- **Deciders:** repository owner
- **Evidence:** [TypeSafe blog](https://typesafe.ai/blog/introducing-system-one-models-and-jev) (fetched 2026-09-24); [reactive-and-jev](../research/reactive-and-jev.md); [decision-engines](../research/decision-engines.md); [13 §4](../13-quick-response-system.md#4-jev-and-similar-tools)

## Context
The owner asked for "JEV from Typesafe" as a fast decision tool. It is **Jev**, from **TypeSafe AI** (early access since 2026-09-15). It is not a product of Typesafe Inc., which became Lightbend and then Akka.

Vendor claims:
- Jev returns typed answers (boolean, choice, score) with calibrated probabilities.
- Latency is 70–500 ms.
- Input costs $0.042 per million tokens; output is free.

Limitations:
- No arithmetic, dates or free text.
- About 68% accuracy on the vendor's own evaluations, which were scored against LLM-generated labels.
- A closed, hosted model with a waitlist.
- The terms and acceptable-use policy were not reviewed (the AUP page returned 404).

## Decision
- Jev is a **candidate for layer L2 only**: triage of filings and headlines (materiality, catalyst type, issuer relevance, routing).
- Its outputs may add tags or change priority. They never compute or override numbers, and never alone trigger a consequential action.
- It runs behind a provider-agnostic `TextTriage` interface with a timeout. On timeout, the system continues with rules only.
- Its probabilities are used internally for thresholds. They are **never shown to users as "confidence"** ([ADR-004](ADR-004-llm-role-grounded-only.md)).

## Adoption criteria (task Q-05 bake-off, n ≥ 500 labelled items)
- Beats or equals the best alternative on macro-F1: Claude Haiku 4.5 or Gemini Flash-Lite with structured output, or a local classifier.
- Calibration: its Brier score is at least as good as the alternative's, and its reliability curve does not systematically overstate probabilities.
- Latency: p95 ≤ 800 ms from our US-East host.
- Cost: acceptable at the projected volume.
- **Terms reviewed by `compliance-analyst`** and accepted by the owner. The review covers financial use, data retention and training on inputs, and passing licensed news text to a subprocessor.
- Rate limits and SLA are adequate, and a fallback path has been tested.

## Amendment (2026-09-24, from the [assistant-300ms-and-jev](../research/assistant-300ms-and-jev.md) research)

Primary-source facts that narrow this decision:
- **Hosting and latency.** US-West only. The estimate from India is about 320–340 ms p50.
- **Service terms.** No streaming. No SLA. Liability is capped at the greater of 12 months' fees or $50.
- **Data handling.** Zero data retention is enterprise-only. **Distillation is forbidden**, so Jev's outputs cannot train our own router.
- **Limits.** Context is 64k tokens, of which 32k can be state. The rate limit is 1,200 requests/min.
- **Language and calibration.** English-first. Calibration ECE is about 0.107 (independent test), so re-calibrate on our own labels.

Decision: use Jev **only for background tagging** (news and filings). Keep it off every live answer path serving Indian users ([ADR-008](ADR-008-india-first-market-assistant-scope.md)).

## Consequences
- Low integration cost thanks to the interface.
- Vendor and early-access risk is contained: if Jev fails, fall back to the alternative.
