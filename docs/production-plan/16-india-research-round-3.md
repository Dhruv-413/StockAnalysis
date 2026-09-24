# 16 — India Research Round 3: Kite and broker APIs, papers, case studies, official sources

← [Index](README.md) · Related: [14 Market assistant](14-global-market-assistant.md) · [15 Finance-model layer](15-finance-model-layer.md) · [ADR-008](adr/ADR-008-india-first-market-assistant-scope.md)

**Status:** research synthesis (2026-09-24). Proposals are marked **[P]**. Nothing here is decided. The owner decisions are in §7.

**The ask.** More research on papers, tools, official sources, case studies and what people have tried, including the Zerodha Kite API.

**Evidence.** Four new appendices, all sources accessed 2026-09-24, with confidence H/M/L inside each:
- [kite-and-broker-apis](research/kite-and-broker-apis.md): market-data-researcher.
- [papers-india](research/papers-india.md): quant-researcher, about 50 papers and regulator reports.
- [case-studies](research/case-studies.md): product-manager.
- [official-sources-and-tools](research/official-sources-and-tools.md): tech-scout.

The corrections they found have been applied as dated banners on the older appendices (§6).

---

## 1. Verdict in brief

1. **Kite Connect can't be our data feed (H).** Its terms bar live display "to the public at large" and caching "with the intent of redistributing". Zerodha support calls it "an execution suite, not a data vending service". Staff said a third-party app "can't show our data". Every broker we checked says much the same (Upstox, Fyers) or says nothing about data display (Dhan). **The product backbone stays a licensed vendor plus NSE/BSE agreements.**
2. **The Kite channel that does work [P, I-M]:** the user runs Zerodha's free **hosted Kite MCP** alongside **our MCP** in their own AI client.
   - Kite data flows between Zerodha and the user's own client and never reaches our servers.
   - Our tools therefore take **symbols and timestamps, not prices**, and our logs drop any price arguments.
   - Zerodha still has to confirm this setup (Q-Z-4).
3. **Official exchange RSS now exists:** 23 NSE feeds and 12 BSE feeds. BSE added its feeds after SEBI fined it ₹15 lakh in 2025 for disclosure asymmetry (H).
   - NSE's terms still ban "systematic or automated data collection" and any display without permission.
   - So these feeds stay **internal evaluation only** until NSE and BSE answer in writing (Q-O1).
4. **Every open-source NSE/BSE library we checked scrapes the exchange sites.** That is 10 libraries, 6 confirmed by grepping their source; see the appendix. They are on **Hold** for product use.
5. **Papers:**
   - Indian corporate events have well-documented price reactions: insider buys, bulk and block deals, promoter pledges, and drift before results. These tell us **what to collect and timestamp**. None of the studies is cost-aware or out-of-sample, so **none is a signal**.
   - LLMs can't recall prices: 0% accuracy from memory versus 98–100% when a tool supplies them. This backs the rule that numbers come from code.
6. **Case studies:**
   - **Stock calls earn money in India only under SEBI registration.** Univest made ₹44 Cr revenue in FY25 but lost ₹30 Cr.
   - **Unregistered sellers were hit by SEBI orders:** Baap of Chart (₹17.2 Cr disgorgement), Asmita Patel (₹53.67 Cr impounded) and Avadhut Sathe (₹546 Cr impounded).
   - **Brokers give AI away free:** Kite MCP, Streak (free since January 2024) and Robinhood Cortex.
   - **Independent tools** pivot to data, API and MCP (FinChat → Fiscal.ai) or get acquired (Composer → SoFi).

## 2. Zerodha Kite Connect: facts (details: [kite-and-broker-apis §1](research/kite-and-broker-apis.md))

| Item | Finding | Conf. |
|---|---|---|
| Plans | Connect: ₹500 per app per month. Personal: free, but with **no market data**. | H |
| Session | Access token expires at 6 AM the next day, so users log in daily. Refresh tokens go only to approved platforms. | H |
| Rate limits | Quotes: 1 request/s. Historical: 3 requests/s. | H |
| WebSocket | 3,000 instruments per connection, 3 connections per key, 5-level depth. Ticks are **snapshots about once a second, not every trade**. | H |
| Historical | Minute bars go back to about 2015, in 60-day chunks. A minute candle can change for about 30 s after the minute closes. Minute volume is the sum of tick volumes. | H |
| SDK | `kiteconnect` 5.2.2 (2026-09-15), MIT licence. The licence covers the code, not the data. (`pykiteconnect` is not a PyPI name.) | H |
| Multi-user platforms | Allowed "after obtaining the required exchange approvals", decided case by case by Zerodha. The approval routes we found cover **order placement**; **display rights aren't confirmed**. | H (terms) / M (scope) |
| SEBI retail-algo static-IP rule | Covers **order endpoints only**. Read-only use still needs a per-user login with 2FA and a daily re-login. | H |
| Hosted Kite MCP | Free to users. Includes quotes and historical data. No place/modify/cancel tools, but has GTT, so it is **not strictly read-only**. The self-hosted version can place orders. | H/M |
| Fit with our detector spec ([06 §1](06-quantitative-validation.md)) | Fails: no display rights, and snapshot ticks rather than every trade. | H |

