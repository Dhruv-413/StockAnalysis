# Fast-fetch research: market data, news, filings, events (US equities/ETFs)

Research date: 2026-09-24. All URLs accessed 2026-09-24 unless noted.
Confidence: H = official vendor doc/PyPI read directly; M = vendor marketing, a search summary of an official page, or a reputable secondary source; L = third-party blog, aggregator, or unverified claim.
Pricing already covered in earlier research is not repeated here; only new price points are listed.

---

## 1. Streaming protocols and client libraries

| Vendor | Transport / encoding | Client libs (latest seen) | Limits | Snapshot / replay / gap recovery | Conf |
|---|---|---|---|---|---|
| **Databento Live** | Raw TCP, binary **DBN** (the same record layout as historical). CRAM challenge-response auth. No WebSocket and no OpenAPI spec. | `databento` **0.87.0** (Python >=3.10, pins `databento-dbn >=0.70.0,<0.71.0`). `databento-dbn` **0.70.0**. Official Rust and C++ clients too. | Per dataset gateway; no symbol cap found in the docs I read. | **Intraday replay** (`start=` on subscribe), guaranteed only for about the **last 24 h**. **MBO `snapshot=True`** gives a book snapshot taken within the last minute. `ts_out` gateway send timestamps let you measure latency. | H (versions), M (replay/snapshot) |
| **Massive (ex-Polygon)** | WebSocket JSON. `wss://socket.massive.com` (real-time), `wss://delayed.massive.com`. Prefix subscriptions (`T.AAPL`, `Q.*`, wildcard `*`). | `massive` **2.8.0** (26 May 2026, Py 3.9–3.14). Package renamed from `polygon-api-client`; defaults to `api.massive.com`, and `api.polygon.io` still works. | **1 connection per asset-class cluster** by default (Business: 3). **No ticker cap** except Options Quotes (~1,000 contracts per connection). Slow consumers are **disconnected** when the server buffer fills. Each message averages about 1.85 trade events / 2.14 quote events. | No replay on the socket; backfill a gap with REST. | H |
| **Alpaca** | WebSocket, **JSON or MessagePack** (set with Content-Type). RFC 7692 compression. `wss://stream.data.alpaca.markets/v2/{iex,sip,delayed_sip}`. News: `/v1beta1/news` (Benzinga-sourced). 24/7 test stream `v2/test` with symbol FAKEPACA. | `alpaca-py` (official) | Usually **1 connection per endpoint** (error 406). Free: 30 trade/quote channels, IEX only. Unlimited plan: no channel cap, SIP. Error 407 = slow client disconnect. | No replay. Channels include `statuses` (halts/LULD), `corrections`, `cancelErrors`. | H |
| **Finnhub** | WebSocket JSON `wss://ws.finnhub.io?token=`; multiplexed by `type`. | community / official SDKs | Free tier: 50 symbols (M). **News stream = Premium; press-release stream = Enterprise.** | None documented | M |
| **Twelve Data** | WebSocket JSON (`/quotes/price`) | `twelvedata-python` | Up to **3 connections**. 1 WS credit per subscribed symbol. Pro 610 plan = 1,500 symbols, Ultra = 10,000. 100 subscribe/unsubscribe events per minute. Claims **~170 ms average latency**. | None | M |
| **Tiingo IEX** | WebSocket JSON arrays, `wss://api.tiingo.com/iex`, nanosecond timestamps, heartbeat "H" messages. | `tiingo` | Not stated | `thresholdLevel` 0/5 (full IEX TOPS) needs an **IEX data agreement since 2025-02-01**. Level 6 is a derived "tngoLast" stream with no agreement. Servers are about 15 miles from NY5. | M |
| **IBKR TWS/Gateway** | Proprietary socket to a local TWS/IB Gateway process. | **`ib_async` 2.1.0** (maintained successor to ib_insync; the original maintainer died in 2024). | **100 market-data lines** by default (more via quote boosters). **Tick-by-tick = 5% of lines**, and one request per instrument per 15 s. `reqMktData` sends **aggregated snapshots several times a second, not every tick**. | None (broker feed) | H/M |
| **Schwab Trader API streamer** | WebSocket JSON (LEVELONE_EQUITIES etc.). | `schwab-py` | A `REACHED_SYMBOL_LIMIT` error exists; I could not verify the exact cap. | None | L/M |

