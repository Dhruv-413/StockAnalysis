# Distribution, competition and positioning research: AI market assistant (India-first plus global)

Research date: 2026-09-24. All URLs were accessed 2026-09-24 unless noted. Confidence: H = primary source read, M = reputable secondary or a primary search snippet, L = vendor or SEO blog, or unconfirmed.
Labels used: **[F]** verified fact, **[I]** inference, **[A]** assumption, **[E]** estimate, **[P]** proposal.

---

## 0. Read first: this conflicts with the current product thesis

`docs/production-plan/02-product-thesis.md` (status: proposal) describes a different product. The owner has to choose explicitly. Neither version should replace the other silently.

| Dimension | 02 (current) | Owner's new ask | What the evidence below says |
|---|---|---|---|
| Market | US-listed only (§4) | India-first plus global | In India, the account-owning incumbents give the "AI assistant" away free (§2). |
| User | Independent researchers, 30–200 names | Everyday users of TradingView, Groww, Zerodha and Angel One | This is mass retail. Willingness to pay is ₹150–500/mo, and brokers bundle the tools (§3). |
| Form | No free-form chat (§5) | Chat assistant | Chat is the most crowded form: GR1, Ask Angel, Fuzz, Perplexity, Chart Copilot, broker MCPs. |
| Claims | No signals, sentiment scores or forecasts (§5) | Sentiment, indicators, "algos" | In India, buy/sell calls need SEBI RA/IA registration. Retail algos fall under the SEBI 2025 algo framework (§5). |
| Speed | "Does not sell speed" (§1) | About 300 ms replies | Achievable only for structured and cached lookups, not for grounded LLM synthesis (§6). |

**[P]** Decide this before any spec work: (a) keep 02 and treat India as a later expansion, or (b) re-thesis around the India wedge in §7. The combination of "India retail chat, signals and algos" is not recommended.

---

## 1. Distribution channels, ranked

Scoring: effort (S/M/L), realistic reach for a new entrant, and ToS/regulatory risk.