**Other brokers** (full table in the appendix §4):
- Upstox: "no market data for commercial purposes".
- Fyers: its terms bar using its data for "charting, technical tools".
- Dhan: has a partner programme, but its data rights are unstated.
- Groww: ₹499/mo early bird, ₹2,000/mo standard. It also runs an **official MCP that can place orders**.

### How we could use Kite

| Mode | Verdict |
|---|---|
| (a) Kite platform login for many users | Blocked pending Q-Z-1 and Q-Z-2. Even if allowed, each user needs a separate, uncached data path, which can't feed the shared card cache. |
| (b) Each user brings their own API key | **Don't build.** Costs the user ₹500/mo, needs a daily login, and we would hold their secret. This is probably the "third-party app" case Zerodha staff ruled out. |
| (c) Hosted Kite MCP beside our MCP | **Recommended channel [P]** (14 §7, rank 1). |
| (d) Licensed vendor feed plus NSE/BSE agreements | **Product backbone.** |

Team members may use their own Kite Connect for their own research. Nothing from it may go into fixtures, the cache, screenshots or demos.

## 3. Official sources: what is free and what is restricted (details: [official-sources-and-tools §1](research/official-sources-and-tools.md))

| Source | Status for a commercial app | Conf. |
|---|---|---|
| NSE RSS (23 feeds, 5-min TTL; some items link to XBRL) | Terms ban automated collection and display without permission. **Internal evaluation only; Q-O1.** Timestamps are naive IST, so normalise them to UTC. | H |
| BSE RSS (12 feeds) | Terms unreadable (403). Same treatment as NSE. | M |
| NSE/BSE LODR XBRL taxonomies | Usable as a **parser schema** against recorded fixtures (Trial). | M |
| NSE D&A Corporate Data / EOD | The licensed route for announcements (quote pending). | M |
| SEBI RSS, PIB RSS | Usable (PIB allows reproduction with acknowledgement). SEBI's `pubDate` has no time of day. | H/M |
| MoSPI API / eSankhyiki | Usable under GODL. **The 2026 base-year revision breaks CPI, GDP and IIP series.** | H |
| RBI RSS | Its disclaimer bans caching and deep links without permission. Needs Q-O5. | H |
| AMFI NAVAll.txt | "Personal and non-commercial use only". **Format changes after 2026-09-30.** | H |
| FBIL benchmarks | A fee is due for redistribution. | M |

## 4. What the papers change (details: [papers-india §3](research/papers-india.md))

All of these are **[P]** for the owners of 06, 13 and 15:

1. **India event types.** Insider trades (PIT/SAST), promoter pledges, bulk/block deals, results (with an intraday vs. after-close flag), LODR Reg 30 categories, and SEBI orders.
   - Timestamp each one at **exchange dissemination time**, not media time.
2. **Timing states on every cited item.** `before_move`, `after_move_start`, or `after_close_disclosure`.
   - Deal files and provisional FII/DII flows are published after the close.
   - Pre-announcement drift is common, so the gold set must include many of these cases.
3. **Wording.**
   - Flows and deals "coincided with" a move, never "caused" it; FII flows follow returns.
   - Cite SEBI loss figures by study, year and broker coverage:
     - per-year loss-maker share: 90.2% / 91.7% / 91.1% / 91.0% for FY22–FY25;
     - FY25 net loss: ₹1,05,603 cr;
     - the "93%" figure is **three-year cumulative**.
4. **India detector additions.**
   - Dimson beta for thinly traded stocks.
   - A local benchmark: Nifty 500 or a sector index.
   - A **band-censoring flag**: when a stock closes at its price band, its abnormal return is a lower bound.
   - Per-stock empirical thresholds.
   - A worked fixture is in the appendix §4, for `financial-correctness-reviewer`.
5. **Datasets.**
   - No Hindi or Hinglish financial-sentiment benchmark exists, so we label our own.
   - SEntFiN is for internal evaluation only; its licence is unconfirmed.
   - The "NIFTY" headline dataset is US data (**exclude**).
