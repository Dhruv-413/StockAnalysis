# What is achievable: data sources, real costs and rights (India-first, US second leg)

- **Author:** market-data-researcher.
- **Access date for every URL:** 2026-09-24.
- **Method:** read-only. No sign-ups, no vendor contact, no forms, no repo edits.
- **Tags:** [F] fact from a primary source; [F-sec] secondary source or search extract; [I] inference; [A] assumption; [E] estimate; [P] proposal. Confidence is H/M/L.
- **Scope:** this adds to the five documents named in the brief. Where a number already appears there, it is **pointed to, not re-derived**:
  - `research/india-market-data-and-sebi.md` (the "India appendix");
  - `research/kite-and-broker-apis.md`;
  - `research/global-news-and-data.md`;
  - `research/official-sources-and-tools.md`;
  - `16-india-research-round-3.md`.

**Conventions**
- **[A] FX:** ₹88 = US$1, assumed for 2026-09-24. It was not verified against RBI or FBIL reference rates, so re-price before any decision.
- **GST:** every INR exchange fee **excludes 18% GST**. Vendor USD prices exclude Indian GST and withholding.
- **Monthly figures:** annual fees are shown as monthly equivalents (÷ 12). All totals are **[E]**.
- **Rights:** every row keeps three things separate:
  - (a) the vendor's software/API licence;
  - (b) the exchange's (or publisher's) **data rights**, which are needed on top of (a);
  - (c) display vs. non-display, storage, derived data and redistribution/export.

---

## 0. Headline findings (new in this pass)

