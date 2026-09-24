# Research: A fast system to fetch data, decide and notify (US equities/ETFs)

Research date: 2026-09-24. Every URL below was accessed on 2026-09-24.
Confidence ratings: **H** = primary or official source, consistent. **M** = vendor claim, or a secondary source that looks credible. **L** = blog, forum, community repo or search snippet only.

---

## 0. TL;DR

- **Network and feed latency matter more than language choice** for anything slower than about 1 ms.
  - A retail vendor websocket reaching a cloud VM has a median of roughly 9–41 ms, and it varies by session. Massive (formerly Polygon) refuses to publish a figure for exactly this reason.
  - Databento quotes 590 µs p90 over the internet and 42 µs p90 over a cross-connect. It does not say where the internet client was, so it was probably in or near the NJ metro.
  - Physics sets a floor of about 1.8–2 ms one-way from Ashburn (us-east-1) to Secaucus (my derivation).
  - Python with uvloop and msgspec adds roughly tens to hundreds of µs per message (my estimate). That cost disappears inside a 10 ms or larger network budget.
- **"JEV" most likely means TypeSafe's *Jev***. It is a "System One" typed decision model, released 2026-09-15, with its hosted API opened 2026-09-21. It returns decisions in 70–500 ms, and the trading-bot hype around it is on X.
  - It fits only the ~1 s tier.
  - It should only classify news and filings. It must never size orders or act as the order and risk authority.
  - Second reading: "JVM", since Deephaven, Disruptor, Aeron and Chronicle all run on the JVM.
  - Third reading: GoRules "JDM"/Zen, a deterministic rules engine that evaluates in microseconds and has Python bindings.
- **Recommendation for this project now: tier A (~1 s).**
  - Keep Python and FastAPI.
  - Take a vendor websocket and poll EDGAR within its fair-access limit.
  - Evaluate rules deterministically in-process with GoRules Zen or plain Python.
  - Optionally call Jev asynchronously for semantic tags on news and filings.
  - Notify via push, Slack or email.
- Moving to tier B (10–50 ms) is mostly about **where the code runs** (same region or PoP as the feed) and **removing LLM or Jev from the hot path**. It is not mainly a rewrite.
- Sub-ms end-to-end (tier C) is impossible from any cloud region outside the NJ data-center metro, because of the physics floor. It is also impossible from a retail vendor websocket (measured medians of 9–41 ms). In practice it requires colocation and direct feeds or a cross-connect.

---

## 1. What "JEV for fast decision" probably means

