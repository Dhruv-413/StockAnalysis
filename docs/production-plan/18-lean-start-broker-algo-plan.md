# 18 — Lean Start: Broker APIs, Backtesting, Paper Trading, Automation, One-Percent-style Features

← [Index](README.md) · Related: [17 What is achievable](17-what-is-achievable.md) · [16 India research round 3](16-india-research-round-3.md) · [ADR-010](adr/ADR-010-lean-start-learn-practise-review.md)

**Status:** proposal (2026-09-24). This is not legal advice. It **conflicts with current project rules**: CLAUDE.md says "never execute trades or add order-placing code", and ADR-008 says information-only. Nothing in those rules changes unless the owner accepts [ADR-010](adr/ADR-010-lean-start-learn-practise-review.md).

**The ask.** Start small and cheap on the **Kotak Neo or Zerodha Kite** APIs, with user **backtesting**, **paper trading** and **automated trading**, plus features like the **One Percent app (Finance With Sharan)**. Find how to build it fast on a small budget.

**Evidence** (four new appendices, accessed 2026-09-24, with H/M/L confidence inside each):
- [algo-legal-path](research/algo-legal-path.md) (compliance-analyst)
- [broker-algo-apis](research/broker-algo-apis.md) (market-data-researcher)
- [one-percent-and-algo-comps](research/one-percent-and-algo-comps.md) (product-manager)
- [fast-cheap-stack](research/fast-cheap-stack.md) (tech-scout)

---

## 1. Verdict in brief

