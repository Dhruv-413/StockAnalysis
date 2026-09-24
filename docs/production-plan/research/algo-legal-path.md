# The legal path in India for backtesting, paper trading, automated trading and One-Percent-style personal-finance features on Kotak Neo / Zerodha Kite

Author role: Compliance Analyst (Governance). Research date and access date for every source: **2026-09-24**.

**This is not legal advice.** It sorts risks and drafts questions. Items marked **CQ-A-n** go to Indian securities counsel through the owner. Nothing has been sent.

**Labels**
- [F]: fact read on a primary page (regulator, exchange, broker or vendor's own page);
- [F-sec]: fact from a secondary source or a search extract, because the primary page timed out, returned 403 or was an unreadable PDF;
- [F-self]: a firm's claim about itself, read on its own site but not checked against an exchange list;
- [I]: inference; [A]: assumption; [E]: estimate; [P]: proposal.

Confidence is H, M or L.

**Scope rule.** This file does not repeat what is already sourced here:
- `research/feature-legality.md` ("FL"): S1–S34, G1–G11, CQ-1..18, the RA cost table (§4), privacy (§5);
- `research/kite-and-broker-apis.md` ("KB"): Kite terms, static IP applying to order endpoints only, 10 OPS, the Fyers and Upstox data clauses;
- `17-what-is-achievable.md` and `16-india-research-round-3.md`.

Where a point is already settled there, this file cites it by section and adds only what is new.

**Access caveat.** These returned timeouts, 403 or unreadable PDFs:
- NSE (nseindia.com, nsearchives), including the empanelled-provider list, the FAQ of 3 Nov 2025, and circulars 69255, 70309, 71820 and 73992;
- BSE notices (403);
- the SEBI circular PDFs.

So circular text below comes from secondary reproductions, labelled [F-sec]. **Counsel must read the primary texts** before relying on any row.

---

## 0. Bottom line

1. **[I, H] The owner's change of direction does not lift this project's own ban.**
   - CLAUDE.md says: "Never execute trades or add order-placing code." FL #24 classes order placement as legally **C** and **D for this project**.
   - Any automated-trading build first needs an ADR that amends that invariant, and the owner must accept it.
   - The research below describes the legal path; it does not authorise building it.
2. **[F-sec, H] The framework is live.**
   - SEBI's retail-algo framework (circular of 4 Feb 2025) became mandatory for all brokers on **1 Apr 2026**, following the glide path in SEBI's circular of 30 Sep 2025 (§1.1).
   - Since then, **anyone who offers algo order placement to other people must be an exchange-empanelled "algo provider" acting as the broker's agent**. A black-box provider must also be a SEBI Research Analyst (RA).
3. **[I, M] Only one automated-trading variant needs no registration: the self-hosted tool (variant a).**
   - The user runs open-source software on their own machine, with their own API key, their own static IP and their own rules, for themselves and their family.
   - OpenAlgo publicly relies on this position (§3.3).
   - On broker terms this is **not yet clean**. KB reads Kite personal use as software the client develops themselves; Zerodha must confirm that running third-party software counts (Q-Z-7).
   - As a hosted SaaS, both (b) user rules and (c) prebuilt strategies need empanelment. Kotak's own page also requires partners to be **"hosted on broker systems"** (§3.1).
4. **[I, M] Backtesting only (d) is posture A. Paper trading (e) is the risky one.**
   - Backtesting is A (FL #17) if runs are private, we ship no strategies and make no return claims.
   - Paper trading on **real-time** prices faces three problems:
     - SEBI's advisory of 4 Nov 2024 names "paper trading" on real-time prices as an unauthorised activity (§1.6);
     - every data source bars it: Kite "virtual/mock trading apps", Fyers "paper trading", TrueData "Virtual trading / Simulation" (KB §1.7, §4);
     - the Online Gaming Act bans online money games, in force from 1 May 2026, if there are fees and prizes.
   - Paper trading on **EOD or 30-day-lagged** data is the defensible form. Whether 15-min delayed data is allowed is a counsel question (CQ-A-5).
5. **[F, H] One Percent (1% Club) is not an unregistered app. It is a precedent for registering.**
   - Its footer shows a SEBI **RIA (INA000018896)** and a **RA (INH000023968)** held through its group entities.
   - It pulls bank and investment data "from account aggregators" under the adviser entity.
   - A One-Percent clone therefore needs:
     - an IA registration (or a partner) for goal-based or personal advice and for Account Aggregator access;
     - an ARN or EOP route (or IA) for mutual-fund transactions.
   - Courses, community, calculators and expense tracking on user-supplied data can be posture A (§4).
6. **[P] Minimum-compliance MVP** (details in §5):
   - hosted private backtests of the user's own rules on licensed EOD history;
   - EOD / next-day paper trading with no prizes and no leaderboards;
   - education and calculators;
   - expense tracking on user-entered or uploaded data;
   - **no order placement.**

   The cheapest later route to automation, in order:
   1. an open-source self-hosted executor (after the ADR);
   2. partnering with an already-empanelled provider or a broker's in-house platform;
   3. our own white-box-only empanelment (no RA);
   4. RA registration only if black-box strategies are ever wanted.

---

## 1. SEBI retail algo framework

### 1.1 Instruments and timeline

| # | Instrument | What it does | Label, conf. |
|---|---|---|---|
| 1 | SEBI circular SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013, **4 Feb 2025**, "Safer participation of retail investors in algorithmic trading" | The framework. Brokers are principals; algo providers are their agents and must be empanelled; algo orders are tagged; there are no open APIs; the white-box / black-box split; the family limit on self-built algos | [F-sec, H] (FL S11; text via finseclaw, Google Groups secmarkupdates, Taxmann) |
| 2 | NSE circular NSE/INVG/66524, 5 Feb 2025 | NSE forwarding of the SEBI circular | [F-sec, M] (cited on uTrade's blog) |
| 3 | NSE/INVG/67858, **5 May 2025**: implementation standards | 10 OPS threshold; static IP (primary plus one backup; one change per week); OAuth/2FA; daily logout; 5-year audit trail. Its SOP required algos to be hosted on the broker's cloud (see #9) | [F-sec, H] (KB §3; Zerodha Z-Connect; Business Standard) |
| 4 | NSE/INVG/69255, **22 Jul 2025**: "Operational modalities for empanelment of Algo Providers and registration of retail algo strategy" | Empanelment in about T+30 days; strategy approval in T+7 working days (execution algos) or T+10 (others) | [F-sec, M] (search extracts; the PDF timed out) |
| 5 | NSE/INVG/70309, **19 Sep 2025**: empanelment criteria | Includes a self-declaration of cyber or adverse technical incidents in the past 3 years (on letterhead; no auditor signature) | [F-sec, L-M] |
| 6 | SEBI circular SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/132, **30 Sep 2025**: glide path | Brokers ready could go live on 1 Oct 2025. **M1** 31 Oct 2025: apply for API algo product registration plus at least one strategy. **M2** 30 Nov 2025: complete registration. **M3** 3 Jan 2026: mock session. From **5 Jan 2026**, brokers that missed the milestones could not onboard new API-algo retail clients. **Mandatory for all brokers from 1 Apr 2026** | [F-sec, H] (BSE copy via the stock-market-circulars mirror; Taxguru; Upstox) |
| 7 | NSE FAQ on retail algo, **3 Nov 2025** | Reported points: static IP only for self-hosted "tech-savvy" clients; clients of broker-hosted platforms need none; "A Research Analyst offering a black-box strategy must first register as an Algo Provider"; "One provider cannot host multiple third-party RA algos"; black-box algos hosted on broker infrastructure; algo-order tag format; limits on market and IOC orders | [F-sec, L-M] (Fintrens and AlgoIP summaries; **the PDF timed out**) |
| 8 | BSE notice, **4 Dec 2025** (and later): "Algo Provider – Provisional Empanelment" | BSE empanels on a *provisional* basis and posts the list on its website | [F-sec, M] (publicnow index; the page returned 403) |
| 9 | NSE/INVG/73992, **30 Apr 2026** | The current reference circular for empanelment ("updated from time to time"); linked from NSE's empanelled-provider page | [F-sec, M] (search extract of the NSE page; not opened) |

**Hosting conflict (unresolved) [F-sec, M]:**
- **Against vendor hosting:** Zerodha staff (Kite forum 15350, Jul 2025) wrote: "The SOP requires that all algo strategies be hosted on the broker's cloud. We've requested the exchanges and SEBI to reconsider." Kotak's 2026 page says partners must be "exchange empanelled" and "hosted on broker systems" [F, H].
- **For vendor hosting:** Tradetron's Zerodha page tells users to whitelist "your Tradetron static IP" in the Kite developer console [F-self, M]. That implies a vendor-hosted model is still accepted at Zerodha.
- **[I, M]** The requirement may differ by broker, or by white-box versus black-box.
- **This matters for variants (b) and (c).** See CQ-A-3 and Q-K-1.

### 1.2 Definitions

| Term | Content | Label, conf. |
|---|---|---|
| Algo provider | An entity providing algo-trading facilities through APIs extended by stock brokers. It "would be considered to be acting as an agent of the broker". SEBI does not register it directly; the exchanges empanel it | [F-sec, H] |
| Broker as principal | Brokers may offer algos only after exchange permission; they may use **only** empanelled providers; they handle complaints; they may share fees or brokerage with providers only with "prominent and complete disclosures" | [F-sec, H] |
| White box ("execution") | "fully transparent algorithms, where the logic, decision making processes and underlying rules are accessible and understandable to users" and replicable | [F-sec, H] |
| Black box | "the internal workings and rationale / logic of the algo is not known to the user and is not replicable" | [F-sec, H] |
| Black-box duty | The provider must "register as research analysts with SEBI and maintain a detailed research report for each such algo". A change of logic means fresh registration and a new report. Zerodha adds that the report is published periodically | [F-sec, H] |
| OPS threshold | **10 orders per second per client per exchange (segment)**. At or below it: no registration; a generic algo ID. Above it: exchange registration with a unique ID, via the broker, with an auditor certificate and strategy and RMS write-ups. Zerodha says the exchange charges are passed on to the client | [F-sec, H]; charges [F, M] (Kite forum 15350) |
| Algo registration and IDs | Every algo order carries an exchange-specified identifier. Strategies from empanelled providers and brokers are registered **whatever their OPS** | [F-sec, H] |
| Self-built algos ("tech-savvy" retail) | Allowed. The algo may be used only by the developer's family: "self, spouse, dependent children and dependent parents". A static IP is whitelisted by the broker. Register only above 10 OPS | [F-sec, H]. **Kotak allows "up to 10 family members" per static IP [F, M]**; how that maps to SEBI's four-person definition is unclear |
| "Coder for hire" | Zerodha's overview: a developer who writes an algo *for* a client needs no registration; the client is responsible | [F-sec, M] (Z-Connect, via fetch summary) |
| No open APIs | Access only through a "unique vendor client specific API key and static IP whitelisted by the broker", with OAuth and 2FA | [F-sec, H] |

### 1.3 Self-written algo versus a platform for many users

| Question | Retail user running their own algo | Platform hosting or executing algos for many users |
|---|---|---|
| Registration | None up to 10 OPS [F-sec, H] | Exchange empanelment as an algo provider, through the brokers it connects to [F-sec, H] |
| Who may use it | Self and family (spouse, dependent children, dependent parents) [F-sec, H] | Any client of an onboarding broker |
| Strategy registration | Only above 10 OPS | **Every** strategy, whatever its OPS [F-sec, M-H] |
| Static IP | The user's own, whitelisted by their broker | The vendor's IP, or the broker's infrastructure (§1.1 conflict) |
| Black-box logic | N/A (the user knows their own logic) | RA registration plus a research report per algo [F-sec, H] |
| Performance claims | — | Brokers must not associate with platforms claiming past or expected returns (2022 circular, FL S12); PaRRVA only for RAs/IAs (FL S15) |

### 1.4 Becoming an empanelled algo provider: what it takes

| Item | Finding | Label, conf. |
|---|---|---|
| Legal form | The applicant is an entity evaluated on "background, infrastructure, systems etc." [F-sec, H]. Body corporate assumed | [A, M] |
| People | At least one key person with at least 2 years of experience in securities markets | [F-sec, M] (Marketcalls summary of exchange requirements) |
| Certifications | ISO 27001:2022, SOC 1/SOC 2 "or similar" | [F-sec, M] |
| Security testing | VAPT certificates from CERT-In empanelled auditors; the NSE audit rules say the same auditor may audit a vendor for at most 3 consecutive years | [F-sec, M] |
| Declarations | Cyber or adverse-incident self-declaration for the past 3 years (NSE/INVG/70309) | [F-sec, L-M] |
| Infrastructure | India-hosted servers; 5-year audit logs; possibly hosting on broker infrastructure (§1.1) | [F-sec, M] |
| Output | An exchange vendor code; then a separate **agreement with each broker**, as the broker's agent, with its due diligence | [F-sec, M] |
| Time | Empanelment about **T+30 days** after a complete application; each strategy T+7/T+10 working days; each logic change needs re-approval (about 10 working days) | [F-sec, M] |
| Exchange empanelment fee | **Not found.** No public fee schedule was located | unverified |
| Net worth | **Not found.** No source states a net-worth floor for algo providers | unverified |
| Our cost estimate | ISO 27001 certification plus a CERT-In VAPT, a compliance retainer and legal work: roughly **₹8–25 L in year 1**, excluding engineering and broker-integration time | [E, L]. Placeholder only; not sourced |
| RA for black-box | Required (FL §4 has the RA costs: ₹1–10 L deposit, NISM XV, fees, audits). **White-box only avoids it** | [F-sec, H] |
| NSE list of empanelled providers | https://www.nseindia.com/static/trade/empanelled-algo-providers-exchange (download link; **not read: timeout**) | — |

### 1.5 Is RA registration needed for black-box strategies?

- **[F-sec, H] Yes.** The SEBI circular requires it, and the NSE FAQ reportedly adds that an RA offering a black-box strategy must *also* be an empanelled algo provider.
- **[I, M] The open question is white-box *prebuilt* strategies.** An empanelled provider shipping a disclosed "RSI < 30 → buy" template is not black-box. But under FL posture analysis, a named, ready-to-run strategy offered to the public can still be a "trading call" or "recommendation" under the RA Regulations (FL S2). That is **CQ-A-2**.

### 1.6 Real-time price data, virtual trading and paper trading

| Instrument | Content | Label, conf. |
|---|---|---|
| SEBI circular SEBI/HO/MRD/MRD-PoD-3/P/CIR/2024/56, **24 May 2024** (effective 30 days later) | Para 2(i): MIIs and registered intermediaries "shall ensure that no real time price data is shared with any third party including various platforms, except where... required for orderly functioning of the securities market or for fulfilling regulatory requirements". 2(ii): an agreement listing activities and justification, reviewed yearly. 2(iii): data for investor education may be shared "without offering any kind of monetary incentive… with a lag of 1 day". "Real-time" is **not defined** | [F-sec, H] (Taxguru reproduction) |
| SEBI circular of **8 May 2026** (effective 1 Jul 2026) | Modifies **only paras 2(iii)–(iv)** of the May 2024 circular (lag becomes **30 days**; agreements must include an audit trail) and FAQ Q8 of the Jan 2025 circular. **The core bar in 2(i) is unchanged.** NISM gets a one-day lag, for its simulation lab only | [F-sec, H] (CorpLawUpdates; FL S9) |
| SEBI press advisory, **4 Nov 2024** | Cautions against "unauthorised platforms offering virtual trading services, **paper trading** or fantasy games based on real time stock price data of listed companies". It defines paper trading as fictional trades "tied to real-time stock prices". It cites the SCRA 1956 and the SEBI Act 1992; users have no recourse to SCORES or SMART ODR | [F-sec, H] (Khaitan, Mondaq/AZB, TeamLease; the SEBI press-release page was not opened) |
| Promotion and Regulation of Online Gaming Act 2025 plus Rules 2026 (in force **1 May 2026**) | Bans online money games, meaning those played for a fee or stake "with an expectation of winning money or other stakes". This kills paid stock-contest or prize "virtual trading leagues" | [F-sec, M] (PIB, Trilegal, Mondaq) |

**[I, M] What this means for paper trading:**
- A paper-trading feature fed by **real-time** prices hits the exact activity SEBI's advisory names. No licensed source will supply it (KB §1.7, §4; IMD §1.1 TrueData).
- **EOD / next-day simulation** is outside the advisory's "real-time" framing.
- **30-day-lagged** data sits inside the education carve-out.
- **15-min delayed** data is undefined: it is not "real-time" in NSE's product sense, but SEBI has not said so. That is CQ-A-5.
- **How brokers do it.** Broker and empanelled-provider paper trading (Streak "virtual deployments", Tradetron "paper trading", AlgoTest "Paper Trade") runs inside or on behalf of a registered broker, which can justify it under para 2(i). **We cannot inherit that justification** [I, M].

---

## 2. The architecture variants

Tests applied to each variant:
- where orders originate (whose IP and server);
- who wrote the logic;
- whether the logic is disclosed;
- who uses it;
- whether we touch market data;
- whether we make claims.

| Variant | SEBI / exchange posture | Broker and data terms | Classification | Conf. |
|---|---|---|---|---|
| **(a)** Desktop or self-hosted open-source tool. The user plugs in their own API key and static IP and runs their own rules on their own machine (OpenAlgo-style) | The user is the "tech-savvy" self-builder: no registration up to 10 OPS; self and family only. **We distribute software only**: no order routing, no strategies, no broker revenue share | **This conflicts with KB and is not settled.** KB reads Kite's personal-use clause ("a private interface **You**, a Client, **develop**s exclusively for customising personal trading") as covering software the client builds, and rejects bring-your-own-key for that reason. Whether a client running **our distributed** open-source software with their own key counts as personal use is untested. OpenAlgo's position is its own claim, not Zerodha's. **Ask Zerodha (Q-Z-7).** The user pays for their own Kite Connect data (₹500/mo) or uses Kotak's free API. **A paper-trading mode inside the tool** may collide with Kite's "virtual/mock trading apps" clause (Q-Z-5) | **Allowed with conditions on SEBI grounds; Zerodha confirmation pending.**<br>• We ship **no strategies or templates that read as calls** (CQ-A-1).<br>• No hosted relay in the order path (for example, a webhook relay on our server makes the order originate from us).<br>• No telemetry of orders or credentials.<br>• No broker revenue share (FL G11).<br>• No performance marketing.<br>• AGPL obligations if we fork OpenAlgo | M (SEBI); L (Kite terms) |
| **(b)** Hosted SaaS running **user-defined white-box** rules through the user's broker API | We host and execute for many clients, so we are an **algo provider**: empanelment, a per-broker agreement, every strategy registered, and possibly hosting on broker infrastructure (Kotak says yes). No RA needed, because the user wrote and knows the logic [I, M] | Kite multi-user needs Zerodha compliance approval (KB §2). Kotak: partners must be empanelled and broker-hosted [F, H]. Quantiply stopped supporting Kotak from 1 Apr 2026 "due to SEBI Algo Trading regulations" [F-self, M] | **Needs empanelment** | H (need); M (hosting) |
| **(c)** Hosted SaaS with **prebuilt** strategies | As (b), plus: if the logic is hidden, **RA registration plus a research report per algo**, and NSE reportedly bars one provider from hosting multiple third-party RA algos. If the logic is disclosed: empanelment, plus the CQ-A-2 risk that a public prebuilt strategy is a "trading call". Any return display breaches the 2022 circular and PaRRVA (FL S12, S15) | As (b) | **Needs empanelment; plus RA if black-box** (and probably RA-partner review even if white-box, CQ-A-2) | H |
| **(d)** Backtesting only | FL #17: **A** when runs are private, of the user's own rules, with costs and slippage shown and no published results or leaderboards | **Hosted:** needs licensed history with storage rights (NSE EOD about ₹1 L/yr, Q-NSE-5). Kite historical data cannot feed a hosted backtest (personal use; no redistribution; KB §1.7). **Local (in variant a):** the user's own Kite data on their own machine | **Allowed** (hosted: licence precondition) | M-H |
| **(e1)** Paper trading with **live** prices | The SEBI advisory of 4 Nov 2024 names it. The May 2024 circular stops intermediaries and MIIs supplying the data | Kite, Fyers and TrueData all bar it | **Not achievable for us** (would need to be a broker or empanelled provider under a broker's justification) | H |
| **(e2)** Paper trading with **15-min delayed** prices | Not addressed by SEBI. The advisory's definition says "real-time" | The NSE delayed licence must permit simulation use (not asked yet: Q-NSE-8). Vendors may refuse | **Allowed with conditions, pending counsel (CQ-A-5)** | L |
| **(e3)** Paper trading on **EOD / next-day** fills, or **30-day-lagged** replay | Outside "real-time"; the 30-day lag matches the education carve-out | The EOD licence must permit it (Q-NSE-8) | **Allowed with conditions**: no prizes, no entry fees for contests (Online Gaming Act), no leaderboards or returns marketing (FL G5), labelled "simulated" | M |

---

## 3. Kotak Neo, Zerodha and the precedents

### 3.1 Kotak Neo

| Item | Finding | Label, conf. |
|---|---|---|
| Neo Trade API | Free "at present"; ₹0 brokerage on Trade Free plans (API orders from 1 Nov 2025); any Kotak Neo account holder can request access; static IP plus TOTP; up to 10 OPS; market orders converted to limit orders with protection | [F, H] (kotakneo.com Trade API page) |
| **Third-party platforms** | Verbatim (**re-checked in a second fetch**): "As per SEBI circular: Your fintech partner must: Get empanelled with exchanges; Host their infrastructure on broker systems". Also: "confirm with your fintech partner: Are they exchange empanelled? Are they hosted on Kotak infrastructure?" | [F, H] (kotakneo.com static-IP page) |
| Kotak disclaimer page | kotakneo.com/disclaimer was read. It has **no** Trade API, third-party, data or paper-trading clauses. It has only a Strategy Bot liability disclaimer. The devportal documents page came back blank | [F, M] |
| Static IP details | At most 2 IPs; one change every 7 days; "up to 10 family members" may share an IP (static-IP use only, no account access); from 1 Apr 2026 | [F, H] |
| One app per client | "only one API application… per client, hence only 1 algo platform… at a time" | [F-sec, L] (search extract; source page not opened) |
| Formal API terms | No separate Trade API terms were found (see the disclaimer row). `api.kotak.com/terms` belongs to Kotak Mahindra **Bank**'s API platform and is not the broking API; don't rely on it | unverified |
| Market effect | Quantiply: "users will not be able to trade with KOTAK 1st April 2026 onwards due to SEBI Algo Trading regulations" (notice of 28 Mar 2026) | [F-self, M] |
| In-house | Kotak runs its own "Strategy Bot" and reportedly partners with empanelled platforms (e.g. AlgoKing) | [F-sec, L] |

**[I, M]** Kotak is the stricter broker for a hosted third party. Building on Kotak Neo means being **empanelled and deploying inside Kotak's infrastructure**, or being a personal-use tool (variant a).

### 3.2 Zerodha

- **Already sourced** (KB §1.7, §2): multi-user access only with Zerodha compliance approval, "for an exchange approved platform which is built to cater mass"; the terms bar "virtual/mock trading apps"; no redisplay of data.
- **New findings:**
  - Static IP applies to all API order placement from 1 Apr 2026. Family sharing is declared in the developer console ("used exclusively by me and/or my immediate family": spouse, dependent children, dependent parents) [F, H].
  - Staff said the NSE SOP requires hosting on the broker's cloud, and that Zerodha had asked for this to be reconsidered (Jul 2025) [F, M].
  - Zerodha's Feb 2025 explainer: marketplaces "cannot continue" in their old form; individuals may share strategies only with family [F-sec, M].
  - No Zerodha page listing the third-party providers it onboards was found.

### 3.3 Where the named platforms stand now

| Platform | Structure now | Label, conf. |
|---|---|---|
| **Streak** | Runs at `streak.zerodha.com`; described as embedded in Kite; free for Zerodha users since 17 Jan 2024 (CS). The operator named in LinkedIn and Wellfound search titles is Streak AI Technologies Pvt Ltd, a Rainmatter-backed partner; the site fetch gave nothing usable. **"Streak became Zerodha's own" is not verified**: no acquisition was found, and Tracxn (Jun 2026) shows none. **Its empanelment status is not verified** | [F] domain; free-since date [F, H] (CS); operator [F-sec, **L**]; the ownership claim is **unverified** |
| **Tradetron** | Oct 2024: SEBI show-cause notices to 120+ brokers over Tradetron marketplace "assured returns" claims (CS §3.1; Business Standard, 9 Oct 2024). Now says "Tradetron static IP" is whitelisted per user in Kite, and still runs a marketplace. **Empanelment is claimed only in one search extract** | [F-sec, M] (SCNs); [F-self, M] (static IP); **[L] empanelment** |
| **AlgoTest** | Claims to be "NSE and BSE empanelled" (own blog). Runs "RA Algos": strategies authored by **several** SEBI-registered RAs and automated by AlgoTest, with paper and forward testing. **This appears to conflict with** the reported NSE FAQ line "One provider cannot host multiple third-party RA algos" (§1.1 #7, L-M). Possible explanations: the rule has a narrower scope (for example, it applies only to black-box RA algos), each RA is separately empanelled, or the FAQ summary is wrong. **Unresolved (CQ-A-10)** | [F-self, M] |
| **uTrade Algos** | "uTrade Solutions Pvt. Ltd. is an empanelled algo vendor for NSE and BSE" | [F-self, M] |
| **Quantiply** | Reported as NSE-empanelled (search extract). Its own docs: Kotak unsupported from 1 Apr 2026; supports Angel One and Upstox | [F-sec, L] (empanelment); [F-self, M] (Kotak) |
| **Stratzy** | "SEBI-registered Research Analyst (Reg. No: INH000009180)", "empanelled with NSE, BSE & MCX". Prebuilt strategies (40+) under its RA licence. Disclaimer: "Backtested results are simulated…" | [F-self, M] |
| **OpenAlgo** | AGPL-3.0 open-source software: "not a service, a subscription platform, a hosted execution engine, an algo marketplace, a broker, or an advisory". The trader uses their own static IP; no strategy distribution; no broker revenue share | [F-self, H] (docs.openalgo.in/compliance) |

**Pattern [I, M].** Every commercial hosted player has converged on two models:
- **empanelled algo provider**, plus RA registration for prebuilt or black-box strategies (Stratzy, AlgoTest RA Algos, uTrade);
- **broker in-house platforms** (Streak, Kotak Strategy Bot).

The only unregistered model still standing is **software the user self-hosts** (OpenAlgo).

---

## 4. Personal-finance features like One Percent

**Precedent [F, H]** (onepercentclub.io home page and T&Cs):
- The 1% Club operates through One Club Ventures Pvt Ltd (the platform), One Centurion Ventures Pvt Ltd (research and advisory) and One Battalion Ventures.
- It holds **RIA INA000018896** and **RA INH000023968**.
- AI tools use "data… download[ed] from account aggregators in accordance with Your consent artefacts".
- It says masterclasses do not "constitute investment advice or research services".
- Investments are "executed through integrations with third-party platforms".
- Its RIA licence was reported in Feb 2025, about 6 months after application (Inc42, YourStory) [F-sec, M].

| Feature | What it needs | Label, conf. |
|---|---|---|
| **Courses and community** | Posture A (FL #27). Conditions:<br>• named-stock price examples use data at least 30 days old (S9, for "solely education" status in the association rules);<br>• no levels, targets or calls, even in examples;<br>• community posts moderated against tips and calls (the enforcement pattern is calls in Telegram groups, CS §3.1);<br>• no performance claims (Reg 16A / S8);<br>• paid courses are fine;<br>• any broker affiliate deal is an "association" the broker must clear (FL G11) | [F-sec, H] for the rules; [I, M] for moderation |
| **Finfluencer rules** | Reg 16A plus the Oct 2024 and Jan 2025 circulars bind *regulated entities*: no association with anyone giving unregistered advice or making return claims. The "solely education" test uses the 30-day lag. Registered entities show their registration number on every post (from 1 May 2026) | [F-sec, H] (FL S6–S9, S18) |
| **Budgeting and expense tracking** | **Not SEBI.** Data protection applies: SPDI Rules now, DPDP from 13 May 2027 (FL §5).<br>• **SMS reading:** Google Play allows READ_SMS for "SMS-based money management… apps that track and manage budget", **subject to Play review**; non-financial SMS must not be exfiltrated.<br>• **Bank-feed via Account Aggregator:** only a **regulated FIU** may receive data (FL S24). Routes: our own RIA registration (as 1% Club), or a technology-service-provider role for a regulated FIU | [F, H] (Play policy); [F-sec, M] (AA/FIU); [I, M] (TSP route) |
| **Goal planning** | Generic calculators (SIP, FIRE, inflation) on user-entered numbers with no product named: A [I, M].<br>Anything that uses the user's circumstances to suggest an allocation, a product or a scheme is **investment advice → IA registration** (FL S5, #16).<br>An ARN holder may give only limited "incidental", goal-based help. **Sources conflict**: AMFI FAQ versus a Value Research headline "MFDs can't offer incidental advice, asserts SEBI" (page returned 403) | [I, M]; conflict **[L]** (CQ-A-8) |
| **MF discovery** | Factual scheme data (NAV, TER, holdings, returns as published) is A, subject to data rights (AMFI/AMC reuse, Q-O questions).<br>"Best funds", rankings by attractiveness, or "top picks" are recommendation → **B/C** (FL #19–21) | [I, M] |
| **MF investing (transactions)** | Three routes:<br>1. **AMFI ARN** (MF distributor): NISM V-A (about ₹1,500 exam); ARN fee about ₹3,000 + GST for an individual (corporate higher); 3-year validity; regular plans with commission; no advice.<br>2. **Execution-Only Platform (EOP)**: SEBI circular SEBI/HO/IMD/IMD-PoD-1/P/CIR/2023/86, 13 Jun 2023, effective 1 Sep 2023; **direct plans only**. Category 1 is registered with AMFI as the AMCs' agent; Category 2 is registered as a stock broker, as the investor's agent. No advice. Capital and net-worth details **not verified**.<br>3. **RIA**: direct plans, fee-only; client-level segregation from distribution | [F-sec, M] (ARN, EOP); [F, H] (EOP circular id) |
| **IA registration cost** | Dec 2024 amendments: the net-worth test was **replaced by a deposit** (₹1–10 L by client count, liened to BSE as IAASB); graduate qualification plus NISM X-A/X-B. A non-individual IA is required at 300 clients or ₹3 Cr fees. Application fee ₹2,000 (Setu blog: 45–90 days processing) | [F-sec, M] |

---

## 5. Minimum-compliance MVP (very small budget, no registrations)

### 5.1 Can launch now (posture A)

These still need a data licence where marked.

| Feature | Conditions | Licence precondition | Conf. |
|---|---|---|---|
| Private backtesting of the user's own rules (hosted) | FL #17 guardrails:<br>• the user writes the rules; results visible only to them;<br>• costs and slippage shown;<br>• "hypothetical; past ≠ future";<br>• **no templates named as outcomes**, no shared or public result pages (CQ-10), no leaderboards;<br>• no "deploy" button | Licensed EOD history with storage rights (about ₹1 L/yr NSE EOD + vendor; 17 §4). **Not Kite data** | M-H |
| Simulated (paper) portfolio on **EOD / next-day** fills | Labelled "simulation";<br>• no prizes, no paid contests (Online Gaming Act);<br>• no rankings or returns marketing;<br>• no real-time or intraday fills | EOD licence must permit simulation (Q-NSE-8) | M (pending CQ-A-5 and CQ-A-7) |
| Education, courses, community | FL #27 plus moderation; 30-day-lagged examples | — | M-H |
| Goal calculators; expense tracking on user-entered or CSV-uploaded data; SMS parsing (Android) | No product suggestions; DPDP / SPDI hygiene (FL §5); Play review for SMS | — | M (calculators); H (Play SMS exception exists) |
| Open-source self-hosted executor (variant a) | **Only after an ADR amends the CLAUDE.md order-placement invariant.** Conditions:<br>• software only;<br>• the user's key, IP and rules;<br>• no strategies shipped;<br>• no hosted order relay;<br>• no broker revenue share;<br>• no performance marketing | The user's own broker data. Our servers never see it. **Zerodha must confirm this counts as personal use (Q-Z-7)**; Kotak's page is silent on self-run third-party software | M (SEBI); L (broker terms) |

### 5.2 Cannot launch without registration or empanelment (H unless stated)

- Hosted auto-trading, whether of user rules (b) or prebuilt strategies (c). H.
- Live-price paper trading. H.
- Strategy marketplace. H.
- Goal-based product advice. M-H.
- Account Aggregator ingestion. M (CQ-A-9 on the TSP route).
- MF transactions. M-H.

### 5.3 Cheapest compliant route to add automated trading later

These are ordered by cost [P, with E/L on costs].

1. **Self-hosted tool (variant a).** Cost: engineering only. [I, M on SEBI; L until Zerodha answers Q-Z-7]
   - Legal risk: CQ-A-1 (templates) and CQ-A-4 (are we an "algo provider" if we provide software updates or a cloud dashboard?).
   - AGPL if forked from OpenAlgo; keep the software licence separate from data rights.
2. **Hand-off to regulated execution** (no registration of our own):
   - Kite Publisher "trade buttons", or a basket link where the user confirms the order in the broker's UI. Static IP and market protection do not apply to Publisher [F, M] (Kite forum 15912).
   - [I, M] This is not algo trading if a human confirms each order. But the buttons must not be attached to *our* suggestions, which would be B (CQ-A-6).
   - Or refer users to a broker's in-house tool (Streak, Kotak Strategy Bot) without revenue share.
3. **Partner with an empanelled provider or an RA** (uTrade, Stratzy; AlgoTest-style RA Algos). [I, M]
   - We stay the backtest and evidence layer; they hold empanelment and RA duties.
   - Watch for association (Reg 16A) and CQ-16 (a platform hosting RA content).
   - **Contingent:** a multi-RA model may be barred by the reported NSE FAQ line (CQ-A-10). Prefer a single empanelled partner that is itself the RA.
4. **Our own empanelment, white-box only.**
   - About ₹8–25 L in year 1 [E, L], plus ISO 27001/SOC 2, CERT-In VAPT and a 2-year market-experience key person.
   - About T+30 days per exchange once the application is complete, **plus** a separate agreement and possibly broker-hosted deployment for each broker.
5. **Add RA registration only if black-box or house strategies are wanted.**
   - ₹1–10 L deposit, NISM XV, PaRRVA for any performance figure (FL §4).

---

## 6. Counsel questions (new; not sent)

| ID | Question | Why |
|---|---|---|
| CQ-A-1 | "If we distribute open-source, self-hosted trading software that the user runs with their own broker API key and static IP, and it ships **example strategy templates** with disclosed logic, are we an 'algo provider' under the SEBI circular of 4 Feb 2025, or a research analyst ('trading calls')? Does removing all templates change the answer?" | Variant (a) |
| CQ-A-2 | "Is a white-box, disclosed-logic prebuilt strategy offered by an empanelled provider to the public a 'research report' or 'trading call' needing RA registration, even though the circular requires RA registration only for black-box algos?" | Variant (c) |
| CQ-A-3 | "After NSE/INVG/67858, 69255 and 73992 and the NSE FAQ of 3 Nov 2025, must an empanelled provider's white-box platform be hosted on each broker's infrastructure, or may it run on its own India-hosted servers with a whitelisted vendor IP?"<br>Evidence to include: Tradetron asks each Zerodha user to whitelist *Tradetron's* IP, while Zerodha's console makes the user declare the IP is used "exclusively by me and/or my immediate family". So either a separate vendor-IP route exists, or those declarations are inaccurate | Variants (b) and (c); the Kotak versus Tradetron conflict |
| CQ-A-4 | "Does any hosted component, such as a cloud dashboard, a signal or webhook relay, or pushed software updates that change execution logic, turn a self-hosted tool into a hosted 'algo provider' service?" | Variant (a) boundary |
| CQ-A-5 | "Does the SEBI advisory of 4 Nov 2024 on paper trading, read with the circular of 24 May 2024, reach a simulation that uses **15-minute delayed** licensed prices, with no monetary incentive? Does it reach EOD or next-day fills?" | Variants (e2) and (e3) |
| CQ-A-6 | "Is a 'send to broker' order button (Kite Publisher-style), where the user confirms each order in the broker's interface, 'algorithmic trading' or order placement on behalf of clients requiring any approval?" | Route 2 |
| CQ-A-7 | "Would a subscription-priced paper-trading feature with no prizes be an 'online money game' under the Online Gaming Act 2025?" | Variant (e) |
| CQ-A-8 | "Can an AMFI ARN holder today give goal-based 'incidental' scheme suggestions, or must that be RIA? Which route (ARN, EOP Category 1 or 2, RIA) is cheapest for an app that lets users invest in direct plans?" | §4 |
| CQ-A-9 | "May an unregistered app receive Account Aggregator data as a technology service provider to a regulated FIU, and on what contract terms?" | §4 |
| CQ-A-10 | "Does the NSE FAQ of 3 Nov 2025 bar one empanelled provider from hosting strategies of several third-party RAs? If so, does it cover white-box RA strategies, and how do multi-RA platforms (e.g. AlgoTest 'RA Algos') comply?" | Route 3 |

**Vendor and exchange questions (new; for the owner to send):**
- **Q-K-1 (Kotak, Neo Trade API support).** "Your static-IP page says fintech partners must be 'exchange empanelled' and 'hosted on broker systems'. What is the onboarding process, what are the fees and infrastructure terms, and is a white-box-only provider treated differently? Is a personal-use open-source tool run by your client on their own IP permitted?"
- **Q-Z-5 (Zerodha).** "Does the Kite terms' ban on 'virtual/mock trading apps' apply to a paper-trading mode inside open-source software that a client runs privately with their own Kite Connect subscription?"
- **Q-Z-6 (Zerodha).** "What is Zerodha's process and hosting requirement for onboarding an exchange-empanelled algo provider after 1 Apr 2026? How is a vendor's shared static IP reconciled with the developer-console declaration that the IP is used only by the client and their immediate family?"
- **Q-Z-7 (Zerodha).** "Does 'personal use' under the Kite Connect terms cover a client running **third-party open-source software** (e.g. OpenAlgo) on their own machine, with their own Kite Connect key and static IP, where the software author never receives the client's data, credentials or orders?"
- **Q-NSE-8.** "Do the EOD and 15-min delayed display licences permit simulated or paper-trading use by the licensee's users, without prizes?"

---

## 7. Unverified and low-confidence items

1. The primary texts of every NSE circular (67858, 69255, 70309, 73992) and the NSE FAQ of 3 Nov 2025: timeouts. The FAQ points in §1.1 #7 are **L-M**.
2. The NSE empanelled-provider list (timeout) and the BSE provisional list (403). Empanelment claims for Tradetron (L), Quantiply (L), AlgoTest, uTrade and Stratzy (vendor self-claims, M).
3. The ownership and empanelment status of Streak. "Became Zerodha's own" is **unverified**.
4. Empanelment fees and any net-worth floor: **not found**. The ₹8–25 L estimate is unsourced [E, L].
5. The final hosting rule (broker infrastructure versus vendor): conflicting evidence.
6. The Kotak Neo formal API T&C. The disclaimer page has none; the devportal page came back blank. The "one API app per client" rule (L).
7. The SEBI press release of 4 Nov 2024 was read only through law-firm summaries. A secondary claim of a SEBI "notification of 17 Aug 2026" on live data (multibagg.ai) was **not verified and is not relied on**.
8. EOP capital and net-worth requirements; corporate ARN fees; the conflict over MFD incidental advice.
9. Whether the Online Gaming Act reaches subscription-only simulations (CQ-A-7).

---

## 8. Sources (all accessed 2026-09-24)

**SEBI and government**
- https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html (headers only). Text via:
  - https://www.finseclaw.com/article/finsec-tracker-on-sebi-issues-guidelines-on-retail-participation-in-algorithmic-trading
  - https://groups.google.com/g/secmarkupdates/c/5rIMqAiiKYc
  - https://www.taxmann.com/post/blog/taxmanns-analysis-making-algo-trading-safer-accessible-for-retail-investors
  - https://spiceroutelegal.com/publications/regulating-algo-providers-sebis-norms-on-algorithmic-trading/
- The SEBI circular of 30 Sep 2025 (CIR/2025/132):
  - https://rhnvrm.github.io/stock-market-circulars/circulars/bse/2025/bse-2025-11-24-e6eac9e12bd239db-adherence-to-milestones-and-the-rules-related-to-retail-algo/
  - https://taxguru.in/sebi/sebi-extends-algo-trading-implementation-timeline-april-2026.html
  - https://upstox.com/news/market-news/financial-regulations/sebi-extends-timeline-for-retail-algo-trading-framework-sets-glide-path-for-brokers/article-182285/
- The SEBI circular of 24 May 2024: https://taxguru.in/sebi/new-sebi-norms-sharing-real-time-price-data-parties.html ; https://www.sebi.gov.in/legal/circulars/may-2024/norms-for-sharing-of-real-time-price-data-to-third-parties_83572.html
- The SEBI circular of 8 May 2026: https://www.corplawupdates.in/updates/sebi-30-day-lag-educational-price-data-norms-2026
- The SEBI advisory of 4 Nov 2024:
  - https://www.khaitanco.com/thought-leadership/SEBI-Cracks-Down-on-Unauthorised-Gaming-and-Trading-Platforms
  - https://www.mondaq.com/india/securities/1552142/sebi-cracks-down-on-unauthorised-gaming-and-trading-platforms
  - https://www.teamleaseregtech.com/updates/article/36751/sebi-issued-an-advisory-on-unauthorized-virtual-tradinggaming-platform/
- EOP: https://www.sebi.gov.in/legal/circulars/jun-2023/regulatory-framework-for-execution-only-platforms-for-facilitating-transactions-in-direct-plans-of-schemes-of-mutual-funds_72479.html ; https://www.taxmann.com/post/blog/sebi-introduces-framework-for-execution-only-platforms-for-investing-in-direct-plans-of-mf-schemes/
- IA amendments: https://www.sebi.gov.in/legal/regulations/dec-2024/securities-and-exchange-board-of-india-investment-advisers-second-amendment-regulations-2024_89980.html ; https://taxguru.in/sebi/sebi-eases-rules-investment-advisers-research-analysts-2024-overhaul.html
- Online Gaming Act:
  - https://www.pib.gov.in/PressReleasePage.aspx?PRID=2241804&reg=3&lang=2
  - https://trilegal.com/knowledge_repository/trilegal-update-the-promotion-and-regulation-of-online-gaming-act-2025-redrawing-indias-online-gaming-landscape/
  - https://www.mondaq.com/india/social-media/1785870/the-promotion-and-regulation-of-online-gaming-act-2025-and-the-promotion-and-regulation-of-online-gaming-rules-2026

**Exchanges** (mostly unreadable here)
- https://www.nseindia.com/static/trade/empanelled-algo-providers-exchange (timeout)
- https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAQ_Retail%20Algo_03112025_NSE.pdf (timeout). Summaries:
  - https://blogs.fintrens.com/nse-retail-algo-trading-rules-nov-2025-static-ip-order-tagging-compliance-guide/
  - https://algoip.in/compliance
- https://nsearchives.nseindia.com/content/circulars/INVG67858.pdf (KB)
- https://www.marketcalls.in/exchange-news/exchange-compliance-for-algo-vendors-what-you-need-to-know.html
- https://www.marketcalls.in/market-regulations/new-nse-rules-for-retail-algo-trading-what-retail-traders-algo-platforms-and-brokers-must-now-do.html
- BSE provisional empanelment: https://www.publicnow.com/view/5EA2216F49EFDA33758575CA12038F245AE5481F?1764830919= (403; search extract)

**Brokers**
- Kotak:
  - https://www.kotakneo.com/platform/kotak-neo-trade-api/
  - https://www.kotakneo.com/platform/kotak-neo-trade-api/static-ip-details/
  - https://www.kotakneo.com/investing-guide/articles/retail-algo-trading-rules-nse-circular/
- Zerodha:
  - https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/static-ip
  - https://kite.trade/forum/discussion/15350/notes-on-the-nse-circular-prescribing-operating-procedures-for-api-usage
  - https://kite.trade/forum/discussion/15912/preparing-to-comply-with-sebis-retail-algo-rules-static-ip-ratelimits-order-types
  - https://zerodha.com/z-connect/business-updates/explaining-the-latest-sebi-algo-trading-regulations
  - https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework
  - https://nithinkamath.substack.com/p/nses-new-retail-algo-trading-circular

**Platforms**
- https://docs.openalgo.in/compliance
- https://tradetron.tech/broker/zerodha
- https://tradetron.tech/
- https://algotest.in/blog/best-tradetron-alternatives-in-2026/
- https://docs.algotest.in/ra-algos/research-analyst/
- https://docs.algotest.in/broker/kotakneo/
- https://www.utradealgos.com/
- https://stratzy.in/
- https://quantiply.tech/documentation/broker-setup/kotak-securities/
- https://quantiply.tech/documentation/sebi-regulations-on-algo-trading-2026/regulations-an-introduction/
- https://streak.zerodha.com/
- https://www.business-standard.com/amp/markets/news/sebi-scrutinises-brokers-linked-to-algo-trading-with-guaranteed-returns-124100901218_1.html

**Personal finance**
- https://www.onepercentclub.io/
- https://www.onepercentclub.io/terms-and-conditions/
- https://inc42.com/buzz/sharan-hegdes-the-1-club-get-ria-licence-from-sebi/
- https://setu.co/blog/licences-for-fintechs-to-go-live-on-account-aggregator
- https://cskruti.com/account-aggregator-is-ria-registration-becoming-more-than-just-about-advice/
- https://support.google.com/googleplay/android-developer/answer/10208820
- ARN and NISM:
  - https://creso.in/blog/nism-fees-registration-costs-2026
  - https://www.bajajfinserv.in/investments/how-to-get-arn-number
  - https://www.amfiindia.com/Themes/Theme1/downloads/FAQsonRoleofMFDsAdvts.pdf (unreadable)
  - https://www.valueresearchonline.com/stories/200465/mutual-fund-distributors-can-t-offer-incidental-advice-asserts-sebi/ (403)