| Rank | Channel | Effort | Reach | ToS/reg risk | Key evidence |
|---|---|---|---|---|---|
| 1 | **Own remote MCP server plus Claude Connectors Directory / ChatGPT apps (Plugin directory)**, composable with the user's own broker MCP | S–M | **M–L.** Skews to technical users on Claude Desktop/web or ChatGPT developer mode. Covers Zerodha, Upstox and Fyers users (official MCPs). **Does not cover Groww or Angel One users**: no official MCP found (community servers only for Angel One), so those users need channel 2 or 3 | **M** (data rights, see note) | Claude directory: anyone may build, but submission needs a Team/Enterprise org, OAuth 2.0, read-only/destructive annotations, a privacy policy, and seven compliance acknowledgements including "financial transactions" [F, H, claude.com/docs/connectors/building/submission]. OpenAI accepts third-party app submissions. The app directory was reportedly migrated into a "Plugin directory" on 2026-07-09 [M, openai.com/index/developers-can-now-submit-apps-to-chatgpt/ returned 403; help.openai.com/en/articles/11487775 via search]. **Data-rights note:** the "user's broker MCP brings prices, we bring evidence" split avoids displaying exchange prices *only if our server uses no prices at all*. Aligning events to a move (before, during, after) and adding sector context needs price data on our side. NSE treats that as non-display use, and publishing derived data externally needs a separate agreement and fees [F, M, NSE non-display policy]. So choose: (a) a **price-free ledger** (events and timestamps only; the host LLM aligns them with the user's broker prices, which is weaker and less reliable), or (b) a **licensed EOD or delayed feed** with derived-data rights (fees unverified; NSE PDFs timed out). |
| 2 | **Responsive web app plus email digest plus web push** (the 02 default) | M | M | Low | No gatekeeper. Needed anyway as the account, billing and archive home [I]. |
| 3 | **Telegram bot** | S | M–H in Indian trading communities | M (reputational) | Bot API has no per-message fee [A, not re-verified this session]. SEBI enforcement targets paid Telegram "tip" channels [L, univest/scoutstack blogs]. The bot must be visibly non-advisory. |
| 4 | **WhatsApp Business Platform**, as a narrow alert/digest bot only | M | H (India) | **High for chat** | Meta's Business Solution Terms bar "AI Providers" whose general-purpose AI assistant is the "primary (rather than incidental or ancillary) functionality", effective 2026-01-15 [F, H-ish: TechCrunch 2025-10-18 quoting the terms; Meta's terms page not fetched]. A market Q&A chatbot is likely to fall inside the ban. A structured "your watchlist digest" utility bot is probably allowed [I, M]. Cost in India: marketing about ₹0.86/msg, utility about ₹0.115/msg plus 18% GST plus BSP markup. Utility messages are charged inside the service window from 2026-10-01 [M, BSP blogs chatmaxima/mark360; Meta page developers.facebook.com/documentation/business-messaging/whatsapp/pricing not fetched]. |
| 5 | **Browser extension over broker web apps** (Kite, Groww) | M | M | M–H | No broker extension program found [I]. Scraping broker UIs likely breaches user agreements [A, unverified per broker]. |
| 6 | **Browser extension overlay on TradingView** | M | H (in theory) | **High** | TradingView's terms forbid automated collection ("scripts, APIs, screen scraping…") and "third-party products, tools… designed to facilitate… non-display usage", and it bans accounts for this [M, search summary of tradingview.com/policies; policy page not fetched]. TradingView ships its own free **AI Chart Copilot** Chrome extension (public beta 2026-04-02; free usage caps; Pine authoring on Essential+) [F, H, tradingview.com/blog/en/tradingview-ai-chart-copilot-beta-57730/]. |
| 7 | **TradingView Advanced Charts / broker integration** | L | n/a | Low | The free Advanced Charts licence requires a public (non-paywalled) site with visible attribution [F, M, tradingview.com/free-charting-libraries/]. The brokerage-integration program is for **brokers only** [F, H, in.tradingview.com/brokerage-integration/]. Neither is a route to TradingView users. Lightweight Charts (Apache-2.0) is the option for our own UI. |
| 8 | **Broker partnership / listing** (Kite Connect apps, Rainmatter, Groww, Angel, Upstox) | L | H if won | M–H | Kite Connect: ₹500/mo for data APIs; order and account APIs free since Mar-2025 [F, H, kite.trade forum and support.zerodha.com]. **But:** "you cannot display data from Kite Connect APIs on other platforms, as this violates the exchange's data vending policies" [F, H, support.zerodha.com …can-i-use-historical-and-live-data…]. Kite Publisher is order buttons only [F, M]. SEBI Jan-2025 circular SEBI/HO/MIRSD/MIRSD-PoD-1/P/CIR/2025/11 restricts regulated entities from associating with persons giving unregistered advice [F title/number, H; body not extracted; details M via law-firm summaries]. A broker partner will require us to be clearly non-advisory or registered. |
| 9 | **Bloomberg App Portal / ASKB** | XL | Nil for this audience | Low | The App Portal is curated with Bloomberg-selected onboarding and reaches about 350k Terminal users [F, M, 2016-era PR]. ASKB (beta 2026-02-23, mobile 2026-08) is Bloomberg's own agentic assistant over 800+ research providers [F, H, bloomberg.com press]. These are institutional buyers, not Groww or Zerodha users. |
| 10 | **Native mobile app** | L | H in theory | Low–M | Worth it only after retention is proven. Excluded in 02 §5. |

### Official broker MCP servers (the "broker-agnostic" layer already exists)

