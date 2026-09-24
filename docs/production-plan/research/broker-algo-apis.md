# Broker APIs for a backtesting, paper-trading and automated-trading product (India): Kotak Neo deep dive, a nine-broker comparison, historical data and execution realities

Research date and access date for every URL: **2026-09-24**. Author role: Market-Data Researcher. This is not legal advice.

This report extends `docs/production-plan/research/kite-and-broker-apis.md` (the "Kite report") and does not repeat it. That report was written for an **information-only** assistant. The owner has now changed direction to **user backtesting, paper trading and automated trading**. That change moves the product into the SEBI/NSE retail-algo framework, which the Kite report treated as mostly out of scope.

**Labels** (same as the Kite report)
- **[F]** fact from a primary source (a broker, exchange or regulator page, official docs or repo, or a staff post on the broker's own forum);
- **[F-sec]** fact from a secondary source or a search-result extract;
- **[C]** community evidence;
- **[I]** inference;
- **[A]** assumption;
- **[E]** estimate;
- **[P]** proposal.

Confidence is H / M / L.

**Method caveat.** Pages were read through an automated fetch-and-summarise tool, so quotes are that tool's extracts. A fact that rests on a single fetch is capped at M unless it is corroborated. Sites that could not be read:
- nseindia.com and nsearchives (ECONNRESET or timeout: the terms of use, the data policy PDF, the retail-algo FAQ of 3 Nov 2025, and circular INVG/73992);
- dotexdata.nseindia.com;
- reddit.com (blocked);
- fyers.in/pricing-brokerage (404).

---

## 0. Bottom line

### 0.1 The owner's three features, one at a time

| Feature | What the evidence says | Verdict | Conf. |
|---|---|---|---|
| **Backtesting on broker historical data** | **Technically possible** at every broker except Kotak's MCX/NSE-commodity segments. **Legally**, broker data is licensed for the account holder's personal use. The Kite report has the Kite detail: "A third-party app can't show our data". No broker we read grants a third-party platform the right to pull a user's historical data to its own servers and show backtest results. | **Only safe pattern:** the backtest runs **on the user's own machine, with the user's own key** (local-first, §3.4). A hosted multi-user backtester needs a **vendor licence** (§3.3) or a written broker answer. | M |
| **Paper trading** | **Expressly barred at two brokers.** The Kite terms prohibit "virtual/mock trading apps". The Fyers API terms say exchange data "shall not be used for… paper trading, gaming, and virtual trading purposes", and Fyers staff wrote (13 Sep 2024): "In compliance with regulations, Fyers does not support paper trading". **Broker sandboxes are a different thing:** they test integration and are not a licence to run a paper-trading product (§2.2). | **Paper trading on Kite or Fyers data is barred whether it is hosted or run locally.** Both clauses restrict the *type of use*, not where the code runs. It is viable only (a) on licensed vendor data, or (b) on a broker whose terms allow it. **None is confirmed yet:** Kotak and Dhan are pending Q-K-2 and Q-D-2. | H (Kite, Fyers clauses) / M (other brokers: terms not published) |
| **Automated trading for users** | If we place orders for other people's accounts, we are an **algo provider**. That requires NSE **empanelment** through a broker (the process takes about T+30 days), and each strategy must be **registered**. Kotak's static-IP page says [F]: fintech platforms must be "exchange empanelled" and "hosted on broker systems". The SEBI circular of 2 Sep 2022 stops brokers associating with platforms that claim past or expected algo returns (PaRRVA carve-out, §3.5). | **Not possible without a broker partner and empanelment.** For a platform that is **not empanelled**, the mechanics also block the workaround. Static IPs can be shared only with family (Kotak: up to 10 family members; Kite: immediate family). Kotak also requires that "the session must be created from the same IP that is sending order requests". So one cloud egress IP cannot carry many users' orders, even if each user brings their own key. **After empanelment this changes.** The Z-Connect overview says vendors "need their own static IP to connect to brokers, eliminating the need for individual users to have static IPs". Static IP therefore marks the **empanelment boundary**; it is not a permanent wall. **Conflict:** Kotak's page still says platforms must be "hosted on broker systems", while Zerodha said that line "will be revised out of the circular" (Q-K-3). | H (static-IP rules) / M (empanelment details; NSE PDFs unreadable) |

### 0.2 Kotak Neo in one paragraph
- **Cost and brokerage.** The API is free "at present". The Trade Free pricing page says there is **zero brokerage on all trades routed via the API**. That is the cheapest execution found. [F, M: "at present" means Kotak can revoke it.]
- **Data.** Quotes and historical data need **only the consumer key**, with no 2FA [F, M]. Historical data covers **1-minute to weekly candles from 1 Jan 2021**, with windows of 30 to 180 days per request [F, M]. The WebSocket allows **3,000 tokens per connection** and 200 per request [F, M].
- **SDK.** `kotakneoapi` 3.0.7 is MIT-licensed, still imports as `neo_api_client`, and was released 18 Sep 2026. The 3.x line **only shipped on 15 Aug 2026**. The v2 repository was archived on 10 Sep 2026. There are 4 open bugs with **no maintainer replies**, including persistent 429 errors on `historical_data()`. SDK maturity: **L**.
- **Gaps.** No public API terms of use were found. No partner programme was found. Session lifetime is undocumented.

### 0.3 Recommendation [P]
The separating constraint is **not** price. It is whether the broker has a **documented third-party route** that covers:
1. multi-user login;
2. use of data for backtesting and paper trading;
3. order placement under empanelment.

| Phase | Recommendation | Why |
|---|---|---|
| **Phase 0: owner-only prototype** (the owner trades their own account from their own static IP) | **Kite for historical data and research; Kotak Neo for execution.** Or Kotak alone if cost matters most | Kotak: free API, ₹0 brokerage on API orders, free 1-minute history back to 2021, and a UAT environment on request. Its drawbacks are an immature SDK and historical 429s that lasted hours. Kite (₹500/month): the most mature SDK and documentation, 1-minute history back to about 2015, and the best staff-answered forum. Personal use of each account is within its terms. **Do not build a paper-trading mode on Kite data, even for the owner's own use (the terms bar mock-trading apps).** |
| **Phase 1: multi-user product** | **Conditional, and decided by written vendor answers (§6).** On current evidence, **Dhan** (formal partner OAuth, a sandbox that needs no account, 5 × 5,000 WebSocket) or **Zerodha** (kite.trade/startups is free for mass-retail platforms, but approval is required) | These are the only brokers with a **published** multi-user or partner route besides Upstox. Upstox has UpLink Business, but applicants report no answers, and staff said "we do not provide market data for commercial purposes". Kotak has **no partner programme found**. |
| **All phases** | **Backtesting:** licensed vendor data (§3.3), or local-first with the user's own key (§3.4). **Paper trading:** licensed vendor data only, until a broker confirms in writing | Local-first keeps broker data off our servers, but it does **not** lift the Kite and Fyers bans on the paper-trading use. |

---

## 1. Kotak Neo Trade API

### 1.1 Price, brokerage and signup

| Item | Fact | Source | Conf. |
|---|---|---|---|
| API fee | "free of cost at present – i.e. no subscription charges" | [Trade API page](https://www.kotakneo.com/platform/kotak-neo-trade-api/) | H (repeated on several Kotak pages) |
| Brokerage on API orders | Pricing page: "Zero API Charges" and "Zero Brokerage on all Trades Routed via API". Press release (10 Nov 2025): zero brokerage and zero fee "across all its digital plans", **effective 1 Nov 2025**, for Trade Free plans. Covers CNC, MIS, NRML, CO, BO and AMO | [Trade Free plan](https://www.kotakneo.com/pricing/trade-free-plan/); [press release](https://www.kotakneo.com/about-us/media-and-press/kotak-neo-introduces-zero-brokerage-zero-fee-trade-apis-for-retail-traders/) | M/H |
| **Conflict** | The Trade API page says "₹0 brokerage on trade free plans" **for the first 30 days**. The pricing page says zero brokerage on **all** API-routed trades. Non-API orders on Trade Free after 30 days: intraday ₹10 or 0.05% (whichever is lower); delivery 0.20%; F&O ₹10 per order. Bracket orders: the square-off leg "will attract standard brokerage". **We cite the pricing page, and it goes on the vendor question list (Q-K-6)** | Trade API page vs pricing page | noted |
| Statutory charges | Exchange, SEBI, GST, STT and stamp duty apply separately | Trade API page | H |
| Signup | Any Kotak Neo trading-account holder. In the app go to Invest → Trade API → API Dashboard → "Create Application" to get a token (consumer key). Register TOTP (Google or Microsoft Authenticator). Register a static IP (for orders) | [API guide](https://www.kotakneo.com/investing-guide/trading-account/kotak-neo-trade-api-guide/); [static-IP page](https://www.kotakneo.com/platform/kotak-neo-trade-api/static-ip-details/) | M |
| Cost formula (owner self-use) [E] | `₹0 API + ₹0 brokerage (API-routed) + statutory charges + static-IP hosting (VPS or static-IP add-on, market price) ` | — | M |

**Stale source.** A Chittorgarh review page (updated 5 Jul 2024) says "brokerage as per your chosen plan". It predates the 1 Nov 2025 change. Do not cite it.

### 1.2 Authentication and session

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Credentials | The consumer key (token) from the API dashboard, plus mobile number, UCC (client code), TOTP and MPIN | [kotak-neo-python README](https://github.com/Kotak-Neo/kotak-neo-python); [totp_login.md](https://github.com/Kotak-Neo/kotak-neo-python/blob/main/docs/functions/authentication/totp_login.md) | H |
| Flow | 1. `totp_login(mobile, ucc, totp)` returns a **view token** (JWT, read-only), a `sid` and a `rid`.<br>2. `totp_validate(mpin)` upgrades it to a trade session.<br>3. The REST guide describes the result as TRADING_TOKEN, TRADING_SID and BASE_URL | same; API guide | H |
| **Data without 2FA** | `quotes()`: "unlike most trading/portfolio methods, `quotes()` does not require a completed 2FA (TOTP) session". `historical_data()` uses the "`Authorization: <consumer_key>` header (no 2FA required)" | [quotes.md](https://github.com/Kotak-Neo/kotak-neo-python/blob/main/docs/functions/market_data/quotes.md); [historical_data.md](https://github.com/Kotak-Neo/kotak-neo-python/blob/main/docs/functions/market_data/historical_data.md) | M |
| TOTP automation | The docs mention saving "the secret key from QR code" for automated TOTP generation, but give no official implementation | totp_login.md | M |
| **Session lifetime** | **Not documented** in the SDK or support pages that we read. AlgoTest's integration guide says "MPIN is required to generate the daily access token", which implies daily re-authentication [I]. A search snippet about "access token validity -2 = infinite" refers to a legacy API-manager setting. **Not used.** | [AlgoTest docs](https://docs.algotest.in/broker/kotakneo/) (third party) | L |
| Static IP | **Effective 1 Apr 2026** ("Optional until 1st April", "Mandatory after 1st April").<br>**Endpoints:** enforced on **Place, Modify and Cancel Order only**. Login, Report, Portfolio, Data and WebSocket APIs are exempt.<br>**Limits:** 2 IPs (a primary and a secondary fallback); changes once every 7 days; IPv4 only ("IPv6 support coming soon").<br>**Same-IP rule:** "The session must be created from the same IP that is sending order requests."<br>**Sharing:** up to **10 family members** may share one IP; this "does not give account access" | [static-IP page](https://www.kotakneo.com/platform/kotak-neo-trade-api/static-ip-details/); [FAQ](https://www.kotakneo.com/support/are-static-ips-mandatory/) | H (two Kotak pages agree) |
| Algo ID | "Algo ID appended automatically by the system" (under 10 OPS) | static-IP page | M |

### 1.3 Endpoints

| Area | Fact | Source | Conf. |
|---|---|---|---|
| Orders | Place, modify and cancel for regular orders and AMO. Order types: MKT, L, SL, SL-M. Products: CNC, MIS, NRML, CO, BO. `place_order(tag=…)` was added in 3.0.7. REST: `POST {BASE_URL}/quick/order/rule/ms/place` | README; [org profile](https://github.com/Kotak-Neo); API guide | H |
| Market orders | FAQ: set `pt` to `MKT`. The Trade API page says [F]: market orders "will be automatically converted into a limit order using a protection price". The static-IP page: "LTP-based protection ranges". A search extract [F-sec] says "market orders are not allowed for retail algo trading". **The direct FAQ URL returned 404** | [support: market order](https://www.kotakneo.com/support/how-do-i-place-a-market-order/); Trade API page; static-IP page | M (conversion) / L (the "not allowed" extract) |
| Portfolio | Holdings, positions, margins and limits. The Order Feed WebSocket carries order and position updates | README | H |
| Quotes (REST) | `GET /script-details/1.0/quotes/neosymbol/{exch}\|{token}[,…]/{quote_type}`. **50 instruments per call.** Types: `ltp`, `ohlc`, `market_depth` (**5 levels**), `oi`, `52w`, `circuit_limits`, `scrip_details`, `all`. **25 requests per second.** The docs state an average latency of 289 ms (250–350 ms) | quotes.md | M |
| Other market data | Scrip master (CSV file paths), search, `expiries()`, `option_chain()`; all added in 3.0.7 | org profile; [bulletin](https://www.kotakneo.com/bulletins/kotak-neo-trade-apis-just-got-more-powerful/) | M |
| WebSocket (market) | The new "Srishti" SFeed.<br>**Modes:** LTP (`subscribe_scrips`), lite quote, depth, **full depth**, index (by name, e.g. "Nifty 50", "SENSEX"), and market status (pre-open and closing auction).<br>**Limits:** "At most **3000 input tokens**… running total across all subscribe requests" per connection. The support FAQ says "A maximum of **200** scrips may be submitted per request". The two limits are compatible: 200 per request, 3,000 per connection.<br>**Undocumented:** the number of levels in "full depth", the connections per key, heartbeat and reconnect behaviour, and tick frequency | [market_feed.md](https://github.com/Kotak-Neo/kotak-neo-python/blob/main/docs/functions/websocket/market_feed.md); [support FAQ](https://www.kotakneo.com/support/what-is-the-maximum-number-of-scrips-which-can-be-subscribed-to-in-a-websocket-simultaneously/) | M |
| **Feed migration** | The legacy HS feed was **deprecated on 15 Sep 2026**: "After this date, the existing feed may no longer deliver market data". OpenAlgo's tracker says to upgrade to `kotakneoapi` ≥ 3.0.1 | [support: feed changes](https://www.kotakneo.com/support/kotak-neo-trade-api-market-feed-changes/); [openalgo #2010](https://github.com/marketcalls/openalgo/issues/2010) | H |

### 1.4 Historical data

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Endpoint | `GET market-data/1.0/historical/details`; `historical_data(neosymbol, interval, from_date, to_date)` | historical_data.md | M |
| Intervals | `1min, 3min, 5min, 10min, 15min, 30min, 60min, D, W` | same | M |
| Per-request window ("backend-enforced") | 1/3/5-min: **30 days**; 10/15-min: 60 days; 30/60-min: 90 days; daily and weekly: 180 days | same | M |
| Depth | "maximum up-to 5 years"; "available from **1st Jan 2021** onwards" | [support: how much history](https://www.kotakneo.com/support/how-much-historical-data-is-available-for-testing/) | M |
| Segments | "not available for the `mcx_fo` and `nse_com` exchange segments" | historical_data.md | M |
| Fields | `[timestamp, open, high, low, close, volume, oi]`, with ISO-8601 timestamps. **`oi` is "currently unpopulated"** | same | M |
| Rate limit | Shared with `quotes()`, but no number is stated for historical. **Issue #35 (21 Sep 2026, open, no staff reply):** 429 "too many request received" persisted for **more than 2 h 45 m** after the user cut load by about 90% and added a 3-minute backoff | same; [issue #35](https://github.com/Kotak-Neo/kotak-neo-python/issues/35) | M (C for the incident) |
| **Conflict** | The support page ["How do I get historical data"](https://www.kotakneo.com/support/how-do-i-get-historical-data/) says: "Historical data is unavailable at the moment. This feature is not allowed for this platform." The same "not allowed for this platform" line appears on the unrelated [What is the NEO Trade API](https://www.kotakneo.com/support/what-is-the-neo-trade-api/) page, so it looks like page boilerplate. The SDK docs (3.0.7) and the bulletin say historical data exists. **We treat the support page as stale [I, M]. The endpoint exists, but it is new and unreliable (issue #35 and v2 issue #70, which reported a 503 on an older `/charts/v1/scrip/history`)** | — | M |
| Cost | No charge found. The API as a whole is "free at present" | — | M |
| Check against the 06 §1 detector spec | Per exchange only, with no NSE+BSE merge. Volume is present, but its method is undocumented. 1-minute bars exist. **Displayable to other people: no licence found.** Verdict: owner research use only | — | [I, M] |

### 1.5 Rate limits (summary)

| Scope | Limit | Source | Conf. |
|---|---|---|---|
| Orders | "up to 10 orders per second" (SEBI 10 OPS); Kotak appends the algo ID | Trade API page; static-IP page | H |
| Quotes | 25 requests per second; 50 instruments per call | quotes.md | M |
| Historical | Shared with quotes; no number published; observed throttling that lasted hours | historical_data.md; issue #35 | M/L |
| Other endpoints | **Not published** | — | — |
| SDK limiter | An optional token bucket (per second, minute and hour), off by default. Mutating calls (place, modify, cancel) are never retried automatically | [PyPI](https://pypi.org/project/kotakneoapi/) | H |

### 1.6 SDK: `kotakneoapi` (import name `neo_api_client`)

**Software licence only (MIT). The licence grants no rights to the data.**

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Package | PyPI `kotakneoapi`; `from neo_api_client import NeoAPI`; Python ≥ 3.10; MIT | [README](https://github.com/Kotak-Neo/kotak-neo-python); [PyPI](https://pypi.org/project/kotakneoapi/) | H |
| Releases | 3.0.0 (15 Aug 2026), 3.0.1 (17 Aug), 3.0.5 and 3.0.6 (5 Sep), **3.0.7 (18 Sep 2026)** | PyPI | H |
| Repo health | 13 stars, 3 forks, **4 open issues, all opened 12–22 Sep 2026, none with a maintainer reply**:<br>#32 carry-forward positions omit the average price;<br>#35 historical 429s;<br>#37 "Order Feed Disconnect Continues" on 3.0.7;<br>#38 order-processing delay | [issues](https://github.com/Kotak-Neo/kotak-neo-python/issues) | H (as of access date) |
| Legacy | `Kotak-neo-api-v2` (v2.0.2, installed from git; the import is also `neo_api_client`) was **archived on 10 Sep 2026**, with 87 stars and 63 open issues left unresolved. The LICENSE file URL returned 404, so its licence is **unverified**. The original `kotak-neo-api` repo returns 404 | [v2 repo](https://github.com/Kotak-Neo/Kotak-neo-api-v2) | H / L (v2 licence) |
| Features | HTTP/2 with HTTP/1.1 fallback; async WebSocket; structured JSON logs with secrets masked; a Jupyter guide; a sync-integration guide for Django, Flask and Celery | README; org profile | M |
| **Assessment [I]** | The feature set is modern, but the SDK has **five weeks of production history**, the WebSocket has just been migrated, and maintainers do not respond on issues. Pin exact versions, wrap the SDK behind our own adapter, and budget for breakage. | — | **L maturity** |

### 1.7 Terms: the three layers kept apart

| Layer | What we found | Conf. |
|---|---|---|
| Software licence | `kotakneoapi` is MIT. It covers the code only | H |
| API terms | **No public Trade API terms of use were found.** The Kotak Neo [disclaimer](https://www.kotakneo.com/disclaimer/) has no API, data or redistribution clauses. The terms may only be shown in the app at activation [A]. **Not used:** `api.kotak.com` and `api.kotak.bank.in` belong to **Kotak Mahindra Bank's** API platform, a different legal entity from Kotak Securities | H (that none was found) |
| Data rights (display, storage, derived data, redistribution, exports) | **Unverified.** The exchange rights sit with NSE and BSE in any case. The default inference [I, M]: as at Zerodha, Upstox and Fyers, Kotak grants personal use only | L |
| Multi-user / third-party / partner programme | **None found.** The only related statement is on the static-IP page [F]: fintech platforms must be "exchange empanelled" and "hosted on broker systems" to offer algo trading to retail users | M |
| Practice (not a precedent) | AlgoTest, OpenAlgo, OptionX and Stocks Developer integrate Kotak Neo. **AlgoTest's docs ask users to enter their Client ID, phone number, TOTP and MPIN on AlgoTest's page** [F-sec]. **[I] That is a credential-handling risk we must not copy.** Holding a user's MPIN and TOTP seed makes us custodian of full trade access | M |

### 1.8 Sandbox / UAT
- Kotak says to "send your UserID… to ks.apihelp@kotak.com" (or your UCC to neo.api@kotak.com) "and they'll provide login information" for UAT or paper trading. See [support: UAT](https://www.kotakneo.com/support/how-can-i-get-access-to-uat-environment-paper-trading-environment-to-test-the-apis/). [F-sec from the search extract; M]
- **Scope is unknown:** whether UAT has live or simulated market data, simulated fills, or historical data (Q-K-7).

### 1.9 Community reliability evidence

| Theme | Evidence | Conf. |
|---|---|---|
| Static-IP cutover | After 1 Apr 2026, bots stopped with timeouts until the IP was registered | [QuotaGuard blog](https://www.quotaguard.com/blog/kotak-neo-api-static-ip) (vendor marketing) L |
| Forced feed migration | The HS feed was deprecated on 15 Sep 2026 at about four weeks' notice after 3.0.1 shipped. Downstream platforms had to scramble ("URGENT" in OpenAlgo) | openalgo #2010, M |
| Order-feed disconnects | These persist on 3.0.7 (#37). There is also an order-processing delay report (#38) | C, M |
| Historical throttling | 429s for hours (#35) | C, M |
| Credential errors | "Incorrect combination of credentials" even with correct inputs (search extract) | L |
| Latency marketing | "under 50ms", "independently audited" (Trade API page). There is no public audit and no independent measurement | F (claim) / L (as a fact) |

---

## 2. Nine-broker comparison for a backtest, paper-trade and auto-trade product

### 2.1 Main table

All data rights are **for the account holder's own use** unless stated. "Unverified" means we read no primary source. Brokerage is quoted before GST and statutory charges.

| Broker | API cost | Brokerage (intraday / F&O options) | Historical: depth, minute data, cost | WebSocket limits | Order rate limits | Algo framework: algo ID and static IP | Partner programme for third-party platforms | Python SDK | Conf. |
|---|---|---|---|---|---|---|---|---|---|
| **Zerodha Kite Connect** | Personal: free (no data). Connect: ₹500/app/month. Free for approved mass-retail platforms | 0.03% or ₹20 / flat ₹20; delivery ₹0 [F: [charges](https://zerodha.com/charges/)] | 1-min from about 2015, daily from the late 1990s; 60 days per 1-min request; included in the ₹500 | 3,000 instruments × 3 connections; 5-level depth; about 1 snapshot per second | 10/s, 400/min, 5,000/day; 25 modifications per order | Static IP 1 Apr 2026, orders only; 2 IPs, immediate family only; market orders need `market_protection` | **kite.trade/startups** (free for mass retail, approval by compliance). Terms bar "virtual/mock trading apps" | pykiteconnect 5.2.2, MIT, 15 Sep 2026: **best** | H (see Kite report) |
| **Kotak Neo** | Free "at present" | **₹0 on API-routed trades** (Trade Free) | 1-min from 1 Jan 2021 (about 5 years); 30 days per 1-min request; free; no MCX; OI empty | 3,000 tokens per connection, 200 per request; 5-level quote depth; "full depth" levels unknown | 10 OPS; quotes 25/s | Static IP 1 Apr 2026, orders only; 2 IPs; ≤10 family members; same-IP session; algo ID automatic | **None found**; platforms must be "exchange empanelled… hosted on broker systems" | kotakneoapi 3.0.7, MIT, **3.x is 5 weeks old**; issues unanswered | M |
| **Upstox** | Free (trading and data) | ₹20 or 0.1% / flat ₹20; delivery ₹20 [F: [brokerage page](https://upstox.com/brokerage-charges/)]. API offer of ₹10/order: the pricing page says "valid till 31 Dec 2025", but the Kite report cites a trading-API page saying 30 Sep 2026. **Conflict** | Minutes from Jan 2022; daily from 2000; 1-month window for 1–15 min; free | 2 connections (5 with Plus); LTPC 5,000, Full 2,000, D30 50 | Orders 10/s unregistered; 50/s, 500/min, 2,000/30 min per API | Static IP, orders only | **UpLink Business** multi-client (email onboarding; applicants report no replies). Staff: "we do not provide market data for commercial purposes" | upstox-python-sdk 2.30.0, MIT, 7 Sep 2026 (classifiers stale: "2.7/3.4+") | M/H |
| **Dhan** | Trading free; **Data API ₹499/month** | 0.03% or ₹20 / ₹20; delivery ₹0 [F-sec: Chittorgarh; primary [pricing](https://dhan.co/pricing/) not fetched] | Daily since inception; intraday 1/5/15/25/60-min, 90-day window, about 5 years back; expired options endpoint | 5 connections × 5,000 instruments; 200-level depth in SDK 2.2.0 | 10/s, 250/min, 1,000/h, 7,000/day (docs; marketing says 25/s) | Static IP, orders only; IP management in the SDK | **Formal partner OAuth** (partner_id/secret, consent); lists smallcase and TradingView | dhanhq 2.2.0, MIT, 24 Apr 2026 (**breaking changes** vs 2.0.2) | M/H |
| **Fyers** | Data free | 0.03% or ₹20 / ₹20 (Prime: ₹15 for ₹499/month); delivery 0.3% or ₹20 [F: [pricing](https://fyers.in/pricing/), M] | 100 days per request for minute resolutions; 366 days for daily; total depth unverified | ≤5,000 symbols per connection; TBT 3 × 5 symbols | 10/s, 200/min, 100k/day; >3 per-minute breaches a day blocks the account for the day | Static IP. Reportedly **disabled third-party platform orders from 1 Apr 2026** (L) | Platforms allowed "after obtaining the required approvals". **Terms bar data use for charting, technical tools and paper trading** | fyers-apiv3 3.1.18, MIT, 17 Sep 2026: good | H (terms) / M |
| **Angel One SmartAPI** | Free | ₹20 or 0.1% / flat ₹20 (₹0 up to ₹500 for the first 30 days) [F: [charges](https://www.angelone.in/exchange-transaction-charges), M] | Intervals 1-min to 1-day; about 30 days per request at 1-min [C]; depth "decades" daily (Kite report) | 3 connections per client; 1,000 tokens | 10 OPS; getCandleData 3/s, 180/min; **false 429s reported** | Static IP 1 Apr 2026 for self-coded algos | "Publisher login"; data terms unverified | smartapi-python 1.5.5, **7 Feb 2025**; classifiers Py 2.7–3.7; licence not stated: **stale** | M |
| **Shoonya (Finvasia)** | Free "for eligible users" | ₹5 or 0.03% / flat ₹5; delivery ₹0 (was ₹0 on everything until 16 Dec 2024) [F-sec] | "Time series" endpoint; depth and window unverified | Unverified | Unverified | Static IP (secondary source: IPv6 static IP at ₹100/month) | None found | ShoonyaApi-py: **proprietary** ("Copying… strictly prohibited"), 57 open issues; the PyPI NorenRestApiPy 0.0.22 is by a third party (quantplay), last released **Dec 2022**, and also proprietary: **weakest** | L/M |
| **ICICI Breeze** | Free, including historical data | Plan-based (unverified) | **1-second** bars: "3 years" (site) vs "10 years" (PyPI description). **Conflict.** Also 1 min, 5 min, 30 min, 1 day. NSE only | Streaming OHLC; limits unverified | 100 calls/min and 5,000/day general; **orders 75/min and 5,000/day** | Static IP from 1 Apr 2026. **Market orders prohibited; "aggressive limit orders" instead** (PyPI) | None found | breeze-connect 1.0.69, MIT, 14 Apr 2026 | M |
| **Groww** | **₹499 + GST per month** (early bird; ₹2,000 standard per the Kite report) | ₹20 or 0.1% (min ₹5) equity; F&O: the fetch returned "₹50 per order" [L, needs re-check] | **From 2020** for equities, indices and F&O; 1–5 min: 30 days per request; 10–30 min: 90 days; hourly to monthly: 180 days. But the main page says "up to 3 months". **Conflict** | 1,000 subscriptions | Two conflicting sets: orders 10/s and 250/min (SDK intro) vs 15/s, 250/min and 3,000/day (search extract) | Static IP unverified. TOTP flow says "No Expiry", which **conflicts with the NSE daily-logout rule** | None found | growwapi 1.5.0, MIT, 6 Dec 2025 | M/L |

Sources beyond the Kite report:
- Groww: [python-sdk](https://groww.in/trade-api/docs/python-sdk), [backtesting](https://groww.in/trade-api/docs/curl/backtesting), [pricing](https://groww.in/pricing).
- Breeze: [breeze page](https://www.icicidirect.com/futures-and-options/api/breeze), [PyPI](https://pypi.org/project/breeze-connect/).
- Shoonya: [apis](https://shoonya.com/apis), [ShoonyaApi-py](https://github.com/Shoonya-Dev/ShoonyaApi-py), [NorenRestApiPy](https://pypi.org/project/NorenRestApiPy/).
- Fyers: [history limits](https://fyers.in/community/t/limit-in-history/13457) (F-sec).
- SDKs on PyPI: [dhanhq](https://pypi.org/project/dhanhq/), [fyers-apiv3](https://pypi.org/project/fyers-apiv3/), [smartapi-python](https://pypi.org/project/smartapi-python/), [upstox-python-sdk](https://pypi.org/project/upstox-python-sdk/), [growwapi](https://pypi.org/project/growwapi/).

### 2.2 The sandbox question: two different things

| Broker | (a) Developer sandbox or UAT (tests integration) | (b) May a third-party **paper-trading product** use this broker's data? |
|---|---|---|
| Zerodha | **None.** Staff (Apr 2026): "Kite Connect does not provide a dedicated sandbox environment"; build "a 'paper trading' or dummy execution layer within your application", or test with an unfunded live account. Mock sessions are held on some Saturdays ([forum 15978](https://kite.trade/forum/discussion/15978/query-regarding-paper-trading-support-via-zerodha-apis)) [F, H] | **No.** The terms prohibit "virtual/mock trading apps" [F, H] |
| Kotak | UAT **on request by email**; scope unknown [F-sec, M] | Unverified (no public terms; Q-K-2) |
| Upstox | **Yes.** Order APIs only (place, modify and cancel, v2/v3, multi-order). The token lasts **30 days**. **One sandbox app per user.** Available 24/7. Market data in the sandbox is not documented ([sandbox](https://upstox.com/developer/api-documentation/sandbox/)) [F, M] | Unverified. Staff: "no market data for commercial purposes" [F, M] → [I] probably no |
| Dhan | **Yes.** "No KYC needed", no Dhan account needed, no static IP needed in the sandbox; the DevPortal is at developer.dhanhq.co ([Marketcalls](https://www.marketcalls.in/algo-trading/dhan-sandbox-kickstart-your-algo-trading-journey-with-risk-free-testing.html), [madefortrade](https://madefortrade.in/t/introducing-dhanhq-sandbox-and-devportal-for-api-based-traders-builders/50426)) [F-sec, M]. The official sandbox docs page did not render its content | Unverified (Q-D-1 in the Kite report, to be extended) |
| Fyers | **None.** Staff: "In compliance with regulations, Fyers does not support paper trading" (13 Sep 2024) [F, H] | **No.** The terms bar "paper trading, gaming, and virtual trading purposes" [F, H] |
| Angel, Shoonya, Breeze, Groww | None found | Unverified |

**[I, H] A sandbox is an integration tool.** Even where one exists, it gives no licence to run a paper-trading product on the broker's live data.

---

## 3. Cheap, legal historical data for backtesting

### 3.1 Is broker historical data allowed for users' own backtests on our platform?

| Pattern | Analysis | Verdict |
|---|---|---|
| **(A) Our servers pull the user's broker history and show backtest results** | Kite: "A third-party app can't show our data". The terms also bar derivative works and caching "with the intent of redistributing" (Kite report §1.7). Upstox: no commercial market data. Fyers: bars "technical tools" and paper trading, and caching needs written consent. Kotak, Dhan, Angel, Breeze, Groww: no public clause found. **[I, M]** A backtest equity curve is a **derived work** computed from broker data and shown by a third party. | **Do not build without written consent** (Q-K-2, Q-Z-5, Q-D-2) |
| **(B) Shared historical cache across users** | Kite bars it explicitly. The NSE policy says members and subscribers "shall not… redistribute any Market Data, except as agreed" [F-sec] | **Never** |
| **(C) Local-first: our open-source or desktop engine runs on the user's machine with their own key** | Data goes from the broker to the user's own machine. This is the Kite terms' "private interface exclusively for customising personal trading". We never receive the data. Leak risks (Kite report §8c) apply: no telemetry of prices, and no upload of results that contain prices. | **Most defensible for backtesting and display [I, M].** It does **not** cure use-type bans: Kite ("virtual/mock trading apps") and Fyers ("paper trading") still apply to a local paper-trading mode |
| **(D) Licensed vendor history on our servers** | The only pattern that fits a hosted, shared backtester. It needs a vendor licence that permits display to our users (§3.3) | **Product path** |

### 3.2 NSE bhavcopy and NSE website data

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Website terms | Use only "by individuals for personal, non-commercial use". "Systematic or automated data collection activities (including scraping, data mining, data extraction and data harvesting)" are prohibited | [NSE terms of use](https://www.nseindia.com/static/nse-terms-of-use) (**search extract; the page returned ECONNRESET**) | M/L |
| Data policy | "Trading Members and Subscribers shall not be permitted to redistribute any Market Data, except as agreed…". Commercial-purpose data "shall be provided by NSE Data at a price approved by its Board" | [NSE data policy](https://www.nseindia.com/static/market-data/nse-data-policy); [policy PDF](https://nsearchives.nseindia.com/web/sites/default/files/inline-files/NSE_DataUsageandSharingPolicy.pdf) (timed out; extract) | M/L |
| Historical data product | NSE sells historical data through a "Historical data web" service at dotexdata.nseindia.com under separate terms ([terms PDF](https://dotexdata.nseindia.com/TermsAndConditions/TermsofUse.pdf); ECONNRESET). **Prices unread** | — | L |
| **Reading [I, M]** | Bhavcopy is fine for the **owner's personal research**, downloaded by hand. **A product must not auto-download bhavcopy (scraping ban) or serve it to users (commercial use and redistribution).** The product route is NSE Data licensing or an authorised vendor. Bhavcopy is also EOD only, so it cannot support intraday backtests | — | M |
| Third-party tools | Getbhavcopy and Samco-style downloaders exist. Their existence is **not** a licence | — | [I] |

### 3.3 Vendor options (lowest tiers; personal vs commercial)

| Vendor | Lowest tier and history | Personal vs commercial | Source | Conf. |
|---|---|---|---|---|
| **TrueData** | Velocity: Lite ₹1,439.83/month, Standard ₹1,949, Optima ₹2,288, Ultima ₹2,795.83 (per segment). Up to 10% off for a year. **"Velocity plans do not include API access."** API history: **tick for the last 5 trading days; 1–60-min bars for 6 months; daily bars 10+ years**; "Extended History" add-on is "coming" (no price) | Terminal and charting use by a single subscriber. API needs "a separate application, compliance review, and approval". Display to clients needs written approval from the exchanges and TrueData (Kite report) | [price](https://www.truedata.in/price); [REST history](https://feedback.truedata.in/knowledge-base/article/historical-data-availability-through-rest-api) | H (plans) / M (history) |
| **Global Datafeeds (GFDL)** | Pricing "tailored" (sales). Minute data retention: **1–5-min for about 3 months; 5–10-min for about 4.5 months**; daily for longer | "charting / analysis use of a single subscriber only"; product display negotiated | [api-pricing](https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/pricing-sales/api-pricing/); [type of data](https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/introduction/type-of-data-available/) | M |
| **Accelpix** | ₹1,599–3,499/month | "strictly… personal, non-commercial use" (Kite report) | accelpix.com/pricing | H |
| **TickData (US)** | NSE equities from 2 Jan 2012: tick trades, L1 quotes and 1-min bars; quote-only | Institutional research licence | [tickdata.com](https://www.tickdata.com/equity-data/national-stock-exchange-of-india) | M |
| **LSEG / Refinitiv** | NSE history from as early as 1994; quote-only | Enterprise | [lseg.com](https://www.lseg.com/en/data-analytics/financial-data/pricing-and-market-data/equities-market-data/national-stock-exchange-india) | M |
| Kaggle and GitHub dumps (for example "Nifty 50 minute data 2015–2026") | Free | **Provenance and licence unknown** → never use in the product, fixtures or demos [I, H] | kaggle.com | — |

**[I, M] Vendor retail minute history is shallow** (TrueData 6 months, GFDL 3–4.5 months). The **broker APIs are deeper** (Kite about 2015; Groww 2020; Kotak 2021; Upstox 2022; Breeze 1-second data for 3 or more years) and free, **but only for personal use**. Multi-year, commercially licensed minute history is a **quote-only** purchase (NSE Data, TickData, LSEG, or a TrueData extended-history add-on).

**Cost formulas [E]**
- Owner-only research: `₹0 (Kotak) or ₹500/month (Kite)`. Everything stays on the owner's machine.
- Hosted multi-user backtester: `vendor_history_licence (quote) + NSE_licence(category) + vendor_display_fee(users) + storage`. **All inputs are unknown until quoted.** Retail plans (TrueData Velocity, Accelpix) are **not** valid inputs.
- Local-first bring-your-own-broker: `₹0 to us for data`. The user pays their own broker fee (₹0 at Kotak, ₹500/month at Kite, ₹499/month at Dhan data or Groww).

### 3.4 What "each user brings their own broker data" means

| Dimension | Legally | Practically |
|---|---|---|
| **Hosted** (the user gives us their key or consent token, and our servers call the broker) | We become the "third-party app" that Kite staff said cannot show broker data. Placing orders makes us an algo provider, which needs empanelment. Holding MPIN, TOTP seeds or api_secret brings DPDP and security duties, and possible SEBI scrutiny | Static IP: **while we are not empanelled, we cannot share one egress IP across unrelated users** (Kotak: ≤10 family members, and the session must come from the order IP; Kite: immediate family). Once we are empanelled, we register our own vendor static IP (Z-Connect). Every user must log in daily (Kite 6 AM expiry; Kotak daily MPIN, inferred). Per-user rate limits (Kotak historical throttling; Kite 3/s) |
| **Local-first** (our engine or desktop app runs on the user's machine) | The user runs a private interface on their own account, which is within personal use. For orders, the user is "tech-savvy retail" with their **own** static IP and ≤10 OPS, so no empanelment is needed **only if the user writes the strategy logic and our code is just a library** [I, **L**]. Angel defines the exemption as "self-coded algorithms or strategies whose logic resides at the client's end". A no-code builder or shipped strategies probably make us the algo provider even if the code runs locally (Q-NSE-8). **Open:** whether distributing strategy templates makes us an "algo provider" (the Z-Connect overview says "If you're just a coder-for-hire, you do not need any registrations"; black-box strategies need a SEBI Research Analyst registration [F-sec]) | The user needs their own static IP for live orders (home broadband rarely has one; a VPS or static-IP add-on). We never see the data, so there is no shared cache and no server-side analytics on prices. Support is harder |

### 3.5 Returns claims (flag for compliance-analyst)
- **The 2022 circular.** SEBI's circular of 2 Sep 2022 bars stock brokers from "directly or indirectly" referring to "the past or expected future return/performance of the algorithm". It also bars them from associating "with any platform providing any reference" to such returns. Sources: the [SEBI circular](https://www.sebi.gov.in/legal/circulars/sep-2022/performance-return-claimed-by-unregulated-platforms-offering-algorithmic-strategies-for-trading_62628.html) and the [NSE/COMP/60341](https://nsearchives.nseindia.com/content/circulars/COMP60341.pdf) circular. [F, M: SEBI page title plus extracts]
- **Later carve-out.** Claims verified by **PaRRVA** are exempt ([Medianama](https://www.medianama.com/2025/04/223-sebi-parrva-guidelines-updates-algo-trading-rules/), secondary, M).
- **[I, M]** Showing a user **their own** backtest of **their own** strategy is not the same as marketing strategy returns. Leaderboards, "top strategies by CAGR", or marketing copy with backtested returns would put our broker partners at risk. **Route this to the compliance-analyst.**

---

## 4. Order-execution realities

| Topic | Fact | Source | Conf. |
|---|---|---|---|
| **Market orders via API** | **Kite:** from 1 Apr 2026, market and SL-M orders need a non-zero `market_protection` ("-1" = automatic, or 1–100 %), otherwise "Market orders without market protection are not allowed via API". pykiteconnect v5.1.0 lacked the parameter (issue #225), and the docs call it optional although live orders require it (issue #242). **Kotak:** market orders "automatically converted into a limit order using a protection price" (LTP-based). **Breeze:** market orders prohibited; use "aggressive limit orders" | [Kite orders docs](https://kite.trade/docs/connect/v3/orders/); [forum 15912](https://kite.trade/forum/discussion/15912/preparing-to-comply-with-sebis-retail-algo-rules-static-ip-ratelimits-order-types) (staff); [#242](https://github.com/zerodha/pykiteconnect/issues/242); Kotak Trade API page; Breeze PyPI | H (Kite) / M |
| **Design rule [P]** | The order layer must **never send bare market orders**. Always send a limit or protected order with an explicit protection %. Treat an order as unfilled until the broker confirms a fill (protected orders can rest unfilled or be cancelled in fast moves) | — | — |
| **NSE Limit Price Protection (LPP)** | The exchange rejects limit orders outside the LPP band. Futures: ±3%. Options with premium > ₹50: ±40%; premium < ₹50: ±₹20. Stop-loss limit orders: both the trigger and the limit must be inside the band. The band flexes after ≥10 rejections involving ≥5 UCCs and ≥3 members. **[I, M] Once brokers turn market orders into protected limit orders, LPP applies to them too.** A wide market_protection % can still be rejected by LPP | [NSE LPP FAQ](https://www.nseindia.com/static/trade/limit-price-protection-faqs) (via search extract); [Zerodha LPP error](https://support.zerodha.com/category/trading-and-markets/alerts-and-nudges/kite-error-messages/articles/price-out-of-lpp-range) | M (figures F-sec) |
| **Freeze quantities** | An order above the freeze limit is **rejected**, not partly filled. Reported from 1 Sep 2026: NIFTY 50 and FINNIFTY 1,800; BANKNIFTY and NIFTY NEXT 50 600; MIDCPNIFTY 2,800; NIFTY India FPI 150 8,500 units. Limits were also revised on 1 Jan and 2 Mar 2026. **Revised often → read them from the exchange circular or instrument master; never hardcode** | [Choice](https://choiceindia.com/news/nse-fo-quantity-freeze-limits-september-2026), [Angel](https://www.angelone.in/news/market-updates/nse-announces-revised-quantity-freeze-limits-for-index-derivatives-from-march-2-2026) (secondary) | M (values F-sec) |
| Slicing | Kite `autoslice=true` splits orders above the freeze limit into **at most 10 slices**. Iceberg orders: 2–50 legs. Each slice counts toward the 10 OPS limit | Kite orders docs | H |
| **10 OPS** | Above 10 orders per second the extra orders get a 429. Kite staff: "10 orders will be placed, and 5 orders will be blocked" (for 15 sent). The limit is per client ID across all apps. Groww: 250 per minute. Breeze: **75 orders per minute** | forum 15912; broker docs | H |
| **Latency** | **No independent measurements found for any broker.**<br>Kite forum (C): placeOrder round trips of about 150 ms rising to more than 500 ms; about 450 ms reported; staff: "not meant for latency-based strategies", with no guaranteed timeline.<br>Kotak: quotes average 289 ms (SDK docs); "<50 ms" execution (marketing).<br>Kite ticks: 800 ms–1 s (one user) | [forum 9594](https://kite.trade/forum/discussion/9594/what-is-order-latency-of-kite-api), [5309](https://kite.trade/forum/discussion/5309/kite-api-call-takes-more-time-than-usual); Kotak docs | L/M |
| **Slippage** | **No primary measurements. No number is estimated here.** [I] Contributors: 1-second L2 snapshots (a signal is about 1 s stale); a round trip of 150–500 ms; protected-limit conversion; LPP rejections; partial fills on illiquid strikes | — | — |
| Common rejections [I, M from docs and forums] | Missing market protection; LPP band; freeze quantity; price outside the circuit band; insufficient margin (RMS); the order was not sent from the whitelisted IP, or the session was created from a different IP (Kotak); the daily session expired; 429 above 10 OPS; the API modification cap (Kite: 25 per order) | Kite report; this report | M |
| **Backtest realism [P]** | The backtester must model: the fill price being worse than the signal price (configurable slippage in bps and ticks); protected-limit non-fills; freeze-quantity splitting and the ≤10 OPS pacing; LPP bands for options; brokerage + STT + exchange + SEBI + GST + stamp duty per broker; and the 1-minute bar revision caveat (Kite about 30 s). Label results "simulated" and never show them as returns claims (§3.5) | — | — |

---

## 5. Check against the detector spec (06 §1)

This spec matters less now. The new product is execution-first rather than a watchlist detector, but the invariants in CLAUDE.md still apply.

| Feed | Consolidated | Full volume | 1-min bars | Displayable to other users | Verdict |
|---|---|---|---|---|---|
| Kotak Neo | No (per exchange) | Unknown method | Yes (from 2021) | No licence found | Owner or local-first only |
| Dhan / Upstox / Groww / Breeze | No | Snapshot (unverified) | Yes | No / unverified | Same |
| Licensed vendor | Yes | Vendor-dependent | Yes | With written approval | Product path |

Every broker-sourced bar must carry `source=<broker>` and entitlement `real-time` or `delayed`, **plus a licence scope tag `personal-use`** so that it can never reach a shared cache (invariant 7). [P]

---

## 6. Vendor questions (exact text; for the user to send; answers not guessed)

**Kotak Securities (ks.apihelp@kotak.com / neo.api@kotak.com)**
- **Q-K-1 (terms):** "Please send the current Terms of Use that govern the Neo Trade API, including any clauses on market-data display, storage, derived data, and redistribution. Are these terms published anywhere outside the app?"
- **Q-K-2 (third-party backtesting and paper trading):** "May a third-party platform, with the Kotak client's consent, call `historical_data()` and quotes for that client and show that same client backtest results or a simulated (paper) portfolio computed from that data? May the platform store the candles on its servers, and for how long? May it cache them across clients?"
- **Q-K-3 (partner route):** "Does Kotak Securities offer a partner or multi-client programme for exchange-empanelled algo providers? If yes, what are the onboarding requirements, fees or revenue share, and is the platform hosted on Kotak systems as your static-IP page says ('hosted on broker systems')?"
- **Q-K-4 (session):** "How long is a Neo Trade API session valid after `totp_validate`? Is there a refresh mechanism, and must the client re-enter MPIN and TOTP every trading day?"
- **Q-K-5 (data limits):** "What are the rate limits for `historical_data()` and for non-order endpoints? How many connections may one consumer key open to the Srishti market feed, and how many levels does 'full depth' carry?"
- **Q-K-6 (pricing durability):** "Is 'Zero Brokerage on all Trades Routed via API' on Trade Free plans permanent or time-limited? The Trade API page mentions 'first 30 days'. Which applies after 30 days?"
- **Q-K-7 (UAT):** "Does the UAT environment include live or simulated market data, simulated fills, and historical data? Can it be used by an algo provider for integration testing on behalf of multiple clients?"

**Zerodha (kiteconnect@zerodha.com)**; adds to Q-Z-1 to Q-Z-4 in the Kite report
- **Q-Z-5:** "An approved platform may let clients backtest their own strategies. May the platform fetch the client's historical candles via Kite Connect and show the client the backtest output? Does the 'virtual/mock trading apps' prohibition cover a paper-trading mode inside an execution platform that is otherwise approved?"

**Dhan (apihelp@dhan.co)**; extends Q-D-1 in the Kite report
- **Q-D-2:** "For a partner onboarded via partner_id/partner_secret: may we (a) fetch a consenting user's historical data and show them backtest results, (b) run a paper-trading mode on live Data API quotes for that user, and (c) place orders as an NSE-empanelled algo provider using your partner route? Does your sandbox provide market data and simulated fills?"

**Upstox (api@upstox.com)**
- **Q-U-2:** "Is the ₹10 per order API brokerage offer still active after 31 Dec 2025? Does the Upstox sandbox include market data, or only order APIs?"

**NSE (via the broker, or the NSE algo desk)**
- **Q-NSE-8:** "Does a platform that only provides backtesting and strategy-building tools, where the client's own machine places orders under the client's own static IP, need algo-provider empanelment? Does distributing white-box strategy templates change the answer?"

---

## 7. Unverified list

1. Kotak Trade API terms (none public); Kotak data rights; Kotak partner programme.
2. Kotak session lifetime; WebSocket connections per key; full-depth levels; historical rate limit.
3. Kotak brokerage conflict: "first 30 days" vs "all API trades".
4. Kotak historical support page ("unavailable") vs SDK docs. Treated as stale.
5. Kotak UAT scope (data and fills).
6. Kotak v2 SDK licence (LICENSE 404).
7. Kotak "<50 ms, independently audited" claim.
8. Kotak "market orders not allowed" (search extract only; FAQ URL 404).
9. Upstox API offer end date (31 Dec 2025 vs 30 Sep 2026).
10. Dhan brokerage (secondary); Dhan sandbox docs (not rendered).
11. Groww F&O brokerage (₹50 fetched; likely a misread); Groww rate-limit sets; Groww "3 months" vs "from 2020".
12. Breeze 1-second history: 3 years vs 10 years.
13. Shoonya limits, history and brokerage (secondary).
14. Angel per-interval windows (community only).
15. NSE terms of use, data policy, historical-data product terms and prices (all unreadable); the NSE retail-algo FAQ (3 Nov 2025) and INVG/73992 empanelment criteria (unreadable).
16. Freeze-quantity values and LPP percentages (secondary).
17. Order latency and slippage (no independent measurement).
18. Whether distributing strategy templates or backtest tools triggers empanelment (Q-NSE-8).

---

## 8. Sources (all accessed 2026-09-24)

**Kotak Neo / Kotak Securities**
- https://www.kotakneo.com/platform/kotak-neo-trade-api/
- https://www.kotakneo.com/platform/kotak-neo-trade-api/static-ip-details/
- https://www.kotakneo.com/pricing/trade-free-plan/
- https://www.kotakneo.com/about-us/media-and-press/kotak-neo-introduces-zero-brokerage-zero-fee-trade-apis-for-retail-traders/ (10 Nov 2025)
- https://www.kotakneo.com/bulletins/kotak-neo-trade-apis-just-got-more-powerful/
- https://www.kotakneo.com/investing-guide/trading-account/kotak-neo-trade-api-guide/
- https://www.kotakneo.com/disclaimer/
- Support pages:
  - https://www.kotakneo.com/support/are-static-ips-mandatory/
  - https://www.kotakneo.com/support/what-is-the-maximum-number-of-scrips-which-can-be-subscribed-to-in-a-websocket-simultaneously/
  - https://www.kotakneo.com/support/how-much-historical-data-is-available-for-testing/
  - https://www.kotakneo.com/support/how-do-i-get-historical-data/
  - https://www.kotakneo.com/support/what-is-the-neo-trade-api/
  - https://www.kotakneo.com/support/how-do-i-place-a-market-order/
  - https://www.kotakneo.com/support/kotak-neo-trade-api-market-feed-changes/
  - https://www.kotakneo.com/support/how-can-i-get-access-to-uat-environment-paper-trading-environment-to-test-the-apis/ (search extract)
- GitHub and PyPI:
  - https://github.com/Kotak-Neo
  - https://github.com/Kotak-Neo/kotak-neo-python (README, docs/functions/*, issues #32 #35 #37 #38)
  - https://github.com/Kotak-Neo/Kotak-neo-api-v2 (archived 10 Sep 2026; issue #70)
  - https://pypi.org/project/kotakneoapi/
- Third party:
  - https://docs.algotest.in/broker/kotakneo/
  - https://github.com/marketcalls/openalgo/issues/2010
  - https://www.quotaguard.com/blog/kotak-neo-api-static-ip
  - https://www.chittorgarh.com/broker/kotak-securities/api-for-algo-trading-review/12/ (stale, 2024)

**Other brokers**
- Zerodha:
  - https://zerodha.com/charges/
  - https://kite.trade/docs/connect/v3/orders/
  - https://kite.trade/forum/discussion/15978/query-regarding-paper-trading-support-via-zerodha-apis
  - https://kite.trade/forum/discussion/15912/preparing-to-comply-with-sebis-retail-algo-rules-static-ip-ratelimits-order-types
  - https://kite.trade/forum/discussion/9594/what-is-order-latency-of-kite-api
  - https://kite.trade/forum/discussion/5309/kite-api-call-takes-more-time-than-usual
  - https://github.com/zerodha/pykiteconnect/issues/242
  - https://github.com/zerodha/pykiteconnect/issues/225
  - https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework
- Upstox:
  - https://upstox.com/brokerage-charges/
  - https://upstox.com/developer/api-documentation/sandbox/
  - https://pypi.org/project/upstox-python-sdk/
- Dhan:
  - https://docs.dhanhq.co/api/v2/sandbox
  - https://pypi.org/project/dhanhq/
  - https://www.marketcalls.in/algo-trading/dhan-sandbox-kickstart-your-algo-trading-journey-with-risk-free-testing.html
  - https://madefortrade.in/t/introducing-dhanhq-sandbox-and-devportal-for-api-based-traders-builders/50426
  - https://www.chittorgarh.com/brokerage_charges/dhan/176/
- Fyers:
  - https://fyers.in/pricing/
  - https://fyers.in/community/t/paper-trading-environment-for-fyers-api/13412
  - https://fyers.in/community/t/limit-in-history/13457
  - https://pypi.org/project/fyers-apiv3/
- Angel One:
  - https://www.angelone.in/exchange-transaction-charges
  - https://pypi.org/project/smartapi-python/
  - https://smartapi.angelone.in/smartapi/forum/topic/4845/max-days-in-historical-data
- Shoonya:
  - https://shoonya.com/apis
  - https://github.com/Shoonya-Dev/ShoonyaApi-py
  - https://pypi.org/project/NorenRestApiPy/
  - https://comparesharebrokers.com/review/finvasia
- ICICI Breeze:
  - https://www.icicidirect.com/futures-and-options/api/breeze
  - https://pypi.org/project/breeze-connect/
- Groww:
  - https://groww.in/trade-api
  - https://groww.in/trade-api/docs/python-sdk
  - https://groww.in/trade-api/docs/curl/backtesting
  - https://groww.in/pricing
  - https://pypi.org/project/growwapi/

**Exchanges, regulators, vendors**
- NSE:
  - https://www.nseindia.com/static/nse-terms-of-use (extract)
  - https://www.nseindia.com/static/market-data/nse-data-policy (extract)
  - https://nsearchives.nseindia.com/web/sites/default/files/inline-files/NSE_DataUsageandSharingPolicy.pdf (timed out)
  - https://dotexdata.nseindia.com/TermsAndConditions/TermsofUse.pdf (ECONNRESET)
  - https://www.nseindia.com/static/trade/limit-price-protection-faqs (extract)
  - https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAQ_Retail%20Algo_03112025_NSE.pdf (timed out)
  - https://www.nseindia.com/static/trade/empanelled-algo-providers-exchange
- SEBI and exchange circulars on returns claims:
  - https://www.sebi.gov.in/legal/circulars/sep-2022/performance-return-claimed-by-unregulated-platforms-offering-algorithmic-strategies-for-trading_62628.html
  - https://nsearchives.nseindia.com/content/circulars/COMP60341.pdf
  - https://www.medianama.com/2025/04/223-sebi-parrva-guidelines-updates-algo-trading-rules/
- Freeze limits and LPP (secondary):
  - https://choiceindia.com/news/nse-fo-quantity-freeze-limits-september-2026
  - https://www.angelone.in/news/market-updates/nse-announces-revised-quantity-freeze-limits-for-index-derivatives-from-march-2-2026
  - https://support.zerodha.com/category/trading-and-markets/alerts-and-nudges/kite-error-messages/articles/price-out-of-lpp-range
- TrueData:
  - https://www.truedata.in/price
  - https://feedback.truedata.in/knowledge-base/article/historical-data-availability-through-rest-api
- Global Datafeeds:
  - https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/pricing-sales/api-pricing/
  - https://globaldatafeeds.in/global-datafeeds-apis/global-datafeeds-apis/introduction/type-of-data-available/
- Other historical-data vendors:
  - https://www.tickdata.com/equity-data/national-stock-exchange-of-india
  - https://www.lseg.com/en/data-analytics/financial-data/pricing-and-market-data/equities-market-data/national-stock-exchange-india
