# US Equity/ETF Market-Data Licensing and Infrastructure Research

> **Corrections (2026-09-24, achievability round; see [17](../17-what-is-achievable.md)):**
> - **Twelve Data covers NSE/BSE at EOD only** (exchanges page, H).

- **Research and access date:** 2026-09-24. Every source below was accessed on this date.
- **Scope:** a small commercial web app for self-directed and pro-am US equity/ETF investors. It offers watchlists and explainable alerts on price and volume moves, news, and filings.
- **Confidence levels:** **H** means a primary source was read directly. **M** means a primary source was read through a summarizer or is partial or older. **L** means a secondary source or a conflicting one.
- **Software license vs. data rights:** a permissive *software* license (for example yfinance under Apache-2.0, or google-genai) grants **no** rights to the *data* it retrieves. Data rights come from the vendor's ToS and, underneath that, from exchange/SIP agreements. Every section below keeps the two separate.

---

## 0. Key findings

1. **None of the five current data integrations can be shown to paying users as configured.**
   - Finnhub, Alpha Vantage, Twelve Data (individual plans), Marketaux, and Yahoo/yfinance are all personal or non-commercial under their free or individual terms. See §A.
2. **Delayed data (15 min or more) removes per-user display fees, but it is not paperwork-free.**
   - CTA: display-unit fees don't apply to delayed data. Vendors still sign the NYSE Agreement for Receipt and Use of Market Data, and pay access fees if they delay a real-time feed themselves.
   - UTP: charges a **$250/mo External Delayed Redistributor fee** and a **$250/yr** admin fee for delayed-only vendors.
   - Both require a conspicuous "delayed 15 minutes" label. See §C.
3. **Server-side alerting on real-time exchange data is probably "Non-Display Use."**
   - Non-display fees are firm-level fees charged on top of display fees.
   - Current CTA schedule: Network A $2,000 last sale + $2,000 quotes; Network B $1,000 + $1,000 per month.
   - Fee-free derived feeds avoid this: Databento US Equities Mini, and the FMV products from Massive and Intrinio.
4. **The SIP fee regime changes on 2027-04-01.**
   - The SEC approved the CT Plan fee schedule on 2026-06-26.
   - The operative date is currently planned for 2027-04-01.
   - All CTA/UTP subscribers must sign with DataCT (the new administrator) by 2027-03-01. See §C.
5. **Real-time options that avoid exchange per-user fees are derived or partial-volume products.**
   - Databento US Equities Mini is a synthetic BBO blended from several venues.
   - Massive "Real-time Fair Market Value" and Intrinio EquitiesEdge are FMV prices, i.e. modeled prices rather than exchange prints.
   - IEX and Cboe One each carry only part of market volume.
   - For **volume-move alerts**, you need full-market volume. That means delayed or T+1 full-volume data (Databento `EQUS.SUMMARY`, SIP-delayed from a licensed vendor) or paid SIP/Nasdaq Basic plus NLS.
6. **Gemini:**
   - `gemini-1.5-flash` is shut down; its underlying `-002` version retired on 2025-09-24.
   - The `google-generativeai` SDK is deprecated and archived; support ended 2025-11-30. Use `google-genai`. See §F.

---

## A. Status of the endpoints this repo uses

### A1. Finnhub (`/quote`, `/company-news`, `/stock/profile2`, `/search`, `/stock/candle`)

- **Free tier:** 60 API calls/min. Websocket limited to 50 symbols. Company news covers 1 year plus real-time. Coverage is US. [F1] **H**
- **`/stock/candle` (OHLC):** the Free column on the pricing matrix shows **no** entry for US "OHLC". The only listed paid plan is **All-In-One at $3,500/mo, billed annually**, which offers "30+ years" of OHLC. Candles are therefore effectively not in the free tier. [F1] **M** (the docs page is JS-rendered and I could not read its "Premium" badge).
- **License:** both Free and All-In-One are labelled "Personal Use. Terms apply". [F1] **H**
- **ToS:** "All plan listed on Finnhub website is strictly for personal use unless explicitly stated otherwise."
  - Commercial users need written approval.
  - You may not "redistribute or share access to data or derived results … with anyone or any 3rd party without written approval".
  - Data must be deleted when the subscription ends. [F2] **H** (no last-updated date shown)
- **Verdict:** you cannot display Finnhub data to paying users without a negotiated commercial or redistribution agreement, and its price is not published.

### A2. Alpha Vantage (`TIME_SERIES_DAILY` with `outputsize=full`, `GLOBAL_QUOTE`, weekly/monthly)

- **Free tier:** "25 API requests per day". [AV1] **H**
- **Premium plans:** $49.99/mo (75 req/min), $99.99/mo (150), $149.99/mo (300), $199.99/mo (600), $249.99/mo (1,200). All have no daily limit. [AV1] **H**
- **Premium-only features:**
  - `outputsize=full`: "The 'full' outputsize is available to premium keys." [AV2] **H** — the repo's `outputsize=full` call will fail on a free key.
  - `TIME_SERIES_DAILY_ADJUSTED`: "this is a premium API function." [AV2] **H**
  - Weekly and monthly series appear to be free. [AV2] **M**
- **Realtime vs. delayed:**
  - `GLOBAL_QUOTE` accepts `entitlement=realtime` or `entitlement=delayed`. Without it, the default returns historical data. [AV2] **H**
  - Realtime and 15-min delayed US data require premium access, enabled through the "Alpha X Terminal", **for personal use**. [AV1] **M**
