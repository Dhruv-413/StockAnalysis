# Fast, cheap build on Kotak Neo / Zerodha Kite: platforms, engines, stack and costs

Author: tech-scout (Research squad). **Access date for every URL and registry read: 2026-09-24.** Read-only: nothing was installed or downloaded. Registry facts come from the PyPI JSON API (`https://pypi.org/pypi/<name>/json`) and the GitHub REST API (`gh api repos/...`). This is not legal advice.

**Labels**
- **[F]** a primary-source fact (registry, vendor page or licence file);
- **[F-sec]** a secondary source or a search extract;
- **[I]** an inference;
- **[E]** an estimate.

Confidence is H, M or L. The rate is ₹88 = $1, as in `docs/production-plan/17-what-is-achievable.md`. Costs exclude GST unless stated.

**What this report does not repeat.** The following are already covered, and this report only cites them:
- tech-radar rows for NautilusTrader, vectorbt, PyBroker, Backtesting.py and the Kite/Indian SDKs;
- `kite-and-broker-apis.md` (Kite pricing, static IP, 10 OPS, the display bar);
- `feature-legality.md` (rows 1, 17, 24 and 27);
- `data-stack-costs.md` (NSE licence tariffs);
- `build-cost-latency.md` (Mumbai hosting).

---

## 0. Gates to clear before any of the stack is "buildable"

The owner's new direction runs into four gates that the existing appendices already establish. The stack below is only as buildable as these gates allow.

| # | Gate | Status today | Consequence |
|---|---|---|---|
| G1 | **Order placement is banned by the project rules.** `CLAUDE.md` says "never execute trades or add order-placing code", and feature-legality row 24 marks auto-trading as legal posture **C**, project **D** | A change of direction relayed by an agent is **not** approval | Needs an **ADR amending the CLAUDE.md hard rule** and the owner's own sign-off before any order-routing code is written. Until then, build only backtest, paper and learning features |
| G2 | **Paper trading on live LTP is the case the appendices flag.** Feature-legality row 1 says "no paper trading or virtual portfolios (vendor and S10 risk)". The Fyers API terms ban exchange data for "paper trading, gaming and virtual trading". SEBI's 24 May 2024 circular (S10) targets sharing real-time prices for virtual trading | **The Kite terms explicitly list "virtual/mock trading apps, trading related games" as a prohibited use** (kite-and-broker-apis §3, "Prohibited uses") | **Paper trading on Kite data is out in both modes.** A paper-trading app that we distribute is a "virtual/mock trading app" even when the user hosts it [I, M-H]. What remains: paper trading on **Kotak** data (terms unread, unverified) or on **licensed** delayed or EOD data, with the S10 risk still open |
| G3 | **Kite data may not pass through our servers** without Zerodha's multi-login or startup approval ("A third-party app can't show our data"; kite-and-broker-apis §0) | Blocked until Zerodha replies in writing (Q-Z-1) | Every design must say which **mode** it assumes (below) |
| G4 | **SEBI retail-algo framework (mandatory from 1 Apr 2026).** A hosted platform that runs strategies for retail clients is an **algo provider**. It must be empanelled with each broker, use exchange algo IDs, and whitelist a static IP for order APIs. Black-box logic needs RA registration (feature-legality S11). IT-system interaction counts as "association" (S8) | Not obtained | Hosted automated trading is a **regulated set-up**, not an 8-week build |

**Two delivery modes.** Every recommendation below is labelled with the mode it assumes.
- **Mode A: hosted SaaS.** Our servers log in to users' broker accounts, run their strategies and show data. Needs G1, G3 (Zerodha platform approval or Kotak's written equivalent), G4 (empanelment) and a licensed data feed for anything displayed. **Months of approvals, not weeks.**
- **Mode B: per-user, self-hosted personal tool.** This is OpenAlgo's model: "single user per deployment... self-hosted on the user's own server... no SaaS component" [F, OpenAlgo CLAUDE.md].
  - The user runs our software on their own PC or VPS, with their own broker API keys and static IP.
  - Data stays between the broker and the user.
  - Our servers sell only licences, content, courses and community. None of them touch market data.
  - This is the **only route that can ship in 8 weeks** [I, M].
  - **Not cleared for Kite.** The Kite personal-use clause covers a client who "develops a private interface" themselves. Staff have said "a third-party app can't show our data". An app that *we* wrote and distribute is arguably that third-party app, even with no data on our servers. **Mode B on Kite is pending Zerodha's written answer (CQ-new-4).** OpenAlgo has operated this way publicly since 2024, but that is precedent, not permission.
  - Residual risks:
    - **(i)** If our cloud pushes strategies or signals into the user's runner, SEBI may still treat us as an algo provider or "associated" (S8, S11). This is a counsel question (CQ-new-1).
    - **(ii)** Distributing code to users triggers GPL and AGPL obligations (§2).

**Static IP is a hosting criterion.**
- Order endpoints need a whitelisted static IP: at most 2, changed at most once a week (Kite). Kotak also requires whitelisting [F, kotakneo.com Trade API page].
- In mode B the IP belongs to the user.
- In mode A the order router must sit on a VM with a dedicated IP (§4.3). Whether **one shared IP may serve many client IDs** is **unverified**. Ask each broker (CQ-new-2).

**Backtest data rights decide cost more than the engine choice does.** NSE scraping libraries are on Hold (radar). The real options are:
- **Mode B:** the user's own broker historical API, used without storing it on our side:
  - Kite requires the ₹500/mo Connect plan per user;
  - Kotak Neo's SDK lists "historical candle data" and the API is "free at present" (terms unverified).
- **Mode A:** a licensed feed. The NSE EOD display licence is ₹1 L/yr (≈ ₹8.3k/mo), plus the vendor's fee (data-stack-costs row 1a). Note that SEBI's 8 May 2026 circular sets a 30-day lag for price data used for education (feature-legality S9).

---

