# Feature-by-feature legal posture: what is achievable in India, and on what conditions

Author role: Compliance Analyst (Governance). Research and access date for every source: **2026-09-24**.

**This is not legal advice.** It sorts risks and drafts questions. Anything marked **CQ-n** goes to Indian securities counsel through the owner.

**Labels** (house rules):
- [F] verified fact from a primary page that was read;
- [F-sec] fact from a secondary source or a search extract, because the primary page returned only headers or an unreadable PDF;
- [I] inference; [A] assumption; [E] estimate; [P] proposal.

Confidence is H, M or L.

**Scope rule.** This file does not repeat data-licence costs (NSE/BSE tariffs, broker API terms, Kite), news-licence analysis or enforcement case facts. Those are in:
- `research/india-market-data-and-sebi.md` (called "IMD" below);
- `research/kite-and-broker-apis.md`;
- `research/case-studies.md` ("CS");
- `16-india-research-round-3.md`;
- `14-global-market-assistant.md` §5.

In the tables below, the **posture** answers only the SEBI question: does this feature need registration? A separate **licence precondition** column points to the data rights, which are a different axis. A feature can be posture A and still unaffordable or unlicensed.

---

## 0. Headline findings

1. **[I, M] Most of the catalogue is posture A.** That covers descriptive data, computed values, factual records, backward-looking evidence, and alerts on thresholds the user sets. The conclusion is ours; it rests on two sourced points:
   - [F-sec, H] The RA Regulations reach a communication only when it contains "analysis or recommendation or an opinion on securities… providing a basis for investment decision" (S1, S4).
   - [F-sec, H] "Statistical summaries of financial data of the companies" and "technical analyses relating to the demand and supply in a sector or the index" are expressly excluded.
2. **[F-sec, H] The bright line is the output, not the price or the technology.** Four kinds of output need RA registration (B), even for a free product, because "consideration" includes any non-cash benefit "from client or otherwise" (S2):
   - buy/sell/hold on a named security;
   - price targets, and trading calls (added to "research services" in Dec 2024);
   - model portfolios and "top picks";
   - a buy/sell view on a single stock drawn from technical analysis (RA FAQs, S4).
3. **Personalisation turns B into C.**
   - [F-sec, M] Advice that uses the user's own circumstances is investment advice under the IA Regulations (S5).
   - [F-sec, M] The IA Regulations exclude advice "widely available to the public" through electronic media.
   - [I, M] That exclusion does not help us: such content falls back into the RA Regulations.
   - So an impersonal "buy X" is B, and "buy X because of your portfolio" is C.
4. **Correction to the brief: the "3-month education carve-out" is obsolete.** [F-sec, H]
   - SEBI's circular of 8 May 2026 (S9, effective 1 Jul 2026) replaced both the Jan 2025 three-month lag and the May 2024 one-day lag with **one 30-day lag**.
   - Scope [F-sec, M]: it defines who counts as "solely engaged in education" for the **association** rules, and governs how MIIs and intermediaries share price data for education.
   - It bars using price data from the last 30 days together with a security's name "in a manner indicating future prices, advice or recommendations".
   - [I, M] It is **not** a general ban on unregistered publishers showing live licensed prices. It is **not** a route to giving advice under an "education" label either: SEBI's Sathe and Patel orders treated "education" with calls as unregistered advice (CS §3.1).
5. **Correction: the Aug 2024 item is a regulation, not a circular.**
   - The rule is Reg 16A of the Intermediaries Regulations, notified 29 Aug 2024 (S6).
   - The implementing circulars are dated **22 Oct 2024** (S7) and **29 Jan 2025** (S8).
   - Reg 16A binds **regulated entities** (brokers, RAs, IAs, MIIs), not us. It bars them from "association" with anyone who gives unregistered advice or makes return/performance claims.
   - [F-sec, M] "Association" includes money or money's worth, client referral, **interaction of IT systems** and sharing client information (S8).
   - [I, H] Every broker API integration or partner deal therefore depends on us staying in posture A and making **no performance claims**.
6. **[F-sec, H] Performance claims are now a regulated channel.**
   - The PaRRVA framework was operationalised on 29 Apr 2026 (S15). CARE Ratings is the agency and NSE is its data centre.
   - After the cut-over, only PaRRVA-verified IAs and RAs may show past performance.
   - Enrolment for IAs and RAs was extended to **3 Sep 2026** (S16).
   - [I, H] An unregistered product can't use PaRRVA, so it must make **no past-performance or accuracy claims at all**. That includes backtest leaderboards, "our alerts were right 80% of the time" and marketplace returns.
7. **[I, H] Two features are legally achievable but banned by this project:**
   - model forecasts, which are legally B;
   - order placement, which is legally C.

   CLAUDE.md invariants (numbers from code only; no forecasts; no order-placing code) make both **D for this project**. Both postures are stated below so the owner sees the difference.
8. **Privacy.**
   - **Today:** IT Act s.43A, the SPDI Rules 2011 and the CERT-In 2022 Directions apply. The CERT-In Directions require **6-hour** incident reporting and 180 days of logs kept in India.
   - **From 13 May 2027:** the DPDP Act and Rules replace s.43A and the SPDI Rules. They bring notice, consent, safeguards and breach reports (Board "without delay", details within 72 h; users "without delay").
   - A **DPO is mandatory only for a Significant Data Fiduciary**. A small app must still publish a contact person.
   - MeitY's Jan 2026 plan to bring the deadline forward is a **proposal**; it was not confirmed as notified.

---

## 1. Authorities (cite by S-ID)

All accessed 2026-09-24. "Page headers only" means the sebi.gov.in HTML returned the title but not the body, so its content comes from the listed secondary source.