6. **Indicators stay descriptive.** No NIFTY-stock study survives costs plus data-snooping tests.
7. **Retail-harm UX rules (IOSCO, ESMA, SEBI).**
   - No engagement mechanics, trending-buy lists or buzz scores.
   - An AI-use disclosure.
   - A dated SEBI risk line on F&O and intraday cards.

## 5. What the case studies change (details: [case-studies §6–7](research/case-studies.md))

- **Positioning [P].** Present the product as an **evidence API plus an MCP server**, not "AI chat". Never use signal, call, target or stop-loss wording, even in educational content.
- **Buyers to test first in I-08 [P].**
  1. SEBI research analysts, who need AI-use disclosure and an audit trail.
  2. Newsletter writers and educators, for whom an evidence tool with no calls helps them stay compliant.
  3. Small brokers and platforms, as a B2B API.
  4. Retail, **metered** only: Screener AI charges about ₹10–30 per answer.
- **What kills products in this space:**
  - Rule shocks: Sensibull's revenue fell 28.7% after the F&O curbs.
  - NSE scraping: nsepy is dead and nsetools gets 403 errors.
  - Wrong numbers in AI summaries: Bloomberg needed 36+ corrections.
  - Unlicensed news reuse: Dow Jones v. Perplexity.
  - AI-washing: SEC and FTC cases.

  Option A already avoids every one of these.
- **Telegram.** Digest format only, with a registration-status disclaimer and no "VIP" or "premium call" language.

## 6. Corrections applied to earlier appendices (as dated banners)

| Appendix | Correction |
|---|---|
| [india-market-data-and-sebi](research/india-market-data-and-sebi.md) | Display of Kite data under platform approval is **unconfirmed**. Hosted Kite MCP includes quotes and historical data and has GTT. Groww, Upstox and Fyers terms corrected. The static-IP rule covers orders only. |
| [distribution-and-competitors-india](research/distribution-and-competitors-india.md) | The Kamath "users build their own AI" citation was wrong. **Groww MCP exists and can trade.** |
| [fast-fetch](research/fast-fetch.md) | `sec-edgar-mcp` is AGPL-3.0. |
| [accuracy-indicators-algos](research/accuracy-indicators-algos.md) | Added the interim expiry-day period from January 2025. `exchange_calendars` has XBOM but no XNSE. |
| [tech-radar](research/tech-radar.md) | Updated with this round's placements, including official feeds, Hinglish symbol resolution, Sarvam-30B (Assess), Langfuse (Trial) and scraping libraries (Hold). |

## 7. Plan changes and decisions

**Draft questions (not sent; the owner sends them).**
- Q-Z-1 to Q-Z-4: Zerodha.
- Q-U-1, Q-D-1, Q-F-1: Upstox, Dhan and Fyers.
- Q-O1 to Q-O5: NSE/BSE RSS, AMFI, NSDL, Sarvam and RBI.
- Exact wording is in the appendices ([Kite §9](research/kite-and-broker-apis.md), [official §7](research/official-sources-and-tools.md)).

**Proposed new tasks [P]** (added to [08](08-implementation-roadmap.md) on acceptance):

| Task | Description | Owner(s) |
|---|---|---|
| R-01 | Send the Zerodha, broker, exchange and regulator questions; log the answers | owner (drafted by market-data-researcher + compliance-analyst) |
| R-02 | India event taxonomy and timing states in the card schema | data-engineer + quant-researcher |
| R-03 | LODR XBRL parser against recorded fixtures (no live polling) | data-engineer |
| R-04 | MCP tool schemas that take symbols and timestamps, never prices; logs redact price arguments | backend-engineer + security-engineer |
| R-05 | Hinglish symbol resolver (rapidfuzz + symspellpy + IndicXlit aliases) with a p95 latency harness | realtime-engineer |
| R-06 | Hindi/Hinglish labelled headline set and licence register for datasets | ml-llm-engineer + compliance-analyst |
| R-07 | Confirm with counsel: the education carve-out in the Sathe and Patel orders; the May-2026 registration-number-per-post rule for unregistered publishers; the Tradetron notices | compliance-analyst |

**Owner decisions**, in addition to [14 §9](14-global-market-assistant.md#9-decisions-needed-from-the-owner) and [15 §9](15-finance-model-layer.md#9-decisions-needed-from-the-owner):
1. Should the first buyers be professional and B2B (SEBI research analysts, educators, small brokers), with retail metered? Or retail first?
2. Does Univest's traction, despite its losses and complaints, change the answer on registered signals (14 §9 Q2)?
3. Adopt the hosted-Kite-MCP-beside-our-MCP channel, subject to Zerodha's answer to Q-Z-4?
4. May we send the drafted questions (R-01)? Each one discloses our product plan to the recipient.