## 1. Open-source Indian algo platforms

| Candidate | What it is / relevance | Licence (software) | Data rights | Maintenance [F] | Fit / verdict | Conf. |
|---|---|---|---|---|---|---|
| **OpenAlgo** (marketcalls/openalgo) | Self-hosted trading platform: unified broker REST API (`/api/v1`), Python strategy host with IST schedules, no-code "Flow" builder, options tools, AI agent, **"API Analyzer" sandbox with ₹1 crore virtual capital** (MARKET/LIMIT/SL/SL-M, margins, square-off schedules, separate DB) | **AGPL-3.0** (License.md). No CLA found in CONTRIBUTING.md. With 1,275 forks and many contributors, relicensing is impractical [I] | Uses the user's own broker session; single user per deployment | 2,721 stars; pushed 2026-09-24; created 2024-02-19; latest tag `openalgo-openscript-chart-alerts` 2026-09-22; 315 open issues | **36 broker plugins, including `kotak` and `zerodha`** (also dhan, upstox, angel, fyers, groww, shoonya, flattrade, fivepaisa, iifl, motilal, hdfcsky, paytm, zebu and others) | H |
| ↳ OpenAlgo architecture | Flask 3 + Flask-SocketIO under **eventlet with a mandatory single worker (`-w 1`)**, **no asyncio**. ZeroMQ market-data bus (port 5555) → WebSocket proxy (8765). **SQLite: 5 DBs** (main, logs, latency, health, sandbox). React 19 + Vite + shadcn + xyflow frontend. LiteLLM agent | — | — | — | Designed as single-tenant, and the eventlet/SQLite/single-worker design does **not** scale to multi-tenant SaaS without a rewrite [I, H] | H |
| ↳ Can it go inside a commercial SaaS? | **No, not as closed source.** AGPL §13 requires offering the source of the modified program to every network user. Copying its broker adapters into our proprietary code makes our code a derivative work | — | — | — | **Learn from it; don't embed it.** Safe patterns [I, M; counsel]: (1) the user runs **unmodified** OpenAlgo on their own VPS and our separate app calls its HTTP API with the **MIT** `openalgo` PyPI SDK (2.0.5, 2026-09-11, author Rajandran R, homepage openalgo.in, which matches the vendor). An HTTP boundary between separate programs is generally not a derivative work. (2) Clean-room our own adapters from the brokers' official SDK docs. **Don't paste OpenAlgo code into the repo** | M |
| **Official SDKs** | `kiteconnect` 5.2.2 (2026-09-15, MIT, Zerodha Technology) — on the radar already. **Kotak: the official SDK is now `kotakneoapi` 3.0.7 (2026-09-18, MIT, author "Kotak Neo <support@kotakneo.com>", repo Kotak-Neo/kotak-neo-python).** The old `Kotak-Neo/Kotak-neo-api-v2` repo is **archived** (legacy, git-installed `neo_api_client`). The new SDK: TOTP login, async SFeed WebSocket, HTTP/2 via httpx, option chain, historical candles, Python ≥ 3.10 | MIT | Broker terms (personal use by default) | Active | **Use the official SDKs only.** Kotak API is "free of cost at present"; ₹0 brokerage on Trade API orders; 10 orders/s; "<50 ms" (vendor claim, "independently audited", method not published) | H (registry) / M (Kotak terms) |
| **jugaad-trader** | "Reverse engineered API for Zerodha": logs in to Kite **with the user's password and PIN** through a CLI and reuses the web session | **No licence file** (GitHub `license: null`; PyPI blank) → all rights reserved | Bypasses Kite Connect → breaches Zerodha terms and SEBI's "no open APIs / client-specific API key" rule | 0.20, 2025-12-19; 167 stars; PyPI author "jugaad-coder <abc@xyz.com>" (placeholder email) | **Hold (hard).** Credential handling, ToS breach, no licence | H |
| **AlgoMojo** | Commercial Indian bridge service (paid), with a thin Python client | `algomojo` 1.4 (PyPI, MIT, **2023-03-25**); GitHub repo `algomojo/algomojo-python` returns 404 | Vendor's own terms (not read) | Client stale since 2023 | Hold as a dependency. It is a paid third-party bridge, which adds another party to the algo-provider chain | M |
| **LEAN brokerage plugins** (new relative to the radar) | QuantConnect **Lean.Brokerages.Zerodha** (Apache-2.0, 25 stars, pushed 2026-09-24) and **Lean.Brokerages.Samco** (Apache-2.0). No Kotak plugin found | Apache-2.0 | Broker terms | Active | Gives LEAN an Indian live path, but LEAN is C#-first (Python via pythonnet) and heavy for 1–2 Python developers. **Assess** | H (metadata) |
| Community "Kotak Neo algo" repos | e.g. danny8806/Kotak-Neo-Algo, ashishchauhan0416-lgtm/algotrade-pro | Mostly **no licence** | — | 0–1 stars | Not reusable (no licence); learning only | H |

---

## 2. Backtesting engines: licences and commercial use

How GPL and AGPL bite, stated explicitly:
- **GPL-3** (backtrader, fastquant) is **not** triggered by running it server-side only (mode A). It **is** triggered in mode B: if we ship an app to users that bundles or links it, the whole app must be offered under the GPL.
- **AGPL-3** is triggered in both modes: network use counts.
- **Commons Clause** bars selling a product "whose value derives entirely or substantially" from the software. That covers paid hosting, whatever the mode.
- **PolyForm Noncommercial** bars any commercial use.