Notes
- Databento publishes latency figures but no live numbers. Its `/latency` dashboard was showing "No data available". The NVIDIA case study says about **63 µs median** through its DPDK firewall/router and **<315 µs to public cloud**, plus "U.S. options online in <242 µs" (M, vendor/partner marketing). A third-party profile quotes **6.1 µs median internal gateway latency** (L).
- Databento **EQUS.MINI has no `status` schema** (no halt/resume flags). The roadmap item is open (H/M). For halts, use Alpaca `statuses`, Massive LULD/status, or Nasdaq Basic/IEX TOPS status on Databento.

Sources: https://databento.com/docs/api-reference-live ; https://pypi.org/pypi/databento/json ; https://pypi.org/pypi/databento-dbn/json ; https://databento.com/blog/live-MBO-snapshot ; https://databento.com/docs/api-reference-live/basics/intraday-replay ; https://www.nvidia.com/en-us/case-studies/databento ; https://roadmap.databento.com/roadmap/status-schema-for-equsmini ; https://pypi.org/pypi/massive/json ; https://massive.com/blog/polygon-is-now-massive ; https://massive.com/knowledge-base/article/how-many-tickers-can-you-subscribe-to-on-a-single-massive-websocket-connection ; https://massive.com/knowledge-base/article/how-many-massive-websocket-connections-can-i-use-at-one-time ; https://docs.alpaca.markets/us/docs/streaming-market-data ; https://docs.alpaca.markets/us/docs/streaming-real-time-news ; https://finnhub.io/docs/api/websocket-news ; https://finnhub.io/docs/api/websocket-press-releases ; https://support.twelvedata.com/en/articles/5194610-websocket-faq ; https://www.tiingo.com/documentation/websockets/iex ; https://github.com/ib-api-reloaded/ib_async ; https://interactivebrokers.github.io/tws-api/market_data.html ; https://interactivebrokers.github.io/tws-api/tick_data.html ; https://schwab-py.readthedocs.io/en/latest/streaming.html

---

## 2. Low-latency news, filings, and event sources

### Newswires and news APIs
| Source | Delivery | Latency / notes | Conf |
|---|---|---|---|
| **Benzinga News WS** | `wss://api.benzinga.com/api/v1/news/stream?token=`. JSON with `action` = created / updated / deleted. Filter by `tickers` and `channels`. Ping every 30–60 s. **`replay` returns the last 100 cached messages** (gap recovery). A TCP server option is also offered. | No published ms figure. Also resold through Massive and Alpaca (the Alpaca news WS is Benzinga). | H (doc) |
| **Benzinga Squawk** | Audio over **WebRTC** (browser) or an **RTP** stream (re-broadcast) | Audio only; needs speech-to-text before it is machine-usable | M |
| **Dow Jones Newswires (DJ Elementized / low-latency multicast)** | Multicast in **Equinix NY4**; elementized (pre-parsed numeric) economic and corporate data | Vendor says it measures latency in **µs**. Enterprise only. | M |
| **LSEG Headlines Direct / MRN** | Headlines Direct: **binary multicast at NY4**, headline only, built for event trading. MRN: RTO/EMA or WebSocket API, with sentiment metadata. | Enterprise | M |
| **Bloomberg B-PIPE** | Enterprise consolidated feed (35M instruments, 350+ exchanges) | Enterprise; news is not the main low-latency product | M |
| **Issuer wires (Business Wire, PR Newswire, GlobeNewswire, AccessWire)** | Issuer press releases usually reach the wires before news rewrites. Direct machine feeds are sold by the wires (terms not public). GlobeNewswire has free RSS/XML feeds (polling). | **NEW: RTPR (rtpr.io)** aggregates all four wires. Vendor claims **p50 190 ms wire-to-screen** (30-day). $139/mo Pro; free tier delayed 5 min; delivers to dashboard, email, or "personal socket". Unverified vendor claim. | L/M |

