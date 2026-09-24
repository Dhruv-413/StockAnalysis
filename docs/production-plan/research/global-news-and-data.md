# Research: Global news + details sources for an AI market assistant (India + US + global)

Research date / access date for all URLs: **2026-09-24** unless stated. Author role: Market-Data Researcher.
Confidence: **H** = the vendor's or regulator's own page was fetched and read; **M** = a primary page appeared in search results but was not fully read, or a reputable secondary source was used; **L** = third-party blog, forum or search snippet only.
Every cost below is an **estimate**. Every "display/summary right" is **unverified** unless it is quoted from the vendor. The right answer is a written licence.

---

## 0. Headline findings

1. **Who owns the article text decides whether you can show a summary, not which API plan you bought.** Sources split into two classes:
   - **Aggregators and indexers** (NewsAPI.org, Marketaux, NewsAPI.ai/Event Registry, Webz.io, GDELT, Finnhub news, Tiingo news). They license their *service and metadata*. They generally **cannot** grant rights over the publishers' text. The safe display is headline + short snippet + link-out. An LLM summary of the full third-party article is a derived work of content the aggregator does not own. It is unverified for every aggregator.
   - **Licensed-content vendors** (Benzinga, Dow Jones Factiva/Newswires, LSEG/Reuters, MT Newswires, Bloomberg Media Distribution, HT Syndication, PTI). These vendors can grant display, summary and GenAI rights for content they own or have sublicensed. Dow Jones states that Factiva holds GenAI rights from 8,000+ sources (M). Benzinga states that its news API is "fully embeddable" (M).
2. **Public-sector sources are the cheapest way to get licensed "details".** These include SEC EDGAR, FRED (excluding third-party-copyrighted series), World Bank (CC BY 4.0), India GODL data, PIB releases, and SEBI/RBI/MoSPI. Watch the exceptions: FRED third-party series and IMF commercial reuse both need permission.
3. **NSE/BSE websites cannot be scraped.** NSE's Terms of Use prohibit "systematic or automated data collection (including scraping…)". Bulk, block, insider and announcement data for India must come from a licensed vendor (NSE Data & Analytics, C-MOTS/Capitaline, Accord, TrueData, or similar), even at pilot stage.
4. **Most cheap prices are non-commercial.** This applies to Massive's $29–$199 plans and its $99 Benzinga add-on ("individual use only"), Tiingo's $50 tier (internal commercial use only), EODHD's personal plans, the Finnhub free tier, the NewsAPI.org Developer plan (dev only), and all FMP plans unless you sign a separate Data Display and Licensing Agreement.
5. **Sentiment is not the same as returns.** The best evidence (Lopez-Lira & Tang, JFE, arXiv v6 2025-10-28) finds that GPT-4 headline scores capture the *non-tradable* initial reaction (about 90% portfolio-day hit rate) and predict some drift, mostly in small stocks and negative news. Returns decline as LLM adoption rises. Look-ahead bias and a "distraction effect" (Glasserman & Lin) contaminate backtests.
6. **SEBI regulatory exposure in India.** SEBI's finfluencer rules (Aug–Oct 2024, with a Jan 2025 clarification) bar unregistered persons from naming a security while using the last 3 months of price data to indicate a future price or recommendation. An assistant that does this for Indian users may fall under Research Analyst (RA) or Investment Adviser (IA) rules. This is an **open legal question** and needs counsel.

---

## 1. Rights framework used in every row

For each source, the table separates:
- **(a) Software/service licence**: the API subscription.
- **(b) Data rights**:
  - display: headline / snippet / full text;
  - internal vs external use;
  - storage and retention;
  - derived data, including LLM summaries and sentiment scores;
  - redistribution, including user exports.

"Unverified → Q#" points to a vendor question in §9.

---

## 2. Global news APIs