| Broker | Official MCP | Scope | Clients | Cost | Source |
|---|---|---|---|---|---|
| Zerodha | Kite MCP (hosted `mcp.kite.trade`, open-source repo) | Read-only on hosted; portfolio, P&L, positions, market data | Claude Desktop, Cursor, VS Code, Windsurf; ChatGPT "working on it" | Free | H, zerodha.com/products/mcp/ ; github.com/zerodha/kite-mcp-server |
| Upstox | Hosted `https://mcp.upstox.com/mcp`, OAuth | Strictly read-only; daily re-auth | Claude (listed in marketplace), Claude Code, ChatGPT dev mode, Cursor, VS Code | Free | H, upstox.com/developer/api-documentation/mcp-integration/ |
| Fyers | FYERS MCP, local installer, 38 tools | **Read and write** (orders, GTT, baskets, square-off) with user review | Claude Desktop/Code, Codex, Cursor, VS Code… | Free | H, fyers.in/mcp |
| Dhan | No official MCP found; community only | — | — | Trading APIs free; Data API ₹499/mo | M, dhanhq.co; dhan.co support |
| Angel One | No official MCP found; SmartAPI community MCPs | — | — | SmartAPI free [A, not verified] | L, glama/lobehub listings |
| Groww | Trade API, ₹499/mo | Orders, data | — | ₹499 plus tax per month | M, groww.in/trade-api (via search) |

**[I]** Brokers are commoditising "connect my account to AI". A third party should not compete on portfolio access. It should supply what broker MCPs lack: cited corporate-event evidence and deal intelligence.

---

## 2. Competitor table (India focus; global competitors are covered in `research/products.md`, also accessed 2026-09-24)

| Product | AI feature | Price | Strengths | Weaknesses / gaps | Source, conf. |
|---|---|---|---|---|---|
| **Dhan: Fuzz** (askfuzz.ai) | Agentic research assistant for NSE/BSE stocks, ETFs and MFs; answers **cite** filings and exchange data; "your own native Indian language"; runs on its own "artham" model on India-owned GPUs | **Free**; paid "watching the market" tier "coming soon" | The closest analogue to the owner's idea: cited, multilingual, India-hosted, and free | India only. No latency claims. Monitoring not yet shipped | H, askfuzz.ai; launch Aug-2025 per X/LinkedIn M |
| **Groww: GR 1** | Portfolio-aware assistant: reads markets, tracks news sentiment, personalised insights; cannot trade without consent | Not disclosed; opt-in beta for 30–50k users (announced 2026-02-28), wider rollout in 3–6 months | Distribution to Groww's base | Personalised, which puts it close to advice. Beta | M, analyticsindiamag; entrackr (BS returned 403) |
| **Angel One: Ask Angel**, plus "Real Time Trading Signals", ARQ Prime | In-app chat covering fundamentals, technicals, news and IPO data; ARQ Prime is a rule-based engine recommending up to 15 stocks | ARQ free ("limited time"); others not stated | Bundled with more than 35M clients [M] | Signals-heavy, which is the regulated zone | H, angelone.in/a1i1 ; ARQ M/L |
| **Zerodha** | No consumer chatbot found. Kite MCP (free, read-only). Kamath: "AI is just table stakes" (2026-08-17); imagines users building their own AI interface over broker rails | Free | Philosophically favours the "bring your own AI" model | No first-party assistant | H (MCP); M, BusinessToday 2026-08-17 |
| **Upstox / Fyers** | Official MCPs (see §1) | Free | — | — | H |
| **Trendlyne** | MarketMind AI via monthly credits (GuruQ 84, StratQ 240, PRO 120, PRO PLUS 480); bulk/block, insider/SAST deal alerts | GuruQ ₹390/mo or ₹1,890/yr (the annual price shown with promo code); StratQ ₹5,900/yr; PRO ₹1,500/mo; PRO PLUS ₹2,000/mo | Already owns **deal alerts** and has AI | Credit-limited AI; not evidence-ledger style | H, trendlyne.com/subscription/plans/ ; help.trendlyne.com |
| **Screener.in: Screener AI** | Q&A over annual reports and concall documents | Premium ₹4,999/yr includes ₹500 of AI credits; then **₹10–30 per answer (up to ₹100)**; ₹100/M input and ₹800/M output tokens | Trusted by fundamental investors; transparent pass-through pricing | Costly per answer; slow ("in seconds") | H, screener.in/ai/ ; premium price M |
| **Tickertape Pro** | No explicit AI on the pricing page; forecasts and scores | ₹399/mo; ₹899 per 3 months; ₹2,999/yr | Large base (claims "60L+") | — | H, tickertape.in/pricing |
| **StockEdge** | Stock AI (Club only); AI chart patterns (Pro/Club) | Premium ₹399/mo or ₹1,649/yr; Pro ₹1,499/mo or ₹6,594/yr; Club ₹2,499/mo or ₹13,194/yr | Scans | — | H, stockedge.com/pricing |
| **Sensibull** | Options analytics; "signals" in Pro | **Free for Zerodha users**; others: Pro reported ₹800–1,300/mo | Owns the F&O context use case | — | H for free-for-Zerodha (freshdesk); prices L |
| **Streak** | No-code algos | Free for Zerodha users (5 live, 15 virtual deployments) | — | Caps | M, z-connect and review blogs |
| **Perplexity Finance (India)** | Live BSE/NSE data, cited answers, SEBI-filing summaries, Indian concall transcripts | Free (Pro $20) | Brand, cited, free | General-purpose; no workflow | M, medianama 2025-08; TechCrunch 2025-08-18 |
| **TradingView** | AI Chart Copilot extension; AI documents; AI corporate-news summaries | Free beta with caps | Owns the chart surface | Technical-analysis-centric | H, TradingView blog |
| **Bloomberg ASKB** | Agentic Terminal assistant | Terminal subscription | Institutional depth | Not reachable by our audience | H |
| **Moneycontrol, INDmoney "Mind"** | Mind: stock and options assistant (YouTube only); Moneycontrol AI: nothing found | — | — | Unverified | L |
| Global: Robinhood Cortex ($5 Gold), Public Agents, Perplexity, Koyfin, Fiscal.ai, Benzinga | See `research/products.md` | — | — | — | H/M there |