### SEC EDGAR
- **`getcurrent` Atom feed** (`/cgi-bin/browse-edgar?action=getcurrent&output=atom`) updates continuously. Filings become public **within seconds of acceptance** during operating hours (M).
- **5:30 pm ET rule:** filings accepted after 5:30 pm are dated the next business day and **withheld from the live feed until the next morning** (Reg S-T Rule 13). Exception: Forms 3/4/5, Rule 144, and 13D/G use a **10:00 pm** cutoff, so insider filings keep flowing (M, edgartools.io, measured 2026-09-03).
- **Structured-disclosure (XBRL) RSS** updates only **every 10 minutes**, Mon–Fri 6am–10pm. **Too slow for alerts** (H).
- **Fair access:** at most **10 requests/s per user across all machines**, plus a declared User-Agent (name + email), or the SEC blocks your IP (H/M). Polling getcurrent every 1–2 s is within budget.
- **PDS (Public Dissemination Service):** a direct push feed of all accepted filings, sold by an SEC contractor (Maximus) under a paid subscription agreement. Historical price is about **$1,500/mo** (2014 Fortune; current price unverified, L). This is the true "wire" for EDGAR.
- **sec-api.io Stream API:** `wss://stream.sec-api.io?apiKey=`, JSON array of filing metadata (150+ form types). Server ping every 25 s; you must pong within 5 s. **Forward-only: no replay**, so backfill through the query API. Pricing page claims **<300 ms** availability. Plans: **$55/mo** monthly or $49 annual (Personal), **$239/mo** or $199 annual (Business). Stream is included on all paid tiers (H for doc/pricing, M for the latency claim).
- **Kaleidoscope (kscope.io):** push notifications to your endpoint on new EDGAR filings, filtered by form, ticker, or CIK. No latency figure published (M).

### Halts, macro, FDA
- **Nasdaq Trader halt RSS** (`nasdaqtrader.com/rss.aspx?feed=tradehalts`): free, but **updated once per minute**, and Nasdaq asks you not to poll faster. **Too slow for a fast alert path.** Use SIP-derived status messages instead: Alpaca `statuses`, Massive, or Databento status (H).
- **BLS:** releases at **8:30 ET**; the BLS publishes a schedule page and an iCal feed. **FOMC:** Fed meeting calendar page (statement at 2:00 pm ET, per standard practice, not re-verified here). The only speed edge is pre-scheduling and polling the release URL at T+0, or buying an elementized feed (DJ/LSEG) (M).
- **FDA:** no official forward PDUFA calendar (confidentiality). There is an official Advisory Committee calendar and a **press-release RSS** (`fda.gov/.../press-releases/rss.xml`). Third-party calendars: pdufa.bio (free JSON API), BPIQ, BiopharmaWatch, Unusual Whales (M).

### Social and alt data
- **X API (2026): pay-per-use only.** No Free, Basic, or Pro for new signups; legacy Basic was migrated after 2026-06-01 and Pro after 2026-09-01. Prices: **$0.005 per post read** (capped at **3M post reads/month** before Enterprise), $0.010 per user read, $0.001 per owned read. Filtered-stream pricing is not stated on the pricing page (H for prices; M for the migration dates).
- **Reddit:** free for non-commercial use at **100 QPM per OAuth client**. Commercial use needs approval and is reported at **$0.24 per 1k calls** (no public rate card; L/M).
- **Stocktwits:** **not accepting new API registrations** (under review). Firestream is for partners only (M).
- **Quiver Quant:** congressional and alt data, **daily** frequency. Not a latency source (M).

### Earnings calls (live)
- **Quartr API:** live transcripts streamed as **JSONL** word by word. Vendor says "close to zero delay" and >97% of events are live (M).
- **Aiera:** enterprise APIs for live event transcription, events, and transcripts. Human-edited 99% accuracy arrives 1–3 h after the event (M).

