# 300 ms market-assistant answer path, plus a TypeSafe Jev deep dive

> **Corrections (2026-09-24, achievability round; see [17](../17-what-is-achievable.md)):**
> - Mumbai → US-East now measures **193 ms**. From India, US-East is not slower than US-West (198 vs 210 ms, Microsoft data).
> - **Gemini 2.5 Flash-Lite and 2.5 Flash retire on Vertex (which has a Mumbai region) on 2026-10-20.** OpenAI's India endpoint stores data in India but does **not** process it there ([build-cost-latency](build-cost-latency.md)).
> - ElastiCache for Valkey is confirmed in Mumbai. Mumbai ↔ Hyderabad is 13.7 ms, which makes Hyderabad viable as a DR region.

Research date: **2026-09-24**. Every URL was accessed on 2026-09-24. Author: tech-scout. Nothing was installed or run. Package facts come from read-only PyPI JSON.

Confidence: **H** = primary source, or several sources agree. **M** = vendor claim or one credible secondary source. **L** = search snippet, summarizer output that could not be cross-checked, or my own derivation.

---

## 0. Bottom line

1. **Define "300 ms" as server-side time to first useful content (TTFUC), measured at the regional ingress (AWS ap-south-1 / GCP asia-south1 for India users).** The last mile on Indian mobile networks (roughly 30–150 ms or more, uncontrolled) comes on top of that. Budget the server at **p95 ≤ 120 ms TTFUC** so user-perceived p50 stays near 300 ms. (Derivation, L.)
2. **For India users, any call to a US-hosted model breaks 300 ms on round-trip time alone.**
   - Mumbai to us-west-2 is about **233 ms p50 RTT**; Mumbai to us-west-1 is about 241 ms (cloudping, 1-day p50, M). The same table shows Mumbai to us-east-1 at 294 ms, which is higher than US-West and backwards for normal routing, so treat it as suspect.
   - Jev is served only from the US West Coast (vendor blog, H). The estimated Jev p50 from Mumbai is **about 300–350 ms on a warm connection** (derivation, L), and worse with a cold TLS handshake.
   - The only architecture that meets 300 ms is: **deterministic routing → precomputed "answer cards" in-region → template-rendered first chunk → optional streamed LLM narrative afterwards.**
3. **LLMs cannot produce the first useful content inside 300 ms, even in the US.**
   - Best measured non-reasoning time to first token (TTFT) on Artificial Analysis (AA): Gemini 2.5 Flash-Lite **0.30 s**, Claude Haiku 4.5 **0.63 s**.
   - Both are p50 figures, measured from GCP us-central1, and exclude your network hop (AA, M–H).
   - Use LLMs for the narrative that streams after the card (target ≤ 1.5 s to first narrative token).
4. **Where Jev fits:**
   - **(a)** Asynchronous enrichment: classify news and filings into card fields such as direction, event type and materiality.
   - **(b)** Offline or backup routing for US users.
   - **(c)** Post-hoc guardrail or citation checks outside the hot path.
   - **Not** on the India live path, and **never** for numbers, dates or symbol resolution.
   - **Blocker:** the Master Customer Agreement (MCA) **forbids training a model to imitate Jev output (distillation)**. You cannot use Jev to label data for a local router.
5. **Accuracy comes from architecture, not model choice.**
   - Tools compute every number, and the LLM only verbalises a typed card.
   - A post-generation validator rejects any number or ticker in the narrative that is not in the card.
   - An exact-key cache (not a semantic cache) guards against entity and time collisions.

---

## 1. TypeSafe Jev deep dive

### 1.1 Identity, package and channels
| Fact | Value | Source | Conf |
|---|---|---|---|
| Vendor / model | TypeSafe AI (SF); Jev 1.13 (`jev-1.13.0`); aliases `jev-latest` and `jev-preview` both point to 1.13.0 | https://docs.typesafe.ai/models.md | H |
| Launch | Blog post 2026-09-15; "early access", with developers "brought off the waitlist" | https://typesafe.ai/blog/introducing-system-one-models-and-jev | H |
| **Python SDK** | **`typesafe-sdk` 0.7.1, uploaded 2026-09-21T15:57:52Z**. MIT, author "TypeSafe AI <support@typesafe.ai>", homepage typesafe.ai, repo github.com/typesafe-ai/typesafe-sdk-python, Python ≥ 3.10. Releases: 0.0.1a0 (09-09), 0.5.7 (09-11), 0.6.0 (09-15), 0.7.0 (09-18), 0.7.1 (09-21). Author and homepage match the vendor. | https://pypi.org/pypi/typesafe-sdk/json | H |
| SDK dependencies | `httpx2>=2.0.0`, pydantic ≥ 2.12, tenacity ≥ 9. **`httpx2` 2.13.1 (2026-09-23)** is a BSD-3-Clause fork of HTTPX stewarded by Pydantic Services (repo github.com/pydantic/httpx2; original author Tom Christie). Legitimate, not a squat, but a young dependency. | https://pypi.org/pypi/httpx2/json | H |
| **Correction to repo doc** | `reactive-and-jev.md` names the SDK `typesafe-python`. **That PyPI name returns 404; the correct name is `typesafe-sdk`.** | PyPI | H |
| SDK surface | `TypeSafeClient` / `AsyncTypeSafeClient`, `.system_one(state, {name: Choice/Score/Noul(...)})`, `models.list()`, `RetryPolicy`, `TypeSafeAPIError` | https://www.marktechpost.com/2026/09/23/a-coding-guide-to-typesafe-ai-jev/ ; https://docs.typesafe.ai/sdk/python.md | M |
| Pydantic AI | `pip install "pydantic-ai-slim[typesafe]"` (pydantic-ai-slim 2.49.0, 2026-09-24). Field types map to questions: bool → noul, Literal/Enum → choice, bounded float → probability, IntEnum → score. **`str`, unbounded numbers and `datetime` raise a UserError.** "There is nothing to stream": streaming returns one atomic event. | https://pydantic.dev/docs/ai/models/typesafe/ | H |
| OpenRouter | `typesafe/jev-1.13` via a **separate alpha endpoint `POST /api/alpha/decisions`**, not chat completions. Same price, 32k context, prepaid credits. The model page 404'd for the fetcher; details come from search snippets and OpenRouter docs links. | https://openrouter.ai/docs/guides/community/jev | M |
| Cloudflare Workers AI | Model `typesafe/jev`. **It proxies to TypeSafe via AI Gateway ("third-party model")**: no edge inference and no India speed-up. Price is shown only in the dashboard. 32k context. | https://developers.cloudflare.com/ai/models/typesafe/jev/ | H |

