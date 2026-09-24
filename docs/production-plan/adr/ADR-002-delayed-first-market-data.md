# ADR-002: Delayed-first market data with explicit entitlement labels

- **Status:** Proposed (2026-09-24). Blocked on written confirmation from vendors (G-DATA).
- **Deciders:** repository owner

## Context
- Real-time SIP display costs:
  - roughly $1 per tape per month for a non-professional user;
  - roughly $92 per month across three tapes for a professional user;
  - about $12k per month in fixed fees at pilot scale (redistribution, access, and non-display).
- 15-minute delayed display has no per-user CTA or UTP fees.
- The target users (newsletter writers and advisers) are probably "professional" subscribers.
- None of the repo's current providers license display to paying users.
- A new SIP fee regime (the CT Plan) starts 2027-04-01. The DataCT agreement must be signed by 2027-03-01.

Sources: [research/market-data.md](../research/market-data.md) §A–C.

## Decision
1. The pilot shows **15-minute delayed** full-volume prices, from a vendor that confirms display rights in writing.
2. An **indicative (modelled/FMV) real-time** feed may be shown **only if it is labelled "Indicative"**.
3. Real-time exchange data (Cboe One Summary or Nasdaq Basic) is a **later paid upsell**. It is gated on a non-professional attestation, with per-user fees passed through in the price.
4. Every displayed price carries:
   - the source;
   - the entitlement (`real-time | indicative | delayed-15 | eod`);
   - an "as of" time.

   Fallback between sources never hides a change of entitlement.
5. yfinance and the free tiers of Finnhub, Alpha Vantage, Twelve Data, and Marketaux are **dev-only**.

## Consequences
- Pilot data cost is estimated at about **$500–3,000 per month**, with $0 per user. **It is unconfirmed which vendor meets the detector's data spec**, meaning consolidated, full-volume, 1-minute delayed bars ([06 §1](../06-quantitative-validation.md#required-data-specification-for-the-intraday-detector)). If none meets it affordably, the detector runs in a price-only, partial-venue fallback mode ([09](../09-costs-and-operating-model.md)).
- If users reject delayed prices (H4), the pilot switches to a *labelled* indicative real-time feed at about $2.5k per month fixed (G-LATENCY in [08](../08-implementation-roadmap.md#stopgo-gates)).
- Exports that subscribers republish are redistribution. They are limited to derived statistics, EDGAR content, and headline links until vendors permit more.
- Alerts on delayed data fire about 16 minutes after the trade. This is acceptable for an explanation product. It is validated as hypothesis H4 in [02](../02-product-thesis.md#6-product-hypotheses-and-how-to-validate-them).
- EDGAR filings are real-time and free to redistribute, so the evidence layer is not delayed.
- The data model must carry entitlement and timestamps from the first migration.