Sources: https://docs.benzinga.com/ws-reference/data-websocket/get-news-stream ; https://github.com/Benzinga/benzinga-squawk-client ; https://www.equinix.com/resources/case-studies/dow-jones-newswires ; https://www.lseg.com/content/dam/data-analytics/en_us/documents/fact-sheets/lseg-headlines-direct-fact-sheet.pdf ; https://lseg.com/en/data-analytics/financial-news-service/machine-readable-news ; https://rtpr.io/ ; https://www.globenewswire.com/rss/list ; https://www.sec.gov/data-research/structured-data/structured-disclosure-rss-feeds ; https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data ; https://www.edgartools.io/edgar-live-feed-after-hours-filings/ ; https://www.sec.gov/files/edgar/pds_dissemination_spec.pdf ; https://fortune.com/2014/10/30/sec-high-frequency-traders/ ; https://sec-api.io/docs/stream-api ; https://sec-api.io/pricing ; https://kscope.io/api-data-feeds/ ; https://www.nasdaqtrader.com/Trader.aspx?id=TradeHaltRSS ; https://www.bls.gov/schedule/2026/home.htm ; https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm ; https://www.fda.gov/advisory-committees/advisory-committee-calendar ; https://www.pdufa.bio/developers ; https://docs.x.com/x-api/getting-started/pricing ; https://www.socialcrawl.dev/blog/reddit-data-api-2026 ; https://api.stocktwits.com/developers ; https://api.quiverquant.com/docs/ ; https://docs.quartr.com/v1/guide/live-transcripts ; https://www.aiera.com/api

---

## 3. Fast networking and parsing

**Python**
- **uvloop 0.22.1:** Linux and macOS only (**no Windows**). Classifiers list Python up to 3.13 (3.14 not listed; check before upgrading) (H). The dev box is Windows 11, so run the hot path under Linux or WSL2 or in a container.
- **picows 2.3.1:** a Cython WebSocket client/server with a zero-copy API. The author's benchmark (tarasko/websocket-benchmark) runs a request/response echo over loopback against a C++ Boost.Beast server at 256 B, 8 KB, 100 KB, and 2 MB, on Linux and Windows. picows is the fastest Python client and at large sizes sometimes beats the Beast reference. The source reports ~1.5–2x over aiohttp generally and 3–5x (aiohttp) / 8–10x (websockets) at small sizes (M; author-run). Best fit for vendor WebSockets such as Massive and Alpaca.
- **websockets** is now **17.0.1**. The new asyncio implementation (Sans-I/O) is the default and legacy is deprecated. It is still the slowest of the three for frame handling (pure-Python framing) (H/M).
- **aiohttp:** solid middle option with Cython frame parsing; also the best mature async HTTP client for REST backfill.
- **niquests:** Requests fork with HTTP/1.1, 2, and 3, plus WebSocket and SSE. The author's multiplexed benchmark (Mar 2026) shows niquests ~2,564 req/s vs httpx ~1,389 vs requests ~1,013 (high-level API), and in "core" mode niquests ~5,882 vs aiohttp ~4,762 vs httpx ~1,886 (M, author-run). HTTP/3 helps only when the vendor serves it (most market-data REST APIs do not).
- **httpx:** convenient, but the slowest of the async options above.
- **JSON:** **msgspec 0.21.1** (Py 3.10–3.14) is about as fast as orjson without a schema. **With a typed `Struct` schema it decodes and validates faster than orjson decodes alone**, and uses 6–9x less memory in its benchmark (H, vendor benchmark). Floats parse about 15% slower than orjson. **orjson 3.12.0** (Py 3.10–3.15) is fastest for untyped dicts and encoding. pysimdjson needs an extra buffer copy and gives little benefit for small messages (M). **Recommendation:** msgspec Structs for vendor messages (Alpaca also offers msgpack, which msgspec decodes natively).
- **Binary formats:** DBN (Databento) needs no JSON at all; `databento-dbn` is Rust-backed and decodes straight to typed records or NumPy/pandas. **Arrow Flight** is a throughput protocol: the peer-reviewed benchmark shows up to 6,000 MB/s DoGet and 4,800 MB/s DoPut (arXiv 2204.03032). Use it for bulk internal transfer, not per-tick latency. **SBE** is the exchange-grade codec (CME, etc.); Python SBE decoders are not optimized (M). FlatBuffers/Cap'n Proto are only worth it for an internal fan-out bus.