| Source | Class | Coverage / langs | Latency | Price (estimate, formula) | Software licence | Display / summary / storage / export | Conf |
|---|---|---|---|---|---|---|---|
| **NewsAPI.org** | Aggregator | Global web news | Dev: 24h delay; paid: real-time | Dev $0 (dev env only); Business $449/mo (250k req, overage $0.0018/req); Advanced $1,749/mo (2M req, overage $0.0009); Enterprise quote | Dev plan "cannot be used in a staging or production environment" | Publisher text not licensed. Headline + snippet + link is the realistic ceiling. Summaries: unverified → Q1 | H (pricing) / L (display) |
| **Marketaux** | Aggregator | 5,000+ sources, 80+ markets, 30+ langs, entity tagging | "Instant" (vendor claim) | Free (100 req/day, 3 articles/req); $29 / $49 / $99 / $199 per month (20% off annual) | Commercial terms not stated on pricing page | Unverified → Q2. Entity sentiment scores exist (M, from docs, not re-read) | H (pricing) |
| **NewsAPI.ai (Event Registry)** | Aggregator + NLP | 150,000+ outlets, 50+ langs, archive from 2014 | Near real-time (not quantified) | Free 2,000 searches; "5K" plan $90/mo; token pricing (recent search = 1 token; historical = 5 tokens/yr searched) | Monthly auto-renew; tokens expire | Unverified → Q3 | H (pricing) |
| **Webz.io** | Aggregator / crawler | 350k+ sources, 170+ langs, 200+ countries | Near real-time | PAYG ≈ $0.01/request + $0.005/record, $5/mo free credit; enterprise quote | Unverified | Unverified → Q4 | L (primary pricing page not fetched) |
| **GDELT 2.0** | Open index (metadata, tone, events) | 100+ langs monitored, 65 machine-translated | **15-minute** updates (Events, Mentions, GKG) | $0 | "Unlimited and unrestricted use for any academic, commercial, or governmental use… without fee", with citation + link required | Covers GDELT's *own* fields (tone, themes, events, URLs). The **linked articles** remain third-party copyright, so show link-out only | H |
| **Finnhub news + news-sentiment** | Aggregator | Global companies | Real-time (vendor claim) | Free tier personal/non-commercial; paid plans per dataset; "All-in-One" ≈ $3,500/mo (L) | Free tier non-commercial | Unverified → Q5 | M/L (pricing page not rendered) |
| **Tiingo News** | Aggregator (curated) | US-centric | Real-time | Power $30/mo (individual); **Internal Commercial $50/mo or $499/yr**; **Redistribution: custom** | Internal use = "sharing or displaying data to others is prohibited" | End-user display needs the Redistribution tier → Q6 | H |
| **Benzinga (direct)** | Licensed content | US equities; 200+ full stories + ~1,000 pieces/day (vendor claim) | Real-time REST / TCP / RSS | Quote only. AWS Marketplace "Basic" free tier (headline + teaser + link) | Vendor licence | Vendor says the news API is "fully embeddable… publish the entire headline, body, and picture". LLM summaries, retention and export unverified → Q7 | M |
| **Massive (ex-Polygon) + Benzinga** | Reseller of Benzinga | US | Real-time Benzinga news (launched "in October", year not stated, M) | Individual plans $29–$199 + Benzinga $99/mo = **individual use only**. Business: **$2,499/mo** base; Benzinga on Business = "contact for pricing"; Financials & Ratios $699/mo | Individual plans restricted to non-professionals | Business display rights unverified → Q8 | H (pricing) |
| **Dow Jones Factiva / DNA (Snapshots, Streams) / Newswires** | Licensed content | 8,000+ sources cleared for GenAI (total source count unverified) | Streams via Pub/Sub, real-time | No public price; quote only (Q9) | Enterprise licence | GenAI/RAG rights with usage-based publisher royalties (vendor/press, M). Summary display to paying retail users → Q9 | M |
| **LSEG / Reuters MRN, Headlines Direct** | Licensed content | 12+ langs, 45,000+ companies, low latency, with analytics (novelty, relevance) | Ultra-low latency | No public price; quote only (Q10) | Enterprise licence | MRN is aimed at machine / non-display use. Retail display needs a separate Reuters media licence → Q10 | M |
| **Bloomberg (B-PIPE / Enterprise / Media Distribution)** | Licensed content | Global | Real-time | Quote only | Terminal and B-PIPE licences restrict display to entitled users (general knowledge, L). Media Distribution syndicates text to publishers in 130+ countries (M) | Retail app display only via a Media Distribution deal → Q11 | M/L |
| **RavenPack / Bigdata.com** | Analytics + licensed "Premium News" | Global | Real-time | Bigdata.com: pay per token, example workflows $0.57–$1.82 per run; content-set subscriptions; enterprise custom licensing. RavenPack feed: quote | Usage-based | Redisplay of Premium News text unverified → Q12 | H (Bigdata pricing page) / M |
| **Aylien → Quantexa News API** | Aggregator + NLP | 80k+ sources | – | Unclear. Sign-ups reportedly redirected (L) | – | Product status unclear → Q13 | L |
| **Alexandria Technology** | Analytics (sentiment) | – | – | Quote only | – | **Not researched / unverified** | – |
| **Moneycontrol / Economic Times / Business Standard / Mint** | Publishers (India) | English + Hindi | – | Syndication quote only. HT Syndication (Mint/HT + ~200 publications) licenses "for use in any digital or print medium" (M). No public ET, Moneycontrol or BS API was found | – | Summaries need an explicit syndication licence → Q14 | M/L |
| **PTI / IANS** | Wire (India) | English + Hindi | Real-time | Subscription quote only. PTI reportedly has historically not licensed to websites (L) | – | → Q15 | L |
| **PIB press releases** | Public | English + Indian languages | Same day | $0 | – | PIB copyright policy: "may be reproduced free of charge… no need for any prior approval". Source must be acknowledged; third-party material is excluded | M |
| **SEBI / RBI press releases, circulars** | Public | English/Hindi | Same day | $0 | – | Copyright pages not fetched. Linking and summarising factual releases is low-risk but unverified | L |

