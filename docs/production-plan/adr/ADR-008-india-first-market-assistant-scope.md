# ADR-008: India-first, information-only market assistant with 300 ms card-first answers

- **Status:** Proposed (2026-09-24). **This needs the owner's decision.** If accepted, it amends [ADR-001](ADR-001-product-direction.md) and the US-only assumption in [02](../02-product-thesis.md).
- **Deciders:** repository owner
- **Evidence:** [14](../14-global-market-assistant.md) and the research appendices:
  - [india-market-data-and-sebi](../research/india-market-data-and-sebi.md)
  - [global-news-and-data](../research/global-news-and-data.md)
  - [assistant-300ms-and-jev](../research/assistant-300ms-and-jev.md)
  - [distribution-and-competitors-india](../research/distribution-and-competitors-india.md)
  - [accuracy-indicators-algos](../research/accuracy-indicators-algos.md)

## Context
The owner wants a daily assistant for users of Indian and global trading platforms: news, sentiment, indicators, algos, deals and history, with replies in about 300 ms, accurate and reliable. The research found five constraints:

1. **Data rights.** Broker APIs can't be redisplayed across users. NSE/BSE display needs a licence, with a tariff category still to be confirmed. News summaries need a licensed-content source.
2. **Regulation.** Recommendations, targets or signals need SEBI Research Analyst registration, even for a free product. Order placement falls under the retail algo framework.
3. **Latency.** 300 ms is achievable for precomputed cards served in Mumbai. It is not achievable for a full answer written by an LLM.
4. **Jev.** Its US-only hosting and English-first design keep it off the India live path.
5. **Competition.** Free, capable assistants already exist (Dhan Fuzz, Groww GR 1, Angel One ARQ, Perplexity).

## Decision (proposed)
1. **Scope: Option A.** An information-only evidence assistant for Indian listed companies, reusing the 02 engine. US stays as a second leg.
2. **Answering: card-first.** Precomputed, in-region answer cards meet p95 ≤ 120 ms server-side on a cache hit and ≤ 300 ms on a miss. They are followed by a streamed narrative grounded in the card and checked by a verifier.
3. **Data: licensed feeds only.** No scraping. 15-minute delayed data until the NSE real-time category and cost are confirmed.
4. **Jev: background tagging only.** It stays behind an interface ([ADR-007](ADR-007-jev-as-optional-triage-classifier.md) is amended accordingly).
5. **Distribution: an MCP server first**, then a web app with a digest, then a Telegram bot.
6. **No signals, targets or order placement** unless the owner later chooses SEBI registration, which would be recorded in a new ADR.

## Consequences
- Adds India data and legal workstreams (tasks I-01 to I-08 in [14 §8](../14-global-market-assistant.md#8-plan-changes)).
- Pricing assumptions move to ₹ and are validated by interviews.
- The product stays legal and defensible: every number is cited and timestamped. The feature list, however, is narrower than "everything".

## Alternatives
- **B, registered advice:** larger feature set but heavy compliance.
- **C, global everything:** licensing multiplies and cost is prohibitive at this stage.
- **D, keep US-only:** does not match the owner's intent.

## Revisit when
- Counsel's advice or NSE's answers change the cost or legal picture.
- Interviews fail the thresholds.
- TypeSafe offers an India region or an SLA.