**No competitor publishes a latency SLA** such as "300 ms". None found [F for the pages read].

---

## 3. Willingness to pay

**India retail** [F, H unless noted]:

| Price point | Products |
|---|---|
| Free | Kite, Upstox and Fyers MCP; Fuzz; ARQ; Perplexity; Chart Copilot; Sensibull and Streak for Zerodha users |
| ₹150–400/mo | Trendlyne GuruQ (₹157/mo annual with promo to ₹390/mo), Tickertape ₹250–399/mo, StockEdge Premium ₹137–399/mo, Screener ₹417/mo effective |
| ₹500–2,500/mo | Kite data API ₹500, Groww API ₹499, Dhan Data ₹499, Trendlyne PRO/PRO+ ₹742–2,000, StockEdge Pro/Club ₹550–2,499, Sensibull Pro (L) |

**Unit economics warning for 09 [E]:** Screener passes through ₹10–30 per LLM answer. At ₹399/mo that covers only about 15–40 grounded answers per user per month before margin. An unlimited-chat plan at Indian retail prices is loss-making unless answers are mostly structured or cached, or run on cheap small models.

**Global:** $5–20 retail bundles; $37–197 for active-trader speed (Benzinga); $209–299 for adviser workflow (Koyfin Advisor) [`research/products.md`, H]. H5 ($39–79/mo) does **not** carry over to Indian retail [I].

**Discrepancies resolved to primary sources:**
- Tickertape: search said ₹249; the primary page says ₹399.
- Trendlyne GuruQ: search said ₹310/mo and ₹2,090/yr; the primary page says ₹390/mo and ₹1,890/yr (promo).
- StockEdge Club: search said ₹23,989/yr; the primary page says ₹13,194/yr.

---

## 4. Differentiators tested against named incumbents