**Rust**
- **tokio-tungstenite:** default choice. Maintainers say versions after 0.26.2 are close to fastwebsockets. **fastwebsockets** was about 2–3.7x faster in older benchmarks (16.7 ms vs 35.4 ms and 38.7 ms vs 142 ms send/echo) (M).
- **sonic-rs** beats **simd-json**, which beats serde_json. sonic-rs parses straight into structs with no tape (M, vendor benchmark).
- Official Databento Rust client plus `dbn` crate. A good choice if you ever build a Rust ingest service.

Sources: https://pypi.org/pypi/uvloop/json ; https://pypi.org/pypi/picows/json ; https://github.com/tarasko/websocket-benchmark ; https://websockets.readthedocs.io/en/stable/ ; https://github.com/jawah/niquests ; https://msgspec.dev/benchmarks ; https://pypi.org/pypi/msgspec/json ; https://pypi.org/pypi/orjson/json ; https://arxiv.org/abs/2204.03032 ; https://github.com/aeron-io/simple-binary-encoding ; https://github.com/cloudwego/sonic-rs ; https://github.com/snapview/tokio-tungstenite ; https://c410-f3r.github.io/thoughts/the-fastest-websocket-implementation/

---

## 4. Hosting near the data

- **Where vendors live:**
  - Massive: Secaucus NJ. Massive's guidance is tens of ms extra one-way elsewhere in North America and >100 ms on other continents (H). Community pings of 1.4–1.6 ms from NYC data centers (L).
  - Alpaca: market-data servers colocated with the SIPs in NYC (Cogent IP); trading API on GCP us-east4 (M, forum).
  - Databento: gateways at Equinix NY4 (Secaucus), CyrusOne Aurora I, Equinix FR2. Its latency dashboard measures from NY4, Aurora, **AWS us-east-1**, AWS Chicago, and FR2 (H).
  - Tiingo: about 15 miles from NY5 (M).
- **Cloud:** AWS us-east-1 (Ashburn) to NY4 round trip is about **3–8 ms** depending on route (L, search summary; plausible from fiber distance of ~330 km, so ~3.3 ms RTT minimum). For a small team the practical choices are **AWS us-east-1 or GCP us-east4**, or a **NY/NJ metro VPS** (QuantVPS, TradingFXVPS, Beeks) at about 1 ms to Massive/Databento. TradingFXVPS measured **0.87 ms average RTT** to Databento over an NY4 cross-connect (M, vendor PR).
- **Colo (µs tier):** Databento sells dedicated cross-connects at NY4/NY5 and Aurora I, or virtual circuits over Equinix Fabric (~22.9 µs mean one-way fabric latency). It also advertised interconnects at AWS, GCP, and Azure (M). Its Arista L1 and L3 switches run at 4 ns and <550 ns port-to-port (M). This makes sense only if the strategy needs <1 ms, which a decision/alert product does not.
- **Realistic budgets:**
  - Home/office internet to a vendor: 20–80 ms plus jitter.
  - us-east-1 to NJ vendor: about 2–5 ms one-way.
  - NJ metro VPS: <1 ms.
  - Colo cross-connect: tens of µs.

Sources: https://massive.com/knowledge-base/article/where-are-massives-servers-located ; https://forum.alpaca.markets/t/alpaca-data-center-locations/5640 ; https://databento.com/latency ; https://databento.com/dedicated-connectivity ; https://tradingfxvps.com/tradingfxvps-establishes-direct-cross-connect-to-databento-at-equinix-ny4/ ; https://www.elitetrader.com/et/threads/databento-launches-dedicated-interconnects-at-aws-google-cloud-azure-and-8-data-centers.375861/

---

## 5. Fan-out to users

