# Competitive Research: Product Direction for an LLM Stock "Why Did X Move?" Tool

Research date / access date for every source below: **2026-09-24**. Prices are in USD unless stated otherwise, and they are list prices as displayed on that date. Promotions are noted where they appeared.

**Confidence rubric**
- **H** (High): a primary page (vendor, regulator or official repo) was fetched and read.
- **M** (Medium): two or more independent secondary sources agree.
- **L** (Low): a single secondary source, or sources that conflict. Every L item is repeated in the "Could not verify" section.

Citations use the form [S#, conf]. The full source list is at the bottom.

---

## 0. TL;DR

- **Explaining why a stock moved is now commoditized for mainstream retail.** Robinhood Cortex Digests cost $5/mo inside Gold [S14, S15, H]. Schwab Portfolio Insights is free to all self-directed US retail clients [S17, H]. Perplexity Finance has price and movement alerts that run an AI query and push the result [S19, H], and its answers cite sources [S20, H]. Snowball Analytics bundles a "Why is it moving" feature at $14.99/mo [S24, H]. Benzinga sells WIIM wholesale to platforms, including Stocks.News (June 2026) and Public.com [S8, H; S9, M].
- **What is still underserved:**
  - Evidence you can audit and export, with a full ledger of sources, timestamps and confidence.
  - An honest "no clear catalyst found" answer.
  - Coverage of small and mid caps, which Robinhood's Digests exclude [S15, H].
  - Workflows for many watchlists or clients: newsletter writers, independent RIAs, small funds.
  - An archive of past explanations that users can search and share.
- **Recommendation:** direction **(b) monitoring with explainable alerts**, repositioned for **pro-am users, newsletter writers and small RIAs**. The research layer (a) should be a supporting feature. De-prioritize (c), (d) and (e); section 8 gives the reasons.

---

## 1. Direction (a): Research & screening

| Product | What it does / target user | Price (verified) | Real-time data | AI features | Weaknesses / gaps |
|---|---|---|---|---|---|
| **Koyfin** | Terminal-style research, dashboards, screeners. Serves retail through advisors. | Free; Plus $39/mo; Premium $79/mo; Advisor Core $209/mo; Advisor Pro $299/mo (monthly billing; up to 30% off annually) [S1, H] | Pricing page gives no real-time detail [S1, H] | AI transcript/earnings summaries [S36, L] | Pricing page lists no alerting or AI tier. Built for research, not for monitoring events as they happen. |
| **Finviz Elite** | Screener, charts, heatmaps. Active retail. | $39.50/mo or $299.96/yr [S3, H] | Real-time including pre/post market; US only [S3, H] | None listed on the Elite page [S3, H] | Alerts are price/news triggers with no explanation. US only. |
| **Seeking Alpha Premium** | Crowd-sourced analysis, Quant Ratings. Retail. | Premium $299/yr [S5, H]; Alpha Picks $499/yr; Pro about $2,400/yr [S6, M] | Not a real-time data product | Virtual Analyst Reports on about 3,000 stocks [S7, M]; "Ask Seeking Alpha" chat [S7b, M] | Opinion-heavy. AI covers only quant-rated stocks. Not built for intraday moves. |
| **Fiscal.ai** (formerly FinChat) | Fundamentals terminal with AI Copilot, plus an MCP server and API. Retail and pro-am. | Pricing page shows the Terminal/MCP/API split and a 7-day trial but no numbers [S10, H]. Secondary sources: Pro $39/mo annual ($49 monthly), Max $79/mo annual; one source says Enterprise $199/mo [S11, L, conflicting] | Not a real-time focus | Copilot over filings, KPIs and segments; MCP server for your own AI tools [S10, H] | Fundamentals-first. Weak on intraday "why". |
| **Perplexity Finance** | Free finance hub: answer engine, Earnings Hub, screener, Plaid portfolio. Everyone. | Hub is free; Pro $20/mo [S21, M] | Quotes, charts, live earnings-call synthesis [S19, H] | Cited answers over SEC/EDGAR [S20, H]; price/move alerts that run a query and push the result [S19, H]; free Morningstar reports [S19, H] | General-purpose. No audit or export workflow. Evidence quality varies by query. |
| **Yahoo Finance Plus** | Portfolio tools, research, screeners. Mass retail. | Annual billing only on the fetched page: Bronze $95.40/yr, Silver $239.40/yr, Gold $479.40/yr (about $7.95, $19.95 and $39.95 per month). Month-to-month prices were not shown [S12, H] | Not specified | None listed on the plan page [S12, H] | Generic. AI is not part of the paid tiers. |
| **Morningstar Investor** | Ratings, fair value, moat, portfolio X-ray. Long-term retail. | $249/yr ($199 first year) [S13, M] | No | AI assistant "Mo" and AI news summaries [S13, L] | Long-horizon. Not event-driven. |
| **AInvest (Aime)** | Chat-first AI stock assistant app. Retail. | AIME+ Pro $34.99/mo or $299.99/yr (app store listing) [S30, L] | Real-time quotes on the free tier [S30, L] | Chat Q&A, news summaries, "trade ideas" [S30, L] | Generic AI assistant. Consumer-focused. Not verifiable on a primary page. |
| **OSS: OpenBB (ODP)** | Open Data Platform: data connectors feeding Python, REST, MCP and Workspace. | Open source. Workspace has a free tier (20 Copilot queries/day) and enterprise quotes [S33, M] | Depends on connected providers | Workspace Copilot/agents | **AGPL-3.0** (confirmed in LICENSE) [S31, H]. Hosting a modified closed service triggers the source-disclosure obligation. |
| **OSS: FinGPT / FinRobot** | Research LLM frameworks. | MIT / Apache-2.0 [S32, H] | n/a | Sentiment, report generation | Research-grade, not a product. |

## 2. Direction (b): Market monitoring and explainable alerts ("why is my watchlist stock moving")

| Product | What it does / target user | Price | Real-time data | AI / "why" features | Weaknesses / gaps |
|---|---|---|---|---|---|
| **Benzinga Pro** | Fast newsfeed, squawk, scanners. Active traders. | Basic $37/mo; Streamlined $147/mo; Essential $197/mo. Annual equivalents $30.58, $124.75 and $166.42 per month [S4, H; page dated 2025-10-07] | Nasdaq Basic real-time [S4, H] | "Benzinga AI" on Essential [S4, H]. WIIM gives a one-line catalyst per move with volume context [S8b, M]. WIIM is sold as an API: Stocks.News (2026-06-11) [S8, H]; Public.com [S9, M] | Expensive. WIIM is a single line with little visible evidence chain. News-speed product, not an audit trail. |
| **TradingView alerts** | Charting plus alerts. Mass active retail. | Monthly price billed annually: Essential $12.95, Plus $29.95, Premium $59.95, Ultimate $199.95 (shown as "special price") [S2, H]. Monthly-billed prices: Essential $14.95, Plus $34.95, Premium $69.95, Ultimate $239.95 (derived from the "Save $24/$60/$120/$480 a year" figures on S2, H; they match S2b) | Exchange data bought per market [S2, H] | Alert caps: price/technical alerts 20, 100, 400 and 1,000 by tier. **Watchlist alerts: 0, 0, 2 and 15** [S2, H]. AI screener quotas [S2, H] | Alerts trigger on price or technicals only, with no explanation. Watchlist alerts are scarce and gated to Premium and above. |
| **Unusual Whales** | Options flow, dark pool, congressional trades. Options traders. | Retail Basic $50/mo ($42/mo annual); Pro $75 ($63); Max $120 ($102) [S16, H] | Real-time on paid tiers; free tier delays flow by 2 days and news by 15 min [S16, H] | "Mr. Whale" AI analyst and trade finder, usage-tiered [S16, H] | Niche: flow-centric. Explanations are about positioning, not news. |
| **Stocktwits Edge** | Social sentiment. Retail traders. | $229.50/yr (was $274.50) [S18, H]; $22.95/mo [S18b, L] | Sentiment in real time | AI summaries of chatter [S18b, L] | Sentiment is not evidence. Noisy. |
| **Robinhood Cortex Digests / Legend** | Broker AI: "what may be driving a stock's price", plus Portfolio Digests. | Inside Robinhood Gold, $5/mo or $50/yr [S14, H]. Cortex Digests are on Legend (desktop) for Gold [S14b, L] | Gold includes Nasdaq Level 2 [S14c, M] | Summarizes news, analyst reports, technicals and proprietary data [S15, H]. Portfolio Digests refresh several times a day [S14, H] | **Popular stocks only**; unavailable during corporate actions [S15, H]. Locked to the Robinhood account. |
| **Schwab Portfolio Insights** | AI summaries of the 5 biggest-moving holdings plus news and Schwab research. | Free; rolled out to all self-directed US retail clients by end of May 2026 [S17, H; released 2026-05-05] | Schwab data | Generative summaries | No per-insight citations described. Schwab's own disclaimer says output "may be inaccurate…hallucinated" [S17, H]. Only 5 holdings. |
| **Public.com** | Agentic brokerage. AI Agents that monitor conditions and execute trades (rollout from 2026-03-31) [S22, H]. Also Alpha, Market Briefing, earnings summaries [S22b, L] | Agent pricing not disclosed [S22, H] | Broker data plus Benzinga WIIM [S9, M] | Agents, Alpha | Tied to the broker account. |
| **Perplexity Finance** | See (a). Watchlist AI briefing [S21, M]. Price/move alerts that run a query and push the result [S19, H] | Free / Pro $20 | Yes | Cited answers [S20, H] | Closest free substitute. No audit ledger and no multi-client workflow. |
| **Snowball Analytics** | Dividend/portfolio tracker with a "Why is it moving" feature on the Investor plan; also offers an MCP server | Investor $14.99/mo or $104.99/yr [S24, H] | n/a | "Why is it moving" [S24, H] | Shows the feature is sold as a bundle add-on at a low price. |

## 3. Direction (c): Portfolio / exposure / risk analysis

| Product | What / who | Price | AI | Gaps |
|---|---|---|---|---|
| **Portfolio Visualizer** | Backtests, Monte Carlo, optimization, factor regression. DIY investors and advisors | Free; Basic $30/mo (annual); Pro $55/mo (annual, commercial use) [S23, H] | None | Old-style UI. No news or events layer. |
| **Sharesight** | Performance, dividend and tax tracking. Retail, especially AU/NZ/UK | Free; Starter $7/mo annual ($9.33 monthly); Standard $18 ($24); Premium $23.25 ($31) [S25, H] | None listed; offers price and portfolio email alerts [S25, H] | No explanations of moves. |
| **Snowball Analytics** | Tracker, dividends, rebalancing, backtests | Starter $55.99/yr; Investor $104.99/yr; Expert $174.99/yr (30%-off promotion was on) [S24, H] | "Why is it moving"; MCP [S24, H] | Retail-only. |
| **Koyfin Advisor** | Model portfolios, client reports, custodian integrations | $209–$299/mo [S1, H] | Limited | Research-first. |
| **Yahoo Finance Plus Bronze** | Portfolio risk and volatility | $95.40/yr [S12, H] | None | Basic. |
| **OSS: Ghostfolio** | Self-hosted wealth tracker | Hosted Premium about $48/yr [S26, L]. **AGPL-3.0** [S32, H] | n/a | AGPL network clause. |
| **OSS: Riskfolio-Lib / QuantStats** | Portfolio optimization / performance tearsheets | BSD-3 / Apache-2.0 [S32, H] | n/a | Libraries, not products. |

## 4. Direction (d): Strategy research and backtesting

| Product | What / who | Price | AI | Gaps |
|---|---|---|---|---|
| **QuantConnect** (LEAN cloud) | Cloud backtest, research and live trading. Quants and small funds | Free tier. Researcher, Team, Trading Firm and Institution tiers; the pricing page lists features but no numbers [S27, H]. Secondary: Researcher about $60/mo, modular nodes starting around $24/mo [S28, L, conflicting] | "Mia" AI assistant [S27, H] | Steep learning curve. |
| **TrendSpider** | Automated technical analysis, backtests, bots. Active technical traders | Four tiers; the page mixed promo prices (up to 50% off through 09/28) [S29, H]. Alert caps: 10, 50, 100 and 400 active alerts [S29, H] | **Sidekick AI is sold separately:** 25 free messages/mo, then $49, $129 or $349 per month [S29, H] | Technical-only. |
| **Composer** | No-code strategies with AI; executes through its own brokerage | Free; Advanced $10/mo; Pro $32/mo or $384/yr [S34, H] | "Trade with AI" [S34, H] | Executes trades itself, so it sits in the regulated broker/adviser space. |
| **Portfolio Visualizer** | Asset-allocation backtests | See (c) | None | Not stock-level. |
| **OSS: LEAN** | Engine behind QuantConnect | Apache-2.0, active (pushed 2026-09-23) [S32, H] | n/a | n/a |
| **OSS: NautilusTrader** | High-performance event-driven engine | **LGPL-3.0**, active [S32, H] | n/a | n/a |
| **OSS: vectorbt** | Vectorized backtesting | **Apache 2.0 with Commons Clause**: you may not sell a product whose value derives "entirely or substantially" from it [S31b, H]. vectorbt.pro is not a public repo (404) | n/a | Blocks commercial use if the product depends on it. |
| **OSS: zipline-reloaded** | Maintained Zipline fork | Apache-2.0; last release 3.1.1 on 2025-07-23 [S32, H] | n/a | Slow cadence. |
| **OSS: backtrader** | Classic event-driven library | GPL-3.0; **last commit 2023-04-19; treat as dormant** [S32, H] | n/a | Unmaintained. |
| **OSS: ai-hedge-fund / TradingAgents** | Multi-agent LLM "analyst teams" | MIT / Apache-2.0. About 63.7k and 108k GitHub stars (per GitHub API, 2026-09-24) [S32, H] | Core function | Demos with no evidence of edge. Huge free mindshare. |

## 5. Direction (e): Paper trading and broker-connected workflows

| Product | What / who | Price | AI | Gaps |
|---|---|---|---|---|
| **Public.com Agents** | Natural-language agents that monitor conditions and execute trades (covered calls, cash sweeps) [S22, H] | Not disclosed | Core function | The broker owns this workflow. |
| **Robinhood Cortex** | Assistant that can research and buy/sell [S14, H] | Gold $5/mo | Core function | Same as above. |
| **Composer** | Automated strategies | $0 / $10 / $32 per month [S34, H] | Trade with AI | n/a |
| **Alpaca** (infrastructure) | Commission-free API broker. Free paper trading [S35, M] | Basic data free (IEX only); Algo Trader Plus $99/mo for full SIP plus OPRA [S35, M] | n/a | Personal-use data costs $99/mo per user. Licensing to redistribute data in a hosted product is separate and has not been quoted. |
| **QuantConnect** | Paper and live trading through IB, Schwab, tastytrade, Alpaca and others [S27, H] | See (d) | Mia | n/a |

---

## 6. Willingness-to-pay evidence (alerting, news and AI)

| Price point | Product | What is paid for | Source |
|---|---|---|---|
| $5/mo | Robinhood Gold (includes Cortex Digests) | Broker bundle | S14, H |
| about $8–13/mo (annual) | Yahoo Bronze; TradingView Essential | Tracking; 20 alerts | S12, S2, H |
| $14.99/mo | Snowball Investor (includes "Why is it moving") | Tracker plus "why" | S24, H |
| $20/mo | Perplexity Pro (the finance hub itself is free) | General AI | S21, M |
| about $25/mo equivalent ($299/yr) | Seeking Alpha Premium $299/yr; Finviz Elite $299.96/yr ($39.50 monthly) | Research; real-time screener with unlimited alerts | S5, S3, H |
| $37/mo | Benzinga Pro Basic (real-time news, watchlist alerts) | News speed | S4, H |
| $42–120/mo | Unusual Whales | Flow data with an AI analyst | S16, H |
| $49–349/mo **on top of** the base plan | TrendSpider Sidekick AI | Separately metered AI usage | S29, H |
| $147–197/mo | Benzinga Streamlined/Essential | Squawk, scanner, AI | S4, H |
| $209–299/mo | Koyfin Advisor | RIA workflows: client reports, custodians | S1, H |

**Takeaways**
- For **mass retail**, the ceiling for monitoring and "why" features is about **$5–15/mo**, and those features come bundled or free (Robinhood, Schwab, Perplexity, Snowball).
- **Active traders** pay **$37–197/mo**, but for speed (Benzinga) and proprietary data (Unusual Whales), not for LLM prose.
- **Pro-am and RIA users** pay **$200–300/mo** for workflows: client reporting, integrations and compliance-friendly output (Koyfin Advisor).
- TrendSpider meters AI usage separately at up to $349/mo. That shows heavy users will pay for AI capacity layered on a tool they already use.

## 7. Where "explainable, evidence-cited move alerts" are commoditized and where they are underserved

**Commoditized**
- A single-ticker, popular-stock "why is it moving" summary. It is free or near-free at Robinhood (popular stocks only), Schwab (5 holdings), Perplexity (cited, alert-triggered), Snowball ($14.99) and Public (via Benzinga WIIM) [S14, S15, S17, S19, S24, S9].
- Benzinga's WIIM licensing lead is explicitly selling it as "the data backbone" for platforms [S8, H]. Any fintech can buy the explanation layer.

**Underserved (the opportunity)**
1. **An evidence ledger, not just prose.** For each claim, show the source URL, publish timestamp relative to the price move, and the type of source (filing, press release, analyst action, news). Schwab describes no per-insight citations and warns about hallucination [S17]. WIIM is one line [S8b].
2. **Calibrated confidence and "no identifiable catalyst."** Include sector or index beta decomposition, so the product can say "moved with the semis ETF; no stock-specific news." No product surveyed advertises this. (It is an inference from the feature lists; confidence M.)
3. **Long-tail coverage.** Robinhood restricts Digests to popular stocks [S15].
4. **Multi-watchlist and multi-client workflows**, plus export to a newsletter or client note with citations and an archive. TradingView gates watchlist alerts to 2–15 [S2]. The RIA price point exists at Koyfin Advisor [S1].
5. **Not locked to a broker.** Broker AI only covers holdings at that broker.

**Do free broker AI summaries undermine a standalone product?** For mainstream retail users who hold popular stocks at Robinhood or Schwab, **yes**: the "why" is now a free or $5 feature inside the app they already open. They do **not** cover cross-broker, auditable, exportable, long-tail and multi-client use cases, and brokers have little incentive to build for newsletter writers or RIAs (Schwab's tool is for its own retail clients). A standalone product should therefore not sell "AI explains the move" as the product. It should sell **trustworthy, auditable monitoring for people who publish or advise**.

## 8. Main failure modes by direction

| Direction | Main reasons it could fail |
|---|---|
| (a) Research & screening | Crowded with deep incumbents (Koyfin, Fiscal.ai, Seeking Alpha, Morningstar) and free Perplexity. Fundamentals data licensing is expensive. The product has no distinct edge. |
| (b) Monitoring & explainable alerts | Commoditized for retail (section 7). Real-time data and news licensing: Alpaca SIP costs $99/mo per user for personal use only [S35], and redistribution licensing for a hosted product is separate and has not been quoted. Alert fatigue. Hallucination liability. Latency versus Benzinga. **Mitigation:** target pro-am users; use delayed or end-of-day plus event-driven checks; free sources (SEC EDGAR filings, company press releases). |
| (c) Portfolio / risk | Cheap trackers ($7–25/mo: Sharesight, Snowball, Yahoo) and free Portfolio Visualizer. Aggregation (Plaid/brokerage linking) is costly. Portfolio-specific "what to do" output moves toward **personalized advice** (Advisers Act). |
| (d) Backtesting | Free, mature open source (LEAN, NautilusTrader), QuantConnect's free tier, and viral LLM agent repos. **vectorbt's Commons Clause** limits commercial reliance. Users churn after one backtest. Overfitting and promotion of backtested performance invite regulatory and marketing scrutiny. |
| (e) Paper trading / broker | Brokers already ship agentic trading (Public Agents, Robinhood Cortex). Order routing requires broker-dealer or adviser status or a partner. Highest regulatory and security exposure. |

## 9. Regulatory product-design risk (US)

| Point | Implication for design | Source |
|---|---|---|
| Advisers Act §202(a)(11)(D) excludes publishers of any "bona fide … financial publication of general and regular circulation". *Lowe v. SEC*, 472 U.S. 181 (1985): impersonal newsletters with specific buy/sell commentary are excluded, provided they do not offer individualized advice tailored to a specific portfolio or client. | Keep output impersonal: the same explanation for everyone who watches ticker X, and no "you should sell given your portfolio." | S37, H (official US Reports PDF) |
| *Seeking Alpha* class action, **S.D.N.Y., Aug 2024 (private suit, not an SEC action)**. The court held Seeking Alpha fits the publisher's exclusion. Real-time or breaking publication does not defeat "general and regular circulation." Portfolio-linked email alerts and filtering of generally available content were not personalized advice. | Watchlist-filtered alerts over generally available content are **supportive, not dispositive** (one district court). | S38, M (law-firm summaries: Katten, Greenberg Traurig) |
| **Open question:** whether on-demand, per-query LLM answers count as a "publication of general and regular circulation" is unsettled. No SEC guidance was found. | Treat it as an open risk. Prefer generating one canonical explanation per ticker-event, published to all subscribers, rather than bespoke advice per user. Get counsel review. | Inference, M |
| SEC "AI-washing" enforcement (Delphia, Global Predictions), **2024-03-18**, $400k total penalties for false AI claims. | Marketing claims about the AI (accuracy, "AI adviser") must be true and substantiated. | S39, H |
| SEC withdrew the Predictive Data Analytics conflicts proposal on **2025-06-12**. | No PDA-specific rule is pending. General anti-fraud and fiduciary duties still apply. | S40, H |
| FINRA Rule 2210 and Regulatory Notice 24-09 (2024-06-27): communications rules apply to AI-generated content. The 2026 Oversight Report adds supervision and recordkeeping expectations for GenAI and agents. | These bind **FINRA member broker-dealers**, not a standalone publisher. They matter if you white-label to or partner with a broker, which would then need to supervise your output. | S41, S42, H |
| Directions (c) and (e): portfolio-tailored recommendations or trading on a user's behalf cross the personalization line and likely require RIA or broker-dealer status or a regulated partner. | Strongest regulatory argument against (c) with recommendations, and against (e). | Inference from S37, M |

---

## 10. Ranked recommendation

1. **(b) Explainable monitoring, repositioned for pro-am users, newsletter writers and small RIAs.** *Best fit.*
   - **Why:** it extends the existing code (quote plus news plus period change plus LLM) directly.
   - **Evidence that the gap is real:**
     - Price levels already paid: $37–197/mo for Benzinga Pro, $209–299/mo for Koyfin Advisor [S4, S1].
     - The explanation layer is sold as a wholesale feed (WIIM), so there is a market for it [S8].
     - Incumbents show clear gaps: Robinhood covers popular stocks only, Schwab covers 5 holdings with no citations described, and TradingView watchlist alerts are scarce [S15, S17, S2].
   - **Differentiators to build:**
     - A per-claim citation ledger with timestamps before and after the move.
     - Market and sector beta decomposition, including "no stock-specific catalyst."
     - Coverage of small and mid caps from SEC EDGAR 8-K/Form 4 and press releases.
     - A digest you can export or share, plus a searchable archive.
     - Impersonal, publisher-style output.
   - **Do not compete on:** news latency, or the mass-retail "why" feature.
2. **(a) Research as a supporting layer.** Let users ask follow-up questions over the cited event archive. On its own it is too crowded (Koyfin, Fiscal.ai, Perplexity for free).
3. **(c) Portfolio exposure analysis.** Only as impersonal exposure views, e.g. "your watchlist is 40% semis", paired with (b). Standalone trackers are cheap and linking accounts is costly. Recommendations become personalized advice.
4. **(d) Backtesting.** Free open source dominates. The license traps are vectorbt's Commons Clause and backtrader being dormant. There is little reason to pay.
5. **(e) Paper trading / broker-connected.** Brokers own it (Public Agents, Robinhood Cortex). It carries the highest regulatory burden. At most, add a free Alpaca paper-trading integration as a demo, not a business.

**Condition that would change the ranking:** Perplexity's free alert-plus-cited-query feature [S19] is the closest substitute. If it adds multi-watchlist digests, exports and an audit trail, the pro-am wedge in (b) narrows substantially. Re-check quarterly.

---

## 11. Could not verify / low confidence

- **Fiscal.ai:** exact plan prices. The primary page shows no numbers, and secondary sources conflict ($39/$79 vs $199 Enterprise).
- **QuantConnect:** tier prices. The primary page shows no numbers, and secondary sources conflict ($60 Researcher vs a modular $10 seat plus nodes).
- **TrendSpider:** base list prices. The page displayed only promo-adjusted figures. The Sidekick AI add-on and alert caps are verified.
- **Morningstar Investor:** the price ($249/yr) and the "Mo" AI assistant. Primary page returned nothing.
- **AInvest:** prices (app-store figures via secondary sources only).
- **Stocktwits Edge:** monthly price and AI summaries. Only the annual price was verified.
- **Ghostfolio Premium:** about $48/yr.
- **Public.com:** its "Alpha" feature details and pricing. The Benzinga WIIM integration is corroborated only by a Benzinga page that returned 403 (headline seen in search) and secondary mentions.
- **Koyfin AI:** feature scope.
- **Seeking Alpha:** "Ask Seeking Alpha" launch date.
- **Unusual Whales:** API pricing.
- **Robinhood Legend:** whether Cortex Digests on Legend are Gold-only. This comes from a single Robinhood X post seen in search; the post itself was not fetched.
- **Data redistribution:** licensing cost for a hosted real-time product (see below).
- **Perplexity:** whether watchlist AI briefings are pushed unprompted (the secondary source says yes) and whether alert notifications include source links. The changelog confirms alerts run a query and push, and the SEC blog confirms answers cite sources.
- **Benzinga WIIM:** how it is generated (human vs AI). Benzinga's API page returned 403.
- **Data costs:** exchange redistribution and display-fee costs for a hosted real-time product were not researched. Get quotes from Polygon/Massive, Nasdaq Basic and similar vendors.
- **Legal:** no SEC staff guidance on LLM chat outputs under the publisher's exclusion was found.

---

## Sources (all accessed 2026-09-24)

- S1 Koyfin pricing: https://www.koyfin.com/pricing/ (pub. n/a) H
- S2 TradingView pricing (USD): https://www.tradingview.com/pricing/?currency=USD (pub. n/a) H. The INR version was also fetched from https://www.tradingview.com/pricing/ for alert caps.
- S2b TradingView secondary: https://www.stockbrokers.com/review/tools/tradingview ; https://fillbench.com/tradingview-plans/ M/L
- S3 Finviz Elite: https://finviz.com/elite.ashx H
- S4 Benzinga Pro pricing: https://www.benzinga.com/pro/pricing (Exa metadata pub. 2025-10-07) H
- S5 Seeking Alpha price update: https://about.seekingalpha.com/premium-subscription-price-update H
- S6 Seeking Alpha plans secondary: https://www.matchmybroker.com/articles/seeking-alpha-subscriptions-compared ; https://www.stockbrokers.com/review/tools/seeking-alpha M
- S7 Seeking Alpha Virtual Analyst Report: https://help.seekingalpha.com/what-is-the-virtual-analyst-report ; https://www.prnewswire.com/news-releases/seeking-alpha-launches-virtual-analyst-reports-its-first-ai-powered-tool-for-smarter-investment-research-302327635.html (search snippet) M
- S7b Ask Seeking Alpha: https://seekingalpha.com/article/4829617-introducing-the-cutting-edge-research-analyst-ask-seeking-alpha (search snippet) M
- S8 Stocks.News adds Benzinga WIIM (PR Newswire): https://finance.yahoo.com/markets/stocks/articles/stocks-news-adds-benzingas-why-110000495.html (pub. 2026-06-11) H
- S8b Benzinga WIIM explainer: https://www.benzinga.com/pro/blog/why-is-a-stock-moving-how-to-find-the-real-answer (search snippet) M
- S9 Public.com WIIM integration: https://benzinga.com/advertising/client-spotlight-public-coms-integration-of-the-benzinga-why-is-it-moving-wiim-api (403; title only) M/L
- S10 Fiscal.ai pricing: https://fiscal.ai/pricing H (no numbers)
- S11 Fiscal.ai secondary: https://www.matchmybroker.com/tools/fiscal-ai-review ; https://quantbrainai.net/blog/fiscal-ai-review-jul-2026/ L
- S12 Yahoo Finance plans: https://finance.yahoo.com/about/plans/select-plan H
- S13 Morningstar Investor secondary: https://traderhq.com/morningstar-investor-review-full-analysis-benefits-tools/ ; https://www.matchmybroker.com/tools/morningstar-investor-review M/L
- S14 Robinhood YES/NO event: https://robinhood.com/us/en/newsroom/robinhood-presents-yes-no-event/ (pub. 2025-12-16) H
- S14b Robinhood X post on Cortex on Legend: https://x.com/RobinhoodApp/status/2031731957252448633 (search snippet) L
- S14c Gold includes Cortex and Level 2: https://www.finder.com/investments/is-robinhood-gold-worth-it M
- S15 Robinhood Cortex Digests support: https://www.robinhood.com/gb/en/support/articles/cortex-digests (pub. 2025-03-27) H
- S16 Unusual Whales pricing: https://unusualwhales.com/pricing H
- S17 Schwab Portfolio Insights press release: https://pressroom.aboutschwab.com/press-releases/press-release/2026/Charles-Schwab-Launches-AI-Powered-Capability-That-Helps-Investors-Understand-Portfolio-Performance-and-Market-Activity/default.aspx (pub. 2026-05-05) H
- S18 Stocktwits subscriptions: https://stocktwits.com/subscriptions H (annual only)
- S18b Stocktwits secondary: https://www.findmymoat.com/tools/stocktwits L
- S19 Perplexity changelog (price alerts, Earnings hub, Morningstar): https://www.perplexity.ai/changelog/what-we-shipped-july-18th (July 18; year inferred as 2025, not shown on the page) H
- S20 Perplexity "Answers for every investor": https://www.perplexity.ai/hub/blog/answers-for-every-investor (pub. 2025-06-05) H
- S21 Perplexity Finance secondary: https://helmterminal.dev/blog/perplexity-stock-research ; https://sidsaladi.substack.com/p/perplexity-finance-101-2026-the-complete M
- S22 Public AI Agents PR: https://finance.yahoo.com/markets/options/articles/public-becomes-first-brokerage-introduce-100000348.html (pub. 2026-03-31) H
- S22b Public AI features secondary: https://www.stork.ai/en/public-com L
- S23 Portfolio Visualizer pricing: https://www.portfoliovisualizer.com/pricing H
- S24 Snowball Analytics pricing: https://snowball-analytics.com/pricing H
- S25 Sharesight pricing: https://www.sharesight.com/pricing/ H
- S26 Ghostfolio pricing: https://ghostfol.io/en/pricing (search snippet) L
- S27 QuantConnect pricing: https://www.quantconnect.com/pricing/ H (features only)
- S28 QuantConnect secondary: https://www.newtrading.io/quantconnect-review/ ; https://www.luxalgo.com/blog/quantconnect-review-best-platform-for-algo-trading-2/ L
- S29 TrendSpider pricing: https://trendspider.com/pricing/ H (promo in effect)
- S30 AInvest: https://apps.apple.com/app/id1539653456 ; https://www.stork.ai/en/ainvest L
- S31 OpenBB LICENSE (AGPL-3.0): https://raw.githubusercontent.com/OpenBB-finance/OpenBB/develop/LICENSE H
- S31b vectorbt LICENSE (Apache 2.0 with Commons Clause): https://raw.githubusercontent.com/polakowo/vectorbt/master/LICENSE.md H
- S32 GitHub API repo metadata (licenses, stars, last push, releases; queried 2026-09-24): https://api.github.com/repos/{OpenBB-finance/OpenBB, AI4Finance-Foundation/FinGPT, TauricResearch/TradingAgents, AI4Finance-Foundation/FinRobot, virattt/ai-hedge-fund, ghostfolio/ghostfolio, dcajasn/Riskfolio-Lib, ranaroussi/quantstats, polakowo/vectorbt, nautechsystems/nautilus_trader, QuantConnect/Lean, stefan-jansen/zipline-reloaded, mementum/backtrader} H. Stars: OpenBB 73.4k; TradingAgents 108.4k (Apache-2.0); ai-hedge-fund 63.7k (MIT); FinGPT 21.3k (MIT); FinRobot 8.1k (Apache-2.0); Ghostfolio 9.3k (AGPL-3.0); Riskfolio-Lib 4.5k (BSD-3); QuantStats 7.7k (Apache-2.0, last push 2026-07-20); vectorbt 9.2k; NautilusTrader 29.3k (LGPL-3.0); LEAN 21.8k (Apache-2.0); zipline-reloaded 1.9k (Apache-2.0); backtrader 23.3k (GPL-3.0, last commit 2023-04-19).
- S33 OpenBB pricing/ODP: https://openbb.co/pricing/ ; https://openbb.co/products/odp/ (search snippets) M
- S34 Composer pricing: https://www.composer.trade/pricing H
- S35 Alpaca data and paper trading: https://docs.alpaca.markets/us/docs/about-market-data-api ; https://docs.alpaca.markets/us/docs/paper-trading (search snippets) M
- S36 Koyfin AI transcripts: https://www.koyfin.com/blog/top-earnings-call-transcripts-platforms/ (search snippet) L
- S37 Lowe v. SEC, 472 U.S. 181 (1985), official US Reports: https://www.govinfo.gov/content/pkg/USREPORTS-472/pdf/USREPORTS-472-181.pdf (decided 1985-06-10). Official citation; the text was fetched from https://supreme.justia.com/cases/federal/us/472/181/. H
- S38 Seeking Alpha publisher's-exclusion decision: https://katten.com/judge-dismisses-case-against-seeking-alpha-implications-for-publishers-of-financial-information (pub. 2024-08-26); https://www.gtlaw.com/en/insights/2024/8/no-need-for-seeking-alpha-to-seek-registration M
- S39 SEC press release 2024-36 (AI washing): https://www.sec.gov/newsroom/press-releases/2024-36 (pub. 2024-03-18) H
- S40 SEC withdrawal of the PDA proposal: https://www.sec.gov/rules-regulations/2025/06/s7-12-23 ; https://www.sec.gov/files/rules/final/2025/33-11377.pdf (pub. 2025-06-12) H
- S41 FINRA Regulatory Notice 24-09: https://www.finra.org/rules-guidance/notices/24-09 (pub. 2024-06-27) H
- S42 FINRA 2026 Oversight Report, GenAI: https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/gen-ai (pub. Dec 2025) H