| Owner wants | Practical answer | Conf. |
|---|---|---|
| **Build on Kotak Neo / Zerodha** | **Yes for the owner's own prototype**: Kite for history and research (₹500/mo, 1-min history from about 2015), Kotak for execution (free API, zero API brokerage *for now*). **For a multi-user product, neither is confirmed**: Kotak has no partner route or public API terms; Kite data cannot pass through our servers without Zerodha's written approval. Dhan (formal partner programme, open sandbox) is the other candidate. | H/M |
| **User backtesting** | **Achievable now** in two forms: (a) it runs on the user's own machine with their own broker key; (b) hosted, on **licensed** end-of-day (EOD) history (NSE EOD about ₹1L/yr + vendor). Results stay private; no published returns. | M-H |
| **Paper trading** | **Live prices: not achievable.** A SEBI advisory of 4 Nov 2024 names virtual trading, the SEBI circular of 24 May 2024 restricts real-time sharing, Kite bans "virtual/mock trading apps", and Fyers bans "paper trading". **EOD / next-day fills on licensed data: achievable**, provided there are no prizes, contests or leaderboards (the Online Gaming Act has been in force since 2026-05-01). 15-min delayed prices need counsel (CQ-A-5). | H / M / L |
| **Automated trading** | **Hosted for other users:** we become an "algo provider". That needs exchange empanelment through a broker (about 30 days per exchange, ISO 27001/SOC 2, a CERT-In audit), registration of each strategy, static IPs, possibly hosting inside the broker (Kotak's own page says so), and **RA registration for black-box strategies**. **The only route with no registration:** open-source software the user self-hosts with their own key, IP and rules. We ship no strategies, relay no orders and take no broker revenue share. Zerodha still has to confirm this counts as personal use (Q-Z-7). | H / M-L |
| **One-Percent-style features** | The 1% Club is **SEBI IA- and RA-registered** (INA000018896, INH000023968). Revenue was ₹54.9 Cr in FY25, with ₹10 Cr raised from Gruhas. Its "AI CFO" is legal *because* it is registered. **We can do without registration:** courses, community, calculators, a trade journal, and expense tracking. **We cannot:** goal-based advice, Account Aggregator data, MF transactions (these need IA, an ARN or the execution-only route). | H |
| **Fast and cheap** | **About ₹6.4k/mo** pilot infrastructure (about ₹14.5k/mo including payment fees and GST at ₹1L of sales). **8 weeks, 1 developer** for the learn-and-practise MVP. Data licences for the practice features are extra and quote-dependent. | M |

## 2. Recommended shape: "Learn → Practise → Review" (Hindi-first, no tips or calls)

Why this shape:
- Brokers now give algo and paper tools away free: Streak, Dhan, Sensibull for Zerodha users, and Kotak's free API.
- The top complaint about incumbents is **backtests that can't be trusted or reproduced** (Streak iOS rating 2.8, Stratzy 3.7).
- Creator-led education monetises well (the 1% Club).
- This gap is guided practice tied to lessons, done honestly. Low prices alone are not a gap. See [one-percent-and-algo-comps](research/one-percent-and-algo-comps.md).

| Tier | Features | SEBI posture | Data cost |
|---|---|---|---|
| **1. Learn (weeks 1–8, ₹0 data)** | Hindi + English lessons; option payoff and position-size calculators (user inputs); a **trade journal** from the user's uploaded broker tradebook (P&L, charges, mistakes tagged by the user); an AI tutor that refuses stock opinions; course and community checkout | A (education; named-stock examples use data at least 30 days old) | ₹0 |
| **2. Practise (built on fixtures; launched when the licence lands)** | **Reproducible backtester** for the user's own rules, with a dated Indian cost model (brokerage, STT at the 2026-04-01 rates, exchange charges, stamp duty, GST); **replay drills** of past sessions (Budget day, expiry days, crash days); **paper trading with EOD / next-day fills** | A (private runs; no published returns, contests or leaderboards) | NSE EOD about ₹1L/yr + a vendor for intraday history (quote only) |
| **3. Automate (gated by ADR-010 + counsel + Zerodha/Kotak answers)** | Step 1: a **self-hosted open-source executor** (user's own key, static IP and rules; we host nothing in the order path). Step 2: **hand-off to the broker** (e.g. Kite trade buttons, where the user confirms each order) or partner with an **empanelled provider**. Step 3: our own empanelment, **white-box strategies only**. Step 4: RA registration only if black-box strategies are ever wanted. | A (step 1, conditional) → C (step 3) → B (step 4) | — |

**Personal-finance add-ons with no registration needed:**
- expense tracking on user-entered or uploaded data (Android SMS reading is a Play exception, subject to review);
- goal calculators, as arithmetic only.

**Anything that tells a user what to do with their money** needs an IA partner.

## 3. Broker choice ([broker-algo-apis](research/broker-algo-apis.md))

| Use | Broker | Why | Caveat |
|---|---|---|---|
| Owner's own research and backtests | **Zerodha Kite Connect** (₹500/mo) | Deepest history (1-min bars from about 2015), best SDK (`kiteconnect` 5.2.2, MIT) | Personal use only; **no paper trading on Kite data** |
| Owner's own execution tests | **Kotak Neo** (free) | Zero API brokerage (the pricing page and API page disagree on whether it lasts only the first 30 days); 1-min history from 2021 (30 days per request); static IP needed only for order calls | No public API terms or partner route. SDK `kotakneoapi` 3.0.7 was rewritten in Aug 2026 and has unanswered bugs. OI field is empty. Reported rate-limit errors lasting about 2.75 h. |
| Multi-user product (later) | **Dhan** or **Zerodha** (pending written answers) | Dhan has a formal partner login and an open sandbox; Zerodha is free for approved mass-retail platforms | Display and paper trading are not granted by any sandbox |

**Execution facts to design for:**
- Market orders sent through APIs become **protected limit orders**, and the limit-price bands apply (futures ±3%, options ±40% or ₹20).
- **Freeze quantities** change several times a year (NIFTY 1,800 and BANKNIFTY 600 from 2026-09-01). Read them from the exchange; never hard-code them.
- Before empanelment, **one static IP can be shared only with family**.

## 4. Fast, cheap build ([fast-cheap-stack](research/fast-cheap-stack.md))

**Stack:**
- **App:** Python 3.12 + FastAPI (from the MIT `full-stack-fastapi-template`), Polars/DuckDB, APScheduler.
- **Backtest and paper engines:** **our own**. One developer can build them in under 2 weeks, plus `bt`/`ffn` (MIT) for metrics.
- **Front end:** React + shadcn + TradingView lightweight-charts, as a PWA (native mobile comes later).
- **Hosting:** DigitalOcean Bengaluru (static IP possible), plus Supabase Pro in Mumbai (Postgres + auth).
- **Payments:** Cashfree (0% on the first ₹20L until 2027-03-31) or Razorpay. Check both restricted-business lists.
- **Courses and community:** Exly or Graphy, plus Discord.

**Licence traps (don't embed these in a paid product):**
- OpenAlgo platform: **AGPL**. Learn from it, or let users run their own unmodified copy; its `openalgo` client is MIT.
- backtrader (GPL), Backtesting.py (AGPL), vectorbt / PyBroker (Commons Clause), fastquant (GPL on PyPI), polars-backtest (non-commercial).

**Never install:** `kotak-neo-api`, `pybroker`, `neo-api-client` or `pykiteconnect` (all unregistered on PyPI, so anyone can squat the name); `htmx` on PyPI (unrelated package); `jugaad-trader` (reverse-engineered password login, no licence).

**Hosting that won't work for broker order calls:** Railway and Render (shared outbound IPs, no India region). Oracle Always Free is for development only.

**Estimated monthly cost:**

| Item | Pilot |
|---|---|
| DigitalOcean BLR server + Supabase Pro + domain/email | about ₹6.4k ($73) |
| + payment commission and GST at ₹1L of course sales | about ₹14.5k ($165) total |
| + NSE EOD display licence (for Practise) | + about ₹8.3k |
| + intraday history vendor | quote |

**8-week plan, 1 developer:**
1. **Week 1:** ADR-010 decision; send the questions; repo tooling and tests (T-01 key rotation first).
2. **Weeks 2–3:** Learn tier. Lessons CMS link-out, calculators, trade-journal upload parser, AI tutor with a refusal template.
3. **Weeks 4–5:** backtester v1 on recorded fixtures, cost model, golden tests (reviewed by `financial-correctness-reviewer`).
4. **Week 6:** replay drills and EOD paper engine on fixtures.
5. **Week 7:** checkout, auth, Hindi copy, the G8 disclosure.
6. **Week 8:** pilot with 5–10 users; buyer interviews.

The live executor stays out of the 8 weeks.

## 5. Guardrails that keep it legal (from [feature-legality](research/feature-legality.md) and [algo-legal-path](research/algo-legal-path.md))

- **No tips, calls, targets, stop-loss "levels" or signals** anywhere: product, AI tutor, community, creator content.
- **No performance or returns claims.** A SEBI rule of Sep 2022 stops brokers working with platforms that advertise algo returns. PaRRVA verification is only open to registered entities.
- **No prizes, contests or public leaderboards** for paper trading.
- **Creators:** only SEBI-registered ones, or education-only creators under contract. This is because of SEBI's finfluencer/association rule (Reg 16A). Zero1 dropped its outside creators in April 2026.
- **Broker data stays on the user's device** unless there is a written licence. No Kite data in our fixtures, cache or demos.
- **Orders:** none, until ADR-010 is accepted and the self-hosted route is confirmed by Zerodha/Kotak and counsel.

## 6. Questions to send (drafted in the appendices; none sent)

- **Counsel:**
  - CQ-A-1 / CQ-A-4: do templates or any hosted part make us an algo provider?
  - CQ-A-3: must empanelled platforms be hosted inside each broker?
  - CQ-A-5: paper trading on 15-min delayed / EOD data.
  - CQ-A-10: partnering with a multi-RA strategy host.
  - CQ-A to CQ-F in the product appendix.
- **Zerodha:**
  - Q-Z-5: can an approved platform show backtests or paper trading?
  - Q-Z-7: does client-run open-source software count as personal use?
- **Kotak:** Q-K-1 to Q-K-7 (API terms, third-party backtest and paper, partner route, session, limits, how long zero brokerage lasts, UAT scope).
- **Dhan:** Q-D-2. **Upstox:** Q-U-2. **NSE:** Q-NSE-8 (do backtest tools or strategy templates trigger empanelment?).
- **Vendors:** quotes for EOD and intraday F&O history, with storage and display rights.

## 7. Decisions for the owner

1. **Accept ADR-010?** It would switch the product to "Learn → Practise → Review", keep automation gated, and supersede ADR-008 scope option A.
2. **Target user:** Indian retail beginners (Hindi-first), replacing doc 02's US equity researchers?
3. **Data spend for Practise:** NSE EOD (about ₹1L/yr) plus a vendor quote for intraday history?
4. **Go-to-market:** lead with paid cohort seats for registered educators, or with consumers (₹99–149/mo or ₹999–1,499/yr)?
5. **Automation path:** stop at the self-hosted executor, or plan for empanelment (white-box only)? RA registration ever?
6. **Permission to send** the questions in §6.