- **SSE vs WebSocket:** for server-to-client pushes, the measured latency difference is under 1 ms (26.3 vs 26.2 ms mean over a simulated 50 ms RTT). SSE over **HTTP/2** multiplexes many streams on one TCP connection, reconnects automatically (`Last-Event-ID` gives free replay), and passes through proxies and CDNs easily. **WebSocket** is only needed for low-latency client-to-server traffic (M).
- **WebTransport** has been **Baseline since Safari 26.4 (Mar 2026)**, alongside Chrome 97+ and Firefox 114+. It runs over HTTP/3/QUIC, avoids head-of-line blocking, and supports unreliable datagrams. Server tooling is still immature, so treat it as optional (M/H).
- **Centrifugo v6** (Jan 2025; v6.9.x in 2026): self-hosted Go server with history/recovery (stream positions give gap-free resume), a PostgreSQL-only cluster mode (no Redis), tag-based publication filters, and synchronized key-value "map" subscriptions. PRO adds a push-notification API (APNs/FCM/Web Push). Strong fit for per-ticker channels (H/M).
- **Ably:** SLA-style claims of **<65 ms p99 round trip** and **37 ms global mean**, with a public latency dashboard (M, vendor).
- **Pusher Channels:** "<240 ms" claim; 9 clusters (M).
- **Phoenix Channels:** Elixir, proven at millions of connections per node (well known; not re-verified here, L).
- **NATS:** server supports WebSocket natively; the `nats.ws` browser client is maintained by NATS (H). Useful as an internal bus that also reaches browsers.
- **Mobile/web push:**
  - Knock's 2025 data measures only **API acceptance**: APNs p50 **65 ms**, FCM p50 **110 ms**, p99 323 ms (M).
  - Device delivery is usually **~1–2 s**, but can take **tens of seconds** under Doze/battery modes. FCM high priority can wake devices. `ttl=0` gives the best latency but drops the message if it cannot be delivered right away (M).
  - There is **no SLA**. Treat push as best effort and keep an in-app live channel as the primary path.

Sources: https://websocket.org/comparisons/sse/ ; https://www.timeplus.com/post/websocket-vs-sse ; https://webrtc.ventures/2026/04/webtransport-is-now-baseline-what-it-means-for-real-time-media/ ; https://webkit.org/blog/17862/webkit-features-for-safari-26-4/ ; https://centrifugal.dev/blog/2025/01/16/centrifugo-v6-released ; https://github.com/centrifugal/centrifugo/releases ; https://ably.com/docs/platform/architecture/latency ; https://pusher.com/channels/ ; https://docs.nats.io/learn/websocket/ ; https://knock.app/push-api-benchmarks/compare/apns-vs-fcm ; https://firebase.google.com/docs/cloud-messaging/android-message-priority

---

## 6. New (2025–2026) tools worth knowing

- **Massive MCP (`massive-com/mcp_massive`):** rebuilt around three composable tools (search, call, query) covering the whole API. Can load results into in-memory SQLite. Available as a Claude Desktop integration (H/M).
- **Alpha Vantage official MCP** at `mcp.alphavantage.co` (listed Jul 2025) (M).
- **Alpaca MCP Server v2:** official; rewritten on FastMCP + OpenAPI; 65 tools across trading and market data (H/M). **Note: it can trade, so gate write tools.**
- **Financial Datasets MCP:** official; fundamentals, prices, news (M).
- **OpenBB `openbb-mcp-server`:** turns ODP/FastAPI into MCP with lazy tool discovery; stdio, SSE, and streamable-http (H/M).
- **EDGAR MCPs:** `stefanoamorelli/sec-edgar-mcp` (PyPI, Docker `mcp/sec-edgar`), `leopoldodonnell/edgar-mcp`. EdgarTools is the Python library behind many of them (M).
- **Databento MCP:** community only (Nice-Wolf-Studio; futures-focused). **No official one found** (M).
- **RTPR:** new aggregated press-release firehose (see §2) (L/M).
- **pdufa.bio:** free JSON API for PDUFA and adcom dates (M).
- **X API pay-per-use** (2026) makes small-volume X monitoring affordable but capped (H).
- **MCP servers are request/response.** They are not a streaming path: use them for LLM research and enrichment, never in the alert hot path.

Sources: https://github.com/massive-com/mcp_massive ; https://massive.com/blog/massive-rebuilds-mcp-server ; https://mcp.alphavantage.co/ ; https://github.com/alpacahq/alpaca-mcp-server ; https://docs.financialdatasets.ai/mcp-server ; https://pypi.org/project/openbb-mcp-server/ ; https://github.com/stefanoamorelli/sec-edgar-mcp ; https://github.com/Nice-Wolf-Studio/databento-mcp-server