### 1.2 API shape
- **Endpoint and auth:** `POST https://api.typesafe.ai/v1/systemone` with `Authorization: Bearer`.
- **Body:** `{model, state, questions: {id: Question}}`. `state` may be a string, object or array.
- **Question types:**
  - **Noul:** returns a probability from 0 to 1. `criteria` is optional.
  - **Choice:** `criteria` maps each option to a description. Up to **255 options**.
  - **Score:** ordered level descriptions, **2 to 10 levels**. Returns a probability-weighted score plus a legend.
- **Response:** `answers[id] = {type, noul | choice + probabilities | score + legend, confidence}` and `usage{input_tokens, output_tokens}`.
- **Errors:** 401, 422, **429** (rate limit; retry with exponential backoff) and **529** (overloaded).

Source: https://docs.typesafe.ai/api.md (H)

| Limit | Value | Source | Conf |
|---|---|---|---|
| Context | **64k total** (state + all questions); **32k** for state + longest question. The Cloudflare and OpenRouter listings say 32k. | docs models.md | H |
| Rate limits | **1,200 RPM (~20 rps) and 250k tokens/s**, "adjusting dynamically" | docs models.md | H |
| Input | Text only. **"English is primary; other languages including CJK are supported but less accurate"**, which matters for Hinglish and Hindi queries. | docs models.md | H |
| Price | **$0.042/M input tokens; output free** | docs models.md; blog | H |
| Streaming | None; answers are atomic | Pydantic AI docs | H |
| Batching | Many questions in one call are evaluated in parallel: "adding more questions usually has little effect on response time". You pay for every question. | https://docs.typesafe.ai/patterns/fan-out.md | H (docs) |
| Regions | **US West Coast only**. The privacy policy says services are hosted in the US. | blog; https://typesafe.ai/legal/privacy-policy | H |
| SLA | **None.** MCA: services provided "AS IS / AS AVAILABLE"; no warranty of uninterrupted service | https://typesafe.ai/legal/mca | H |

### 1.3 "Speculative fan-out" (MarkTechPost coding guide, 2026-09-23)
- **The pattern:**
  - Ask every question you *might* need, including branch-only ones, in one call.
  - Let code read only the answers that apply.
  - The docs example (support ticket: category + bug_severity + refund_requested + frustration) ignores the severity answer unless the category is `bug_report`.
- **Cost trade-off:** you pay for the unused questions (docs, H).
- **Claimed gain:** one cookbook example reports 13 questions in one call as "12.2x cheaper and 10x faster" than 13 sequential calls (search snippet quoting the cookbook, M).
- **MarkTechPost's 10-question figures** (a single call vs 1.8× slower and 5.7× more tokens) were garbled in extraction, so rate them L.
- **Other guide figures:** per-call latency of about 50–100 ms, and 12 tickets through `asyncio.gather` in about 800 ms of wall time, so about 67 ms amortised. The measuring location is not stated (M/L).
- **Confidence thresholds in the guide** rise with the stakes: 0.50 / 0.70 / 0.85 / 0.90.
- **Mapping to this product:** one Jev call per news item, with `{direction: choice, event_type: choice(≤255), materiality: score, mentions_symbol_X: noul...}`. This is a good fit for **asynchronous** news-card enrichment.