| Proposed differentiator | Incumbent already doing it | Verdict |
|---|---|---|
| Cited, evidence-first answers | Fuzz (cites filings and exchange data, free), Perplexity (cited), Screener AI | **Not a differentiator on its own.** A per-claim **timestamped ledger** (before/during/after the move) plus explicit abstention is still unclaimed by the pages read [I, M]. |
| Hindi and regional languages | Fuzz ("native Indian language"); Sarvam APIs make it cheap for anyone | **Table stakes**, not a moat. |
| F&O context | Sensibull (free for Zerodha users), Fyers MCP option chains with Greeks, Angel signals | **Crowded** and near the advice/signals line. |
| Bulk/block and insider/SAST deal intelligence | Trendlyne deal alerts and Superstar alerts (₹157–390/mo) | **Data is commoditised.** Linking deals to moves and filings with citations and timing is not advertised [I]. |
| Broker-agnostic via MCP | Brokers ship free official MCPs themselves | The **rails are free.** The opening is being the *evidence server* users add next to their broker MCP [I]. |
| About 300 ms speed | No one claims it | Only credible for structured and cached answers (§6). Not a durable moat. |
| **Audit trail for SEBI RAs** (Reg 19(vii) AI-use disclosure plus record-keeping) | Nothing found | **Candidate wedge.** Small market (reportedly about 1,400 RAs [L]) but a compliance reason to pay. Needs validation. |

---

## 5. Licensing and regulatory touchpoints (for `compliance-analyst`)

0. **Top priority: derived-data rights for the MCP evidence server.** Can we compute before/during/after alignment and sector context from NSE/BSE EOD or delayed data and publish the derived labels, not prices, to third parties? What does NSE charge for that? This decides whether channel #1 uses option (a) or (b).
1. **Exchange data.**
   - Kite Connect data cannot be displayed on other platforms [F, H].
   - NSE requires a distribution licence for passing data to third parties "in any format", with separate agreements and fees for non-display and for external redistribution of derived data [F, M, nseindia data policy and non-display policy PDFs via search].
   - NSE's domestic price file (nsearchives …/2026-03/NSE_Pricing_file_-_Domestic_clients_20260309171343.pdf) **timed out twice**, so the fees are unverified.
   - TrueData's API access needs a separate compliance review [F, H].
2. **Advice.**
   - RA Regulations 3rd Amendment (in force 2024-12-16): Reg 19(vii) requires disclosing the extent of AI-tool use; RAs are solely responsible for client-data security [F, M, law-firm summaries; primary gazette not fetched].
   - "AI-only advisory is not permissible" is **L** (vendor blog only).
   - Buy/sell "signals" to the public almost certainly need RA/IA registration [I, M].
3. **Association rule.** SEBI circular 2025/11 (29-Jan-2025) restricts brokers and other regulated entities from associating with unregistered advice-givers. It includes an education carve-out conditioned on not using the **last three months of price data** [F title, H; condition M via Business Standard / law-firm summaries]. This affects any broker partnership, and any "educational" positioning that shows live prices.
4. **Algos.** SEBI retail algo framework (Feb-2025 circular; compliance deadline 2025-10-01 after extension; Algo-ID on every algo order from 2026-04-01) [M, secondary]. Algo providers must empanel with exchanges and go through brokers. "Algos" in the owner's list = a regulated product.
5. **WhatsApp** general-purpose-AI ban (2026-01-15) [F, H-ish].
6. **TradingView** ToS on non-display use and third-party tools [M].
7. **Claude directory** "financial transactions" acknowledgement; read-only annotations [F, H].
8. **Global:** US publisher's exclusion analysis per 02 §2 still applies to the US leg.

---

## 6. About 300 ms: define before promising

**[P]** Metric: p95 **time-to-first-useful-token** measured at the client, split into two classes.
- **Structured lookups** (quote, deals table, "last 5 filings", indicator value from a cache): about 300 ms p95 is plausible from an India region.
- **Grounded synthesis** (retrieval plus LLM plus citations): target first token ≤ 1 s and full answer ≤ 3–5 s.