| ID | Authority | URL | Label, conf. |
|---|---|---|---|
| S1 | SEBI (Research Analysts) Regulations 2014, **last amended 6 Aug 2025** (consolidated). Research-report definition and exclusions | https://www.sebi.gov.in/legal/regulations/aug-2025/securities-and-exchange-board-of-india-research-analysts-regulations-2014-last-amended-on-august-6-2025-_96110.html | [F-sec, M]. Listing seen; definition text taken from secondary extracts. **The content of the Aug 2025 amendment was not checked** |
| S2 | RA (Third Amendment) Regulations, 16 Dec 2024. "Consideration" includes non-cash benefit; trading calls; deposit; AI disclosure; qualifications | https://www.sebi.gov.in/legal/regulations/dec-2024/securities-and-exchange-board-of-india-research-analysts-third-amendment-regulations-2024_89979.html ; summaries https://complisec.in/?p=854 , https://www.compliancecalendar.in/learn/sebi-ra-registration-process-fees-after-3rd-amendment-regulations-2024 | [F-sec, H] |
| S3 | Guidelines for Research Analysts, circular SEBI/HO/MIRSD/MIRSD-PoD-1/P/CIR/2025/004, 8 Jan 2025. Fee cap, advance fee, AI disclosure, MITC | https://www.sebi.gov.in/legal/circulars/jan-2025/guidelines-for-research-analysts_90634.html ; https://taxguru.in/sebi/sebi-clarifies-rs-1-51-lakh-fee-cap-research-analysts.html | [F-sec, H] |
| S4 | RA FAQs, circular SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/105, 23 Jul 2025. Exclusions; technical analysis on a single security is covered | https://www.sebi.gov.in/sebi_data/faqfiles/jul-2025/1753269723942.pdf (PDF not machine-readable here) ; https://taxguru.in/sebi/comprehensive-analysis-sebi-s-faqs-research-analysts.html | [F-sec, M]. **FAQ numbering comes from the secondary source** |
| S5 | SEBI (Investment Advisers) Regulations 2013, last amended 16 Dec 2024. Advice "widely available to the public" is excluded; NISM X-A/X-B; deposit | https://www.sebi.gov.in/legal/regulations/dec-2024/securities-and-exchange-board-of-india-investment-advisers-regulations-2013-last-amended-on-december-16-2024-_90151.html | [F-sec, M] |
| S6 | Intermediaries (Amendment) Regulations 2024 (Reg 16A), 29 Aug 2024 | https://www.sebi.gov.in/legal/regulations/aug-2024/securities-and-exchange-board-of-india-intermediaries-amendment-regulations-2024_86338.html | [F-sec, H] |
| S7 | Circular "Association of persons regulated by the Board and their agents with certain persons", Oct 2024 | https://www.sebi.gov.in/legal/circulars/oct-2024/association-of-persons-regulated-by-the-board-and-their-agents-with-certain-persons_87837.html | [F-sec, M] |
| S8 | Circular SEBI/HO/MIRSD/MIRSD-PoD-1/P/CIR/2025/11, 29 Jan 2025. Details and clarifications on association; the "solely education" test; IT-system interaction counts as association | https://www.sebi.gov.in/legal/circulars/jan-2025/details-clarifications-on-provisions-related-to-association-of-persons-regulated-by-the-board-miis-and-their-agents-with-persons-engaged-in-prohibited-activities_91356.html ; https://taxguru.in/sebi/sebi-clarifications-association-persons-miis-prohibited-activities.html | [F-sec, M] |
| S9 | Circular HO/47/17/12(11)2025-MRD-POD3/I/11107/2026, 8 May 2026, "Norms for sharing and usage of price data for educational purposes". 30-day lag, effective 1 Jul 2026 | https://www.sebi.gov.in/legal/circulars/may-2026/norms-for-sharing-and-usage-of-price-data-for-educational-purposes_101293.html ; https://www.livelawbiz.com/securities-law/sebi/securities-and-exchange-board-of-india-revises-norms-sharing-and-usage-market-price-data-educational-purposes-533509 ; https://www.business-standard.com/markets/news/sebi-allows-30-day-lag-for-use-of-market-data-in-educational-content-126050801450_1.html | [F-sec, H] |
| S10 | Circular on real-time price data sharing, 24 May 2024 | https://www.sebi.gov.in/legal/circulars/may-2024/norms-for-sharing-of-real-time-price-data-to-third-parties_83572.html | [F-sec, M] (see IMD §1.1) |
| S11 | Retail algo framework, 4 Feb 2025 (SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013); extension of 30 Sep 2025; mandatory for all brokers from 1 Apr 2026 | https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html ; NSE FAQ https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAQ_Retail%20Algo_03112025_NSE.pdf ; https://zerodha.com/z-connect/business-updates/explaining-the-latest-sebi-algo-trading-regulations | [F-sec, H]. **Black-box algos need an RA-registered provider** |
| S12 | Circular of 2 Sep 2022, "Performance/return claimed by unregulated platforms offering algorithmic strategies for trading". Brokers must not refer to past or expected algo returns, or associate with platforms that do | https://www.sebi.gov.in/legal/circulars/sep-2022/performance-return-claimed-by-unregulated-platforms-offering-algorithmic-strategies-for-trading_62628.html | [F-sec, H] |
| S13 | NSE circular NSE/INVG/73992, 30 Apr 2026. Algo-provider empanelment detail | Cited by https://www.quantinsti.com/articles/algorithmic-trading-india/ | [F-sec, L]. Not opened |
| S15 | PaRRVA operationalisation, circular HO/38/14/(4)2026-MIRSD-POD/I/10557/2026, 29 Apr 2026 | https://www.sebi.gov.in/legal/circulars/apr-2026/operationalisation-of-past-risk-and-return-verification-agency-parrva-_101185.html ; https://www.outlookmoney.com/news/sebi-operationalises-parrva-framework-sets-deadline-for-advisers-to-verify-data-on-past-performance | [F-sec, H] |
| S16 | PaRRVA enrolment extended to 3 Sep 2026 (circular of Aug 2026) | https://www.sebi.gov.in/legal/circulars/aug-2026/extension-of-timeline-for-enrolment-with-parrva-as-specified-in-sebi-circular-no-ho-38-14-4-2026-mirsd-pod-i-10557-2026-dated-april-29-2026_103314.html ; https://www.outlookmoney.com/invest/sebi-extends-parrva-enrolment-date-for-investment-advisors-research-analysts | [F-sec, M]. **Conflict:** one secondary source gives 3 Aug 2026; the later circular gives 3 Sep 2026, which is used here |
| S17 | Interim certified-performance arrangement before PaRRVA, Oct 2025 | https://www.sebi.gov.in/legal/circulars/oct-2025/ease-of-doing-business-interim-arrangement-for-certified-past-performance-of-investment-advisers-and-research-analysts-prior-to-operationalisation-of-past-risk-and-return-verification-agency-parrv-_97556.html | [F-sec, M] |
| S18 | Circular of Feb 2026: regulated entities must show registered name and number on social-media profiles and on every securities post, effective 1 May 2026 | https://www.sebi.gov.in/legal/circulars/feb-2026/ease-of-doing-investment-eodi-disclosure-of-registered-name-and-registration-number-by-sebi-regulated-entities-and-their-agents-on-social-media-platforms-smps-_100005.html ; https://www.medianama.com/2026/02/223-sebi-mandates-registration-number-on-social-media/ | [F-sec, M] |
| S19 | SEBI consultation on responsible AI/ML use, 20 Jun 2025. Whether it was finalised was **not verified**; the SEBI chair said on 2026-06-12 that guidelines are still being worked on | https://www.sebi.gov.in/reports-and-statistics/reports/jun-2025/consultation-paper-on-guidelines-for-responsible-usage-of-ai-ml-in-indian-securities-markets_94687.html ; https://www.caalley.com/news-updates/indian-news/sebi-deploying-ai-to-track-influencers-and-insider-trading-in-real-time-tuhin-kanta-pandey | [F-sec, M] |
| S20 | DPDP Rules 2025 (notified 13–14 Nov 2025) | https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf ; Rule 7 text https://www.dpdpa.com/dpdparules/rule7.html | [F-sec, H] |
| S21 | MeitY proposal to accelerate (Jan 2026) | https://chambers.com/articles/meity-plans-to-cut-short-dpdp-compliance-timeline-and-notify-cross-border-restrictions-for-sdfs | [F-sec, M]. **Proposal only** |
| S22 | Section 43A and the SPDI Rules apply until s.44(2) of the DPDP Act commences on 13 May 2027 | https://www.legal500.com/intelligence/india/privacy/what-happens-to-existing-spdi-rules-after-full-dpdp-enforcement ; https://www.snrlaw.in/indias-digital-personal-data-protection-regime-takes-effect/ | [F-sec, M] |
| S23 | CERT-In Directions under s.70B(6), 28 Apr 2022: 6-hour reporting; 180-day logs in India | https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf ; https://www.cert-in.org.in/Directions70B.jsp | [F-sec, H] |
| S24 | Account Aggregator: a Financial Information User must be "registered with and regulated by any financial sector regulator" | https://financialservices.gov.in/account-aggregator-framework | [F-sec, M] |
| S30 | *Lowe v. SEC*, 472 U.S. 181 (1985): the publisher's exclusion. "Bona fide" means "genuine", containing "disinterested commentary and analysis". "General and regular circulation" means not "timed to specific market activity, or to events affecting or having the ability to affect the securities industry". The exclusion does not cover "hit and run tipsters" or "touts" | https://www.law.cornell.edu/supremecourt/text/472/181 (Justia returned 403) | [F, H] |
| S31 | *SEC v. Park* ("Tokyo Joe"), 99 F. Supp. 2d 889 (N.D. Ill. 2000): exclusion denied (not bona fide; not of general and regular circulation) | https://law.justia.com/cases/federal/district-courts/FSupp2/99/889/2290926/ | [F-sec, M] |
| S32 | SEC withdrawal of the predictive-data-analytics proposal, 12 Jun 2025 (Rel. 33-11377) | https://www.sec.gov/files/rules/final/2025/33-11377.pdf ; https://www.sec.gov/rules-regulations/2025/06/s7-12-23 | [F-sec, H] |
| S33 | FINRA Regulatory Notice 24-09 (GenAI); FINRA 2026 Oversight Report, GenAI section | https://www.finra.org/rules-guidance/notices/24-09 ; https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/gen-ai | [F-sec, H] |
| S34 | SEC AI-washing: Delphia and Global Predictions (2024-36); Rimar (2024-167); Saniger (LR-26282). FTC Operation AI Comply | https://www.sec.gov/newsroom/press-releases/2024-36 ; https://www.sec.gov/newsroom/press-releases/2024-167 ; https://www.sec.gov/enforcement-litigation/litigation-releases/lr-26282 ; https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes | [F-sec, M/H] (see CS §3.2) |