- **ToS:** the license is "for personal, non-commercial use". Use is commercial if you "provide information … as part of any type of commercial activity that allows individuals or entities other than User to access information directly or indirectly", or if you act on behalf of a corporation. For commercial use, contact premium@alphavantage.co. [AV3] **H**
- **Verdict:** not displayable to paying users on standard plans.

### A3. Twelve Data (`/quote`, `/time_series`)

**Individual plans** [TD1] **H** — stated as "personal, internal, and non-commercial purposes":

| Plan | Price | API credits/min | Daily limit | Websocket credits |
|---|---|---|---|---|
| Basic (free) | $0 | 8 | 800/day | 8 (trial) |
| Grow | $79/mo | 55 | Unlimited | 8 (trial) |
| Pro | $229/mo | 610 | Unlimited | 500 |
| Ultra | $999/mo | 2,584 | Unlimited | 2,500 |

**Business plans** [TD2] **M**:

- **Basic (free):** "internal non-display usage" only.
- **Venture ($499/mo, or $414/mo billed annually):** 2,584 API + 2,500 WS credits/min. For "companies showcasing data on client-facing apps or websites".
- **Enterprise ($1,099/mo):** includes "External distribution market data".
- **Enterprise+ (custom):** adds "Custom exchange licenses".

**Not verified:** whether Venture or Enterprise includes US real-time exchange/SIP per-user fees, or whether you would still need your own exchange agreements.

### A4. Marketaux (`/news/all`)

- **Plans** [MX1] **H**:

| Plan | Price | Requests/day | Articles/request |
|---|---|---|---|
| Free | $0 | 100 | 3 |
| Basic | $29/mo | 2,500 | 20 |
| Standard | $49/mo | 10,000 | 50 |
| Pro | $99/mo | 25,000 | 100 |
| Pro 50K | $199/mo | 50,000 | 100 |

- The API returns only "a short snippet of articles along with their links". [MX2] **H**
- **ToS** (2021): license "solely for your personal, non-commercial use". The site "may not be used in connection with any commercial endeavors except those that are specifically endorsed or approved by us." [MX3] **H**
- **Verdict:** commercial display needs written approval. The underlying articles belong to their publishers; show only a headline and a link.

### A5. Yahoo Finance / yfinance

- **Software:** yfinance is Apache-2.0. Its README says it is "not affiliated … with Yahoo", is "intended for research and educational purposes", and that "the Yahoo! finance API is intended for personal use only." [Y1] **H**
- **Data (Yahoo ToS):**
  - Prohibits automated collection "using any automated means … scrapers … without our express, prior permission".
  - Prohibits using the data "to create any database … data feed … that competes with" Yahoo.
  - "Unless otherwise expressly stated, you may not access or reuse the Services … for any commercial purpose." [Y2] **H**
- **Verdict:** **remove yfinance from the production path.** Keep it for local research at most.

---

## B. US equity real-time and delayed data vendors

"Display to external users" means showing data to your paying customers. Exchange per-user fees apply on top unless the row says otherwise.