Consistent with 13-quick-response-system.md (Tier A p95 ≤ 1 s event-to-alert; SSE fan-out p95 ≤ 250 ms) [F, repo].

Through MCP in Claude or ChatGPT, host-model latency dominates and is outside our control [I].

---

## 7. Positioning and first-market recommendation [P]

**Do not build** a general India retail AI chat assistant covering news, sentiment, indicators, algos and advice. Account-owning brokers give it away free (Fuzz, GR 1, Ask Angel, broker MCPs, Perplexity), Indian retail pays ₹150–500/mo, LLM cost per answer eats that, and signals or algos pull us into SEBI RA and algo-provider regimes.

**If India is a must, the sharpest wedge is:**

> **"The cited evidence layer for Indian listed companies."** A remote MCP server plus web digest. For any NSE/BSE name or watchlist it returns a timestamped ledger:
> - exchange corporate announcements;
> - results and concall dates;
> - bulk/block and insider/SAST deals;
> - shareholding changes;
> - index and sector context.
>
> Each item is marked before, during or after a move, and the ledger ends with an explicit "no disclosed catalyst found" when that is the case. It is descriptive only: no calls, no signals. It is designed to sit **next to** the user's own Kite/Upstox/Fyers MCP. Move alignment requires either a licensed EOD/delayed feed with derived-data rights, or dropping alignment altogether (the price-free option). See the §1 data-rights note and compliance item 0.
>
> Groww and Angel One users are reached through the web app and Telegram digest, not through MCP.

- **Revenue ceiling [E]:** about 1,400 RAs (L) × ₹1,500–5,000/mo × 12 = **about ₹2.5–8.4 crore per year at 100% capture**. A realistic 5–15% capture gives roughly ₹0.13–1.3 crore. Independent analysts, educators and the retail/global legs have to supply the rest. This does not change the recommendation, but the owner should see the ceiling.

- **First users:** SEBI-registered RAs and independent India-market analysts, newsletter writers and educators. They must cite sources, disclose AI use (Reg 19(vii)) and keep records. Price target: ₹1,500–5,000/mo [E, unvalidated]. The retail free tier goes through the Claude/ChatGPT directory for reach.
- **Global leg:** keep 02 (US independent researchers) as is. The same ledger engine serves both.
- **First market to test:** India RAs and analysts **only if** 10–15 interviews pass the 02 H1–H3 thresholds; otherwise stay US-first per 02. This is a choice for the owner.

**Squads (from 12-team-operating-model.md):**
- product-manager runs the interviews and fake-door test.
- The **Research squad** (market-data-researcher) gets NSE/BSE EOD, derived-data, announcement and deal-file rights and quotes.
- The **Governance squad** (compliance-analyst) covers the SEBI RA/association/algo questions and the WhatsApp and TradingView terms.
- The Platform squad (data-engineer) starts only after those gates.

---

## 8. Unverified items

- NSE domestic data fees (PDF timed out); rights to redistribute NSE/BSE corporate announcements and bulk/block deal files; NSE website scraping terms.
- SEBI circular 2025/11 body text (only title and number read); RA Reg 19(vii) primary gazette; RA record-retention period; RA count (about 1,400 is L).
- Meta WhatsApp Business Solution Terms page itself; Meta India rate card (BSP figures only).
- TradingView policies page (search summary only); whether TradingView has any third-party app store (none found).
- OpenAI app/Plugin directory rules for finance apps (the primary page returned 403); whether ChatGPT app monetisation is available in India.
- Sensibull non-Zerodha prices; Angel SmartAPI pricing; Groww GR 1 pricing and GA date; INDmoney Mind; Moneycontrol AI; Fuzz paid-tier price.
- Telegram Bot API cost (assumed free, not re-fetched this session).
- Zerodha ChatGPT support status for Kite MCP (the page says "working on it"; a community fly.dev server exists and is not official).
- Bloomberg App Portal current state (sources are 2016-era).
- NSE EOD tariff PDF (timed out as well); NSE derived-data redistribution fee.
- Kavout, Benzinga AI and Public: not covered in this report (see `research/products.md` for Benzinga and Public; Kavout not covered anywhere).