---

## 7. Recommended fast-fetch stacks

### A. About 1 s end-to-end (event to user screen); small team, cloud-hosted
- **Host:** one Linux VM in **AWS us-east-1 or GCP us-east4**. Optionally put the ingest box on a NJ-metro VPS.
- **Prices:** Massive WS (all tickers, wildcard) or Alpaca SIP WS (msgpack). For halts, use the Alpaca `statuses` channel or Massive's status/LULD feeds, not the Nasdaq RSS.
- **News:** Benzinga WS, direct or through Massive/Alpaca. Use `replay` (last 100) after reconnect.
- **Press releases:** RTPR, or Finnhub Enterprise PR stream if budget allows.
- **Filings:** sec-api.io Stream (forward-only), plus a **getcurrent Atom poller every 1–2 s** (within 10 req/s) as a cross-check and backfill. Remember the 5:30 pm hold.
- **Macro/FDA:** scheduled pollers armed at T-5 s on BLS/Fed/FDA URLs, using the BLS iCal and pdufa.bio for scheduling.
- **Code:** Python 3.12/3.13 + **uvloop + picows** (or aiohttp) + **msgspec Structs**. One asyncio process per feed. Put an in-process ring buffer or Redis Streams/NATS in the middle for fan-out.
- **Gap recovery:** track the last timestamp per feed; on reconnect, backfill over REST (Massive, Alpaca) or `start=` replay (Databento).
- **To users:** **SSE over HTTP/2** (with `Last-Event-ID` replay) or **Centrifugo** (history recovery). APNs/FCM push as a secondary channel.
- **Expected budget:**
  - vendor ingest 5–50 ms
  - parse and rules <5 ms
  - broker/fan-out 5–20 ms
  - internet to user 30–100 ms
  - **roughly 100–250 ms to an open browser, 1–3 s for mobile push**

### B. About 50 ms end-to-end (to a user or model process in the same region)
- **Host:** ingest in the **NJ metro** (NY4/NY5 VPS or small colo). Optionally use Databento cross-connect or Equinix Fabric.
- **Prices:** **Databento Live** (raw TCP, DBN, `ts_out` for latency measurement), with the Rust client or `databento` Python. Use `snapshot=True` and `start=` replay for recovery.
- **News/filings:** Benzinga TCP/WS; sec-api.io Stream. For true µs news you need enterprise feeds (DJ low-latency multicast, LSEG Headlines Direct at NY4, EDGAR PDS).
- **Decision engine:** co-located in the same process or the same host. Rust (tokio + sonic-rs / dbn), or Python with picows + msgspec and no cross-process hops on the hot path.
- **Fan-out:** NATS or Centrifugo in the same metro. End users outside NJ still add 10–80 ms of internet RTT, so 50 ms to a remote human is only reachable for NE-US users. **Push notifications cannot meet 50 ms.**

---

## Unverified or low-confidence items
1. Databento internal gateway latency "6.1 µs" (third-party profile). The Databento `/latency` dashboard showed no data.
2. AWS us-east-1 to NY4 "3–8 ms RTT" (search summary; no primary measurement).
3. EDGAR PDS current price (~$1,500/mo is a 2014 figure; now via a Maximus subscription agreement).
4. RTPR p50 190 ms and sec-api.io "<300 ms" are vendor claims with no independent measurement.
5. Schwab streamer per-service symbol cap (error exists; number not confirmed).
6. Finnhub free-tier 50-symbol WS cap (secondary sources).
7. Reddit commercial pricing ($0.24/1k; $12k/mo tier) is not on a public rate card.
8. X API migration dates and the absence of a filtered-stream price (the pricing page does not list stream pricing).
9. picows, niquests, msgspec, and sonic-rs benchmarks are author- or vendor-run.
10. Quartr "near-zero delay" and Aiera live-transcription latency have no published numbers.
11. picows 2.3.1 upload date (PyPI metadata was ambiguous).
12. uvloop Python 3.14 support (not in classifiers).
13. FOMC 2:00 pm ET statement time (standard practice; not re-read from the Fed page in this pass).