1. **[F, H] NSE's own tariff sheet says the delayed, EOD and Corporate Data fees are annual.** This resolves Q-NSE-4's billing-period question for the 2022 sheet. The NSE D&A "Market Data Product Tariff, effective April 1, 2022" (https://archives.nseindia.com/content/press/Other_Data_Product_Pricing_effective_Apr012022.pdf, read in full) states: "All tariff mentioned below are on annual basis". Domestic fees:

   | Product | Fee per year |
   |---|---|
   | 15-min delayed snapshot, CM | ₹80,000 |
   | 15-min delayed snapshot, F&O | ₹80,000 |
   | 5-min snapshot, CM (per segment) | ₹3,75,000 |
   | 2-min snapshot, CM | ₹7,50,000 |
   | 1-min snapshot, CM | ₹14,00,000 |
   | **EOD data, "Display on Website/application/information tools", CM + F&O** | **₹1,00,000** |
   | Historical trade data, "Others" | ₹90,000 per segment |
   | **Corporate Data** | **₹10,00,000** |
   | Real-time stock-wise (single stock) | ₹10,000 |

   - The undated sheet quoted in the India appendix §1.2 gives ₹60,000 for delayed data. The 2022 sheet gives **₹80,000**.
   - A newer sheet exists: "NSE Market Data Pricing – Domestic", effective 1 April 2026. It timed out again. Its search extract mentions a "1,30,000" figure whose product is unknown. **The current delayed fee is therefore somewhere between ₹60k and ₹1.3L a year, confidence M.**
2. **A free-to-user app still pays a fixed real-time fee.** The table is [F, H]; the reading of the 2025 extract is [I, M]. Source: NSE's real-time tariff for domestic vendors (https://archives.nseindia.com/content/press/Download_Real_Time_Tariff_Domestic_01042020.pdf, read in full). The filename says `01042020`, but the document says "Effective April 1, 2021". Level 1 CM:

   | Usage | Fixed fee per year | Domestic variable fee |
   |---|---|---|
   | Terminals | ₹19.0 L | ₹800/user/month |
   | Software/charting | ₹19.0 L | ₹600/user/month |
   | Open website | ₹21.0 L | NIL |
   | Mobile, paid-user app | ₹11.0 L | 10% revenue share, minimum ₹11 L per annum |
   | **Mobile, free-to-user app** | **₹21.0 L** | NIL |

   - So "NIL" is the **variable** fee only. A free app pays the same fixed fee as an open website.
   - **Open website and free app are separate rows, each with its own fixed fee.** [I, M] A product with real-time data on **both** web and app would pay two fixed fees (≈ 2 × ₹27.5 L at 2025 levels) unless NSE confirms otherwise. This is added to Q-NSE-1/Q-NSE-2.
   - [I, M] The 2025 extract's "NIL for free-to-user apps" almost certainly means NIL *variable*. Budget the free app at about the open-website fee (₹27.5 L in the 2025 extract).
   - A note at the foot of the same sheet says "Mobile Phones (paid user app) – Revenue share of 20% net of taxes from 1 user". That contradicts the 10% line in the table. It is still unresolved (Q-NSE-2).
3. **[F, H] Real-time NSE index values are priced separately from real-time CM.**
   - The same 2021 sheet labels CM as "Capital Market (Excluding Indices)" and prices **Indices** separately: **₹3.0 L per year fixed + ₹200 per domestic end user per month**.
   - The existing docs assumed NIFTY values come with the CM licence. **For real-time data, they do not.**
   - The 2022 delayed/EOD sheet has **no** "excluding indices" qualifier. Whether delayed or EOD index values come with those licences is **unconfirmed** (Q-DS-1). Do not assume that they are excluded.
   - Whether indices have an open-website or free-app variant is **not stated**, so this is a new question (Q-DS-1).
   - NSE Indices Ltd "index licensing" covers **financial products** (ETFs, index funds, benchmarking), not display ([F-sec, M] https://www.nseindia.com/static/nse-indices/index-licensing, timed out; search extract).
4. **[F, H] Every Indian corporate-data or market-data vendor checked is quote-only or personal-use-only for API or display use.**
   - TrueData says API access "requires a separate application, compliance review, and approval". Its standard licence is "internal use only".
   - GFDL has "flexible pricing... tailored".
   - Accord (ACE), CMOTS/APIDataFeed and Capitaline publish no price.
   - Accelpix retail plans are "personal, non-commercial".
   - CMIE Prowess is **non-commercial and forbids building a database** (H, agreement read).
   - **No startup or pilot plan was found for any of them.**
5. **[F, H] Twelve Data is EOD-only for NSE and BSE.** Its exchange list shows XNSE and XBOM as "EOD" on "Grow / Venture". It **cannot supply real-time or delayed Indian prices**, and it is not on the NSE authorised-vendor list. So the NSE EOD display licence (₹1 L/yr) still applies before showing even EOD data.
6. **[F, H] EODHD commercial:** "Internal Use" costs **$399/mo**. It says "Displaying the data or sharing it with individuals outside your company is not permissible". "Enterprise" costs **$2,499/mo**, and its display terms are not stated on the page. EODHD covers NSE (`SYMBOL.NSE`, delayed "live" and EOD; M). It is not an NSE-authorised vendor, so NSE display licences apply as well.
7. **[I, H] Consequence for budgets.**
   - ₹25k/mo (₹3 L/yr) can pay for **one** NSE delayed or EOD display licence plus free or cheap non-price sources. It cannot pay for licensed corporate data.
   - ₹1 L/mo (₹12 L/yr) can pay for delayed CM + F&O and EOD, plus **one** quote-dependent corporate-data feed. NSE's own Corporate Data (₹10 L/yr) takes most of that tier.
   - ₹5 L/mo (₹60 L/yr) is the first tier where **real-time NSE CM** is possible. It is only possible via the open-website/free-app category (Q-NSE-1), and **not if the ₹18 L non-display fee applies** as well as real-time F&O.

---

## 1. Master table: data need → best practical source → cost → rights → confidence

Costs are **[E]** monthly equivalents, excluding GST. "Exch" means the exchange fee payable to NSE/BSE, which is separate from the vendor fee.

| # | Data need | Best practical source (licensed) | Cost ₹/mo | Cost $/mo | Rights (vendor licence / data rights / display / redistribution) | Conf |
|---|---|---|---|---|---|---|
| 1a | NSE equity **EOD** prices | NSE D&A EOD display licence, with data via NSE files or any authorised vendor (TrueData, GFDL, Accord, CMOTS) | Exch ₹8,333 (₹1 L/yr covers CM + F&O) + vendor quote (or ₹0 if taken direct from NSE) | ~$95 + vendor | NSE sheet column is headed "Display on Website/application/information tools", so display is covered. Storage, derived data and CSV export are not stated (Q-NSE-5) | H (2022 fee) / M (current) |
| 1b | NSE equity **15-min delayed** | NSE D&A 15-min delayed snapshot (1-minute files, FTP) | Exch ₹6,667 per segment per medium (₹80k/yr, 2022); ₹5,000 on the undated sheet | ~$76 | "Per medium": web and app are charged separately (undated sheet, India appendix §1.2). A feed to others needs NSE written consent | H (fee, 2022) / M (current) |
| 1c | NSE equity **real-time** | Authorised vendor (TrueData, GFDL; quote) + NSE agreement | Open website ≈ ₹2.29 L (₹27.5 L/yr, 2025 extract). Per-user: ₹2 L + ₹820 × N. Free app ≈ open-website fixed fee (finding 2) | ~$2,600+ | Display only under the NSE category signed. Non-display derived analytics: + ₹1.5 L/mo (₹18 L/yr, 2016 annexure; Q-NSE-3) | M |
| 1d | **BSE** prices (any delay) | BSE Information Products tariff (Feb 2025 sheet; PDF returns 403) | **Unknown** | — | BSE describes a "monthly website fee" that lets vendor clients display delayed or EOD data ([F-sec, M] search extract of https://www.bseindia.com/market_data_products.html) | L |
| 1e | **Index values** (NIFTY, SENSEX) | NSE D&A "Indices" feed; BSE Index Services (formerly Asia Index) for SENSEX | NSE real-time: ₹25,000 fixed + ₹200 × N per month (2021 sheet). Delayed/EOD index fee: unknown (Q-DS-1) | ~$284 + $2.3 × N | Separate from the CM licence. SENSEX display terms not found | H (2021 fee) / L (current, BSE) |
| 2 | F&O **option chain, OI, Greeks inputs** | TrueData Options Chain API ("IV, and Greeks"); GFDL OptionChain + "option greeks" API; NSE F&O segment licence | Vendor quote + F&O segment exch (delayed ₹6,667/mo; real-time as 1c) | — | Vendor-computed IV and Greeks are the vendor's derived data. Showing them needs vendor permission as well as the F&O display licence. Computing our own IV is non-display derived use (Q-NSE-3). **Risk-free rate:** FBIL is fee-liable and RBI prohibits caching (official-sources §1.3), so **unresolved**. Take the rate from the vendor, or use a disclosed fixed assumption | M |
| 2b | FII/DII participant OI (EOD) | Vendor (CMOTS/Accord; not confirmed) | Quote | — | The NSE web page is ToU-restricted (official-sources §1.1) | L |
| 3 | **Corporate announcements / filings** (structured) | (i) NSE D&A **Corporate Data** ₹10 L/yr; (ii) vendor feeds: TrueData Corporate Announcement API, CMOTS "Announcement" API, Accord "Corporate Announcements", TickerPlant (~₹3 L/yr, forum report); (iii) stockinsights.ai Business (quote) | (i) ₹83,333; (ii) quote, **~₹25,000** for TickerPlant (L); (iii) quote | (i) ~$947 | (i) What "Corporate Data" includes is **not stated** on the sheet (Q-DS-2). (ii) TrueData: "Redistribution, resale, or public sharing of data is not allowed without prior written permission". (iii) the stockinsights Developer plan is "internal tools, prototypes"; the Business plan is for "customer-facing applications... redistribution" (quote). Link-out to the exchange PDF is the lowest-risk display | H (NSE fee) / L (TickerPlant) / H (stockinsights plan split) |
| 4 | **Fundamentals, ratios, shareholding, promoter pledge** | Accord ACE feed ("Latest 5 Years Financial & 8 Qtr. Result & Shareholding"); CMOTS/Capitaline API; TrueData Corporate Data API ("shareholding patterns, financial ratios") | Quote only (all three) | — | Display and redistribution by contract. **CMIE Prowess is excluded**: "non-commercial", "may not be used to construct a database of any kind" (agreement, H). Pledge data (SAST Reg 31) comes via the announcements feed | M (products) / L (price) |
| 5 | **Corporate actions** | Accord ("Corporate Action – BSE EOD"); CMOTS; TrueData Corporate Data | Quote | — | Usually bundled with 4. Needed for invariant 3 (adjustment table) | M |
| 6a | **Bulk/block deals** | Vendor (CMOTS, Accord; inferred); NSE Corporate Data (contents unconfirmed) | Quote | — | Published after hours. **Not listed** among TrueData's API products | L |
| 6b | **Insider (PIT) / SAST** | Announcements feed (row 3); NSE Corporate Data | As row 3 | — | As row 3 | M |
| 6c | **FII/DII cash flows** | Vendor (unconfirmed). **NSDL FPI Monitor is not usable**: "reproduction, redistribution and transmission... strictly prohibited" ([F-sec, M] https://www.fpi.nsdl.co.in/Reports/ReportsListing.aspx) | Quote | — | NSE provisional figures fall under NSE ToU | L |
| 7 | **MF NAVs and portfolios** | Accord ACE MF ("Scheme Master, NAV, NAV Historical, Latest Portfolio"); CMOTS MF API; TrueData Mutual Fund API ("Schemes, NAVs, holdings"); Morningstar India (quote) | Quote | — | AMFI NAVAll.txt is "personal and non-commercial use only" (official-sources §1.3). Free wrappers (mfapi.in, mfdata.in) redistribute AMFI data, so **Hold**. Monthly portfolios on AMC sites fall under each AMC's terms | M (products) / L (price) |
| 8a | **Indian market news, English** | Headline + link: Marketaux (`countries=in` supported) $49–$199; licensed text: HT Syndication (HT, Hindustan; "any digital or print medium"; quote), PTI (subscription required; quote), ANI (~₹1.5–2 L/mo for TV channels, forum/Quora, L), vendor news (Accord "ACE Live News", CMOTS News, TrueData News API; quote) | Marketaux ₹4,300–₹17,500; licensed text: quote (≥ ₹1 L/mo is plausible, L) | $49–$199; quote | Aggregators license metadata only: headline + snippet + link (global-news §0). AI summaries of full text need a publisher licence (Q14/Q15) | H (Marketaux) / L (wire prices) |
| 8b | **Indian market news, Hindi** | Marketaux (`hi` listed among supported languages); HT Syndication (Live Hindustan); PTI Bhasha / IANS Hindi (quote) | As 8a | — | As 8a. NewsAPI.ai lists "50+ languages" but Hindi is not named on its plans page | H (Marketaux language param) / L |
| 9 | **Global news** | GDELT (free, link-out); Marketaux / NewsAPI.ai $90; NewsAPI.org Business $449; Factiva / LSEG (quote) | ₹0–₹39,500 | $0–$449 | See global-news §2. Only licensed-content vendors grant summary rights | H (prices) |
| 10a | **US prices** | Delayed: Twelve Data Venture ($499/mo, client-facing) or Massive; real-time: Nasdaq Basic ($2,140/mo + $1/non-pro) | ₹43,900 → ₹1.9 L+ | $499 → $2,140 + $1 × N | See `research/market-data.md` (Twelve Data, Nasdaq, IEX rows). IEX delayed is free but covers only the IEX venue, so it **fails the "consolidated" spec** (06 §1) | H (from market-data.md) |
| 10b | **US news / filings** | SEC EDGAR (free); Benzinga (quote); Marketaux | ₹0 → quote | $0 → quote | global-news §2, §6 | H |

---

## 2. Vendor purchasability (can a small startup actually buy it?)

"Sales call?" means the price is not self-serve. "Startup plan" means a published startup or pilot tier.

| Vendor | Product relevant here | Public price? | Sales call? | Startup/pilot plan? | Minimum contract (as found) | NSE-authorised? | Source | Conf |
|---|---|---|---|---|---|---|---|---|
| **NSE D&A (direct)** | Delayed, EOD, Corporate Data, real-time | **Yes** (tariff PDFs) | Agreement required (marketdata@nse.co.in) | No | Annual fees (2022 sheet: "annual basis") | — | 2022/2021 PDFs above | H |
| **BSE** | Information products | PDF exists (Feb 2025) but returns 403 | Yes (datafeed.sales@bseindia.com, per search extract) | No | Unknown | — | https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf | L |
| **TrueData** | Real-time/EOD API, option chain + Greeks, corporate announcements, corporate data, MF, news | No (retail Velocity terminal ₹1,440–₹2,796/mo **excludes API**) | Yes: "separate application, compliance review, and approval" | Trial: "limited-period evaluation account... subject to exchange compliance approval" | "No commitment required, flexible pricing" (API product page); "No refunds once API access is activated" | Yes (CM, F&O, CD) | https://www.truedata.in/market-data-apis ; https://www.truedata.in/price ; https://www.truedata.in/products/marketdataapi | H |
| **Global Datafeeds (GFDL)** | Real-time (1-s), historical, OptionChain, option Greeks, Exchange Snapshot; NSE, NFO, BSE, BFO, MCX | No: "flexible pricing policy which is tailored" | Yes (sales@globaldatafeeds.in) | Trial referenced; no startup tier | Unknown | Yes | https://globaldatafeeds.in/apis/ ; https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/pricing-sales/api-pricing/ | H (no price) |
| **Accelpix** | Real-time API, IEOD | Retail ₹1,599–₹3,499/mo, **personal non-commercial** | Yes, for "commercial licensing" | No | Unknown | Yes (CM, F&O) | https://accelpix.com/pricing/ ; https://accelpix.com/ | H (retail) / L (commercial) |
| **Accord Fintech (ACE)** | Intraday/EOD prices, corporate actions, financials + shareholding, MF NAV + portfolio, ACE Live News, announcements; FTP/API | No | Yes ("inquiry or request a callback") | No | Unknown | Yes ("Authorized data feed vendor of BSE/NSE/MCX/NCDEX") | https://www.accordfintech.com/market-data-feed | H (catalogue) |
| **CMOTS / APIDataFeed / Capitaline** | "200+ APIs": equity, derivatives, MF, IPO, news, announcements, company information; delayed/historical/EOD (no real-time listed) | No | Registration "API subscription process"; pricing not shown | No | Unknown | Not on the 2016-era NSE real-time list excerpt (unverified) | https://www.apidatafeed.com/ ; https://www.capitaline.com/ | M |
| **CMIE Prowess IQ** | Fundamentals database | ₹1.70 L/yr login (2020 price list; rises capped at 7%/yr) | Self-serve subscription | No | Annual | n/a | https://www.cmie.com/kommon/bin/sr.php?kall=warticle&dt=20191023143103&msec=790&ver=pf ; agreement: https://prowessiq.cmie.com/kommon/bin/sr.php?kall=wagreepp&tab=agree&dl=1 | H: **not usable in product** (non-commercial; no database) |
| **Dion Global (Insight)** | Fundamentals, news, MF | No | Yes | No | Unknown | Unknown | https://www.dionglobal.com/stock-market-data-content-and-financial-research-solutions.html | L. **Vendor-viability flag:** listed market cap ₹7.25 Cr (05/06/2026, Angel One / IIFL page extract) |
| **Trendlyne** | Consumer plans; "AI MCP plans... from ₹299/month" | Consumer only | Yes (contact@trendlyne.com) | No B2B API terms found | — | No | https://trendlyne.com/subscription/plans/ | L |
| **Tijori** | Research app; Tijori Stack concall API | Stack API **$150/mo or $1,200/yr** (search extract) | Enterprise data: contact support | No | — | No (sources "approved data vendors") | https://www.tijorifinance.com/plans/ ; https://www.tijoristack.ai/concall-monitor/ | L |
| **stockinsights.ai** | India announcements tagged feed, transcripts | Retail Pro ₹333/mo; API Developer 7-day trial (100 calls); **Business: quote** | Yes, for Business | Developer plan for "prototypes" (internal) | — | No | https://www.stockinsights.ai/pricing ; https://docs.stockinsights.ai/api-reference/india_endpoints/announcements-tagged-feed | H |
| **indianapi.in** | Live NSE/BSE prices, fundamentals, MF, news | Plans named (Free → Pro); prices not captured | Self-serve | — | — | **No licensing claim found**, so **Hold** until its data origin is shown | https://indianapi.in/indian-stock-market | L |
| **TickerPlant** | Corporate announcement API | ~₹3 L/yr (forum user report) | Yes | No | — | Unverified | https://tradingqna.com/t/corporate-announcement-data-api/178154 | L |
| **Twelve Data** | NSE/BSE **EOD only**; US real-time | Individual tiers are "personal, internal, and non-commercial" (prices conflicting between fetches; §7); Venture $499 / Enterprise $1,099 (market-data.md) | Self-serve | Venture is the smallest client-facing tier | Monthly | No | https://twelvedata.com/exchanges ; https://twelvedata.com/pricing | H |
| **EODHD** | NSE delayed + EOD; global fundamentals | Personal $19.99–$59.99; **Internal Use $399/mo (no display)**; Enterprise $2,499/mo | Commercial: "we will reach out to you" | "Startups & Enterprise" = the $399+ tiers | Monthly/annual | No | https://eodhd.com/pricing ; https://eodhd.com/commercial-pricing ; https://eodhd.com/exchange/NSE | H (prices) / M (NSE coverage) |
| **FMP** | Covers `.NS` tickers (e.g. BSE.NS profile) | Pricing page returned 403 this pass (global-news §4: $22–$149/mo, L) | Display needs a "Data Display and Licensing Agreement" (quote) | No | — | No | https://site.financialmodelingprep.com/profile/BSE.NS | M (coverage) / L (price) |
| **LSEG (Refinitiv)** | NSE L1/L2/L3/TBT, Reuters news | No; Workspace reportedly $15k–$22k per user per year (Vendr/secondary) | Yes | No | Annual enterprise | Yes | https://www.lseg.com/en/data-analytics/financial-data/pricing-and-market-data/equities-market-data/national-stock-exchange-india ; https://www.vendr.com/marketplace/refinitiv | L (price) |
| **Bloomberg B-PIPE / Data License** | Global incl. NSE | No; B-PIPE reportedly $2k–$3k/mo base (secondary) plus exchange fees | Yes | No | Enterprise | Yes | https://www.bloomberg.com/professional/product/market-data/ ; https://multiples.vc/compare/bloomberg-api-alternatives | L |
| **ICE Consolidated Feed** | NSE MBP / L2 | No | Yes | No | Enterprise | Yes | https://developer.ice.com/fixed-income-data-services/catalog/national-stock-exchange-india-nse | M (coverage) |
| **Morningstar India** | MF and equity data | No | Yes ("use-case based access") | No | Enterprise | n/a | https://developer.morningstar.com/direct-web-services/documentation/data-and-research/equity-data | L |
| **PTI / IANS / ANI** | English + Hindi wires | No (PTI: "you must subscribe"; IANS services page 403) | Yes | No | Annual subscription | n/a | https://en.wikipedia.org/wiki/Press_Trust_of_India ; https://www.ians.in/services ; https://www.aniin.com/ | L |
| **HT Syndication** | HT, Hindustan (Hindi), ~200 publications | No | Yes | No | — | n/a | https://www.htsyndication.com/ | M |
| **Times Syndication Service (ET) / Network18 (Moneycontrol)** | ET text; Moneycontrol | No public syndication offer found for Moneycontrol; ET via 3DSyndication (not opened) | Yes | No | — | n/a | search only | L |
| **Marketaux** | Global + India news, Hindi | $0 / $29 / $49 / $99 / $199 per month | Self-serve | Yes (self-serve tiers) | Monthly | n/a | https://www.marketaux.com/pricing ; https://www.marketaux.com/documentation | H |
| **NewsAPI.ai** | Global news | 5K plan $90/mo | Self-serve | Free 2,000 searches | Monthly | n/a | https://newsapi.ai/plans | H |

**[I, H] Bottom line:** the only Indian items a startup can **buy today at a published price** are:
- NSE D&A's own delayed, EOD and Corporate Data licences (annual);
- consumer-grade tools, which cannot be used in a product.

Every vendor that can deliver Indian data **into an app with display rights** needs a sales conversation.

---

## 3. Minimum viable data stack at three budgets

Totals exclude GST (add 18%) and engineering or hosting costs.
- **[A] The tiers assume GST input-tax credit** (a GST-registered company).
  - If the budget is gross and GST is not recoverable, ₹25k gross is about ₹21.2k net, and Tier A's headroom falls to about ₹1.9–3.6k/mo.
- **[I, M] Non-display.** The NSE non-display policy (India appendix §1.2) is worded around "real time NSE market data". So the ₹18 L non-display fee most likely does **not** apply to indicators computed from delayed or EOD data in Tiers A and B. It is a live risk only in Tier C. Confirm via Q-NSE-3. **"Fits if quote ≤ ₹X"** marks the headroom left for a line whose price is quote-only. No number has been invented for those lines.

### Tier A: about ₹25,000/mo (₹3 L/yr)

| Line | Annual | Monthly [E] | Source |
|---|---|---|---|
| NSE EOD display licence, CM + F&O | ₹1,00,000 | ₹8,333 | 2022 NSE sheet |
| NSE 15-min delayed, CM, **one medium (web)** | ₹60,000–₹80,000 (2026 fee unknown) | ₹5,000–₹6,667 | undated sheet / 2022 sheet |
| Marketaux Standard (India and Hindi filters, headline + link) | — | ~₹4,300 ($49) | marketaux.com/pricing |
| GDELT, SEC EDGAR, SEBI/PIB RSS, MoSPI API | ₹0 | ₹0 | global-news §2; official-sources §1.3 |
| **Subtotal** | | **~₹17,600–₹19,300** | |
| Data delivery (vendor feed, or NSE FTP files direct) | — | **fits if quote ≤ ~₹5,700–₹7,400/mo** | quote |

**Can show**
- NSE equity **EOD** prices and returns, and **15-minute-delayed** NSE cash-market prices on the **website only**, labelled `delayed-15` (invariant 1).
- Deterministic computed values (returns, RVOL, indicators) from delayed or EOD data, subject to Q-NSE-3/Q-NSE-4 on derived data.
- Headline + link news (English and Hindi), SEBI/PIB releases, MoSPI macro, US SEC filings.

**Cannot show**
- **Any real-time price.**
- **Index values: unconfirmed.** They may come with the delayed/EOD licence (Q-DS-1). Until NSE answers, show "index: not licensed" rather than a number.
- F&O prices, OI or an option chain.
- BSE prices.
- The **mobile app** medium: a second medium costs another ₹60–80k/yr and exceeds the tier if the delivery quote exceeds ~₹1k/mo.
- Structured announcements, fundamentals, corporate actions, bulk/block, insider or FII/DII data. There is no licensed source at this price, so show **link-out only** once Q-O1 permits.
- MF NAVs (AMFI is non-commercial).
- Publisher article text or AI summaries of it.
- US prices: Twelve Data Venture at $499 ≈ ₹43,900 exceeds the whole tier.

**Also:** without licensed corporate actions, **adjusted** history cannot be built (invariant 3). Show raw EOD only and say "unadjusted".

### Tier B: about ₹1,00,000/mo (₹12 L/yr)

| Line | Annual | Monthly [E] | Notes |
|---|---|---|---|
| NSE EOD display, CM + F&O | ₹1,00,000 | ₹8,333 | |
| NSE 15-min delayed, CM + F&O × web + app (4 licences) | ₹2,40,000–₹3,20,000 | ₹20,000–₹26,667 | "per medium" rule |
| Marketaux Pro 50K | — | ~₹17,500 ($199) | India + Hindi headlines |
| GDELT, EDGAR, SEBI/PIB, MoSPI | ₹0 | ₹0 | |
| **Subtotal** | | **~₹45,800–₹52,500** | |
| **Corporate data feed** (announcements + corporate actions + fundamentals + shareholding + bulk/block), from Accord ACE, CMOTS or TrueData Corporate Data | quote | **fits if quote ≤ ~₹47,500–₹54,000/mo** (about ₹5.7–6.5 L/yr) | NSE's own Corporate Data (₹10 L/yr = ₹83,333/mo) **does not fit** together with the lines above |
| Alternative for announcements only: TickerPlant | ~₹3 L/yr (L) | ~₹25,000 | leaves ~₹22–29k/mo for fundamentals |

**Can show** everything in Tier A, plus:
- delayed F&O (futures and options prices, with OI if the snapshot carries it; Q-DS-3), on web **and** app;
- **if the corporate-data quote fits:** structured announcements with exchange dissemination timestamps, corporate actions (so **adjusted** series become possible, invariant 3), fundamentals and ratios, shareholding and pledge, and bulk/block deals, all subject to that vendor's display clause.

**Cannot show**
- Real-time anything.
- Index values: **unconfirmed**. They may be included in the delayed/EOD licences (Q-DS-1).
- BSE-only listings (the BSE tariff is unknown).
- An option chain with IV and Greeks, unless the vendor includes it in the same quote.
- MF NAVs and portfolios, unless bundled (Accord and CMOTS list MF modules).
- Licensed news text or summaries.
- US prices (a US leg means dropping Marketaux Pro and fitting Twelve Data Venture at ~₹43,900, which squeezes corporate data to ≤ ~₹21k/mo).

### Tier C: about ₹5,00,000/mo (₹60 L/yr)

Two paths, depending on the NSE category answer (Q-NSE-1) and non-display (Q-NSE-3).

**Path C1: real-time NSE CM under the open-website / free-app category, for ONE medium only (web or app; if NSE agrees)**

Real-time on **both** web and app would need two fixed fees (finding 2), about ₹55 L/yr for CM alone. That **exceeds this tier** unless NSE confirms one licence covers both.

| Line | Annual | Monthly [E] |
|---|---|---|
| NSE real-time CM, open website (2025 extract) | ₹27,50,000 | ₹2,29,167 |
| NSE indices real-time (2021 sheet; open-website variant unknown) | ₹3,00,000 + ₹200 × N × 12 | ₹25,000 + ₹200 × N |
| NSE 15-min delayed F&O, web + app | ₹1,60,000 | ₹13,333 |
| NSE EOD display | ₹1,00,000 | ₹8,333 |
| NSE Corporate Data | ₹10,00,000 | ₹83,333 |
| Marketaux Pro 50K + NewsAPI.ai 5K | — | ~₹25,400 |
| US: Twelve Data Venture | — | ~₹43,900 |
| **Subtotal** (N = 0 index users) | | **~₹4,28,500** |
| Real-time vendor feed (TrueData/GFDL) + fundamentals vendor | quote | **fits if combined quote ≤ ~₹71,500/mo − ₹200 × N** |
| **Index-viewer cap** | | Even with a vendor fee of zero, ₹71,500 ÷ ₹200 means **N ≤ ~350 users seeing real-time indices**. With any vendor fee, the cap is lower. Indices appear on nearly every card, so this cap binds |
| **If NSE non-display applies** (₹18 L/yr = ₹1.5 L/mo) | | **Tier exceeded** (~₹5.8 L before vendor fees) |

**Path C2: per-user real-time (software/charting category)**
- `₹24 L + ₹820 × N × 12` per year for CM alone, plus other lines as in C1.
- The fixed lines come to ₹24 L + ₹23.9 L (index fixed, delayed F&O, EOD, Corporate Data, news, US) = ₹47.9 L/yr. That leaves about ₹12 L/yr of headroom. Each real-time user costs ₹820 (CM) + ₹200 (indices) = ₹1,020/month, so **N ≤ ~100 real-time users** [E] **before any vendor fee**. Everyone else stays on delayed data.

**Can show (C1)**
- Real-time NSE cash-market prices and computed values.
- Index values, at a per-user index cost.
- Delayed F&O.
- NSE Corporate Data (contents to confirm, Q-DS-2).
- Global and India headlines.
- US delayed or real-time via Twelve Data Venture (exchange fees not verified; market-data.md).

**Cannot show**
- Real-time F&O and a live option chain (another ₹24–27.5 L/yr).
- Licensed Indian publisher text, which still needs a quote.
- BSE real-time (unknown).
- Anything at all, if non-display applies.

**[I, M] The ₹5 L tier is only viable for real-time if NSE confirms, in writing, the category and the non-display treatment.** Otherwise the realistic ₹5 L stack is Tier B's delayed stack plus:
- NSE Corporate Data;
- the vendor corporate feed;
- a licensed Indian news quote (HT Syndication or PTI);
- a US Nasdaq Basic leg ($2,140 + $1/user ≈ ₹1.9 L/mo).

### Cost formulas (all [E], monthly, excl. GST)

```
Tier A = 1.0L/12 + d×1/12 + 4,300 + vendor_delivery          where d ∈ [₹60k, ₹80k] (2026 fee unknown)
Tier B = 1.0L/12 + 4×d/12 + 17,500 + corp_vendor_quote
Tier C1 = 27.5L/12 + (3.0L/12 + 200×N_idx) + 2×d/12 + 1.0L/12 + 10L/12 + 25,400 + 43,900 + rt_vendor_quote + fund_vendor_quote [+ 18L/12 if non-display]
Tier C2 = (24L + 820×N_rt×12)/12 + (other C1 lines)
```

---

## 4. Check against the detector data spec (06-quantitative-validation §1)

The spec is: consolidated (India: NSE + BSE), full-volume, 1-minute bars, displayable.

| Source | Consolidated | Full-volume | 1-minute | Displayable | Verdict |
|---|---|---|---|---|---|
| NSE 15-min delayed snapshot | NSE only | Snapshot; cumulative volume unverified (Q-NSE-4) | Yes (1-minute files) | Yes (licence) | **Candidate** for a delayed detector, pending Q-NSE-4 |
| NSE EOD | NSE only | Yes (daily) | No | Yes | Daily detector only |
| Twelve Data / EODHD NSE | NSE only | Unknown | EODHD: delayed intraday unknown; Twelve Data: EOD | Only with an NSE licence too | Not a spec source |
| TrueData / GFDL real-time | NSE + BSE (separately) | TrueData tick (claimed); GFDL 1-s snapshot | Yes | With vendor + exchange approval | Candidate (India appendix §6) |

---

## 5. Corrections to existing appendices (for the doc owners; not applied)

1. **India appendix §1.2 / §1.3, "Mobile app: NIL for free-to-user apps".**
   - The 2021 primary sheet shows **₹21 L fixed per annum**, NIL variable [F, H].
   - That the 2025 extract means the same thing is [I, M].
   - Rewrite the formula `Free-to-user mobile app: ₹0 variable` as **fixed ≈ open-website fee + ₹0 variable, charged per medium**.
2. **India appendix §1.2, delayed fee "period not stated".** The 2022 sheet says "annual basis", CM ₹80,000. [F, H]. The 2026 value is still unknown.
3. **India appendix §1.3, "CM" real-time.** CM **excludes indices**. Add an index line: ₹3 L/yr + ₹200 per domestic user per month (2021). [F, H]
4. **Global-news §4, "India: CMIE Prowess IQ... redistribution unlikely (L)".** Upgrade to **H: prohibited**. The agreement (v. 20 Feb 2020) grants a "non-exclusive, non-commercial, limited right" and says the data "may not be used to construct a database of any kind".
5. **market-data.md, Twelve Data:** add that NSE and BSE are **EOD only** (exchanges page, H). The individual-plan prices are **not** a correction; see §7.

---

## 6. New vendor and exchange questions (exact text; for the user to send; not sent)

IDs `Q-DS-*` avoid collisions with Q-NSE-*, Q-V-*, Q1–Q22, Q-O*, Q-Z-*, Q-B-*.

- **Q-DS-1 (NSE D&A, marketdata@nse.co.in):** "Your real-time tariff lists Indices separately from Capital Market ('Excluding Indices') at a fixed annual fee plus a per-user monthly fee. (a) Is there an open-website or free-to-user-app category for index values? (b) Are NIFTY index values included in the 15-minute delayed CM snapshot and the EOD display licence, or do they need a separate index-data licence from NSE Indices Ltd? (c) Please send the index fees in the pricing file effective 1 April 2026."
- **Q-DS-2 (NSE D&A):** "Your 'Corporate Data' product is listed at ₹10,00,000 per year (tariff effective 1 April 2022). Does it include (a) corporate announcements with dissemination timestamps, (b) corporate actions, (c) shareholding patterns and SAST pledge disclosures, (d) SEBI PIT insider disclosures, (e) bulk and block deals, and (f) daily FII/DII provisional figures? What is the delivery method and latency after website dissemination? Does the fee include display to end users of a web and mobile app, and may we show AI-generated summaries of announcements with a link to the original?"
- **Q-DS-3 (NSE D&A):** "Do the 15-minute delayed F&O snapshot files include open interest and change in OI per contract? Is the annual fee for delayed data per segment per medium (website and app charged separately) under the 1 April 2026 pricing file, and what is the current amount?"
- **Q-DS-4 (BSE, datafeed.sales@bseindia.com):** "Please send the Information Products Domestic Tariff (February 2025 or later) for (a) EOD display, (b) 15-minute delayed display on a website and a mobile app, (c) real-time display (open website, free-to-user app, per-user), (d) SENSEX and other index values, and (e) corporate announcements. Is the website fee monthly or annual?"
- **Q-DS-5 (Accord Fintech, CMOTS/APIDataFeed, TrueData, each):** "For a startup information app in India (web and mobile, under 1,000 users at launch), please quote an API or FTP feed of: corporate announcements, corporate actions, quarterly and annual financials, ratios, shareholding (including promoter pledge), bulk/block deals, insider/SAST disclosures, FII/DII daily flows, and MF NAV plus monthly portfolios. For each module, state: (1) display rights to our end users; (2) whether we may show AI-generated summaries; (3) storage and retention limits after termination; (4) whether user CSV export is allowed; (5) which exchange agreements we must sign directly; (6) minimum term, and whether a pilot or startup price exists."
- **Q-DS-6 (TrueData, GFDL):** "Do your Option Chain APIs supply IV and Greeks computed by you? If so, which risk-free rate and dividend assumption do you use, and may we display your IV/Greeks to end users? Is that covered by the F&O display licence or by a separate agreement with you?"
- **Q-DS-7 (EODHD):** "Does the Enterprise plan ($2,499/mo) permit display of NSE delayed and EOD prices to our end users? Are you licensed by NSE for this, or must we sign NSE's display licence ourselves? Same question for fundamentals of Indian companies."
- **Q-DS-8 (stockinsights.ai):** "Please quote the Business plan for the India announcements tagged feed and transcripts, for display to end users of a commercial app. What is your source for NSE/BSE announcements, and your latency after exchange dissemination?"
- **Q-DS-9 (indianapi.in):** "What is the source of your NSE/BSE live prices, and are you an NSE/BSE-authorised data vendor? Do your paid plans permit displaying the data to our users?"
- **Q-DS-10 (PTI, IANS, ANI, each):** "Please quote a digital subscription to your English and Hindi business wire for a commercial information app, covering display of headlines, a short excerpt and AI-generated summaries with attribution and link-back. Please include archive/retention terms and minimum term."
- **Q-DS-11 (Morningstar India):** "Please quote MF data (NAV, category, monthly portfolios, ratios) for display in a retail information app in India, up to N users. Is there a startup tier?"

---

## 7. Unverified items and gaps

1. The **2026 NSE domestic pricing file** (effective 1 Apr 2026) timed out, so the current delayed, EOD, Corporate Data, real-time and index fees are unconfirmed. The 2021 and 2022 sheets are primary but **may be superseded**.
2. The BSE tariff (PDF 403); SENSEX/BSE Index Services display terms.
3. Every vendor API price (TrueData, GFDL, Accord, CMOTS, Capitaline, Dion, LSEG, Bloomberg, ICE, Morningstar, PTI, IANS, ANI, HT, TSS, Network18).
4. Whether Marketaux actually tags NSE/BSE entities (the docs confirm only `countries=in` and `hi`).
5. FMP's current pricing (403) and India depth.
6. indianapi.in data origin and prices.
7. A lawful **risk-free-rate** source for Greeks.
8. Dion Global's business continuity.
9. The TickerPlant price (single forum report).
10. The FX rate (assumed ₹88/$).
11. **Twelve Data individual prices.** Two fetches of https://twelvedata.com/pricing on the same day returned different figures: $29/$99/$329 and $79/$229/$999 (Grow/Pro/Ultra). Unresolved. The Venture ($499) figure used in the tiers comes from market-data.md.
12. Whether one NSE real-time licence can cover both web and app (the 2021 sheet lists them as separate rows).

## Sources (all accessed 2026-09-24)

**NSE**
- 2022 product tariff: https://archives.nseindia.com/content/press/Other_Data_Product_Pricing_effective_Apr012022.pdf
- 2021 real-time tariff: https://archives.nseindia.com/content/press/Download_Real_Time_Tariff_Domestic_01042020.pdf
- 2026 file (timed out): https://nsearchives.nseindia.com/web/mediaattachment/2026-03/NSE_Pricing_file_-_Domestic_clients_20260309171343.pdf
- Index licensing: https://www.nseindia.com/static/nse-indices/index-licensing

**BSE:** https://www.bseindia.com/market_data_products.html ; https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf

**Indian market-data vendors**
- TrueData: https://www.truedata.in/market-data-apis ; https://www.truedata.in/price ; https://www.truedata.in/products/marketdataapi
- GFDL: https://globaldatafeeds.in/apis/ ; https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/pricing-sales/api-pricing/
- Accelpix: https://accelpix.com/pricing/

**Indian corporate-data vendors and research tools**
- Accord: https://www.accordfintech.com/market-data-feed
- CMOTS: https://www.cmots.com/ ; https://www.apidatafeed.com/ ; https://www.capitaline.com/
- CMIE: https://www.cmie.com/kommon/bin/sr.php?kall=warticle&dt=20191023143103&msec=790&ver=pf ; https://prowessiq.cmie.com/kommon/bin/sr.php?kall=wagreepp&tab=agree&dl=1
- Dion: https://www.dionglobal.com/stock-market-data-content-and-financial-research-solutions.html
- Trendlyne: https://trendlyne.com/subscription/plans/
- Tijori: https://www.tijorifinance.com/plans/ ; https://www.tijoristack.ai/concall-monitor/
- stockinsights: https://www.stockinsights.ai/pricing
- indianapi: https://indianapi.in/indian-stock-market
- TickerPlant (forum): https://tradingqna.com/t/corporate-announcement-data-api/178154
- NSDL: https://www.fpi.nsdl.co.in/Reports/ReportsListing.aspx

**Global data vendors**
- Twelve Data: https://twelvedata.com/exchanges ; https://twelvedata.com/pricing
- EODHD: https://eodhd.com/pricing ; https://eodhd.com/commercial-pricing ; https://eodhd.com/exchange/NSE
- FMP: https://site.financialmodelingprep.com/profile/BSE.NS
- LSEG: https://www.lseg.com/en/data-analytics/financial-data/pricing-and-market-data/equities-market-data/national-stock-exchange-india ; https://www.vendr.com/marketplace/refinitiv
- Bloomberg: https://www.bloomberg.com/professional/product/market-data/ ; https://multiples.vc/compare/bloomberg-api-alternatives
- ICE: https://developer.ice.com/fixed-income-data-services/catalog/national-stock-exchange-india-nse
- Morningstar: https://developer.morningstar.com/direct-web-services/documentation/data-and-research/equity-data

**News**
- Marketaux: https://www.marketaux.com/pricing ; https://www.marketaux.com/documentation
- NewsAPI.ai: https://newsapi.ai/plans
- HT Syndication: https://www.htsyndication.com/
- PTI: https://en.wikipedia.org/wiki/Press_Trust_of_India
- IANS: https://www.ians.in/services
- ANI: https://www.aniin.com/ ; https://www.quora.com/How-much-does-a-news-agency-like-PTI-ANI-UNI-Reuters-AP-cost-in-India
