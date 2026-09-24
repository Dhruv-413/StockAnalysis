# ADR-009: Finance-specialised model layer — deterministic engines first, foundation models as gated challengers

- **Status:** Proposed (2026-09-24). **This needs the owner's decision.**
- **Deciders:** repository owner
- **Evidence:**
  - [15](../15-finance-model-layer.md)
  - [finance-models-catalogue](../research/finance-models-catalogue.md)
  - [finance-models-evidence](../research/finance-models-evidence.md)

## Context
The owner prefers finance-specialised components, such as Kronos, over general AI models. They are open to a layered design, or a simple one for speed.

The research found:
- **Kronos:** code and small weights are MIT, and its training data includes NSE and BSE. Its headline gains come from a closed model, and three independent post-cutoff checks are negative, including one on NSE.
- **Independent studies:** time-series foundation models don't reliably predict returns. For volatility, Log-HAR is the bar to beat. An equal-weight TTM + Log-HAR combination is robust.
- **Finance LLMs:** self-benchmarked, Chinese-centric, or non-commercial.
- **India:** no credible India-specific model exists.

## Decision (proposed)
1. **Layers.**
   - **L0:** deterministic finance engines (TA-Lib, HAR/EWMA/GARCH, detectors, calendars). They are the only source of numbers on cards.
   - **L1:** internal tagging (a FinBERT-class encoder, optionally Jev).
   - **L2:** batch challengers (TTM, Kronos, FinCast), combined with Log-HAR and scored against it.
   - **L3:** offline research (pyqlib, RD-Agent).
2. **Pilot runs Option S** (L0, plus rules-based tagging). The L1 and L2 layers are added only after their gates pass.
3. **Kronos is placed in Assess**, as a volatility or regime challenger only. It is evaluated only on data from 2024-07 onward.
4. **No generative model on the 300 ms path.** No forecasts, targets, probabilities or sentiment scores are shown to users.
5. **A licence register tracks code, weights and training data** separately. Non-commercial and AGPL items stay in Hold.

## Consequences
- Fast, reproducible, licence-clean answers. The "AI forecasting" feature is not offered.
- A model becomes a product feature only by winning a pre-registered comparison against a finance baseline.
- It adds tasks F-01 to F-06.

## Alternatives
- **Kronos as the headline forecast band:** rejected on evidence (miscalibrated on NSE), on invariant 5, and on SEBI RA/PaRRVA.
- **Finance LLM as the core answerer:** rejected. The evidence is weak and has licence problems; a general LLM plus retrieval, gated by benchmarks, is safer.
- **An ensemble of many models voting on direction:** rejected. No component has shown out-of-sample skill, so an ensemble of them doesn't either.

## Revisit when
- An independent India walk-forward, net of costs, shows a model beating HAR or LightGBM.
- Kronos-large is released.
- The owner chooses SEBI RA registration (ADR-008 option B).