| Candidate | Evidence | Fit |
|---|---|---|
| **TypeSafe Jev** (primary interpretation) | The official blog was published on 2026-09-15 and calls Jev the first "System One Model". It returns type-safe structured values (Choice, Score, Noul = yes/no) instead of text. Latency is "70ms-500ms" versus "3 to 329 seconds" for frontier LLMs. Evals were "run from our laptops on the West Coast", with no percentile or hardware stated, and the blog does not mention finance. https://typesafe.ai/blog/introducing-system-one-models-and-jev **H** (existence) / **M** (latency). Pricing is $0.042 per 1M input tokens, with output free (official blog) **H**. The hosted-API open date (2026-09-21) and the endpoint POST api.typesafe.ai/v1/systemone come from search snippets only, and docs.typesafe.ai did not show them **L**. It is listed on OpenRouter as "jev-1.13" (https://openrouter.ai/typesafe/jev-1.13) **M**. The trading hype comes from X posts, e.g. "calibrated buy/sell decisions in under 100 ms" (https://x.com/RohOnChain/status/2101311813908652069), and from a "JEV-Trader" open-source bot. Community repos (a survey of 16 projects, 2026-09-20: https://gist.github.com/drillan/6916b16e8ea31a8ec36c8f59d6483150) are mostly crypto (Monad/Kuru, Hyperliquid, Kraken), and several are placeholders **L**. An independent review warns that "typed is not correct": Jev is weak on numeric precision and date comparison, and it must not calculate prices, sizes or risk limits or act as the sole order authority (https://wavect.io/blog/jev-ai-decision-model-review/) **M**. | Timing and wording both match. Useful as a fast semantic classifier on news and filings (e.g. "is this 8-K material? bullish, bearish or neutral?"). Too slow and nondeterministic for the 10–50 ms or sub-ms tiers. If served from the US West Coast, calling it from us-east adds roughly 60–70 ms RTT (my estimate, not cited). Note: jevtypesafeai.com and jevmodel.org appear to be third-party sites, not official. |
| **JVM** (Java low-latency stack) | This is how low-latency finance software is typically built: LMAX Disruptor, Aeron, Chronicle, Agrona, and Deephaven (a Java engine from Walleye's trading systems). | A plausible mishearing of "JVM". |
| **GoRules JDM / Zen Engine** | JDM means JSON Decision Model: decision graphs stored as JSON. The Zen engine is written in Rust and has bindings for Python, Node, Go, Java, Kotlin, .NET and Swift. The vendor says "Decisions evaluate in microseconds". Version 2.0 is the first stable release of the new engine line, and the repo was active on 2026-09-22 (https://github.com/gorules/zen, https://docs.gorules.io/developers/jdm/standard) **M**. The license is MIT per the repo (verify). | The best fit for a **deterministic**, auditable, fast decision layer. Business users can edit the rules. It works well alongside Jev. |
| Hazelcast Jet / literal "jev" packages | I did not find a relevant finance package literally named "jev" on PyPI or crates (not searched exhaustively). Hazelcast Jet has been merged into the Hazelcast Platform. | Unlikely. |

**Ask the owner** which one they mean. If they mean TypeSafe Jev, place it off the critical path: tick → deterministic rules → alert, with Jev enriching news and filings asynchronously.

---

## 2. Latency tiers: language and runtime (measured numbers only where cited)

### Network and feed floor (this dominates)

| Path | Number | Source / conf |
|---|---|---|
| SIP processing, UTP (Nasdaq-listed) | median about 12–16 µs (the page states "16.3-12.7 µs") | https://utpplan.com/PageParts/Overview.html **M** |
| SIP processing, CTA (CQS/CTS) | median under 20 µs | https://www.ctaplan.com/index (via search) **M** |
| Databento to your app | **p90 42 µs over a cross-connect, 590 µs over the internet** | https://databento.com/datasets/XNAS.ITCH **M** (vendor) |
| Equinix Fabric overhead | about 22.9 µs mean one-way **added on top of distance**. This is not the NY4-to-AWS path latency. | https://databento.com/docs/architecture/dedicated-connectivity-guide **M** |
| Alpaca plans | Basic (free) is **IEX only** with 30 websocket symbols. Algo Trader Plus is **$99/mo** for all US exchanges (SIP) with unlimited symbols. | https://docs.alpaca.markets/us/docs/about-market-data-api **H** |
| Massive (Polygon) websocket | No published figure. Their own two test sessions had medians of **41 ms and 9 ms**, and client network conditions dominate. | https://massive.com/knowledge-base/article/what-is-the-average-latency-for-polygons-websockets **H** |
| Alpaca IEX websocket | about 4–5 ms p50 and 18–25 ms p99 in one hobby measurement | https://github.com/rgrewal/alpaca-market-data **L** |
| Benzinga news via Massive | "~25 ms" websocket | third-party blog https://mediawatcher.ai/... **L** |
| AWS us-east-1 (Ashburn) to NY4 (Secaucus) | 3–8 ms RTT reported. Physics floor: about 350–400 km of fiber at about 5 µs/km gives about 1.8–2 ms one-way (my derivation). | search snippet **L**; derivation **M** |
| SEC EDGAR | The fair-access limit is **10 requests/s** and requires a declared User-Agent (https://www.sec.gov/os/accessing-edgar-data) **H**. The delay from acceptance to the RSS feed averaged about 25 s across about 4,000 filings (Friedman, Aug 2025, via https://www.alphanume-research.com/p/a-cracked-quants-guide-to-beating) **L-M**. The Structured Disclosure (XBRL) RSS feeds update every 10 minutes, which is a different feed from latest-filings (https://www.sec.gov/data-research/structured-data/structured-disclosure-rss-feeds) **H**. The daily index is built nightly, so use the latest-filings feed for real time. Submissions after 5:30 pm ET (10 pm for ownership forms) are disseminated the next business day (accessing-edgar-data page) **H**. | |

**Conclusion.**
- Over a retail websocket in cloud, the feed alone costs 1–40+ ms with a heavy tail.
- Databento's 590 µs internet p90 comes from an unstated client location, very likely near NJ.
- From us-east-1, the physics floor is about 2 ms one-way from NJ-originated data.
- **Sub-ms end-to-end is impossible from any cloud region outside the NJ metro, and in practice needs colocation plus a cross-connect.** Filings arrive tens of seconds after acceptance, so filing-driven signals are inherently a ~1 s-or-slower tier.

### Runtime and compute tier (in-process, per event)

| Stack | Realistic p50 / p99 for "decode → update state → evaluate rule" | Evidence / conf |
|---|---|---|
| (a) Python asyncio + uvloop + msgspec (+ picows) | About tens of µs p50. p99 in the 100s of µs to ms range because of GIL and GC hiccups. Fine for tiers A and B. | uvloop is "still a little faster than vanilla asyncio from Python-3.13" but "not very well maintained anymore" (https://github.com/tarasko/websocket-benchmark) **L-M**. I found no rigorous p99 benchmark (unverified). |
| (b) Rust + tokio | Single-digit µs possible in the hot path. There is no GC, so the tail is flat. | No rigorous cited p99 (unverified). NautilusTrader is Rust-native (see §5). |
| (c) Go | µs-range hot path. GC pauses have historically been sub-100 µs (since Go 1.8). Green Tea GC arrived experimentally in 1.25 and became default in 1.26. | https://github.com/golang/go/issues/73581 **M**. The "40% lower pause" claim is **L**. |
| (d) Java/JVM | Disruptor: **52 ns mean per hop vs 32,757 ns for ArrayBlockingQueue**, measured on 2011 hardware with Java 6 (https://lmax-exchange.github.io/disruptor/disruptor.html) **H but dated**. Aeron on AWS c6in.16xlarge (published 2026-02-12, round-trip): at 100k msg/s, OSS Java p50 21 / p99 32 / p99.9 46 µs. At 1M msg/s, OSS Java p99 57 µs versus 39 µs for Premium with kernel bypass (https://aws.amazon.com/blogs/industries/aeron-on-aws-2025-performance-benchmark-results/) **M** (vendor with AWS). Chronicle Queue OSS stays "below 100 µs" 99.99% of the time, and Enterprise below 10 µs (vendor, https://github.com/OpenHFT/Chronicle-Queue) **M**. Generational ZGC pauses are sub-ms, typically 0.1–0.5 ms, and ZGC is generational-only in JDK 25 LTS (https://openjdk.org/jeps/439, https://inside.java/2023/11/28/gen-zgc-explainer/) **M-H**. | Azul Prime and GraalVM native were not researched (unverified). |
| (e) C++ (Seastar, Folly) | Sub-µs to single-digit µs hot paths are the norm in HFT. | Not researched; no cited numbers (unverified). |
| (f) kdb+/q, KDB-X | Tick-plus-analytics standard, and STAC-M3 is its benchmark. The **KDB-X Community Edition is free for commercial use** within limits: **16 GB RAM, 24 cores, 4 secondary threads/process, 16 connections/process, single instance** (https://code.kx.com/licensing/usage-restrictions.html) **H**. KDB-X GA was planned for early 2026 (https://www.businesswire.com/news/home/20251119593382/en/) **H**. | I found no cited in-memory tick-to-subscriber µs figure. |
| (g) Elixir/BEAM | Soft real-time with per-process GC and no global stop-the-world. Good for fan-out and notification. Heavy JSON and number parsing hurts the tail. | A forum microbenchmark shows BEAM beating tokio at message passing (https://elixirforum.com/t/.../44332) **L**. |

---

## 3. Stream processing and incremental engines

| Engine | Lang / License | Latency class | Status (2026) | Ops burden / small-team fit |
|---|---|---|---|---|
| Apache Flink (+PyFlink) | Java, Apache-2.0 | Tens to hundreds of ms typical, depending on checkpointing and buffers | 2.2.0 released 2025-12-04; 2.2.1 released 2026-05-15 (https://flink.apache.org/2026/05/15/apache-flink-2.2.1-release-announcement/) **H** | High: a JVM cluster plus state backend. Overkill for one user. |
| Arroyo | Rust, Apache-2.0 | Sub-second SQL windows | Joined **Cloudflare** 2025-04-10 and powers Cloudflare Pipelines. It stays OSS, but velocity slowed, with about 1 release (v0.15) in H2 2025 (https://www.arroyo.dev/blog/arroyo-is-joining-cloudflare/) **H**/**M** | Medium. Roadmap risk. |
| RisingWave | Rust, Apache-2.0 | Sub-second freshness. The vendor claims sub-100 ms. | Active | Medium (Postgres-wire). Vendor comparisons are biased. **M** |
| Materialize | Rust, BSL | Vendor claims single-digit ms freshness | **Self-Managed Community Edition is free**, capped at **24 GiB memory / 48 GiB disk** (https://materialize.com/blog/materialize-for-everyone/) **H**. This contradicts RisingWave's claim that Materialize is not self-hostable. | Medium |
| Feldera (DBSP) | Rust. Core MIT per repo (verify; an enterprise edition exists) | Incremental SQL over arbitrary queries, low-ms class | Very active, e.g. dbt-feldera 0.318.0 on 2026-07-08 (https://github.com/feldera/feldera) **M** | Low-medium. A strong incremental model. |
| Pathway | Python API over a Rust engine, **BSL 1.1** (converts to Apache after 4 years) | Vendor benchmark (2023) claims lower latency than Flink | Active (https://github.com/pathwaycom/pathway/blob/main/LICENSE.txt) **H** license / **L** perf | **Good fit for a Python team** |
| Bytewax | Python/Rust, Apache-2.0 | n/a | **The company is no longer commercially viable (May 2025).** The project is community-maintained and waxctl was archived 2025-03-20 (https://github.com/bytewax/bytewax) **H** | **Avoid for new builds** |
| Quix Streams | Python, Apache-2.0, Kafka-native | Bounded by Kafka latency (ms) | Active (https://github.com/quixio/quix-streams) **M** | Low if you already run Kafka or Redpanda |
| Timeplus Proton | C++ (ClickHouse-based), Apache-2.0 | Vendor claims 4 ms end-to-end and 90M EPS on an M2 Max laptop (https://www.timeplus.com/proton) **L-M** | Active | Low: a single binary |
| Kafka Streams | Java | ms-class | Mature | Needs Kafka |
| ksqlDB | Java, Confluent Community License | ms to s | Confluent promotes Flink. A "maintenance mode" claim comes from a third-party blog only, and I found **no official EOL** notice (https://docs.confluent.io/platform/current/ksqldb/overview.html) **L** | Avoid for new builds |
| Estuary | Managed CDC | Vendor claims sub-100 ms (https://estuary.dev/product/) **M** | Active | Useful for CDC, not tick analytics |
| Polars (streaming) | Rust/Python, MIT | **Batch / out-of-core, not an event-stream processor.** Use it for fast recompute per bar. | 2.0 RC released 2026-09-02 makes streaming the default LazyFrame engine (https://pola.rs/posts/announcing-polars-2/) **M-H** | Excellent in-process |
| DuckDB | C++, MIT | Batch. Suited to fast recompute or query, not incremental processing. | Mature | Excellent in-process |
| **Deephaven** | See §4 | Micro-batched incremental processing. Each cycle defaults to 1000 ms and can be tuned down. | | |

---

## 4. Time-series and tick databases (hot path)

### Deephaven (deep dive)
- **What it is**: a real-time, column-oriented, time-series analytics engine with relational features.
  - Changes (adds, removes, modifies and shifts) propagate incrementally through a live DAG, so only the changed rows recompute.
  - Processing is chunk-oriented, about 4,096 elements per chunk.
  - It came out of Walleye's trading systems (https://deephaven.io/core/docs/conceptual/deephaven-design/) **H**.
- **Update cadence**: the key latency knob.
  - `PeriodicUpdateGraph.targetCycleDurationMillis` defaults to **1000 ms**. It can be lowered, and `requestRefresh()` starts the next cycle "as soon as practicable".
  - Other settings: `minimumInterCycleSleep` (default 0), `updateThreads` (-1 means all CPUs), and `interCycleYield` (https://deephaven.io/core/42.3/docs/conceptual/periodic-update-graph-configuration/) **H**.
  - The docs describe 10–100 ms as a typical configured frequency **M**.
  - So Deephaven fits **tier A and the upper part of tier B (10–100 ms)**, not sub-ms.
- **Python**:
  - The Java engine is driven from Python via jpy.
  - `pip install deephaven-server` runs it without Docker, and Java 17–25 is required (https://github.com/deephaven/deephaven-core) **H**.
  - It supports Kafka, Parquet, CSV, Arrow and SQL ingestion, plus gRPC and Arrow Flight/Barrage clients.
- **Releases**: very active. 42.3 shipped 2026-07-28, and 41.3 through 42.3 all shipped in 2026 (https://github.com/deephaven/deephaven-core/releases) **M** (via search).
- **License**: the Community Core engine is under the **Deephaven Community License (DCLA)**.
  - It allows commercial use and distribution.
  - Its main restriction is that third parties may not add, define or modify schemas for *input* tables that the software accesses.
  - Clients, UI, Barrage and jpy are Apache-2.0 (https://deephaven.io/community/license/) **H**.
- **Fit**: a strong candidate for "live tables of bars, indicators and signals with a UI" for a Python-first small team. It ties the "JVM" reading of JEV to a Python workflow.

### Others
| DB | License | Notes |
|---|---|---|
| kdb+/KDB-X | Proprietary. The Community Edition is free, including commercial use, within 16 GB / 24 cores. | The gold standard for tick data. q has a steep learning curve, though Python and SQL interfaces now exist. **H** (limits) |
| QuestDB | Apache-2.0 | 10.0.x adds QWP (a binary columnar ingest protocol), Live Views (beta) and native arrays. The vendor claims 19M rows/s ingest (https://github.com/questdb/questdb/releases) **M**. The 10.0 release date is **unverified**: the fetch showed 2024, which conflicts with 9.x being 2025. |
| ClickHouse | Apache-2.0 | Excellent for analytics and bars. Not an event-driven hot path (unverified numbers). |
| DolphinDB | Proprietary, with a free community edition (limits unverified) | The vendor claims ms to sub-ms streaming engines (https://docs.dolphindb.com/en/Tutorials/streaming_tutorial.html) **L-M** |
| TimescaleDB | Core Apache-2.0. Advanced features (continuous aggregates, Hypercore) use the TSL, which is source-available and forbids offering it as a service. | The company renamed to **TigerData** on 2025-06-17 (https://www.tigerdata.com/legal/licenses) **M-H**. Good for the Postgres ecosystem, not for µs. |
| ArcticDB (Man Group) | **BSL 1.1**: free for non-commercial use, production needs an agreement, and it converts to Apache after 2 years | 6.23.0 shipped 2026-08-17. A serverless DataFrame store on S3 or LMDB. Good for history and research, not the live hot path (https://github.com/man-group/ArcticDB) **M-H** |

---

## 5. Messaging

| System | Latency (cited) | Notes |
|---|---|---|
| Aeron | OSS Java at 100k msg/s: p50 21 / p99 32 µs round-trip on AWS c6in.16xlarge. Aeron Cluster at 100k: p99 136 µs (OSS). | https://aws.amazon.com/blogs/industries/aeron-on-aws-2025-performance-benchmark-results/ **M** |
| Chronicle Queue | OSS stays below 100 µs 99.99% of the time (vendor) | **M** |
| iceoryx2 (shared-memory IPC, Rust) | About 100 ns polling mode (vendor). v0.9.0 released 2026-05-18, with 1.0 planned before end of 2026. | https://ekxide.io/blog/iceoryx2-0.9-release/ **M** |
| NATS JetStream | 1–5 ms p99 with R=3 (secondary sources). Core NATS without persistence is sub-ms. | **L** |
| Redpanda | The vendor claims p99 is 10× lower than Kafka and under 5 ms | **L-M** (vendor) |
| Kafka | 5–10 ms p99 when tuned (secondary) | **L** |
| Redis Streams | Sub-ms median in-memory (secondary) | **L** |
| ZeroMQ | Not researched (unverified) | |

For a small team: in-process queues first. Then NATS (simple) or Redis Streams if you need a bus. Kafka or Redpanda only when you need durability and replay at scale. Aeron or Chronicle only for tier C.

---

## 6. Rust/Python hybrid options
- **PyO3 + maturin**:
  - PyO3 0.26 supports Python 3.14 and free-threaded 3.14t, and PyO3 0.29.x now exists (https://github.com/pyo3/pyo3/releases) **M**.
  - This is the standard way to move a hot function into Rust.
- **Polars**: Rust core. The 2.0 RC (2026-09-02) makes streaming the default (https://pola.rs/posts/announcing-polars-2/) **M-H**.
- **NautilusTrader**:
  - A Rust-native, deterministic, event-driven trading engine with Python bindings.
  - Releases are frequent; 1.227.0 shipped 2026-05-18 and another release on 2026-09-02 (https://github.com/nautechsystems/nautilus_trader/releases) **M**.
  - LGPL-3.0 (verify).
  - A strong path to real order decisions later, because backtest and live share the same code.
- **Numba**: JIT for numeric loops. Mature (not re-verified).
- **Mojo**:
  - Mojo **1.0 was announced 2026-08-11**, and the compiler was open-sourced under Apache-2.0 with LLVM exceptions on 2026-08-18. Outside contributions to the compiler are not yet accepted (https://www.opensourceforu.com/2026/08/modular-launches-mojo-language/, https://www.phoronix.com/news/Modular-Mojo-Open-Source) **M**.
  - **Qualcomm announced its acquisition of Modular on 2026-06-24 (about $3.9B) and completed it on 2026-07-29** (https://www.qualcomm.com/news/releases/2026/06/qualcomm-to-acquire-modular) **H**.
  - Still young for finance I/O.
- **Cython**: mature and low-risk.
- **Codon**: switched from BSL to **Apache-2.0** in 2025 and added a compiled NumPy (https://www.exaloop.io/blog/codon-2025) **H**. It is not CPython-compatible for all libraries.

---

## 7. Architecture options

### (A) About 1 s end-to-end: recommended now
- **Fetch**:
  - Market data: a vendor websocket (Massive, Alpaca SIP, or Databento over the internet).
  - Filings: EDGAR polled at 10 req/s or less, with a User-Agent.
  - News: a vendor news websocket such as Benzinga.
- **Compute**: Python asyncio (uvloop, msgspec) in a single process. Keep in-memory rolling state or Polars/DuckDB per bar. Optionally use Deephaven as the live table and UI layer.
- **Decide**:
  - Deterministic rules via **GoRules Zen** (in-process Python binding, µs) or plain Python.
  - **Jev** (70–500 ms) only as an async enrichment step for text: news and filing materiality or sentiment.
  - Log every decision, and pin the Jev model version.
- **Notify**: Slack, Telegram, push or email.
- **Infra and team**: 1 developer, one VM (preferably us-east-1 near the vendor), roughly $50–300/month plus data fees (my estimate). Nothing new to learn.
- **Entitlements**:
  - A retail vendor plan. Alpaca Basic is free but IEX-only, and full SIP costs $99/mo on Algo Trader Plus.
  - Massive or Databento plans are an alternative.
  - Professional vs non-professional status affects cost (unverified).
  - EDGAR is free.

### (B) About 10–50 ms tick-to-alert
- Run in the **same cloud region or PoP as the feed**. Databento offers dedicated interconnects to AWS, GCP and Azure (https://databento.com/dedicated-connectivity) **M**. Even with an interconnect, us-east-1 is about 2+ ms one-way from NJ-originated data. That still fits this tier.
- Use Databento's binary DBN feed or Massive's in-region access, not a trans-continental websocket.
- Hot path in Rust (tokio) or Java (Disruptor, ZGC), or Python with PyO3 kernels. Deephaven with `targetCycleDurationMillis` at about 10–20 ms is an alternative (vendor-typical 10–100 ms).
- Messaging in-process or via core NATS.
- **No LLM or Jev in the hot path**. Semantic enrichment runs on a side lane.
- Measure latency against exchange timestamps. Massive's KB describes the method.
- Team: 1–2 developers with systems experience. Infra about $300–2k/month plus higher data tiers (my estimate).
- **Entitlements**: once signals feed automated orders, exchange and SIP **non-display use** licensing applies. Examples in the plan policies include "automated order or quote generation" and "price referencing for algorithmic trading". One source cites a fee of about **$3,500 per non-display application** (UTP/CTA policies: https://www.utpplan.com/DOC/datapolicies.pdf, https://www.ctaplan.com/publicdocs/ctaplan/notifications/trader-update/Policy%20-%20CTA%20Non%20Display%20with%20FAQ.pdf) **M** (current fee amounts unverified). Check whether your vendor's retail plan covers non-display or automated use.

### (C) Sub-ms
- **Requires colocation** at NY4/NY5 (Secaucus), Carteret (Nasdaq) or Mahwah (NYSE).
- **Direct exchange feeds** (ITCH, Pillar) over a cross-connect, not SIP via a vendor websocket. Even Databento's cross-connect is 42 µs p90. Its internet path is 590 µs p90 before any compute.
- C++, Rust or Java with Disruptor, Aeron or Chronicle, kernel bypass (Aeron Premium-class), CPU pinning, and no GC in the hot path. Most likely an FPGA or NIC-offload discussion follows.
- Requires:
  - exchange direct-feed licenses (per venue), plus non-display licensing
  - colocation rack and cross-connect fees
  - a broker-dealer or sponsored market-access relationship for orders
- Expect $10k+/month and specialist staff (my estimate; unverified).
- **Not appropriate** for an analysis and alerting product at this stage.

---

## 8. Unverified or open items
- Official source on ksqlDB status. I found no Confluent EOL notice.
- QuestDB 10.0 release date (conflicting year).
- Deephaven GitHub star count (fetched 362, which seems low; omitted).
- Rigorous p99 numbers for Python uvloop+msgspec, tokio, Go, Seastar/Folly, Azul Prime, GraalVM native, ZeroMQ, Kafka Streams, Agrona, Chronicle Map, and a ClickHouse hot path.
- kdb+ in-memory tickerplant-to-subscriber latency.
- DolphinDB community edition limits.
- Licenses for Feldera core (MIT per search), GoRules Zen (MIT?) and NautilusTrader (LGPL-3.0?). Verify on the repos.
- Benzinga or news-feed latency (only a third-party ~25 ms claim).
- Professional vs non-professional SIP entitlement costs and vendor redistribution terms.
- TypeSafe Jev: its serving region, p99, rate limits, and whether any equity-specific evals exist.
- The AWS us-east-1 to NY4 RTT (3–8 ms is from a snippet; the ~2 ms one-way floor is derived).
- The client location behind Databento's 590 µs internet p90 is not stated.
- Current SIP non-display fee amounts, and whether retail plans (Alpaca, Massive) license automated or non-display use.
- The Jev API open date and endpoint (snippet only).
- Literal "jev" packages on GitHub, PyPI or crates were not searched exhaustively.
