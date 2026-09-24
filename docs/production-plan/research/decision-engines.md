# Decision-System Tooling Research (US equities/ETFs)

Research date: 2026-09-24. All sources were accessed on 2026-09-24. Citations use the form `[S#·H/M/L]`: S# is a row in the Sources table at the end, and the letter is the confidence.

- **H**: confirmed on a primary page (repo, PyPI, or vendor docs).
- **M**: taken from a secondary source, or a primary page where the year or version had to be inferred.
- **L**: a single weak source, or conflicting sources.

Scope: ingest events (bars/ticks, news, SEC filings, earnings), evaluate rules and models, and emit alerts or decisions with an audit trail. Paper or live trading may come later. Only **US equities/ETFs** are in scope, so crypto-only tools are marked poor fit.

---

## 0. TL;DR

1. **The explainability core should be a deterministic rule engine.** The best fit is **GoRules Zen Engine + JDM**:
   - MIT license, Rust core, bindings for Python, Node, Go, JVM, .NET and more.
   - Microsecond evaluation, with a replayable trace for every decision [S1·H][S2·H].
   - Rules are JSON files that live in git, so each decision can be tied to a rule version by git SHA.
2. **CEL (cel-python / cel-go) is the lightweight alternative** for single-expression guards and filters [S9·H]. Use **OPA/Rego** or **Cedar** only if the decisions are really authorization or policy (for example "may this account trade X?").
3. **Everything is audited, but only deterministic parts can be replayed.**
   - For each decision, record: input snapshot, rule version (JDM + git SHA), engine trace, output, model version and features, and a durable-workflow ID.
   - Zen, CEL, OPA and Drools decisions can be **re-run bit-for-bit** from that record.
   - LLM and "Jev"-style calls can only be **recorded**, not reproduced. Keep them off the hot path and label them advisory.
4. **Backtest → paper → live with identical code, for US equities** (see the table in section 2):
   - **NautilusTrader via Interactive Brokers.** Use stable 1.x. v2 is still a release candidate, and its Alpaca adapter is only an RFC [S12·H][S13·H][S14·H][S15·H].
   - **QuantConnect LEAN via Alpaca, IBKR or Tradier** [S16·H].
5. **ML:** the default should be GBDT (LightGBM/CatBoost) compiled with lleaves or Treelite, or exported to ONNX Runtime, for microsecond-scale scoring. Add River for online drift and anomaly models.
   - **Time-series foundation models are weak for return forecasting.** Zero-shot out-of-sample R² was −1.37% and −2.80%, behind CatBoost [S31·H]. Gains over a random walk were "small and sparse" [S32·H].
   - Chronos-2 and TimesFM 2.5 have Apache-2.0 weights and are commercially usable [S27·H][S81·H][S82·H]. TimesFM 3.0 weights and Moirai 2.0 are **non-commercial** [S28·H][S30·H].
6. **LLMs:** use them for triaging news and filings and writing explanations, **not for the decision itself**. Recommended defaults:
   - **Claude Haiku 4.5** ($1/$5 per MTok, cache reads $0.10, structured outputs supported) [S37·H][S38·M].
   - **Gemini 2.5 Flash-Lite** ($0.10/$0.40) [S39·H].
   - Groq or Cerebras when open-model speed is needed [S40·M][S41·H].
7. **Durable execution / audit:** **DBOS** (MIT, Postgres-only, Python; 3.0.0 released Sep 16 2026) [S46·H] is the lowest-friction choice for a Python team. **Temporal** (MIT SDK 1.33.0) suits multi-service or polyglot setups [S47·H]. **Restate** is strong but its server is BSL [S48·H][S49·M].
8. **"JEV" means TypeSafe AI's Jev.** Jev 1.13 was released Sep 18 2026: a closed, hosted, waitlisted "System One" model that returns typed and calibrated decisions in 70–500 ms [S52·M]. It is **an LLM-style triage service, not an explainable rule engine**, and is too new and unverified for anything but experiments. Details in section 1.9.

---

## 1. Decision / rule engines with explainability

### 1.1 GoRules Zen Engine + JDM (deep dive)

| Attribute | Finding |
|---|---|
| What it is | Business-rules engine that evaluates **JDM (JSON Decision Model)** graphs made of nodes and edges. Node types: decision tables, switch, expression, function (JS) and reusable sub-decisions [S1·H][S3·H] |
| Language | Rust core. SDKs for Node.js, Python, Go, Rust, Java/Kotlin, C#, Swift and WASM (UniFFI-based bindings for the JVM and others) [S1·H][S3·H] |
| License | Engine: **MIT**. The JDM editor is a separate open-source React component. The **BRMS** (cloud or self-hosted management UI) is commercial, on Business and Enterprise plans [S1·H][S2·M] |
| Latest release | python / nodejs / uniffi **v2.0.2, Aug 24 2026**, a bug-fix release ("correct readme examples and java native library loader"). About 2.0k stars and 216 forks [S4·H] |
| Maturity | v2 line, active, releases GPG-signed [S4·H]. The community is small compared with Drools |
| Perf claims | Evaluates "in microseconds", precompiled, "allocation-light", identical results across platforms [S1·H]. These are vendor claims; there is no independent benchmark |
| Explainability | "Every answer comes with a replayable trace" [S1·H]: each node's input and output is recorded. JDM files are git-friendly JSON, and unknown top-level fields are ignored, so you can attach your own metadata such as a rule owner or rationale [S3·H] |
| Fit | **Excellent** for alert and decision rules. Analysts can edit decision tables in the visual editor while engineers keep them versioned in git. It embeds in-process in Python or Rust, so there is no network hop |
| Cost | Engine and editor are free. BRMS pricing is on request [S2·M] |
| Lock-in | Low. JDM is an open JSON format and the engine is MIT. Function nodes in JS reduce portability a little |