## Sources (accessed 2026-09-24)
- https://zerodha.com/products/mcp/ ; https://github.com/zerodha/kite-mcp-server ; https://zerodha.com/z-connect/featured/connect-your-zerodha-account-to-ai-assistants-with-kite-mcp
- https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/can-i-use-historical-and-live-data-taken-from-kite-connect-api-on-other-platforms
- https://kite.trade/forum/discussion/15015/revising-kite-connect-fees-from-2000-to-500-per-month ; https://kite.trade/publisher/
- https://upstox.com/developer/api-documentation/mcp-integration/
- https://fyers.in/mcp
- https://dhan.co/ai-info/ ; https://askfuzz.ai/ ; https://dhanhq.co/trading-apis ; https://dhan.co/support/platforms/dhanhq-api/how-does-the-dhanhq-data-api-subscription-work/
- https://groww.in/trade-api ; https://analyticsindiamag.com/ai-news/groww-unveils-ai-assistant-for-investing-expands-bonds-and-trading-tools ; https://entrackr.com/news/groww-showcases-ai-powered-investing-tools-at-groww-next-2026-11168623
- https://www.angelone.in/a1i1 ; https://www.investorgain.com/article/angel-one-arq-prime-review/162/
- https://www.businesstoday.in/technology/artificial-intelligence/story/ai-is-no-longer-a-startup-pitch-differentiator-says-zerodha-ceo-nithin-kamath-549595-2026-08-17
- https://trendlyne.com/subscription/plans/ ; https://help.trendlyne.com/support/solutions/articles/84000374336
- https://www.screener.in/ai/ ; https://www.screener.in/premium/
- https://www.tickertape.in/pricing ; https://stockedge.com/pricing ; https://sensibull.freshdesk.com/support/solutions/articles/43000586718
- https://zerodha.com/z-connect/streak/streak-is-now-available-for-all-zerodha-users-at-no-cost
- https://www.medianama.com/2025/08/223-perplexity-launches-bse-nse-tracking-tool-india/ ; https://techcrunch.com/2025/08/18/perplexity-now-supports-live-earnings-call-transcripts-for-indian-stocks/
- https://www.tradingview.com/blog/en/tradingview-ai-chart-copilot-beta-57730/ ; https://www.tradingview.com/free-charting-libraries/ ; https://in.tradingview.com/brokerage-integration/ ; https://www.tradingview.com/policies/
- https://www.bloomberg.com/company/press/meet-askb-first-look-at-future-of-the-bloomberg-terminal-in-the-age-of-agentic-ai/ ; https://www.bloomberg.com/company/press/bloomberg-launches-enterprise-app-portal-to-financial-markets/
- https://techcrunch.com/2025/10/18/whatssapp-changes-its-terms-to-bar-general-purpose-chatbots-from-its-platform/ ; https://chatmaxima.com/whatsapp-api-pricing/india/ ; https://mark360.ai/blog/whatsapp-service-message-pricing-october-1-2026
- https://claude.com/docs/connectors/building/submission ; https://help.openai.com/en/articles/11487775-apps-in-chatgpt
- https://www.sebi.gov.in/legal/circulars/jan-2025/details-clarifications-on-provisions-related-to-association-of-persons-regulated-by-the-board-miis-and-their-agents-with-persons-engaged-in-prohibited-activities_91356.html
- https://www.scconline.com/blog/post/2024/12/19/sebi-research-analyst-third-amendment-regulations-2024/
- https://www.nseindia.com/static/market-data/nse-data-policy ; https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Non_Display_Policy.pdf ; https://www.truedata.in/price
- https://www.sarvam.ai/api-pricing
