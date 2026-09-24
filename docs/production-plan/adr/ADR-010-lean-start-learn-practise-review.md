# ADR-010: Lean start: "Learn → Practise → Review", with automation gated

- **Status:** Proposed (2026-09-24). **This needs the owner's decision.** If accepted, it:
  - supersedes the scope in [ADR-008](ADR-008-india-first-market-assistant-scope.md), option A;
  - amends [ADR-001](ADR-001-product-direction.md);
  - requires a reviewed change to CLAUDE.md's "never execute trades" rule. That change applies only when automation step 1 is approved, not before.
- **Deciders:** repository owner
- **Evidence:**
  - [18](../18-lean-start-broker-algo-plan.md)
  - [algo-legal-path](../research/algo-legal-path.md)
  - [broker-algo-apis](../research/broker-algo-apis.md)
  - [one-percent-and-algo-comps](../research/one-percent-and-algo-comps.md)
  - [fast-cheap-stack](../research/fast-cheap-stack.md)

## Context
The owner wants to start small and cheap on the Kotak Neo or Zerodha APIs. The wish list is:
- backtesting;
- paper trading;
- automated trading;
- One-Percent-style learning features.

The research found five constraints:
1. **Automated trading for other users.** The SEBI retail-algo framework has been mandatory since 2026-04-01. Automated trading for other users requires exchange empanelment as an algo provider, plus RA registration for black-box strategies.
2. **Paper trading on live prices.** SEBI's advisory (2024-11-04) and Kite's and Fyers' terms bar it.
3. **Broker data in our product.** Broker data can't feed our servers without written permission, and Kotak has no public terms or partner route.
4. **Competition.** Brokers now give algo and paper tools away free. Incumbents' backtests are widely distrusted.
5. **Registration.** Creator-led education earns well, but advisory features need IA/RA registration (the 1% Club holds both).

## Decision (proposed)
1. **Product:** a Hindi-first **Learn → Practise → Review** app. It gives no tips, calls, targets, returns claims, contests or leaderboards.
2. **Learn** launches first, with no data cost: lessons, calculators, a trade journal built from uploaded tradebooks, and an AI tutor that refuses opinions.
3. **Practise** launches only on **licensed** history: a reproducible backtester, replay drills, and paper trading with EOD or next-day fills. It never uses live broker data.
4. **Automation is gated.** The steps are, in order:
   1. A self-hosted open-source executor (the user's own key, IP and rules). This requires counsel's opinion plus written answers from Zerodha and Kotak.
   2. Hand-off to the broker, or a partnership with an empanelled provider.
   3. Our own empanelment, white-box strategies only.

   RA registration for black-box strategies is out of scope unless a new ADR says otherwise.
5. **Brokers:** use Kite and Kotak only for the owner's own prototyping. The multi-user broker (Dhan or Zerodha) is chosen after their written answers.
6. **Stack:** FastAPI + Postgres (Supabase Mumbai) + a React PWA on a DigitalOcean Bengaluru server. Backtest and paper engines are built in-house. No GPL, AGPL or Commons Clause engines are embedded.

## Consequences
- The pilot costs about ₹6.4–14.5k a month for infrastructure plus about ₹1L a year for NSE EOD. The Learn MVP takes about 8 weeks with one developer.
- The earlier evidence-assistant work (docs 13–17) is kept as a later module. Its "why it moved" cards can feed the Review lessons.
- Order-placing code enters the repo only after automation step 1 is approved. It then goes through `security-engineer` and `financial-correctness-reviewer`, and CLAUDE.md is updated in the same change.

## Alternatives
- **Hosted auto-trading from day one.** Rejected: empanelment, audits and possibly hosting inside the broker are needed first.
- **Live-price paper trading.** Rejected: blocked by SEBI and by broker terms.
- **Copying the 1% Club's advisory features.** Rejected without IA/RA registration.
- **Keeping ADR-008 option A (information-only assistant).** This is still valid. It costs more in data licences and competes with free broker AI.

## Revisit when
- Counsel's answers or the Zerodha, Kotak or Dhan answers arrive.
- NSE clarifies whether backtest tools or templates trigger empanelment.
- Pilot users show demand for automation.
