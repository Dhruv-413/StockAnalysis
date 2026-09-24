# India market data, broker APIs and SEBI posture: research notes

> **Corrections (2026-09-24, achievability round; see [17](../17-what-is-achievable.md)):**
> - **Real-time on a free-to-user app** costs **₹21L/yr fixed** (NSE 2021 sheet), charged per medium. "NIL" refers to the variable per-user fee only ([data-stack-costs §5](data-stack-costs.md)).
> - The **15-min delayed fee is annual**: ₹80,000 per segment on the 2022 sheet. The current (2026) value is unknown.
> - **Indices are a separate licence**: real-time is ₹3L/yr + ₹200 per user per month (2021 sheet).
> - **Education data lag:** SEBI replaced the 3-month condition with a **30-day lag from 2026-07-01** (circular of 8 May 2026). The lag defines "solely education" status under the association rules. It is not a general ban on price display ([feature-legality](feature-legality.md)).

> **Corrections (2026-09-24, research round 3; see [16](../16-india-research-round-3.md)):**
> - **Kite display.** No source confirms that a Kite Connect platform may show Kite data, even per user and even after approval. The only direct Zerodha staff statement says a third-party app cannot show Kite data ([kite-and-broker-apis §2](kite-and-broker-apis.md)). Read any "same-user display under platform approval" line below as **unconfirmed**.
> - **Hosted Kite MCP** is free to users and includes quotes and historical data (Zerodha, 2025-05-20). It has no place, modify or cancel order tools, but it does have GTT, so it is **not strictly read-only**.
> - **Broker API table.** Groww costs ₹499/mo (early bird) or ₹2,000/mo (standard). Upstox staff say it provides "no market data for commercial purposes". Fyers' terms bar using its data to build "charting, technical tools".
> - **Static-IP rule** (SEBI retail algo framework): covers order endpoints only. Read-only use still needs a per-user login with 2FA and a daily re-login.

Research date: 2026-09-24. Author role: Market-Data Researcher. Nothing in this file is legal advice. Every claim is labelled:
- **[F]** verified fact from a primary source;
- **[F-sec]** fact taken from a secondary source or a search summary, because the primary page timed out or returned only headers;
- **[I]** inference;
- **[A]** assumption;
- **[E]** estimate;
- **[P]** proposal.

Confidence is H, M or L. All access dates are 2026-09-24 unless stated otherwise.

NSE web properties (nseindia.com, and nsearchives for the 2025 and 2026 tariff PDFs) timed out repeatedly from this environment. The NSE tariff numbers below therefore come partly from search-result extracts. They are marked M and must be re-read from the PDFs before anyone relies on them.

---

## 0. Headline findings

1. **[F, H] Broker APIs are execution suites, not data licences.** Zerodha's own support page says: "No, you cannot display data from Kite Connect APIs on other platforms, as this violates the exchange's data vending policies... Kite Connect API is primarily an execution suite, not a data vending service." The same page tells anyone who needs to distribute data to use an exchange-authorised data vendor. Kite terms also forbid displaying live data "to the public at large" and forbid building "databases... or keep cached copies with the intent of redistributing". Multi-user login is available only to "exchange approved platforms" such as smallcase and Streak.
   - **[I, M]** "Use each user's own broker session" is therefore legitimate only as a per-user, same-user display, and only under a platform/partner approval from each broker.
   - You cannot pool those sessions into a shared cache. That rules them out as the backbone for a 100k-user, ~300 ms product.
   - **[I, H] The scalable path is one licensed central feed (vendor + NSE/BSE licence) plus your own cache.**
2. **[F-sec, M] Choosing a licence category decides the cost.** NSE's per-user display route is a ₹24 lakh fixed fee per segment per year plus ₹820–1,075 per user per month. The "open website" route is ₹27.5 lakh a year flat. "Free-to-user mobile app" is reportedly NIL on top of a base licence. See §1.3.
   - The most important question for NSE is which category a login-gated, free or freemium AI assistant falls into (§7, Q-NSE-1).
3. **[F-sec, M] Education is not a usable safe harbour for a live assistant.** SEBI's circular of 8 May 2026 (effective 1 July 2026) sets a uniform **30-day lag** for sharing and using price data in investor education. It supersedes the Jan 2025 "three-month" rule and the May 2024 "one-day" rule.
4. **[F-sec, H] Being free does not exempt you from RA registration.** The RA definition counts "consideration" as "any form of economic benefit including non-cash benefit, received or receivable, directly or indirectly... from client or otherwise". Ad-supported or freemium models therefore count.
   - There are two viable postures: (a) strictly information-only, or (b) SEBI-registered RA, or partnership with one (§3.6).
