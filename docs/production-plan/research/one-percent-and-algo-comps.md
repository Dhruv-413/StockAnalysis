# Research: the 1% Club, creator-led finance apps, and Indian algo / backtest / paper-trading platforms, plus a lean MVP for the new direction

**Author:** product-manager. **Access date for all sources:** 2026-09-24. **Status:** research draft for the owner (not in the repo).

**Labels:** [F] fact, [I] inference, [A] assumption, [E] estimate, [P] proposal.

**Confidence:**
- **H:** a primary page was read.
- **M:** a reputable secondary source (Inc42, Business Standard, BusinessToday, a law firm), or a primary page summarised by the fetch tool.
- **L:** vendor blogs or SEO sites, review sites, or a single unverified source.
- **Snippets:** a search snippet from a *primary* page (a vendor's own docs or an official disclosure) is **M**, following the case-studies convention. A snippet from a secondary or SEO page is **L**.

**Scope rule.** This report does not repeat material already in the repo. It cross-links instead.
- [research/case-studies.md](case-studies.md):
  - Streak's free switch and its old pricing;
  - Sensibull's FY25 revenue;
  - the Tradetron show-cause notices;
  - OpenAlgo;
  - Univest, Liquide and the finfluencer enforcement cases.
- [17-what-is-achievable.md](../17-what-is-achievable.md):
  - NSE licence prices;
  - the NOW / LICENCE / REG / NO verdict key;
  - guardrails G1–G11.
- [research/kite-and-broker-apis.md](kite-and-broker-apis.md):
  - Kite display terms;
  - static IP and the 10 orders-per-second limit;
  - empanelment basics.

---

## 0. Bottom line: three constraints decide the MVP more than any competitor

1. **Automated trading is ruled out by this project's own rules today** [F, H: CLAUDE.md].
   - CLAUDE.md: "Never execute trades or add order-placing code."
   - feature-legality #24 rates order placement "Legal: C; project: D".
   - The owner's new direction (automated trading on Kotak Neo or Kite) needs an **ADR that supersedes ADR-008 and amends the CLAUDE.md rule**. This is owner decision #1.
   - Even with that ADR, offering order automation to *other people* needs all of the following:
     - NSE/BSE algo-provider empanelment (per broker);
     - broker-as-principal arrangements;
     - per-user static IPs;
     - an RA registration if any logic is black-box.
   - Fee-based strategy sharing between users is not allowed. Zerodha's reading of the Feb-2025 framework: "individuals are permitted to share their strategies only with family members" [F, M, Z-Connect 2025-02-06].
   - **[P]** Keep order automation out of the 8–12-week MVP and show it as a gated Phase 3.

2. **A third party offering paper trading on live prices is the biggest legal risk in this direction.**
   - SEBI circular SEBI/HO/MRD/MRD-PoD-3/P/CIR/2024/56 (24 May 2024, effective about 23 Jun 2024) says:
     - Exchanges and **registered intermediaries (brokers)** must ensure "no real time price data is shared with any third party including various platforms", except for orderly market functioning or regulatory requirements.
     - Price data may be shared "for investor education and awareness activities without offering any kind of monetary incentive to the participants, **with a lag of 1 day**" [F, M, TaxGuru reproduction of the circular].
   - SEBI PR 37/2024 (4 Nov 2024) warned that apps offering "virtual trading services or paper trading or fantasy games" on listed-company price data violate the SCRA 1956 and the SEBI Act 1992 [F, M, Business Standard / TeamLease; the SEBI page body did not load].
   - Nithin Kamath: the circular "ends all platforms offering trading competition, demo trading, CFDs, and more" [F, M, BusinessToday 2024-05-25].
   - **Two different lags apply to two different things. Do not merge them:**
     - **1 day:** sharing price data for investor education with no monetary incentive (May-2024 circular).
     - **30 days (formerly 3 months):** an *unregistered* person naming securities in education content (Jan-2025 finfluencer rules, as updated; see doc 17 §3 #27).
   - **[P]** Make the replay lag a **compliance-set parameter**, not a hard-coded value. No prizes, competitions or cash leaderboards.
   - Sensibull virtual trade, AlgoTest forward tests, Tradetron paper trading, Dhan, FrontPage and NSE Paathshala still appear to offer live or near-live simulation. **Their legal basis is unexplained** (broker agreements? licensed vendor data? exchange-owned?). Treat them as **unexplained, not as precedent**.

3. **The finfluencer association rule cuts through both the creator go-to-market and the broker-API foundation.**
   - From 29 Aug 2024, SEBI-regulated entities (brokers included) may not associate with unregistered persons who give advice or make return/performance claims. That covers money, client referrals **and "interaction of IT systems"**. Existing contracts were to be ended within three months of the 22 Oct 2024 circular [F, M, Outlook Money / Legal500 / Business Standard].
   - If our brand, or a creator we partner with, gives tips or makes return claims, Kotak or Zerodha must cut our API or referral link [I, M].
   - Zero1 (the Zerodha–LearnApp JV) **wound down its creator partnerships by March 2026** and moved to in-house content. Inc42 links this to the SEBI finfluencer rules [F, M, Inc42 2026-04-23].
   - **[P]** Go-to-market goes through **SEBI-registered creators**, or **education-only contracts** that respect the lag and forbid return claims.

4. **Data rights are binding for the "practice" half too** (doc 17 §1.2).
   - Replaying past sessions and backtesting both need **licensed history**:
     - EOD: about ₹1L/yr (doc 17 #3 and #17);
     - historical option chains: #13;
     - intraday F&O history: vendor quote only.
   - The free routes are excluded:
     - NSE bhavcopy (NSE terms ban automated collection; project rules say no scraping);
     - Kite historical API (a third-party app can't show it);
     - yfinance (banned in product code).
   - **Truly NOW with zero data spend:**
     - lessons;
     - a journal on the user's **uploaded** tradebook;
     - an AI tutor;
     - calculators where **the user types in** spot, IV and premiums (the Zero1 calculator pattern).

**The honest shape of a cheap start [P]:** a Hindi + English **learn → practise → review** app, in two releases.
- **Weeks 1–12 (NOW, no data spend):**
  - lessons;
  - payoff/Greeks and position-size calculators on user inputs;
  - the trade journal on uploaded tradebooks;
  - the AI tutor.
  - Build the replay sandbox and backtester **on internal fixture data only**, not user-facing.
- **When the history licence lands** (doc 17's calendar floor for licence answers is about 3 months, so this overlaps the whole window): launch the replay sandbox (lagged, event drills) and the backtester of the user's own rules.
- Order automation on Kotak or Kite comes later, only after the ADR, and only through an empanelled route or a user-self-hosted mode (§5.5).
- **"Cheap" therefore depends on the history vendor quote.**

**Target user.** This direction **replaces** the target user in 02 (independent equity researchers covering 30–200 US names) with Indian retail beginners and intermediates. That is an owner decision to record, not something to retrofit into 02 §4/§6.

---

## 1. The 1% Club (Sharan Hegde, "Finance With Sharan")

### 1.1 What it is

| Item | Finding | Label, conf. |
|---|---|---|
| Legal entities | One Club Ventures Pvt Ltd (Inc42 lists it as the company); the site also lists One Battalion Ventures Pvt Ltd and One Centurion Ventures Pvt Ltd | [F] H (site footer, fetched); M (Inc42) |
| Founders, dates | Sharan Hegde and Raghav Gupta; founded 2022; Mumbai | [F] M |
| Brands | 1% Club (education and community); **PersonalCFO** (advisory / wealth); **Pillow** (insurance); **Bombay Trading School** (trading education); **1% Club Capital** | [F] H (site) |
| Education | Masterclasses of about 2 hours at ₹99–499; 6-hour bootcamps (personal finance, stock market, insurance, credit cards, tax); "Money School" in the app; the "Retire Early (FIRE) blueprint" | [F] M (search snippets from YourStory 2024; YourStory itself returned 403) |
| Membership | ₹14,999 list price, often "50% off" at ₹7,499. A 7-day refund promise is referenced in complaints | [F] L–M (search snippet; Trustpilot) |
| App features (iOS listing) | **AI CFO**, spend and cash-flow tracking, MF and stock portfolio research, Money School, insurance consultation, account connectivity | [F] H (App Store page, fetched) |
| AI CFO (launched 2026-08-20) | "India's first AI CFO". Analyses cash flow, net worth and holdings, answers affordability questions, reviews portfolios on 8 metrics (returns, fund quality, benchmark, allocation, concentration, overlap, cost, tax), and sends news relevant to holdings. Price not disclosed | [F] M (Buzzincontent) |
| **Bombay Trading School** | A 12-week online programme: technical analysis, derivatives, risk, psychology, **"Python-based strategy building, broker API integrations, backtesting frameworks"** and AI tools. **3,000+ students over two years.** Price not disclosed. It cites SEBI's FY25 figure that 91% of individual F&O traders lost money | [F] M (Goodreturns 2026-05-21) |

**[I] Direct overlap.** The 1% Club already teaches exactly the "backtesting + broker API + algo" skills the owner wants to productise. It sells them as a cohort course, not a tool. A tool that its students (and similar cohorts) *practise on* is a partnership angle as well as a competitive threat.

### 1.2 Regulatory structure

| Registration | Finding | Conf. |
|---|---|---|
| SEBI **Investment Adviser (RIA)** | **INA000018896**. Announced Feb 2025 as the "first finfluencer-led company" with an RIA licence. It allows one-to-one financial planning (PersonalCFO) | [F] H (number on the site); M (Inc42 2025-02-03) |
| SEBI **Research Analyst (RA)** | **INH000023968** (listed on the site) | [F] H |
| AMFI ARN (MF distribution) | **Not found / unverified** | — |
| IRDAI (Pillow insurance) | **Not found / unverified.** Pillow is listed as a brand, but no IRDAI broker or corporate-agent number was seen | — |
| RBI | **Not found**. No NBFC or AA licence was seen | — |

Hegde has said he wants "more SEBI licences" for "stock recommendations, small cases, high-yielding debt" [F, M, Inc42 2025-02-03].

**[I]** The AI CFO's personalised portfolio reviews rely on the RIA/RA registrations. **For an unregistered entrant, the AI CFO feature set is REG** (doc 17 verdict key).

### 1.3 Scale, money, funding (with conflicts flagged)

| Metric | Value | Source, conf. |
|---|---|---|
| Revenue | FY24 ₹31.4 Cr; **FY25 ₹54.9 Cr** (+74.8%) | Inc42 company page, M |
| Cumulative revenue | "Over ₹150 Cr in three years" | Buzzincontent 2026-08, M |
| Profitability | "35–40% EBITDA margin"; "$8M annualised revenue" (Nov 2024) | StartupTalky citing founder posts, L–M |
| Paying clients | **85,000 active paying clients** (Nov 2024) | StartupTalky, L–M |
| Community / students | **Conflict:** "6 lakh+ community" (site) vs "about 1 million students" (Aug-2026 article) vs 85k paying (2024) | H (site) / M / L–M |
| Assets | **Conflict:** "₹50,000 Cr+ assets tracked" (site) vs "₹4,000 Cr client assets tracked; ₹2,000 Cr AUA" (Aug 2026) vs ₹750 Cr AUA (Feb 2025) | H / M / M |
| Funding | ₹10 Cr (about $1.2M) pre-Series A, Oct 2023, led by **Gruhas (Nikhil Kamath and Abhijeet Pai)**. Hegde said the money sat in an FD at 8.5% | Forbes India / BusinessToday 2023-10-31, M |
| Headcount | About 200 after a **15% layoff (Nov 2024)**, attributed to rapid-expansion inefficiencies and AI savings. Inc42 now shows 729 (probably includes advisers or contractors; unverified) | StartupTalky, L–M; Inc42, M |
| Creator reach | "1 Crore+ followers across Instagram, YouTube and LinkedIn" | LinkedIn / site, L |

### 1.4 Ratings and review themes

| Channel | Rating | Themes | Conf. |
|---|---|---|---|
| Apple App Store (IN) | **4.6 (3.2k ratings)**; #52 in Finance | Praise: complex topics made simple. Complaint: a paid member couldn't access live sessions; the mentor "acts more like a coordinator"; support unresponsive | H |
| Google Play | **3.8 (about 695 reviews)** (search snippet; the page did not load) | — | L |
| Trustpilot | **3.8 / 5, 1,485 reviews** (76% 5-star, 7% 1-star) | Complaints: slow refunds on the ₹14,999 membership, support tickets unresolved for 6+ days, no-show sessions, "promotional rather than educational", "rushing us to pay", content "adapted from Varsity". Praise: PersonalCFO, clarity | H (page fetched); themes L |

### 1.5 Why it works [I, M]

1. **Creator-led, near-zero customer acquisition cost.** More than 10M followers send traffic into ₹99–499 masterclasses (a low-friction tripwire). Those upsell to ₹7.5–15k memberships, then to RIA advisory (PersonalCFO), insurance (Pillow) and trading school (BTS). **The money is in the funnel, not the app.**
2. **Registration as a moat.** RIA plus RA lets it personalise (AI CFO, PersonalCFO) where unregistered competitors cannot.
3. **The founder's personal brand carries trust.** Complaints are about *service delivery* (support, refunds, sessions), not about returns. That is because it avoids selling calls.
4. **A strategic investor inside the Zerodha orbit** (Nikhil Kamath's Gruhas).

**Lesson for us [P].** We cannot copy the registration moat or the audience cheaply. What we *can* offer is the missing **practice layer** that creator cohorts lack. The 1% Club's review themes (support, delivery) point to service ops as the failure mode for education businesses.

---

## 2. Other creator-led finance businesses in India

| Business | Model and price | Scale | Registration | What changed recently | Conf. |
|---|---|---|---|---|---|
| **Ankur Warikoo: WebVeda** | Cohort and recorded courses, then (May 2026) **converted to a subscription: all courses for ₹1,999/yr** | ₹100 Cr revenue over 5 years, ₹25 Cr profit, **5 lakh students**, all upgraded to membership for free | None needed (general skills, not securities advice) | Warikoo "shut down" the ₹100 Cr per-course business in favour of the subscription: "Between making more money and helping more people – the choice was super clear" | M (BusinessToday 2026-05-17; the ₹1,999 figure from Buzzincontent snippet, M–L) |
| **CA Rachana Ranade** | Paid courses in an app (Basics of Stock Market, Fundamental and Technical Analysis, Personal Finance). One PC course is listed at about $93 with a 38% discount | 286k+ learners (self-claim); 28 employees; revenue band ₹0–10 Cr FY25 (Tracxn) | Not found | No change found | L–M |
| **Pranjal Kamra: Finology** | Ticker (research tool), **Recipe** (DIY financial planning), smallcases, courses | "1M registered users" (2022); FY20 revenue ₹2.2 Cr (older) | **SEBI RIA INA000012218 and RA INH000024277** | Registered on both sides, like the 1% Club | M (Finology's own disclosure pages via snippet) |
| **Zero1 by Zerodha** (JV with LearnApp, launched Oct 2023) | Free: videos, calculators, community events | 800k+ YouTube subscribers; about 500M views; 450k calculator users; about 100k weekly viewers (Aug 2026) | Zerodha is the regulated parent | **Apr 2026: stopped creator partnerships and moved to in-house content** (Inc42 ties this to SEBI finfluencer rules). **Aug 2026: "Zero1 Hindi" original content replaced failed dubbing.** It is **operating**; an earlier search snippet saying it had "shut down" is contradicted by the primary Z-Connect post of 2026-08-13 | H (Z-Connect); M (Inc42) |
| **Pushkar Raj Thakur** (Hindi) | YouTube-led; sponsored partnerships with **Upstox** and Investing.com | About 18M followers (CreatorDB, L) | Not found | Shows broker-sponsor money flows to Hindi creators; the association rule now constrains this | L |
| **Akshat Shrivastava** | Stock market course reported at about ₹23,000 per year of access | n/a | Not found | — | L |
| **Labour Law Advisor** | Courses app (tax, compliance careers); 4M+ followers | n/a | n/a | A career-skills pivot, not markets | L |

**Patterns [I, M]:**
- Creator education is **profitable at small scale** (WebVeda ₹25 Cr profit; the 1% Club's 35–40% EBITDA claim). Retail research SaaS mostly burns cash (Tickertape, Smallcase and Univest in case-studies).
- **Prices are converging downward to all-access subscriptions** (WebVeda ₹1,999/yr).
- **Everyone that personalises gets registered** (1% Club, Finology).
- **The one market-focused, free creator network owned by a broker dropped outside creators** (Zero1).

---

## 3. Indian algo, backtest and paper-trading platforms

"Post-framework" means after the SEBI retail-algo circular (4 Feb 2025) and the NSE operational circulars. Static IP and algo-ID enforcement began 2026-04-01; see kite-and-broker-apis §3.

**Empanelment status is unverified for every platform.** The NSE empanelled-provider list page timed out. The vendor claims below are **L** unless noted.

| Platform | Features | Pricing (2026) | Users | Brokers | Post-framework behaviour | Complaints | Conf. |
|---|---|---|---|---|---|---|---|
| **Streak (Zerodha)** | No-code conditions, scanners, backtests, virtual (paper) deployments, TradingView charts | Free for Zerodha users since Jan 2024 (see case-studies). Fair use: 5 live, 15 virtual, 5 scanners, about 50 dynamic-options backtests/day | n/a | **Zerodha only** | Compliant through Zerodha as broker. Limited to 5 conditions, no multi-timeframe logic (L) | **iOS 2.8 (135 ratings)**: execution not matching the strategy; the same backtest giving different results; instability | H (iOS); L (limits) |
| **Tradetron** | 150+ keyword builder, cloud execution, **strategy marketplace**, paper trading | Free (1 deployment) / Starter ₹300 / Starter+ ₹850 / Retail ₹1,200 / Retail+ ₹2,500 / Creator ₹5,000 / Creator+ ₹9,000 per month. 7% off quarterly, 17% off yearly. Marketplace listing only on Creator tiers | n/a | "70+" (L); Kotak Neo supported | Oct-2024 notices to 120+ brokers (case-studies). **Marketplace still listed on the pricing page.** The page makes no RA or empanelment claim, which sits uneasily with Zerodha's reading that fee-based strategy sharing is out | iOS reviews: "live auto not functioning", unresolved support (L) | H (pricing page); L (reviews) |
| **AlgoTest** | Options-first backtesting (multi-leg), simulator, **forward test = paper trading**, execution. After the framework it became a **marketplace of SEBI-RA-published strategies ("600+ strategies from verified RAs")**; AlgoTest itself is "not an RA" | Credits: ₹499 / 500, ₹999 / 1,100, ₹2,499 / 3,000, ₹5,999 / 7,500. 100 backtests = 100 credits; unlimited 30 days = 1,599 credits; **25 free backtests/week**; forward test 50 credits per strategy for 28 days; Signals ₹1,299 for 30 days | "35k+ traders" (banner, L) | 20+ (L) | Moved to **RA-published strategies** to keep the marketplace legal. Claims NSE/BSE empanelment (snippet, **L**) | Thin | M (docs via snippets); L (empanelment) |
| **uTrade Algos** (uTrade Solutions) | No-code builder, "uTrade Originals" prebuilt strategies, payoff charts, margin calculator, paper trading at 5 credits per run | **Pricing page (fetched): Beginner ₹99 / Essentials ₹499 / Pro ₹1,999 / Elite ₹4,999 per month.** **Conflict:** a snippet cites ₹999–14,999 (older?) | n/a | Zerodha, Angel One, Dhan, Share India, Fyers, **Kotak Neo** "and many more". The iOS app shows only Share India or guest login | Claims NSE and BSE empanelment (snippet, L) | iOS 4.8 (20 ratings; a small sample) | H (pricing page); L (the rest) |
| **Quantiply** | Fully automated index F&O (Nifty, BankNifty) | ₹250–2,000/mo (AlgoTest blog, L) | n/a | **After 1 Apr 2026 only 4 brokers: Angel One, IIFL, Upstox, Finvasia Shoonya**. Offers free plans through broker referral links | Clear evidence of **broker attrition after the framework**; pricing is now subsidised by broker referrals | n/a | H (its own docs) |
| **Stratzy** | 43+ prebuilt algos "designed by SEBI-registered RAs" | Monthly or quarterly; a "2% of capital annually" figure (snippet, **L**) | n/a | Zerodha, Dhan, Upstox, Groww, Motilal, Angel | **Is itself an RA (INH000009180)**. Claims NSE/BSE/MCX empanelment (L). Does not allow testing before deploying (per AlgoTest, a competitor, L) | **iOS 3.7 (204)**: "backtesting data does not appear reliable"; pricey relative to ideas | H (iOS rating and reviews); M (RA number, from a snippet of stratzy.in); L (fees, empanelment) |
| **Opstra (Definedge)** | Options analytics, strategy builder, simulator, options backtesting (Pro) | Free (15-min delayed data, 2 portfolio trades); Pro price undisclosed; subscription refunded as brokerage wallet points | n/a | **Needs a Definedge demat** for full access | Broker-tied model | iOS 2.3; compulsory KYC before features; instability | M (Strike review 2026-01) |
| **Sensibull** | Options chain, strategy builder, **virtual trading** | Free / Pro about ₹1,300/mo or about ₹392/mo billed annually; free for Zerodha users | "2M+" (L) | Zerodha, Angel, Upstox, ICICI, 5paisa | FY25 revenue fell 28.7% (case-studies) | Play 4.1 (41k); chart and loading issues | M |
| **Dhan Options Trader** | Strategy builder, **Quant Mode** (strike selection by delta/premium logic), payoff, prebuilt strategies, DhanHQ API | **Free for Dhan account holders** | n/a | Dhan only | Positions itself as 2026-compliant (L) | n/a | M (Dhan pages via snippet) |
| **TradingView paper trading** | Global paper trading | Free plan has **15-min delayed NSE data**; **paper trading does not accept orders on delayed ("D") symbols**, so free Indian users effectively can't paper trade NSE | Global | Broker integrations (Fyers, Dhan, Angel) | Delayed free NSE data, citing exchange licensing | Indian users angry about the delay | M (AlgoTest blog, Fyers community, Business Upturn) |
| **FrontPage** (Bengaluru, YC-backed, about $748k raised) | Social trading community, "Trade Lab" paper trading with ₹10L virtual cash, F&O and commodities | Free | "1M+ active" (self-claim, L); 458k+ downloads, 4.3 | n/a | **Unclear how it complies** with the May-2024 data rule | n/a | L |
| **NSE Paathshala** | Exchange-run virtual trading, ₹5L virtual cash | Free | n/a | n/a | Exchange-owned, so presumably exempt [I] | Users call the interface poor (TradingQnA 2017) | L |
| **Kotak Neo (own)** | Trade API with REST and WebSocket, 10 orders/sec, static IP; StockShaala algo-trading course (6 modules); **Kotak Neo Trade API free** | **Zero brokerage on API orders on Trade Free plans from 2025-11-01** (Kotak press, M). **Conflict:** the Kotak page also frames zero brokerage as a "first 30 days" offer. Square-off leg of bracket orders charged. Static IP about ₹100/mo via third parties | n/a | — | **No native no-code builder or paper trading found**. Relies on third parties (Tradetron, AlgoTest, uTrade, AlgoKing). **Data-display terms for third-party apps are unverified.** Do not assume Kotak allows display | n/a | H/M |

**Cross-cutting findings [I]:**
1. **Brokers have pushed tools to free**: Streak, Dhan Options Trader, Sensibull for Zerodha users, the free Kotak API with zero brokerage, and Quantiply's free plans through broker referral links. **A paid, standalone "algo tool" is squeezed from above by free broker tools.**
2. **After the framework, independents took one of three routes:**
   - **registered themselves** (Stratzy as RA);
   - **turned into marketplaces of RA-published strategies** (AlgoTest);
   - **shrank their broker list** (Quantiply, down to 4).
   Tradetron's position is unclear.
3. **Backtest trust is the most common complaint**: Streak inconsistency, Stratzy "not reliable". A **reproducible, audit-logged backtester** (costs stated, fills explained) is a real differentiator. This is consistent with invariant 5 and doc 17 feature #17.
4. **Execution reliability is the second complaint** (Streak, Tradetron). This is another reason not to own execution in the MVP.

---

## 4. Gaps a small entrant could fill cheaply

Reddit could not be reached through the tools (site: searches returned nothing), and YouTube comments were not accessible. **Every niche below is an interview hypothesis (L)**, backed by these signals:

| Gap / niche | Evidence | Strength |
|---|---|---|
| **Guided, curriculum-tied, Hindi-first practice** (not "paper trading" as such) | Plain paper trading is **already abundant and free**: Sensibull virtual trade (free for Zerodha users), Streak's 15 virtual deployments, FrontPage, NSE Paathshala, and AlgoTest free forward tests (L). **The gap is pedagogy, not access:** drills on specific events (Budget day, expiry days, crash sessions) linked to lessons, with a debrief. Signals: TradingQnA requests since 2017 (Zerodha's standalone was not delivered; Sensibull's arrived in 2019); TradingView free can't paper trade NSE; SEBI's figure that 91% of individual F&O traders lost money in FY25 (about ₹1.1 lakh average) | L–M |
| **Hindi-first (original, not dubbed)** | Zero1 found **dubbing failed** and launched original Hindi content (Aug 2026). Pushkar Raj Thakur's Hindi audience is about 18M (L) | M |
| **Trustworthy, reproducible backtests** | Streak and Stratzy review complaints | M |
| **Practice layer for creator cohorts** | Bombay Trading School (3,000+ students) teaches APIs and backtesting; the 1% Club's complaints show under-served post-course support | L–M |
| **Loss awareness / trade journal** | The F&O loss statistic; Zerodha's own "Nudge" friction (case-studies) | L |
| **Cheaper pricing** | Weak. The market is already at ₹0–499/mo (uTrade ₹99, Tradetron ₹300, AlgoTest 25 free backtests/week, Streak free) | **Weak: do not compete on price** |
| **Combined personal finance + learning + paper trading** | The 1% Club is converging here, **with registrations we lack**. The personal-finance side (budgets, affordability) is NOW; portfolio advice is REG | L |

**[P] Recommended niche:** *"Hindi-first F&O and equity practice gym for beginners: learn, practise on replayed markets, review your real trades. No tips, no calls."* The wedge is **practice plus honest review**, not signals, not automation, not price.

---

## 5. Lean MVP (1–2 developers, 8–12 weeks) [P]

### 5.1 Feature list ranked by value against effort, with legal verdicts

Verdicts use doc 17's key. Effort: S ≤ 1 engineer-week, M 2–3, L 4+. Estimates [E].

| Rank | Feature | User value | Effort | Verdict | Notes / guardrails |
|---|---|---|---|---|---|
| 1 | **Lesson paths in Hindi and English** (F&O basics, risk, position sizing, costs), with quizzes | High | M (off-the-shelf CMS / LMS) | **NOW** | No named-stock data newer than the compliance-set lag; G2 deny-list; no return claims |
| 2 | **Payoff / Greeks / position-size calculators on user-entered inputs** (spot, IV, premiums typed in) | High | S–M | **NOW** | No market data. Model stated. No "expected expiry" language. This is the Zero1 calculator pattern (450k users) |
| 3 | **Replay paper-trading sandbox with event drills**: index options and futures plus liquid stocks on **lagged historical bars**; the user steps through a past session (Budget day, expiry, crash days); virtual ₹; realistic costs (STT, brokerage, slippage) shown | High | L | **LICENCE** (intraday F&O history; vendor quote) **and pending the lag question** (CQ-A) | Build it on internal fixtures during weeks 1–12 and launch when the licence lands. Lag is a compliance-set parameter (1 day vs 30 days). **No prizes, contests or cash leaderboards.** Label "replay of <date>, not live" (G7). Replayed option chains are LICENCE (doc 17 #13) |
| 4 | **Trade journal** from the user's **uploaded** tradebook / contract-note CSV (Kotak, Zerodha formats): P&L, costs share, win/loss, holding time, F&O loss awareness | High | M | **NOW** (descriptive, feature #16 A) | Descriptive only; no "you should…" (posture C). **Upload, not API**, for the MVP (the Kite display question stays open) |
| 5 | **No-code backtester of the user's own rules** on **end-of-day** data, reproducible (seeded, versioned data, costs and fills explained, audit log) | Medium–High | L | **LICENCE** (NSE EOD about ₹1L/yr; doc 17) | White-box only; private to the user; no sharing or selling of strategies. Golden-fixture tests (invariant 5) |
| 6 | **AI tutor** that explains concepts and the user's *own* journal numbers, and refuses stock opinions | Medium | S–M | **NOW** (G9 refusal) | Numbers only from deterministic code (invariant 5); pin the model; eval harness |
| 7 | **Creator cohort tooling**: a creator assigns a replay "drill" to their students and sees aggregate completion (not P&L rankings) | Medium (B2B) | M | NOW | Creator must be SEBI-registered, or bound by an education-only contract (§5.3) |
| 8 | Intraday (1-min) replay | Medium | S once data exists | **LICENCE** (vendor quote: TrueData / GDFL) | Storage rights question (doc 17, Q-NSE-5) |
| — | Live-price paper trading | High | M | **Gated** | Only via a broker/exchange agreement or a counsel opinion (CQ-B) |
| — | **Order automation on Kotak or Kite** | High (owner ask) | L | **NO until the ADR**; then C (empanelment) | See §5.5 for the Phase-3 path |
| — | Strategy marketplace / copy trading | — | — | **NO** | Framework: family-only sharing; association rule |
| — | AI CFO / portfolio advice / "should I buy" | — | — | **REG** | 1% Club and Finology hold RIA/RA for this |

**MVP cut (8–12 weeks, 2 developers):**
- **User-facing:** ranks 1, 2, 4 and 6. All NOW, zero data spend.
- **Built on internal fixtures, launched when the licence lands:** ranks 3 and 5.
- **One developer:** ship ranks 1, 2, 4 and 6 only; defer rank 7.
- **Critical path:**
  - the history vendor quote (EOD and intraday F&O) and its storage and display rights;
  - the lag answer (CQ-A).
  - Doc 17's about 3-month licence floor overlaps the whole MVP window.

**Do not** use yfinance or scraped NSE data (CLAUDE.md invariant 7; nsepy / nsetools failures in case-studies).

### 5.2 Monetisation [P]

- **Free:** lessons (level 1), 3 replay sessions per week, journal on one upload.
- **"Practice Pro" at ₹99–149/mo or ₹999–1,499/yr** [E]. Includes unlimited replays, all lesson paths, the backtester, journal history, and the AI tutor with metered questions.
  - Anchors: WebVeda ₹1,999/yr all-access; uTrade ₹99 entry; Tradetron ₹300.
  - Metered AI follows the Screener pattern (case-studies §1.3).
- **B2B cohort seats** for SEBI-registered educators and RAs: ₹X per student per cohort (quote after interviews).
  - This is the highest-leverage revenue [I]. The 1% Club, BTS and Rachana Ranade-style cohorts need a practice layer.
- **Broker account-opening referrals** (Kotak, Zerodha, Upstox): **only if counsel confirms** we are outside the association rule's prohibited categories.
  - That means no advice, no return claims, and lag-compliant education.
  - Treat as upside, not the base case [I].
- **Ruled out:**
  - performance-linked or profit-share pricing;
  - "signals" subscriptions;
  - paid strategy listings;
  - contests with prizes.

### 5.3 Go-to-market: creator partnerships [P]

1. **Partner only with SEBI-registered creators** (RA/RIA: the Finology and 1% Club type), or with education-only creators under a contract that:
   - bans tips and return claims;
   - enforces the named-security data lag;
   - allows content review.
   Zero1's pivot shows the unregistered route is closing.
2. **Offer:** a white-label "practice gym" for the creator's cohort. The creator earns a revenue share on Pro upgrades from their cohort. It is **not** tied to trading volume or P&L.
3. **Hindi first:** produce original Hindi content, not dubs (the Zero1 lesson).
4. **Owned channels:** YouTube and Instagram explainers on "what a replay of the 2024 Budget-day Nifty taught me", using lag-compliant data. Telegram only as a digest with the "information only, not SEBI-registered" line (case-studies §5).
5. **The first 10 partners come from interviews**:
   - 5 registered educators / RAs;
   - 5 cohort programmes (BTS-like);
   - 10 beginner traders in Hindi-belt cities.

### 5.4 Metrics that show it worked [P]

- **Activation:** % of sign-ups who complete lesson 1 **and** one replay session within 7 days (target ≥ 35% [E]).
- **Retention:** W4 replay retention ≥ 20% [E].
- **Conversion:** free to Pro ≥ 2–3% of monthly active users [E].
- **B2B:** ≥ 3 paying cohort partners by week 16.
- **Outcome proxy (honest):** among journal users, the share of cost/charges in gross P&L that they *see*. **No claims that users "made money".**

### 5.5 Phase 3 (gated): order automation on Kotak Neo or Kite

**Preconditions:**
1. An owner ADR that supersedes ADR-008 and amends the CLAUDE.md "never execute trades" rule.
2. Counsel memo.
3. **Either** (a) NSE/BSE algo-provider empanelment through each broker, **or** (b) a **user-self-hosted mode**, where the software runs on the user's own machine with the user's own API key and static IP, like OpenAlgo (AGPL, case-studies §4).

Whether (b) makes us a "provider" is **CQ-C**. Other requirements:
- white-box strategies only (no RA);
- kill switch, per-order confirmations and 10 orders/sec throttling;
- no managed accounts.

Kotak's free API with zero brokerage makes (b) attractive to users [I], but Kotak's data-display terms are unverified.

### 5.6 Key risks

| Risk | Likelihood / impact | Mitigation |
|---|---|---|
| A legally required **lagged replay is less realistic** than the free live-ish incumbents (Sensibull, Streak, FrontPage) | H / M | Sell replay as **event drills plus a debrief tied to lessons**, not as "paper trading" |
| Replay paper trading judged a "virtual trading platform" under PR 37/2024 even when lagged | M / H | Counsel before launch (CQ-A/B); no incentives; lag parameter; label everything "education replay" |
| A creator partner gives tips or claims returns, and brokers cut us off (association rule) | M / H | Registered-first partner list; contract clauses; content review; kill-switch on partner links |
| Data licence cost or timing for history (EOD ₹1L/yr; intraday quote only) | M / M | Start with EOD plus a licensed sample; do not scrape |
| Free broker tools out-feature us (Streak, Dhan, Sensibull) | H / M | Don't compete on tools. Compete on Hindi-first pedagogy + replay + honest journal |
| The 1% Club / BTS builds its own practice tool | M / M | Pitch it as a partner first; stay B2B-friendly |
| F&O regulatory tightening shrinks the audience (Sensibull −28.7%) | M / M | Equity and investing tracks too, not F&O-only |
| Backtest or replay accuracy errors damage trust | M / H | Golden fixtures, cost model shown, reproducible runs (invariants 3–5) |
| Scope creep into signals or "AI picks" | H / H | G2 deny-list, refusal template, no "AI signals" marketing (AI-washing cases) |
| Support and refund failures (the 1% Club's top complaint) | M / M | Self-serve refunds; a small paid tier keeps expectations low |

---

## 6. Owner decisions needed

1. **Scope ADR.** Replace ADR-008 option A with an "India retail learn-practise-review" direction. Decide whether automation is ever in scope; if so, amend the CLAUDE.md rule. **Until then, automation is NO.**
2. **Target user.** Replace 02's US equity-researcher persona with Indian retail beginners and intermediates (Hindi-first)? 02 §4/§6 workflows and hypotheses need rewriting.
3. **Data spend:** NSE EOD (about ₹1L/yr) and a vendor quote for intraday F&O history. **Whether the start is "cheap" depends on this quote.** Without it, only the NOW set can ship.
4. **B2B-first or consumer-first** go-to-market.
5. **Whether to pursue RA registration later** (it unlocks AI CFO-type personalisation, as the 1% Club and Finology did).

## 7. Questions for compliance-analyst (flagged)

- **CQ-A:** For a **replay** of named stocks and index options by an unregistered provider with no monetary incentive, which lag applies? The **1-day** investor-education lag in circular 2024/56, or the **30-day** named-security lag for unregistered educators? Does PR 37/2024 reach a lagged replay at all?
- **CQ-B:** On what basis do Sensibull, AlgoTest forward tests, Tradetron, FrontPage and NSE Paathshala offer live or near-live paper trading after June 2024? Is there a broker-agreement route open to us?
- **CQ-C:** Does distributing self-hosted software that places orders from the user's own machine, key and static IP make us an "algo provider" that needs empanelment?
- **CQ-D:** Can an unregistered, education-only platform receive **broker referral fees** under the Aug/Oct-2024 association circulars?
- **CQ-E:** May a third-party app read a user's **tradebook via the Kite or Kotak API** (account data, not market data) and show analytics to that user?
- **CQ-F:** Does a creator revenue share on Pro upgrades create any "association" exposure for a registered creator partner?

## 8. Unverified / low-confidence list

- The NSE empanelled-provider list (timed out). All empanelment claims (AlgoTest, uTrade, Stratzy, AlgoBulls) are **L**.
- 1% Club: AMFI, IRDAI (Pillow) and RBI registrations not found. The metric conflicts in §1.3 are unresolved. Google Play rating from a snippet only. YourStory article returned 403.
- Stratzy's "2% of capital" fee (snippet); Quantiply prices (AlgoTest blog); uTrade price conflict (₹99–4,999 on the page vs ₹999–14,999 in a snippet).
- Kotak zero-brokerage duration ("first 30 days" vs no end date). Kotak data-display terms for third-party apps were not read.
- The operative text of SEBI PR 37/2024 (the SEBI page body did not load). The Trilegal and Lexology analyses were only partly read.
- How FrontPage and NSE Paathshala handle real-time data after June 2024.
- Reddit and YouTube comment sentiment: not accessible.
- The WebVeda ₹1,999/yr price (Buzzincontent snippet; the BusinessToday article did not state it).
- The 1% Club's Inc42 headcount of 729 vs about 200 after the layoff.

## 9. Sources (all accessed 2026-09-24)

**1% Club**
- https://www.onepercentclub.io/about-us/ (H)
- https://apps.apple.com/in/app/1-club/id1631535570 (H)
- https://play.google.com/store/apps/details?id=com.freedom.android&hl=en_US (snippet, L)
- https://inc42.com/company/the-1-club/ (M)
- https://inc42.com/buzz/sharan-hegdes-the-1-club-get-ria-licence-from-sebi/ (2025-02-03, M)
- https://www.buzzincontent.com/news/finance-creator-sharan-hegdes-1-club-launches-ai-cfo-12398862 (2026-08, M)
- https://www.goodreturns.in/updates/bombay-trading-school-brings-ai-and-automation-to-trading-education-1509883.html (2026-05-21, M)
- https://startuptalky.com/news/sharan-hegde-one-percent-club-layoffs/ (2024-11-09, L–M)
- https://www.businesstoday.in/entrepreneurship/start-up/story/zerodhas-nikhil-kamath-invests-in-finfluencer-sharan-hegdes-start-up-the-1-club-403907-2023-10-31 (M)
- https://www.trustpilot.com/review/onepercentclub.io (H page; L themes)
- https://yourstory.com/2024/07/1-percent-club-simplify-personal-finance-masterclasses-financial-products (403; snippet only)

**Creators**
- https://www.businesstoday.in/latest/trends/story/makes-no-sense-to-continue-ankur-warikoo-shuts-down-profitable-rs100-crore-courses-business-531869-2026-05-17 (M)
- https://www.buzzincontent.com/influencer-marketing/creator-ankur-warikoo-changes-webveda-to-subscription-based-platform-11846364 (snippet, M–L)
- https://tracxn.com/d/companies/ca-rachana-ranade/__Y6nb9R7qmrar_O6s9wVPE3UgKZX_7WHADf9l3IcVPbY (L)
- https://recipe.finology.in/disclaimer (snippet, M)
- https://zerodha.com/z-connect/business-updates/3-years-of-zero1-by-zerodha (2026-08-13, H)
- https://inc42.com/buzz/zerodha-pivots-creator-led-zero1-to-in-house-content-model/ (2026-04-23, M)
- https://creatordb.app/creatorstats/pushkar-raj-thakur/ (L)

**Algo / paper platforms**
- https://tradetron.tech/pages/pricing (H)
- https://docs.algotest.in/getting-started/pricing-breakdown/backtest-pricing/ (snippet, M)
- https://algotest.in/blog/ra-algos-vs-stratzy/ (L, competitor blog)
- https://algotest.in/blog/8-best-algo-trading-platforms-in-india-2026/ (L)
- https://www.utradealgos.com/pricing (H)
- https://apps.apple.com/in/app/utrade-algos/id6446798782 (H)
- https://quantiply.tech/documentation/sebi-regulations-on-algo-trading-2026/brokers-supported-1st-april-onwards/ (H)
- https://stratzy.in/ (L)
- https://apps.apple.com/in/app/stratzy-smart-algo-trading/id1591722308 (H)
- https://apps.apple.com/in/app/streak-unlimited-access/id6476100104 (H)
- https://www.strike.money/reviews/sensibull (M)
- https://www.strike.money/reviews/definedge-opstra (M)
- https://dhan.co/options-trader/ (snippet, M)
- https://www.kotakneo.com/platform/kotak-neo-trade-api/ (H)
- https://investmentguruindia.com/newsdetail/-kotak-neo-introduces-zero-brokerage-zero-fee-trade-apis-for-retail-traders231083 (M)
- https://intradaylab.com/blog/algo-trading-without-coding-india-platforms-comparison (2026-04-04, L)
- https://algotest.in/blog/tradingview-charts-showing-delayed-data/ (L)
- https://businessupturn.com/finance/stock-market/tradingview-free-users-hit-with-a-15-minute-delay-on-nse-and-bse-data-and-how-to-switch-real-time-back-on/ (M)
- https://tracxn.com/d/companies/frontpage/__rg3vxr0EEk5KbH-BpTEgBxRG_IaFZ6pSIygiAhAAJV0 (L)
- https://tradingqna.com/t/can-zerodha-develop-a-platform-that-allows-users-to-paper-trade-derivatives-before-entering-the-market/14286 (2017, H)
- https://www.nseindia.com/static/trade/empanelled-algo-providers-exchange (timed out)

**Regulation**
- https://zerodha.com/z-connect/business-updates/explaining-the-latest-sebi-algo-trading-regulations (2025-02-06, H)
- https://www.sebi.gov.in/legal/circulars/may-2024/norms-for-sharing-of-real-time-price-data-to-third-parties_83572.html (listing); text via https://taxguru.in/sebi/new-sebi-norms-sharing-real-time-price-data-parties.html (M)
- https://www.businesstoday.in/markets/stock-picks/story/sebis-circular-essentially-means-zerodhas-nithin-kamath-highlights-sebis-new-rules-on-real-time-share-price-430915-2024-05-25 (M)
- https://www.sebi.gov.in/media-and-notifications/press-releases/nov-2024/advisory-on-unauthorized-virtual-trading-gaming-platforms_88200.html (PR 37/2024; body not loaded)
- https://www.business-standard.com/markets/stock-market-news/sebi-warns-investors-against-using-unauthorised-virtual-trading-platforms-124110400804_1.html (M)
- https://trilegal.com/knowledge_repository/trilegal-update-sebis-bar-on-sharing-live-stock-market-data-implications-for-virtual-trading-apps/ (M)
- https://www.outlookmoney.com/news/sebi-vs-finfluencers-market-regulator-introduces-new-rule-to-curb-spread-of-investment-advice-from-unregistered-advisories (M)
- https://www.business-standard.com/markets/news/sebi-sets-rules-to-differentiate-educators-from-financial-influencers-125013001316_1.html (M)
- https://www.multibagg.ai/market-pulse/articles/paper-trading-live-data-rules-cmud4c3t200072spfhp0855ry (L)
