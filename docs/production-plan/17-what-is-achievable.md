# 17 — What Is Practically Achievable (feature-by-feature)

← [Index](README.md) · Related: [14 Market assistant](14-global-market-assistant.md) · [15 Finance-model layer](15-finance-model-layer.md) · [16 India research round 3](16-india-research-round-3.md)

**Status:** proposal (2026-09-24). This is not legal advice; the counsel questions are in §9. All costs are **estimates**. They exclude 18% GST and assume ₹88 = $1.

**The ask.** "Define everything that is achievable practically." This covers every capability the owner has asked for:
- news from around the world;
- sentiment;
- indicators and algos;
- deals;
- stock details and history;
- replies in about 300 ms;
- accuracy, reliability and "real";
- use by Zerodha, Groww, Angel One, TradingView and Bloomberg users.

**Evidence** (three new appendices, all accessed 2026-09-24, with H/M/L confidence inside each):
- [data-stack-costs](research/data-stack-costs.md) (market-data-researcher): what data can be bought, at what price, with what display rights.
- [feature-legality](research/feature-legality.md) (compliance-analyst): 28 features classified by SEBI posture, plus guardrails.
- [build-cost-latency](research/build-cost-latency.md) (sre-engineer): infrastructure, LLM cost, measured latency, engineering effort.

They build on the earlier appendices: [16](16-india-research-round-3.md), [15](15-finance-model-layer.md) and [14](14-global-market-assistant.md).

**Verdict key** (how each item is labelled in the tables below):

| Label | Meaning |
|---|---|
| **NOW** | Buildable today with free or official sources and no registration. |
| **LICENCE** | Buildable once a data licence or vendor contract is signed. |
| **REG** | Needs SEBI Research Analyst (RA) or Investment Adviser (IA) registration, or a registered partner. |
| **NO** | Not achievable, or ruled out by this project's rules. |

---

## 1. Bottom line

1. **Most of what the owner wants can be built legally, as information only.** Of the 28 features assessed, about 20 are "posture A" in [feature-legality](research/feature-legality.md): an unregistered publisher may offer them, provided the product never:
   - recommends a stock;
   - gives an opinion on a named stock;
   - personalises output to the user's holdings;
   - claims returns or accuracy.
2. **The binding constraint is data rights, not technology.**
   - Indian vendors that allow display are **quote-only, with no startup plans**.
   - The only published prices are NSE's annual licences:
     - EOD display: ₹1L per year.
     - 15-min delayed: about ₹80k per segment per medium per year.
     - Corporate Data: ₹10L per year.
     - Real-time, even in a free app: ₹21L per year fixed.
   - Kite and the other broker APIs **cannot** feed a product ([16 §2](16-india-research-round-3.md)).
3. **"300 ms" is achievable for the card part of an answer, not for an AI-written answer.**
   - **Server-side card time: 10–70 ms (expected).**
   - **On a phone over 4G with the connection already open: about 85 ms median, about 240 ms at p95.**
   - **On a cold connection: about 250 ms median, about 690 ms at p95.**
   - The AI narrative streams afterwards, taking 0.3–1.5 s.
4. **Infrastructure is cheap; licences and people are what cost money.**
   - Hosting in Mumbai costs about **₹19–27k/mo for a pilot** and **about ₹1.15L/mo at 100k users**.
   - Generating one AI narrative **per card version** (not per query) costs **$88–977/mo at 100k users**. Generating one per query would cost $2.9k–32.6k/mo.
5. **Build effort is about 29–59 engineer-weeks.**
   - 1 developer: 8–17 months.
   - 2 developers: 5–11 months.
   - 4 developers: 3–6.5 months.
   - There is a **3-month calendar floor** set by the NSE and vendor licence answers, the counsel memo, and labelling the gold set.

## 2. The owner's wishlist and what is achievable