### 1.4 Latency: vendor methodology and independent measurements
| Source | Setup | Result | Conf |
|---|---|---|---|
| Vendor blog | "70ms-500ms" end to end, network included. Evals "generally run from our laptops on the West Coast". No percentiles, no sample size. The vendor admits this favours them. | 70–500 ms | M |
| LiteLLM auto-router benchmark (2026-09-18) | 80 authored cases × 3 = 240 calls; client and provider regions unstated. LiteLLM authored the labels (conflict acknowledged). | **Jev p50 127 ms / p95 231 ms** vs Haiku 688 / 897 ms. Tier-label match: Jev 95.0%, Haiku 73.75%. | M |
| AY Automate (2026-09-19) | Banking77 (8-way n=160, 77-way n=231), deepset prompt-injections (n=400). Jev accessed via the OpenRouter alpha endpoint from one laptop, concurrency 4. | **Jev p50 0.33 s**; GPT-5.4 nano 1.15 s; Gemini 3.5 FL 0.67 s; Haiku 4.5 1.02 s. Accuracy is about the same as the small models (8-way 83.8% vs nano 90.0%; 77-way 78.8%). A **≥ 0.80 confidence gate plus escalation to GPT-5.6 Terra** matched Terra's accuracy at 26–28% of its cost. | M |
| jev-phishing-bench (2026-09-17) | 2,000 emails; **measured from France** | **Jev p50 ~239 ms** vs Haiku 687 ms. One-question accuracy 62.6% (Haiku 81.3%). Five atomic nouls plus a logistic regression reached 95.0%. **ECE 0.107** (under-confident on nouls, over-confident on choice/score). | https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval (M, secondary write-up of GitHub anisselbd/jev-phishing-bench) |
| **Mumbai estimate (mine)** | France to US-West RTT is about 140–150 ms, which implies Jev server-side p50 of about 90–100 ms. Add Mumbai to us-west-2 RTT of about 233 ms. | **~320–340 ms p50, warm connection**; p95 is likely well above 400 ms | L (derivation) |

### 1.5 Accuracy, weaknesses and calibration
- **Known weaknesses** (vendor "Jev 1.13 jaggedness" page, H):
  - literal reading;
  - "not a calculator" (counting and arithmetic);
  - numeric representations;
  - reads dates as text;
  - multi-hop reasoning and double negatives;
  - **context rot as irrelevant state grows**;
  - **prompt injection from state**;
  - P(noul) ≠ 1 − P(not noul);
  - option-order sensitivity (Pydantic AI docs).
- **Vendor accuracy:** about 68% on its own four-workflow eval, with frontier-model outputs as the reference rather than ground truth (see `reactive-and-jev.md`; M). The vendor claims "0% hallucination" because output is schema-constrained. That only means it can't produce an invalid *type*; it can still pick a wrong answer (H critique; KDnuggets and wavect in the prior appendix).
- **Implication:** confidence gates **must be recalibrated** (e.g. Platt or isotonic scaling) on our own labelled set before use.

### 1.6 Terms, AUP and data
| Topic | Finding | Source | Conf |
|---|---|---|---|
| MCA | **Effective 2026-09-23.** Governed by California law. **Liability cap is the greater of the fees paid in the prior 12 months or $50.** Suspension is allowed for breach, fees more than 30 days overdue, legal change or risk to the service. Output rights are assigned to the customer. Output "may not be unique". | https://typesafe.ai/legal/mca | H |
| **Distillation ban** | Customer may not "use the Services … to perform model distillation, train a model to imitate the output". **This rules out using Jev labels to train our own local router or classifier.** | same | H |
| AUP | Last updated 2026-09-23. General bans: illegal content, "manipulative or deceptive activities", circumventing safety controls. **No explicit ban on financial advice or automated decisions found.** The earlier 404 is resolved. | https://typesafe.ai/legal/acceptable-use-policy | M (summarizer read) |
| Training | Privacy policy: "We will not train or fine tune any … models on your prompts or other Input". MCA: no training on Customer Data without consent. **Telemetry may be used "without restriction".** | privacy policy (updated 2025-11-19); MCA | H |
| Retention | DPA (updated 2026-04-24): retained "as long as necessary"; **no fixed period**. Subprocessors listed at trust.typesafe.ai/subprocessors (not fetched). **ZDR available only for enterprise** (privacy@typesafe.ai). | https://typesafe.ai/legal/data-processing ; https://docs.typesafe.ai/legal.md | M |
| Data location | US; EEA/UK users transfer data to the US. There is **no India region**, so check DPDP Act cross-border posture with compliance-analyst (user query text may be personal data). | privacy policy | H |