5. **[F-sec, H] Reg 16A of the Intermediaries Regulations (Aug 2024)** bars brokers and other regulated entities from associating with unregistered persons who give advice or recommendations, or who make return or performance claims.
   - **[I, H]** Your advice posture therefore decides whether any broker partnership (Zerodha, Upstox, Angel One and others) is possible at all.
6. **[I, H] India has no consolidated tape (no source cited).** For the detector spec in `06-quantitative-validation.md` §1 (consolidated, full-volume, 1-minute, displayable), "consolidated" means NSE + BSE.
   - **[I, M]** NSE-only is a close proxy for most liquid cash-equity names. BSE's share of cash volume was not verified here.
   - **[I, H]** A 1-second snapshot feed (GFDL "1 second frequency") is not full-volume tick data. Volume can be reconstructed from cumulative-volume fields, but every trade is not guaranteed. Validate before use.

---

## 1. Exchange data licensing (NSE, BSE)

### 1.1 Regulatory overlay: SEBI circular of 24 May 2024 on real-time price data
- **[F-sec, M]** Circular SEBI/HO/MRD/MRD-PoD-3/P/CIR/2024/56, 24 May 2024, effective about 23 June 2024. It bars market infrastructure institutions (MIIs) and registered intermediaries from sharing real-time price data with third parties except where needed for orderly market functioning or regulatory compliance. It targets gaming, fantasy and virtual-trading platforms.
  - Sources: https://www.sebi.gov.in/legal/circulars/may-2024/norms-for-sharing-of-real-time-price-data-to-third-parties_83572.html (the page returned only headers); https://www.truedata.in/blog/sebi-norms-on-sharing-real-time-price-data (TrueData says it "do[es] not support any kind of Gaming / Virtual trading / Simulation usage").
  - **[I, M]** Authorised data vendors keep selling real-time data for trading and analytics. Paper-trading or "virtual portfolio" features in the assistant would put the vendor contract at risk.
- **[F-sec, M]** SEBI circular HO/47/17/12(11)2025-MRD-POD3/I/11107/2026, 8 May 2026, effective 1 July 2026. It sets a 30-day lag for sharing and using price data in investor education and awareness. Data-sharing agreements must keep an audit trail. NISM is the only exception (1-day lag, simulation lab).
  - Sources: https://www.corplawupdates.in/updates/sebi-30-day-lag-educational-price-data-norms-2026 ; https://www.outlookmoney.com/invest/sebi-revises-norms-for-sharing-and-usage-of-price-data-for-educational-purposes ; consultation background at https://www.theweek.in/news/biz-tech/2026/01/07/sebi-mulls-30-day-lag-on-sharing-stock-market-data-for-investor-education-here-is-why.html (pub 2026-01-07).

### 1.2 NSE Data & Analytics policies
- **[F, H] Non-display policy** (primary PDF read in full): https://archives.nseindia.com/content/press/Non_display.pdf
  - Non-display means "use of real time NSE market data as part of automated calculations or algorithms to support trading decision making processes... If the real time NSE data is used for deriving any value (Derived Data) for internal analysis, it will also fall under the non-display policy."
  - Derived Data is data processed "in such a way that the underlying market data cannot be identified, recreated or re-engineered".
  - A data vendor's clients must sign directly with NSE Data & Analytics. NSE "reserves the right to request... Data vendors to stop supplying" clients who do not.
  - Enterprise fee (per legal entity, per segment, per year, from 1 Jan 2016): Level 1 CM ₹18,00,000; Level 2 CM ₹25,00,000; Level 1 F&O ₹18,00,000; Level 2 F&O ₹25,00,000. Global (group) fee: Level 1 CM ₹28,00,000. All exclusive of taxes.
  - The annexure is dated 2014/2016 and may have been superseded by the March 2026 pricing file, which timed out: https://nsearchives.nseindia.com/web/mediaattachment/2026-03/NSE_Pricing_file_-_Domestic_clients_20260309171343.pdf. **Confidence that these are the current prices: M.**
  - **[I, M]** Real-time indicators, sentiment-plus-price scores, alert triggers and AI summaries computed from real-time NSE data meet the "derived data for internal analysis" wording. That makes a non-display fee likely on top of display fees. Ask NSE (Q-NSE-3).