| Owner asked for | What is practically achievable | Verdict | What it depends on |
|---|---|---|---|
| **News from around the world** | English and Hindi Indian headlines plus global headlines, each shown as **headline + link + time**, with our own event tags. Full-text AI summaries only from **licensed** text (PTI, HT Syndication, vendor news). | **NOW** (headlines: Marketaux ~₹4–17.5k/mo; GDELT free) / **LICENCE** (summaries; quote) | Copyright; Dow Jones v. Perplexity is the warning case |
| **Official news and events** | SEBI and PIB RSS, the MoSPI macro API, US EDGAR: free. NSE and BSE announcement RSS: internal evaluation only until NSE/BSE confirm in writing. | **NOW** (SEBI, PIB, MoSPI, EDGAR) / **LICENCE** (NSE/BSE announcements: Corporate Data ₹10L/yr or a vendor feed) | Q-O1; NSE terms ban automated collection |
| **Sentiment** | A **text-tone label on each headline** (for example "tone of headline: negative"), plus internal ranking. **No per-stock sentiment score or bullish/bearish gauge.** | **NOW** (per item) / **REG** (per-stock score) | Our own English + Hindi labelled set (no public benchmark exists); reconcile invariant 5 (§8) |
| **Indicators** | RSI, MACD, moving averages, VWAP, ATR, Supertrend, pivots and so on, shown as **values with formula and threshold**. Computed by TA-Lib to a canonical spec. | **NOW** (the compute) / **LICENCE** (the price data underneath) | Golden fixtures ([accuracy](research/accuracy-indicators-algos.md)) |
| **Screeners** | Filters the user builds ("RSI(14) < 30", "52-week high today"). | **LICENCE** | Curated "stocks to buy" screens are **REG** |
| **Algos** | A **private backtest** of the user's own rules, shown only to that user, with costs stated. | **LICENCE** (history data) | Live "deploy", a strategy marketplace or order placement are **NO** under project rules (legally REG/IA plus empanelment) |
| **Deals** | Bulk, block, insider (PIT/SAST) and FII/DII records, shown **verbatim with dissemination time**, labelled "after close". | **LICENCE** (vendor or NSE Corporate Data; quote) | "Smart money is buying" framing is **REG** |
| **Stock details** | Fundamentals, ratios, shareholding, promoter pledge and corporate actions, shown as numbers with period and source. | **LICENCE** (Accord / CMOTS / TrueData; quote only) | CMIE Prowess is **prohibited** for products. No "fair value" or quality score. |
| **History** | EOD history and charts, adjusted from a corporate-action table. | **LICENCE** (EOD ₹1L/yr + vendor) | Without corporate-action data, history must be labelled "unadjusted" |
| **Live prices** | Delayed 15-min is realistic. Real-time costs ≥ ₹21–27.5L/yr **per medium**. | **LICENCE** | The NSE category answer (Q-NSE-1) |
| **Options** | Option chain with Greeks, PCR and max pain, shown as plain statistics with the model stated. | **LICENCE** (F&O segment + vendor) | Never "expected expiry level"; include a dated SEBI F&O loss line |
| **"Why did it move"** | Cited evidence cards, with before / after timing states and "no catalyst found" when that is the answer. **The core product.** | **LICENCE** (prices + announcements) | Counsel CQ-7 (whether this counts as "research analysis") |
| **~300 ms reply** | Cards in 10–70 ms server-side; about 85 ms / 240 ms (median / p95) on 4G with the connection already open. AI narrative 0.3–1.5 s after that. | **NOW** (tech) | Choice of LLM region (§8) |
| **Very accurate, reliable, "real"** | Every number comes from code. Each carries a source, an entitlement label and an `as_of` time. A verifier drops unmatched numbers. Abstain when there is no evidence. Target 99.5% availability on a single availability zone (99.9% multi-AZ costs +40–50%). | **NOW** (design) | A gold set of about 800 cases; this is not "real-time" unless licensed |
| **Buy/sell calls, targets, top picks, "should I buy"** | Refuse, and show the evidence cards instead. | **REG** (or **NO** under the ADR-008 option A scope) | RA route: NISM XV exam, a ₹1–10L deposit, audits, PaRRVA for any claim |
| **Forecasts (Kronos-type)** | Internal volatility challenger only. | **NO** for users | Invariant 5; [15](15-finance-model-layer.md) |
| **For Zerodha / Groww / Angel / TradingView users** | Our **MCP server** alongside **Zerodha's hosted Kite MCP** in the user's own AI client; a web app; a Telegram digest; a TradingView-style link-out. **We cannot show their broker data.** | **NOW** (MCP, web, Telegram) / **NO** (redisplaying broker data) | Q-Z-4; a broker partnership needs the broker's own compliance sign-off (Reg 16A) |