---

## 2. Cross-cutting guardrails for posture A (G-codes used in §3)

- **G1 Impersonal and canonical.** The same event or symbol gives the same content to every user. There is **one canonical explanation per event**. User choice of *which* symbols to watch is allowed; content that changes with *who* the user is is not.
- **G2 No recommendation vocabulary** in UI copy, LLM output, notifications, marketing or tool descriptions. Deny-list plus classifier (14 §5). Banned terms:
  - buy/sell/hold/accumulate/avoid/exit;
  - target, stop-loss, entry, "levels";
  - signal, call, trade idea, pick, "opportunity";
  - bullish/bearish as a verdict on a security;
  - undervalued/overvalued/fair value;
  - "strong", "weak" or star ratings on a security.
- **G3 No forward-looking statements** about a security's price. No "likely to", "expected to", "should rebound", and no ranges or probabilities.
- **G4 Descriptive naming.** Show computed values with their formula and threshold, for example "RSI(14) = 74; the conventional 70 threshold is exceeded". Do not show an interpretation such as "overbought → reversal".
- **G5 Claims discipline.**
  - **Banned:** return, hit-rate or performance claims about securities, alerts, screens, backtests or strategies ("our alerts were right 80% of the time"). Such claims make brokers unable to associate with us (S8, S12), and PaRRVA is closed to unregistered entities (S15).
  - **Allowed only with documented evidence:** operational and capability claims, such as delay labels, the share of answers with citations, and the fact that figures pass a numeric verifier. Unsubstantiated AI capability claims are the FTC s.5 and SEC AI-washing risk (S34).
- **G6 Evidence timing.** Every cited item carries `before_move`, `after_move_start` or `after_close_disclosure`. Use "coincided with", never "caused" (16 §4).
- **G7 Entitlement labels.** Every price shows its source, a real-time/delayed/EOD label and an `as_of` time. Delayed data is conspicuously labelled (CLAUDE.md invariant 1).
- **G8 Standing disclosure** on every surface: "Information only. Not investment advice or research. [Company] is not registered with SEBI as an Investment Adviser or Research Analyst. AI is used to select and phrase cited evidence; figures are computed by code."
  - [I, M] The Feb 2026 registration-number-per-post rule (S18) applies to **regulated** entities only. An unregistered publisher should **not** display anything that resembles a registration number.
  - CQ-1 asks counsel to approve this wording.