**Caveats:**
- Decision-table hit policies (first/collect) and the exact trace schema were not confirmed from the docs index. Check them in the JDM reference before building the audit schema (listed under Unverified).
- JS function nodes are an escape hatch. Restrict them in code review so rules stay declarative and auditable.

**How to use it here:**
- Keep one JDM graph per decision type, for example `earnings_surprise_alert.json` and `8k_item_triage.json`.
- Feature values come in as JSON context. Evaluate with `trace=True` and store the trace, the JDM git SHA and the input hash in the audit log.

### 1.2 Other engines

| Tool | What / language | License | Latest release | Fit / notes |
|---|---|---|---|---|
| **Drools / Apache KIE** | Java Rete/Phreak engine plus DMN, running in the JVM | Apache-2.0 (ASF incubating) [S5·H] | KIE **10.1.0 in Jul 2025**; **10.2.0 announced Apr 2026** [S6·H][S7·M]. The GitHub releases page returned garbled years, so the year here is inferred (M) | Most mature engine for a JVM team, with full DMN 1.x, FEEL and forward chaining. Heavy for Python teams. Explainability comes from DMN decision results and audit listeners |
| **DMN in Python** | pyDMNrules (DMN 1.3 via Excel workbooks and pySFeel), cDMN, dmn_python [S8·M] | Various, mostly OSS | Most of the documentation dates from 2022 or earlier [S8·M] | Poor to moderate fit. Low activity. Prefer Zen, or Drools DMN over REST |
| **CEL** (cel-python, cel-go) | Google Common Expression Language: non-Turing-complete, side-effect-free, linear-time | Apache-2.0 | cel-python **0.5.0, Jan 31 2026**, Beta, maintained by the Cloud Custodian team [S9·H]. cel-go has no GitHub releases (it uses tags); version not verified [S10·H] | Very good for **single expressions** such as filters, thresholds and user-defined alert conditions. Safe to accept from end users. Not a decision-table or graph tool. Explanations come from the expression plus the bound variables |
| **Open Policy Agent / Rego** | Go policy engine; Rego is a Datalog-like language | Apache-2.0 (CNCF) | **v1.21.0, Sep 24 2026**. This release added a `rule_labels` parameter to the Data/Query APIs [S11·H] | Good for **policy and entitlement** (who may see or trade what, and risk limits as policy). Decision logs are built in. Awkward for numeric scoring logic |
| **Cedar** | AWS authorization language written in Rust, with formal analysis | Apache-2.0 (license not visible on the page; M) | **v4.13.0, Sep 15 2026** [S17·H] | Authorization only (principal/action/resource). Not a fit for trading rules |
| **json-logic** | Rules stored as JSON ASTs; ports exist in JS and Python | MIT | The original Python package looks abandoned. `panzi-json-logic` and the Maykin Media fork are maintained [S18·M] | Fine for simple, UI-serializable conditions. No native trace |
| **durable_rules** | Rete engine in C, bound to Python, Node and Ruby | MIT | **2.0.28, Jun 7 2020** [S19·H] | **Stale. Avoid** for new work |
| **Esper** | Java/.NET CEP with EPL streaming SQL, time windows and pattern matching | **GPLv2**, commercial license available [S20·H] | 9.0.0, needs Java 17+. The release page shows no year [S21·M] | Strong for **temporal patterns** ("3 down-bars then volume spike within 5 min"). GPL is a trap if you distribute. JVM only |
| **Siddhi** | Java CEP, formerly from WSO2 | Apache-2.0 | Development has effectively moved into WSO2 products; the SourceForge project is retired [S22·M] | Low activity. Avoid for new work |

**Cost, lock-in and performance for table 1.2:**
- **Cost:** free OSS libraries, except Esper (commercial license if you redistribute) and Drools (Red Hat/IBM paid support is optional).
- **Lock-in:** low for CEL, OPA and Cedar, which are embeddable and have standard or specified languages. Lock-in is also low for Drools DMN, because DMN is an OMG standard; Drools DRL is Drools-specific. Esper EPL is moderate.
- **Performance:** no vendor figures were collected. CEL is linear-time by design. OPA and Cedar evaluate in-process in µs to sub-ms (general knowledge, M).

**Decision tables vs CEP:** Zen, CEL and OPA do not handle windows or time on their own. Do temporal aggregation *upstream*, in Polars or Nautilus indicators, or in Esper if you are on the JVM, and feed the resulting features to the rule engine. This keeps rules stateless and replayable.

### 1.9 "JEV": what the search found