### 1.7 Alternatives to Jev for the "typed decision" role
| Option | What | Licence | Latest (registry) | Notes | Conf |
|---|---|---|---|---|---|
| **Local router** (model2vec static embeddings + logistic regression or kNN) | CPU-only intent classifier; potion-base-8M is about 8 MB | MIT | model2vec 0.9.0 (2026-08-12) | Claims "up to 500× faster on CPU" than the source transformer, with no ms figure. Expect roughly 1–5 ms in-process (my estimate, L). **Must be trained on our own or human labels, not Jev labels.** | M |
| semantic-router (Aurelio) | Embedding-based route matching | MIT | 0.1.16 (2026-07-26) | Pre-1.0; thin layer | M |
| fastembed (Qdrant) | ONNX embeddings on CPU | Apache-2.0 | 0.8.1 (2026-09-22) | Useful for in-region query embeddings | H |
| **AnyJev** (Nokia Applied Research) | "Turn any open LLM into a Jev-style decision model": calibrated typed choices, no training | Apache-2.0 | **anyjev 0.0.2 (2026-09-21)**, PyPI author Jiamu (Morris) Zhang, homepage github.com/MorrisZJ/AnyJev | The GitHub repo resolves under nokia-applied-research, and Zhang is a listed author, so it is probably legitimate. **Flag the PyPI homepage mismatch (personal URL) and the 0.0.x maturity.** Vendor claim: about 0.25 s per decision at batch 32 on one H100 with Qwen3-8B. Self-hosting in Mumbai removes the US round trip. | M |
| Structured-output small LLM | Haiku 4.5 or Gemini Flash-Lite JSON-schema | commercial | — | Slower (0.3–0.6 s TTFT at US p50) but explains itself | H |

---

## 2. Where 300 ms is realistic: stage by stage