## 3. Sentiment

### Vendor sentiment
| Vendor | What | Conf |
|---|---|---|
| **LSEG MarketPsych Analytics** | 100k+ companies, 4,000+ news/social sources, 12 langs, 100+ scores per asset (Fear, Uncertainty, etc.), history from 1998; refreshes every 60s, hourly and daily. Quote only | M |
| **RavenPack** | Entity-level relevance, novelty and event sentiment. Quote only; Bigdata.com offers token-based API access | M |
| **Bloomberg** | News and social sentiment on the Terminal and in Enterprise data. Quote only | L |
| **Benzinga** | Via partners. Sentiment product scope unverified | L |
| **Finnhub / Marketaux** | Cheap entity or news sentiment scores. Methodology undisclosed; treat as a feature, not a signal | M |

### Open models
- **FinBERT (ProsusAI) and variants**: English, trained on Financial PhraseBank. Cheap to self-host.
- **FinBERT2 (arXiv 2506.06335)**: fine-tuned discriminative encoders "outperform leading LLMs by 9.7%–12.3% on average across five financial classification tasks". **Caveat: this is a Chinese-language model**, trained on 32B Chinese financial tokens, so it is not directly usable for English or Hindi. (H, abstract read)
- **FinSentLLM (arXiv 2509.12638)**: an ensemble of multiple LLMs with structured signals, reporting about 98% on FPB (search snippet, **not verified against the PDF**).
- **Multilingual / Indic**: MuRIL (17 Indian languages plus transliterated text) and IndicBERT (12 languages, AI4Bharat). **There is no well-established public Hindi financial-sentiment benchmark.** The one Hindi stock-tweet study found (Springer) reports 72% test accuracy with an LSTM (M). Plan to label your own Hindi and Hinglish evaluation set.

