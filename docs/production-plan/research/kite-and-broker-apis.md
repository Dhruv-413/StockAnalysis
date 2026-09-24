# Zerodha Kite Connect and Indian broker APIs: a deep dive for an information-only, India-first assistant

Research date and access date for every URL: **2026-09-24**. Author role: Market-Data Researcher. This is not legal advice.

**Labels**
- **[F]** fact from a primary source (vendor, exchange or regulator page, or a staff post on the vendor's own forum);
- **[F-sec]** fact from a secondary source or a search-result extract;
- **[C]** community evidence (a user post, not staff);
- **[I]** inference;
- **[A]** assumption;
- **[E]** estimate;
- **[P]** proposal.

Confidence is **H / M / L**.

**Method caveat.** Pages were read through an automated fetch-and-summarise tool, so "quotes" are that tool's extracts. Where a claim rests on one fetch, the confidence is capped at M unless the wording was re-checked (marked "re-checked"). Several sites could not be read:
- reddit.com is blocked for this agent;
- nseindia.com / nsearchives timed out;
- bseindia.com returned 403;
- x.com returned 402.

Read with: `docs/production-plan/research/india-market-data-and-sebi.md` (the "appendix"). This report verifies, deepens and **partly corrects** the appendix's Kite conclusion.

---

## 0. Bottom line

1. **"Kite data cannot be redisplayed" holds for any data that passes through our servers.** (H)
   - The Kite terms bar display "to the public at large" and caching "with the intent of redistributing".
   - Zerodha's support page says you "cannot display data from Kite Connect APIs on other platforms, as this violates the exchange's data vending policies", and calls Kite Connect "an execution suite, not a data vending service".
   - Zerodha staff said it directly in April 2021: **"A third-party app can't show our data. If you intend to use market data then you can contact some exchange registered data vendor."**
2. **Correction to the appendix.** The appendix inferred that per-user, same-user display is legitimate under platform/partner approval. **I found no source that supports this.** (H that no source was found; M on the conclusion)
   - Every approval route found is about **execution**: "exchange approvals" for trading platforms, algo-provider empanelment, and SEBI registration for "placing orders on behalf of clients".
   - No source grants a platform the right to **display** market data.
   - How Sensibull, Streak and smallcase source the live data they display is **unverified**.
   - **[I, M]** An information-only app with no order placement may have **no exchange-approval category to apply under**. The multi-login route may not exist for us at all. This must be asked (Q-Z-1).
3. **Deepened: Kite does have a platform route, but it is execution-oriented.**
   - The terms allow "build[ing] platforms which You may in turn offer to other Clients of Zerodha (after obtaining the required exchange approvals)" (H).
   - Multi-user login is granted case by case by Zerodha compliance (kiteconnect@zerodha.com), "usually... for an exchange approved platform which is built to cater mass" (H).
   - The APIs are free for mass-retail platforms (kite.trade/startups) (H).
   - Long-lived refresh tokens exist "only... to certain approved platforms" (H).
   - **No fee schedule is published.** Revenue share is by enquiry.
4. **Other brokers are the same or stricter.** No broker was found that grants display rights to third-party apps.
   - Upstox staff: "we do not provide market data for commercial purposes" (30 Jul 2024).
   - The Fyers API terms (re-checked) say exchange data "shall not be used for the development of different charting, technical tools, paper trading, gaming, and virtual trading purposes". Caching or redistribution needs written consent.
   - Dhan runs a formal partner OAuth programme, but its data rights for partners are unstated.
   - (M overall)
5. **Kite also fails the 06 §1 detector spec for a product feed.** (H/M)
   - It is not displayable.
   - The WebSocket carries L2 snapshots at about 1 tick per second per instrument, not every trade.
   - Minute candles can be revised about 30 seconds after the minute closes.
6. **SEBI/NSE retail-algo rules barely touch read-only use.** (H)
   - Static IP applies to **order endpoints only** at Zerodha, Dhan, Upstox and Angel.
   - What still applies to us: per-user OAuth/2FA, client-specific API keys ("no open APIs"), and daily session expiry (Kite: 6 AM next day).
7. **Recommendation [P].** The product data feed stays **licensed vendor + NSE/BSE agreements** (appendix §8), and no Kite-sourced data should reach our servers.
   - The only low-risk Kite integration is **side-by-side MCP**: the user's own AI client runs Zerodha's official Kite MCP next to ours.
   - Bring-your-own-key and platform multi-login are **blocked until Zerodha answers in writing**.

---

## 1. Kite Connect: official scope

### 1.1 Products and pricing

| Item | Fact | Source | Conf. |
|---|---|---|---|
| **Personal** plan | Free. "Full-fledged order, GTT, alerts management", margins and portfolio. **"No historical or real-time data included"** | [support: charges](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/what-are-the-charges-for-kite-apis); [forum 14868](https://kite.trade/forum/discussion/14868/introducing-kite-connect-personal-apis-free-apis-for-personal-use) (Mar 2025) | H |
| **Connect** plan | **₹500 per app per month**. Everything in Personal plus WebSocket real-time data and historical candles. "Available for retail users" | same support page; [zerodha.com/products/api](https://zerodha.com/products/api/) | H |
| Price history | Cut from ₹2,000 to ₹500 per month. Historical data (previously a separate ₹2,000) bundled from **8 Feb 2025** | [forum 15015](https://kite.trade/forum/discussion/15015/revising-kite-connect-fees-from-2000-to-500-per-month); [forum 14806](https://kite.trade/forum/discussion/14806/historical-data-is-now-free-with-base-kite-connect-subscription); [Marketcalls](https://www.marketcalls.in/algo-trading/zerodha-makes-trading-api-free-for-personal-use-bundles-historical-data-with-connect-api.html) (secondary) | H/M |
| **Startups / mass-retail platforms** | "If your platform is targeted at the mass retail market, the Kite Connect APIs are available free of cost... Zerodha can assist in obtaining necessary regulatory approvals." Revenue share: enquire by email. No published fee | [kite.trade/startups](https://kite.trade/startups/) | H |
| Fees clause (terms) | Zerodha may charge "fixed or variable" fees at its "sole discretion", and fees are non-refundable | [kite.trade/terms](https://kite.trade/terms/) | H |
| Liability cap | Zerodha's liability is capped at **INR 100** | kite.trade/terms | H |

**Cost formula (developer self-use only) [E]:** `₹500 × apps × months`. A product-wide formula does not exist, because Kite is not a product data licence.

### 1.2 Auth and session

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Login flow | 1. Redirect the user to `kite.zerodha.com/connect/login?v=3&api_key=…`.<br>2. A `request_token` comes back to the registered redirect URL.<br>3. POST `/session/token` with checksum = SHA-256(api_key + request_token + api_secret) to get the `access_token`. | [docs: user](https://kite.trade/docs/connect/v3/user/) | H |
| Expiry | The access token "will expire at 6 AM on the next day (regulatory requirement)", or earlier on logout or master-logout | same | H |
| Refresh token | "only available to certain approved platforms" | same | H |
| Daily manual login | Staff (2019): "It is mandatory by the exchange that a user has to login at least once a day... you can't bypass the login process" | [forum 5961](https://kite.trade/forum/discussion/5961/kite-connect-multiple-user) | H |
| 2FA/TOTP | Mandatory TOTP for API order placement from **3 Oct 2021**, citing SEBI cyber-security rules. Staff: "You'll need the TOTP to login only once per day." Automating TOTP (pyotp) is discussed by users but **not officially endorsed** | [forum 10391](https://kite.trade/forum/discussion/10391/mandatory-totp-for-all-kite-connect-apps); [forum 9738](https://kite.trade/forum/discussion/9738/totp-and-auto-access-token-generation) | H / M (automation stance) |
| Static IP | Required from **1 Apr 2026**, for **order endpoints only**: "The WebSocket market data stream and other APIs, such as orderbook and positions, can continue to be accessed from any IP address." Up to 2 IPs; one change per calendar week; can be shared only with immediate family | [support: static IP](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/static-ip); [forum 15912](https://kite.trade/forum/discussion/15912/preparing-to-comply-with-sebis-retail-algo-rules-static-ip-ratelimits-order-types) (staff, Mar 2026) | H |
| **Conflict** | The Kite API FAQ says static IP applies "from 1 April **2025**". All other Zerodha pages say 2026. Probably a typo | [support: FAQ](https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/kite-connect-api-faqs) | noted |

### 1.3 Rate limits

| Endpoint | Limit | Source | Conf. |
|---|---|---|---|
| Quote (`/quote*`) | **1 req/s** | [docs: exceptions](https://kite.trade/docs/connect/v3/exceptions/) | H |
| Historical candles | 3 req/s | same | H |
| Order placement | 10 req/s; 400 orders/min; 5,000 orders/day per user/API key; 25 modifications per order | same | H |
| All other endpoints | 10 req/s | same | H |
| Instruments per quote call | `/quote` 500; `/quote/ohlc` and `/quote/ltp` 1,000 | [docs: market quotes](https://kite.trade/docs/connect/v3/market-quotes/) | H |
| SEBI 10 OPS | 10 orders per second per client ID. Above that, the strategy must be registered with the exchange; 429 on breach | forum 15912; FAQ | H |

### 1.4 WebSocket ticker (KiteTicker)

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Modes | `ltp` (8 bytes), `quote` (44 bytes, no depth), `full` (184 bytes, with depth) | [docs: websocket](https://kite.trade/docs/connect/v3/websocket/) | H |
| Capacity | **3,000 instruments per connection; 3 connections per API key** (so 9,000 instruments at most) | same | H |
| Depth | 5 bid + 5 ask | same | H |
| Frequency and semantics | Not documented. Staff (2018): "You can expect one tick per second on a liquid instrument usually"; ticks are "level 2 snapshot", not tick-by-tick; the NSE commitment is "5 depth 1 second refresh"; TBT "can be technically consumed only by a machine in colo" | [forum 4814](https://kite.trade/forum/discussion/4814/what-is-the-maximum-number-of-ticks-sent-for-a-very-active-scrip) | H (staff) |
| Latency | A user measured 800 ms–1 s. Staff (Jan 2024): "We just relay the tick... We don't throttle... Kite Connect is not meant for HFT or latency based strategies"; suggests colocation "around 20 lakh+ per annum" | [forum 13587](https://kite.trade/forum/discussion/13587/fast-market-data) | H (staff) / L (the latency figure is one user's) |
| Heartbeat | 1-byte heartbeat "every couple seconds" when idle | docs: websocket | H |

### 1.5 Historical API

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Intervals | minute, 3/5/10/15/30/60-minute, day | [docs: historical](https://kite.trade/docs/connect/v3/historical/) | H |
| OI | `oi=1` returns open interest | same | H |
| Expired F&O | `continuous=1` returns **day** candles across expired NFO/MCX futures only | same | H |
| Depth of history | Staff (Jun 2024): daily NSE data from the "late 1990s"; minute data from "around early 2015" | [forum 14149](https://kite.trade/forum/discussion/14149/historical-data-retention-policy) | H (staff) |
| Per-request window | Minute: 60 days; 3–10 min: 100 days; 15–30 min: 200 days; 60 min: 400 days; day: 2,000 days. From forum posts, **not the docs**; the forum lists some intervals that are not in the docs | forum 14149; [forum 15111](https://kite.trade/forum/discussion/15111/historical-data-limit-60-days) | M |
| Fitness for live use | Staff (Jul 2025): "It is not guaranteed that a minute candle will be available exactly at the end of the minute"; candles were seen changing at about :30 s; build live candles from ticks instead | [forum 15351](https://kite.trade/forum/discussion/15351/historical-data-changing-on-30th-second-of-every-minute-for-past-1-candles-data) | H |
| Volume method | Staff (May 2025): historical minute volume = **sum of per-tick volumes**. The delta of cumulative `volume_traded` misorders because "we receive only seconds-level tick timestamps from the exchange" | [forum 14999](https://kite.trade/forum/discussion/14999/kite-connect-api-volume-discrepancy-between-websocket-ticks-and-historical-api-for-nfo-futures) | H |

### 1.6 Other endpoints and SDKs

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Instruments dump | `api.kite.trade/instruments`, gzipped CSV, **authenticated**, generated once a day ("last_price is not real time"). Fields include instrument_token, exchange_token, tradingsymbol, expiry, strike, tick_size, lot_size, segment | [docs: market quotes](https://kite.trade/docs/connect/v3/market-quotes/) | H |
| Alerts API | Simple alerts, and ATO (Alert Triggers Order); **500 active alerts per user**. Plan availability is not stated on the docs page; the support page lists "alerts management" under Personal | [docs: alerts](https://kite.trade/docs/connect/v3/alerts/); support: charges | H / M |
| GTT | Included in Personal ("Full-fledged order, GTT, alerts management") | support: charges | M |
| Publisher (offsite orders) | JS/HTML trade buttons, basket of up to 10, no API integration needed; **order placement only**: "you can't access orderbook, positions or holdings" (staff 2017) | [kite.trade/publisher](https://kite.trade/publisher/); [docs: basket](https://kite.trade/docs/connect/v3/basket/); [forum 1985](https://kite.trade/forum/discussion/1985/multi-user-apps) | H |
| pykiteconnect | **v5.2.2, released 15 Sep 2026**; MIT licence. PyPI metadata says "Python 3.5+" (likely stale; v5 dropped 2.7) | [PyPI](https://pypi.org/project/kiteconnect/); [GitHub](https://github.com/zerodha/pykiteconnect) | H (version, licence) / L (Python floor) |
| Kite MCP server | MIT. Hosted `mcp.kite.trade` is **free with no paid Kite Connect subscription**. Z-Connect (20 May 2025): "completely free of charge"; 22 tools including "Real-time quotes and last traded price", OHLC and "Historical price data", plus holdings, positions and margins; read-only except GTT | [GitHub](https://github.com/zerodha/kite-mcp-server); [Z-Connect](https://zerodha.com/z-connect/featured/connect-your-zerodha-account-to-ai-assistants-with-kite-mcp) | H (licence, free) / M (tool list) |

**Correction to the appendix (Kite MCP).** The appendix says hosted MCP has no historical data ("Self-hosted only") and leaves open (Q-B-4) how hosted MCP serves quotes to free Personal users.
- Both the GitHub README and the Z-Connect post list quotes and historical tools on the hosted server, and state it is free.
- **[I, M]** Zerodha serves this data under its own arrangement to the user's own AI client. That answers the cost half of Q-B-4 (free to the user).
- The rights half stays open: may a third-party app direct its users to hosted MCP? Keep Q-B-4 open on that point.

**Keep the three layers apart.**
- *Software licence:* pykiteconnect and kite-mcp-server are MIT. That covers the code only and grants **no** data rights.
- *API terms:* kite.trade/terms (below).
- *Data rights:* these belong to the exchanges (NSE/BSE) and are never granted by Zerodha to a third-party app (support page).

### 1.7 Kite Connect terms: clause map ([kite.trade/terms](https://kite.trade/terms/), no last-updated date shown; H)

| Right | Clause (fetched extract) | Reading |
|---|---|---|
| **Display, internal vs external** | "live market data obtained via Kite Connect cannot be displayed to the public at large" | External display is barred. **[I, M]** "Public at large" arguably leaves room for a closed, approved platform. But support and staff statements close that gap for data: "A third-party app can't show our data" |
| **Personal use** | "This may be for personal use, where You, a Client, develops a private interface exclusively for customising personal trading and investment experience" | Default scope is personal |
| **Platforms / multi-user** | "You may use the APIs to build platforms which You may in turn offer to other Clients of Zerodha (after obtaining the required exchange approvals)"; "The development of trading platforms is bound by various norms and regulations stipulated by various exchanges and SEBI..." | The platform route is framed around **trading platforms** |
| **Storage / retention** | "Scrape, build databases, or otherwise create permanent copies of such content, or keep cached copies with the intent of redistributing"; "delete any cached or stored content that was permitted by the cache header" | A shared cross-user cache is barred. Per-user caching for the user's own use is not explicitly barred [I, M] |
| **Derived data** | Barred: "Copy, translate, modify, create a derivative work of, sell, lease, lend, convey, distribute, publicly display, or sublicense to any third party"; plus a ban on reverse-engineering or "deriv[ing] the composition" | As extracted, the clause is about "content" in general; market data is not clearly its object. Taken with the support page ("execution suite, not a data vending service") and the 2021 staff line, indicators or AI summaries computed from Kite data and shown to third parties are most likely not allowed [I, M] |
| **Commercial use** | No explicit commercial-use clause was found. The ₹500 Connect plan is "Available for retail users". The commercial route is kite.trade/startups: free for mass-retail platforms, revenue share on enquiry. Fees are "at the sole discretion of Zerodha" | There is no self-serve commercial data licence [I, H] |
| **Redistribution incl. exports** | Covered by the above. There is no export clause | CSV export of Kite data to other people = redistribution [I, H] |
| **Prohibited uses** | "virtual/mock trading apps, trading related games" | Paper trading is out |
| **Termination** | Zerodha may terminate "without cause effective immediately"; the user must give 15 days' written notice | Platform risk: no continuity guarantee |
| **Law** | India; arbitration in Bangalore | — |

---

## 2. The multi-user / platform model (the key question)

| Question | Evidence | Conf. |
|---|---|---|
| Can a third-party app let many users log in with their own Kite accounts? | **Yes, but only with approval.** Staff (Sep 2023): "Kite Connect is provided only for personal use. The multi user access is provided only for product that is built for mass and needs an exchange approval." Staff (Dec 2022): "write to compliance... before building any kind of platform for mass" (kiteconnect@zerodha.com; the 2017/2019 threads said talk@rainmatter.com) | H ([13135](https://kite.trade/forum/discussion/13135/request-for-multi-user-api-access), [12172](https://kite.trade/forum/discussion/12172/multi-login-support-for-mass-retail-solutions)) |
| Precedents | smallcase, Streak, Sensibull. Zerodha's X post (Apr 2025, via search extract) says Kite Connect launched in 2016 "to allow platforms like Smallcase, Sensibull, Streak, etc., to build on top of us... we would take care of the execution and regulatory compliance" | M (x.com unreadable) |
| What approval means | The terms speak of "exchange approvals" for **trading platforms**. A 2025 TradingQnA staff reply says placing orders for clients needs "Sebi Registered Advisor or some similar certification". NSE algo empanelment (NSE/INVG/69255, 22 Jul 2025) covers any provider offering API order placement | H ([TradingQnA 183338](https://tradingqna.com/t/how-to-connect-with-zerodha-something-like-smallcase-streak/183338)) |
| Is there a public "Kite Connect for platforms" fee schedule? | **No.** Free for mass-retail platforms; revenue share "write to learn more" | H |
| **Can per-user data be shown only to that same user?** | **No source says yes.** Every direct statement found says no: support ("cannot display... on other platforms"); staff Apr 2021 ("A third-party app can't show our data... contact some exchange registered data vendor"; [forum 9569](https://kite.trade/forum/discussion/9569/is-their-licensing-restriction-with-the-market-quote-and-historical-data-returned-by-the-api)); community member MAG, not staff: "any other broker provided API is designed only for individual use" ([forum 13828](https://kite.trade/forum/discussion/13828/few-questions-related-to-kite-api)) | H (the statements) / M (that approved platforms get no display carve-out) |
| How do Sensibull, Streak and smallcase show live prices? | **Unverified.** They may hold their own exchange or vendor licences, or have a Zerodha arrangement. Do not infer a precedent | — |
| Account data vs market data | Holdings, positions and funds are **the user's personal data** (DPDP), not exchange market data. But Kite's holdings and positions responses include `last_price`, which is exchange data. **[I, M]** An "own portfolio" view would therefore still carry live prices and meet the same display question | M |

---

## 3. SEBI retail algo framework: what applies to read-only use

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Circular | SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013, **4 Feb 2025**, "Safer participation of retail investors in algorithmic trading" | [SEBI page](https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html) (headers only); [CSE copy](https://www.cse-india.com/upload/upload/Feb_042025.pdf) | M |
| Timeline | 1 Aug 2025 → 1 Oct 2025 → glide path (SEBI 30 Sep 2025) → **mandatory 1 Apr 2026** | appendix; Kite forum 15350 | H |
| NSE operating circulars | NSE/INVG/67858 (5–6 May 2025); NSE/INVG/69255 (22 Jul 2025: empanelment of algo providers, registration of retail algos); NSE FAQ 3 Nov 2025 (timed out) | [INVG67858](https://nsearchives.nseindia.com/content/circulars/INVG67858.pdf); [forum 15350](https://kite.trade/forum/discussion/15350/notes-on-the-nse-circular-prescribing-operating-procedures-for-api-usage); [Z-Connect overview](https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework) | H/M |
| "No open APIs" | Access only by a "unique vendor-client-specific API key" and a whitelisted static IP; OAuth/2FA | [Business Standard](https://www.business-standard.com/markets/capital-market-news/nse-lays-down-new-ground-rules-for-retail-algo-trading-to-boost-safety-and-compliance-125050600690_1.html) (secondary); Z-Connect | M |
| Static IP | For **order** APIs. Zerodha: "Only order endpoints... will be validated against the static IP. All other API endpoints — WebSocket data, order book, positions, etc. — remain accessible from any IP." Dhan, Upstox and Angel say the same | Kite forum 15912; [Dhan auth](https://dhanhq.co/docs/v2/authentication/); Upstox announcement (appendix); [Angel](https://www.angelone.in/news/market-updates/what-s-changing-in-angel-one-s-smartapi-access-from-april-1-2026) | H |
| 10 OPS threshold | ≤10 orders per second per client per exchange: no registration (generic algo ID). Above that: exchange registration with a unique ID, auditor certificate and strategy documents | forum 15350; Angel; Z-Connect | H |
| "Tech-savvy" retail | Clients who write their own algos may self-host with a registered static IP. Above 10 OPS they register through their broker. Otherwise strategies are hosted on the broker | Angel page; [Mondaq](https://www.mondaq.com/india/commoditiesderivativesstock-exchanges/1581380/sebi-circular-safeguarding-retail-investors-in-algorithmic-trading) (secondary) | M |
| Empanelment | Any provider offering API order placement to others must be exchange-empanelled (about T+30 days); brokers act as principal | [TrueData blog](https://www.truedata.in/blog/new-nse-rules-on-retail-algo-trading-what-traders-platforms-and-brokers-need-to-know) (secondary); NSE empanelled list page | M |
| Session logout | API sessions must be logged out before the next trading session | Business Standard (secondary); Kite 6 AM expiry (primary) | M / H |
| Market effect | Fyers reportedly disabled order placement via third-party platforms from 1 Apr 2026 | [LinkedIn post](https://www.linkedin.com/posts/kirubakaran-rajendran-90745a9b_fyers-just-disabled-order-placement-for-all-activity-7444217244890546176-6yPl) | L |

**What still applies to us (information-only, no orders) [I, H]:**
- No empanelment, no algo ID and no static IP.
- Still applies to any per-user broker connection:
  - per-user OAuth with 2FA;
  - an API key specific to the vendor and client (a single shared "open" key is barred);
  - a daily session that ends at 6 AM (Kite), so the user must re-login every trading day;
  - no refresh tokens unless we are an approved platform.
- **Open [A]:** whether refresh tokens for approved platforms still survive the NSE daily-logout rule (Q-Z-3).

---

## 4. Comparable broker APIs

Everything in this table is for the user's **own account and own use**, unless the "Terms" column says otherwise. "Unverified" means no primary terms were read.

| Broker | Cost | Ticks / depth | Historical / OI | Rate limits | WebSocket limits | Terms: redistribution / multi-user | Conf. |
|---|---|---|---|---|---|---|---|
| **Zerodha Kite Connect** | Personal free (no data); Connect ₹500 per app per month; free for approved mass-retail platforms | ~1 tick/s L2 snapshot; 5-level | 1-min from ~2015, daily from late 1990s; OI yes; 60-day minute window | Quote 1/s; historical 3/s; others 10/s; 10 OPS | 3,000 instr × 3 connections | No display to the public; no redistribution cache; multi-login only via compliance approval; "third-party app can't show our data" | H |
| **Upstox API v2/v3** | "All trading + data APIs are free"; ₹10/order offer until 30 Sep 2026 | Modes ltpc / option_greeks / full (5-level) / full_d30 (30-level, Upstox Plus); marketing says "tick-by-tick" (unevidenced) | Minutes and hours from **Jan 2022**; days, weeks and months from Jan 2000; 1–15 min: 1-month window; OI in candles | Per user per API: 50/s, 500/min, 2,000/30 min; orders 10/s unregistered (50/s registered) | 2 connections (5 with Plus); LTPC 5,000 keys; Full 2,000; D30 50 | Multi-client "UpLink Business" API exists (onboarding by email). Staff, 30 Jul 2024: **"we do not provide market data for commercial purposes"** | M/H ([trading-api](https://upstox.com/trading-api/), [feed v3](https://upstox.com/developer/api-documentation/v3/get-market-data-feed/), [historical v3](https://upstox.com/developer/api-documentation/v3/get-historical-candle-data/), [rate limits](https://upstox.com/developer/api-documentation/rate-limiting/), [community 5858](https://community.upstox.com/t/access-to-the-multi-client-api-as-a-partner-of-upstox/5858), [community 14024](https://community.upstox.com/t/request-for-uplink-business-multi-client-api-access/14024)) |
| **Angel One SmartAPI** | Free | WebSocket 2.0 | "Decades" of equity candles (appendix); getCandleData 3/s, 180/min | Documented; users report false 429s far below the limits (Aug 2026) | 3 connections per client code; 1,000 tokens | Has "Publisher login" for platforms. Data terms **unverified** | M ([forum 5639](https://smartapi.angelone.in/smartapi/forum/topic/5639/getcandledata-rate-limit-false-positives-at-0-003-req-sec-six-independent-reports-zero-acknowledgment)) |
| **Dhan (DhanHQ v2)** | Trading free; **Data API ₹499/month + tax** | Ticker / Quote / Full (5-level + OI) | Daily since inception; intraday 1/5/15/25/60-min, 90-day window, ~5 years back; OI; expired options endpoint | Orders 10/s, 250/min, 1,000/h, 7,000/day; data 5/s, 100k/day; quote 1/s. (The marketing page says "25 orders/second" and "20,000 requests per day": conflict) | 5 connections × 5,000 instruments | **Formal partner OAuth** (partner_id/secret, consent flow); lists smallcase and TradingView as partners. Token 24 h. Data rights for partners **unstated** | M/H ([docs](https://dhanhq.co/docs/v2/), [feed](https://dhanhq.co/docs/v2/live-market-feed/), [historical](https://dhanhq.co/docs/v2/historical-data/), [auth](https://dhanhq.co/docs/v2/authentication/), [partners](https://dhanhq.co/trading-apis), [data sub](https://dhan.co/support/platforms/dhanhq-api/how-does-the-dhanhq-data-api-subscription-work/)) |
| **Fyers API v3** | Data "absolutely zero fees" | Data socket plus TBT socket | Yes (limits unverified) | 10/s, 200/min, 100k/day; 10 OPS; >3 per-minute breaches in a day blocks the account for the day | Data ≤5,000 symbols per connection; TBT 3 connections × 5 symbols | **Terms (re-checked):** exchange data "shall not be used for the development of different charting, technical tools, paper trading, gaming, and virtual trading purposes". Caching or redistribution only with "written consent". Platforms allowed "after obtaining the required approvals from the relevant Exchange and statutory authorities" | H (terms) / M (limits) ([terms](https://fyers.in/terms-and-conditions-api), [FyersDev rate-limits](https://github.com/FyersDev/fyers-skills/blob/master/skills/fyers-trading/references/rate-limits.md), [support](https://support.fyers.in/portal/en/kb/articles/do-i-need-to-pay-for-datafeeds)) |
| **ICICI Breeze** | Free | Streaming OHLC; option chain | **3 years of 1-second LTP**; intervals 1 s, 1 min, 5 min, 30 min, 1 day; OI in option chain | 100 calls/min, 5,000/day; orders 10/s | Unverified | NSE only (no BSE/MCX). Terms **unverified** | M ([breeze](https://www.icicidirect.com/futures-and-options/api/breeze), [docs](https://api.icicidirect.com/breezeapi/documents/index.html)) |
| **Kotak Neo** | Free "at present" | WebSocket (up to 30 scrips per request) | "Several years" (vague) | 10 OPS | Unverified | Unverified | L/M ([Kotak Neo](https://www.kotakneo.com/platform/kotak-neo-trade-api/)) |
| **5paisa Xstream** | "completely free of charge" | WebSocket with depth and OI | Daily since inception; intraday 6 months | Conflicting snippets (25 OPS vs 50 req/min on other APIs) | Unverified | Unverified | L ([charges](https://forum.5paisa.com/portal/en/kb/articles/what-are-the-charges-to-use-5paisa-apis), [xstream](https://xstream.5paisa.com/)) |
| **Groww Trade API** | **₹499 + tax per month early bird; ₹2,000 standard** (resolves the appendix conflict) | LTP / quote / OHLC; feed | Up to 3 months of candles; OI for derivatives | Unverified | 1,000 feed subscriptions; 50 instruments per quote call | Unverified | M ([groww.in/trade-api](https://groww.in/trade-api)) |
| **Shoonya (Finvasia)** | "Free" (secondary) | Quotes, depth, option chain | Candles | Unverified | Unverified | Unverified | L ([docs](https://shoonya.com/api-documentation)) |
| **Alice Blue (ANT)** | Free to clients and partners (secondary) | WebSocket feeds | Historical endpoint exists | Unverified | Unverified | Unverified | L ([v2 docs](https://v2api.aliceblueonline.com/)) |

**Cross-broker takeaways**
- **[I, M]** Every broker whose terms or staff statement was found (Zerodha, Upstox, Fyers) restricts third-party display or commercial data use. Fyers goes further and names "charting, technical tools".
- **[I, M]** Dhan and Upstox have the most formal multi-client programmes (partner OAuth, UpLink Business). Both are framed around trading and investing, and neither publishes data rights for partners. They are the best candidates for a written answer.
- **[I, H]** Per-user rate limits make a broker a **per-user lane**, never a product backbone. For example, Kite quotes are limited to 1 request per second per key.

---

## 5. Community evidence

reddit.com is **blocked** for this agent; no Reddit threads were read. TradingQnA and the Kite, SmartAPI and Upstox forums were used instead.

| Theme | Evidence | Source | Conf. |
|---|---|---|---|
| Token expiry / daily login | A daily manual login is mandated; many threads try to automate TOTP (pyotp). Staff do not endorse it | Kite forums 5961, 9738, 10391, 11930 | H |
| WebSocket 1006 disconnects | Causes: an invalid token (403 on upgrade); more than 3 connections (429); blocking inside `on_tick`; drops after 2–3 h | [pykiteconnect #102](https://github.com/zerodha/pykiteconnect/issues/102), [#88](https://github.com/zerodha/pykiteconnect/issues/88); Kite forums 13327, 10476 | M |
| Tick drops / delay | Users report missing ticks and ticks arriving about 2 s late; staff: no guaranteed tick count; all ticks are impossible over the internet | Kite forums 11418, 14074, 11645 | M |
| Latency | One user measured 800 ms–1 s (vs 30 ms network); staff: not meant for latency strategies | forum 13587 | L (one measurement) |
| Historical gaps | A 25-minute gap in 1-min/5-min candles; 1–2-point differences vs charts; a mismatch in the 3:25 PM candle | Kite forums [8969](https://kite.trade/forum/discussion/8969/data-missing-gap-in-historical-data-candles), 11162, 10029 | M |
| Volume mismatch | Tick-summed vs historical volume on NFO futures (differences of 50 to 25,350); explained by the method (§1.5) | forum 14999 | H |
| Candle revision | Minute candles change at about :30 s | forum 15351 | H |
| Angel rate limits | Six reports of 429s at about 0.003 req/s; staff replies dismissive; threads deleted | SmartAPI forum 5639 | M |
| Multi-user approval | No builder report of **receiving** approval was found. Staff (sujith, Jun 2021): "if you are intending to develop a product for mass then you need to get a go-ahead from the compliance team before starting the project", otherwise "all the effort of development may be of no use"; the same thread's summary says "each user should have their own API key" (context unclear, M). Upstox applicants report forms going unanswered (May 2024) | [Kite forum 9859](https://kite.trade/forum/discussion/9859/what-is-the-recommended-way-to-support-multiple-users-in-same-application); Upstox community 5858 | H (staff quote) / M |

---

## 6. Official NSE/BSE alternatives (only what is new versus the appendix)

| Item | Fact | Source | Conf. |
|---|---|---|---|
| NSE 2026 pricing file | Reportedly **effective 1 Apr 2026**. The search extract says: "The mobile app for data vendor is not available on standalone basis and can be only subscribed in addition to either terminal or software/charting application usage." This updates appendix unresolved item 1, but the extract may come from an older file. The PDF timed out again | [NSE pricing 2026-03](https://nsearchives.nseindia.com/web/mediaattachment/2026-03/NSE_Pricing_file_-_Domestic_clients_20260309171343.pdf); [NSE data vending](https://www.nseindia.com/static/nse-data-and-analytics/data-information-vending) | M/L |
| NSE feed levels | L1 = best bid/ask; L2 = 5-level; L3 = 20-level; TBT = full order book. Leased-line multicast, or via an authorised vendor | [NSE real-time subscription](https://www.nseindia.com/static/market-data/real-time-data-subscription) (search extract) | M |
| TrueData | Offers "Tick, 1-Minute, 2-Minute, 5-Minute, 15-Minute (Delayed), and EOD". To "Display data on a website or app for public or client access... You must first obtain written approval from the exchanges and TrueData." Velocity (retail) plans exclude API access; API needs "a separate application, compliance review, and approval". **No public API prices** | [market-data-apis](https://www.truedata.in/market-data-apis); [price](https://www.truedata.in/price) | H (policy) |
| Global Datafeeds (GFDL) | "Flexible pricing... tailored"; sales@globaldatafeeds.in; L1 at 1-second frequency; standard terms "for charting / analysis use of a single subscriber only" with no redistribution. A product display licence must be negotiated | [api-pricing](https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/pricing-sales/api-pricing/); [apis](https://globaldatafeeds.in/apis/) | M |
| Accelpix | Pix Connect ₹1,599–3,499 per month (10–300 symbols, 1 segment, excl. GST). **Licensed "strictly... for personal, non-commercial use"**. Do **not** use these in product cost formulas; commercial use "requires separate exchange-approved licensing" | [accelpix.com/pricing](https://accelpix.com/pricing/) | H |
| Accord Fintech (ACE) | Authorised vendor of BSE, NSE, MCX and NCDEX (already in the appendix) | [accordfintech](https://www.accordfintech.com/market-data-feed) | M |
| BSE | Tariff PDF returned **403**. Domestic datafeed sales contact from the search extract: datafeed.sales@bseindia.com. Products are distributed by leased line and via vendors | [BSE tariff PDF](https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf) (unread) | L |

**Cost formula (unchanged in structure from appendix §1.3) [E]:**
`NSE_licence(category, S) + BSE_licence + vendor_product_display_fee (quote) + non-display/derived (if applicable)`.

Retail vendor plans (Accelpix, TrueData Velocity) are **not** inputs to this formula.

---

## 7. Check against the detector spec (06 §1)

| Feed | Consolidated (NSE + BSE) | Full volume | 1-minute bars | Displayable to our users | Verdict |
|---|---|---|---|---|---|
| Kite Connect | Per exchange, no merge | L2 snapshot at ~1/s. Minute volume = sum of tick volumes (Zerodha's own method), so exact exchange volume is **unverified** | Yes (history from ~2015; live candles revised up to ~30 s late) | **No** | **Fails** (display). Usable only by a developer on their own account |
| Upstox / Dhan / Fyers / Angel | Per exchange | Snapshot (unverified per broker) | Yes | No / unverified | Fails on display until written consent |
| Licensed vendor (TrueData / GFDL) + NSE/BSE agreements | Both | TrueData tick claimed; GFDL 1-second snapshot | Yes | Yes, with written approval | Candidate (appendix Q-V-*) |

---

## 8. Implications for our product

Card-first, about 300 ms, a shared exact-key card cache, information-only.

| Mode | How it works | Allowed? | Blocker | Fit with a 300 ms card cache | Verdict |
|---|---|---|---|---|---|
| **(a) Kite platform multi-login** (like smallcase/Streak) | We register one app; users "Login with Kite"; we call Kite for them | Only with compliance approval, which is framed for exchange-approved **trading** platforms. **Data display is not shown to be included** | An information-only app may have no approval category. Display unconfirmed. Terminable without cause | Poor: a per-user, uncached lane. It cannot feed the shared card cache (redistribution-cache clause), and there is 1 quote request per second per key | **Blocked pending Q-Z-1/Q-Z-2** |
| **(b) Bring-your-own API key** | Each user creates their own Kite Connect app (₹500/mo) and gives us the api_key/secret; we run the login flow | **[I, M] Most likely not.** This is the "third-party app" showing Kite data that staff ruled out; the user's personal licence is for "a private interface" they develop themselves | User pays ₹500/mo; daily login; we would hold their api_secret (security and DPDP burden) | Poor: the same per-user lane, and every user must log in daily | **Do not build** |
| **(c) Side-by-side MCP** | The user's own Claude/ChatGPT client connects Zerodha's official Kite MCP **and** our MCP. The client, not our server, fetches Kite data | **Most plausible [I, M]**: Kite data flows between Zerodha and the user's own client. We never receive, store or display it | **Leak risk:** if our tools accept Kite-sourced numbers as arguments (for example "explain this price 2,413.5"), Kite data reaches our servers and logs. Our tool schemas must take symbols and timestamps, not prices; logs must drop price arguments; and our answers must use our licensed or delayed data, labelled with its own source and entitlement | Our cards keep our own licensed data; unaffected. **User cost:** hosted Kite MCP is free (Z-Connect, May 2025), so no ₹500/mo is needed. Whether a third-party app may direct users to it is still open (Q-B-4, Q-Z-4) | **Recommended as a channel (14 §7 rank 1)** |
| **(d) Licensed central feed** | Vendor + NSE/BSE agreements → our cache → cards | Yes, with licences (appendix §1.3, §8) | Cost and category (Q-NSE-1 to Q-NSE-7) | Only mode that fits a shared cache and 100k users | **Product backbone** |

**Account data.** Holdings, positions and funds via a broker are personal data under DPDP, and they include `last_price` (exchange data). Any "your portfolio" feature is mode (a) and has the same display question. Defer it until Q-Z-2 is answered.

**Developer use.** Team members may use their own Kite Connect (₹500/mo) for their own research only. Nothing from it may go into fixtures, the cache, screenshots or demos shown to others. **[I, H]** The derivative-work and display clauses cover demos.

**Recommended edits to the appendix [P]** (for the owner or tech lead to apply; this agent does not edit repo files):
- §0.1 and the §6 table: replace "legitimate only as a per-user, same-user display... under a platform/partner approval" with "no source confirms display rights even for approved platforms; the only direct staff statement says a third-party app cannot show Kite data".
- §2 table: correct Groww (₹499 early bird / ₹2,000 standard), and add Fyers' "charting, technical tools" clause and Upstox's "no market data for commercial purposes".
- Mark NSE unresolved item 1 as "2026 file reportedly keeps the not-standalone clause (M/L)".
- §2 Kite MCP row: hosted MCP includes quotes and historical data and is free to users (Z-Connect, 20 May 2025). Narrow Q-B-4 to the rights question.

---

## 9. New vendor questions (exact text; for the user to send; answers not guessed)

These add to appendix Q-B-1 to Q-B-4; they do not repeat them.

**Zerodha (kiteconnect@zerodha.com)**
- **Q-Z-1:** "We are building an information-only market assistant. It places no orders and gives no advice. Is there any multi-user or platform approval route for an app that never places orders? If the only route is the exchange-approved trading-platform route, which exchange approval would apply to us?"
- **Q-Z-2:** "For approved multi-user platforms such as smallcase or Streak, does the approval include displaying Kite Connect market data (LTP, quotes, candles), or holdings with last_price, to the same logged-in user inside the platform? Or must platforms license displayed market data separately from an exchange-authorised vendor?"
- **Q-Z-3:** "After NSE's retail-algo operating procedures (NSE/INVG/67858 and 69255), are refresh tokens still issued to approved platforms? What is the session lifetime for an approved platform's user?"
- **Q-Z-4:** "If a user connects Zerodha's official Kite MCP (mcp.kite.trade) and our separate MCP server in the same AI client, and our server never receives Kite data, does any Kite Connect term apply to us?"

**Upstox (api@upstox.com)**
- **Q-U-1:** "On 30 Jul 2024 your team said on the community forum that 'we do not provide market data for commercial purposes'. Does this cover showing an UpLink Business user their own live quotes and holdings' LTP inside a partner app? Is there any partner tier with display rights?"

**Dhan (apihelp@dhan.co)**
- **Q-D-1:** "When a partner onboarded with partner_id/partner_secret calls the Data APIs on behalf of a consenting Dhan user, may the partner display that data to the same user? Who pays the ₹499 Data API fee in partner mode? May the partner cache the data across users?"

**Fyers**
- **Q-F-1:** "Your API terms say exchange data 'shall not be used for the development of different charting, technical tools...'. Does this bar a third-party app from computing indicators from a user's own data and showing them to that user? What does 'written consent' for caching or redistribution cover, and what does it cost?"

**BSE (datafeed.sales@bseindia.com)**
- Add this address to appendix **Q-BSE-1**. The tariff PDF returned 403.

---

## 10. Unverified list

1. Whether any Kite platform approval includes **display** of market data to the same user (Q-Z-2).
2. Whether an information-only (no orders) app can get multi-user approval at all (Q-Z-1).
3. How Sensibull, Streak and smallcase source their displayed live data (their own licence, a vendor, or a Zerodha arrangement).
4. Zerodha platform fees and revenue share (no public schedule).
5. Whether refresh tokens survive the 2026 NSE rules (Q-Z-3).
6. Kite historical per-request windows: from the forum, not the docs; interval names differ.
7. Kite TOTP automation: permitted or not (no clear staff statement).
8. Kite API FAQ "1 April 2025" static-IP date vs 2026 elsewhere.
9. The pykiteconnect Python floor ("3.5+" on PyPI; likely stale).
10. Upstox "tick-by-tick" marketing claim; Upstox product page (50/s) vs rate-limit page (10/s orders unregistered).
11. Dhan marketing (25 OPS, 20k/day) vs docs (10/s, 100k/day); Dhan data rights for partners.
12. Angel, Breeze, Kotak, 5paisa, Groww, Shoonya and Alice Blue data-display terms (primary terms not read); 5paisa rate limits (conflicting); Shoonya and Alice Blue limits.
13. NSE 2026 domestic pricing (PDF timed out); whether the "not standalone" mobile clause is from the 2026 file.
14. BSE domestic tariff (403).
15. TrueData, GFDL and Accord product display prices (quote-only).
16. Reddit community evidence (domain blocked for this agent).
17. The Zerodha X post (Apr 2025) wording (x.com returned 402; search extract only).
18. The full text of SEBI's 4 Feb 2025 circular and the NSE FAQ of 3 Nov 2025 (timeouts or headers only).
19. Hosted Kite MCP tool list: now corrected against the appendix (quotes and historical are hosted, and it is free), but it rests on the README and a May 2025 post. The current hosted tool set was not tested (no login). Q-B-4's rights question (may a third-party app direct users to it) is open.

---

## 11. Sources (all accessed 2026-09-24)

**Zerodha, primary**
- https://kite.trade/terms/
- https://zerodha.com/products/api/
- https://kite.trade/startups/
- https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/what-are-the-charges-for-kite-apis
- https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/can-i-use-historical-and-live-data-taken-from-kite-connect-api-on-other-platforms
- https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/kite-connect-api-faqs
- https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/static-ip
- Kite Connect v3 docs:
  - https://kite.trade/docs/connect/v3/user/
  - https://kite.trade/docs/connect/v3/exceptions/
  - https://kite.trade/docs/connect/v3/websocket/
  - https://kite.trade/docs/connect/v3/historical/
  - https://kite.trade/docs/connect/v3/market-quotes/
  - https://kite.trade/docs/connect/v3/alerts/
  - https://kite.trade/docs/connect/v3/basket/
  - https://kite.trade/publisher/
- Kite developer forum discussions: 1985, 4814, 5961, 9569, 9738, 10391, 12172, 13135, 13587, 13828, 14149, 14806, 14868, 14999, 15015, 15111, 15350, 15351, 15912, 8969
  - URL pattern: `https://kite.trade/forum/discussion/<id>/...` (full URLs inline above)
- https://tradingqna.com/t/how-to-connect-with-zerodha-something-like-smallcase-streak/183338
- https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework
- https://pypi.org/project/kiteconnect/
- https://github.com/zerodha/pykiteconnect
- https://github.com/zerodha/pykiteconnect/issues/102
- https://github.com/zerodha/pykiteconnect/issues/88
- https://github.com/zerodha/kite-mcp-server

**Other brokers**
- Upstox:
  - https://upstox.com/trading-api/
  - https://upstox.com/developer/api-documentation/v3/get-market-data-feed/
  - https://upstox.com/developer/api-documentation/v3/get-historical-candle-data/
  - https://upstox.com/developer/api-documentation/rate-limiting/
  - https://community.upstox.com/t/access-to-the-multi-client-api-as-a-partner-of-upstox/5858
  - https://community.upstox.com/t/request-for-uplink-business-multi-client-api-access/14024
- Angel One:
  - https://www.angelone.in/news/market-updates/what-s-changing-in-angel-one-s-smartapi-access-from-april-1-2026
  - https://smartapi.angelone.in/smartapi/forum/topic/5639/getcandledata-rate-limit-false-positives-at-0-003-req-sec-six-independent-reports-zero-acknowledgment
- Dhan:
  - https://dhanhq.co/docs/v2/
  - https://dhanhq.co/docs/v2/live-market-feed/
  - https://dhanhq.co/docs/v2/historical-data/
  - https://dhanhq.co/docs/v2/authentication/
  - https://dhanhq.co/trading-apis
  - https://dhan.co/support/platforms/dhanhq-api/how-does-the-dhanhq-data-api-subscription-work/
- Fyers:
  - https://fyers.in/terms-and-conditions-api
  - https://github.com/FyersDev/fyers-skills/blob/master/skills/fyers-trading/references/rate-limits.md
  - https://support.fyers.in/portal/en/kb/articles/do-i-need-to-pay-for-datafeeds
- ICICI Breeze:
  - https://www.icicidirect.com/futures-and-options/api/breeze
  - https://api.icicidirect.com/breezeapi/documents/index.html
- Kotak Neo: https://www.kotakneo.com/platform/kotak-neo-trade-api/
- 5paisa:
  - https://forum.5paisa.com/portal/en/kb/articles/what-are-the-charges-to-use-5paisa-apis
  - https://xstream.5paisa.com/
- Groww: https://groww.in/trade-api
- Shoonya: https://shoonya.com/api-documentation
- Alice Blue: https://v2api.aliceblueonline.com/

**Regulation**
- https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html
- https://www.cse-india.com/upload/upload/Feb_042025.pdf
- https://nsearchives.nseindia.com/content/circulars/INVG67858.pdf
- https://www.business-standard.com/markets/capital-market-news/nse-lays-down-new-ground-rules-for-retail-algo-trading-to-boost-safety-and-compliance-125050600690_1.html
- https://www.mondaq.com/india/commoditiesderivativesstock-exchanges/1581380/sebi-circular-safeguarding-retail-investors-in-algorithmic-trading
- https://www.truedata.in/blog/new-nse-rules-on-retail-algo-trading-what-traders-platforms-and-brokers-need-to-know

**Exchanges and vendors**
- https://nsearchives.nseindia.com/web/mediaattachment/2026-03/NSE_Pricing_file_-_Domestic_clients_20260309171343.pdf (timed out; search extract only)
- https://www.nseindia.com/static/market-data/real-time-data-subscription (search extract)
- https://www.bseindia.com/downloads1/Information_Products_Pricing_Sheet.pdf (403)
- TrueData:
  - https://www.truedata.in/market-data-apis
  - https://www.truedata.in/price
- Global Datafeeds:
  - https://globaldatafeeds.in/apis/
  - https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/pricing-sales/api-pricing/
- Accelpix: https://accelpix.com/pricing/
- Accord Fintech: https://www.accordfintech.com/market-data-feed
