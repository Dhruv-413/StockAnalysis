# Case studies: what people and companies have actually tried (India-first information-only market assistant)

Research and access date for every source: **2026-09-24** unless noted otherwise. Owner: product-manager. Status: research appendix draft (not yet in `docs/production-plan/research/`).

**Labels** (as in the house rules): [F] verified fact, [I] inference, [A] assumption, [E] estimate, [P] proposal. **Confidence:** H = primary page read; M = reputable secondary source (Entrackr, Inc42, Business Standard, law firm) or a primary search snippet; L = vendor or SEO blog, review sites, Reddit, Trustpilot, or a single unverified source.

In §9, "H listing" means the primary URL appeared in search results but its body was not read. Treat those as **M**.

**Tech stack** is "not disclosed" unless stated. Known stacks:
- Public Alpha: OpenAI GPT-4;
- Composer: Alpaca trading API;
- Dhan Fuzz: its own "artham" model on India-hosted GPUs (prior appendix);
- BloombergGPT: a 50B-parameter in-house model;
- Kite MCP: Go, on the Kite Connect APIs (repo);
- the Indian OSS sentiment repos: FinBERT plus scraped news.

**Scope rule.** This appendix does not repeat the prices and features already in [distribution-and-competitors-india.md](distribution-and-competitors-india.md) and [products.md](products.md): Trendlyne, Screener, Tickertape, StockEdge, Sensibull and Streak pricing; the Fuzz, GR 1 and ARQ feature rows; the Upstox and Fyers MCP basics; Perplexity, Robinhood, Schwab, Public, Composer and Koyfin pricing; SEC 2024-36; and the agent-repo star counts. It adds **outcomes**: traction, what worked, what failed, regulatory run-ins, pivots and shutdowns.

---

## 0. Bottom line

1. **In India, the products that make money from retail "stock ideas" are SEBI-registered.** Univest (RA INH000013776) grew revenue to ₹44.1 Cr in FY25 with 5 lakh+ paid users but still lost ₹30 Cr [F, M, Inc42 2026-02-21]. Liquide (RA INH000009816, per its own site) runs an AI bot, "LiMo", that gives BUY/SELL/HOLD [F, L]. Angel One's ARQ Prime runs under Angel's RA licence INH000000164 [F, M]. The unregistered versions of the same idea end in SEBI orders:
   - Baap of Chart: ₹17.2 Cr disgorgement (2023);
   - Asmita Patel: ₹104 Cr collected, ₹53.67 Cr impounded (2025);
   - Avadhut Sathe: ₹601 Cr from 3.37 lakh people, ₹546 Cr impounded (Dec 2025);
   - Yash Garg: Telegram "premium calls" (Mar 2026).

   14 §1 already says signals need RA registration. **What is new is traction evidence:** registered signals businesses grow in India (Univest) and carry losses and complaints about their calls (Trustpilot, L). This is an input to the owner's decision in 14 §9 Q2. It does not correct the doc.
2. **The account-owning platforms give AI away free, and the independents survive by specialising or being acquired.**
   - Zerodha: Kite MCP is free; Streak was made free in Jan 2024.
   - Perplexity: India finance data is free.
   - Robinhood: Cortex is bundled into $5 Gold; Digests had been used by ~1M customers.
   - Composer was **acquired by SoFi** (June 2026).
   - FinChat **renamed itself** Fiscal.ai to move from "chat" to "data infrastructure plus API plus MCP" (June 2025).
   - The funded winners (AlphaSense at $700M ARR, Rogo at 35k bankers) sell **proprietary content plus workflow to institutions**. They do not sell chat to retail.