- **G9 LLM abstention.** Questions that ask for an opinion ("should I…", "is X a good buy", "what will X do") get a refusal template plus the relevant cards. Every such refusal is logged.
- **G10 Retail-harm UX.** No trending-buy lists, buzz scores, streaks or engagement mechanics. F&O and intraday cards carry a dated SEBI loss-statistics line (16 §4.7).
- **G11 No broker association that looks like distribution of advice.** Any broker deal needs the broker's own compliance sign-off under Reg 16A (S6, S8).

---

## 3. Feature catalogue

Posture key:
- **A:** an unregistered information publisher can offer it;
- **B:** needs RA registration or an RA partner;
- **C:** needs IA registration, broker or algo-provider empanelment, or exchange approval;
- **D:** not achievable, or too risky for this project.

"Licence precondition" points to the data-rights appendices; it is not part of the posture.

### 3.1 Market data and reference pages

| # | Feature | Posture | Deciding authority | Guardrails to stay in A | Flips to B/C if… | Licence precondition | Counsel | Conf. |
|---|---|---|---|---|---|---|---|---|
| 1 | Live or delayed price display | **A** | No SEBI registration applies. S10 limits *MIIs and intermediaries* sharing real-time data with third parties, aimed at gaming and virtual trading; it does not bar a licensed display | G7. No paper trading or virtual portfolios (vendor and S10 risk). Delayed data is never shown as live | Never, as a SEBI matter | NSE/BSE display licence via a vendor; category and cost are open (IMD §1.2–1.3, Q-NSE-1/2). Broker APIs can't be redisplayed (kite-and-broker-apis) | None on SEBI | H |
| 2 | Stock detail page (fundamentals, shareholding, corporate actions) | **A** | S1 excludes "statistical summaries of financial data of the companies" | Report ratios, growth and shareholding changes as numbers with period and source. No composite "quality/valuation score", no "fair value", no peer ranking framed as attractiveness | Adding a score, grade, star rating, intrinsic value or "undervalued" label makes it a research opinion → **B** | Corporate and fundamentals data vendor (IMD §4, Q-NSE-6). No scraping | CQ-2: may we show a *neutral* percentile ranking ("P/E is in the 80th percentile of sector")? | M |
| 3 | Historical charts | **A** | Same as #1 | G7. Adjusted or unadjusted is labelled (invariant 3) | Drawn-on "target zones", "support/resistance to trade" → B | Storage and retention rights for history (Q-NSE-5, Q-V-4) | None | H |
| 4 | Technical indicator values (RSI, MACD, moving averages…) | **A** | S1 plus S4: a buy/sell/hold on a *specific security* based on technical analysis is research; the values themselves are not | G4: values plus formula plus threshold. No "buy signal", "bullish crossover" or colour coding meant as "go/stop" | Interpretive verdicts on a single stock ("bullish", "trend reversal likely") → **B** | Non-display/derived-data fee if computed from real-time data (IMD Q-NSE-3) | CQ-3: are conventional state words ("overbought", "golden cross") used as neutral descriptors a recommendation? | M |
| 5 | Indicator-based screeners | **A** (user-built filters); **B** (curated "idea" screens) | S1/S4 as #4. A screen result is a list of securities meeting stated criteria | The user sets the criteria. Presets are named by their criteria ("RSI(14) < 30", "52-week high today"), not by an outcome ("Stocks to buy", "Bullish breakouts", "Multibaggers"). Sort by the user's chosen field; no "best match" ranking | Named outcome presets, editorial "screen of the week", or ranking by an attractiveness score → **B** | As #4, plus fundamentals licence | CQ-3 (preset naming) | M |
| 6 | Chart pattern detection ("head and shoulders found") | **B by default**; **A only in a narrow form** | The S1 exclusion covers technical analysis of a *sector or index*, not a single stock. Classic pattern names carry a conventional direction and often a "measured move" target | A-form: the user defines geometric criteria; the output is "pattern criteria met at [time]" with no direction, no target and no success-rate statistics. Index and sector patterns are safer (the S1 exclusion) | Any direction ("bearish H&S"), breakout level or target, or "historical success rate" → **B**; success rates also breach G5 | As #4 | **CQ-4: is naming a classic pattern on a single stock a "research analysis… providing a basis for investment decision"?** | L |
| 7a | News aggregation (headline + link + time) | **A** | No SEBI hook: this is third-party content | Headline verbatim, link and first-publication time. No editorial selection of "stocks in news to buy" | Adding our own view on the stock → B | Copyright and terms of each source (14 §1, CS §2 Perplexity). Headline-plus-link only unless licensed | None on SEBI | H |
| 7b | News summaries (AI) | **A** (SEBI); **licence-gated** | S1: a faithful summary of a third party's reporting is not *our* opinion on a security [I] | Summarise only what the article says, cite it, and attribute any opinion to the source ("Brokerage X says…"). Numbers must match the card (verifier) | Adding our own implication ("positive for the stock") → B | **Summary rights only from licensed sources** (14 §1; Dow Jones v. Perplexity) | CQ-5: does republishing a named brokerage's target price in a summary make us a research distributor? | M |
| 8 | Sentiment labels shown to users | **A** only as a per-item **text-tone** label | S1 [I]: a label of the *text* is not an opinion on the *security* | Label per headline ("tone of headline: negative", with model version). No per-stock aggregate "sentiment score", no bullish/bearish gauge, no link to expected price | A per-stock aggregated bullish/bearish score is effectively a view on the security → **B risk** | News licence as #7 | CQ-6. **Project conflict to raise:** CLAUDE.md invariant 5 bans LLM sentiment scores, while 14 §1 allows text labels. The tech-lead/owner should confirm that a per-item tone label from a pinned, evaluated classifier is allowed and that aggregates are not | M |
| 9 | "Why did it move" evidence cards | **A** | S1: backward-looking, factual, cited; not a recommendation | G1, G3, G6. Canonical per event. Say "No catalyst found" when that is the case. Never "overreaction", "opportunity", "likely to continue" | Any forward inference or trading implication → **B** | Price and news licences as above | CQ-7: confirm that an LLM-phrased causal *attribution* ("coincided with the Q2 results filing at 15:42") is not "research analysis". US leg: see §6 on event-timed content | M |
| 10 | Corporate event calendars (results, dividends, AGMs, splits) | **A** | Factual, from exchange filings | Dates and sources only. No "expect a beat" | Earnings "previews" with expectations → B | Corporate-data vendor (no scraping) | None | H |
| 11 | Bulk, block and insider (PIT/SAST) deal feeds | **A** | Factual regulatory records | Show records verbatim with dissemination time. No "smart money is buying", "follow the promoter" or curated "notable deals to act on" | Curation framed as a signal, or ranking deals by "conviction" → B | Licensed vendor or NSE D&A (IMD §4). Deal files arrive after the close (14 §1) | None | M-H |
| 12 | FII/DII flows | **A** | S1: market-wide statistics and "general trends in the securities market" | Show the source, whether provisional or final, and publication time. "Coincided with", not "caused" (16 §4.3) | Market-direction calls ("FIIs selling, market to fall") → B risk | Source terms (exchange or NSDL/CDSL publications; check reuse) | None | H |
| 13 | Option chain with Greeks, PCR and max pain | **A** | Computed values (as #4). Index-level analytics fall within the index exclusion | Show the model (Black-76 or BS, rate and IV source), inputs and timestamp. **Max pain and PCR shown as statistics, never as "expected expiry level" or "market bias"**. Dated SEBI F&O loss line (G10) | "Max pain suggests Nifty expires near X", "PCR bullish" → B; strategy suggestions ("sell this straddle") → B | **F&O segment licence** (IMD §4, S = 2) | CQ-3 | M |

### 3.2 Alerts, personal features and tools

| # | Feature | Posture | Deciding authority | Guardrails to stay in A | Flips to B/C if… | Licence precondition | Counsel | Conf. |
|---|---|---|---|---|---|---|---|---|
| 14a | Price alerts (user-set threshold) | **A** | The user writes the rule; we report a fact | Alert text is factual: "[symbol] crossed ₹X at [time] (delayed-15)" | Suggested thresholds ("set a stop-loss at…") → B | Alerts computed from real-time data may be non-display usage (Q-NSE-3) | None | H |
| 14b | Custom rule alerts / system abnormal-move alerts | **A** | As #9 | G1: the same alert content goes to every watcher of that event. Explain the threshold ("return z = 3.1 vs 60-day baseline"). No action words | "Unusual activity — consider buying/selling", or urgency marketing → B | As 14a | US: see §6 (event-timed alerts vs "regular circulation") | M |
| 15 | Watchlist digest | **A** | G1 [I]: choosing which symbols to see is not personalised advice | Each item is the canonical card for that symbol and event. Ordering is neutral (by time or the user's own sort) | Prioritising or annotating by the user's holdings, risk profile or goals ("you should review X") → **C** | As above | CQ-8: confirm that a per-user *selection* of impersonal cards stays outside the IA Regulations | M |
| 16 | Portfolio analytics on user-uploaded holdings (P&L, sector exposure, risk) | **A** for descriptive arithmetic; **C** for any evaluative output | S5: "investment advice" is advice on investing or dealing in securities, including financial planning. Pure arithmetic on the user's data is not advice [I] | P&L, XIRR, sector weights, historical volatility, beta and drawdown as **statistics with definitions**. No "too concentrated", "high risk for you", "rebalance", "suitability", or risk-profile questionnaire. Holdings come **only from user upload** (CSV or contract notes) | Evaluative flags, rebalancing, suitability, or goal-based output → **C (IA)** | **Account Aggregator ingestion is closed to us.** FIUs must be regulated by a financial-sector regulator (S24). Broker holdings APIs need broker approval and are an "association" for the broker (S8) | **CQ-9: do threshold colour codes (e.g. red above 30% single-stock weight) count as advice?** Privacy: §5 | M |
| 17 | Backtesting tool (user-defined rules, historical data) | **A** (private runs of the user's own rules); **C/D** otherwise | S1 (the user's own analysis), S12 (return claims), S15 (PaRRVA), S11 (live linkage = algo) | The user writes the rules; results are shown only to that user, with cost and slippage assumptions and a "hypothetical; past ≠ future" line. **We ship no strategies**, publish no results, run no leaderboards and make no "strategy returned X%" marketing. No "deploy live" button | Publishing our strategies or their returns → **B** (and G5/PaRRVA breach); a "deploy" link to a broker → **C** (algo framework); shared or public results → association risk for brokers (S12) | Historical data storage rights (Q-NSE-5) | CQ-10: is a shareable backtest link a "performance claim"? | M |
| 18 | Strategy marketplace | **D** for us; **C** only as a fully regulated set-up | S11: black-box strategy providers must be RA-registered; algos must be exchange-registered; the provider is empanelled and acts as the broker's agent. S12 and S15: return display only via PaRRVA. S2: creators selling strategies need RA registration | Not achievable in A | Always B or C: the creators need RA registration; the platform needs algo-provider empanelment; performance must be PaRRVA-verified | — | Tradetron precedent (CS §3.1: SCNs to 120+ brokers) | M-H |
| 19 | Buy/sell/hold ratings | **B** (impersonal); **C** if personalised | S2: "research services" include buy/sell/hold and trading calls; consideration includes non-cash benefit | Not achievable in A. Third-party ratings may be shown only as **attributed, licensed consensus data** ("n analysts: x buy, y hold"), and even that is CQ-5 | — | Consensus-data licence | CQ-5 | H |
| 20 | Target prices | **B** | S2 (price target) | Not achievable in A | — | — | — | H |
| 21 | "Top picks" list | **B** (model portfolio or recommendation); **C** if tailored | S2 / S3 model-portfolio provisions; G10 | Not achievable in A. "Most viewed" or "trending" lists are also avoided (G10, retail-harm) | — | — | — | H |
| 22 | AI chat answering "should I buy X" | **A only as a refusal**; B if answered impersonally; C if answered using the user's situation | S2 (impersonal opinion = research); S5 (personalised = advice; the "widely available" exclusion pushes impersonal content back into the RA Regulations) | G9: refuse, then show the evidence cards for X. Log the refusal. Test the classifier against adversarial prompts in the offline eval set | Any yes/no, lean, "if I were you", or "depends on your risk appetite, but…" → B or C | LLM subprocessor disclosure (§5) | CQ-11: is a *refusal plus evidence cards* response itself "a basis for investment decision"? | H |
| 23 | Model forecasts (Kronos-type) shown as ranges | **Legal: B**; **project: D** | S2: a forecast range for a named security is in substance a price target [I, M]. CLAUDE.md invariant 5 bans forecasts | Not achievable in A. Internal research use only | — | Also US AI-washing exposure if accuracy is claimed (S34) | CQ-12 (confirm only if the owner wants to revisit) | M |
| 24 | Auto-trading or order placement via broker APIs | **Legal: C**; **project: D** | S11: broker as principal, algo-provider empanelment, static IP, algo IDs, RA registration for black-box logic. CLAUDE.md: "Never execute trades" | Not achievable in A | — | Broker platform approval (kite-and-broker-apis) | — | H |
| 25 | Telegram / WhatsApp digests | **A** in digest form | Same as #15. The enforcement pattern is calls in Telegram groups (CS §3.1) | Digest (not chat); verified channel identity; G8 in the channel bio and in every message; no "VIP", "premium", "calls" or "jackpot"; no paid tiers named like tip services | Interactive advice chat, or "premium calls" wording → B | WhatsApp Business policy bars general-purpose AI assistants (from 2026-01-15, per 14 §1); digests use template messages only (**verify with Meta**) | CQ-1 (disclaimer wording) | M |
| 26 | MCP server for users' own AI clients | **A** | G1: our tools return the same impersonal cards as the app | Tools take symbols and timestamps, never prices or holdings (16 R-04). Tool descriptions say "returns cited facts; does not provide recommendations". Tool outputs carry G8 | Tools that accept holdings and return evaluations → C. Tool names or descriptions that invite recommendations ("get_trade_ideas") → B | Licences as the underlying cards. Output may be reshaped by a third-party LLM outside our control | **CQ-13: if the user's own LLM (e.g. Claude with Kite MCP) turns our facts into a recommendation, are we "providing" research? We believe not, since we supply impersonal data, but confirm.** Log tool calls | L-M |
| 27 | Educational content (courses, explainers) | **A** | S9 (30-day lag, for "solely education" status in the association rules); S1; the Sathe and Patel orders | Concepts, methods and history. When a named security appears with price data, use **data at least 30 days old** and no forward framing. No levels, targets or stop-losses, **even in examples** | Live examples with levels, or "homework trades" → B (enforcement pattern) | Same data licence; note that S9 requires audit trails from MIIs and intermediaries sharing education data | CQ-14: does the 30-day condition bind us, or only matter if a broker wants to "associate" with us as an educator? | M-H |
| 28 | Paid subscriptions for any of the above | **Posture unchanged** | S2: "consideration" includes non-cash benefit "from client or otherwise", so free does not help and paid does not hurt an **A** feature | Price the A features only; no "premium insights" wording that implies opinions | Charging for any B feature makes RA registration unavoidable. For an RA, individual/HUF clients are capped at ₹1,51,000 per family per year, with at most 1 year's fee in advance (S3) | The NSE paid-app category differs from free (IMD §1.2: revenue share / ₹11.5 L minimum) | None extra | H |

### 3.3 Summary counts

- **A:** 1, 2, 3, 4, 5 (user-built), 7a, 7b, 8 (text-tone only), 9, 10, 11, 12, 13, 14a, 14b, 15, 16 (descriptive), 17 (private), 22 (refusal only), 25, 26, 27, 28.
- **B:** 5 (curated ideas), 6 (default), 19, 20, 21, 22 (impersonal answer), 23 (legal).
- **C:** 16 (evaluative), 17 (with deploy), 18 (regulated set-up), 19/21/22 if personalised, 24 (legal).
- **D for this project:** 18, 23, 24.

---

## 4. What RA registration costs in practice

| Item | Finding | Label, conf. |
|---|---|---|
| Who registers | An individual, a partnership, an LLP or a body corporate. A partnership whose partners don't meet the qualification must convert to an LLP or body corporate (deadline 30 Sep 2025) | [F-sec, M] S2 |
| Qualification | Individual RA, principal officer, and staff giving research: a professional qualification, or a graduate/PG degree or diploma in finance, accountancy, business management, commerce, economics, capital markets, banking, insurance, actuarial science or financial services; or the NISM PG programme (Research Analysis); or the CFA charter. **The experience requirement was removed** in Dec 2024. Associated staff: a graduate in any discipline | [F-sec, M] S2 (compliancecalendar, complisec) |
| Certification | **NISM Series XV (Research Analyst)**, kept valid, for everyone "associated with research services", including client-facing sales staff (FAQ) | [F-sec, M] S2, S4 |
| Net worth vs deposit | **The net-worth test was replaced by a deposit** held as a lien in favour of the RA Administration and Supervisory Body (**RAASB = BSE**): ₹1 lakh for up to 150 clients; ₹2 lakh for 151–300; ₹5 lakh for 301–1,000; **₹10 lakh for more than 1,000** | [F-sec, M] S2 |
| SEBI fees | Application (non-refundable): ₹2,000 for individuals and partnerships, ₹20,000 for body corporates and LLPs. Registration: ₹3,000 / ₹30,000. **Renewal every 5 years** | [F-sec, M] (renewal cycle M) |
| Other set-up costs | NISM exam fee; RAASB membership or annual fee; compliance officer (an ICAI/ICSI/ICMAI professional allowed for non-individuals); website with prescribed disclosures; recording and CRM systems | [F-sec, M] for the obligations; **amounts unverified** |
| Time to register | No primary source found | [E, L] roughly 2–6 months from application, including exam preparation; counsel to confirm |
| Part-time RA | Allowed for an individual or partnership that has other business, with a "Part-time Research Analyst" label. A 75-client cap appears in one secondary summary only | [F-sec, M] label; [L] cap |
| Ongoing: audit and records | Annual compliance audit by a CA or CS; records kept for at least 5 years; KYC of fee-paying clients; recorded client interactions; a rationale documented for every recommendation (FAQ) | [F-sec, M] S2, S4 |
| Ongoing: AI-use disclosure | Disclose "the extent of use of AI tools" at the time of agreeing terms (existing clients by 30 Apr 2025). The RA remains fully responsible for AI output and data security. Reg 16C (Feb 2025) says the same for all regulated entities | [F-sec, H] S2, S3; IMD §3.4 |
| Ongoing: fee rules | Individual and HUF clients: at most **₹1,51,000 per family per year** (excluding statutory charges; reviewed every 3 years). Advance fees at most 1 year. Accredited investors and non-individual clients are said to be outside the cap, but no source was read for this ([A, M]; §8). MITC must be given | [F-sec, H] S3 |
| Ongoing: PaRRVA | Any past-performance or return figure shown to clients must be PaRRVA-verified. CARE Ratings is the agency, NSE the data centre; live from 4 May 2026; enrolment to 3 Sep 2026 | [F-sec, M-H] S15, S16 |
| Ongoing: social media | From 1 May 2026, the registered name and number go on the profile and at the start of every securities post | [F-sec, M] S18 |
| Ongoing: segregation | Research clients and distribution clients are segregated at group level | [F-sec, M] S2 |
| Ongoing: cyber | Whether SEBI's CSCRF (Aug 2024) applies to RAs, and at what tier | **Unverified**; CQ-15 |
| Ongoing: algos | A black-box algo provider must be an RA, publish a periodic strategy report and notify changes to the exchange | [F-sec, H] S11 |

**Cost estimate [E, L].** For a body-corporate RA serving more than 1,000 clients:
- **One-off:** about ₹0.5 L in SEBI fees, ₹10 L deposit (refundable, but locked), plus exam and legal set-up at ₹2–6 L.
- **Annual:** ₹6–15 L for a compliance officer or retainer, audit, and recording/CRM tools.
- This is before the salary of a qualified principal officer.

The estimate is not sourced. Treat it as a planning placeholder.

**RA-partner option [I, M].** A registered RA is the author and accountable party. We are the delivery and evidence layer.
- The RA's name and number appear on every B output. The RA signs off the content and makes the AI-use disclosure. Performance figures come only through the RA's PaRRVA enrolment.
- **Risks:**
  - Fee flows between the RA and us are "association" (S8). That is lawful only while *we* give no unregistered advice and make no return claims, which our A posture already ensures.
  - Whether a platform that hosts and monetises RA content needs its own registration is unresolved (CQ-16).
  - The client-fee cap and KYC stay with the RA.
- **Precedent:** Smallcase distributes RA/IA model portfolios through brokers (CS §1.3). Angel One's ARQ runs under Angel's own RA licence.

---

## 5. Privacy: what applies to a small app that stores watchlists or holdings

| Period | Regime | What it means for us | Label, conf. |
|---|---|---|---|
| **Now, until 12 May 2027** | IT Act s.43A plus the **SPDI Rules 2011** (S22) | A privacy policy on the site; "reasonable security practices" (ISO 27001 or an equivalent documented programme); consent for sensitive personal data. Passwords and "financial information such as bank account… details" are SPDI. **Whether holdings count as SPDI is unclear (CQ-17)**; treat them as if they do | [F-sec, M] |
| **Now** | **CERT-In Directions 2022** (S23) | Report listed cyber incidents to CERT-In **within 6 hours** of noticing. Keep ICT logs for a rolling **180 days in India**. Name a point of contact | [F-sec, H] |
| From 13 Nov 2026 | DPDP: Consent Manager registration opens | Optional for us; users may manage consent through a registered consent manager | [F-sec, M] S20 |
| **From 13 May 2027** | **DPDP Act plus Rules 2025** in full; s.43A and the SPDI Rules are omitted | See the obligations below | [F-sec, H] S20 |
| Proposed | MeitY's Jan 2026 plan to bring deadlines forward by 6 months (mainly for SDFs) and apply retention within 90 days | **Not confirmed as notified.** Track it | [F-sec, M] S21 |

**DPDP obligations for a small data fiduciary (from 13 May 2027)** [F-sec, M unless stated]:
- **Notice (Rule 3).** A standalone, plain-language notice that itemises the data collected (email, watchlist, uploaded holdings, chat logs), the purpose of each item, how to withdraw consent, and how to complain to the Board.
- **Consent (s.6).** Free, specific, informed, unambiguous and affirmative; given **per purpose**; as easy to withdraw as to give. Bundled consent for model training is not allowed; **do not train on user data** [P].
- **Security (Rule 6).** Encryption, masking or tokenisation, access control, and monitoring logs. **Keep logs for at least 1 year** (Rule 6/8, M); this is stricter than CERT-In's 180 days for some logs. Backups. Contracts with processors, **including the LLM subprocessor**.
- **Breach (Rule 7; S20 text read via dpdpa.com).**
  - **Board:** notify "without delay", then send a detailed report **within 72 hours** (or longer if the Board allows).
  - **Affected users:** notify "without delay", with the nature of the breach, its consequences, the mitigation and a contact.
  - This applies to **any** breach, whatever its size. The CERT-In 6-hour report runs in parallel. **Plan to the shortest clock: 6 h.**
- **Erasure (s.8(7)).** Delete when the purpose is served or consent is withdrawn. The Third Schedule deletion timelines apply only to large e-commerce, gaming and social platforms [F-sec, M], not to us.
- **Children (s.9, Rule 10).** Verifiable parental consent is required. [P] Gate the service to users aged 18 and over, and state it in the terms.
- **Contact person (s.8(9), Rule 9).** Publish the business contact of a person who can answer data questions.
- **DPO.** Required **only for a Significant Data Fiduciary** (s.10). A small app is unlikely to be notified as one [I, M]. An SDF also needs a DPO based in India, annual DPIAs and audits.
- **Grievances.** Respond within the published period. Rule 14 is reported as allowing up to 90 days [F-sec, L].
- **Cross-border transfer (s.16).** Allowed unless the destination is on the government's restricted list. An LLM API hosted in the US is currently permitted [F-sec, M].
- **Penalties.** Up to ₹250 Cr for failing to take reasonable security safeguards [F-sec, M].

**Product rules [P]:**
- Watchlists are confidential personal data, because they reveal financial interests.
- Store uploaded holdings encrypted at field level, with a TTL and a one-click "delete my data".
- Never send holdings or watchlists to the LLM with the user's identifiers. The LLM receives only symbol-level card content.
- Disclose the LLM subprocessor by name and region.
- If we later become an RA, KYC and record-keeping duties (5 years) override erasure for those records, under DPDP's legal-obligation ground.

---

## 6. US leg (brief)

1. **Publisher's exclusion (Advisers Act s.202(a)(11)(D); *Lowe v. SEC*, S30)** [F, H]. An unregistered publisher is outside the "investment adviser" definition when its publication is:
   - **impersonal:** not tailored to any client;
   - **bona fide:** genuine, disinterested commentary, not touting;
   - of **general and regular circulation:** not "timed to specific market activity, or to events affecting or having the ability to affect the securities industry".

   *SEC v. Park* (S31) denied the exclusion to a paid-members stock-pick email service that was touting and not regularly circulated.
   - **[I, M] Our risk point is event-driven alerts.** Push alerts triggered by price moves look like "timed to market activity".
   - Mitigations:
     - the content is **factual evidence, not advice** (the exclusion matters less if nothing is "advice as to the value of securities");
     - the same canonical content for all users (G1);
     - a regular digest schedule alongside the alerts;
     - no staff trading in covered names around alerts (a written personal-trading policy);
     - no tailoring.
   - **CQ-18** for US counsel: do event-triggered factual alerts need the exclusion at all, and if so do they qualify?
2. **Personalised chat** fails the "impersonal" prong. Same G9 refusal rule as India.
3. **AI-washing.**
   - *Delphia and Global Predictions* (S34) were brought under the Marketing Rule and s.206 against **registered** advisers.
   - For an unregistered publisher, the live hooks are:
     - **FTC Act s.5** (Operation AI Comply) for consumer-facing capability claims;
     - **Rule 10b-5 / Securities Act s.17(a)** when AI capability claims are made **to investors while raising capital** (*Rimar*, *Saniger/Nate*).
   - [P] Investor decks and marketing make no accuracy or "AI-powered signals" claims; any capability claim is substantiated and documented.
4. **The SEC's predictive-data-analytics proposal was withdrawn on 12 Jun 2025** (S32). No AI-specific SEC rule binds us.
5. **FINRA.** RN 24-09 and the 2026 Oversight Report (GenAI and agents) say Rule 2210 content standards apply to AI-generated communications (S33).
   - FINRA binds **member broker-dealers only**. It reaches us only if a US broker-dealer distributes our content, in which case expect supervision and review clauses in the contract.
6. **US data display** (pro/non-pro, exchange fees) is outside this file; see `04-real-time-data-strategy.md`.

---

## 7. Counsel questions (for the owner to send; not sent)

| ID | Question | Why it matters |
|---|---|---|
| CQ-1 | "Please approve this standing disclosure for an unregistered information publisher: [G8 text]. Should we avoid any reference to SEBI, given the Feb 2026 rule that regulated entities show registration numbers?" | Every surface (#25) |
| CQ-2 | "Is a neutral statistical percentile of a company metric against its sector (e.g. P/E percentile) a 'statistical summary of financial data' or an opinion?" | Stock pages (#2) |
| CQ-3 | "Are conventional technical-analysis state terms (overbought, oversold, golden cross, PCR, max pain) used as neutral descriptors of a single stock a 'research analysis… providing a basis for investment decision'? Does the answer differ for indices and sectors?" | #4, #5, #13 |
| CQ-4 | "Is automated detection and naming of classic chart patterns on a single stock, without direction or target, research under the RA Regulations?" | #6 |
| CQ-5 | "May we show attributed, licensed third-party analyst consensus or target prices, or summaries of named brokerage notes, without RA registration?" | #7b, #19 |
| CQ-6 | "Is a per-headline tone label (not aggregated per stock) an opinion on a security?" | #8 |
| CQ-7 | "Is a cited, backward-looking attribution of a price move to a disclosed event 'research analysis'?" | #9, the core product |
| CQ-8 | "Does a user-selected watchlist digest of identical, impersonal cards stay outside the IA Regulations?" | #15 |
| CQ-9 | "For analytics on uploaded holdings, which outputs cross into investment advice: concentration thresholds, risk colour codes, volatility or beta?" | #16 |
| CQ-10 | "Is a user-shareable backtest result page a 'performance claim' under Reg 16A, the Jan 2025 circular or the Sep 2022 algo circular?" | #17 |
| CQ-11 | "Is a refusal that then shows factual evidence cards for the same stock itself a basis for an investment decision?" | #22 |
| CQ-12 | "Confirm that a probabilistic price range for a named security is a price target under the RA Regulations." | #23 (only if revisited) |
| CQ-13 | "If a user's own AI client combines our impersonal MCP output with their broker's MCP and produces a recommendation, is that attributable to us?" | #26 |
| CQ-14 | "Does the 8 May 2026 30-day price-data lag bind an unregistered publisher's own education pages, or only matter for association with regulated entities?" | #27 |
| CQ-15 | "Does the CSCRF apply to a body-corporate RA, and at what tier?" | §4, if we register |
| CQ-16 | "If we host and deliver a registered RA's research and share revenue, do we need our own registration? What contract terms protect both sides under Reg 16A?" | RA-partner option |
| CQ-17 | "Are securities holdings and watchlists 'sensitive personal data or information' under the SPDI Rules before 13 May 2027?" | §5 |
| CQ-18 (US) | "Do event-triggered factual alerts need the publisher's exclusion, and if so do they meet the 'general and regular circulation' prong after *Lowe* and *Park*?" | §6 |
| From 16 R-07 | The Sathe/Patel education carve-out; the per-post registration-number rule for unregistered publishers; the Tradetron notices | Carried over; partly answered by S9, S18 and §3 #27 |

---

## 8. Unverified or low-confidence items

1. The full operative text of S1, S2, S4, S7, S8, S9 and S15. The sebi.gov.in pages returned headers only, and the PDFs could not be read in this environment. Definitions and conditions come from reputable secondary sources (M). **Counsel should read the primary texts.**
2. What the RA amendment of 6 Aug 2025 changed. Only the consolidated-regulations listing was seen.
3. RAASB (BSE) annual fees; NISM Series XV exam fee; realistic time to register.
4. The part-time RA client cap (75, L); renewal cycle (M).
5. Whether SEBI's AI/ML guidelines (S19) have been finalised.
6. Whether MeitY's accelerated DPDP timeline (S21) was notified.
7. DPDP Rule 14 grievance period; the exact Rule 6/8 log-retention wording.
8. PaRRVA enrolment date conflict (3 Aug vs 3 Sep 2026). The later circular is used.
9. NSE circular NSE/INVG/73992 (30 Apr 2026) on algo-provider empanelment was not opened.
10. The claim that accredited investors and non-individual clients fall outside the RA fee cap: no source was read ([A, M]).
11. WhatsApp Business policy for template-only digests (Meta terms not re-read this session).