### 2.1 Measured model TTFT (Artificial Analysis)
AA methodology: **p50 over the past 72 h**, 8 runs per day. The primary client is a **GCP us-central1-a** VM. Workloads are about 1k, 10k (default) and 100k input tokens. Parallel runs use 10 concurrent requests. (https://artificialanalysis.ai/methodology/performance-benchmarking, H.)

**Reasoning-configuration TTFTs include thinking time, so compare only non-reasoning runs.**

| Model / provider | TTFT (s) | Output tok/s | Conf |
|---|---|---|---|
| **Gemini 2.5 Flash-Lite (non-reasoning), Google** | **0.30** | 279 | H (AA page) |
| **Claude Haiku 4.5 (non-reasoning), Anthropic** | **0.63** | 87 | H |
| gpt-oss-120B (high), Baseten / Crusoe / Together | 0.26 / 0.36 / 0.54 | 200 / 255 / 88 | M. **Not comparable to answer-token TTFT.** These probably measure the first *reasoning* token, so they understate time to useful content; do not read Baseten as the fastest model. |
| gpt-oss-120B (high), Cerebras / SambaNova / Groq | 1.63 / 3.89 / 4.96 | **1,766** / 709 / 473 | M (same caveat; throughput leaders) |
| Llama 3.1 8B, Groq / Bedrock | 0.92 / 0.70 | 647 / 188 | M |
| Gemini 3.5 Flash-Lite, GPT-5.4 nano | not comparable (AA only ran reasoning configurations: 8.2 s / 86.7 s) | — | — |

**Take-away:** even the best US-measured p50 (about 0.3 s) uses the whole budget before any network hop from India. **LLM output cannot be the first useful content.**

### 2.2 India hosting facts
| Item | Finding | Source | Conf |
|---|---|---|---|
| AWS Mumbai inter-region p50 | Self 1.4 ms; Singapore 63 ms; Ireland 121 ms; us-west-2 233 ms; us-west-1 241 ms; us-east-1 295 ms (suspect). 1-day window. | https://www.cloudping.co/ | M |
| Bedrock Claude in India | Haiku 4.5 is reachable from ap-south-1/ap-south-2 **via Global cross-region inference** (`global.anthropic.claude-haiku-4-5-20251001-v1:0`), which routes across all commercial regions, so it is **not Mumbai-local**. | https://aws.amazon.com/blogs/machine-learning/access-anthropic-claude-models-in-india-on-amazon-bedrock-with-global-cross-region-inference | M–H |
| Vertex AI asia-south1 | Search snippet: Gemini 2.5 Flash is available in asia-south1. Flash-Lite availability in asia-south1 is **unverified** (the docs page did not render). A third-party catalogue lists 61 models from 9 publishers, including Google and Anthropic. | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations ; https://modelavailability.com/platforms/gcp/regions/asia-south1 | L |
| Cloudflare Workers AI | GPUs in "Mumbai, New Delhi" (search snippet from the CF blog). Only helps for models Cloudflare *hosts* (e.g. Llama, Gemma), **not for Jev (proxied)**. | https://blog.cloudflare.com/ | L |
| NSE data vendors | Authorised vendors include TrueData and Global Datafeeds (websocket / REST). TrueData claims "<1 ms server-side processing"; no end-to-end figure. Redistribution and display need NSE Data & Analytics agreements, and non-display use has its own policy. **Hand off to market-data-researcher and compliance-analyst.** | https://www.truedata.in/ ; https://globaldatafeeds.in/ ; https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Non_Display_Policy.pdf | M |

### 2.3 Per-stage latency budget
Server-side, India users, measured at ingress in ap-south-1. Targets are p95. Figures are design estimates (L) unless cited.

| # | Stage | Tech | Budget p95 | Notes |
|---|---|---|---|---|
| 0 | Ingress | Keep-alive HTTP/2 or SSE/WebSocket to an ALB/Cloud Run in ap-south-1 | 5 ms | TLS is done once per session |
| 1 | Normalise + **entity resolution** | Symbol dictionary (NSE/BSE codes, `.NS`, BSE scrip codes, company aliases, Hinglish spellings); Aho-Corasick plus rapidfuzz | 2 ms | **Deterministic.** Jev's 255-option cap and weak literal reading make it unfit for this |
| 2 | **Intent routing** | Rules/regex for high-precision patterns ("bulk deal", "RSI", "support") → model2vec/fastembed + logistic regression for the rest → if confidence < τ, a clarifying chip or the generic "overview" card | 5–10 ms | Train on our own human-labelled queries (not Jev labels, which the MCA bans). Include Hinglish in the eval |
| 3 | **Exact-key card lookup** | Redis/Valkey in the same AZ: key = (intent, symbol, timeframe, as-of bucket) | 2 ms | Time-to-live tied to the source's freshness (1-min bars → ≤ 60 s) |
| 3b | Card miss → compute | Postgres/Timescale or ClickHouse over recent bars; TA-Lib on a ≤ 500-bar window; DuckDB for ad-hoc work | 20–50 ms | Precompute on bar close for watchlist and index constituents so misses are rare |
| 4 | **Render the first useful content** | Deterministic template from card JSON, e.g. "RELIANCE −2.1% vs NIFTY −0.4% at 11:32 IST; Energy −1.5%; 2 news items since 09:15 [links]" | 2 ms | Numbers come only from the card |
| | **TTFUC, server-side** | | **≈ 20–70 ms** | Leaves ~200+ ms for the last mile |
| 5 | Streamed narrative (optional) | LLM with a large static system prompt (≥ 4,096 tokens to be cacheable on Haiku 4.5) plus card JSON | 0.4–1.5 s to first narrative token | Arrives after the card; the user already has the answer |
| 6 | **Numeric/citation validator** on the narrative stream | Regex-extract numbers and tickers and check each is in the card (with tolerance for rounding) | < 5 ms per chunk | On failure, drop the narrative and keep the card |
| async | News enrichment | Ingest → dedupe → **Jev fan-out** (direction, event type, materiality, per-symbol relevance) or a local classifier → store on the news card | seconds | This is where Jev's price and speed help. US round trip is irrelevant here |

**Question → card mapping:**
- **"Why is RELIANCE down?"**
  - Move card: price change vs NIFTY and the sector index, beta-adjusted residual, volume vs 20-day average.
  - Top news items in the window, ranked by Jev/classifier relevance and direction, with timestamps and links.
  - Corporate actions and deals.
  - Wording must be "coincident with", not "caused by".
- **"RSI and support for NIFTY":** indicator card (RSI-14 Wilder, pinned definition) plus a levels card (classic/Camarilla pivots from the prior session plus swing-low clusters). Recompute on each 1-min/5-min close.
- **"Bulk deals in HDFCBANK today?":** deals card from the NSE/BSE after-hours files.
  - **Bulk and block deals are disseminated after market hours on the same day** (SEBI, H). During market hours the correct answer is "Today's bulk/block deal file is not published until after the close; last published: <date>".
  - Block windows (SEBI circular 2025-10-08): 08:45–09:00 and 14:05–14:20 IST, ±3% of the reference price, ₹25 cr minimum (https://www.icicidirect.com/research/equity/finace/sebi-revises-block-deal-rules, M).
- **"News on TSLA":** news digest card (US-side ingest; served from the region nearest the user).

### 2.4 Caching
| Layer | Recommendation | Evidence | Conf |
|---|---|---|---|
| **Exact-key card cache** | Primary. Key = normalised (intent, entity, timeframe, as-of bucket). **Self-host Valkey (BSD-3-Clause) or use ElastiCache for Valkey.** | Design | — |
| **LICENCE FLAG: Redis server** | **Redis Open Source 8.x is tri-licensed RSALv2 / SSPLv1 / AGPLv3**, and search and vector (RediSearch, Query Engine) come under the same tri-licence. The client libraries redisvl and langcache are MIT; this flag is about the *server*. Prefer Valkey, or managed Redis Cloud, where the licence is the vendor's concern. | https://redis.io/legal/licenses/ | H |
| redisvl on Valkey | Reportedly works via a `valkey://` URL **if the valkey-search module (FT.\*) is present**. There is a redis-py ≥ 6 import-name gotcha. | https://docs.litellm.ai/blog/valkey_semantic_caching ; https://github.com/BerriAI/litellm/pull/40863 | L |
| **Semantic cache** | **Only for phrasing → canonical intent, never across entity or time.** Risks: "HDFC" vs "HDFCBANK" collisions, "up" vs "down" near-duplicates, stale numbers. | Design | L |
| Redis LangCache | Managed REST semantic cache; **public preview**; illustrative $1.5/M input tokens, "final GA pricing TBD". Python SDK `langcache` 0.14.0 (2026-08-24, MIT, Redis). | https://redis.io/docs/latest/operate/rc/langcache/ ; https://redis.io/calculator/langcache/ ; PyPI | M |
| redisvl `SemanticCache` | Self-hosted on Redis; redisvl 0.27.2 (2026-09-10, MIT, Redis Inc.) | PyPI | H |
| **GPTCache** | **Hold.** Last release 0.1.44 on **2024-08-01** (Zilliz, MIT) | PyPI | H |
| **Prompt caching** (Anthropic) | Minimum cacheable prompt for **Haiku 4.5 is 4,096 tokens**; shorter prompts silently don't cache. Cache read costs 0.1× input; 5-min and 1-h TTLs have the same latency. The "up to 85% latency reduction" claim is for *long* prompts, so it barely helps short card prompts. | https://platform.claude.com/docs/en/build-with-claude/prompt-caching | H |
| Speculative decoding | A provider-side technique we don't control via hosted APIs. Relevant only if we self-host (vLLM/SGLang) in Mumbai. Not researched further. | — | L |

### 2.5 Retrieval (open-ended questions only; symbol-keyed queries use metadata lookup)
| Engine | Latest (registry) | Licence | Latency evidence | India region | Conf |
|---|---|---|---|---|---|
| **pgvector** (in existing Postgres) | Python client pgvector 0.5.0 (2026-07-06). The extension has no GitHub Releases, so its version was not checked. | PostgreSQL-style (ext.) / MIT (client) | No independent p99 fetched | Anywhere Postgres runs (RDS ap-south-1) | M |
| **Qdrant** | qdrant-client 1.19.1 (2026-09-16), Apache-2.0 | Apache-2.0 | Vendor benchmarks (updated **2024**, Azure 8 vCPU, relative numbers only, vendor admits bias) | Self-host in ap-south-1; managed India region **unverified** | M |
| **Turbopuffer** | turbopuffer 2.10.2 (2026-09-23), MIT client; service is proprietary SaaS | Client MIT | Homepage: **warm vector p50/p90/p99 = 14/17/27 ms** (10M docs, 1024 dims, top-10, 8 QPS). Its FTS figure (p50 874 ms) is probably a cold-namespace number; **keep namespaces warm**. | **aws-ap-south-1 (Mumbai) listed** | M (vector), L (FTS) |
| **LanceDB** | lancedb 0.39.0 (2026-09-17), Apache-2.0 | Apache-2.0 | Not fetched | Embedded, so anywhere | M |

**News index freshness:** use synchronous upsert on ingest, and search with "strong" or read-after-write consistency for the latest window, or simply query the last-N-hours news table by symbol (SQL). For the example queries, metadata filtering by (symbol, time window) beats ANN on both latency and correctness.

---

## 3. Accuracy

### 3.1 Numeric grounding
- Every number shown is computed by code into a card with `as_of_ts`, `source` and `method_version`. The LLM only verbalises the card.
- The post-hoc validator (stage 6) rejects any number, percentage, ticker or date that is absent from the card.
- Literature signal: a tool-grounded framework (CIFQA, arXiv 2608.26114) reports **95.54% on calculation-intensive fixed-deposit queries**, outperforming "direct LLM baselines even when provided with complete formulas" (abstract, M). The per-model arithmetic hallucination rates quoted in search snippets (e.g. 54.95% / 29.70% / 16.34%) are **not in the abstract** (L).

### 3.2 Indicator libraries
| Library | Latest (PyPI) | Licence | Status | Verdict | Conf |
|---|---|---|---|---|---|
| **TA-Lib** (Python wrapper) | **0.8.1 (2026-09-21)**; 0.8.0 (09-13), 0.7.x (Jul) | BSD-style (not in PyPI metadata; repo says BSD-2-Clause, unverified this session) | Active; homepage github.com/ta-lib/ta-lib-python, author John Benediktsson (the long-time maintainer) | **Adopt** as the reference implementation | H (release), M (licence) |
| **pandas-ta** | 0.4.71b0 (**2025-09-14**, beta), Python ≥ 3.12 | Unstated in metadata | Maintainer set an archive deadline of 2026-07-01 unless funded. **github.com/twopirllc/pandas-ta now returns 404.** | **Hold** | H (PyPI), M (404) |
| **talipp** (incremental/streaming) | 2.7.0 (2025-09-09) | MIT | About a year since the last release | **Assess** for O(1) per-tick updates; cross-check against TA-Lib | M |
| polars-talib | 0.2.0 (2026-09-23) | Unstated | Polars plugin that wraps TA-Lib | Assess | L |
| polars-ta | 0.5.17 (2026-01-27) | MIT | Separate reimplementation | Assess (needs a correctness diff) | L |

**Correctness notes:**
- RSI and EMA depend on seeding and warm-up: Wilder smoothing, and TA-Lib's "unstable period" (TA_SetUnstablePeriod).
- Pin one definition, fetch at least 250 bars of warm-up, and golden-test against broker or TradingView values for NIFTY, RELIANCE and HDFCBANK.
- Adjust history for splits and bonuses (common in India) before computing levels.
- Timezone is IST (NSE session 09:15–15:30).

### 3.3 Evals
| Eval | Scope | Use | Source | Conf |
|---|---|---|---|---|
| FinanceBench (Patronus) | US 10-K/10-Q/8-K QA (150-question open sample; 10,231 total) | Retrieval plus numeric QA on filings. Shared vector store accuracy drops sharply (the paper says GPT-4-Turbo + RAG failed 81%). | https://github.com/patronus-ai/financebench | M |
| FinQA / TAT-QA | Numeric reasoning over tables and text | Test the narrative verbaliser and any calc path | (not fetched) | L |
| **IndiaFinBench** | 406 expert QA pairs from 192 SEBI/RBI documents: regulatory, numerical, contradiction and temporal tasks. **CC BY 4.0**. Gemini 2.5 Flash 89.7% (best); Gemma 4 E4B 70.4%. | India-specific regulatory grounding | https://arxiv.org/abs/2604.19298 | M |
| Vectara HHEM leaderboard (updated 2026-09-22) | Summarisation hallucination rate | Gemini 2.5 Flash-Lite **3.3%**, Llama 3.3 70B 4.1%, Gemini 3.1 FL Preview 8.2%, **Haiku 4.5 9.8%**, GPT-5.4 nano 10.5%, GPT-5 mini 12.9%, gpt-oss-120B 14.2% | https://github.com/vectara/hallucination-leaderboard | M–H |
| **Own golden set** (must build) | ≥ 300 real queries: English, Hinglish, Hindi; NSE, BSE, US; intraday and post-close | Router accuracy, card correctness, narrative validator pass rate, TTFUC p50/p95 | — | — |

---

## 4. Recommended architecture and ranking

```
client (SSE/WebSocket) ──► ap-south-1 edge/API (India)  | us-east-1 (US users)
   1 normalise + symbol resolve (dict + fuzzy)          2 ms
   2 route: rules → model2vec/LR → clarify               5–10 ms
   3 exact-key Redis card  ─miss─► compute (TA-Lib/SQL)  2 / 20–50 ms
   4 template render → FIRST CHUNK                       ~20–70 ms server-side
   5 LLM narrative stream (Flash-Lite in-region if available; Haiku via Bedrock global CRIS) 0.4–1.5 s
   6 numeric/citation validator on stream
background: bar-close card precompute · news ingest → Jev fan-out (or local/AnyJev) → news cards · post-close NSE/BSE deals ingest
```

**Ranked recommendation:**
1. **Deterministic router + precomputed cards + template-first streaming** (Adopt). This is the only design that meets 300 ms for India. H confidence in the principle; the budget is L (design estimate).
2. **Jev for asynchronous news/filing enrichment and US-side guardrails** (Trial, behind an interface). It is cheap, and its fan-out fits card fields. Recalibrate its confidence before relying on it.
3. **Local router trained on human labels** (Trial). Use AnyJev/Qwen3-8B in Mumbai (Assess) if a Jev-like typed decider is needed in-region.
4. **Streamed narrative model** (Trial):
   - Gemini 2.5 Flash-Lite (lowest measured TTFT and HHEM rate; check asia-south1 availability).
   - Haiku 4.5 via Bedrock global CRIS as the second option.
   - Groq/Cerebras only if throughput matters more than TTFT.

**Proposed radar deltas** (for tech-lead; repo not edited):
- **Fast text decisions:**
  - Keep **Jev in Trial for asynchronous enrichment only**.
  - Add "**Jev on India live path: Hold**" (round trip, English-primary, no SLA).
  - Add AnyJev to Assess.
  - Add model2vec + LR router to Trial.
- **Caching:**
  - Add "exact-key card cache on **Valkey** (BSD-3): Adopt".
  - Add "**Redis 8 server self-hosted: flag** (RSALv2/SSPLv1/AGPLv3)".
  - Add "semantic cache (LangCache/redisvl) for phrasing only: Assess".
  - Add "GPTCache: Hold".
- **Indicators:** add "TA-Lib: Adopt"; "talipp / polars-talib: Assess"; "pandas-ta: Hold".
- **Vector:** add "pgvector: Adopt (existing PG)"; "Turbopuffer (has Mumbai): Assess"; "Qdrant self-host: Assess".
- **Correct `reactive-and-jev.md`:**
  - The SDK is `typesafe-sdk`, not `typesafe-python`.
  - Context is 64k total / 32k for state plus the longest question.
  - The AUP is now published (2026-09-23).
  - Cloudflare's Jev is a proxy.
  - Rate limits: 1,200 RPM / 250k tokens per second.
- **Scope note:** the production plan (02/04/13) is US-equities-only. India NSE/BSE support needs a new data-licensing ADR: NSE Data & Analytics display and non-display agreements, plus an authorised vendor.

**Conditions that would change this recommendation:**
- TypeSafe opens an India or Asia region, or publishes an SLA → re-test Jev as a live router.
- The owner accepts a US-only user base → Jev as a live router becomes viable (about 130–230 ms p50 from US-West/East, per LiteLLM and France data).
- A model with sub-100 ms TTFT becomes available in Mumbai.
- The own golden set shows the local router below about 90% accuracy on Hinglish.

---

## 5. Unverified / open
1. Jev: subprocessor list (trust.typesafe.ai not fetched); Cloudflare-side price; OpenRouter model page (404 to the fetcher); p99 latency from any independent source; the Mumbai figure is a derivation, not a measurement; the AUP was read through a summarizer only.
2. The cloudping Mumbai → us-east-1 figure (295 ms) is anomalous. Re-measure from a Mumbai VM with `curl -w` against api.typesafe.ai (needs approval to run).
3. Gemini 2.5/3.x Flash-Lite availability in Vertex asia-south1: the docs table did not render.
4. Cloudflare Workers AI GPUs in Mumbai and New Delhi (snippet only); which hosted models actually run there.
5. TA-Lib wrapper licence text; polars-talib licence; talipp correctness vs TA-Lib.
6. pandas-ta: whether the repo was deleted, renamed or made private (404 only).
7. Turbopuffer FTS latency figure, and whether it is a cold-namespace number.
8. Qdrant Cloud India region; pgvector extension version and independent p99.
9. CIFQA per-model arithmetic hallucination rates (snippet only); FinQA and TAT-QA not fetched.
10. NSE bulk/block deal file publish time (exact clock time after close) and redistribution rights for deal data; the block-deal ₹25 cr minimum is from a secondary source.
11. The LiteLLM and AY Automate client regions are unstated, so they cannot be transferred to India.
12. The AnyJev H100 latency is a vendor claim; the PyPI homepage points to a personal GitHub account.
13. **Latency from NSE/BSE data vendors (TrueData, Global Datafeeds) to ap-south-1 / asia-south1 is unmeasured.** Only TrueData's "<1 ms server-side" claim exists.
14. Speculative decoding was not researched (irrelevant for hosted APIs; relevant only if self-hosting in Mumbai).
15. Groq, Cerebras and SambaNova serving regions, and their round trip from India, were not checked. The AA figures are from us-central1.
16. Whether redisvl `SemanticCache` works end to end on Valkey plus valkey-search (secondary sources only). Valkey's BSD-3 licence was not re-fetched this session.

## 6. Sources (all accessed 2026-09-24)
- TypeSafe: https://typesafe.ai/blog/introducing-system-one-models-and-jev · https://docs.typesafe.ai/llms.txt · https://docs.typesafe.ai/api.md · https://docs.typesafe.ai/models.md · https://docs.typesafe.ai/patterns/fan-out.md · https://docs.typesafe.ai/patterns/intent-routing.md · https://docs.typesafe.ai/model-jaggedness/jev-1.13.md · https://docs.typesafe.ai/legal.md · https://typesafe.ai/legal/mca · https://typesafe.ai/legal/acceptable-use-policy · https://typesafe.ai/legal/privacy-policy · https://typesafe.ai/legal/data-processing
- Registries: https://pypi.org/pypi/typesafe-sdk/json · https://pypi.org/pypi/httpx2/json · PyPI JSON for qdrant-client, lancedb, turbopuffer, pgvector, redisvl, langcache, TA-Lib, pandas-ta, talipp, polars-talib, polars-ta, pydantic-ai-slim, openrouter, anyjev, sentence-transformers, model2vec, fastembed, semantic-router, gptcache
- Channels: https://pydantic.dev/docs/ai/models/typesafe/ · https://developers.cloudflare.com/ai/models/typesafe/jev/ · https://openrouter.ai/docs/guides/community/jev
- Independent reviews: https://www.marktechpost.com/2026/09/23/a-coding-guide-to-typesafe-ai-jev/ · https://docs.litellm.ai/blog/jev-auto-router-benchmark · https://www.ayautomate.com/blog/jev-vs-llm-benchmark · https://www.beri.net/article/typesafe-jev-typed-decision-model-calibration-decomposition-shadow-eval · https://www.marktechpost.com/2026/09/23/nokia-open-sources-anyjev-a-training-free-layer-that-turns-any-open-llm-into-a-calibrated-decision-model/ · https://github.com/nokia-applied-research/AnyJev
- TTFT: https://artificialanalysis.ai/methodology/performance-benchmarking · https://artificialanalysis.ai/models/claude-4-5-haiku · https://artificialanalysis.ai/models/gemini-2-5-flash-lite · https://artificialanalysis.ai/models/gpt-oss-120b/providers · https://artificialanalysis.ai/models/llama-3-1-instruct-8b/providers · https://artificialanalysis.ai/leaderboards/models
- Regions: https://www.cloudping.co/ · https://aws.amazon.com/blogs/machine-learning/access-anthropic-claude-models-in-india-on-amazon-bedrock-with-global-cross-region-inference · https://turbopuffer.com/docs/regions · https://turbopuffer.com/
- Caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching · https://redis.io/docs/latest/operate/rc/langcache/ · https://redis.io/calculator/langcache/
- Retrieval: https://qdrant.tech/benchmarks/
- Accuracy: https://github.com/vectara/hallucination-leaderboard · https://arxiv.org/abs/2608.26114 · https://arxiv.org/abs/2604.19298 · https://github.com/patronus-ai/financebench · https://www.pandas-ta.dev/
- India market structure: https://www.icicidirect.com/research/equity/finace/sebi-revises-block-deal-rules · https://www.nseindia.com/report-detail/display-bulk-and-block-deals · https://nsearchives.nseindia.com/web/sites/default/files/inline-files/Non_Display_Policy.pdf · https://www.truedata.in/ · https://globaldatafeeds.in/