3. **What kills or damages products in this space:**
   - regulatory change (Sensibull revenue −28.7% in FY25 after the F&O curbs; Tradetron's broker links cut after SEBI notices to 120+ brokers);
   - scraping exchange sites (nsepy and nsetools broke repeatedly, 2021–2024);
   - hallucinated numbers (Bloomberg's AI news summaries needed ≥36 corrections in Q1 2025);
   - false AI claims (SEC: Delphia, Global Predictions, Rimar; SEC/DOJ: Nate);
   - news-licence exposure (Dow Jones v. Perplexity, headed to a jury trial).
4. **Implication [P].** Our wedge in 14 §2 option A (cited, information-only evidence layer, delivered over MCP) is consistent with every failure case here. It is weakest on **monetisation**. No standalone Indian AI *assistant* has shown paid traction. The paid information products are small-team tools where AI is metered or an add-on: Screener AI at ₹10–30 per answer, and StockEdge at ₹33 Cr FY25 revenue (L) from tools plus education. Larger paid traction sits in registered advice (Univest) or in B2B/professional data (the Fiscal.ai API/MCP; TipRanks and Benzinga selling to brokers). Test B2B (RAs, brokers, newsletter writers) alongside a metered retail tier, not unlimited retail chat.

---

## 1. Indian AI and market-assistant products

### 1.1 Zerodha (Kite, Kite MCP, Varsity, Nudge, Streak)

| Field | Finding | Label, conf. |
|---|---|---|
| What they built | **Kite MCP** (announced 2025-05-15/20): connects a Zerodha account to Claude, Cursor, VS Code and Windsurf. Portfolio, P&L, positions, margins and market data. **Hosted `mcp.kite.trade` is read-only** ("excludes potentially destructive trading operations"). **Self-hosted** builds expose `place_order`/`modify_order`/`cancel_order`, which can be disabled with `EXCLUDED_TOOLS`. | [F] H, github.com/zerodha/kite-mcp-server; zerodha.com/products/mcp |
| Kite MCP terms | Repo licence **MIT**. About 317 stars (GitHub page; API returned 403). The product page and the support article give **no AI-specific data-use or AI-output-responsibility terms**. They carry only generic disclaimers ("we don't give stock tips"; "subject to market risks"). **ChatGPT is not listed** as a supported client on either page. The **support article conflicts with the product page**: it says "Order placement is not available except for **GTT orders**", and that portfolio and historical trade data are "currently unavailable". The product page says read-only including portfolio. Treat hosted scope as "read-mostly, GTT allowed" until clarified. Hosted use needs no API keys. The **Kite Connect** rule still applies: data "cannot be displayed on other platforms" (see prior appendix). | [F] H (licence, clients, support article); stars M; scope conflict unresolved |
| Rationale (founder) | Kamath: "AI tools have become so good that you can have a reasonably competent personal financial assistant." In the same post he **quotes Kailash Nadh ("K")**: accessing services "outside of their walled gardens and bloated UIs riddled with dark patterns" is "liberating", but it "concentrates decision-making and mediation in the hands of AI blackboxes." | [F] H, nithinkamath.me/blog/zerodhas-kite-mcp-is-now-live (2025-05-15); X post M |
| CTO view | Nadh ("MCP seems viral", 2025-05-19): technically "a very simple API spec", but he worries about accountability for "errors and failures with real-world implications" in AI orchestration. Nadh ("This time, it feels different", 2023-05-13): LLMs could obsolete 20%+ of jobs at Zerodha. This led to the 2023 "we will not fire anyone" AI policy. | [F] H, nadh.in; M, BusinessToday 2023-05-12 |
| AI as a differentiator | Kamath (2026-08-17): decks leading with "we use AI" make his "eyes roll". AI is table stakes. **Correction to the prior appendix:** that BusinessToday article does **not** contain the "users build their own AI interface over broker rails" idea. The closest source is **Nadh's** "walled gardens" line, quoted in Kamath's Kite MCP post (above). | [F] H |
| Nudge / Kill Switch | Order-ticket "nudges" warn on risky orders (naked options, large orders near expiry) and require acknowledgement. The Kill Switch disables segments. This is behavioural friction *against* over-trading, not a signal. | [F] M, z-connect kill-switch post; secondary explainers |
| Varsity | Free; no login, no ads, no Zerodha pitch ("no agenda"). About 2M users and 4M downloads (secondary). Varsity Live added in 2024. | [F] M, BusinessToday 2024-05-27; Kamath X post |
| Streak pricing change | Paid tiers were about ₹500 / ₹900 / ₹1,400 per month [M]. **Free for all Zerodha users from 2024-01-17** via the Rainmatter partnership (5 live, 15 virtual deployments, 5 live scanners). Zerodha's stated reason: enable disciplined, rule-based trading. **No mention of SEBI.** Comments complained that free users lost paid features (dynamic contracts). | [F] H, z-connect 2024-01-17 |
| Link to SEBI algo rules? | The free switch (Jan 2024) **predates** the SEBI retail-algo consultation (Dec 2024) and circular (Feb 2025). Any causal link is **not supported**. The more plausible driver is Zerodha's pattern of bundling Rainmatter tools free to retain brokerage (Sensibull, Streak) [I]. | [I] M |
| Business model | Brokerage. FY25 revenue ₹8,809 Cr, PAT ₹4,231 Cr (down from ₹9,949 Cr / ₹5,494 Cr in FY24). | [F] M, secondary financial summaries |
| Regulatory | None found against these products. | — |
| **Lesson for us** | The largest Indian broker's strategy is **free rails, no first-party chatbot, no tips, and friction against over-trading**. Our server must sit *beside* Kite MCP (14 §7). It should never try to replicate portfolio access. Kite MCP's lack of data-use terms does **not** override the Kite Connect no-redisplay rule. | [I] |

### 1.2 Broker assistants: Dhan Fuzz, Groww GR 1, Angel One ARQ Prime

| Product | New outcome data (beyond the prior appendix) | Label, conf. | Lesson |
|---|---|---|---|
| **Dhan: Fuzz** | Announced Aug-2025 by Raise Financial Services. It was to "connect with users' financial portfolios and income tax returns" to give personalised insights and "**actionable recommendations**". Free tier, premium "coming". No user or query numbers found. Tracxn lists no funding (L). | [F] M, Moneycontrol journalist post on X; bankonbasak.com | A broker-owned, cited, multilingual assistant is already free. The "actionable recommendations" wording is covered by Dhan's own registrations, which we would lack. |
| **Groww: GR 1** | Launched at Groww Next on 2026-02-28. Opt-in beta for 30–50k users. "Advises but does not act"; consent layers. No GA date or price found. | [F] M, Business Standard 2026-02-28; Entrackr | Groww frames its assistant as "research analyst"-like and portfolio-personalised. It can do that as a regulated intermediary. |
| **Angel One: ARQ Prime** | A rule-based engine recommending up to 15 stocks, with a published history of past calls. Runs under **Angel One's SEBI RA registration INH000000164**. | [F] M, angelone.in support page and knowledge centre | Signals from a broker are legal because the broker is a registered RA. This is not a loophole we can use. |

### 1.3 Independent research and analytics platforms

| Product | What they built / stack | Traction (source, date) | Model and price | Worked / failed | Regulatory | Conf. | Lesson |
|---|---|---|---|---|---|---|---|
| **Screener.in** | Fundamentals screener since 2009. **Screener AI** (July 2025) answers questions over annual reports and concalls. | "1.6 crore Indians" (self-described, not active users) [L]; team of 1–10, no outside funding [M, Tracxn / about page] | Premium plus pass-through AI credits (see prior appendix) | **Worked:** a tiny team and trust with value investors. Pricing each AI answer at LLM cost-plus keeps margins safe. | None found | M | Pass-through, metered AI pricing is **accepted** by serious Indian users. Evidence that a metered tier beats unlimited chat (see 09). |
| **Tickertape** (Smallcase spin-off, Nov 2021) | Screener, scorecards, Pro tier | FY22 revenue ₹3.01 Cr, loss ₹16.4 Cr. **Laid off 29 people (~30%) on 2023-04-27** ("internal restructuring", tight funding) | Subscription (prior appendix) | **Failed (partly):** a revenue-to-burn mismatch in retail research subscriptions | None found | M (Entrackr page read; secondary) | Retail research SaaS in India burns cash. Budget for a small team. |
| **Smallcase** | Model-portfolio distribution through brokers; managers are SEBI RAs/RIAs | FY25 revenue ₹106 Cr (+57%), net loss ₹34 Cr, EBITDA loss ₹9 Cr; about $120M raised; ~$285–290M valuation | Fees from managers and brokers | **Worked:** B2B2C through broker integrations. **Still loss-making at ₹100 Cr.** | Managers are registered | M (Entrackr, Head & Tale) | Distribution through brokers works, but only with **registered** content creators. |
| **Trendlyne** | Analytics, deal alerts, MarketMind AI credits | About $2.64M raised (IIFL, others) [L]; no FY25 figures found | Subscription plus ads | Unknown | None found | L | Deal alerts already exist. Differentiate on move alignment and citations. |
| **Tijori Finance** | Research and tracking tools (segment data, concall notes) | **$5M round led by Zerodha, Nov 2025**; about $9.3M total; ~45 staff [L, Tracxn / Inc42 profile] | Subscription | Alive, not shut down | None found | L–M | Zerodha/Rainmatter funds research tools, a possible partner route. Needs verification. |
| **Sensibull** | Options analytics; free for Zerodha users | **FY25 revenue ₹28.4 Cr, down 28.7% from ₹39.8 Cr; PAT ₹0.48 Cr** [M, Inc42 financials] | Freemium, subsidised by the broker | **Hurt by** the SEBI F&O curbs (Nov 2024 onward) [I] | None against it | M | **Regulatory concentration risk.** An F&O-dependent product shrank when SEBI tightened F&O. Keep options analytics non-core. |
| **StockEdge** (Kredent / StockEdge Fintech) | Scans, AI chart patterns, Elearnmarkets education | FY25 revenue ₹33.3 Cr (StockEdge Fintech) vs ₹26.3 Cr FY24 (Kredent) [L, Tracxn]; about $13.4M raised; 2M+ users (2021) | Subscription tiers plus courses | Steady growth; pairs education with tools | None found | L | Education plus tools is a proven bundle, but stay inside SEBI's education carve-out (no recent price data in education content). |
| **Stockal / Borderless** | US-stocks investing for Indians | "$2B+ transactions" (self-claim) [L] | Brokerage / FX | No shutdown found | LRS/TCS constraints | L | The global leg for Indian users is a distinct and crowded category. Not our core. |
| **Univest** | "Advisory-first broking superapp": RA stock picks, F&O ideas, broking from Feb 2025 | **FY25 revenue ₹44.1 Cr (3.5×), net loss ₹30 Cr, 5 lakh+ paid users, 75 lakh+ downloads**; broking 10–12% of revenue, 60–65% of it from F&O; FY26 target about ₹130 Cr [M, Inc42 2026-02-21]. Series A $10M [M, Entrackr] | ₹5–17/day subscriptions | **Worked:** paid retail demand for calls. **Failed (per users):** Trustpilot complaints of losses, upsell pressure, and "5/5 targets" marketing [L] | Registered RA INH000013776 | M (financials); L (complaints) | Paid retail demand exists for *calls*, not information. It comes with reputational risk and heavy compliance. |
| **Liquide** | App with AI bot "LiMo" giving BUY/SELL/HOLD; RA-registered | "50,000+ investors", "5M+ downloads" (self-claims) [L]; pre-seed per Crunchbase [L] | Subscription | Unknown | RA INH000009816 (vendor site) [L] | L | An "AI advisor" in India = a registered RA plus an LLM front end. |

### 1.4 AI "stock advisor" apps SEBI acted against

**Finding [F, M]:** no SEBI order was found that targets an app *specifically for AI claims*. The enforcement pattern is **unregistered advice sold as education or through Telegram/WhatsApp**, whatever the technology (§3.1). SEBI is using AI *against* violators:
- the in-house tool **Sudarshan** (2025);
- **1.33 lakh** misleading posts escalated in FY26 up to Feb-2026;
- **66 fake trading apps** removed;
- with Google, a "verified" Play Store badge on 600+ registered-entity apps (2026-03-26) [F, M, MediaNama; newsonair].

The one near-AI case is **Tradetron**: SEBI issued show-cause notices to **120+ brokers** (including Zerodha, Motilal Oswal and 5paisa) in Oct 2024 for continuing to integrate with an algo platform that allegedly showcased strategies promising assured returns [F, M, Outlook Money]. Listed as unverified: the primary SEBI document was not found.

---

## 2. Global AI finance assistants

| Case | What they built / stack | Traction (source) | Model / price | Worked / failed / pivot | Regulatory / legal | Conf. | Lesson |
|---|---|---|---|---|---|---|---|
| **BloombergGPT** (Mar 2023) | A 50B-parameter model trained on Bloomberg's proprietary data plus public data (arXiv 2303.17564) | Internal | n/a | **Overtaken:** later work found GPT-4 matched or beat it on most public financial NLP benchmarks without finance pretraining (Li et al., EMNLP 2023 industry track, arXiv 2305.05862; the abstract compares with domain-specific models but does not name BloombergGPT). Bloomberg shifted to grounded product features. | — | L (the arXiv abstract read does not name BloombergGPT; the head-to-head claims are secondary) | **Do not train or fine-tune a "finance LLM" as a moat.** Data, grounding and workflow are the moat (consistent with 15-finance-model-layer). |
| **Bloomberg Terminal AI** | Earnings Call Summaries (2024-01-23) with **each point shown beside its source**; Document Insights Q&A (2025-04-07); ASKB (2026) | Terminal base | Terminal subscription | **Worked:** source-adjacent summaries for institutions. **Failed (news side):** Bloomberg News AI article summaries (from 2025-01-15) needed **≥36 corrections by late March 2025**: a hallucinated tariff date, wrong figures, active vs passive funds confused. Bloomberg: 99% met standards. | — | M (NYT via Washington Times, Nieman Lab); H for the launch PR | A 1% error rate on numbers is public and embarrassing at scale. **This supports our numeric verifier** (14 §6: numbers only from the card). |
| **Perplexity Finance** | Answer engine plus finance hub; India data (Aug 2025); concall transcripts | Finance usage "grew 8×" since its 2025 launch (company claim via Outlook Business) [L–M]; Airtel Pro bundle offered to ~360M *eligible Airtel subscribers* (not Perplexity users) [M] | Free / Pro $20 | Growing free distribution | **Dow Jones & NY Post v. Perplexity** (S.D.N.Y. 1:24-cv-07984): copyright and trademark claims over its RAG index, verbatim reproduction and **hallucinations attributed to the publishers**. Survived jurisdiction; in discovery; jury trial expected [M, CourtListener, Loeb] | M | **News summaries need licences** (matches 14 §1). A hallucination attributed to a named source is also a trademark risk. Headline plus link plus our own facts only. |
| **Robinhood Cortex** | Digests, then a chat assistant that can research and trade (Q1 2026) | Digests used by **~1M customers**; Gold 4.3M subscribers (Q1 2026) [M, Robinhood Q1-2026 results/transcript] | Bundled in $5 Gold | **Worked as retention for a bundle.** Separately, Robinhood's robo-adviser (2025) **walked back plans to use AI** for picks and relies on human teams [M, RIABiz 2025-02-07] | Registered BD/RIA | M | AI is a feature of the account owner, not a standalone retail product. |
| **Public.com Alpha / Agents** | Alpha on GPT-4 (2023); agents that execute (2026-03); prediction-market agents (2026-09-24) | Not disclosed | In-broker | Evolved from chat to agents that act. That requires broker status. | BD | M | The destination of retail AI is execution, which is out of scope for us (CLAUDE.md). |
| **Composer** | No-code, AI "Trade with AI" strategies; executes on Alpaca | "$215M of automated trades per day" (vendor claim) [L] | $0–32/mo | **Acquired by SoFi, announced 2026-06-23** (SoFi 10-Q, BusinessWire) | Composer Securities LLC (broker) | M | The exit for AI trading tools is acquisition by a platform with an account base. |
| **Fiscal.ai (formerly FinChat)** | Fundamentals terminal plus Copilot, then an API and MCP | $10M Series A (June 2025, Portage); $13M total [M] | Subscription plus API | **Pivot:** renamed because "ambitions expanded beyond the Chat interface" toward "financial data infrastructure through its Terminal and APIs" [M, TMCnet / company X post; blog page returned 403] | — | M | **Chat alone was not the business; verified data plus API/MCP was.** This directly supports our "evidence server" framing. |
| **AlphaSense** | Enterprise search over filings, broker research and expert calls | ~$540M ARR end-2025 to ~$700M (June 2026); $7.5B valuation ($350M round, 2026-06-03); 88% of the S&P 100 [L–M, Sacra/secondary]; **bought Tegus for $930M** (2024) [M, PR Newswire] | Enterprise seats (~$18k/seat claimed, L) | **Worked:** proprietary content (expert transcripts) plus workflow | — | M | Moats are **licensed or proprietary content**, not models. |
| **Rogo** | Agentic platform for bankers | 35k+ bankers at 250 firms; Series B $50M (Apr 2025), C $75M (Jan 2026), D $160M (Apr 2026); >$300M total [M, PR Newswire, SiliconANGLE] | Enterprise | Worked in an institutional niche | — | M | Vertical workflow for professionals raises money; retail chat does not. |
| **Hebbia** | Document-analysis agents for finance and law | ~$13M ARR (Jun 2024) to ~$24.6M (2025) [L, Latka/Sacra]; $130M Series B at ~$700M (Jul 2024, a16z) [M] | Enterprise | Growth slower than its valuation implied [I] | — | L–M | Even well-funded document AI grows linearly. Treat Indian enterprise TAM estimates cautiously. |
| **Koyfin** | Terminal-style dashboards | 100k users (2020) to 500k+ (2023) [L]; ~$3.9M revenue est. 2025 [L]; bootstrapped 2 years, about $6.7M raised [M] | Freemium, $39–299/mo | Capital-efficient; moved up to an Advisor tier | — | L–M | A small team plus a professional tier is viable. |
| **Magnifi (TIFIN)** | Conversational AI investing app plus trading | $2B+ linked assets (mid-2024) [M, PR Newswire] | Subscription | No shutdown found | — | M | No clear outcome. |
| **Kavout** | Kai Score (1–9) ML ranking plus InvestGPT | No numbers found | Subscription | Still operating; "predicts outperformance" | None found | L | Score-based "AI predicts" products are exactly what our invariants forbid. |
| **Danelfin** | AI Score (1–10), "probability of beating the market" | Self-reported backtest alpha (+21% annualised for 10/10 stocks since 2017) [L] | Subscription | Operating | None found | L | Marketing that rests on backtested alpha is the AI-washing risk zone (§3.2). |
| **TipRanks** | Smart Score; AI Analyst reports (Apr 2025); **Enterprise API sold to brokers** | Not disclosed | Retail plus B2B | B2B licensing to brokers is a durable channel [I] | — | L–M | Selling to brokers is a route that avoids retail CAC. |
| **Q.ai (Forbes-backed)** | "AI investing" robo app (2021) | — | Managed kits | **Shut down 2023-12-08** [L, blog; PitchBook] | — | L | An "AI" label did not rescue robo economics. |

---

## 3. Enforcement and failure cases

### 3.1 SEBI: finfluencers and unregistered advice (India)

| Case | Date | Conduct | Channels | Amounts | Legal hook | Conf. | Lesson |
|---|---|---|---|---|---|---|---|
| **Mohammad Nasiruddin Ansari, "Baap of Chart"** (+ Padamati, Golden Syndicate Ventures) | Interim order cum SCN, **2023-10-25** | Stock recommendations "under the garb of educational courses"; misleading profit claims | X, Telegram, YouTube (4.43 lakh subscribers), paid courses | **₹17.2 Cr** disgorgement; market ban | Unregistered IA (SEBI Act s.12(1), IA Regulations) | M (SEBI order page seen as a search listing only; details from Business Standard / Inc42) | "Education" is no shield if content names stocks with levels. |
| **Asmita Patel Global School of Trading** ("She Wolf"/"Options Queen") + 5 others | Interim order **2025-02-06** | Course participants given "specific buy/sell recommendations along with stop loss, target price" | Telegram groups, email, live sessions | ₹104.6 Cr collected; **₹53.67 Cr impounded** | Unregistered IA/RA | M (Business Standard, Tribune) | Stop-loss and target outputs are the bright line. |
| **Avadhut Sathe Trading Academy (ASTAPL)**, Avadhut and Gouri Sathe | Interim order **2025-12-04**; **SAT 2026-01-22** made relief conditional on a **₹100 Cr deposit** | Stock tips, live trading calls, unrealistic return claims sold as education | Courses, live sessions | **₹601.37 Cr from 3.37 lakh+ people; ₹546 Cr impounded** | Unregistered IA and RA | M (Business Standard; the order PDF exceeded the fetch size limit) | The largest case to date. Scale does not protect a "trading academy". |
| **Yash Garg / Yash Trading Academy** | Order, **Mar 2026** | Paid "premium calls" and account handling; claimed SEBI registration and guaranteed returns | Telegram channels (YTA, YTA Premium), matched to phone numbers | ₹92.98 lakh; refunds; **2-year ban** | Unregistered IA/RA/PMS | M (SEBI order listing plus MediaNama) | SEBI traces Telegram operators through phone numbers and bank accounts. |
| **Tradetron / 120+ brokers** | Oct 2024 | An algo platform allegedly showcasing strategies with assured returns; brokers kept integrating after undertakings to stop | Broker APIs | SCNs to brokers | 2022 circular on algo returns claims; association rules | M (Outlook Money) | Brokers carry the association risk, so **brokers will cut off partners** that look like advice or assured returns. |
| **Systemic** | 2025–26 | SEBI PR 27/2025 (2025-05-21) warning about WhatsApp/Telegram scams. From May 2026, registered entities must show their registration number on every post. AI surveillance (Sudarshan, Google) | — | 1.33 lakh posts escalated | — | M | A new Telegram or WhatsApp market bot will be pattern-matched against scam channels. Show "not SEBI-registered; information only" prominently. |

### 3.2 US: AI-washing (SEC / DOJ / FTC)

| Case | Date | What was claimed vs reality | Outcome | Conf. |
|---|---|---|---|---|
| Delphia; Global Predictions | 2024-03-18 | False claims about AI use and client data in models | $400k total (see products.md S39) | H |
| **Rimar Capital** (Itai Liptz, Clifford Boro) | 2024-10-10 | Claimed "AI-driven" trading and inflated AUM ($16–20M claimed vs < $2M actual); raised ~$4M from 45 investors | $310k penalties; 5-year bar for Liptz plus ~$213k disgorgement | M (sec.gov 2024-167 search listing; Debevoise) |
| **FTC Operation AI Comply** | 2024-09-25 | DoNotPay ("AI lawyer"), Ascend Ecom (≥ $25M consumer harm), Ecommerce Empire Builders, Rytr (fake reviews), FBA Machine/Passive Scaling (> $15.9M) | Settlements and bans (DoNotPay $193k) | H (ftc.gov press release read) |
| **Nate Inc. / Albert Saniger** (SEC + SDNY criminal) | 2025-04-09 | "AI" shopping app whose transactions were done manually by contract workers; raised $42M+ | Pending; first AI-washing actions under the new administration | M (DLA Piper, Debevoise; SEC LR-26282 search listing) |

**Pattern:** enforcement targets **capability and performance claims**, not the use of AI. Any "accuracy", "AI-powered signals" or backtested-alpha marketing needs substantiation (consistent with 14 §6 "honest claims").

---

## 4. Open-source attempts (GitHub; stars via api.github.com search, 2026-09-24, H)

| Repo | Stars | Last push | Licence | What / fate |
|---|---|---|---|---|
| marketcalls/**openalgo** | 2,721 | 2026-09-24 | **AGPL-3.0** | Self-hosted algo platform bridging to Indian brokers. Active. Now operates under the SEBI algo framework (static IP, algo IDs from 2026-04-01) [I] |
| zerodha/**pykiteconnect** | 1,310 | 2026-09-15 | MIT | Official client. Healthy because it uses the *licensed* API |
| maanavshah/stock-market-india | 1,039 | 2023-12-17 | MIT | NSE/BSE scraping API. **Stale since 2023** |
| vsjha18/**nsetools** | 907 | 2025-03-18 | MIT | Scrapes nseindia.com. Issues: "not working in AWS & Heroku" (2021-07), "HTTP 301 Moved Permanently" (2023-08, 2024-01), "403 forbidden" (2024-12), "is nsetools… being discontinued for free usage?" (#149) |
| swapniljariwala/**nsepy** | 808 | 2023-12-24 | Other | Issues: "Nsepy is Not working on Cloud" (2022-01), "**NSEPY no longer work after April 2023** – TooManyRedirects" (2023-05), still open 2025. **Effectively dead** |
| pranjal-joshi/Screeni-py; pkjmesra/PKScreener | 706; ~398 | 2026 | MIT | Breakout screeners. Active |
| kaushikjadhav01/Stock-Market-Prediction… | 893 | 2024-02 | MIT | ML plus sentiment "prediction" web app, a student-project pattern |
| zerodha/kite-mcp-server | ~317 | active | MIT | Official MCP (§1.1) |
| mtwn105/zerodha-mcp and others | ≤ 32 | 2025 | various | Community MCPs pre-dating the official one; superseded |
| Indian news-sentiment repos (e.g. rooneyrulz/agentic-stock-research-system 119; RelativelyBurberry/Indian-Stock-News-Sentiment-Analysis 6) | ≤ 119 | 2025–26 | mostly none | FinBERT plus scraped news. Tiny adoption. Most carry **no licence**, so they cannot be reused |

**Common failure modes [F, H from issue titles; I for causes]:**
1. NSE changes its site or cookie flow and adds bot protection: redirect loops, 301s and 403s.
2. Cloud IP ranges are blocked (AWS/Heroku), so a scraper that works on a laptop fails in production.
3. Maintainers abandon the project once the cat-and-mouse becomes unsustainable.
4. Sentiment and "prediction" repos stay demos: no licensed data, no evaluation, no licence.

Only repos built on **licensed broker APIs** stay healthy, and those APIs forbid redistribution. This confirms the 14 §5 rule: no NSE/BSE scraping.

---

## 5. Distribution lessons

| Channel | Evidence of what happened | Conf. | Lesson |
|---|---|---|---|
| **Telegram / WhatsApp market bots** | Almost every Indian enforcement case in §3.1 ran on Telegram. NSE issues named warnings (e.g. "Trade with Anjali/Neha", Aug 2026 PR). SEBI PR 27/2025 targets WhatsApp and Telegram "VIP" groups. OSS alert bots exist (e.g. an NSE_Alerts_Telegram_Bot repo) but show no traction. WhatsApp bans general AI assistants from 2026-01-15 (prior appendix). | M | Telegram reach is real, but the channel is **stigmatised**. Use a verified identity, a visible "information only, not SEBI-registered" line, no calls, no "VIP", and no assured-return language. Prefer a digest format over chat. |
| **Broker MCP servers** | Zerodha Kite MCP (free, MIT, hosted read-only, self-hosted can trade); Upstox and Fyers official (prior appendix). Kamath's rationale: users escaping "walled gardens". No AI-specific data-use terms on Zerodha's page. | H | Brokers are giving away "connect my account". Our lane is the evidence server beside it. Kite Connect's no-redisplay clause means we cannot pull prices from the user's Kite MCP into our own store. |
| **TradingView** | Brokerage integrations are live for Fyers (2023-06-27), Dhan ("40,000+ traders connected", L) and Angel One; Zerodha has no direct integration. A cottage industry of webhook-to-broker bridges (tradingviewbot.in etc.) now falls under the SEBI algo framework. TradingView ships its own AI Copilot (prior appendix). | M | TradingView is a **broker's** channel (integration program) and an **algo** channel (webhooks, regulated). Neither suits an information product. Our route to TradingView users is a web app or MCP, not an overlay. |
| **Brokers as distributors** | Smallcase (₹106 Cr revenue via broker integrations) and TipRanks/Benzinga (B2B to brokers) show that broker distribution works. Tradetron shows brokers will be forced to cut partners. | M | A broker partnership needs us to be demonstrably non-advisory, with logs (the 14 §5 guardrails), or registered. |

---

## 6. Patterns

**What wins**
1. **Owning the account** (Robinhood, Groww, Dhan, Angel, SoFi via Composer). AI becomes a free retention feature [F/I, M].
2. **Registration plus calls** in Indian retail (Univest, Liquide, Angel ARQ). This makes revenue, but losses and complaints persist [M].
3. **Proprietary or licensed content plus professional workflow** (AlphaSense/Tegus, Rogo, Bloomberg). Institutions pay [M].
4. **A data/API layer instead of chat** (Fiscal.ai's pivot; TipRanks Enterprise; Benzinga WIIM) [M].
5. **A small team with trusted, cost-pass-through pricing** (Screener) [M].
6. **Answers shown with their sources** (Bloomberg earnings summaries, Perplexity citations) [M].

**What kills or damages**
1. **Unregistered advice under the "education" label**, especially on Telegram. The largest penalties in Indian market history for individuals fall here [M/H].
2. **Regulatory shocks to the underlying activity** (the F&O curbs cut Sensibull revenue 28.7%; algo rules reshaped Tradetron and the bridges) [M].
3. **Scraping exchange sites.** Breakage is guaranteed and ToS exposure follows [H].
4. **Hallucinated numbers at scale** (Bloomberg's ≥36 corrections) and **unlicensed news reuse** (Dow Jones v. Perplexity) [M].
5. **Overstated AI capability or performance** (SEC/DOJ/FTC cases) [H/M].
6. **Retail research subscriptions without a cost-disciplined team** (Tickertape layoffs; Smallcase and Univest still loss-making) [M].
7. **Building a domain LLM as the moat** (BloombergGPT overtaken by general models) [M].

---

## 7. Implications for our scope and positioning [P]

1. **Keep option A (information-only, cited evidence layer)**. No case contradicts its safety. **New input for 14 §9 Q2:** registered signals (option B) is a real market. Univest reached ₹44 Cr revenue, but at a ₹30 Cr loss and with complaints about its calls.
2. **Lead with B2B or professional buyers; offer retail only as a metered tier.** Retail information products earn small, metered revenue (Screener AI, StockEdge). Larger paid traction exists for registered advice and for professional/institutional data and workflow. Priority for I-08 interviews:
   - SEBI RAs (they need an AI-use disclosure and audit trail);
   - newsletter writers and educators (they must avoid the Baap of Chart / Sathe trap: an evidence tool with no calls helps them stay compliant, a candidate value proposition to test);
   - small brokers or platforms (B2B API, like TipRanks and Benzinga).
3. **Market it as a data/evidence API plus MCP server, not "AI chat".** This follows the Fiscal.ai pivot and Kamath's "AI is table stakes". Avoid "AI-powered signals" language entirely (AI-washing cases).
4. **Hard product rules reinforced by cases:**
   - numbers only from deterministic cards (Bloomberg);
   - headline, link and time only for unlicensed news (Perplexity suit);
   - no NSE/BSE scraping (nsepy, nsetools);
   - no stop-loss, target or "calls" wording, even in educational content (Patel, Sathe);
   - options analytics non-core (Sensibull).
5. **Telegram is allowed, but in digest form.** Show a registration-status disclaimer, keep it identity-verified, and never use VIP or premium-call language.
6. **Exit reality:** independent AI trading and assistant tools tend to be acquired by account owners (Composer to SoFi) or funded by them (Tijori by Zerodha). A Rainmatter/Zerodha relationship is a plausible strategic path [I], but only for a strictly non-advisory product.

**For compliance-analyst:** (a) confirm the Tradetron SCN facts and the association-rule consequences for any broker B2B deal; (b) confirm the education carve-out as applied in the Sathe and Patel orders; (c) confirm that the May-2026 registration-number-per-post rule does not apply to unregistered information publishers, and what disclaimer they should show instead.

---

## 8. Unverified / low-confidence list

- Avadhut Sathe order body (the PDF exceeded the fetch size limit); all figures come from Business Standard (M).
- Baap of Chart order body (only the SEBI page listing and press coverage); the Asmita Patel order was not opened.
- Tradetron: the primary SEBI/NSE document was not found (Outlook Money only).
- No SEBI order specifically about "AI" claims by a stock-advice app was found. This may exist under different wording.
- Kite MCP star count (GitHub API 403; page says ~317). ChatGPT support status: absent from both the product page and the support article, not confirmed either way. **Hosted scope conflict:** the product page says read-only with portfolio; the support article says GTT orders are allowed and portfolio/historical data are "currently unavailable". The repo language (Go) was not re-checked this session.
- Fiscal.ai rename rationale: the company blog returned 403; wording from a TMCnet repost and the company X post.
- BloombergGPT vs GPT-4 benchmark claims: the arXiv abstract read does not name BloombergGPT; the specific numbers (e.g. FinQA 68.79%) are from a secondary blog (L).
- AlphaSense ARR figures (Sacra/secondary, L–M); Hebbia ARR (Latka, L); Koyfin revenue (Latka, L).
- Dhan Fuzz traction: none published. The "actionable recommendations" wording is from the launch coverage, not askfuzz.ai.
- Liquide and Univest user counts are company or app-store claims; Univest complaints are Trustpilot (L).
- Sensibull FY25 figures from the Inc42 financials page via search (M); the causal link to the F&O curbs is [I].
- Tijori $5M Zerodha-led round (Tracxn/Inc42 profile snippet, L–M).
- Stockal status; Magnifi, Kavout and Danelfin traction; TipRanks broker-licensing scale.
- Varsity user numbers (secondary).
- Q.ai shutdown date (a single blog plus PitchBook, L).
- Dhan's "40,000+ traders connected to TradingView" (secondary, L).
- Robinhood Cortex "~1M customers" and Gold 4.3M (search snippet of the Q1-2026 transcript, M; primary not opened).
- Reddit / TradingQnA / HN sentiment: no substantive Kite MCP or AI-assistant threads were found; not covered.

---

## 9. Sources (all accessed 2026-09-24)

**Zerodha**
- https://github.com/zerodha/kite-mcp-server (H)
- https://zerodha.com/products/mcp/ (H)
- https://support.zerodha.com/category/trading-and-markets/general-kite/others-kite/articles/connect-zerodha-ai-assistant (H)
- https://nithinkamath.me/blog/zerodhas-kite-mcp-is-now-live/ (2025-05-15, H)
- https://x.com/Nithin0dha/status/1925137840868147302 (M)
- https://nadh.in/blog/mcp-seems-viral/ (2025-05-19, H)
- https://nadh.in/blog/this-time-it-feels-different/ (2023-05-13, H)
- https://www.businesstoday.in/technology/news/story/we-will-not-fire-anyone-nithin-kamath-shares-zerodhas-new-ai-policy-381045-2023-05-12 (M)
- https://www.businesstoday.in/technology/artificial-intelligence/story/ai-is-no-longer-a-startup-pitch-differentiator-says-zerodha-ceo-nithin-kamath-549595-2026-08-17 (H)
- https://zerodha.com/z-connect/streak/streak-is-now-available-for-all-zerodha-users-at-no-cost (2024-01-17, H)
- https://zerodha.com/z-connect/console/introducing-kill-switch (M)
- https://www.businesstoday.in/india/story/instead-of-just-listening-to-experts-you-can-nithin-kamath-introduces-varsity-live-takes-stock-market-education-beyond-lectures-431097-2024-05-27 (M)

**Indian products**
- https://x.com/chandrarsrikant/status/1960301326245703749 (Fuzz, M)
- https://www.bankonbasak.com/p/introducing-fuzz (M)
- https://www.business-standard.com/companies/news/groww-builds-ai-powered-platform-across-trading-wealth-and-fixed-income-126022800536_1.html (M)
- https://entrackr.com/news/groww-showcases-ai-powered-investing-tools-at-groww-next-2026-11168623 (M)
- https://www.angelone.in/support/other/research-recommendations (M)
- https://www.investorgain.com/article/angel-one-arq-prime-review/162/ (L)
- https://x.com/ayushmitt/status/1942861243632509159 (Screener AI, M)
- https://entrackr.com/2023/04/smallcase-backed-tickertape-layoff-30-workforce/ (2023-04-27, H)
- https://entrackr.com/exclusive/exclusive-smallcase-crosses-rs-100-cr-revenue-mark-in-fy25-9493192 (M)
- https://theheadandtale.com/news/smallcase-operating-revenue-jumps-57--to-rs-106-crore-in-fy25/ (M)
- https://inc42.com/company/sensibull/financials/ (M)
- https://inc42.com/company/tijori/latest/ (L–M)
- https://tracxn.com/d/companies/tijori/__tY1XUcRUCW-t8el7Cjp2NHwLGFWA0Jg_vbqbrzQJrFI/funding-and-investors (L)
- https://tracxn.com/d/legal-entities/india/stockedge-fintech-private-limited/__7unROlJbUR99_5Jdto6YJr2RkhtSy-5Z0RNJp6QFIMc (L)
- https://inc42.com/buzz/univest-eyes-nearly-200-revenue-growth-in-fy26-ceo-pranit-arora/ (2026-02-21, H)
- https://entrackr.com/snippets/retail-advisory-platform-univest-raises-10-mn-in-series-a-8550272 (M)
- https://www.trustpilot.com/review/univest.in (L)
- https://liquide.life/ (L)
- https://pitchbook.com/profiles/company/171222-76 (Trendlyne, L)

**Global**
- https://arxiv.org/abs/2303.17564 (M)
- https://arxiv.org/abs/2305.05862 (H abstract)
- https://www.bloomberg.com/company/press/bloomberg-launches-ai-powered-earnings-call-summaries (H listing)
- https://www.washingtontimes.com/news/2025/mar/29/bloombergs-use-ai-summaries-articles-leads-numerous-corrections/ (M)
- https://www.niemanlab.org/reading/bloomberg-has-a-rocky-start-with-a-i-summaries/ (M)
- https://www.courtlistener.com/docket/69280523/dow-jones-company-inc-v-perplexity-ai-inc/ (M)
- https://www.loeb.com/en/insights/publications/2025/08/dow-jones-and-company-inc-v-perplexity-ai-inc (M)
- https://www.outlookbusiness.com/deeptech/artificial-intelligence/perplexity-adds-live-transcripts-india-market-data-to-finance-dashboard-free-access-for-users (M)
- https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-first-quarter-2026-results (M)
- https://www.fool.com/earnings/call-transcripts/2026/04/28/robinhood-hood-q1-2026-earnings-transcript/ (M)
- https://riabiz.com/a/2025/2/7/robinhood-is-launching-plain-vanilla-robo-advisor-an-ria-that-allocates-with-algorithms-but-walks-back-intent-to-use-ai-and-will-rely-on-human-teams-to-pick-investments (M)
- https://tearsheet.co/the-quarterly-review/the-quarterly-review-publics-leif-abraham-on-three-new-products-simplification-and-ai-washing/ (M)
- https://fortune.com/2026/09/24/public-ai-trading-agents-prediction-markets-kalshi-tie-up/ (M)
- https://www.businesswire.com/news/home/20260623095057/en/Introducing-Composer-by-SoFi-AI-Powered-Investing-From-Idea-to-Execution (M)
- https://www.sec.gov/Archives/edgar/data/0001818874/000181887426000054/sofi-20260630.htm (H listing)
- https://x.com/Fiscal_ai/status/1934990836334297337 (M)
- https://blog.tmcnet.com/blog/rich-tehrani/financial/finchat-rebrands-as-fiscal-ai-raises-10m-series-a-to-build-the-future-of-financial-data-infrastructure.html (M)
- https://www.prnewswire.com/news-releases/alphasense-completes-acquisition-of-tegus-302190934.html (M)
- https://sacra.com/c/alphasense/ (L–M)
- https://www.prnewswire.com/news-releases/rogo-raises-160m-series-d-to-scale-the-agentic-platform-for-finance-302756546.html (M)
- https://sacra.com/c/hebbia/ (L)
- https://getlatka.com/companies/hebbia.com (L)
- https://www.alleywatch.com/2019/09/koyfin-invest-financial-data-analytics-rob-koyfman/ (M)
- https://getlatka.com/companies/koyfin.com (L)
- https://www.prnewswire.com/news-releases/magnifi-now-providing-ai-powered-investment-intelligence-on-over-2b-of-linked-self-directed-assets-302183080.html (M)
- https://www.kavout.com/academy/investgpt (L)
- https://danelfin.com/ (L)
- https://www.tipranks.com/news/tipranks-launches-the-worlds-most-comprehensive-ai-stock-analyst (L)
- https://enterprise.tipranks.com/ (L)
- https://dandesim.one/2023/11/07/farewell-to-q-ai-is-this-the-end-of-ai-investing (L)

**Enforcement: India**
- https://www.sebi.gov.in/enforcement/orders/oct-2023/interim-order-cum-scn-in-the-matter-of-unregistered-investment-advisory-activities-of-mohammad-nasiruddin-ansari-baap-of-chart_78333.html (H listing)
- https://inc42.com/buzz/sebi-cracks-down-on-finfluencer-baap-of-chart-orders-inr-17-cr-disgorgement/ (M)
- https://www.business-standard.com/markets/news/fined-rs-17-crore-by-sebi-all-you-need-to-know-about-baap-of-chart-123102600383_1.html (M)
- https://www.business-standard.com/markets/news/sebi-bans-asmita-patel-she-wolf-stock-market-finfluencer-crackdown-125020700959_1.html (M)
- https://www.sebi.gov.in/sebi_data/attachdocs/dec-2025/ORDER_1764842991.pdf (Sathe order; fetch exceeded the size limit)
- https://www.business-standard.com/markets/news/sebi-impounds-rs546-cr-bars-avadhut-sathe-academy-unregistered-advice-125120401454_1.html (M)
- https://www.business-standard.com/markets/news/sat-directs-avadhut-sathe-trading-academy-to-deposit-100-crore-126012201233_1.html (M)
- https://www.sebi.gov.in/enforcement/orders/mar-2026/order-in-the-matter-of-mr-yash-garg-proprietor-of-yash-trading-academy_100663.html (H listing)
- https://www.medianama.com/2026/03/223-sebi-unregistered-advisor-telegram-social-media-scrutiny-complaint/ (M)
- https://www.outlookmoney.com/invest/equity/sebi-issues-notices-to-more-than-120-stockbrokers-over-tradetrons-assured-returns-claims-report-reveals (M)
- https://www.sebi.gov.in/media-and-notifications/press-releases/may-2025/caution-to-investors-on-stock-market-scams-through-social-media-platforms_94064.html (H listing)
- https://www.medianama.com/2026/03/223-sebi-google-verify-stock-trading-apps-use-ai-track-finfluencers/ (2026-03-26, M)
- https://nsearchives.nseindia.com/web/pressrelease/2026-08/PR_cc_10082026_20260810132028.pdf (M, search snippet)

**Enforcement: US**
- https://www.sec.gov/newsroom/press-releases/2024-167 (Rimar, H listing)
- https://www.debevoise.com/insights/publications/2024/10/sec-announces-settled-charges-against-rimar-cap (M)
- https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes (H listing)
- https://www.ftc.gov/news-events/news/press-releases/2025/02/ftc-finalizes-order-donotpay-prohibits-deceptive-ai-lawyer-claims-imposes-monetary-relief-requires (M)
- https://www.sec.gov/enforcement-litigation/litigation-releases/lr-26282 (Saniger, H listing)
- https://www.dlapiper.com/en/insights/publications/2025/04/doj-and-sec-send-warning-against-ai-washing-with-charges-against-technology-startup-founder (M)

**Open source (H, GitHub API)**
- https://api.github.com/search/repositories?q=kiteconnect&sort=stars
- https://api.github.com/search/repositories?q=nse+OR+nsepy+OR+jugaad+OR+openalgo+OR+pykiteconnect+OR+nsetools&sort=stars
- https://api.github.com/search/repositories?q=indian+stock+sentiment&sort=stars
- https://github.com/swapniljariwala/nsepy/issues/251
- https://github.com/swapniljariwala/nsepy/issues/220
- https://github.com/vsjha18/nsetools/issues/152
- https://github.com/vsjha18/nsetools/issues/149
- https://github.com/vsjha18/nsetools/issues/129

**Distribution**
- https://www.tradingview.com/blog/en/fyers-broker-joins-tradingview-38898 (M)
- https://kr.tradingview.com/chart/NIFTY/lbmpNXa7-Now-Live-Trade-Directly-on-Dhan-from-TradingView-Mobile-Apps (L)
- https://tradingqna.com/t/zerodhas-integration-with-tradingview/177136 (L)
- https://tradetron.tech/blog/sebi-algo-trading-rules-in-india-2025 (L)