- **[F, H] 15-minute delayed data tariff** (primary PDF read): https://archives.nseindia.com/content/press/Snapshot_15_delayed_data.pdf
  - CM ₹60,000; F&O ₹60,000; CDS ₹60,000 (domestic, INR). The billing period is **not stated** on the sheet. [A] It is probably annual; verify.
  - The fee is "per medium of data display... website and mobile app are considered two different mediums and charged separately."
  - Real-time vendors may show 15-minute-plus delayed data "on their proprietary terminal/software without any additional fees for display usage only". A feed of delayed data to the vendor's clients needs "written consent from NSE Data & Analytics".
  - The same fee applies to any delay of 15 minutes or more.
- **[F-sec, M] Real-time tariff for domestic vendors, effective 1 Apr 2025.** Source: https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Real_Time_Tariff_Domestic_01042025_.pdf. The PDF timed out; the numbers below come from the search extract.
  - Terminal, CM Level 1: ₹24,00,000 per year fixed, plus ₹1,075 per month per domestic end user (₹1,775 international).
  - Terminal, F&O: ₹24,00,000 per year, plus ₹1,100 per month domestic.
  - Software/charting, CM: ₹24,00,000 per year, plus ₹820 per month domestic. F&O: ₹24,00,000 per year, plus ₹825 per month.
  - Mobile app: 10% revenue share, minimum ₹11.5 lakh a year, for paid-user apps; **NIL for free-to-user apps**.
  - Open website: ₹27,50,000 per year fixed, no variable fee.
  - **Conflict:** the 1 Apr 2023 tariff extract (https://nsearchives.nseindia.com/s3fs-public/inline-files/Download_Real_Time_Tariff_Domestic_01042023.pdf) says **20%** revenue share. It also says mobile apps are "not available on a standalone basis", only as an add-on to a terminal or software licence. If that clause is still in force, the ₹24 lakh base applies even to a mobile-only product. **Unresolved; confidence M/L.**
- **[F, H] Authorised real-time vendor list** (undated archive PDF): https://archives.nseindia.com/content/press/List_data_Vendors.pdf
  - The 37 real-time vendors include Accelpix (CM, F&O), Global Financial Datafeeds LLP (CM, F&O, CD), TrueData (CM, F&O, CD), TradingView Inc (CM, F&O), RKSV/Upstox (CM, F&O, CD), Google India, Yahoo India, Refinitiv, Bloomberg and ICE.
  - There are six "1-minute snapshot" vendors, including Icharts and Proseon.
  - The list is undated, so it may be stale. Confidence M.
- **[F, H] NSE's non-display policy says** that "applications... that solely facilitate display or redistribution" are priced under the regular price lists, not the non-display policy.
- **[F-sec, M] The NSE website Terms of Use** (https://www.nseindia.com/static/nse-terms-of-use; page timed out) prohibit "systematic or automated data collection activities including scraping, data mining, data extraction and data harvesting" without written consent.
  - **[P]** Do not scrape nseindia.com or bseindia.com in any phase, including for corporate announcements, bulk/block deals, option chains and shareholding.

### 1.3 Cost formulas for NSE display licensing [E, all figures M, excl. GST, per segment]
Let N be the number of entitled real-time users and S the number of segments (CM, F&O).
- **Per-user software route:** `S × (₹24,00,000 + N × ₹820 × 12)` per year.
  - N = 1,000 → CM only ≈ ₹24 L + ₹98.4 L = **≈ ₹1.22 Cr per year**.
  - N = 100,000 → CM only ≈ **₹98.6 Cr per year**. Not viable.
- **Open-website route:** `S × ₹27,50,000` per year flat. Break-even against the per-user route is about 36 users (₹3.5 L ÷ ₹9,840).
- **Free-to-user mobile app:** `₹0` variable. If "not standalone" holds, add a base licence (`₹24 L` per segment).
- **Paid app:** `max(₹11.5 L, 10% or 20% × net revenue)`.
- **Non-display (derived analytics):** add `₹18 L` per segment per year (Enterprise, 2016 annexure).
- **Delayed-only (15 min):** `₹60,000 × S × mediums` (website and app counted separately; period unverified).
- **Vendor fee:** add the vendor's quoted price. GFDL says going through a vendor can reduce the cost by about 20% compared with going direct, but "you still need to get a data vending agreement with NSE" (https://www.marketcalls.in/datafeed/get-to-know-about-datafeed-vendors-and-which-data-vendors-to-use.html, secondary, M).

### 1.4 BSE
- **[F-sec, M]** BSE publishes a domestic information-products tariff: https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf. It was not retrieved in this pass.
- **[F-sec, M]** The BSE announcement of 29 June 2026 says BSE will license **international** clients directly from 1 Jan 2027, ending the Deutsche Börse arrangement; nothing changes for domestic clients. Sources: https://www.freepressjournal.in/business/bse-to-directly-license-market-data-products-for-international-clients-from-january-2027 ; Business Standard returned 403.
- Search results mixed in the Budapest Stock Exchange (bse.hu). Those were discarded.

---

## 2. Broker APIs

| Broker | API cost (as found) | Market data via API | Historical | Source(s) | Conf. |
|---|---|---|---|---|---|
| Zerodha Kite Connect | Connect ₹500/mo per API key; Personal free (no market data) | WebSocket streaming in Connect | Included in Connect since Feb 2025 | https://zerodha.com/products/api/ ; https://kite.trade/forum/discussion/14868/introducing-kite-connect-personal-apis-free-apis-for-personal-use | H |
| Zerodha Kite MCP | Free | Hosted `mcp.kite.trade` is read-only, with GTT the only write; self-hosted with your own key gives full tools (orders, historical); MIT licence; maintained by Zerodha | Self-hosted only | https://github.com/zerodha/kite-mcp-server ; https://zerodha.com/z-connect/featured/connect-your-zerodha-account-to-ai-assistants-with-kite-mcp (pub 2025-05-20) | H |
| Upstox | "₹0" trading and market-data APIs; ₹10/order offer "valid till 30th September 2026" (not GTT); 50 req/s | WebSocket V3 (up to 5 connections per user on Upstox Plus) | V3 candles, custom intervals | https://upstox.com/trading-api/ ; https://upstox.com/developer/api-documentation/v3/get-market-data-feed/ | M (the search summary tied the 30 Sep date to API access; the fetched page ties it to the order offer) |
| Angel One SmartAPI | Free (trading, WebSocket, historical) | WebSocket | "Decades" of NSE equity candles | https://www.angelone.in/knowledge-center/smartapi/detailed-introduction-to-smartapi ; April 2026 changes: https://www.angelone.in/news/market-updates/what-s-changing-in-angel-one-s-smartapi-access-from-april-1-2026 | M |
| Dhan (DhanHQ) | Trading APIs free; **Data API ₹499/mo + tax** | Live market feed | Unverified depth | https://dhan.co/support/platforms/dhanhq-api/how-does-the-dhanhq-data-api-subscription-work/ ; https://dhanhq.co/trading-apis | M |
| Fyers API v3 | Data free ("absolutely zero fees") | Data socket up to 5,000 symbols; separate depth socket | Yes | https://support.fyers.in/portal/en/kb/articles/do-i-need-to-pay-for-datafeeds | M |
| ICICI Breeze | Free ("no cost or fees... API or the data") | WebSocket OHLC | 3 years of second-level LTP (secondary) | https://www.icicidirect.com/faqs/fno/what-is-the-cost-or-fees-for-using-breeze-api | M |
| Kotak Neo Trade API | Free "at present"; zero API brokerage on Trade Free plans from 1 Nov 2025 | Yes | Unverified | https://www.kotakneo.com/support/is-neo-trade-api-free-of-cost/ | M |
| Groww Trade API | ₹499/mo + tax (page also shows ₹2,000 "early bird"; conflict unresolved) | LTP, quote, OHLC | Up to 3 months of candles | https://groww.in/trade-api | M |
| 5paisa | Not researched this pass | — | — | — | — |

**Terms that matter for an AI assistant**
- **[F, H]** Kite terms (https://kite.trade/terms/, no last-updated date shown):
  - live data "cannot be displayed to the public at large";
  - no reverse engineering or "deriv[ing] the composition" of the data;
  - no virtual/mock trading or games;
  - no scraping, databases or cached copies "with the intent of redistributing";
  - redistribution leads to termination.
  - Multi-user apps need approved-platform status (forum: https://kite.trade/forum/discussion/5961/kite-connect-multiple-user).
- **[F, H]** Support page: https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/can-i-use-historical-and-live-data-taken-from-kite-connect-api-on-other-platforms
- **[I, M]** Other brokers' data terms were not found in primary form. Assume the same exchange-driven restriction applies to all of them. This is unverified and each needs a vendor question.
- **[I, H]** Kite MCP is a per-user tool: the user's own Claude, Cursor or similar client talks to Zerodha. It is not a backend your app can call on a user's behalf. [Unverified] How the hosted MCP serves quotes when the free Personal tier has no market data.

**SEBI retail algo framework** (circular of 4 Feb 2025: https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html; the page returned headers only, so details are F-sec, M)
- Brokers act as principal. Algo providers must be **empanelled with the exchange** and act as the broker's agents.
- Open APIs are prohibited. Access is by vendor/client-specific API key and whitelisted **static IP**, with OAuth and 2FA.
- Above **10 orders per second** per exchange, the algo must be registered and gets a unique ID.
- **Black-box algos require the provider to be SEBI-registered as an RA.**
- Timeline: originally 1 Aug 2025; extended to 1 Oct 2025, then a glide path (circular of 30 Sep 2025, https://www.sebi.gov.in/legal/circulars/sep-2025/extension-of-timeline-for-implementation-of-sebi-circular-dated-february-04-2025-on-safer-participation-of-retail-investors-in-algorithmic-trading-_96979.html); **mandatory for all brokers from 1 Apr 2026**.
- Broker implementations as found:
  - Upstox: static IP for order endpoints only; data endpoints are "not restricted by Static IP"; IP change allowed once a week (https://upstox.com/developer/api-documentation/announcements/algo-trading-circular/).
  - Angel One: market and IOC orders are banned for algos; strategies are hosted on the broker's servers unless the client self-hosts with a static IP.
- **[I, H]** An assistant that places or automates orders for users is an algo provider. It needs exchange empanelment, per-user static-IP handling, and RA registration if the logic is black-box. **[P]** No order placement through the pilot.

---

## 3. SEBI regulation affecting the assistant

1. **RA Regulations 2014, as amended 16 Dec 2024 (Third Amendment)** (https://www.sebi.gov.in/legal/regulations/dec-2024/securities-and-exchange-board-of-india-research-analysts-third-amendment-regulations-2024_89979.html) [F-sec, H]
   - "research analyst means a person who, for consideration, is engaged in the business of providing research services". "Consideration" includes any economic benefit, including non-cash, "from client or otherwise".
   - Registered RAs must disclose the extent of AI tool use to clients and remain fully responsible for AI output and data security.
   - Reg 19(vii) is cited in secondary sources (M).
   - A matching disclosure duty applies to Investment Advisers (IA) under the Dec 2024 IA amendment.
2. **Exclusions from "research report"** [F-sec, M]: general market trends; economic, political or market commentary; broad-based index discussion; statistical summaries of corporate financials; and technical analysis across sectors or indices. See also the SEBI RA FAQs of 23 Jul 2025 (https://taxguru.in/sebi/comprehensive-analysis-sebi-s-faqs-research-analysts.html).
   - **[I, M]** Stock-specific views, rankings, buy/sell/hold, target prices or "signals" are research or recommendations.
   - Anything tailored to the user's own portfolio or risk moves toward **investment advice** (IA Regulations 2013), which matters for any Kite-MCP-style holdings analysis.
3. **Intermediaries (Amendment) Regulations, Aug 2024, Reg 16A** [F-sec, H] (https://www.sebi.gov.in/legal/regulations/aug-2024/securities-and-exchange-board-of-india-intermediaries-amendment-regulations-2024_86338.html)
   - Regulated entities must not associate directly or indirectly with persons giving unregistered advice or recommendations, or making return or performance claims.
   - The Specified Digital Platform safe harbour is optional (SEBI press release 31/2024, 4 Dec 2024).
4. **Intermediaries (Amendment) Regulations, 10 Feb 2025 (Reg 16C)** [F-sec, M]: regulated entities using AI/ML, in-house or third-party, are solely responsible for data privacy and for AI output.
   - The consultation on AI/ML guidelines (20 Jun 2025) proposes governance, testing, disclosure and bias controls (https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html).
   - Final guidelines as of 2026-09 were **not verified**.
   - **[I, H]** If your broker partner is the regulated entity, it carries this liability and will push obligations down to you by contract.
5. **Finfluencer and education rules** [F-sec, M]: the circular of 29 Jan 2025 (three-month lag, bar on association) has been **superseded on the lag point** by the circular of 8 May 2026 (30-day lag, effective 1 Jul 2026). SEBI enforcement treats buy/sell calls labelled "education" as advice (Avdhoot Sathe order, Dec 2025, ₹546 Cr disgorgement; secondary).
6. **[P] Posture options**
   - **A. Information-only (unregistered).** Show:
     - licensed prices;
     - factual computed values (returns, RVOL, indicator values with their formulas);
     - verbatim or summarised filings, corporate actions, and bulk/block deal records;
     - news with sentiment labelled as a model output about text, not about price.
   - Posture A must never show buy/sell/hold, targets, stop-losses, "top picks", rankings framed as attractiveness, strategy signals, personalised suitability, or performance claims.
   - Posture A needs guardrails at the LLM output layer (refusal templates), logged outputs, and a disclaimer. It **cannot** partner with brokers in any way that looks like an association with an advice-giver, and must not place orders.
   - **B. Registered.** Register as an RA (body corporate; NISM certification, net worth and compliance-officer requirements not checked in this pass), or embed a registered RA as the accountable party. Then follow AI disclosure, record-keeping and fee rules. Order placement additionally needs algo-provider empanelment via each broker.
   - **[P] Recommendation:** Posture A for the prototype and pilot. Decide on B before scale if stock-specific opinions are core to the value. Get an Indian securities lawyer to review both before launch.
7. **DPDP Act 2023 and DPDP Rules 2025** [F-sec, M]: the rules were notified on 13/14 Nov 2025 and phase in over 18 months.
   - The Data Protection Board provisions are live now.
   - Consent-manager provisions take effect about 13 Nov 2026.
   - Full obligations (notice, consent, security safeguards, breach notification, erasure) apply from about **13 May 2027**.
   - Source: https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf
   - **[I, H]** Broker-linked holdings and positions are personal data. Store the minimum, keep tokens encrypted, and delete on disconnect.

---

## 4. Corporate and F&O data (announcements, bulk/block deals, SAST/PIT, shareholding, OI, option chain)
- **[F-sec, M]** NSE and BSE publish all of these on their websites, but NSE's ToS forbids automated collection. There is **no public official API** for them.
- NSE Data & Analytics sells "Corporate Data" products; price not retrieved.
- TrueData advertises Corporate Announcement, Corporate Data, Mutual Fund and News APIs (https://www.truedata.in/market-data-apis). GFDL advertises Option Chain and Exchange Snapshot APIs (https://globaldatafeeds.in/apis/). Accord Fintech (ACE) is also an authorised vendor for corporate data (https://www.accordfintech.com/market-data-feed).
- Prices, latency (time from exchange dissemination to API delivery) and display/redistribution rights are **unverified** for all of these. See the questions in §7.
- OI and option chain are part of the F&O real-time feed, so they fall under the F&O licence segment. Budget S = 2 (CM + F&O) if they are shown.

## 5. US/global data for Indian LRS users
- **[F-sec, M]** Vested holds US assets at DriveWealth (FINRA/SIPC). INDmoney runs a GIFT City (IFSCA) route (https://vested.blog/posts/vested-finance-review-2026, vendor-authored, L/M).
- The data needs are the same as the US product. Reuse the US vendor analysis in `04-real-time-data-strategy.md` §6 and `research/market-data.md`. Indian residents viewing US data are still counted as users and pro/non-pro status is judged under US exchange rules.
- **[Unverified]** Whether Vested or INDmoney expose any partner API. Not researched further.

## 6. Check against the detector spec (`06-quantitative-validation.md` §1)
Spec: consolidated (all-venue), full-volume, 1-minute OHLCV, trade-based timestamps, displayable to paying users; may be 15-minute delayed. For India, read "consolidated" as NSE + BSE and change the benchmark from SPY to NIFTY 50 plus a sector index.

| Feed | Venues | Granularity | Full volume? | Displayable to your users? | Meets spec? |
|---|---|---|---|---|---|
| Broker APIs (Kite, Upstox, Angel, Fyers, Dhan, Breeze) | NSE + BSE per instrument (no merged tape) | Ticks/WS + minute candles | Yes per venue | **No** except to the same logged-in user under an approved-platform arrangement | Per-user only; not as a central feed |
| TrueData API | NSE, BSE, MCX | Tick + 1-min (claimed) | Likely [A] | Only with a vendor licence + NSE agreement (unverified) | **Candidate**, pending Q-TD |
| GFDL API | NSE, BSE, MCX | **1-second snapshots**, tick/min historical | Snapshot, not every trade [I] | Unverified | Candidate for bars if 1-min history is exchange-derived; validate |
| Accelpix | NSE CM/F&O (+BSE claimed) | Real-time + IEOD | Unverified | Unverified | Unknown |
| NSE direct 15-min delayed snapshot | NSE only | 1-min snapshot files, 15-min delay (FTP) | Snapshot, not every trade [I] | Yes, ₹60k per medium per segment | Candidate: meets only if the files carry per-minute OHLC and exact cumulative volume; unverified (Q-NSE-4) |
| Scraped NSE/BSE web data | — | — | — | **Prohibited by ToS** | No |

---

## 7. Open vendor questions (exact text; for the user to send; answers not guessed)

**NSE Data & Analytics (marketdata@nse.co.in)**
- Q-NSE-1: "We are building an AI market-information assistant for retail users in India, delivered as a login-gated web app and mobile app. It is free at launch and may add a paid tier later. Which tariff category applies: software/charting application (per-user), open website, or mobile application (free-to-user / paid)? Does a login wall change the category?"
- Q-NSE-2: "Your real-time tariff lists a mobile-app revenue share, and an earlier sheet says mobile apps are not available on a standalone basis. Is a mobile-only licence available under the tariff effective 1 April 2025 or later? If not, which base licence is required? Please confirm the current revenue-share percentage and annual minimum."
- Q-NSE-3: "If we compute indicators, alert triggers, sentiment-adjusted scores and AI-generated text summaries from real-time NSE data and show the results to end users, is that non-display usage requiring the Enterprise non-display fee, derived-data redistribution under a separate agreement, or covered by the display licence? Please confirm current non-display fees; is the 2016 annexure still current?"
- Q-NSE-4: "Is the ₹60,000 fee for 15-minute delayed data per year or per month? Does it cover display on one website of unlimited users? Do we need a separate licence for derived data computed from delayed data? Do the 1-minute snapshot files carry per-minute open, high, low, close and exact cumulative traded volume for every symbol?"
- Q-NSE-5: "What are the storage and retention rules: may we store real-time or delayed ticks and 1-minute bars indefinitely for historical charts shown to our users? May users export CSVs of prices or derived values? Are exports treated as redistribution?"
- Q-NSE-6: "Is there a licensed feed for corporate announcements, bulk/block deals, SAST/PIT disclosures and shareholding patterns? What are its price, latency from dissemination, and display rights?"
- Q-NSE-7: "Please send the current list of authorised real-time and snapshot data vendors, and the current domestic pricing file (March 2026)."

**TrueData / Global Datafeeds / Accelpix (each)**
- Q-V-1: "Does your API licence permit us to display your real-time or delayed NSE/BSE data to our own end users in a third-party web or mobile app, or only for internal use or your own terminal? Which exchange agreements must we sign directly?"
- Q-V-2: "What are your API prices for (a) development/internal use, (b) display to up to 1,000 users, (c) display to 100,000 users, split into your fee and pass-through exchange fees?"
- Q-V-3: "What is the typical and p99 latency from exchange to your WebSocket in Mumbai? Is your real-time feed every trade (tick-by-tick), or snapshots at a fixed interval? Are 1-minute bars built from all trades, with full volume?"
- Q-V-4: "How much historical depth do you provide for 1-minute and tick data (CM, F&O, including expired contracts)? Can we store it permanently and show it to users?"
- Q-V-5 (TrueData, GFDL): "Do your Corporate Announcements, Corporate Data and News APIs include display and redistribution rights to end users? What is the latency from exchange dissemination?"
- Q-V-6 (GFDL): "Your site says realtime updates at 1-second frequency. Is cumulative traded volume exact at each snapshot, so that 1-minute volume is exact?"

**Zerodha (Kite Connect platform team) / Upstox (api@upstox.com) / Angel One / Dhan / Fyers**
- Q-B-1: "We want to let each user connect their own account so they can see their own holdings and live quotes inside our assistant. Nothing is shown to other users and nothing is cached across users. Is this permitted under your API terms and exchange rules? Which platform or partner approval is required, and what is the process, timeline and fee?"
- Q-B-2: "Does your API have per-app (not per-user) rate limits that would apply if 1,000 or 100,000 users connect through one app?"
- Q-B-3: "Given SEBI Intermediaries Regulations Reg 16A, what content restrictions do you impose on partner apps? For example, no recommendations and no return claims."
- Q-B-4 (Zerodha): "How does the hosted Kite MCP server provide live quotes to users on the free Personal plan? May a third-party app direct its users to the hosted MCP?"

**BSE (information products)**
- Q-BSE-1: "Please share the current domestic tariff for real-time and 15-minute delayed display in a web and mobile app, plus non-display and derived-data terms."

---

## 8. Recommended India stack [P] with cost formulas [E]

**(a) Prototype, internal team only, no public display**
- Data: one vendor API on a development/internal licence (TrueData or GFDL; ask Q-V-2). Developers may also use their own personal broker API (Kite Connect ₹500/mo, or free Fyers/Angel/Upstox) for their own data only.
- Nothing is shown to outside users. Corporate data comes from a vendor trial or manual review, not scraping.
- Cost formula: `vendor_dev_fee + Σ personal broker APIs (₹0–500/mo each)`. [E] Expect about ₹5k–30k per month; the vendor price is unverified.
- Posture A. No orders.

**(b) Pilot, 1,000 users**
- **Preferred: delayed-first**, matching ADR-002. NSE 15-minute delayed display plus BSE delayed, via vendor or direct, with derived analytics from delayed data.
  - Cost formula: `₹60,000 × S × mediums (web, app) [period unverified] + vendor_fee + BSE_delayed_fee (unknown) + corporate_data_fee (unknown)`. With S = 2 and web only: **≈ ₹1.2 lakh (period TBD) + vendor**.
- Optional per-user live quotes via Upstox or Angel login, for that user only, **only after written approval (Q-B-1)**.
- Real-time alternative: `S × (₹24 L + 1,000 × ₹820 × 12) ≈ ₹1.22 Cr per segment per year`, unless Q-NSE-1 places you in the free-app or open-website category (**≈ ₹27.5 L per segment per year**). Add non-display `₹18 L per segment per year` if applicable.
- Posture A, with lawyer sign-off. Output guardrails and audit logs. DPDP-ready consent flows before 13 May 2027.

**(c) Scale, 100,000 users**
- One central licensed real-time feed from a vendor, with NSE/BSE agreements signed directly, feeding your own cache and fan-out. [I, H] This is the only architecture that meets ~300 ms at 100k users within the terms found.
- Cost formula depends on category:
  - open website: `S × ₹27.5 L`;
  - free app: `₹0 variable + base licence`;
  - paid app: `max(₹11.5 L, rev-share % × revenue)`;
  - per-user: **≈ ₹98.6 Cr per segment per year**, which is infeasible;
  - plus non-display `S × ₹18 L`, plus vendor fee, plus corporate-data fee.
- Broker connections stay optional, per-user, and approved.
- Posture: decide between A and B (registered RA). Algo or order features only with empanelment.

---

## 9. Unverified items
1. Current NSE real-time tariff (2025 and March 2026 PDFs timed out); the mobile revenue-share figure (10% or 20%); the "not standalone" clause; the category for a login-gated app.
2. Whether the NSE non-display annexure (2016) is current.
3. Billing period of the NSE ₹60k delayed fee.
4. BSE domestic tariff.
5. Vendor API prices, latency, historical depth and display rights (TrueData, GFDL, Accelpix, Accord).
6. Data display terms for Upstox, Angel, Dhan, Fyers, Breeze, Kotak and Groww (primary terms not read).
7. The Groww price conflict (₹499 vs ₹2,000); Dhan Data API conditions; whether Upstox API access stays free after 30 Sep 2026.
8. How hosted Kite MCP serves quotes to Personal-plan users.
9. Full operative text of the SEBI circulars of 24 May 2024 and 4 Feb 2025 (SEBI pages returned headers only).
10. Whether SEBI's AI/ML guidelines (consultation Jun 2025) were finalised.
11. RA registration requirements for a body corporate (net worth, certification) in 2026.
12. BSE's share of cash-equity volume, which decides whether NSE-only data meets "full-volume".
13. Whether Vested or INDmoney offer partner APIs.
14. 5paisa API (not researched).