## 3. Full feature catalogue (from [feature-legality §3](research/feature-legality.md), plus data, speed and effort)

"Speed" is server-side for the card; "Build" is engineer-weeks inside the §6 totals.

| # | Feature | SEBI posture | Data needed (cheapest licensed route) | Speed | Verdict |
|---|---|---|---|---|---|
| 1 | Price display (delayed or EOD) | A | NSE delayed ₹80k/yr per segment per medium; EOD ₹1L/yr | cached < 10 ms | LICENCE |
| 2 | Stock page (fundamentals, shareholding) | A | Accord / CMOTS / TrueData (quote) | cached | LICENCE |
| 3 | Historical charts | A | EOD + corporate actions | cached | LICENCE |
| 4 | Indicator values | A | Any price licence above | precomputed | LICENCE |
| 5 | User-built screeners | A | Same | < 100 ms for about 2k symbols (estimate) | LICENCE |
| 5b | Curated idea screens | **B** | — | — | REG |
| 6 | Chart-pattern naming | **B** by default | — | — | REG (a narrow A form needs counsel, CQ-4) |
| 7a | Headline + link aggregation | A | Marketaux, GDELT, SEBI/PIB RSS | cached | NOW |
| 7b | AI news summaries | A | Licensed full text | 0.3–1.5 s stream | LICENCE |
| 8 | Tone label on each headline | A | Our own labelled set | precomputed | NOW |
| 9 | "Why it moved" cards | A | Prices + announcements | cached | LICENCE |
| 10 | Event calendar | A | Corporate-data vendor | cached | LICENCE |
| 11 | Deal feeds | A | Vendor / NSE Corporate Data | cached | LICENCE |
| 12 | FII/DII flows | A | Vendor (NSDL FPI Monitor prohibits redistribution) | cached | LICENCE |
| 13 | Option chain, Greeks, PCR, max pain | A | F&O licence + vendor | precomputed | LICENCE |
| 14 | Price alerts / abnormal-move alerts | A | Price licence (real-time alerts may trigger NSE's non-display fee, Q-NSE-3) | ≤ 90 s after the bar | LICENCE |
| 15 | Watchlist digest | A | Same | batch | LICENCE |
| 16 | Portfolio arithmetic on uploaded holdings | A (descriptive) / C (evaluative) | User upload only (Account Aggregator needs a regulated entity) | < 100 ms | NOW for arithmetic; NO for "you should…" |
| 17 | Private backtest of the user's own rules | A | History licence (storage rights, Q-NSE-5) | seconds (batch) | LICENCE |
| 18 | Strategy marketplace | C | — | — | NO |
| 19–21 | Ratings, target prices, top picks | B | — | — | REG |
| 22 | "Should I buy X" chat | A only as a refusal | — | < 50 ms refusal + cards | NOW (refusal) |
| 23 | Forecasts shown to users | B legally / project D | — | — | NO |
| 24 | Order placement | C legally / project D | — | — | NO |
| 25 | Telegram digest | A | Same as the cards | batch | NOW |
| 26 | MCP server | A | Same as the cards; tools take symbols and timestamps, never prices | 10–70 ms | NOW |
| 27 | Education content | A | Named-stock data at least 30 days old (SEBI, 8 May 2026) | static | NOW |
| 28 | Paid subscriptions | Posture unchanged | — | — | NOW for A features |

**Guardrails that keep features in posture A** (G1–G11 in [feature-legality §2](research/feature-legality.md)):
- **G1:** the same canonical content for every user.
- **G2:** a deny-list of recommendation words (buy/sell/hold, target, stop-loss, signal, call, pick, bullish/bearish as a verdict, undervalued).
- **G3:** no forward-looking statements.
- **G4:** show values with their formula, not an interpretation.
- **G5:** no performance claims.
- **G6:** evidence timing states.
- **G7:** entitlement labels.
- **G8:** a standing "information only, not SEBI-registered" disclosure.
- **G9:** the AI refuses opinion questions.
- **G10:** no engagement or trending mechanics.
- **G11:** broker deals need the broker's compliance sign-off.

## 4. Three practical packages (monthly, estimates)

| | **Starter (~₹50k/mo)** | **Standard (~₹1.3L/mo)** | **Pro (~₹5.5–7L/mo)** |
|---|---|---|---|
| Data | ~₹25k: NSE EOD + 15-min delayed cash market (**web only**); headlines with links; SEBI, PIB, MoSPI, EDGAR | ~₹1L: delayed cash + F&O on **web and app**; EOD; one corporate-data feed (if quoted ≤ ~₹50k/mo) | ~₹5L: **real-time NSE cash market on one medium** + NSE Corporate Data, if NSE accepts the open-website or free-app category |
| Infra (AWS Mumbai) | ~₹19k (single AZ, pilot ~1k users) | ~₹27k (multi-AZ) to ~₹42k (10k users) | ~₹1.15L (100k users, multi-AZ) |
| LLM narrative (per card version) | < ₹2k | < ₹5k | ₹8k–85k |
| **Can show** | EOD and delayed charts, indicators, SEBI/PIB events, headline cards, unadjusted history, MCP + web + Telegram | + F&O chain, the app, adjusted history, announcements, deal and fundamental cards (if the vendor quote fits) | + real-time prices on one medium; full announcement coverage |
| **Cannot show** | Real-time, F&O, the app, fundamentals, announcements, US prices | Real-time, BSE, licensed news text | Real-time on both web and app, real-time F&O, real-time indices beyond ~350 users |

One-time costs on top:
- counsel memo;
- pentest ($5–15k);
- optional RA registration (₹50k in SEBI fees + ₹1–10L deposit + audits).

NSE's answers to Q-NSE-1 and Q-NSE-3, and to Q-DS-1 and Q-DS-2, decide which package is real ([data-stack-costs §3](research/data-stack-costs.md)).

## 5. Speed: what "300 ms" can honestly mean ([build-cost-latency §3](research/build-cost-latency.md))

| Leg | Figure | Conf. |
|---|---|---|
| Server: cached card (Valkey same-AZ GET + template) | 10–70 ms (expected; our 120 ms / 300 ms targets are easy) | M |
| Delhi user → Mumbai, 4G, **connection already open** | about 85 ms median / about 240 ms p95 | M/L |
| Same, **new connection** | about 250 ms median / about 690 ms p95 (about 430 ms with TLS terminated at an India CDN edge) | L |
| Mumbai → US-East (LLM APIs without an India endpoint) | 193 ms RTT | M |
| LLM first token (Gemini 2.5 Flash-Lite, measured in the US) | about 0.30 s | M |

**Achievable promise:** "first useful content in under 300 ms for a warm session". Report server-side and on-device timings separately.

## 6. Build effort and timeline ([build-cost-latency §4](research/build-cost-latency.md), low confidence)

| Component | Engineer-weeks |
|---|---|
| Symbol master + Hinglish resolver | 2–4 |
| Licensed EOD/delayed ingest | 3–5 |
| Card precompute (indicators, volatility, events, golden tests) | 4–7 |
| Cache + API + latency harness | 2–4 |
| Grounded narrative + verifier + eval harness (+ 60–80 h gold-set labelling) | 3–5 |
| MCP server | 1–3 |
| Web app | 4–8 |
| Telegram bot | 1–2 |
| Observability, CI, tests | 3–5 |
| Security hardening | 2–4 |
| **Total including 15–25% overhead** | **≈ 29–59** |

| Team size | Elapsed time |
|---|---|
| 1 developer | 8–17 months |
| 2 developers | 5–11 months |
| 4 developers | 3–6.5 months (3-month calendar floor) |

## 7. Phased plan (proposal)

**Phase 0: now to about 4 weeks. No licences needed; zero data spend.**
- Rotate the leaked keys (T-01), add tooling and tests (T-02, T-03).
- Send the drafted questions:
  - NSE, vendors and news wires: Q-NSE, Q-DS;
  - brokers: Q-Z/U/D/F;
  - official-data owners (AMFI, NSDL, Sarvam, RBI): Q-O;
  - counsel: CQ-1 to CQ-18.
- Build on free and official data only:
  - symbol master + Hinglish resolver;
  - canonical indicator spec with golden fixtures (recorded data only);
  - SEBI, PIB, MoSPI and EDGAR event cards;
  - a read-only MCP server skeleton (tools take symbols and timestamps);
  - the refusal template and G2 deny-list.
- Start labelling the gold set, and 500 English and Hindi headline tones.
- 12–15 buyer interviews (I-08): SEBI RAs, educators, small brokers, retail.

**Phase 1: about months 2–4. Starter or Standard licence.**
- EOD + delayed ingest.
- Card precompute (indicators, volatility, "why it moved").
- Cache + API with the p95 harness.
- Grounded narrative + verifier.
- Web app and MCP beta to 50–200 users.
- Telegram digest.

**Phase 2: about months 4–6.**
- Corporate-data feed (announcements, deals, fundamentals).
- F&O chain.
- Alerts.
- Private backtests.
- US second leg (Twelve Data Venture delayed, $499/mo, or Massive).

**Phase 3: gated.**
- Real-time prices, only if the NSE answers and willingness to pay justify ≥ ₹21L/yr per medium.
- L1 and L2 model layers ([15](15-finance-model-layer.md)).
- The RA route, only if the owner chooses option B.

## 8. Decisions and open conflicts for the owner

1. **Budget package:** Starter, Standard or Pro? (§4)
2. **LLM region.** Gemini 2.5 Flash-Lite and 2.5 Flash **retire on Vertex (the Mumbai region) on 2026-10-20**. The choices are:
   - (a) the global Gemini API (no promise that processing stays in India);
   - (b) the Vertex replacements, whose fast-mode latency hasn't been measured;
   - (c) self-hosted Sarvam-30B on one Mumbai GPU ($876–1,632/mo).

   OpenAI's India endpoint stores data in India but processes it elsewhere.
3. **Sentiment rule.** CLAUDE.md invariant 5 bans LLM sentiment scores, while doc 14 allows tone labels. **Proposed reconciliation [P]:**
   - allow a per-headline *text-tone* label, labelled with its model version;
   - ban per-stock aggregate scores and gauges.

   Amend the invariant wording only once you approve.
4. **Scope.** Keep ADR-008 option A (information only), or pursue RA registration for ratings and "should I buy" answers?
5. **Team:** 1, 2 or 4 developers (§6)?
6. **Permission to send the questions** drafted in the appendices. Each one reveals the product plan to the recipient.

## 9. Counsel priorities ([feature-legality §7](research/feature-legality.md))

- **CQ-7:** do cited "why it moved" cards count as research analysis? **The core product depends on this.**
- **CQ-4:** naming chart patterns on a single stock.
- **CQ-9:** warning flags on uploaded holdings.
- **CQ-13:** a user's AI turning our MCP output into advice.
- **CQ-18:** US event-timed alerts under the publisher's exclusion.
- **CQ-1:** the wording of the standing disclosure.

## 10. Corrections applied to earlier appendices (dated banners)

- [india-market-data-and-sebi](research/india-market-data-and-sebi.md):
  - The free-app real-time fee is **₹21L/yr fixed** (not NIL).
  - The delayed fee is **annual**.
  - Indices are a **separate** licence.
  - The education data lag is **30 days** from 2026-07-01 (it was 3 months).
- [global-news-and-data](research/global-news-and-data.md): CMIE Prowess commercial use is **prohibited** (H).
- [market-data](research/market-data.md): Twelve Data covers NSE/BSE at **EOD only**.
- [assistant-300ms-and-jev](research/assistant-300ms-and-jev.md): Mumbai → US-East is 193 ms; the Gemini 2.5 Vertex retirement is 2026-10-20; ElastiCache Valkey is confirmed in Mumbai.