- **TypeSafe AI "Jev"** is a proprietary "System One" decision model.
  - It reads text or JSON state and returns **typed answers** (a choice, a rubric score, or yes/no) with calibrated confidence. It does not generate free text.
  - Jev 1.13 was released **Sep 18–19 2026**. Latency is **70–500 ms end-to-end**, and the vendor demo showed 0.114 s.
  - Pricing is **$0.042 per M input tokens, with output free**.
  - It is a hosted API in **early access behind a waitlist**, with **no weights, no parameter count and no self-hosting**.
  - The architecture is undisclosed ("new architecture, parallel sampler, RLCD").
  - Benchmarks are vendor-run: "193.6x faster, 444.6x cheaper" than GPT models, and the vendor says real-world gains will be at the low end.
  - The docs state that answers can still be wrong [S52·M][S53·M].
- **Registries:**
  - **PyPI `jev` 0.3.0** (Sep 18 2026): a decorator that compiles Python functions into Jev queries, published by a third party [S54·H].
  - **crates.io `jev` 0.1.2** (Sep 22 2026): a client for the "TypeSafe System One API and compatible self-hosted backends" [S55·H].
  - **npm `jev`**: an unrelated empty 0.0.0 package from 2022 [S56·H].
- **GitHub:** many small repos appeared within days, all low signal:
  - `swisnl/decision-engine` (PHP, MIT, 1 commit, claims about 100 ms calls) [S57·H]
  - `jev-control-plane`, `awesome-jev`, and "Verdict-open-jev" [S58·L]
- **Conflicts (L):** an "awesome-jev" catalog claims "896 verified projects" only days after launch, and one repo claims Jev runs on "DiffusionGemma 26B-A4B". Both contradict the vendor's "architecture undisclosed / no weights" statement [S52·M vs S58·L]. The Jev facts come from a secondary source (MarkTechPost); no TypeSafe-owned page was fetched. Treat them as unreliable.
- The OpenRouter listing link returned **404** [S59·H]. Vercel AI Gateway availability is reported but was not verified [S52·M].
- **Assessment:** Jev may be useful as a *cheap, fast classifier* for triage, for example "is this 8-K material? → {none, low, high}". It is **not** a replacement for an explainable rule engine:
  - It is network-bound and closed.
  - Its outputs cannot be reproduced for audit.
  - It is five days old.
  If you use it, log the full request, response, model version and confidence, and gate actions on a deterministic rule.
- No trading-specific "JEV" project was found.

---

## 2. Trading / backtest / live frameworks