### LLM sentiment: evidence and caveats
- **Lopez-Lira & Tang** (arXiv 2304.07619 v6, 2025-10-28; JFE): GPT-4 achieves about a 90% portfolio-day hit rate on the **non-tradable** initial reaction. Scores predict subsequent drift, especially for small stocks and negative news. Predictability falls as LLM adoption rises. (H)
- **Glasserman & Lin** (arXiv 2309.17322, 2023): in-sample, anonymised headlines outperform, meaning the **distraction effect** (the model's prior knowledge of the company) outweighs look-ahead bias, most strongly for large caps. The authors recommend anonymising names for backtests and live use. (H)
- **Practical caveats**:
  - Sentiment is not the same as expected return, and most of the edge sits in the first minutes after news.
  - Backtests on data from before the model's cutoff are contaminated.
  - Duplicates or reposts of the same story inflate the signal.
  - Sentiment on regulatory filings behaves differently from sentiment on news.
  - Any "bullish/bearish" label shown to Indian users is exposed to SEBI RA rules (see §0.6).

## 4. Fundamentals, estimates, ownership

| Source | Coverage | Price (estimate) | Display/redistribution | Conf |
|---|---|---|---|---|
| **FactSet, S&P Capital IQ, LSEG, Morningstar** | Global, institutional | No public price; quote only (enterprise contact-sales) | Redistribution licence required | L – list only |
| **Koyfin** (reference point) | Uses **S&P Capital IQ** (fundamentals, estimates, valuation), Morningstar (funds), FRED and Trading Economics (macro), plus "over a dozen" vendors | – | Shows that CapIQ can be licensed for retail display at scale | H (Koyfin FAQ) |
| **TIKR** (reference point) | S&P Global Capital IQ (+ Morningstar per third-party sources) | – | Same | M |
| **EODHD** | 1985+ US, 2000+ non-US fundamentals, insider transactions, news, calendar | Fundamentals $59.99/mo; All-in-One $99.99/mo (personal). Commercial use requires the "Startups & Enterprise" plan (quote) | → Q16 | H |
| **FMP** | Global fundamentals, estimates, insider, 13F, M&A feeds | $22 / $59 / $149 per month (annual, L). Build and Enterprise plans exist | Public display requires a **Data Display and Licensing Agreement** (FMP ToS/FAQ, M) → Q17 | M |
| **Finnhub** | 65k+ companies, estimates, transcripts, ownership, insider, congressional trades | Per dataset; All-in-One ≈ $3,500/mo (L) | → Q5 | M/L |
| **Tiingo fundamentals** | US | Add-on; supplied through a third-party provider | → Q6 | H |
| **Massive Financials & Ratios** | US | $29/mo individual; $699/mo business | → Q8 | H |
| **India: Capitaline (C-MOTS)** | 35,000+ companies; fundamentals, corporate actions, announcements, news | Quote only | Redistribution contract required | M |
| **India: ACE Equity (Accord Fintech)** | 40,000+ companies, 1,750 fields; FTP/API feed that includes announcements, news, corporate actions; authorised BSE/NSE vendor | Quote only | → Q18 | M |
| **India: CMIE Prowess IQ** | 37,780 companies | Single-user, "hits"-metered subscription | Research licence; redistribution unlikely (L) | M |
| **India: Screener.in data origin** | Reported as C-MOTS / Capitaline. **Sources conflict** | – | – | L |
| **India: Tickertape data origin** | Not found | – | – | unverified |
| **India: Trendlyne** | Consumer plans ₹310/mo (GuruQ), ₹5,900/yr (StratQ). **No public data-licensing API terms found** | – | → Q19 | L |

## 5. Macro and economic calendars

| Source | Free / licensed | Terms (key clause) | Conf |
|---|---|---|---|
| **FRED API** | Free | Commercial apps allowed but may not "replicate… the essential user experience of FRED". **Third-party-owned series require the owner's permission.** Must display "This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis". Rate limits at the Fed's discretion | H |
| **World Bank** | Free | CC BY 4.0, commercial use allowed with attribution | M |
| **IMF** | Free to access | Commercial reuse requires emailing copyright@imf.org for permission | M |
| **Trading Economics API** | Licensed | Standard ≈ $149/mo, Professional ≈ $299/mo (annual, L); price scales with "the distribution you make". Trial: 100k data points / 100 requests. Includes calendar, indicators and news | H (trial terms) / L (prices) → Q20 |
| **MoSPI eSankhyiki** | Free | API over NAS, CPI, IIP and ASI (10 yrs); beta MCP server (MIT source). GODL-India applies to govt data: royalty-free, commercial use and derivatives allowed, attribution required | M |
| **RBI DBIE** | Free download (Excel/CSV/PDF) | **No official public API found** (M). Third-party wrappers exist. Check RBI site terms before automating | M |
| **data.gov.in** | Free | GODL-India | M |

## 6. Deals: M&A, bulk/block, insider

| Source | Notes | Price | Conf |
|---|---|---|---|
| **SEC EDGAR** (8-K, SC 13D/G, Forms 3/4/5, 13F) | Free and public. **10 requests/second** fair-access limit; a declared User-Agent is required. Indexes update nightly. Filings after 5:30 pm ET are disseminated next business day. Real-time **PDS** feed is fee-based. JSON via data.sec.gov | $0 (PDS: fee, quote) | H |
| **Filing deadlines** (8-K, Form 4, 13D) | Unverified in this pass; confirm on sec.gov before using them for latency design | – | unverified |
| **NSE/BSE bulk and block deals** | Bulk deal = over 0.5% of equity in a day. **Block deals: SEBI circular SEBI/HO/MRD/POD-III/CIR/P/2025/134 of 2025-10-08**: minimum ₹25 cr (up from ₹10 cr, set 2017); windows 8:45–9:00 and 2:05–2:20; ±3% band; delivery mandatory; effective 2025-12-07; exchanges disclose after hours the same day | Data via licensed vendor | M (secondary legal sites; circular itself not opened) |
| **NSE website** | ToU prohibits "systematic or automated data collection (including scraping, data mining, data extraction and data harvesting)". Market data is licensed through **NSE Data & Analytics**; no redistribution except as agreed | Quote | M |
| **BSE insider (SEBI PIT) and SAST disclosures** | Public web pages; data is from depositories and BSE disclaims accuracy. Vendor APIs (stockinsights.ai and others) sell tagged announcement feeds. A forum reports BSE announcement feeds at about ₹3 lakh/yr | Quote / L | L |
| **Refinitiv/LSEG Deals, Mergermarket, PitchBook** | Institutional M&A databases | Quote only; not affordable at pilot stage | L |
| **Crunchbase API** | Free tier gone; requires an Enterprise or Applications licence, reportedly $50k+/yr | Quote | L |
| **FMP / Finnhub M&A and insider endpoints** | Cheap, derived from EDGAR | See §4 | M |

## 7. Social and alternative data

| Source | Status / price | Rights | Conf |
|---|---|---|---|
| **X API (pay-per-use, launched 2026)** | Post read **$0.005**; user read $0.010; post create $0.015 ($0.20 with a URL); capped at **3M post reads per month**, above that Enterprise. Up to 20% back in xAI credits | Developer Agreement (last updated 2026-04-27):
- §II(A)(2): display of "a reasonable amount" of X Content is allowed, subject to the Display Requirements.
- **§III(A)(k): may not "use the X API or X Content to fine-tune or train a foundation or frontier model".**
- §III(A)(l): no off-X ad targeting using X Content or derivative analysis.

Developer Policy: keep displayed content intact; **delete or modify within 24h** when content changes on X; no storage of DMs. → Q21 | H |
| **Reddit Data API** | Free non-commercial (100 QPM per OAuth client, manual approval). Commercial use needs a separate contract: reportedly $0.24 per 1k calls or about $12k/mo for 50M calls | The Data API Terms reportedly bar commercial use without a separate licence. **Primary page could not be fetched** | L |
| **Stocktwits API** | Developer page: "not accepting new registrations" while under review (M) | – | M |
| **Telegram (India channels)** | SEBI actively acts against unregistered tip channels (e.g., SCN dated 2025-11-24). Since Feb 2026, regulated entities must show their SEBI registration number on social posts (secondary sources) | Ingesting tip channels risks amplifying unregistered advice. Do not surface these as signals | M |
| **YouTube finfluencers** | YouTube API ToS not researched. SEBI's Aug 2024 rules bar regulated entities from associating with unregistered finfluencers | – | unverified |

## 8. Recommended stack (estimates; costs as formulas)

### Prototype (internal, not user-facing). ≈ $0–$250/mo
- **News**: GDELT (free, 15-min, link-out only) + NewsAPI.ai 5K ($90) or Marketaux Standard ($49) for entity-tagged headlines.
- **Filings / deals (US)**: SEC EDGAR (free, 10 rps).
- **Macro**: FRED, World Bank, MoSPI eSankhyiki, PIB (free, with attribution).
- **India deals**: no free lawful automated source. Use a vendor trial, or wait for the pilot.
- **Sentiment**: self-hosted FinBERT + LLM scoring with anonymised entities; build a labelled English + Hindi eval set.
- `Cost ≈ 0 + NewsAPI.ai(90) + Marketaux(0–49) + LLM_tokens`

### Pilot (paying users, US + India). ≈ $3k–$6k/mo + quotes
- **US news with display rights**: Benzinga direct (quote), or Massive Business ($2,499) + Benzinga (quote).
- **Headline-only breadth**: NewsAPI.org Business ($449).
- **Fundamentals**: FMP Display Agreement (quote), or EODHD Startups plan (quote), or Tiingo Redistribution (quote).
- **Macro calendar**: Trading Economics Standard/Pro ($149–$299, distribution tier TBC).
- **India**: C-MOTS/Capitaline or Accord ACE feed for fundamentals, corporate actions, announcements, bulk/block and insider data (quote).
- **Social**: X pay-per-use.
- **Cost formula**:
  `Monthly ≈ Benzinga_quote (or 2,499 + Benzinga_addon_quote) + 449 + Fundamentals_display_quote + TE(149–299) + India_vendor_quote + 0.005 × X_posts_read + 0.010 × X_users_read + LLM_tokens`
  Add `exchange_display_fees × users` only if quotes are shown (see 04-real-time-data-strategy §6).

**Pilot gap: India and global news display rights.**
- At pilot, only US news (Benzinga) has a vendor-stated display path.
- India and global news at pilot means:
  - headline + snippet + link-out from aggregators (NewsAPI.org, Marketaux, NewsAPI.ai, GDELT);
  - exchange announcements through the licensed Indian vendor;
  - PIB/SEBI/RBI releases.
- Licensed Indian and global publisher text, and AI summaries of that text, come only at scale, or earlier if Q14, Q15 or Q18 come back positive.

**Scope note.** The detector data spec in 06-quantitative-validation §1 (consolidated, full-volume, 1-minute bars, displayable) applies to price feeds, not to the news, fundamentals or macro sources covered here. Price feeds are out of scope for this note. The Massive Business base plan is listed only as the route to Benzinga.

### Scale (global, multilingual)
- Dow Jones Factiva DNA/Streams with GenAI rights.
- LSEG MarketPsych or RavenPack for sentiment.
- S&P Capital IQ or FactSet fundamentals under a retail-display licence (the Koyfin/TIKR model).
- HT Syndication or PTI for Indian publisher text.
- X Enterprise.
- `Cost = Σ enterprise quotes (fixed + per_user × users)`

### Realistically NOT affordable (pre-Series A)
These are judged by what was observed: enterprise-only, no self-serve price, contact-sales. The dollar amounts were not verified.
- Bloomberg B-PIPE / Enterprise display.
- LSEG MRN / Headlines Direct.
- Dow Jones low-latency Newswires.
- FactSet / Capital IQ / LSEG / Morningstar redistribution.
- Mergermarket, PitchBook, LSEG Deals.
- Crunchbase API (enterprise-only; reported ≈ $50k+/yr, L).
- Reddit commercial (reported ≈ $12k/mo, L).
- X Enterprise (above 3M reads per month).
- RavenPack full feed.

## 9. Vendor questions (drafts for the user to send; not sent)

- **Q1 NewsAPI.org**: "On the Business plan, may we display article titles, descriptions and URLs to paying end users of a commercial app? May we store returned metadata indefinitely? Do you grant any rights to generate and display AI summaries of the underlying articles, or must that be licensed from each publisher?"
- **Q2 Marketaux**: "Do your paid plans permit displaying headlines, snippets and your entity sentiment scores to paying end users? Are there retention limits on stored articles and scores? Is user export (CSV) permitted?"
- **Q3 NewsAPI.ai / Event Registry**: "Which plan permits external display to paying users? Does any plan convey rights to article body text or to AI summaries derived from it? What is the typical publish-to-API latency?"
- **Q4 Webz.io**: "Please confirm current per-request and per-record prices and whether returned full text may be summarised and shown to paying end users."
- **Q5 Finnhub**: "What is the price of a commercial licence covering news, news sentiment, fundamentals, estimates and insider transactions displayed to up to N paying users? Is derived data (our own scores) freely redistributable?"
- **Q6 Tiingo**: "Please quote the Redistribution tier for news + EOD + fundamentals displayed to N end users in India and the US, including retention and export terms."
- **Q7 Benzinga**: "Does a display licence permit showing AI-generated summaries of Benzinga articles to paying end users? May full text and summaries be cached beyond N days? May users export them? What is the pricing formula (fixed + per user)? Are analyst ratings, guidance and earnings included?"
- **Q8 Massive**: "On Stocks Business ($2,499/mo), what is the Benzinga add-on price? Does it include rights to display news and AI summaries to paying end users? What exchange fees apply if we show only news and fundamentals, not quotes?"
- **Q9 Dow Jones Factiva**: "For a retail-facing AI assistant, which Factiva sources carry GenAI summary display rights? What is the pricing model (per query or royalty)? What are the minimum commitment and retention rules?"
- **Q10 LSEG**: "Is there a Reuters news licence permitting AI summaries displayed to retail end users, separate from MRN non-display? What is the minimum annual commitment?"
- **Q11 Bloomberg Media Distribution**: "Do you license Bloomberg News text or summaries to third-party retail fintech apps? What are the terms and minimums?"
- **Q12 RavenPack / Bigdata.com**: "May Premium News content or excerpts retrieved via Bigdata.com be displayed to our paying users, or only used for internal analysis? Are RavenPack sentiment scores redistributable as a derived signal?"
- **Q13 Quantexa**: "Is the Aylien/Quantexa News API still accepting new commercial customers? What are the pricing and display terms?"
- **Q14 HT Syndication / Times / Business Standard**: "Please quote a digital licence to display headlines plus AI-generated summaries (≤N words) with link-back to paying users, including Hindi content, retention and archive rights."
- **Q15 PTI**: "Does PTI license its English/Hindi business wire to digital apps for summary display? What are the pricing and attribution requirements?"
- **Q16 EODHD**: "Please quote the Startups plan for fundamentals, news, calendar and insider data displayed to N paying users, with retention and export terms."
- **Q17 FMP**: "What does a Data Display and Licensing Agreement cost for fundamentals, estimates, insider trades and M&A data shown to N paying users? Does it cover Indian companies?"
- **Q18 C-MOTS/Capitaline and Accord (ACE)**: "Please quote an API/FTP feed of Indian fundamentals, corporate actions, announcements, bulk/block deals and SEBI PIT/SAST disclosures, with rights to display to paying end users and to generate AI summaries, plus latency after exchange dissemination. Your feed lists a news component: does that news carry rights to display it and to show AI summaries of it to paying users?"
- **Q19 Trendlyne**: "Do you offer a B2B data API (analyst targets, insider/bulk deals, fundamentals)? What are the redistribution terms and pricing?"
- **Q20 Trading Economics**: "Which plan permits displaying the economic calendar and indicators to paying end users of a third-party app? What is the price formula for distribution?"
- **Q21 X**: "Under pay-per-use, may we display AI-generated summaries and sentiment scores derived from posts to paying users? Does §III(A)(k) also cover fine-tuning a small sentiment classifier, which is not a foundation model? What are the enterprise pricing and terms above 3M post reads per month?"
- **Q22 NSE Data & Analytics**: "Please share the licence and fees for corporate announcements, bulk/block deals and insider-trading disclosure data for display in a retail app, and any non-display fee."

## 10. Unverified items / gaps
- FMP, Finnhub and Trading Economics prices come from snippets or third-party sources (their pricing pages were blocked or did not render).
- Webz.io PAYG rates (primary pricing page not fetched).
- Reddit pricing and terms (redditinc.com could not be fetched).
- X Display Requirements document (not fetched).
- Factiva total source count.
- Block-deal circular (confirmed via secondary legal sites; sebi.gov.in PDF not opened).
- NSE Data Usage & Sharing Policy PDF (timed out; the scraping ban comes from a ToU search snippet).
- SEBI, RBI and BSE website copyright/terms.
- Screener data origin (C-MOTS vs Capitaline conflict) and Tickertape data origin.
- Alexandria, IANS, Moneycontrol/ET/BS licensing.
- MarketPsych and RavenPack prices.
- FinSentLLM figures (snippet only).
- Hindi financial-sentiment benchmark availability.
- YouTube API ToS.
- SEC filing deadlines (from general knowledge).
- Whether the assistant's Indian-stock outputs trigger SEBI RA/IA registration (legal counsel needed).

## Sources (accessed 2026-09-24)
- NewsAPI.org pricing: https://newsapi.org/pricing
- Marketaux pricing: https://www.marketaux.com/pricing
- NewsAPI.ai plans: https://newsapi.ai/plans
- GDELT about/terms: https://www.gdeltproject.org/about.html ; 15-min & 65 langs: https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/
- Webz.io pricing: https://webz.io/pricing/ (via search)
- Tiingo pricing: https://www.tiingo.com/about/pricing
- Massive pricing: https://massive.com/pricing ; business: https://massive.com/business ; Benzinga partnership: https://massive.com/blog/benzingadata-partnership
- Benzinga news API: https://www.benzinga.com/apis/cloud-product/stock-news-api/ ; AWS listing: https://aws.amazon.com/marketplace/pp/prodview-xwgvhwowjmw3g
- EODHD pricing: https://eodhd.com/pricing
- FMP pricing/terms: https://site.financialmodelingprep.com/pricing-plans ; https://site.financialmodelingprep.com/developer/docs/terms-of-service
- Finnhub pricing: https://finnhub.io/pricing ; https://tradingdatacompare.com/providers/finnhub/
- Bigdata.com pricing: https://bigdata.com/pricing
- LSEG MRN: https://www.lseg.com/en/data-analytics/financial-data/financial-news-coverage/political-news-feeds-analysis/real-time-news
- MarketPsych: https://www.lseg.com/en/data-analytics/market-data/quantitative-economic-data-solutions/marketpsych-analytics-and-models
- Factiva GenAI sources: https://finance.yahoo.com/news/dow-jones-factiva-surpasses-8-110000805.html
- Bloomberg licensing: https://www.bloomberg.com/distribution/ ; https://www.bloomberg.com/help/question/how-can-i-license-bloomberg-content/
- Quantexa/Aylien: https://aylien.com/ ; https://newsapi.ai/blog/quantexa-aylien-news-api-alternative-comparison/
- HT Syndication: https://www.htsyndication.com/
- PTI: https://en.wikipedia.org/wiki/Press_Trust_of_India
- PIB copyright: https://www.pib.gov.in/content/102_2_Copyright-Policy.aspx?reg=3&lang=1
- GODL: https://www.data.gov.in/Godl
- FRED terms: https://fred.stlouisfed.org/docs/api/terms_of_use.html
- World Bank: https://datacatalog.worldbank.org/public-licenses ; IMF: https://www.imf.org/en/about/copyright-and-terms
- Trading Economics: https://tradingeconomics.com/api/pricing.aspx
- MoSPI eSankhyiki: https://www.pib.gov.in/PressReleaseIframePage.aspx?PRID=2029708 ; https://github.com/nso-india/esankhyiki-mcp
- RBI DBIE: https://data.rbi.org.in/
- SEC EDGAR access: https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
- NSE ToU: https://www.nseindia.com/static/nse-terms-of-use ; data policy: https://www.nseindia.com/static/market-data/nse-data-policy
- Block deal circular: https://www.taxmann.com/post/blog/sebi-revises-block-deal-framework-minimum-order-size-rs-25-crore ; https://mehta-mehta.com/sebi-circular-review-of-block-deal-framework-8th-october-2025/
- BSE announcements: https://www.bseindia.com/corporates/ann ; forum cost: https://tradingqna.com/t/corporate-announcement-data-api/178154
- Crunchbase: https://about.crunchbase.com/products/data-licensing ; https://pipeline.zoominfo.com/sales/crunchbase-api
- Koyfin data: https://www.koyfin.com/help/faq/where-do-you-get-your-data/ ; TIKR: https://support.tikr.com/hc/en-us/articles/5403705233947
- Capitaline: https://www.capitaline.com/ ; ACE: https://www.accordfintech.com/market-data-feed ; CMIE: https://prowess.cmie.com/ ; Trendlyne: https://trendlyne.com/subscription/plans/
- X pricing: https://docs.x.com/x-api/getting-started/pricing ; X policy: https://docs.x.com/developer-terms/policy ; X agreement: https://docs.x.com/developer-terms/agreement
- Reddit: https://www.socialcrawl.dev/blog/reddit-data-api-2026 (secondary, L)
- Stocktwits: https://api.stocktwits.com/developers
- SEBI finfluencer: https://www.medianama.com/2024/09/223-sebi-regulated-firms-barred-from-collaborating-with-unregistered-finfluencers/ ; https://www.business-standard.com/markets/news/sebi-finfluencer-circular-live-stock-data-market-education-rules-125013000571_1.html
- SEBI Telegram action: https://www.medianama.com/2026/03/223-sebi-unregistered-advisor-telegram-social-media-scrutiny-complaint/
- Lopez-Lira & Tang: https://arxiv.org/abs/2304.07619 ; Glasserman & Lin: https://arxiv.org/abs/2309.17322 ; FinBERT2: https://arxiv.org/abs/2506.06335 ; FinSentLLM: https://arxiv.org/pdf/2509.12638
- Indic NLP: https://github.com/AI4Bharat/indicnlp_catalog ; Hindi tweets: https://link.springer.com/chapter/10.1007/978-981-99-0835-6_17