| Engine | PyPI name (verified) | Latest release [F, PyPI] | Licence [F] | GitHub | Mode A (hosted, closed) | Mode B (we distribute) | Notes | Conf. |
|---|---|---|---|---|---|---|---|---|
| backtrader | `backtrader` | 1.9.78.123, **2023-04-19** | GPL-3.0+ | 23.3k stars; last push **2024-08-19**; no GitHub releases | OK legally, but **unmaintained** | **Trap (GPL)** | Event-driven, mature API, but dead upstream | H |
| Backtesting.py | `backtesting` (author Zach Lûster = kernc; homepage matches) | 0.6.6, 2026-07-22 | **AGPL-3.0** | 9.0k stars; active | **Trap** | **Trap** | Radar: Hold in product | H |
| vectorbt (OSS) | `vectorbt` | 1.1.0, 2026-07-05 | **Apache-2.0 + Commons Clause** (LICENSE text verified; GitHub shows NOASSERTION) | 9.2k stars | **Trap** (paid product) | **Trap** | Internal research only | H |
| zipline-reloaded | `zipline-reloaded` | 3.1.1, 2025-07-19 | Apache-2.0 | 1.9k stars; last push 2026-01-06 | OK | OK | Daily-bar, bundle-centric, US-calendar legacy; heavy to adapt to NSE; slowing maintenance | H |
| **bt** | `bt` | **1.2.3, 2026-09-12** | **MIT** | 3.0k stars; pushed 2026-09-24 | **OK** | **OK** | Portfolio/rebalancing "algo stack" backtests; weak for intraday order-level logic | H |
| **ffn** | `ffn` | 1.2.2, 2026-09-17 | **MIT** | 2.7k stars | OK | OK | Performance statistics (Sharpe, drawdown, calendar tables). **Reuse for metrics** | H |
| NautilusTrader | `nautilus_trader` (also `nautilus-trader`, same project) | 1.231.0, 2026-08-02 | LGPL-3.0+ | 29.4k stars | OK as a library | OK if dynamically linked and replaceable (LGPL) | **No Indian broker adapter**; steep learning curve | H |
| LEAN | `lean` on PyPI is the **CLI** (1.0.229, 2026-08-28, Apache) | Engine: GitHub QuantConnect/Lean (Apache-2.0, 21.8k stars, active) | Apache-2.0 | — | OK | OK | Zerodha and Samco plugins (§1); C#/.NET runtime | H |
| PyBroker | **`lib-pybroker`** (2.0.1, 2026-08-28). **`pybroker` does not exist on PyPI: a squatting risk; never `pip install pybroker`** | — | **Apache-2.0 + Commons Clause** (PyPI: "Free for non-commercial use") | 3.5k stars | **Trap** | **Trap** | — | H |
| fastquant | `fastquant` | 0.1.8.1, **2023-01-04** | GitHub says MIT, but the **PyPI classifier says GPLv3**, and it wraps backtrader → **treat as GPL** | 1.8k stars; last push 2023-09 | OK legally but stale | **Trap** | Abandoned | H |
| fast-trade (Polars) | — | — | **AGPL-3.0** | 597 stars; active | **Trap** | **Trap** | Polars-based, low-code | H |
| polars-backtest | `polars-backtest` 0.1.7 (2026-07-05) | — | **PolyForm Noncommercial 1.0.0** | Yvictor/polars_backtest_extension (13 stars) | **Trap** | **Trap** | — | H |
| AlphaPurify (Polars) | — | — | MIT | 552 stars; 2026-07 | OK | OK | Factor research, not order simulation | M |
| Ziplime (Polars Zipline) | `ziplime` 1.19.16 (2026-06-18) | — | **Licence blank on PyPI; repo not found** | — | Unverified | Unverified | Keep off until the licence is known | L |
| quantstats | `quantstats` 0.0.81 (2026-01-13) | — | Apache-2.0 | — | OK | OK | HTML tear sheets (depends on yfinance for some helpers: never call those in product) | M |

**Write it ourselves in under 2 weeks (1 developer) [E, M].** Scope:
1. A **vectorised Polars bar backtester** (≈ 3–4 days):
   - signals → target positions → fills at the **next bar's open** (no look-ahead);
   - per-trade Indian cost model (§3);
   - lot sizes;
   - long/short;
   - MIS square-off time;
   - returns, equity and drawdown.
2. A **simple event-driven loop** over bars for intraday, stop and target logic (≈ 3 days). It uses the same cost and fill functions as the paper engine, so backtest and paper stay at parity.
3. **Metrics** via `ffn` (MIT) plus our own golden tests (≈ 1 day).
4. A **calendar** from `exchange_calendars` XBOM (≈ 0.5 day). Check that NSE and BSE holidays match, and don't use weekday arithmetic (invariant 4).
5. **Golden-fixture and property tests**, plus `/financial-validation` (≈ 2 days).

**Out of scope for 2 weeks:**
- tick or queue-position simulation;
- SPAN/exposure margin for multi-leg options;
- corporate-action-adjusted history (this needs the versioned CA table in invariant 3);
- walk-forward optimisation UI.

**Recommendation:** own engine (MIT/Apache dependencies only) + `ffn` + `bt` for portfolio-style strategies. This avoids every licence trap in both modes.

---

## 3. Paper trading and simulators for Indian markets

**What exists.**
- **OpenAlgo's API Analyzer / sandbox** is the only mature India-specific simulator found (AGPL; single-user; learn from it, §1).
- Every GitHub hit for "paper trading zerodha / NSE simulator" is a toy: 0–6 stars, and most have **no licence**. Examples: amey1907/modular-paper-trading-engine, xeonee/tradeSim, madhug9/zerodha-paper-intraday.
- **No reusable, licensed engine exists. Build one** [F, H for the search; I for the conclusion].

**Legal reminder (G2).**
- **Never on Kite data:** the Kite terms prohibit "virtual/mock trading apps".
- Candidates, all pending: the user's own **Kotak** session (terms unread) or licensed delayed/EOD data.
- Don't host a public "virtual portfolio" game.
- Build the engine anyway, because it is the same fill and cost code that the backtester needs for parity.

**Design for our own engine (≈ 4–5 days) [P]**