| Framework | Lang | License | Latest | US equities live | Same code backtest → paper → live? | Notes |
|---|---|---|---|---|---|---|
| **NautilusTrader** | Rust core, Python API | **LGPL-3.0** [S12·H] | Stable **1.231.0** on PyPI [S13·H]. **2.0.0rc5, Sep 15 2026** (full Rust + PyO3 rewrite, Cython removed) [S14·H]. The vendor says RCs should *not* be used for live capital [S13·H] | **Interactive Brokers** (stable) and **Databento** data (stable), among 22 integrations [S15·H]. **Alpaca: only an RFC** (issue #3374) [S60·H] | **Yes.** "The same strategy and execution-algorithm code can run across backtest and live" [S12·H]. Paper trading via IB paper accounts | Nanosecond event-driven engine, about 29k stars [S12·H]. Breaking changes between releases [S12·H]. Best OSS choice if you want Rust speed and a Python API |
| **LEAN (QuantConnect)** | C#, Python | Apache-2.0 [S16·H] | Active; about 21.8k stars; needs .NET 10 SDK [S16·H] | **Alpaca, IBKR, Tradier** [S16·H] | **Yes.** One algorithm runs in backtest, paper and live | Most complete US-equities data and brokerage coverage. Cloud: Researcher about $60/mo; live nodes from about $24/mo [S61·M] |
| **QuantConnect cloud** | as LEAN | SaaS | — | as LEAN | Yes | Lock-in comes from the data licensing and cloud IDE. LEAN itself is portable |
| **Barter-rs** | Rust | MIT | Active (date not shown) [S62·H] | Mainly crypto integrations | Near-identical via mock components [S62·H] | Explicitly **not for production or live use** [S62·H]. Poor fit |
| **hftbacktest** | Rust, Python (Numba) | MIT | Active, about 4.8k stars [S63·H] | Live only on **Binance Futures and Bybit** [S63·H] | Rust only | Queue-position and latency modelling on L2/L3 data. Overkill and a poor fit for US equities unless you buy L3 data |
| **Hummingbot** | Python | Apache-2.0 | Active [S64·H] | **Crypto only** [S64·H] | — | Poor fit |
| **freqtrade** | Python | GPL-3.0 (not re-verified) | **2026.8**; the fetched page said "Aug 31 2024", but 2026 is inferred from the version [S65·M] | **Crypto only** | Yes, for crypto | Poor fit |
| **Jesse** | Python | MIT [S66·H] | Date not shown | **Crypto only** [S66·H] | Yes, for crypto. Whether live trading needs a paid license is unclear (Unverified) | Poor fit |
| **vectorbt PRO** | Python/Numba, Rust core claimed | Proprietary membership; source visible to members; no competing use [S67·H] | — | **No live trading mentioned** [S67·H] | No | Fastest vectorized research tool; claims "4.7B bars/s" on an M3 (vendor benchmark) [S67·M]. Research only |
| **Zipline-reloaded** | Python | Apache-2.0 | **3.1.1, Jul 19 2025** [S68·H] | No | No | Legacy Quantopian API. Research only |
| **Ziplime** (Polars rebuild of Zipline) | Python/Polars | not verified | 2026 [S69·M] | Claims stocks and ETFs live | Claimed | New, unverified maturity |
| **bt** | Python | MIT | **1.2.3, Dec 24 2024** [S70·H] | No | No | Portfolio and allocation backtests only |
| **Backtesting.py** | Python | **AGPL-3.0** [S71·H] | **0.6.6, Jul 22 2026** [S71·H] | No | No | AGPL is a trap for a hosted product |
| **PyBroker** | Python/Numba | **Apache-2.0 + Commons Clause** [S72·H] | Active, about 3.5k stars [S72·H] | Alpaca data; live trading unclear [S72·M] | Partial | Commons Clause forbids selling the software, which is a trap for a commercial tool |
| **Polars-based backtesters** | Python/Polars | various | PolarBT (Mar 2026), polars_backtest_extension (updated Jul 2026), backtest-lib [S69·M] | No | No | Young projects. Fine for vectorized research. Polars itself is **1.44.2**, MIT [S73·H] |

**Cost, lock-in and performance for table 2:**
- **Cost:** free OSS unless noted. The paid options are QuantConnect cloud (about $60/mo plus nodes) [S61·M] and the vectorbt PRO membership (price not verified). Market data is the real cost (Databento, IB market-data subscriptions, Alpaca SIP) and was not researched here.
- **Lock-in:**
  - NautilusTrader and LEAN: moderate, because strategies are written against framework APIs.
  - QuantConnect cloud: higher, because of the data licences and cloud IDE.
  - vectorbt PRO: proprietary.
  - LGPL (Nautilus) is fine for use as a library.
  - AGPL (Backtesting.py) and Commons Clause (PyBroker) are traps for commercial use.
- **Performance claims:**
  - Nautilus: Rust core, nanosecond resolution [S12·H].
  - vectorbt PRO: 4.7B bars/s (vendor) [S67·M].
  - hftbacktest: queue and latency realism, not throughput [S63·H].
  - The others made no claims.

**Parity answer:** for US equities, only **NautilusTrader (IB)** and **LEAN (Alpaca/IBKR/Tradier)** give credible identical-code backtest, paper and live today. Everything else is research-only or crypto-only.

**Recommended pattern:**
1. Do vectorized research in Polars or vectorbt.
2. Put the validated signal into the event-driven engine as a feature producer.
3. Keep the **decision rules in Zen or CEL, outside the strategy class**. The same JDM file is then evaluated in backtest and in live trading, which gives rule-level parity even across frameworks.

---

## 3. Real-time ML, online learning and features

| Tool | What | License | Latest | Fit / notes |
|---|---|---|---|---|
| **Polars** | Rust DataFrame and streaming engine | MIT | 1.44.2 [S73·H] | The backbone for bar and feature computation in Python. Use lazy mode with `group_by_dynamic` for rolling features |
| **River** | Online ML: incremental models, drift detection, anomaly detection | BSD-3 | **0.26.1, Aug 21 2026** [S23·H] | Good for per-event updates (drift detectors, online anomaly scores on volume and spreads). Not a replacement for batch GBDT alpha models |
| **Feast** | OSS feature store | Apache-2.0 | **v0.66.0, Aug 21 2026** [S24·H] | Only needed with many models and teams. For a single app, Postgres or Redis plus Polars is enough |
| **Tecton** | Real-time feature platform | commercial | **Acquired by Databricks, Aug 2025**, being folded into Databricks and Agent Bricks [S25·M] | Not a standalone option any more. Avoid unless you are on Databricks |
| **Fennel** | Incremental feature engine | commercial | **Acquired by Databricks, Apr 2025** [S26·M] | Same as Tecton |
| **Chronon (Airbnb)** | Feature definition, backfill and serving on Spark and Flink | Apache-2.0 | Active; used at Airbnb, Stripe, OpenAI and others [S33·H] | Heavy (Scala, Spark, Flink, Bazel). Overkill here |
| **Pathway** | Python API on a Rust Differential Dataflow engine; unified batch and stream; LLM xpack | **BSL 1.1** (converts to Apache after 4 years) [S34·H] | active | Interesting for live news and RAG plus streaming joins. The BSL terms need review for commercial use |
| **ONNX Runtime** | Cross-framework inference | MIT | **v1.30.0, Sep 10**; the fetch said 2024, 2026 is inferred [S35·M] | Standard for low-latency NN or GBDT inference (tree ensembles via onnxmltools). Single-row CPU inference is typically tens of µs (general knowledge, not benchmarked here) |
| **lleaves** | LLVM compiler for LightGBM | MIT | active [S36·H] | Claims ≥10x speedup: **9.6 µs vs 52 µs single-row** on NYC-taxi [S36·H] |
| **Treelite** | Model compiler for XGBoost, LightGBM and sklearn | Apache-2.0 | **4.7.2**; the fetch said Sep 2 2024, but sklearn 1.10 support implies 2026 [S74·M] | Codegen moved to TL2cgen (general knowledge, M) |

**Cost and lock-in for the ML tools:**
- Everything above is free OSS, except Tecton and Fennel, which are now Databricks-only (**high lock-in**), and Pathway (BSL).
- Lock-in is low when you standardize on ONNX, LightGBM text models and Parquet features.

### Time-series foundation models, and whether they help with returns

| Model | License | Latest | Notes |
|---|---|---|---|
| **Chronos-2 / Chronos-Bolt** (Amazon) | **Apache-2.0** code and weights [S27·H][S82·H] | Chronos-2, **Oct 2025**, 120M parameters, covariate support. Bolt: "up to 250x faster" than the original Chronos [S27·H] | Commercially clean |
| **TimesFM 2.5 / 3.0** (Google) | Code Apache-2.0. **2.5 weights: Apache-2.0** [S81·H]. **3.0 weights: non-commercial** [S28·H] | 3.0, **Aug 2026**, multivariate with covariates. 2.5 has 16k context. About 48 ms per call (MLX on M4 Max, ctx 512, horizon 64) [S28·H] | License trap for 3.0 |
| **Moirai 2.0** (Salesforce) | **CC-BY-NC-4.0** weights [S30·H] | 2025 | Non-commercial |
| **TimeGPT** (Nixtla) | Closed model; SDK Apache-2.0; enterprise pricing, 30-day trial [S29·M] | — | Hosted API, adds network latency. Vendor lock-in |

**Evidence on returns forecasting (weak):**
- Rahimikia, Ni and Wang (Nov 2025) tested zero-shot TSFMs on daily excess returns:
  - Chronos-large reached **R² −1.37%** with about 51% directional accuracy.
  - TimesFM-500M reached **−2.80%**, with directional accuracy below 50%.
  - Linear models scored −0.47% and CatBoost −0.10%.
  - Only models **pre-trained from scratch on financial data** helped [S31·H].
- Noguer i Alonso and Pereira Franklin (Jun 2026) tested five TSFMs on five US stocks. Gains over a random walk were "small and sparse", with statistical significance only for Chronos on AMZN and Moirai-2.0 on GOOG. They conclude TSFMs are "not universal engines for … reliable alpha" [S32·H].
- **Verdict:** do not use TSFMs as alpha. Possible uses are **volatility and volume forecasting, and anomaly baselines** (for example "is today's volume unusual versus the Chronos forecast band?"), where the signal is stronger. That use is not verified here.

---

## 4. Fast LLM inference for event triage and explanations

| Option | Pricing / speed | Notes |
|---|---|---|
| **Claude Haiku 4.5** | $1 in / $5 out per MTok. Cache write $1.25, **cache read $0.10**. Batch −50% [S37·H] | **Structured outputs** (JSON-schema constrained decoding plus `strict` tools) are supported on Haiku 4.5. The docs say GA, but examples still show the `structured-outputs-2025-11-13` beta header [S38·M]. Good default for summarizing filings and news into a typed schema |
| **Gemini 2.5 Flash-Lite** | $0.10 / $0.40; cache $0.01 [S39·H] | Cheapest option |
| **Gemini 3.1 Flash-Lite** | $0.25 / $1.50 [S39·H] | Newer |
| **Gemini 3.5 Flash-Lite** | $0.30 / $2.50 [S39·H] | Newer |
| **Cerebras** | about 3,000 tok/s on gpt-oss-120B, about 2,500 on Llama 3.3 70B / Llama 4 Maverick [S40·M] | Fastest throughput for open models. Figures are from secondary blogs |
| **Groq** | about 400–500 tok/s on the same models [S40·M] | Low, consistent TTFT. **Vendor risk:** in Dec 2025 Nvidia licensed Groq's technology and hired its leadership for about $20B. GroqCloud continues independently under a new CEO [S41·H] |
| **SambaNova** | about 132 tok/s on Llama 405B; about 255 on DeepSeek R1 [S40·L] | Older figures |
| **TypeSafe Jev** | $0.042 per M input tokens, output free, 70–500 ms [S52·M] | Typed decisions only. Waitlisted. See section 1.9 |
| **Semantic caching** | Redis LangCache (managed, REST API) [S42·H]; GPTCache (Zilliz OSS, maintenance unclear) [S43·M] | Limited value here, because news and filings are mostly unique. Exact-match and prompt caching (static system prompt and schema) give more |

**Guidance:**
- **Never put an LLM on the decision hot path.**
  - Latency is 100 ms to seconds.
  - Outputs are non-deterministic and cannot be replayed.
  - Prompt injection via news or filing text is a risk.
- Use LLMs asynchronously to:
  1. classify and extract structured fields from 8-Ks, earnings releases and news (with a schema), then feed those fields into Zen rules;
  2. write human-readable explanations *from the Zen trace* after the decision is made.
- Cache the static system prompt and schema. Use batch mode for backfills.
- Speculative decoding is provider-internal. It lowers vendor latency but is not something you control (not verified per vendor).

---

## 5. Agent frameworks for research workflows

| Framework | License | Latest | Fit / caution |
|---|---|---|---|
| **LangGraph** | MIT | **1.2.12, Sep 21 2026** [S44·H] | Stateful graphs, checkpointing, human-in-the-loop. Mature. Brings in the LangChain ecosystem |
| **Pydantic AI** | MIT | **2.49.0, Sep 24 2026** [S45·H] | Typed outputs and dependency injection. The cleanest fit for a Python-first, type-safe codebase. Very fast release cadence, so pin versions |
| **Claude Agent SDK** | MIT (SDK) | **0.2.159, Sep 23 2026** [S50·H] | Claude Code harness with hooks and in-process MCP tools. Pre-1.0 and Claude-only |
| **Google ADK** | Apache-2.0 | **2.9.2, Sep 18 2026** [S51·H] | Graph workflow runtime, agent-to-agent tasks. Leans towards Gemini and GCP |
| **CrewAI** | MIT | **1.15.22, Sep 16 2026** [S75·H] | Role-based crews plus Flows. Tracing and control plane are in the paid AMP suite |
| **OpenBB** | ODP: **AGPL**. Agent "Rita": **MIT** (Jun 2026) [S76·M] | — | Workspace (hosted) supports custom agents. OpenBB has said the suite will move to a permissive license (M). Useful as a data layer and UI for research. AGPL affects any hosted product that embeds ODP |

**Caution:** agents belong in **research and analyst-assist** work, such as drafting rules or summarizing filings. They must not auto-promote rules to production. Treat agent-proposed JDM changes as pull requests that need human review and a backtest.

---

## 6. Event sourcing, durable execution and audit

| Tool | What | License | Latest | Fit |
|---|---|---|---|---|
| **DBOS Transact (Python)** | Durable workflows, queues, scheduling and exactly-once processing, **checkpointed in Postgres**, as a library | MIT | **3.0.0, Sep 16 2026** [S46·H][S77·H] | **Best fit for a Python-first team.** Workflow and step history are Postgres rows, so audit data can be queried with SQL. No extra servers |
| **Temporal** | Durable workflows with a full event history and deterministic replay | SDK MIT [S78·H]. Server MIT (not verified here, M) | Python SDK **1.33.0, Sep 15 2026** [S47·H][S78·H] | Best for polyglot or multi-service setups and long-running workflows. Needs a Temporal cluster or Temporal Cloud. Workflow code has determinism constraints |
| **Restate** | Rust durable runtime; SDKs for TS, Java/Kotlin, Python, Go and Rust | Server **BSL 1.1**. Free to use except to run a managed Restate service for third parties. Converts to Apache-2.0 four years after each release [S83·H]. SDKs MIT [S49·M] | **v1.7.12, Sep 22 2026** [S48·H] | Low latency, single binary. The BSL is fine for internal use |
| **KurrentDB** (formerly EventStoreDB) | Purpose-built event store | **Kurrent License v1** (renamed from ESLv2 with v25.0, Mar 2025) [S79·H] | **v26.1.2**; the fetch said 2024, 2026 is inferred from the version [S80·M] | Useful if you want event sourcing as the system of record. KLv1 terms not reviewed (Unverified). A Postgres append-only table is enough for most needs |

**Audit record (recommended schema, one row per decision):**
- `decision_id`
- `event_ids[]`: the source events with their provider timestamps and ingest timestamps
- `as_of_ts`
- `input_snapshot_hash` and a pointer to a blob holding the full JSON context
- `rule_id`, `rule_version` (JDM git SHA), `engine` and `engine_version`
- `trace` (JSON)
- `model_ids` and versions, plus the feature vector hash
- `llm_calls[]`: provider, model, prompt hash, response and confidence; advisory only
- `output` and `action`
- `workflow_id` (DBOS or Temporal)
- `operator_override`

Replay means: load the snapshot, check out the rule SHA, re-run the engine, and diff the result.

**Determinism conditions for bit-for-bit replay:**
- the engine version is pinned;
- all time comes from `as_of_ts` in the input, never from a wall-clock read inside rules;
- function and JS nodes make no `now()`, random or I/O calls (this is the main reason to restrict them);
- the feature snapshot is stored, not recomputed from vendor data that may later be revised or corrected.

**Cost and lock-in for durability tools:**
- DBOS and Temporal self-hosted are free. Temporal Cloud and DBOS Cloud are paid.
- Lock-in is moderate. Workflow code is written against each SDK's programming model, while the audit table in plain Postgres stays portable.

---

## 7. Recommended decision stacks

### (a) Python-first team

- **Ingest:** Polars for bars and features. SEC EDGAR, news and earnings go into Postgres as append-only event tables.
- **Rules:** **Zen Engine (Python binding) + JDM in git**, plus **cel-python** for user-defined alert expressions.
- **Models:** LightGBM compiled with **lleaves**, or exported to ONNX Runtime. **River** for drift and anomaly detection.
- **Durability and audit:** **DBOS** on the same Postgres. The audit table follows section 6.
- **LLM (async):** Haiku 4.5 or Gemini Flash-Lite with structured outputs, to extract filing and news fields and write explanations from the trace.
- **Trading, later:** **NautilusTrader stable 1.x + IB**, or **LEAN + Alpaca**. The Zen decision is called from the strategy's `on_bar` or `on_data`. Starting on Nautilus 1.x means a later migration to the v2 Rust/PyO3 rewrite (2.0.0rc5 is dated Sep 15 2026). Plan for API churn.
- **Explainability story:** every alert shows the Zen trace, rendered as "table X row 3 matched: surprise > 5% AND rel_vol > 2", plus the rule version and input snapshot. The LLM text is labelled as a narrative, not the reason.

### (b) Rust/Python hybrid

- **Hot path in Rust:** an event loop on NautilusTrader's Rust core (v2 once it is GA), or a custom tokio pipeline, calling the **zen-engine crate in-process** (sub-ms).
- **Features:** Polars in Rust. GBDT via Treelite/TL2cgen codegen or ONNX Runtime (Rust bindings).
- **Research:** Python with Polars and vectorbt PRO (if the license is acceptable), then promote the same JDM files into production.
- **Durability:** **Restate** (Rust-native, but review the BSL) or **Temporal**. The audit store is Postgres, or KurrentDB if you want native event sourcing.
- **Explainability:** the same JDM and trace artifacts across Rust and Python bindings, and Zen promises identical results across platforms [S1·H].

### (c) JVM team

- **Rules:** **Drools/Apache KIE 10.x with DMN** (the standard notation, which business users can read), or **Zen via the JVM/UniFFI binding** if you want JDM portability.
- **CEP:** **Esper** for temporal patterns (buy a commercial license if you distribute) [S20·H].
- **Trading:** none of the frameworks in scope is JVM-native and supports backtest → live. LEAN runs on .NET (C#). The JVM option is the IB Java API directly, with your own simulator and the same rule artifacts.
- **Durability:** **Temporal Java SDK**. The audit store is Postgres or KurrentDB.
- **Explainability:** DMN decision-result events plus Drools audit listeners, the rule-artifact version (kjar GAV), and the input snapshot.

**Common to all stacks:**
- Rules and model artifacts are versioned in git or a registry.
- Every decision is replayable from a snapshot.
- LLMs and Jev are advisory and logged.
- Alerts go live before paper trading, and paper trading before live trading. Each promotion needs a backtest of the same JDM version.

---

## 8. Unverified items / open questions

- Zen JDM decision-table **hit policies** (first/collect) and the exact **trace JSON schema**. Read the docs.gorules.io reference pages.
- **GoRules BRMS pricing** (on request).
- **cel-go** latest version (no GitHub releases; check pkg.go.dev).
- **OPA governance** after Styra's maintainers moved (reported 2025) and whether that affects the cadence. The release cadence looks healthy [S11·H].
- **KurrentDB KLv1** actual terms (what is free vs paid).
- **Siddhi** repo status (siddhi-io/siddhi), which looks dormant.
- **Jesse** live-trading license (free vs paid plugin). **freqtrade** license not re-checked.
- **vectorbt PRO** membership price.
- **Chronon** commercial steward (Zipline AI?), not confirmed.
- **Pathway BSL** "additional use grant" details.
- **ONNX Runtime 1.30, Treelite 4.7.2 and KurrentDB 26.1.2** release years were inferred as 2026 because the fetched pages showed 2024.
- **Esper 9.0.0** release year.
- **Drools 10.2.0** exact date: the announcement says Apr 2026, but the GitHub page showed garbled years.
- **Cerebras / Groq / SambaNova** tok/s figures come from secondary blogs. Check artificialanalysis.ai before relying on them.
- **Jev:** OpenRouter availability (404), Vercel AI Gateway availability, independent benchmarks, and the "DiffusionGemma" and "896 projects" claims (L). Also whether a dedicated TypeSafe docs domain exists; jevtypesafeai.com looks third-party.
- **Ziplime** license and live-trading maturity. **PyBroker** live-trading support.
- **TSFMs for volatility/volume** (as opposed to returns): plausible but not verified here.
- **Speculative decoding** usage per provider.
- **NautilusTrader 1.231.0** release date (PyPI JSON gave no date).
- **Temporal server** license (assumed MIT).
- **Tecton acquisition** details: $900M valuation (secondary source) and exact product continuity.

---

## Sources (all accessed 2026-09-24)

| # | URL |
|---|---|
| S1 | https://github.com/gorules/zen |
| S2 | https://docs.gorules.io/ |
| S3 | https://docs.gorules.io/reference/json-decision-model-jdm |
| S4 | https://github.com/gorules/zen/releases |
| S5 | https://github.com/apache/incubator-kie-drools/releases |
| S6 | https://kie.apache.org/blog/kie_10_1_0_release/ |
| S7 | https://kie.apache.org/blog/kie_10_2_0_release/ |
| S8 | https://github.com/russellmcdonell/pyDMNrules ; https://cdmn.readthedocs.io/en/latest/DMN_guide.html |
| S9 | https://pypi.org/project/cel-python/ |
| S10 | https://github.com/google/cel-go/releases |
| S11 | https://github.com/open-policy-agent/opa/releases |
| S12 | https://github.com/nautechsystems/nautilus_trader |
| S13 | https://pypi.org/pypi/nautilus_trader/json |
| S14 | https://github.com/nautechsystems/nautilus_trader/releases |
| S15 | https://nautilustrader.io/docs/latest/integrations/ |
| S16 | https://github.com/QuantConnect/Lean |
| S17 | https://github.com/cedar-policy/cedar/releases |
| S18 | https://github.com/panzi/panzi-json-logic ; https://github.com/maykinmedia/json-logic-py ; https://snyk.io/advisor/python/json-logic |
| S19 | https://pypi.org/project/durable-rules/ |
| S20 | https://www.espertech.com/esper/esper-license-and-trademark/ |
| S21 | https://github.com/espertechinc/esper/releases |
| S22 | https://siddhi.sourceforge.net/ ; https://openhub.net/p/siddhi-cep |
| S23 | https://pypi.org/project/river/ |
| S24 | https://github.com/feast-dev/feast/releases |
| S25 | https://www.mi-3.com.au/27-08-2025/databricks-acquires-tecton-boost-real-time-ai-agent-capabilities ; https://blogs.perficient.com/2025/09/26/databricks-acquires-tecton/ |
| S26 | https://siliconangle.com/2025/04/17/databricks-buys-feature-engineering-startup-fennel-enhance-ai-model-development/ |
| S27 | https://github.com/amazon-science/chronos-forecasting |
| S28 | https://github.com/google-research/timesfm |
| S29 | https://github.com/Nixtla/nixtla/blob/main/README.md ; https://www.g2.com/products/nixtla/pricing |
| S30 | https://huggingface.co/Salesforce/moirai-2.0-R-small |
| S31 | https://arxiv.org/abs/2511.18578 |
| S32 | https://arxiv.org/abs/2606.27100 |
| S33 | https://github.com/airbnb/chronon |
| S34 | https://github.com/pathwaycom/pathway |
| S35 | https://github.com/microsoft/onnxruntime/releases |
| S36 | https://github.com/siboehm/lleaves |
| S37 | https://claude.com/pricing |
| S38 | https://platform.claude.com/docs/en/build-with-claude/structured-outputs |
| S39 | https://ai.google.dev/gemini-api/docs/pricing |
| S40 | https://inworld.ai/resources/fastest-llm-inference-api ; https://fast.io/resources/fastest-ai-2026/ |
| S41 | https://groq.com/newsroom/groq-and-nvidia-enter-non-exclusive-inference-technology-licensing-agreement-to-accelerate-ai-inference-at-global-scale ; https://www.cnbc.com/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html |
| S42 | https://redis.io/docs/latest/develop/use-cases/semantic-cache/ |
| S43 | https://github.com/zilliztech/gptcache |
| S44 | https://pypi.org/project/langgraph/ |
| S45 | https://pypi.org/project/pydantic-ai/ |
| S46 | https://pypi.org/project/dbos/ |
| S47 | https://github.com/temporalio/sdk-python/tags |
| S48 | https://github.com/restatedev/restate/releases |
| S49 | https://news.ycombinator.com/item?id=42821705 |
| S50 | https://pypi.org/project/claude-agent-sdk/ |
| S51 | https://pypi.org/project/google-adk/ |
| S52 | https://www.marktechpost.com/2026/09/19/typesafe-ai-releases-jev/ |
| S53 | https://www.firecrawl.dev/blog/what-is-jev ; https://flaviocopes.com/jev/ |
| S54 | https://pypi.org/pypi/jev/json |
| S55 | https://crates.io/api/v1/crates/jev |
| S56 | https://registry.npmjs.org/jev |
| S57 | https://github.com/swisnl/decision-engine |
| S58 | https://github.com/heyjunpenn/awesome-jev ; https://github.com/yeqin4814/jev ; https://github.com/JxWayne890/jev-control-plane |
| S59 | https://openrouter.ai/typesafe/jev-1.13 (404) |
| S60 | https://github.com/nautechsystems/nautilus_trader/issues/3374 |
| S61 | https://www.quantconnect.com/pricing/ ; https://newyorkcityservers.com/blog/quantconnect-review |
| S62 | https://github.com/barter-rs/barter-rs |
| S63 | https://github.com/nkaz001/hftbacktest |
| S64 | https://github.com/hummingbot/hummingbot |
| S65 | https://github.com/freqtrade/freqtrade/releases |
| S66 | https://github.com/jesse-ai/jesse |
| S67 | https://vectorbt.pro/ |
| S68 | https://pypi.org/project/zipline-reloaded/ |
| S69 | https://pypi.org/project/polarbt/ ; https://github.com/Limex-com/ziplime ; https://github.com/Yvictor/polars_backtest_extension |
| S70 | https://pypi.org/pypi/bt/json |
| S71 | https://pypi.org/project/backtesting/ |
| S72 | https://github.com/edtechre/pybroker |
| S73 | https://pypi.org/pypi/polars/json |
| S74 | https://github.com/dmlc/treelite/releases |
| S75 | https://pypi.org/project/crewai/ |
| S76 | https://openbb.co/blog/introducing-agent-rita/ ; https://openbb.co/products/odp/ |
| S77 | https://github.com/dbos-inc/dbos-transact-py |
| S78 | https://github.com/temporalio/sdk-python |
| S79 | https://www.kurrent.io/releases/kurrentdb/25-0/ |
| S80 | https://github.com/kurrent-io/KurrentDB/releases |
| S81 | https://huggingface.co/google/timesfm-2.5-200m-pytorch |
| S82 | https://huggingface.co/amazon/chronos-2 |
| S83 | https://github.com/restatedev/restate/blob/main/LICENSE |