| Vendor / plan | Instruments | Real-time vs delayed | WebSocket | History | Corp actions | Price (verified) | Software/API license | Data rights for external display | Exchange per-user fees | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|
| **Massive (formerly Polygon.io; renamed 2025-10-30)** Stocks Basic / Starter / Developer / Advanced [M1][M2] | All US stocks | Basic: end of day. Starter/Developer: 15-min delayed. Advanced: real-time | Starter and up | 2 / 5 / 10 / 20+ yrs | Yes (all tiers) | $0 / $29 / $79 / $199 per month | API | **"Individual use" only** | n/a (no display rights) | H |
| **Massive Stocks Business** [M3] | US | "Real-time **Fair Market Value**" (modeled, not exchange prints) | Streaming FMV and minute aggregates | 20+ yrs, trades and quotes | Yes | $2,499/mo | API | "Business use". **Not verified** whether that explicitly includes display to your customers | "No Exchange Fees or Approvals" | M |
| **Massive expansions** [M3] | US exchanges | Full Market Delayed (15 min) $499. Full Market real-time $1,999. Nasdaq Basic $1,999. Cboe EDGX $1,999. IEX $499 | — | — | — | per month | — | "Additional exchange fees apply". **Not verified** whether expansions require the $2,499 base plan | Pass-through (exchange approval needed) | M |
| **Databento US Equities** Standard [DB2][DB3] | 15 exchanges + 30 ATSs | Live: US Equities Mini (synthetic BBO and last sale, no license fees). `EQUS.SUMMARY` gives 100% intraday volume **delayed** plus consolidated end-of-day OHLCV, no license fees | Raw TCP / live API | 7 yrs OHLCV; 12 mo L1 | Yes (215 exchanges per [DB5]) | $199/mo (Jan-2025 blog) | API | Mini is described as supporting "external redistribution and non-display trading without licensing restrictions" [DB3]. The pricing table lists "External distribution" as a Plus feature. **Whether Standard + Mini covers a customer-facing app is not verified** | Mini: none. Nasdaq Basic w/ NLS Plus: $2,140 distribution + $0.50 per personal user / $14.10 per commercial user, passed through with a 2.9% card fee [DB1] | M |
| **Databento Plus / Unlimited** [DB4] | as above | as above | yes | 16+ yrs L1 (on the CME page) | Yes | CME page shows $1,750 / $4,500 "license fees"/mo, annual contract. **US-equities pricing not verified** | API | "External distribution", "Real-time distribution", "Delayed distribution" | Pass-through | L-M |
| **Alpaca Market Data – Trading API** [AL1][AL2] | US stocks, ETFs, options | Basic: IEX real-time; the SIP window excludes the latest 15 min. Algo Trader Plus: all US exchanges (CTA + UTP) | Basic: 30 symbols. Plus: unlimited | Since 2016 | Yes | $0 / $99 per month | API | **No redistribution.** "you cannot redistribute Alpaca API data" [AL3]. ToS is personal/non-commercial; making data available through a User Application needs 30 days' notice and can be refused [AL4] | n/a | H |
| **Alpaca – Broker API** [AL1] | same | Standard plans: "real time IEX or 15 mins delayed SIP" | yes | same | Yes | Standard included; $500 / $1,000 / $2,000 per month for higher RPM | API | For broker partners serving **their own brokerage customers**. Not applicable to a non-broker analytics app | not verified | M |
| **Tiingo** [TI1][TI2] | US and Chinese stocks, ETFs, mutual funds | IEX real-time; end of day | Yes (IEX WS) | 30+ yrs | Yes | Free / $30 (individual); $50/mo or $499/yr "internal commercial" | API | Plans are "Internal Use Only". Redistribution is priced "on our Product pages" (JS-rendered, not read). A Tiingo blog claims a $50 plan gives "redistribution rights"; a search summary claimed $250/$500. **Conflicting — Low** | IEX real-time redistribution is licensed by IEX ($500/mo TOPS fee payable by the Data Subscriber) [IEX1] | L |
| **EODHD** [EO1][EO2] | Global; US end of day, intraday, 15-min delayed live | 15-min delayed "Live" API; end of day | Yes (US) | US EOD from earliest; 1-min since 2004 | Yes | $0 (20 calls/day); $19.99–$99.99/mo personal | API | Listed plans are **personal only**; non-pro users may not display or redistribute. Commercial use is quoted on request, and commercial users are reported to exchanges | via quote | H |
| **Intrinio** Individual / Startup / Enterprise [IN1] | US equities, options, fundamentals, news | EquitiesEdge = **FMV real-time**; Cboe One 15-min delayed (about 10–15% of volume); SIP delayed and Nasdaq Basic at Enterprise | Yes | 50+ yrs EOD | Yes (adjusted and unadjusted) | $150/mo (personal, "No redistribution or display"). **Startup: $333/mo for 6 mo, then $666 for 6 mo, then $999**. Enterprise $1,250+/mo | API | Startup: "Commercial Use and Display Rights", business-wide license | "No exchange fees or paperwork" for FMV and Cboe One delayed | H |
| **Finnhub paid** [F1] | Global | real-time | Unlimited | 30+ yrs | Dividends | $3,500/mo (annual) | API | Still labelled "Personal Use"; redistribution needs written approval | not stated | H |
| **Twelve Data Venture / Enterprise** [TD2] | 85+ markets | real-time US | Yes | not verified | not verified | $499 / $1,099 per month | API | Client-facing display / external distribution | **not verified** | M |
| **IEX Cloud** | — | — | — | — | — | — | — | **Shut down 2024-08-31.** Assets bought by ex-execs (Blue Sky Data) | — | M [IX1][IX2] |
| **Nasdaq Basic (direct or via a vendor)** [NQ1][NQ2] | All US-listed (Nasdaq, NYSE, American) | real-time Nasdaq-venue BBO and last sale (+ NLS Plus for TRF volume) | vendor | — | — | 2026: $2,140/mo external distributor. Non-pro $0.50 + $0.25 + $0.25 = $1.00/user. Pro $14.10 + $7.20 + $7.20 = $28.50/user. Option: $1,500/mo for Derived Data to unlimited non-pros | — | Display allowed under the Nasdaq distributor agreement | per-user as listed | H |
| **Nasdaq Last Sale (NLS / NLS Plus)** [NQ1] | All US-listed (last sale only; NLS Plus adds TRF prints) | real-time last sale, no quotes | vendor | — | — | 2026 NLS distributor fee $1,680/mo. A tiered external-subscriber distributor table in the Nasdaq rulebook ($2,680 / $5,350 / $8,030 for 1–499 / 500–9,999 / 10,000+ or open website) is **probably** NLS; product not confirmed. **Non-pro per-user fee not verified** | — | via Nasdaq agreement | not verified | L-M |
| **Cboe One Summary / Premium** [NQ2] | All US-listed (Cboe venues) | real-time | vendor | — | — | Summary: $5,000 external distribution, $10 pro, **$0.25 non-pro**, $1,000 consolidation, $50k enterprise. Premium: $12,500 / $15 / $0.50 | — | via Cboe agreement | per-user | M (quoted in a Nasdaq SEC filing, not Cboe's own schedule) |
| **IEX TOPS (direct)** [IEX1] | IEX-traded only | real-time (small share of volume) | — | — | — | $500/mo real-time; delayed free | — | "A Data Subscriber may redistribute Real-Time IEX market data … to a natural person or entity" | none per-user (IEX fee only) | H |

---

## C. Exchange and SIP licensing economics

### C1. Current CTA (Tapes A and B) schedule [CTA1] **H**

- **Professional display fees:**
  - Network A: $45/device for 1–2 devices, $27 for 3–999, $23 for 1,000–9,999, $19 for 10,000+.
  - Network B: $23/device.
- **Non-professional:** $1.00 per network per month. Per-quote-packet billing is capped at $1.00 per non-pro per month.
- **Redistribution:** $1,000/mo per network. This applies to "any entity that makes … information available to any other entity or to any person other than its employees".
- **Non-Display Use:**
  - Network A: $2,000 last sale + $2,000 quotes.
  - Network B: $1,000 + $1,000.
  - (Per month. These are the category rates printed in the schedule. How the three categories stack for this use case is not verified.)
- **Access fees:**
  - Direct: A $1,250 last sale / $1,750 bid-ask; B $750 / $1,250.
  - Indirect: A $750 / $1,250; B $400 / $600.
  - Access fees apply to non-display use, or when the recipient receives data "in such a manner that the data can be manipulated and disseminated".
- **Delayed data** [CTA2] **H**:
  - The delay is 15 minutes.
  - "At present, display unit fees do not apply in respect of a Delayed Information … display service" for pro or non-pro users.
  - Anyone redistributing delayed data must sign the NYSE Agreement.
  - If you receive real-time data and delay it yourself, you pay access fees.
  - A conspicuous delay statement is required (e.g., "Prices Delayed 15 Minutes").

### C2. Current UTP (Tape C) schedule [UTP1] **H**

- **Display fees:** Pro $24/mo; non-pro $1/mo.
- **Redistributor fees:** real-time external redistributor $1,000/mo per firm (includes delayed). Delayed-only external redistributor $250/mo.
- **Admin fee:** delayed-only vendors pay $250/yr.
- **Delayed display:**
  - "Delayed Subscriber Usage is not currently fee liable" on controlled products.
  - No subscriber agreements are needed for delayed or end-of-day data.
  - A prominent delay message is required.
- **Not verified:** UTP non-display and access fee amounts.

### C3. CT Plan (replaces CTA/UTP)

- **Status:**
  - The SEC approved the fee schedule, as modified, on **2026-06-26** (Rel. 34-105778) [CT1] **H**.
  - Operative date currently planned for **2027-04-01**.
  - All subscribers and distributors must sign a new agreement with **DataCT** before **2027-03-01** [CT2] **H**.
- **Proposed fees** from the Amended Fee Proposal [CT3][CT4] — **M**. Treat the approval order's Exhibit F as authoritative; I did not read Exhibit F line by line.
  - **Professional:** $26 Tape A, $23 Tape B, $24 Tape C.
  - **Non-professional, per tape, marginal tiers:**

    | Non-pro users | Fee per user per tape |
    |---|---|
    | 1–2,000 | $0.90 |
    | 2,001–50,000 | $0.75 |
    | 50,001–250,000 | $0.60 |
    | 250,001–1,000,000 | $0.40 |
    | 1,000,001+ | $0.25 |

  - **Real-time redistributor:** $1,155 per tape.
  - **Access fees (inflation-adjusted):** direct last sale A $1,445 / B $865 / C $1,155; indirect last sale A $865 / B $460 / C $230.
  - **Non-display:** also inflation-adjusted; amounts **not verified**.
  - **Tape-C-only fees eliminated:** delayed redistributor, delayed access, and voice-response fees.
  - **Enterprise caps (non-pro):** $648,000 A / $490,000 B / $648,000 C.
- **Professional definition:** "any use of market data by or on behalf of any entity … or … by an individual to provide a service to a third party for compensation". Redistributors that rely in good faith on subscriber representations have a safe harbor [CT4]. **Pro-am users can be professionals, so you need a non-pro attestation flow that defaults unknown users to Pro.**

### C4. Market Data Infrastructure (MDI) and Regulation NMS changes

- **Round lots:** the new definition went live **2025-11-03**. Tiers: 100 shares (≤$250), 40 ($250.01–$1,000), 10 ($1,000.01–$10,000), 1 (>$10,000). Tiers are reassigned semiannually. SIP quote sizes are now in **shares**, not lots [RL1][RL2][RL3] **H**.
- **Odd-lot information** (including best odd-lot orders): compliance date was 2026-05-04 [RL2] **M** (I did not confirm it went live).
- **Competing consolidators (Rule 614):** still in the CFR [MDI1]. I found no source confirming any competing consolidator is operating as of 2026-09. **Not verified.**
- **Other 2026 proposals:** the SEC proposed on 2026-06-11 to rescind Rules 611 and 610(e) [NMS1] **H**. This is not directly relevant to display licensing.
- **Extended SIP hours:** approved; implementation expected 2026-12-06 [CTA3] **H**.

### C5. Vendor bundling

- **Fee-free because derived or FMV:** Massive Business, Intrinio EquitiesEdge, Databento Mini.
- **Fees passed through:** Databento passes venue fees through with no upcharge (plus 2.9% on card), and acts as vendor of record [DB1]. Massive expansions: "Additional exchange fees apply" [M3].

---

## D. Reference, fundamental, and other data

- **SEC EDGAR:**
  - `data.sec.gov` submissions and XBRL (`companyconcept`, `companyfacts`, `frames`) need "no authentication or API keys". They update in real time, with a nightly bulk ZIP [SEC1] **H**.
  - Fair access: at most 10 requests/second, and you must declare a User-Agent such as "Company Name admin@…" [SEC2] **H**.
  - Reuse: "Information presented on sec.gov is considered public information and may be copied or further distributed … without the SEC's permission." The SEC seal and "EDGAR" marks are restricted [SEC3] **H**.
- **FRED API:**
  - Series "may be owned by third parties and subject to copyright restrictions". Before using them for "anything other than your own personal use, you must contact the data owner". Copyrighted series say "Copyright" in their notes [FR1] **H**.
  - Check each series. Government series (BLS, BEA, Fed H.15, etc.) are generally fine; vendor series such as ICE BofA and S&P/Case-Shiller are not.
- **OpenFIGI (symbology):**
  - Free and open. Mapping: 25 requests/min without a key, 25 per 6 s with a key. Search: 5/min without a key, 20/min with [OF1] **H**.
  - Commercial redistribution terms for FIGI: not verified (FIGI is published as an open standard).
- **Corporate actions:**
  - Massive includes "Corporate Actions" on every stocks tier, including free (individual use) [M2].
  - Databento covers corporate actions for 215 exchanges [DB5].
  - EODHD includes dividends and splits [EO1].
  - Intrinio provides adjustment factors and split ratios [IN1].
  - Nasdaq corporate-actions feed: not researched.
- **ETF holdings:**
  - Public source: Form N-PORT. Today only the quarter-end month is public, about 60 days after quarter end.
  - The 2024 amendments (monthly public N-PORT with a 60-day lag) were **delayed to 2027-11-17** (large fund groups) and 2028-05-18 (small) [NP1][NP2] **H**.
  - ETFs also publish daily holdings on issuer websites; those terms vary and were not researched.
  - Commercial sources: Finnhub All-In-One ETF holdings [F1]; ETF Global via Massive at $99/mo individual or contact sales for business [M2][M3].
- **Bonds:**
  - **FINRA TRACE:** real-time vendor feed $1,500/mo per data set. Professional display $60/user/data set, or $7,500/mo enterprise. **Non-pro real-time display is free**. Delayed data costs nothing in display fees but is not available directly from FINRA. A Vendor Agreement and monthly usage reporting are required [TR1][TR2][TR3] **H**.
  - **MSRB EMMA:** website terms forbid scraping or building databases from Content [MS1]. Subscription prices seen: Real-Time Transaction Data (RTRS) $11,000, Comprehensive Transaction $5,500, Continuing Disclosure $45,000, Primary Market $20,000 [MS2] **M** (2022 agreement PDF; the period (annual or otherwise) was not verified).
  - **Verdict: leave bonds out of the MVP.** The target users are equity/ETF investors, and bonds add a separate licensing stack plus five-figure MSRB fees.

---

## E. News licensing

| Source | Display to paying users? | Price | Conf. |
|---|---|---|---|
| Finnhub company-news | No, unless Finnhub gives written approval (see ToS, §A1) | not published | H |
| Marketaux | Only with approval (ToS "personal, non-commercial"). Returns snippet + link only | $0–$199/mo | H |
| **Benzinga direct** | Yes. The Stock News API "is built to be displayed on your platform … fully embed the entire story and image" [BZ1] | licensing@benzinga.com; not published | H |
| Benzinga Basic (free tier via AWS Marketplace) | Headline, teaser, and link to benzinga.com; subject to the vendor EULA [BZ2] | $0 | M |
| **Benzinga via Massive** | "Benzinga News Business" plan exists [BZ3]. The individual add-on is individual use only | $99/mo per dataset (individual); business "Contact for pricing" [M2][M3] | M |
| Intrinio NewsEdge | Licensing labelled "Business Use" [IN1] | on Startup/Enterprise | M |
| Tiingo News | Internal use unless licensed for redistribution [TI1] | not verified | L |
| SEC EDGAR filings (8-K, Forms 3/4/5) | Yes. Public information [SEC3] | $0 | H |

**Practical rule:** without a display license, show only a headline, source, timestamp, and link, plus *your own* generated summary. Whether an LLM-written summary of licensed article text counts as "derived data" under the vendor's terms is **not verified**; ask the vendor in writing.

---

## F. Google Gemini

- **`gemini-1.5-flash`:** retired.
  - `gemini-1.5-flash-002` retired 2025-09-24; `-001` retired 2025-05-24 [G1] **H** (Vertex lifecycle table).
  - The Gemini API deprecations page no longer lists 1.5 at all [G2].
  - Developers report `404 models/gemini-1.5-flash is not found` [G3] **M**.
- **SDK:** `google-generativeai` is deprecated and its repo is archived. "All support for this repository ended permanently on November 30, 2025." Use `google-genai` [G4] **H**.
- **Current flash-tier models:** `gemini-3.8-flash` (2026-09-02), `gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite` (shutdown 2027-05-07), `gemini-2.5-flash`, and `gemini-2.5-flash-lite` [G2] **H**.
  - `gemini-2.0-flash` shut down 2026-06-01.
- **Paid-tier prices per 1M tokens (input / output):**

  | Model | Input | Output | Conf. |
  |---|---|---|---|
  | `gemini-3.8-flash` and `gemini-3.7-flash` | $0.75 | $3.75 (through 2026-12-31; $1.50 / $7.50 from 2027-01-01) | H |
  | `gemini-3.6-flash` | $0.75 | $3.75 (same promo, then $1.50 / $7.50) | M |
  | `gemini-3.5-flash` | $1.50 | $9.00 | M |
  | `gemini-3.5-flash-lite` | $0.30 | $2.50 | M |
  | `gemini-3.1-flash-lite` | $0.25 | $1.50 | M |
  | `gemini-2.5-flash-lite` | $0.10 | $0.40 | M |

  [G5]
- **Free tier:** content on the free tier is "used to improve our products". Paid-tier content is not [G5] **H**. **Do not send user or watchlist data on the free tier in production.**

---

## 2. Recommended data stack by stage

All costs are **estimates**. Exchange fees are monthly and use the 2026 schedules unless marked "CT Plan (from 2027-04-01)". Formulas are shown so you can re-run them.

### Stage 1 — Development, roughly $0–50/mo (no paying users; internal use only)

- **Prices and bars:**
  - Alpaca Basic ($0): IEX real-time plus historical bars since 2016; SIP bars older than 15 min. Internal use only.
  - Or Massive Stocks Basic ($0): end of day plus 2 years.
  - Or Massive Starter ($29): 15-min delayed plus WebSocket.
- **Filings and fundamentals:** SEC EDGAR data.sec.gov ($0). Set a User-Agent and stay at or under 10 requests/s.
- **Symbology:** OpenFIGI ($0).
- **Macro:** FRED ($0, public-domain series only).
- **News for development:** Marketaux free or Finnhub free, internal only.
- **LLM:** Gemini paid tier using `gemini-2.5-flash-lite` or `gemini-3.5-flash-lite` via the `google-genai` SDK. Expect pennies to a few dollars at dev volumes.
- **Remove:** yfinance and Alpha Vantage `outputsize=full` (premium only).
- **Estimate:** $0 to about $29 + $20 ≈ **$0–50/mo**.
- **Caveat:** Massive Basic/Starter and Alpaca Basic are "individual" or "personal/non-commercial" use. A company building a commercial product on them is arguably already commercial use, even during development.

### Stage 2 — Paid pilot, 50–200 non-professional users

**Option P1 (recommended): delayed, full-volume data plus fee-free real-time indications**

- **Delayed (15 min) quotes and bars with display rights:**
  - Intrinio Startup: $333/mo for months 1–6, $666 for months 7–12, then $999. Includes commercial display rights, Cboe One 15-min delayed, FMV real-time, EOD 50+ yrs, and fundamentals.
  - Or Twelve Data Venture: $499/mo; exchange-fee inclusion **unverified**.
- **Full-volume daily bars for volume-move alerts:** Databento `EQUS.SUMMARY` (delayed intraday volume plus consolidated EOD, no license fees) on Standard at $199/mo. Display rights under Standard are **unverified**; if Standard doesn't cover display, use it only server-side for signals.
- **News:** show headline + link from EDGAR 8-K/RSS ($0), or license Benzinga (quote required).
- **Exchange fees:**
  - Delayed display carries no CTA/UTP display fees.
  - If you are the vendor of record for delayed UTP data: $250/mo delayed redistributor + $250/yr admin.
  - If your vendor is the redistributor under its own agreements, $0 to you. Which applies is **unverified**; ask the vendor.
- **Estimate:**
  - Low: $333 + $199 + (0 to $250) = **about $530–780/mo**.
  - Steady state (Intrinio at $999): **about $1,200–1,450/mo**.
  - Per-user fees: **$0** × users.

**UI rule for FMV/derived real-time** (Intrinio EquitiesEdge, Massive Business FMV, Databento Mini): label these prices "indicative"/"FMV", not "last trade". An alert fired on a modeled price can disagree with actual prints, which undermines an explainable alert.

**Option P2: real-time display using a fee-free derived feed**

- Databento US Equities Mini (live BBO and last sale, no per-user fees, non-display allowed) on Standard at $199. Plus is needed if Standard lacks external distribution; US-equities Plus pricing is **unverified** (CME Plus shows $1,750/mo).
- **Estimate:** $199 to about $2,000/mo, fixed. Per-user fee = $0.
- Alternative: Massive Stocks Business at **$2,499/mo** (FMV, no exchange fees).

**Option P3: true real-time exchange data (for comparison only)**

- **SIP real-time via a vendor, today:**
  - Redistributor fees: 3 × $1,000 = $3,000.
  - Indirect access (if you receive a manipulable feed): A $750 + $1,250, B $400 + $600, C not verified — about $3,000.
  - Non-display, if alerts run on this data: A $4,000 + B $2,000 — about $6,000 (C not verified).
  - Per-user: $1 × 3 tapes × N.
  - **At N = 200: about $12,000 + $600 ≈ $12.6k/mo, plus the vendor plan.**
- **Nasdaq Basic via Databento (a real-time alternative to SIP):**
  - Formula: ($2,140 external distributor + $0.50 per non-pro user on the Nasdaq-only line) × 1.029.
  - At 200 users: ≈ **$2.3k/mo** plus the Databento plan, plus Nasdaq non-display fees if alerts run on this data (not verified).
  - Figures come from Databento's table [DB1]. The $1,680 figure there is the internal-only distributor fee; the $2,140 external fee covers internal use too [NQ1]. The full three-market non-pro fee would be $1.00/user [NQ2].
- **Massive expansions:** Full Market real-time $1,999 plus pass-through exchange fees, possibly on top of the $2,499 base.
  - With base: ≈ **$4.5k/mo + fees**.
  - Delayed variant: $499 + $2,499 base ≈ **$3.0k/mo**, or **$499** if the base isn't required (unverified).

### Stage 3 — Growth, about 5,000 users (assume 10% professional as a sensitivity)

**Formulas.** N = 5,000; P = professional users; NP = non-professional users.

- **SIP real-time, today:** 3 × $1,000 + about $3,000 access + about $6,000 non-display + $3 × NP + ($45 + $23 + $24) × P.
  - Why $45: under CTA note 2, each external professional subscriber sets its own Tape A tier from its own device count. A solo pro-am user has 1–2 devices, which is the $45 tier.
  - P = 0: ≈ $12,000 + $15,000 = **$27,000/mo**.
  - P = 500: ≈ $12,000 + $13,500 + $46,000 = **$71,500/mo**.
- **SIP real-time under the CT Plan (from 2027-04-01):**
  - Per tape non-pro = $0.90 × 2,000 + $0.75 × (NP − 2,000).
  - P = 0: per tape $1,800 + $2,250 = $4,050; × 3 = $12,150.
  - Plus redistributor 3 × $1,155 = $3,465, plus access and non-display (not verified).
  - **≈ $15.6k/mo + access/non-display.**
  - Pro users add ($26 + $23 + $24) = $73 each: 500 pros ≈ **+$36.5k/mo**.
- **Nasdaq Basic (all three markets):** $2,140 (external, or external and internal, distributor) + $1.00 × NP + $28.50 × P. Nasdaq non-display fees are separate and **not verified**.
  - P = 0: ≈ **$7,140/mo**.
  - P = 500: ≈ $2,140 + $4,500 + $14,250 = **$20,890/mo**.
  - Alternative: the $1,500/mo Derived-Data-to-unlimited-non-pros option could cut this further for derived displays; applicability **unverified**.
- **Cboe One Summary:** $5,000 + $0.25 × NP + $10 × P + $1,000 consolidation.
  - P = 0: ≈ **$7,250/mo**.
  - P = 500: ≈ **$12,125/mo**.
- **Fee-free derived feed (Databento Mini, Massive Business FMV, or Intrinio Enterprise):** fixed. Roughly $2.5k–5k+/mo based on published entry prices; enterprise terms not verified.
- **Recommendation:**
  - Stay on **delayed full-volume data plus a fee-free derived real-time indication**.
  - Add a single real-time proprietary feed (Cboe One Summary or Nasdaq Basic) as a **paid upsell tier**, so per-user fees scale with revenue.
  - Model professional users explicitly, and gate the upsell behind a non-pro attestation.
- **LLM (estimate):**
  - Formula: 5,000 users × 20 alert explanations/day × 30 days = 3M calls/mo, at about 1,500 input and 300 output tokens per call.
  - `gemini-2.5-flash-lite`: 4.5B × $0.10/M + 0.9B × $0.40/M ≈ **$810/mo**.
  - `gemini-3.5-flash-lite`: ≈ $1,350 + $2,250 = **$3,600/mo**.
- **Filings, macro, symbology:** EDGAR, FRED (public series), and OpenFIGI remain $0. Consider an EDGAR bulk mirror to respect the 10 requests/s limit.

---

## 3. Could not be verified

1. The Finnhub docs "Premium" badge on `/stock/candle` (JS-rendered page). The inference comes from the pricing matrix only.
2. Finnhub commercial or redistribution pricing, which is not published.
3. Twelve Data Venture/Enterprise: whether US real-time exchange per-user fees are included, or whether separate exchange agreements are needed.
4. Databento US Equities: current Standard price (the $199 figure is from a Jan-2025 blog); whether Standard + Mini allows display to paying external users; Plus/Unlimited pricing for US equities.
5. Massive: whether expansions (Full Market Delayed $499, etc.) require the $2,499 Stocks Business base; whether "Business use" explicitly includes display to your customers; Benzinga business pricing.
6. Tiingo redistribution pricing. Sources conflict: $50 "internal commercial" per the pricing page, a blog calling it "commercial-use license", and a $250/$500 figure from a search summary.
7. Alpaca Broker API market-data terms for non-broker apps (probably not applicable).
8. UTP non-display and access fee amounts. How CTA non-display categories 1/2/3 stack for a SaaS alerting use case.
9. CT Plan final fee figures in Exhibit F of the approval order (34-105778). I used the Amended Fee Proposal numbers. CT Plan non-display and inflation-adjusted amounts beyond access and redistributor fees.
10. Who counts as the "Vendor" or redistributor (you or your upstream vendor) for delayed CTA/UTP display, and therefore whether you must sign the NYSE/UTP agreements yourself.
11. Cboe One fees are quoted from a Nasdaq SEC filing (Sep-2026), not from Cboe's own fee schedule.
12. Whether any competing consolidator under Rule 614 is operational. Whether odd-lot SIP dissemination went live on 2026-05-04.
13. Gemini prices other than 3.7/3.8-flash were read through a summarizer (M).
14. Whether LLM summaries of licensed news text count as permitted "derived data" under each news vendor's terms.
15. MSRB subscription fee period (annual vs. other) and whether the 2022 prices are current.
16. Marketaux commercial or redistribution pricing, which is not published.
17. Nasdaq non-display fees for Nasdaq Basic, and Nasdaq Last Sale non-pro per-user pricing. Also which product the tiered external-subscriber distributor table belongs to.

---

## Sources (all accessed 2026-09-24)

- [F1] https://finnhub.io/pricing (via rendered fetch)
- [F2] https://finnhub.io/terms-of-service
- [AV1] https://www.alphavantage.co/premium/
- [AV2] https://www.alphavantage.co/documentation/
- [AV3] https://www.alphavantage.co/terms_of_service/
- [TD1] https://twelvedata.com/pricing
- [TD2] https://twelvedata.com/pricing-business
- [MX1] https://www.marketaux.com/pricing
- [MX2] https://www.marketaux.com/faq
- [MX3] https://www.marketaux.com/tos
- [Y1] https://github.com/ranaroussi/yfinance
- [Y2] https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html
- [M1] https://massive.com/blog/polygon-is-now-massive (2025-10-30)
- [M2] https://massive.com/pricing
- [M3] https://massive.com/business
- [DB1] https://databento.com/docs/api-reference-live/basics/metered-pricing (2026 license fee table)
- [DB2] https://databento.com/blog/introducing-databento-us-equities (2025-01-13)
- [DB3] https://databento.com/blog/databento-us-equities-mini-now-available (2025-02-01)
- [DB4] https://databento.com/pricing
- [DB5] https://databento.com/blog/migrating-from-iex-cloud-to-databento (2024-06-28)
- [AL1] https://docs.alpaca.markets/docs/about-market-data-api
- [AL2] https://alpaca.markets/data
- [AL3] https://alpaca.markets/support/redistribute-alpaca-api
- [AL4] https://files.alpaca.markets/disclosures/library/TermsAndConditions.pdf
- [TI1] https://www.tiingo.com/about/pricing
- [TI2] https://www.tiingo.com/blog/iex-cloud-alternatives/ (updated 2026-07-23)
- [EO1] https://eodhd.com/pricing
- [EO2] https://eodhd.com/financial-apis/terms-conditions
- [EO2b] https://eodhd.com/financial-apis/commercial-vs-personal-license-use
- [IN1] https://intrinio.com/pricing
- [IEX1] https://www.iex.io/resources/trading/fee-schedule
- [IX1] https://www.waterstechnology.com/trading-tech/7951983/ (2024-08-30)
- [IX2] https://www.integrity-research.com/iex-cloud-shuttered-though-former-execs-acquire-assets/ (2024-09-16)
- [NQ1] https://www.nasdaqtrader.com/content/ProductsServices/PriceList/Nasdaq_US_Equities_Price_List_2025_2026_2027.pdf
- [NQ2] https://www.federalregister.gov/documents/2026/09/16/2026-18932/ (Nasdaq Basic Plus / TotalView Plus fee filing; includes Cboe One and NYSE BQT comparisons)
- [CTA1] https://www.ctaplan.com/publicdocs/ctaplan/Schedule_of_Market_Data_Charges.pdf (text extracted)
- [CTA2] https://www.ctaplan.com/publicdocs/ctaplan/Policy_Delayed_Market_Data.pdf
- [CTA3] https://www.sec.gov/files/rules/sro/nms/2026/34-105779.pdf (2026-06-26)
- [UTP1] https://www.utpplan.com/doc/DataPolicies.pdf
- [CT1] https://www.sec.gov/files/rules/sro/nms/2026/34-105778.pdf (2026-06-26); FR notice 2026-07-01
- [CT2] https://consolidatedtape.com/
- [CT3] https://www.sec.gov/files/rules/sro/nms/2025/34-104512.pdf (2025-12-23)
- [CT4] https://www.govinfo.gov/content/pkg/FR-2026-04-03/html/2026-06463.htm (Rel. 34-105125)
- [RL1] https://www.sec.gov/files/rules/sro/finra/2025/34-104441.pdf
- [RL2] https://www.sidley.com/en/insights/newsupdates/2024/10/sec-adopts-rules-modifying-minimum-pricing-increments-access-fee-caps-and-order-transparency
- [RL3] https://www.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-28
- [MDI1] https://www.law.cornell.edu/cfr/text/17/242.614
- [NMS1] https://www.sec.gov/newsroom/press-releases/2026-54-sec-proposes-rescission-regulation-nms-rules-611-610e
- [SEC1] https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- [SEC2] https://www.sec.gov/os/accessing-edgar-data
- [SEC3] https://www.sec.gov/about/privacy-information (Website Dissemination)
- [FR1] https://fred.stlouisfed.org/docs/api/terms_of_use.html
- [OF1] https://www.openfigi.com/api/documentation
- [NP1] https://www.sec.gov/rules-regulations/2025/04/s7-26-22
- [NP2] https://www.sec.gov/files/rules/final/2025/ic-35538.pdf
- [TR1] https://www.finra.org/filing-reporting/trace/pricing
- [TR2] https://www.finra.org/rules-guidance/rulebooks/finra-rules/7730
- [TR3] https://www.finra.org/filing-reporting/trace/content-licensing/real-time-end-day-market-data-agreements
- [MS1] https://www.msrb.org/Municipal-Securities-Rulemaking-Boards-Website-Terms-Use
- [MS2] https://www.msrb.org/sites/default/files/2022-09/Subscription-Service-Agreement.pdf
- [BZ1] https://www.benzinga.com/apis/cloud-product/stock-news-api/
- [BZ2] https://aws.amazon.com/marketplace/pp/prodview-xwgvhwowjmw3g
- [BZ3] https://massive.com/docs/rest/partners/benzinga/news
- [G1] https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions
- [G2] https://ai.google.dev/gemini-api/docs/deprecations
- [G3] https://stackoverflow.com/questions/79779187/ (2025-10-24)
- [G4] https://github.com/google-gemini/deprecated-generative-ai-python
- [G5] https://ai.google.dev/gemini-api/docs/pricing