| Element | Rule |
|---|---|
| Market order | Fill at the **next received LTP** ± slippage. Default is `max(1 tick, k × spread)` when depth is available, else a fixed bps by liquidity bucket. Kite WS is ~1 snapshot per second (kite-and-broker-apis §0 #5), so fills are approximate: label them "simulated" |
| Limit order | A buy fills when LTP ≤ limit (a sell when LTP ≥ limit). Option: a "strict" mode that requires a trade *through* the limit by 1 tick (conservative) |
| SL / SL-M | Trigger on LTP crossing, then treat as a limit or market order. Market orders are auto-converted to limit orders at some brokers per SEBI rules (Kotak page): mirror this |
| Constraints | F&O lot size and freeze quantity; price bands and circuit limits (reject); tick size; MIS auto square-off time (broker-specific, e.g. ~15:20; configurable); the 10 orders/s limit enforced in the simulator too |
| Costs | A dated, versioned cost table (below). Record the source URL and effective date per row |
| Audit | Every simulated fill stores the LTP, `event_ts`/`ingest_ts` (UTC, tz-aware), source and entitlement (invariant 1) |

**Cost model, NSE rates [F, zerodha.com/charges, 2026-09-24]**

| | Equity delivery | Equity intraday | Futures | Options |
|---|---|---|---|---|
| Brokerage (Zerodha) | ₹0 | 0.03% or ₹20/order, whichever is lower | 0.03% or ₹20 | Flat ₹20/order |
| Brokerage (Kotak Neo "Trade Free") | 0.20% (Trade Free) / 0.10% (Pro ₹249/mo) | ₹10 or 0.05%, whichever is lower | ₹10 | ₹10. **₹0 on Trade API orders** (vendor claim) |
| STT/CTT | 0.1% buy & sell | 0.025% sell | **0.05% sell** | **0.15% on the sell premium**; 0.15% of intrinsic value on exercised long options |
| NSE transaction charge | 0.00307% | 0.00307% | 0.00183% | 0.03553% on premium |
| SEBI fee | ₹10/crore | same | same | same |
| Stamp duty (buy side) | 0.015% | 0.003% | 0.002% | 0.003% |
| GST | 18% on (brokerage + SEBI + transaction charges) | same | same | same |
| DP charge (sell, delivery) | ₹15.34 per scrip (Zerodha) | — | — | — |

- **F&O STT effective date: 1 Apr 2026** (Budget 2026, announced 1 Feb 2026). Futures went from 0.02% to 0.05%; options went to 0.15% [F-sec, H: ICICI Direct, HDFC Securities note, Cleartax].
- **BSE transaction charges were not collected** (unverified).
- The Kotak brokerage figures come from kotakneo.com/pricing on the second fetch [F, M: extracted by the summariser].

---

## 4. The fastest, cheapest full stack for 1–2 developers

### 4.1 Application stack

| Layer | Recommendation | Registry facts [F] | Why / alternatives | Mode |
|---|---|---|---|---|
| API / backend | **FastAPI** on Python 3.12 (radar: Adopt) | `fastapi` 0.141.1, 2026-07-29, MIT | Keeps the existing codebase and team skills. Start from **fastapi/full-stack-fastapi-template** (MIT, 45.7k stars, release 0.12.0 on 2026-08-12): FastAPI + SQLModel + Postgres + React/Vite + Docker Compose + auth | A & B |
| DB | **Postgres**: Supabase (Mumbai `ap-south-1` available) or DO Managed PG BLR1. In mode B, SQLite or DuckDB on the user's box | `supabase` 2.31.0, MIT | Radar: Postgres is Adopt. Supabase adds Auth, Storage and Realtime in one bill | A (Supabase) / B (SQLite) |
| Analytics | **Polars + DuckDB** (radar: Adopt) | `polars` 1.44.2, 2026-09-09, MIT | Bar storage in Parquet; backtests run in-process | A & B |
| Frontend | **React + Vite + shadcn/ui + TradingView lightweight-charts** (from the template) | shadcn/ui MIT (124.5k stars); lightweight-charts **Apache-2.0**, v5.2.1 on 2026-08-12 (**keep TradingView's attribution notice**) | Next.js is fine too, but it adds SSR complexity nobody needs here. **HTMX** (0BSD, 49.5k stars) is quickest for a Python-only developer, but is weaker for live charts and a PWA | A & B |
| MVP-only UI | **Streamlit** (1.64.0, 2026-09-15, Apache-2.0) for internal and prototype dashboards only. **Reflex** (0.9.12, 2026-09-22, Apache-2.0) is a possible single-language option | — | Streamlit's per-session rerun model and thin auth make it poor for a multi-user paid product [I, M]. Reflex compiles to React (Assess) | Internal |
| Mobile | **PWA first** (installable, web push). Flutter or React Native only after product-market fit | — | One codebase. App-store review of trading/finance apps adds weeks and possibly policy declarations (unverified) | A & B |
| Scheduler / jobs | **APScheduler** 3.11.3 (2026-06-28, MIT) for IST cron triggers, run in a single leader process (Postgres advisory lock). **procrastinate** 3.10.0 (2026-09-23, MIT; a Postgres-backed queue) for jobs. **DBOS** 3.0.0 (2026-09-16, MIT; radar Adopt) for durable, audited order workflows once G1 clears | — | Celery + Redis is heavier; Temporal is overkill (radar: Assess) | A & B |
| Fan-out | **SSE from FastAPI** (radar: Adopt) for per-user updates. **Centrifugo** (Apache-2.0, v6.9.6 on 2026-09-14; radar: Trial) above ~1k concurrent connections. Supabase Realtime: 500 concurrent / 5M messages on Pro | `python-socketio` 5.17.0, MIT (if bidirectional) | In mode B, fan-out is local and trivial | A |
| Broker adapters | Our own thin interface over **`kiteconnect`** and **`kotakneoapi`**, or the user's own **OpenAlgo** via the MIT `openalgo` SDK (mode B) | above | No AGPL code in our tree | A & B |
| Auth | **Supabase Auth** (included: 50k MAU free / 100k on Pro, then $0.00325/MAU). Alternative: **Clerk** (free up to 50k MRU per app; Pro $25/mo or $20/mo billed annually; $0.02/MRU for 50,001–100k) | — | Prefer Google + email magic-link login. **Indian SMS OTP needs TRAI DLT sender registration** (unverified in this pass); defer phone OTP | A |
| Payments | **Cashfree** or **Razorpay** (§4.4) | `razorpay` 2.0.1 (2026-03-09, MIT); `cashfree-pg` 6.0.1 (2026-05-18, Apache-2.0) | Both official. **PyPI `htmx` 0.0.0 (2023) is unrelated to htmx: never install it** | A |

### 4.2 AI coding speedups

- **Templates [F].**
  - Start from **fastapi/full-stack-fastapi-template**, MIT, active.
  - `wasp-lang/open-saas` (MIT, 16k stars) and `nextjs/saas-starter` (MIT, 16.1k stars; last push 2025-12) are JS-first; skip them for a Python team.
  - `vercel/nextjs-subscription-payments` is **archived**.
- **Claude Code practice for 1 developer [P].**
  1. Use this repo's role subagents with **path-scoped ownership**, e.g. `backend-engineer` on `app/api`, `data-engineer` on `app/data`, and `quant-researcher` plus `financial-correctness-reviewer` on `app/backtest`.
  2. Write **golden fixtures first** (recorded broker JSON, never live calls), then let agents implement against the tests (`/plan-task` → `/verify-change`).
  3. Use the context7 docs server for current SDK APIs (`kotakneoapi` 3.x changed its API from v2).
  4. Use **anthropics/claude-code-action** (MIT, 8.9k stars, active) for PR review in CI once a remote exists.
  5. Keep the ADR gate: any agent touching order routing must hit a failing check until ADR-G1 is merged.
- `Trade-With-Claude/cbt-framework` (MIT, 71 stars) and `rahulcommercial/claude-code-for-indian-traders` (MIT, 2 stars) are low-signal references. Read them; don't depend on them.

### 4.3 Hosting (India latency, static IP, price)

| Host | India region? [F] | Static egress IP for broker order APIs [F] | Price [F] | Verdict |
|---|---|---|---|---|
| **DigitalOcean BLR1** | Yes (Bengaluru) | **Yes.** A droplet's public IPv4 is static; a Reserved IP can be moved between droplets (in-region latency to Mumbai brokers is unmeasured) | Basic droplets: 1 GB $6, **2 GB $12**, 4 GB $24, 8 GB $48 /mo. Managed PG from **$15.15/mo** (1 GiB/1 vCPU/10 GiB); managed Valkey from $15/mo. BLR1 price parity not stated | **Recommended for the pilot** (and for a mode-A order router) |
| **Oracle Cloud Mumbai (Always Free)** | Yes (Mumbai, Hyderabad) | Yes (reserved public IP) | $0 within Always Free. **Conflict:** the docs now say **1,500 OCPU-h / 9,000 GB-h ≈ 2 OCPU + 12 GB for Always Free tenancies**, while build-cost-latency.md quotes 3,000 / 18,000 (probably the PAYG-tenancy figure). **Always Free only exists in the home region, which is chosen once.** **Idle instances are reclaimed** if 95th-percentile CPU, network and memory all stay < 20% for 7 days. "Out of host capacity" errors happen | **Dev/staging only.** The reclamation rule and capacity errors make it unfit for an order router |
| **Fly.io** | **Yes: `bom` (Mumbai).** But `bom` lacks Fly Gateway and **Managed Postgres (MPG)** | App-scoped static egress IPv4 **$3.60/mo** per IP per region [F-sec, search extract of Fly docs] | Pay as you go | Viable for app servers. The DB must live elsewhere (e.g. Supabase Mumbai) |
| **Railway** | **No.** Nearest is Singapore (`asia-southeast1`) | Static outbound IPs on Pro only, **may be shared with other customers** | Hobby $5 (incl. $5 usage); Pro $20/workspace (incl. $20); ~$20/vCPU-mo, ~$10/GB-mo RAM, $0.05/GB egress | Not for order routing (shared IP, SG region). Fine for non-trading web |
| **Render** | **No.** Nearest is Singapore | Shared regional ranges by default; dedicated outbound IPs available as an add-on (price not read) | Free tier: spins down after 15 min; free PG **expires after 30 days** | Not recommended |
| Supabase | Mumbai `ap-south-1` | n/a (DB/auth) | Free: 500 MB DB, 50k MAU, pauses after 1 week idle. **Pro $25/mo**: 8 GB disk, 100k MAU, 250 GB egress, $10 compute credit (Micro), 7-day backups | Recommended DB + auth for mode A |

**Frontend hosting.**
- Cloudflare Pages (free) or the same droplet behind Caddy.
- **Vercel Hobby is limited to non-commercial use** [I, M: from memory; re-check before choosing]. Vercel Pro costs $20 per user per month.

### 4.4 Payments

| Gateway | Standard fee [F] | Setup / AMC | Recurring | Notes |
|---|---|---|---|---|
| **Razorpay** | **2% platform fee** on cards, UPI, netbanking and wallets (UPI is "zero MDR", but the 2% platform fee applies); international up to 3% | ₹0 / ₹0 | Card recurring 0.9% + platform fee; UPI AutoPay/NACH "on request" | Effective cost with 18% GST on the fee: **2.36%** |
| **Cashfree** | **1.95%** on domestic cards; UPI "as per applicable law"; international 2.99% | ₹0 | Card mandate ₹7.5 creation + ₹7.5 per presentation; UPI AutoPay ₹7.5 + ₹5 (<₹1,000) or + ₹15 | **Promo: 0% fees on the first ₹20 lakh GMV, valid to 2027-03-31.** Model 1.95% (2.30% with GST) after that |

- **Unverified blocker.** Neither gateway's restricted-business list for "stock tips, investment advisory, algo subscriptions" could be read (Razorpay's docs URL returned 404).
- Onboarding may ask for SEBI registration if the product looks like advice or signals. Ask both gateways' sales teams before building checkout (CQ-new-3).

---

## 5. Creator / course / community stacks (One-Percent-style features)

**Compliance first.** Feature-legality row 27 applies:
- education is posture A;
- a named security with price data needs **data at least 30 days old** (SEBI circular of 8 May 2026, effective 1 Jul 2026);
- "education" that includes calls is unregistered advice (the Sathe and Patel orders).
- No strategy-return marketing (S12).

**Platform comparison** [F, vendor pricing pages]. Commission is shown **at an assumed GMV of ₹1 L/mo**; GST is excluded.

| Platform | Fixed fee | Commission | Cost at ₹1 L/mo GMV [E] | Branded app | Fit |
|---|---|---|---|---|---|
| **Exly** | Starter ₹0; Pro ₹2,500/mo (₹30k/yr); Premium ₹9,000/mo | 10% / 6% / 3% | Starter ₹10,000; **Pro ₹8,500** | Add-on from ₹60k/yr | Good Indian creator fit (UPI, WhatsApp) |
| **TagMango** | Basic ₹0; Pro ₹5,000/mo; Advanced ₹15,000/mo; Ultimate ₹30,000/mo | 10% / 5.5% / 3.5% / 0% (+1.5% gateway) | Basic ₹10,000; Pro ₹10,500 | ₹74,999–1,00,000 one-time | Community and webinars built in |
| **Graphy** | Launch ₹1,999/mo billed annually (₹24,999/yr); Grow ₹49,999/yr; Rise ₹99,999/yr | 10% / 7.5% / 5% (min ₹10) | Launch ≈ ₹12,000 | Android on Launch/Grow; iOS from Rise | Strong LMS; live classes |
| **Teachable** | Starter $39 ($29 annual); Builder $89 ($69); Growth $189 ($139) | 7.5% / 0% / 0% (with teachable:pay) | Starter ≈ ₹2,550 + ₹7,500 | Student iOS/Android apps on all plans | USD billing; weaker UPI/India fit [I] |
| **Circle** | Professional $89; Business $199; Scale $419 | 2% / 1% / 1% | Professional ≈ ₹7,830 + ₹2,000 | Branded app only on Circle Plus (custom price) | Best community UX; pricey at pilot scale |
| **Discord** | Free | 0% (sell access through our own gateway plus a role bot) | Gateway 2.36% ≈ ₹2,360 | n/a | Cheapest community; moderation load; no LMS |
| **In-house** | Our infra (already paid) | Gateway only (2.30–2.36%) | ≈ ₹2,300–2,400 + **~1.5–2 dev-weeks** to build course pages, progress and quizzes | PWA | Best integration with backtest and paper "labs" |

**Recommendation.**
- **Weeks 1–8:** Exly Starter or Pro, or Graphy Launch, **plus Discord**. That costs nothing to engineer and keeps developers on the core product.
- **Later:** move courses in-house once GMV exceeds ~₹3–5 L/mo. At that point the platforms' commissions exceed the build cost [E].

---

## 6. Recommended stack

**Ranked recommendation (for 1–2 developers, small budget, 8 weeks)**

1. **Mode B first: the "personal trading workstation" [H on licences; M/L on regulatory fit, with Kite pending CQ-new-4 and paper trading barred on Kite data].**
   - **Runtime and stack:** Python 3.12 + FastAPI + SQLite/DuckDB + Polars, running on the user's own PC or VPS, with the user's own static IP.
   - **Brokers:** official `kiteconnect` and `kotakneoapi` adapters behind our own interface. Optionally, the user's own unmodified OpenAlgo through the MIT `openalgo` SDK.
   - **Engines:** our own backtester, paper engine and cost model, plus `ffn` and `bt`.
   - **Scheduling:** APScheduler (IST triggers), with DBOS or procrastinate later.
   - **UI:** React/Vite + shadcn + lightweight-charts, installable as a PWA.
   - **Distribution:** Docker Compose. Ship proprietary or source-available code, and keep GPL/AGPL/Commons Clause dependencies out.
2. **Our cloud (mode A-lite: no market data, no orders).**
   - **Hosting:** one DO BLR1 droplet (or Fly `bom`) + Supabase Pro Mumbai (auth + DB).
   - **Scope:** licence keys, accounts, strategy *templates the user edits*, course and community links.
   - **Payments:** Cashfree (0% promo) with Razorpay as backup.
   - **Courses and community:** Exly or Graphy + Discord.
3. **Mode A (hosted automated trading) only after:**
   - ADR-G1;
   - Zerodha platform or multi-login approval and the Kotak equivalent;
   - broker algo-provider empanelment;
   - a licensed historical/EOD data contract.

   Then the order router moves to a dedicated-IP VM (DO BLR1), with DBOS durable workflows and an audit ledger.

**What would change this**
- Zerodha or Kotak grants platform approval with data display → mode A becomes viable sooner. Kotak's "free API" makes it the cheaper primary broker.
- Counsel says a user-side runner fed by our cloud *is* an algo provider → mode B must be fully offline: strategies authored locally, with no signals pushed from our servers.
- An Apache/MIT Indian paper engine appears, or OpenAlgo offers a commercial licence → reuse it instead of building.
- The owner wants store apps in v1 → add Flutter (≈ +3–4 weeks).

---

## 7. One-developer, 8-week build plan (mode B + cloud A-lite)

| Week | Deliverable | Verification (from CLAUDE.md) |
|---|---|---|
| 0 (before) | **ADR-G1** (amend "no order code"); ADR for mode B; send counsel questions CQ-new-1..3 and the Zerodha/Kotak data-terms questions | Owner sign-off recorded |
| 1 | Fork the structure of full-stack-fastapi-template (not its git history). Settings with no secrets in code; broker-adapter interface; Kite + Kotak login flows using the **user's own** keys and TOTP; instrument master; typed errors | Adapter unit tests on recorded fixtures; tz-aware UTC timestamps asserted |
| 2 | Historical candles through the user's session into local Parquet/DuckDB (never uploaded); XBOM calendar; entitlement and source labels on every bar | Fixture tests; no weekday arithmetic |
| 3 | **Backtester v1** (vectorised Polars, next-bar-open fills) + **Indian cost model** (dated table, §3) + `ffn` metrics | Golden-fixture and property tests; `/financial-validation` |
| 4 | Backtester v2: event loop (stops, targets, MIS square-off, lot sizes); strategy DSL (a Python function template, or CEL/GoRules rules per radar); results page with a "hypothetical; past ≠ future" line | Parity test: vectorised and event-driven give the same P&L on shared cases |
| 5 | **Paper engine** (LTP-crossing fills, slippage, costs, circuit/lot/tick checks); audit log of simulated fills. Enable it on live feeds only for a broker whose terms allow it: **Kite is barred**, Kotak is pending. Until then, run it only in replay over recorded fixtures | Replay tests from recorded tick fixtures |
| 6 | **Live runner** (only if ADR-G1 is approved): APScheduler IST triggers; **manual-confirm mode by default**; 10 orders/s limiter; kill switch; max-loss per day; idempotent client order IDs; static-IP check at startup | Stub broker tests; `security-engineer` review; no live calls in tests |
| 7 | Cloud A-lite: Supabase auth, Cashfree checkout, licence-key issue/verify, landing page, PWA shell; courses on Exly/Graphy + Discord linked | Endpoint and auth tests; generic error bodies |
| 8 | Packaging (Docker Compose, one-line installer), docs, telemetry opt-in (no market data), pilot with 5–10 users on their own VPS | `/readiness-review`; secrets scan |

**Buffer:** none. With 2 developers, parallelise weeks 3–5 (quant) against weeks 6–7 (platform), which leaves about 2 weeks for hardening.

---

## 8. Monthly cost at pilot scale

Assumed pilot: ~200 registered users, ~20–50 active traders, course GMV ₹1 L/mo. Costs are in INR (USD); GST is added where it applies.

| Item | Mode B + cloud A-lite (recommended) | Mode A hosted SaaS (after approvals) |
|---|---|---|
| App server | DO BLR1 2 GB droplet $12 (≈ ₹1,056) | 2 × 4 GB droplets (app + order router with a dedicated IP) $48 (≈ ₹4,224) |
| DB + auth | Supabase Pro $25 (≈ ₹2,200) | Supabase Pro + Small compute ≈ $30 (≈ ₹2,640), or DO PG $15.15 + separate auth |
| Fan-out | — (local to each user) | SSE in-app ₹0; Centrifugo on the same droplet ₹0 |
| Frontend hosting | Cloudflare Pages ₹0 | ₹0 |
| Static IP | User's own (a DO $6 droplet ≈ ₹528 per user, **paid by the user**) | Included with the droplet (+ Fly $3.60 per IP if on Fly) |
| Broker API | User pays: Kite Connect ₹500 per app per month if they want data; **Kotak ₹0 "at present"** | Kite: free for approved platforms (revenue share by enquiry); Kotak unverified |
| Historical / market data | ₹0 to us (user's own session) | NSE EOD display licence ₹1 L/yr ≈ **₹8,333/mo** + vendor quote; more for delayed or real-time (data-stack-costs) |
| Courses / community | Exly Pro ₹2,500 + 6% commission (₹6,000 at ₹1 L GMV) + Discord ₹0 | same |
| Payments | Cashfree 0% until ₹20 L GMV or 2027-03-31; then ~2.30% incl. GST (≈ ₹2,300 at ₹1 L) | same |
| Email / monitoring / domain | Free tiers + domain ≈ ₹100/mo [E] | ≈ ₹1,000/mo [E] |
| Dev tools | Claude Code seat(s) (owner's existing plan; not priced here); Kite Connect dev app ₹500 | same |
| **Total, excl. commissions** | **≈ ₹6,400/mo (~$73)** | **≈ ₹16,000–20,000/mo (~$180–230) + vendor fee + empanelment/legal (unknown)** |
| **Total, incl. course commission at ₹1 L GMV** | **≈ ₹12,400/mo (~$141)** | ≈ ₹22,000–26,000/mo |

**Add 18% GST** on SaaS fees, the course-platform commission and gateway fees. On the mode B total at ₹1 L GMV that is ≈ +₹2,100: commission ₹1,080, Exly fee ₹450, Supabase ≈ ₹400, DO ≈ ₹190. That brings mode B to **≈ ₹14,500/mo (~$165) including GST and commission**. Infra costs are **estimates [E, M]** built from list prices read on 2026-09-24.

---

## 9. PyPI and licence trap list

| Name | Problem |
|---|---|
| `pybroker` | **Not registered**: the real package is `lib-pybroker`. A squatting risk; pin the real name |
| `htmx` (PyPI 0.0.0, 2023, "CJ Lazell") | Unrelated to htmx.org |
| `polars-backtest` | PolyForm **Noncommercial** |
| `fastquant` | GitHub says MIT, PyPI says **GPLv3** (and it wraps backtrader) |
| `lean` (PyPI) | Is QuantConnect's **CLI**, not the engine (legitimate, Apache) |
| `jugaad-trader` | No licence; reverse-engineered login; placeholder author email |
| `kotak-neo-api`, `neo-api-client`, `kotakneo`, `pykiteconnect`, `kite-connect`, `openalgo-sdk` | **Not on PyPI.** Anyone could register them later. Use only `kotakneoapi` and `kiteconnect` (and `openalgo`, which is MIT, by Rajandran/openalgo.in) |
| OpenAlgo (platform) | **AGPL-3.0** |
| Backtesting.py, fast-trade | **AGPL-3.0** |
| backtrader | **GPL-3.0** (a trap in mode B) |
| vectorbt, lib-pybroker | **Commons Clause** |

---

## 10. Counsel and vendor questions (new)

- **CQ-new-1:** If our cloud service distributes strategy templates or signals to a runner that the user self-hosts and that places orders through the user's own API key and static IP, are we an "algo provider" under SEBI's 4 Feb 2025 framework, or "associated" under the 29 Jan 2025 circular?
- **CQ-new-2 (Zerodha, Kotak):** May one static IP be whitelisted for many client IDs by a platform? Does the Kotak Neo Trade API allow a third-party multi-user platform, and what are its data-display terms?
- **CQ-new-4 (Zerodha, kiteconnect@zerodha.com; same to Kotak):** Is a distributed app that the user self-hosts, using the user's own Connect app and keys with no data leaving the user's machine, a permitted "private interface"? Does the "virtual/mock trading apps" ban cover a paper-trading module inside such an app?
- **CQ-new-3 (Razorpay, Cashfree):** Is a subscription for backtesting/paper-trading software plus trading education an allowed business category without SEBI registration?

---

## 11. Unverified list

1. Kotak Neo data-display and multi-user terms, WebSocket limits and the historical-data window (vendor page silent).
2. Whether one shared static IP can serve multiple clients (all brokers).
3. BSE transaction charges; Kotak's statutory-charge schedule (only brokerage was read).
4. Razorpay and Cashfree restricted-business lists for trading and advisory categories.
5. TRAI DLT requirement for SMS OTP (from memory; not re-read).
6. Vercel Hobby's non-commercial restriction (from memory).
7. The Oracle Always Free quota conflict (1,500 vs 3,000 OCPU-h). Probably Always-Free-only vs PAYG tenancy.
8. Fly `bom` static egress availability (pricing came from a search extract; region support was not confirmed on the page).
9. Render's dedicated-IP price; whether DO BLR1 prices match other regions.
10. Ziplime's licence; the maturity of `lib-pybroker`'s live-trading support.
11. The Kotak "<50 ms" latency claim (audit methodology not published).
12. App-store policy for Indian trading or securities apps (Play/App Store declarations).
13. Whether OpenAlgo's maintainer would offer a commercial licence (no CLA found; not asked).

## Sources (all accessed 2026-09-24)

**Registry and GitHub**
- PyPI JSON:
  - Kotak, Zerodha and OpenAlgo clients: https://pypi.org/pypi/kotakneoapi/json, /kiteconnect/json, /openalgo/json, /jugaad-trader/json, /algomojo/json
  - Backtesting engines: /backtrader/json, /backtesting/json, /vectorbt/json, /zipline-reloaded/json, /bt/json, /ffn/json, /nautilus_trader/json, /lean/json, /lib-pybroker/json, /fastquant/json, /polars-backtest/json, /ziplime/json, /quantstats/json
  - Web, jobs and payments: /polars/json, /streamlit/json, /reflex/json, /fastapi/json, /supabase/json, /apscheduler/json, /procrastinate/json, /dbos/json, /razorpay/json, /cashfree-pg/json, /htmx/json
  - Checked and found 404: /pybroker/json, /kotak-neo-api/json, /neo-api-client/json
- GitHub API:
  - Broker platforms and SDKs: repos/marketcalls/openalgo (plus contents/broker, CLAUDE.md, License.md, CONTRIBUTING.md), Kotak-Neo/kotak-neo-python, Kotak-Neo/Kotak-neo-api-v2, jugaad-py/jugaad-trader
  - LEAN broker plugins: QuantConnect/Lean.Brokerages.Zerodha, QuantConnect/Lean.Brokerages.Samco
  - Backtesting engines: mementum/backtrader, kernc/backtesting.py, polakowo/vectorbt (license), edtechre/pybroker (license), jrmeier/fast-trade, Yvictor/polars_backtest_extension
  - Templates: fastapi/full-stack-fastapi-template, wasp-lang/open-saas, nextjs/saas-starter, vercel/nextjs-subscription-payments
  - Frontend and infra: tradingview/lightweight-charts, centrifugal/centrifugo, bigskysoftware/htmx (license), anthropics/claude-code-action

**Vendors**
- Brokers:
  - https://zerodha.com/charges/
  - https://www.kotakneo.com/pricing/
  - https://www.kotakneo.com/platform/kotak-neo-trade-api/
- Hosting:
  - https://docs.fly.io/reference/regions/
  - https://fly.io/docs/networking/egress-ips/ (via search extract)
  - https://railway.com/pricing
  - https://docs.railway.com/reference/deployment-regions
  - https://docs.railway.com/reference/static-outbound-ips
  - https://render.com/docs/regions
  - https://render.com/docs/free
  - https://render.com/docs/outbound-ip-addresses
  - https://www.digitalocean.com/pricing/droplets
  - https://www.digitalocean.com/pricing/managed-databases
  - https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm
- Database and auth:
  - https://supabase.com/pricing
  - https://supabase.com/docs/guides/platform/regions
  - https://clerk.com/pricing
- Payments:
  - https://razorpay.com/pricing/
  - https://www.cashfree.com/payment-gateway-charges/
- Course and community platforms:
  - https://graphy.com/pricing
  - https://www.teachable.com/pricing
  - https://circle.so/pricing
  - https://www.tagmango.com/pricing
  - https://exlyapp.com/pricing

**STT (secondary sources)**
- https://www.icicidirect.com/ilearn/futures-and-options/articles/stt-changes-in-budget-2026-what-f-o-traders-should-know
- https://cleartax.in/s/securities-transaction-tax-stt
- HDFC Securities note of 7 Feb 2026 (hdfcsec.com)
