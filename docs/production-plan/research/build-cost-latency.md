# Research: what it costs, how it performs, and how long it takes to build (India-first, Mumbai-served)

- **Author:** sre-engineer (Quality & Ops)
- **Date:** 2026-09-24. Every URL was accessed on 2026-09-24.
- **Scope:** the build/run economics and physical latency limits for the card-first assistant in [14](../14-global-market-assistant.md) (targets: p95 120 ms on a cache hit, 300 ms on a miss, served from Mumbai). This complements, and does not repeat:
  - [09](../09-costs-and-operating-model.md) (US-East costs, the LLM-per-event model);
  - [13](../13-quick-response-system.md);
  - [assistant-300ms-and-jev](assistant-300ms-and-jev.md) (AA TTFT table, cloudping, stage budget);
  - [official-sources-and-tools](official-sources-and-tools.md) (Sarvam API price, Valkey 9.1, Langfuse).
  - Links are repo-root-relative. Rewrite them (`../14-…`) if this file moves into `docs/production-plan/research/`.
- **Method:** read-only.
  - **AWS prices** were read from the official AWS Price List bulk files (`pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<service>/current/ap-south-1/index.json`) and the metered-unit maps used by the AWS pricing pages. The publication dates of the files are quoted.
  - **Azure prices** come from the public Azure Retail Prices API (`prices.azure.com`).
  - **Oracle prices** come from Oracle's public price-list API (`apexapps.oracle.com/pls/apex/cetools/api/v1/products/`).
  - **GCP prices:** GCP pages render prices client-side from an authenticated API, so GCP Mumbai figures come from the page's default-region (Iowa) table plus an aggregator for Compute. Confidence is labelled accordingly.
  - Nothing was signed up for, benchmarked against third parties, or edited in the repo.
- **Confidence:** **H** = primary page, price file or registry read directly. **M** = primary page read through a summarizer, or a reputable secondary source. **L** = search snippet, a vendor with a conflict of interest, or my own derivation.
- **Tags:**
  - **[F]:** a verified fact.
  - **[E]:** an estimate, with the arithmetic shown.
  - **[I]:** an inference.
  - **[P]:** a proposal.
- **Conventions:**
  - 730 h per month.
  - 21 NSE trading days per month.
  - Session 09:15–15:30 IST = 375 min = 22,500 s.
  - **₹96 per US$** (BookMyForex quote for 2026-09-24, M). Change this one number to re-base every ₹ figure.
  - **GST (18%) and reverse-charge on imported cloud/API services are not modelled.** All prices are list, on-demand, and exclude Savings Plans, CUDs and reservations.

---

## 0. Bottom line

1. **Infrastructure is cheap; people, data licences and the LLM call pattern are not.** [E]
   - Running the whole card-first stack on AWS Mumbai (list prices) costs about:

     | Scale | Single-AZ ("99.5%") | Multi-AZ ("99.9%") |
     |---|---|---|
     | Pilot (1k users) | **~$200/mo (₹19k)** | **~$280/mo (₹27k)** |
     | 10k users | ~$320/mo | ~$480/mo |
     | 100k users | ~$860/mo | **~$1,200/mo (₹1.15 lakh)** |

   - These exclude market-data licences, which are much larger ([14 §4](../14-global-market-assistant.md)).
   - Even at 100k users the peak load is only **~110 req/s, with bursts of about 360 req/s** (§1.5).
2. **The LLM is the only line that can explode, and design decides it, not model choice.** [E]
   - **Narrative on every query at 100k users:** $2.9k/mo (Gemini 2.5 Flash-Lite) up to $32.6k/mo (Claude Haiku 4.5).
   - **One narrative per card version, cached by exact key and shared across users** (the [09 §2](../09-costs-and-operating-model.md) principle): **$88–$977/mo**.
3. **The fastest measured model is about to disappear from the India region.** [F, H]
   - Gemini 2.5 Flash-Lite is the only sub-second non-reasoning TTFT on record (0.30 s, AA, US-measured). **It retires on Vertex AI on 2026-10-20.**
   - On the Gemini Developer API it has "no shutdown date announced", but that endpoint gives no India processing guarantee.
   - The Vertex replacements (3.1 / 3.5 Flash-Lite) have **only reasoning-mode TTFTs measured (5.6 s and 8.2 s)**. Their fast-mode TTFT is **unmeasured**.
   - This is an owner decision (§2.4).
4. **OpenAI's India data residency is storage-only.** [F, H] `in.api.openai.com` lists "Storage: Yes / Processing: No". Inference therefore still crosses to a non-India region, adding ~190–240 ms RTT.
5. **300 ms end to end on 4G for a cached card: yes when warm, no as a guaranteed p95 on a cold connection.** [E, from H/M inputs]
   - **Warm connection** (keep-alive HTTP/2 or WebSocket): about 1 RTT plus server time.
     - Median Delhi user on 4G/5G: **~85–100 ms**.
     - p95: **~240 ms**.
   - **Cold connection** (DNS + TCP + TLS 1.3): 3–4 RTT.
     - Median: **~235–250 ms**.
     - p95: **~690 ms**.
     - Terminating TLS at an in-city CDN edge brings the cold p95 to about 430 ms.
   - Keep 300 ms as a **server-side** SLO. Report client p95 from RUM separately, split warm vs cold (§3.6).
6. **Delta corrections to existing appendices** (all accessed today):
   - **Cloudping Mumbai → us-east-1 now reads 193 ms p50** (1-day), down from the "suspect" 295 ms in assistant-300ms. The anomaly has cleared. [F, M]
   - **Azure's official P50 (30 days to 2026-07-30):** Central India → East US 198 ms, West US 2 210 ms. So US-East is *not* slower than US-West from India. [F, H]
   - **ElastiCache for Valkey is available in ap-south-1**, node-based and Serverless. This closes the open item in official-sources §3.1. [F, H]
   - **Mumbai ↔ Hyderabad (ap-south-2) is 13.7 ms p50.** This is a same-country DR region. [F, M]
7. **Engineering effort for the MVP** listed in the brief: **~29–59 engineer-weeks** [E, L]. That is about:
   - 8–17 months with 1 developer;
   - 5–11 months with 2 developers;
   - 3–6.5 months with 4 developers (§4).

   The calendar floor comes from **NSE licensing and counsel answers (I-01, I-02) and gold-set annotation**, not coding.

---

## 1. Mumbai infrastructure prices and monthly totals

### 1.1 AWS ap-south-1 (on-demand, USD)

Sources: AWS Price List bulk files for EC2 (metered-unit map published 2026-09-21), RDS (2026-09-22), ElastiCache (2026-09-14), DataTransfer (2026-09-16), CloudFront (2026-09-16), ELB (2026-09-11) and VPC (2026-09-17). All **[F, H]** unless marked.

| Item | Rate | ×730 h (month) | Notes |
|---|---|---|---|
| **EC2 t4g.medium** (2 vCPU, 4 GiB, Graviton, burstable) | $0.0224/h | $16.35 | Pilot app tier |
| EC2 t4g.large (2 vCPU, 8 GiB) / t4g.xlarge (4 vCPU, 16 GiB) | $0.0448 / $0.0896 | $32.70 / $65.41 | |
| **EC2 c7g.large** (2 vCPU, 4 GiB) / **c7g.xlarge** (4 vCPU, 8 GiB) | $0.0491 / $0.0982 | $35.84 / $71.69 | Non-burstable; the choice for predictable p95 |
| EC2 c8g.large / c8g.xlarge | $0.05398 / $0.10796 | $39.41 / $78.81 | Newer Graviton4 |
| EC2 m7g.large (2 vCPU, 8 GiB) / m7g.xlarge | $0.0583 / $0.1166 | $42.56 / $85.12 | |
| EC2 c7i.large (x86) | $0.08925 | $65.15 | x86 costs ~1.8× Graviton here |
| **RDS PostgreSQL db.t4g.micro** Single-AZ / Multi-AZ | $0.021 / $0.042 | $15.33 / $30.66 | |
| **RDS PostgreSQL db.t4g.small** Single / Multi | $0.042 / $0.084 | $30.66 / $61.32 | Pilot DB |
| RDS PostgreSQL db.t4g.medium Single / Multi | $0.084 / $0.167 | $61.32 / $121.91 | |
| RDS PostgreSQL db.m7g.large Single / Multi | $0.24 / $0.479 | $175.20 / $349.67 | 100k scale |
| RDS gp3 storage Single / Multi-AZ | $0.131 / $0.262 per GB-mo | — | Backup beyond the free allocation: $0.095/GB-mo |
| **ElastiCache Valkey cache.t4g.micro / small / medium** | $0.016 / $0.0328 / $0.0648 | $11.68 / $23.94 / $47.30 | Valkey is ~20% below Redis OSS here (Redis t4g.small $0.041) |
| ElastiCache Valkey cache.m7g.large / r7g.large | $0.1312 / $0.1792 | $95.78 / $130.82 | |
| ElastiCache **Serverless** Valkey | $0.054/GB-hour stored + $0.0015 per million ECPU | — | **Anomaly:** these are *below* us-east-1 ($0.084 / $0.0023), while Mumbai node prices are *above* us-east-1 (t4g.small $0.0328 vs $0.0256). Re-check in the AWS calculator before relying on them |
| ALB | $0.0239/h + $0.008 per LCU-hour | $17.45 + LCU | |
| Public IPv4 (in use) | $0.005/h per address | $3.65 each | An ALB uses one per AZ |
| **Data transfer out to internet** (EC2 → Internet, India) | $0.1093/GB first 10 TB; $0.085 next 40 TB; $0.082; $0.080 | — | Cross-AZ: **$0.01/GB each way** |
| Mumbai → us-west-2 inter-region | $0.086/GB | — | Relevant only for Jev or US-hosted LLM payloads (tiny) |
| **CloudFront, India edge (pay-as-you-go)** | $0.109/GB first 10 TB … down to $0.072/GB > 5 PB. HTTPS requests **$0.012 per 10k**; origin-fetch $0.16/GB | — | India is among CloudFront's more expensive geographies |
| **CloudFront flat-rate plans** (launched Nov 2025) | **Free $0 / Pro $15 / Business $200 / Premium $1,000 per month** (M, secondary). Allowances [F, H, AWS docs]: **1M / 10M / 125M / 500M requests** and 100 GB / 50 TB / 50 TB / 50 TB. "No overage charges"; sustained excess may see "traffic delivery … adjusted" | — | **The cheapest CDN option at every scale here.** WAF, DDoS and Route 53 are included. Real-time logs are not supported |
| NAT gateway (Mumbai) | **Not verified from a primary source** (secondary sources give $0.045–0.056/h plus the same per GB) | ~$33–41 per NAT | [P] Avoid NAT: use public-subnet instances with strict security groups, or VPC endpoints for S3/ECR/SSM. Two NATs would be 15–20% of the pilot bill |
| GPU: g4dn.xlarge (T4 16 GB) / g6.xlarge (L4 24 GB) / g5.xlarge (A10G 24 GB) / **g6e.xlarge (L40S 48 GB)** | $0.579 / $0.9664 / $1.208 / **$2.235** per hour | $423 / $705 / $882 / **$1,632** | See §2.5. New accounts start with a GPU vCPU quota of 0, so request a quota increase early |

### 1.2 GCP asia-south1 (Mumbai)

| Item | Rate | Conf | Notes |
|---|---|---|---|
| e2-standard-2 (2 vCPU, 8 GB) | **$0.0805/h → $58.77/mo** (Iowa $0.067) | M (gcloud-compute.com, updated 2026-09-21) | Mumbai ≈ **1.20×** Iowa for E2 |
| g2-standard-4 (1× L4 24 GB) | **$0.7358/h → $537/mo** (available in asia-south1) | M (same) | Cheapest L4 in Mumbai among the clouds checked |
| Cloud SQL PostgreSQL, **Iowa default table**: vCPU $0.0413/h, memory $0.007/GiB-h; HA doubles both; db-f1-micro $0.0105/h, db-g1-small $0.035/h (shared core, **no SLA**); SSD $0.000232877/GiB-h (≈ $0.17/GiB-mo), HA SSD ≈ $0.34 | H (Iowa) | **Mumbai estimate: × 1.20 (L).** For example, 2 vCPU / 8 GiB Enterprise in Mumbai ≈ (2×0.0413 + 8×0.007) × 1.2 × 730 ≈ **$121/mo** single, ~$242 HA [E] |
| Memorystore for Valkey, **Iowa default table**: shared-core-nano (1.4 GB) $0.0318/h; standard-small (6.5 GB) $0.1425/h; highmem-medium (13 GB) $0.1923/h | H (Iowa) | Mumbai estimate × 1.20 → nano ≈ **$27.9/mo per node** [E, L]. The minimum node count per instance was not captured |
| Internet egress, Premium tier (Iowa table): $0.12/GiB (1 GiB – 1 TiB) → $0.11 → $0.085 to Asia | H (Iowa source) | **Mumbai-source egress rates not captured**; assume similar (L) |
| Cloud CDN, cache egress to Asia-Pacific: $0.09/GiB (0–10 TiB) → $0.06 → $0.05 → $0.04; cache fill within APAC $0.02/GiB | H | Cheaper per GB than CloudFront PAYG in India, but there is no flat-rate plan |
| Vertex Gemini in asia-south1 | Listed in the "Asia Pacific" group, which includes Mumbai (§2.3) | M | |

### 1.3 Cheaper alternatives with Indian regions

| Provider | Region(s) | Small app VM | Managed Postgres | Managed cache | Egress | Conf | Notes |
|---|---|---|---|---|---|---|---|
| **DigitalOcean** | **BLR1 (Bengaluru)**. No Mumbai | Basic 2 vCPU/4 GB **$24/mo**, 4 vCPU/8 GB $48 (4–5 TB transfer included); General Purpose 2 vCPU/8 GB $63 | 1 vCPU/1 GB **$15.15**, 1/2 GB $30.45, 2/4 GB $60.90 (standby node pricing not captured) | **Valkey** 1 GB $15, 2 GB $30 | Bundled allowance; overage not captured | M (pricing pages read via summarizer; BLR1 managed-DB availability from a search snippet) | Bengaluru adds ~12–25 ms for Mumbai/Delhi users versus a Mumbai host (AIC table, §3.1). No hosted LLM |
| **Hetzner** | **No India location.** Nearest is **Singapore** | not captured | — | — | — | M | Singapore is ~63 ms RTT from Mumbai (cloudping), which uses most of the 120 ms hit budget before any work. **Not suitable** for India users |
| **E2E Networks** (Indian listed company) | Delhi NCR and Mumbai (M, search snippet) | E1 2 vCPU/6 GB **$32.32/mo**; 4 vCPU/12 GB $64.64 | Smallest DBaaS listed: 4 vCPU/16 GB/200 GB **$98.55/mo** | not captured | "$0.045/GB" | M (pricing page shown in USD; INR not captured) | **GPUs in India:** L4 $0.57/h, **L40S $1.20/h (≈ $876/mo)**, A100 40 GB $1.98/h, H100 $2.69/h. This is the cheapest India-resident GPU found for self-hosting Sarvam-30B |
| **Oracle Cloud (OCI)** | Mumbai, Hyderabad | **Ampere A1: $0.01 per OCPU-h + $0.0015 per GB-h, with the first 3,000 OCPU-h and 18,000 GB-h per month free**. That is roughly 4 OCPU/24 GB always-free. Prices are the same in all regions | "Database with PostgreSQL" x86: $0.098 per OCPU-h | "Cache with Redis": $0.0194 per GB-h (≤10 GB nodes) | **Outbound from APAC: first 10 TB/month free**, then $0.025/GB | H (Oracle price-list API; free-tier ranges in the API; 10 TB free on the networking page) | For A1, 1 OCPU = 1 physical Arm core (≈ 1 vCPU). For x86, 1 OCPU = 2 vCPU. **Verify before comparing.** The egress terms are the best found. **L40S $3.50 per GPU-h** (dearer than AWS) |
| **Azure Central India** | **Pune, not Mumbai.** (South India = Chennai, West India = Mumbai) | B2s (2 vCPU/4 GB) $0.0448/h ($32.70); D2ps_v5 (Arm) $0.0506/h ($36.94); D2as_v5 $0.0556/h | PG Flexible B1ms $0.0245/h ($17.89); B2s $0.098/h | Azure Cache for Redis C0 Basic $0.022/h ($16.06); C1 Standard $0.138/h | $0.12/GB (Microsoft network, first tier after 100 GB free); $0.11 (internet routing) | H (Retail Prices API) | Pune ↔ Mumbai is a few ms. Azure Redis is Redis-licensed (see Valkey note in assistant-300ms §2.4) |

**Pilot-equivalent arithmetic** [E], against AWS single-AZ at $197:

| Provider | Line items | Total | Not captured |
|---|---|---|---|
| **DigitalOcean BLR1** | 2 × Basic 2 vCPU/4 GB ($24) + PG 1 vCPU/1 GB ($15.15) + Valkey 1 GB ($15) | **≈ $78/mo** | Load balancer, backups, standby node |
| **Oracle Mumbai** | 2 app VMs on Ampere A1 (inside the 3,000 OCPU-h / 18,000 GB-h free tier) $0 + Postgres x86 1 OCPU ($0.098 × 730 = $71.54) + Cache with Redis 2 GB (2 × $0.0194 × 730 = $28.32) | **≈ $100/mo** | PG storage, OCPU sizing for x86 PG. The Flexible Network Load Balancer is listed as free |

[I] **Findings from the comparison:**
- For a pilot, DigitalOcean BLR1 (≈ $78 + LB) or Oracle Mumbai (≈ $100 + storage) would cost **roughly half of AWS or less**. The price is weaker managed-service breadth, and on DigitalOcean a Bengaluru-hosted origin.
- AWS or GCP Mumbai remain the default for the ≤ 120 ms server budget because of in-region Valkey + Postgres + Vertex/Bedrock and the flat-rate CDN.
- The cost difference at pilot scale (~$100–150/mo) is noise next to data licences.

### 1.4 Assumptions for the three scales [E]

| Assumption | Value | Why / sensitivity |
|---|---|---|
| Queries per registered user per trading day | **10** | Card lookups, not chat turns. At ×3 (30/day), every per-query line scales ×3; infra barely moves |
| Trading days per month | 21 | |
| Share of queries inside 09:15–15:30 | 80% | Rest pre-open and post-close ("deals not yet published" etc.) |
| Intraday shape | Peak ≈ **3× the session average** at open and close; bursts **10× the average for ~10 s** | NSE intraday volume is U-shaped (Sampath & Gopalaswamy 2020, SAGE; Monash/IIMA studies, M). Zerodha: "A 10x burst in traffic over a period of 10 seconds is quite common on a trading platform" (zerodha.tech, 2020-06-14, M) |
| Cache hit ratio | **≥ 90% pilot, ≥ 95% at scale** | Set by **precompute coverage and as-of bucket size**, not user count. Precompute every card for the watchlist ∪ index constituents on each bar close |
| Payload per query | **~5 KB** (card JSON + short narrative, compressed) | Web assets go through the CDN and are cached by the browser |
| Precompute CPU | 2,000 symbols × 375 one-minute bars × ~5 ms per card ≈ **3,750 CPU-s per day ≈ 0.17 vCPU averaged over the session** | One worker is enough at every scale. With 15-minute delayed data it is 1/15 of that |
| Per-request CPU | ~5 ms on a hit (Python render + JSON), ~40 ms on a miss | At the 100k burst: 356 req/s × (0.95×5 + 0.05×40) ms ≈ **2.4 vCPU busy** |

### 1.5 Monthly totals, AWS ap-south-1, infrastructure only [E]

Formula per scale: `app + ingest/precompute worker + RDS (instance + gp3) + Valkey + ALB (+LCU) + public IPv4 + egress + cross-AZ + CloudFront plan + ~$30 (S3 backups ~$10, CloudWatch/logs ~$20)`. The script is reproducible from the rates in §1.1.

| Scale | Queries/mo | Load (avg / peak / burst req/s) | Topology | Single-AZ ("99.5%") | Multi-AZ ("99.9%") |
|---|---|---|---|---|---|
| **Pilot, 1k users** | 1k×10×21 = **210k** | 0.4 / 1.1 / 3.6 | 2× t4g.medium app; 1× t4g.medium worker; db.t4g.small + 50 GB; cache.t4g.small; CloudFront Pro | **$197** (≈ ₹18.9k) | **$278** (≈ ₹26.7k). Adds a warm-standby worker in AZ-b, RDS Multi-AZ, and a Valkey replica |
| **10k users** | **2.1M** | 3.6 / 10.7 / 36 | 2× c7g.large; 1× c7g.large worker; db.t4g.medium + 100 GB; cache.t4g.medium; CloudFront Pro | **$323** (≈ ₹31k) | **$483** (≈ ₹46k) |
| **100k users** | **21M** | 35.6 / 107 / 356 | 3× c7g.xlarge (spread across AZs only in the multi-AZ column); 1× c7g.large worker; db.m7g.large + 200 GB; cache.m7g.large; **CloudFront Business** (21M API + asset requests > Pro's 10M) | **$864** (≈ ₹83k) | **$1,202** (≈ ₹1.15 lakh) |

Line items at 100k multi-AZ, for audit: app $215.06; workers $71.69; RDS $402.07 (349.67 + 200 × 0.262); Valkey $191.55 (2 × 95.78); ALB $52.49; IPv4 $25.55; egress 105 GB × $0.1093 = $11.48; cross-AZ ≈ $2.10; CloudFront $200; other $30.

**Reading the table:**
- Egress is negligible: 21M × 5 KB ≈ 105 GB/mo, about $11.
- CPU is small.
- The **multi-AZ premium is about +40–50%**: +$81 (+41%) pilot, +$161 (+50%) at 10k, +$338 (+39%) at 100k.
- **CloudFront Pro at 10k users is borderline.** 2.1M API requests plus asset requests (e.g. ~20 per session × 2 sessions × 21 days × 10k users ≈ 8.4M) can pass Pro's 10M allowance. Treat Business (+$185/mo) as the 10k sensitivity case.
- The dominant fixed cost at 100k is the Multi-AZ database.
- **Not included:**
  - market-data and news licences ([14 §4](../14-global-market-assistant.md));
  - the LLM (§2);
  - error tracking and uptime SaaS (see [09 §1](../09-costs-and-operating-model.md) for the equivalents);
  - self-hosted Langfuse (+1 small VM and ClickHouse, roughly $40–120/mo, L);
  - GST.

**GCP equivalent at pilot scale** [E, L]:

| Component | Monthly cost |
|---|---|
| 2× e2-standard-2 | $117.5 |
| Cloud SQL, 1 vCPU/3.75 GB class | ~$60 (Iowa × 1.2) |
| Memorystore Valkey nano | ~$28 |
| Load balancer | ~$18 (not captured) |
| **Total** | **≈ $230–260/mo single-zone** |

That is broadly on par with AWS.

---

## 2. LLM cost per answer (≈ 800 input + 150 output tokens)

### 2.1 Prices and per-answer cost

| Model | Price per 1M tokens (in / out) | Cost per answer = 800·in + 150·out | Hindi/Hinglish sensitivity: output × 2 | Conf |
|---|---|---|---|---|
| **Gemini 2.5 Flash-Lite** | $0.10 / $0.40 (Batch/Flex $0.05 / $0.20; Priority $0.18 / $0.72) | **$0.000140** | $0.000200 | H (ai.google.dev pricing) |
| Gemini 3.1 Flash-Lite (Vertex replacement) | $0.25 / $1.50 (thinking tokens billed as output) | $0.000425 | $0.000650 | H |
| Gemini 3.5 Flash-Lite | $0.30 / $2.50 | $0.000615 | $0.000990 | H |
| **Gemini 2.5 Flash** | $0.30 / $2.50 | **$0.000615** | $0.000990 | H |
| **Claude Haiku 4.5** | $1 / $5 (Batch $0.50 / $2.50; cache read 0.1×). **Bedrock/Vertex regional endpoints +10%** vs global | **$0.00155** (regional: $0.00171) | $0.00230 | H (platform.claude.com pricing) |
| **GPT-4.1-mini** | $0.40 / $1.60 | **$0.00056** | $0.00080 | H (developers.openai.com model page) |
| GPT-6 Luna (current OpenAI small model; reasoning effort settable to `none`) | $0.10 / $0.50. Regional-processing endpoints +10% for eligible models released on or after 2026-03-05 | $0.000155 | $0.000230 | H |
| **Sarvam 105B** (API; Sarvam 30B API is **deprecated**) | ₹29.28 / ₹73.20 (cached input ₹10.98) → at ₹96/$: $0.305 / $0.7625 | **₹0.0344 ≈ $0.000358** | $0.000473 | M (price from official-sources §3.4) |

**Assumptions that must hold for these figures** [I]:
- **Thinking off.**
  - Gemini 3.x bills thinking tokens as output.
  - Sarvam 105B's `reasoning_effort` **defaults to `low` (on)**; the docs say to set `reasoning_effort=None` to cut tokens (docs.sarvam.ai, M).
  - GPT-6 Luna defaults to `medium`.
- **No prompt-cache discount.** An 800-token prompt is below the caching minimums (Haiku 4.5 needs ≥ 4,096 tokens; see assistant-300ms §2.4).
- **Token counts are for English.** Hindi (Devanagari) and Hinglish usually tokenise into more tokens on non-Indic tokenizers. Hence the ×2-output sensitivity column (L). Sarvam's tokenizer is Indic-optimised per the vendor.

### 2.2 Monthly LLM spend under two designs [E]

- **(a) Per query:** a narrative is generated for every query.
- **(b) Per card version:** one narrative per (intent, symbol, timeframe, as-of bucket), cached by exact key and shared across users. This is the 09 §2 principle applied to the assistant.
  - Assumed distinct card versions narrated per day: 3k (pilot), 10k (10k users), 30k (100k users). The upper bound is 2,000 symbols × 5 intents × 25 fifteen-minute buckets = 250k per day.

| Model | Pilot (a) / (b) | 10k (a) / (b) | 100k (a) / (b) |
|---|---|---|---|
| Gemini 2.5 Flash-Lite | $29 / $9 | $294 / $29 | **$2,940 / $88** |
| Gemini 3.1 Flash-Lite | $89 / $27 | $893 / $89 | $8,925 / $268 |
| Gemini 2.5 Flash | $129 / $39 | $1,292 / $129 | $12,915 / $387 |
| Claude Haiku 4.5 | $326 / $98 | $3,255 / $326 | **$32,550 / $977** |
| GPT-4.1-mini | $118 / $35 | $1,176 / $118 | $11,760 / $353 |
| GPT-6 Luna (reasoning none) | $33 / $10 | $326 / $33 | $3,255 / $98 |
| Sarvam 105B (reasoning off) | $75 / $23 | $753 / $75 | $7,526 / $226 |

[I] Design (b) is **10–35× cheaper** and also faster: a cached narrative is a Valkey GET, with no TTFT. Pair it with a **daily token cap and per-provider budget alarms** ([09 §6](../09-costs-and-operating-model.md)) so that a cache-key bug cannot silently turn (b) into (a).

### 2.3 Region availability in India

| Provider | India-region inference? | Evidence | Conf |
|---|---|---|---|
| **Vertex AI (Google)** | **Yes, asia-south1 is listed** for Gemini 2.5 Flash, 2.5 Flash-Lite, 3.1 Flash-Lite, 3.5 Flash-Lite, 3.x Flash, and for Claude-on-Google-Cloud models. The table groups "Asia Pacific" regions together, so per-region model availability should be confirmed in the console | docs.cloud.google.com/vertex-ai/…/learn/locations | M |
| **Vertex retirement** | **gemini-2.5-flash and gemini-2.5-flash-lite retire 2026-10-20**. Replacements: gemini-3.5-flash; gemini-3.5-flash-lite or gemini-3.1-flash-lite | …/learn/model-versions | **H** |
| Gemini Developer API (AI Studio) | gemini-2.5-flash-lite: "No shutdown date announced". **Global endpoint; no India processing commitment** | ai.google.dev/gemini-api/docs/deprecations | H |
| **Anthropic (Claude API)** | Global by default. `inference_geo: "us"` costs 1.1×. **No India geo option.** On Bedrock, Haiku 4.5 reaches ap-south-1 only via **Global cross-region inference** (not Mumbai-local; assistant-300ms §2.2) | platform.claude.com pricing | H |
| **OpenAI** | **`in.api.openai.com`: Storage Yes, Processing No** ("Requires MAM or ZDR"). Inference runs outside India | developers.openai.com/api/docs/guides/your-data | **H** |
| **Sarvam** | Vendor says the models are "trained entirely in India". An API hosting region is not stated in the docs read (official-sources §3.4) | sarvam.ai blog (2026-03-06); docs | M/L |
| Self-hosted (Sarvam-30B, Apache-2.0) | Yes, on any Mumbai GPU | §2.5 | H |

### 2.4 Time to first token (TTFT) from India

**No India-measured TTFT exists in any public source found.** The only defensible method is: `TTFT_india ≈ TTFT_measured (AA, GCP us-central1, 10k-token default workload) + RTT(Mumbai → serving region) (+ TLS setup if cold)`.

| Model / configuration | AA TTFT p50 (US) | Serving region seen from Mumbai | Estimated TTFT from Mumbai [E] | Conf |
|---|---|---|---|---|
| **Gemini 2.5 Flash-Lite, non-reasoning** (AI Studio) | **0.30 s**, 279 tok/s | Vertex asia-south1 (≈ 1–5 ms), until 2026-10-20; AI Studio global (unknown POP) | **~0.3 s** in-region; ≤ 0.55 s if routed to the US | H (AA) / L (derivation) |
| Gemini 3.1 Flash-Lite (AI Studio, **preview slug, AA marks it deprecated**) | **5.63 s** (reasoning time shown as "--", but the figure is consistent with default thinking) | asia-south1 | **Fast-mode TTFT unmeasured** | M |
| Gemini 3.5 Flash-Lite (**reasoning**) | **8.21 s**, 351 tok/s | asia-south1 | **Non-reasoning TTFT unmeasured** | M |
| Claude Haiku 4.5, non-reasoning | 0.63 s (assistant-300ms) | Global CRIS (unknown region) | 0.65–0.9 s | M |
| GPT-6 Luna (AA default reasoning) | **108 s** (reasoning) | Non-India processing (+~190–240 ms RTT) | Unmeasured at `reasoning=none` | M |
| Sarvam 105B ("high" reasoning) | **22.24 s** | Sarvam API (India per the vendor) | Unmeasured with reasoning off | L (search snippet of AA) |
| Sarvam-30B self-hosted | none published | Mumbai GPU | Unmeasured. The vendor claims only relative throughput (3–6× Qwen3 per H100; 1.5–3× on L40S), with no ms figures | M |

[I] AA's 10k-token default input probably **overstates** TTFT for an 800-token prompt, because prefill is shorter (L).

**Owner decision (new):** after 2026-10-20 there is **no in-region model with a measured sub-second TTFT**. The options are:
1. Keep Gemini 2.5 Flash-Lite on the **global** Gemini API. It is measured and fast, but has no India processing guarantee. This is a DPDP question for compliance-analyst.
2. Move to **Vertex asia-south1 gemini-3.1/3.5-flash-lite with thinking disabled**. It is in-region but its latency is unmeasured. Measure it in I-07 before committing.
3. **Self-host Sarvam-30B in Mumbai** (§2.5). It is in-region, has an Indic tokenizer, and gives full control, but costs a fixed GPU bill and its latency is unmeasured.

In every case the card ships first. The narrative is optional, and the 120/300 ms SLO does not depend on it.

### 2.5 Self-hosted Sarvam-30B on one Mumbai GPU

| Fact | Value | Conf |
|---|---|---|
| Weights | `sarvamai/sarvam-30b` stored as F32 (32.15B params, 128.6 GB). **`sarvam-30b-fp8`: 38.6 GB.** `sarvam-30b-gguf` Q4_K_M: **≈ 19.6 GB** (six shards). Apache-2.0. MoE, 2.4B active non-embedding params | H (HF API) |
| Fits on | **FP8 on L40S 48 GB**: leaves about 9 GB for KV cache and activations, which is enough for short prompts and modest concurrency. **Q4 GGUF on L4 24 GB**: fits with ~4 GB headroom, at a quality and speed cost (llama.cpp rather than vLLM). A100/H100 80 GB is comfortable | I |

| GPU option | $/h | 24×7 per month (730 h) | Market hours only (8 h × 21 d = 168 h) | Conf |
|---|---|---|---|---|
| AWS g6e.xlarge (L40S) | $2.235 | **$1,632** | $375 | H |
| AWS g6.xlarge (L4) | $0.9664 | $705 | $162 | H |
| GCP g2-standard-4 (L4), asia-south1 | $0.7358 | $537 | $124 | M |
| **E2E Networks L40S** (India) | $1.20 | **$876** | $202 | M |
| E2E H100 | $2.69 | $1,964 | $452 | M |
| OCI L40S | $3.50 | $2,555 | $588 | H |

- **Break-even against API calls** at 800/150 tokens, per answer, using g6e 24×7 ($1,632): about **11.7M answers/mo vs Gemini 2.5 Flash-Lite**, **4.6M vs the Sarvam API**, and **1.05M vs Haiku 4.5** [E].
- Under design (b) the assistant needs well under 1M narratives per month even at 100k users.

**So self-hosting is justified by residency, Hindi quality or latency control, not by cost.** [I]
- If it is chosen, **schedule the GPU for market hours** (~$160–375/mo).
- **Pre-warm before 09:00 IST**, because a cold load of 20–40 GB of weights takes minutes.
- Treat it as a separately monitored dependency, with degraded mode meaning "card only".

---

## 3. Latency facts and what is physically achievable

### 3.1 Indian cities → Mumbai cloud regions

| Path | RTT | Source | Conf |
|---|---|---|---|
| Mumbai ↔ Pune (Azure Central India), ↔ Ahmedabad, ↔ Hyderabad, ↔ Bengaluru, ↔ **Delhi**, ↔ Chennai, ↔ Kolkata → **AWS ap-south-1** | 8 / 20 / 22 / 28 / **30** / 32 / **40** ms (median, ICMP/TCP-SYN, 500 packets, Airtel/Jio/ACT/BSNL/MTNL fixed + Airtel/Jio 4G/5G vantage points, 2026-07-15…18) | AIC Cloud "India Cloud Latency Benchmark 2026" | **L–M: the publisher is a hosting vendor with a conflict of interest.** The numbers are consistent with fibre physics: Delhi–Mumbai ~1,150 km great-circle ⇒ ≥ 11.5 ms RTT in fibre; real routes about 2× |
| Same, → GCP asia-south1 | Within 1 ms of AWS in every city | same | L–M |
| Same, → DigitalOcean BLR1 | Bengaluru 12, Chennai 18, Hyderabad 20, **Delhi 42, Kolkata 55** | same | L–M |
| **AWS ap-south-1 ↔ ap-south-2 (Hyderabad)** | **13.7 ms** p50 (1-day) | cloudping.co | M |
| **Azure Central India (Pune) ↔ South India (Chennai)** | **19–20 ms** P50 (30 days to 2026-07-30) | learn.microsoft.com azure-network-latency | **H** |
| Azure Central India ↔ Jio India West (Jamnagar) | 29 ms P50 | same | H |

### 3.2 Mumbai → US (for Jev and US-hosted LLM APIs)

| Path | RTT p50 | Source | Conf |
|---|---|---|---|
| **AWS ap-south-1 → us-west-2 / us-west-1** | **241.6 / 241.3 ms** (1-day) | cloudping.co, read today | M |
| **AWS ap-south-1 → us-east-1 / us-east-2** | **192.9 / 200.5 ms** | same. **Corrects the 295 ms "suspect" figure** in assistant-300ms | M |
| AWS ap-south-1 → ap-southeast-1 (Singapore) / eu-west-1 | 63.2 / 120.7 ms | same | M |
| **Azure Central India → East US / Central US / West US 2 / West US / West US 3** | **198 / 223 / 210 / 218 / 231 ms** P50, 30 days to 2026-07-30 | learn.microsoft.com azure-network-latency | **H** |
| Jev (US-West only) from Mumbai | ≈ 90–100 ms server + ~240 ms RTT ⇒ **≈ 330–340 ms p50 warm** (unchanged from assistant-300ms; that appendix used a 233 ms RTT) | derivation | L |

### 3.3 In-region data-store latency

| Item | Figure | Source | Conf |
|---|---|---|---|
| Same-AZ EC2 ↔ EC2 RTT | "sub-millisecond" (enhanced networking) | AWS docs and whitepaper (search result) | M |
| **Cross-AZ RTT, ap-south-1** | **0.43 ms** (ap-south-1a ↔ 1c, among the fastest AZ pairs measured; ping, t3.micro) | bitsand.cloud, 2023-10-28 | M |
| **ElastiCache Serverless Valkey** | **p50 < 1 ms; p99 7–8 ms (v8.0), 8–9 ms (v7.2)**. Measured **during a 0 → 5M req/s scaling ramp**, 512-byte values, 80/20 read/write | aws.amazon.com blog, 2024-11-21 | H (vendor) |
| [I] Node-based Valkey, same AZ, keep-alive client | GET ≈ network RTT (~0.1–0.3 ms) + µs server time. **Use node-based, not Serverless, for the p95 120 ms path**, and keep an in-process L1 (cachetools) for the hottest cards | derivation | L |
| **Postgres simple query** | pgbench select-only (PK lookup) is "mostly bound by connection latency". CYBERTEC: **1.135 ms average with 10 concurrent local clients**; 21.66 ms with 10 ms added delay; 112.6 ms with 50 ms added. This is 10-client queueing in 2020, **not** single-query latency | cybertec-postgresql.com (2020-05); postgresql.org pgbench docs | M |
| [I] RDS PG PK lookup, same AZ, pooled connection | ≈ 0.3–1 ms. **A cross-AZ primary after a Multi-AZ failover adds ~0.4–1 ms per round trip**, so keep queries to 1–2 round trips per miss | derivation | L |

### 3.4 Mobile last mile in India

| Metric | Value | Source | Conf |
|---|---|---|---|
| **India mobile median latency, August 2026** | **35 ms** (fixed broadband: 16 ms). Median *idle* latency to the **nearest** Speedtest server. **Not p95, not loaded, not to Mumbai** | speedtest.net/global-index/india ("Updated August 2026") | H |
| Per-operator mobile latency, 12 months to end of Q1 2026 | **Airtel 62.9 ms, Jio 67.1 ms, Vi 92.4 ms, all 68.9 ms**. Fixed: ACT 22.6, all 40.2 ms. About 61k mobile tests (3G/4G/5G) on SpeedGeo's V-Speed | telecomtalk.info citing SpeedGeo (M) | M |
| Opensignal India (Feb 2026 report, Oct–Dec 2025 window) | Reports "Games Experience" scores (Airtel 70.6, Vi 69.9, Jio 65.9, BSNL 56) that fold in latency, jitter and loss. **No ms figures in the public page** | insights.opensignal.com | M |
| 5G SA (Jio) latency | "< 20 ms" (secondary blog) | ddkisan.in | L |
| Radio wake-up (RRC idle → connected) on 4G | Typically tens to ~100 ms for the first packet after idle | general 3GPP behaviour; no India-specific measurement found | L |

### 3.5 Physically achievable: a cached card on 4G/5G [E]

**Model:** `client time = connection setup RTTs × RTT_to_Mumbai + 1 × RTT (request) + server time + transfer`.
- `RTT_to_Mumbai ≈ last mile + inter-city leg`.
- **Median Delhi user:** 35 ms (Ookla median) + 30 ms (Delhi → Mumbai) ≈ **65 ms**.
- **Bad-tail user:** SpeedGeo's Vi mean of 92 ms is not a p95. I assume **p95 last mile ≈ 150–200 ms** under load (L), giving **≈ 200 ms** to Mumbai.
- Server time for a hit is 10–30 ms (in-region Valkey + render). A 5 KB transfer is negligible at 100+ Mbps median downlink (Ookla India mobile median 164.97 Mbps).

| Connection state | Arithmetic (median Delhi) | Median | Arithmetic (p95) | p95 | Meets 300 ms? |
|---|---|---|---|---|---|
| **Warm** (keep-alive HTTP/2, SSE or WebSocket already open) | 1 × 65 + 20 | **≈ 85 ms** | 1 × 200 + 40 | **≈ 240 ms** | **Yes** at median and p95. Tight at p95 on Vi |
| Cold, HTTP/3 (QUIC 1-RTT handshake) | 2 × 65 + 20 + DNS ~20 | ≈ 170 ms | 2 × 200 + 40 + 50 | ≈ 490 ms | Median yes; **p95 no** |
| **Cold, TCP + TLS 1.3** | 3 × 65 + 20 + DNS ~20 | **≈ 235–250 ms** | 3 × 200 + 40 + 50 | **≈ 690 ms** | Median borderline; **p95 no** |
| Cold, TLS terminated at an **in-city CloudFront edge** (edges in Mumbai, New Delhi, Chennai, Hyderabad, Bengaluru, Kolkata; M), with the edge holding a warm connection to the origin | 3 × 35 + 30 (edge → Mumbai) + 20 | ≈ 155 ms | 3 × 120 + 30 + 40 | ≈ 430 ms | Median yes; **p95 still no** |
| + 4G radio wake-up after idle | + 50–100 ms | | | | Pushes cold p95 further out |

**Verdict:**
- A **server-side p95 of 120 ms on a hit and 300 ms on a miss is achievable** with room to spare: 10–70 ms expected (assistant-300ms §2.3).
- **A user-perceived p95 ≤ 300 ms on 4G is achievable only on warm connections.** It is **not physically guaranteed** on cold connections, whatever the server does.
- This is a **yes/no split by connection state, not by engineering effort.**

**Mitigations, in order of value** [P]:
1. Open the connection on app start or focus, keep it alive, and prefetch the watchlist cards.
2. Use HTTP/3 where the client supports it.
3. Terminate TLS at an India edge (CloudFront or Cloud CDN), with the API behind it.
4. Keep responses ≤ 14 KB so they fit in the TCP initial congestion window.
5. Show the card from the local cache immediately, with its `as_of` visible, then refresh.

### 3.6 SLI definitions to adopt [P]

| SLI | Measured at | Target |
|---|---|---|
| **`ttfuc_server_ms`**: ingress receive → first card byte flushed | ALB/app, per intent, split hit/miss | p95 ≤ 120 ms (hit), ≤ 300 ms (miss) |
| **`ttfuc_client_ms`**: tap → card rendered | RUM beacon, **split warm/cold and by network type** | Report only (not an SLO) at first. Set targets after 4 weeks of data |
| `narrative_ttft_ms` | App → LLM | Report only; the card never waits for it |
| `card_freshness_s` during market hours | Precompute worker heartbeat vs bar close | Per feed; alert on stall (a heartbeat, not HTTP uptime) |

---

## 4. Engineering effort (MVP)

**Evidence base:** there are no public effort reports for this exact product. The anchors are:
- **The existing plan:** [08](../08-implementation-roadmap.md) estimates **33–47 engineer-weeks (ew) for US Stages 0–5** with 1 senior engineer + 0.3 FTE frontend. That is about 8–11 months elapsed.
- **Comparable finance MCP servers:**
  - Zerodha `kite-mcp-server` (Go): created 2025-02-24, first release v0.0.1 on **2025-04-29**, about 9 calendar weeks, one dominant contributor (42 of 43 commits in the top-5 list).
  - Massive `mcp_massive` (Python): created 2025-03-19, v0.1.0 on **2025-05-14**, about 8 weeks, one dominant contributor.
  - These are **calendar time, not effort** (GitHub API, H for dates; L as an effort proxy).
- **Scope decisions already made** in 13, 14 and official-sources: TA-Lib, Valkey, the rapidfuzz + IndicXlit resolver, a read-only MCP, and Langfuse.

All figures below are **[E, L]** ranges for one competent Python engineer, excluding vendor and counsel wait time.

| Component | Task IDs | ew (low–high) | What drives the range |
|---|---|---|---|
| Symbol master + resolver (NSE/BSE codes, ISIN, symbol-change history, Hinglish aliases pre-generated offline) | I-03 | **2–4** | Alias quality for Hinglish; corporate-action and ISIN change history |
| Ingest of licensed EOD + delayed feed (adapter, calendars and half-days, entitlement labels, backfill, freshness SLI, recorded fixtures) | I-01 dependency; T-ingest in 08 | **3–5** | Vendor API quality; the gap-fill and replay story |
| Card precompute engine (canonical indicator spec, volatility, events, versioned cards, golden tests) | I-05 | **4–7** | Golden-fixture work against TradingView/Kite values; the Indian dated rules (expiry days, closing auction) |
| Cache + API (Valkey exact keys, L1, as-of buckets, stale labelling, auth, latency harness) | I-04, Q-01 | **2–4** | The harness and p95 proof on a recorded day |
| Grounded narrative + verifier (prompt, numeric/ticker validator, abstention, offline eval harness) | I-07, 06 §5 | **3–5** | Plus **60–80 h of gold-set annotation** ([09 §5](../09-costs-and-operating-model.md)) and Hinglish cases |
| MCP server (read-only evidence tools, OAuth for directory listing) | I-06 | **1–3** | The directory-listing requirements of Claude and ChatGPT |
| Web app (cards, watchlists, freshness/entitlement badges, auth, accessibility) | T-23 analogue | **4–8** | Design polish; 0.3 FTE design is assumed separately |
| Telegram bot (non-advisory guardrails, rate limits, link-outs) | — | **1–2** | Guardrail copy review with compliance-analyst |
| Observability, CI, tests (T-02 tooling, T-03 tests, SLO dashboards, heartbeat/freshness alerts, runbooks, deploy pipeline) | T-02, T-03, Q-01 | **3–5** | The drill logs and runbooks per 07 §5 |
| Security hardening (authz and tenant isolation, secrets, rate limiting, input validation, dependency audit) | T-36 analogue | **2–4** | Plus an external pentest of $5–15k (09 §5) |
| **Subtotal** | | **25–47** | |
| Integration, bug-fix and ops overhead (+15–25%) | | +4–12 | |
| **Total** | | **≈ 29–59 ew** | |

**Team-size scenarios** [E, L]:
- **One method for all rows:** `elapsed weeks = ew ÷ (developers × parallel efficiency × 0.8)`.
  - The 0.8 is the share of each week spent on build (the rest goes to meetings, support, on-call and vendor calls).
  - Parallel efficiency is assumed to be 1.0 for one developer, 0.8 each for two, and 0.65 each for four, reflecting coordination cost (Brooks). Four developers do not deliver 4× throughput.
- Months are weeks ÷ 4.35.

| Team | Divisor | Elapsed for 29–59 ew | Binding constraint |
|---|---|---|---|
| **1 developer** (08's current assumption, plus 0.3 FTE design) | 1 × 1.0 × 0.8 = 0.8 | **≈ 36–74 weeks → 8–17 months** | Everything is serial. On-call is one person, which [09 §6](../09-costs-and-operating-model.md) already flags |
| **2 developers** (platform/data + app/frontend) | 2 × 0.8 × 0.8 = 1.28 | **≈ 23–46 weeks → 5–11 months** | Card spec, golden tests and the ingest adapter are the critical path |
| **4 developers** (data, quant/cards, backend/MCP, frontend) | 4 × 0.65 × 0.8 = 2.08 | **≈ 14–28 weeks → 3–6.5 months** | **Calendar floor of ~3 months** from I-01 (NSE/vendor licence answers), I-02 (counsel memo) and gold-set annotation, regardless of headcount |

---

## 5. Reliability: 99.5% vs 99.9%

### 5.1 What the SLA contracts actually back [F, H + arithmetic]

| Component | Single-AZ SLA | Multi-AZ SLA | Source |
|---|---|---|---|
| EC2 | 99.5% (instance level) | 99.99% (region level, multi-AZ) | aws.amazon.com/compute/sla (updated 2022-05-25) |
| RDS | 99.5% (single-DB instance) | 99.95% (Multi-AZ) | aws.amazon.com/rds/sla (updated 2024-01-22) |
| ElastiCache | 99.5% (single-AZ) | 99.99% (Multi-AZ and Serverless) | aws.amazon.com/elasticache/sla (updated 2024-10-16) |

- **In series, single-AZ:** 0.995³ ≈ **98.5%**. **A 99.5% SLO on a single-AZ stack is not backed by any SLA.** It relies on AWS usually beating its SLA.
- **Multi-AZ:** 0.9999 × 0.9995 × 0.9999 ≈ **99.93%**. That backs a 99.9% SLO, with little margin left for our own deploys and bugs.

### 5.2 Error budgets: define the window

| SLO | Market-hours window (375 min × 21 d = 7,875 min/mo) | Calendar month (43,800 min) |
|---|---|---|
| 99.5% | **39 min/mo** | 219 min/mo |
| 99.9% | **7.9 min/mo** | 43.8 min/mo |

[P] **Measure availability over market hours plus the pre-open window.** That is when the product matters, and it matches the on-call model in 09 §6. At 99.9% that leaves **under 8 minutes of market-hours downtime per month**.
- **Consequences:**
  - no deploys during market hours except hotfixes;
  - rolling deploys with health checks;
  - a singleton ingest that stops before it starts, behind an advisory lock;
  - expand/contract migrations after a backup.
- **Exclude from the availability SLI** (or cover with degraded mode): the LLM narrative and the data vendor.
  - The **vendor feed bounds the freshness SLO**, which gets its own SLI and a heartbeat alert. HTTP uptime checks do not catch a stalled feed.

### 5.3 Architecture and cost delta [E]

| | 99.5% (single-AZ) | 99.9% (multi-AZ) | Delta |
|---|---|---|---|
| App | ≥ 2 instances (same AZ), rolling deploy | ≥ 2 instances across 2–3 AZs behind the ALB | ≈ $0 (same count) |
| Ingest/precompute worker | 1 instance | 1 active + **warm standby in AZ-b** (advisory lock; stop-before-start) | +1 worker |
| Postgres | RDS Single-AZ + automated backups (PITR) | **RDS Multi-AZ** (sync standby, ~60–120 s failover, M) | ≈ 2× instance + 2× storage |
| Valkey | 1 node; cold-start is fine because precompute can refill | Primary + replica with Multi-AZ auto-failover | 2× |
| Cross-AZ traffic | — | $0.01/GB each way | negligible (~$2/mo at 100k) |
| **Monthly (from §1.5)** | $197 / $323 / $864 | $278 / $483 / $1,202 | **+$81 / +$161 / +$338 (+41% / +50% / +39%)** |
| Region-level DR (optional, for 99.95%+) | — | Warm standby in **ap-south-2 Hyderabad** (13.7 ms away) or asia-south2 Delhi: ~+60–100% | Only after a paying need |

[I] **For this product the 99.9% premium is small in money (~₹8k–32k/mo), and the real cost is operational discipline.** That means:
- zero-downtime deploys;
- failover drills every quarter (restore drill already in 09 §6);
- runbooks for every failure scenario in 07 §5.

### 5.4 Exchange-hours load pattern (India)

| Window (IST) | Expected load | Evidence / implication |
|---|---|---|
| 08:45–09:15 (pre-open, block window 08:45–09:00; new pre-open phases from 2026-09-07) | Rising: watchlist refresh, overnight news cards | Pre-warm GPU and caches by 08:45. Precompute EOD/overnight cards before 08:30 |
| **09:15–09:45 (open)** | **Peak: ~3× session average; 10× bursts over ~10 s** | U-shaped NSE intraday volume (SAGE 2020; Monash/IIMA, M). Zerodha's 10× in 10 s (M). **Scale out before 09:10 on a schedule, not reactively** |
| 11:00–14:00 | Trough | Safe window for non-urgent batch work, never for deploys |
| 14:05–14:20 (second block window) and **15:00–15:30 (close; closing auction sets the official close from 2026-08-03)** | Second peak | Cards must say "closing auction in progress" or show the official close only once published |
| Post-close (bulk/block deal files, results, F&O participant OI ~19:00) | Moderate spike for "deals" and "results" intents | Batch ingest; cards say "not yet published" until then |
| Nights, weekends, NSE holidays | Low | Deploy window. Use `exchange_calendars` for holidays and half-days (invariant 4) |

---

## 6. Recommendations (for the tech-lead and owner)

1. **Host on AWS ap-south-1**, or GCP asia-south1 if Vertex-local Gemini is chosen.
   - Graviton c7g for the app tier.
   - Node-based ElastiCache Valkey plus an in-process L1.
   - RDS PostgreSQL.
   - CloudFront Pro/Business flat plan with TLS at the India edges.
   - Budget **~₹20–30k/mo for the pilot** and **≤ ₹1.2 lakh/mo at 100k users** for infrastructure, before data and the LLM. [E]
2. **Adopt "one narrative per card version"** as a hard design rule with a daily token cap. That keeps the LLM at **≤ $1k/mo at 100k users** on any model listed. [E]
3. **Decide the narrative model before 2026-10-20** (§2.4). Extend I-07 to measure, from a Mumbai VM with approval:
   - Vertex asia-south1 3.1/3.5 Flash-Lite with thinking off;
   - Gemini API 2.5 Flash-Lite;
   - Haiku 4.5 via Bedrock global CRIS;
   - Sarvam 105B API with reasoning off;
   - Sarvam-30B FP8 on one L40S (E2E or g6e).

   Record p50/p95 TTFT, Hindi token counts and cost.
4. **Write the latency SLO as server-side TTFUC** (§3.6). Publish client p95 split warm/cold, and never promise "300 ms on 4G" without the "warm connection" qualifier.
5. **Choose 99.9% measured over market hours** once there are paying users. Until then, run a single-AZ pilot with backups, and state honestly that it is **not SLA-backed**.
6. **Plan staffing with the calendar floor in mind.** Adding developers beyond two does not beat the NSE-licence and counsel timelines.

## 7. Unverified / open

1. **GCP Mumbai prices** for Cloud SQL, Memorystore and egress. The ×1.20 uplift over Iowa is inferred from E2 only.
2. **Mumbai NAT gateway price** (primary not read).
3. **CloudFront flat-plan prices** ($15/$200/$1,000) come from secondary sources. The allowances are from AWS docs (H).
4. **The ElastiCache Serverless Valkey Mumbai rates** look anomalously low against us-east-1.
5. **DigitalOcean BLR1:** managed-DB availability and standby pricing.
6. **E2E:** INR prices and exact regions.
7. **Oracle:** OCPU-to-vCPU normalisation for x86 Postgres.
8. **No India-measured LLM TTFT** for any provider. No non-reasoning AA measurement for Gemini 3.1/3.5 Flash-Lite, GPT-6 Luna or Sarvam.
9. **Per-region (not grouped) Vertex model availability** for asia-south1.
10. **Mobile p95 / loaded latency for India:** Ookla gives a median idle only, and Opensignal's ms figures are paywalled. The p95 last-mile figure in §3.5 is an assumption.
11. **Intercity latency** comes from a vendor-published benchmark (AIC Cloud) with a conflict of interest. WonderNetwork (independent) was unreachable today.
12. **The INR/USD rate** is from a secondary quote. The Federal Reserve H.10 page was blocked by a bot challenge.
13. **The Valkey node-based p95 in Mumbai** is not measured. Q-01/I-04 should measure it on a recorded day.

## 8. Sources (all accessed 2026-09-24)

**AWS (official price files and docs)**
- EC2 Mumbai metered-unit map (publication 2026-09-21): https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/ec2/USD/current/ec2-ondemand-without-sec-sel/Asia%20Pacific%20(Mumbai)/Linux/index.json
- RDS (2026-09-22): https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/current/ap-south-1/index.json
- ElastiCache (2026-09-14): https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonElastiCache/current/ap-south-1/index.json (us-east-1 file for the cross-check)
- DataTransfer (2026-09-16): https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSDataTransfer/current/ap-south-1/index.json
- CloudFront (2026-09-16): https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudFront/current/index.json
- ELB (2026-09-11): https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AWSELB/current/ap-south-1/index.json
- VPC (2026-09-17): https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonVPC/current/ap-south-1/index.json
- CloudFront flat-rate plans: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/flat-rate-pricing-plan.html
- Plan prices (secondary): https://cloudburn.io/blog/amazon-cloudfront-pricing
- SLAs: https://aws.amazon.com/compute/sla/ ; https://aws.amazon.com/rds/sla/ ; https://aws.amazon.com/elasticache/sla/
- Valkey latency: https://aws.amazon.com/blogs/database/amazon-elasticache-version-8-0-for-valkey-brings-faster-scaling-and-improved-memory-efficiency
- CloudFront India edges (secondary): https://aws.amazon.com/about-aws/whats-new/2020/05/cloudfront-kolkata-hamburg/ ; https://aws.amazon.com/about-aws/whats-new/2018/09/cloudfront-second-edge-location-delhi/
- NAT (secondary, unverified): https://costgoat.com/pricing/aws-nat-gateway

**GCP**
- https://cloud.google.com/memorystore/docs/valkey/pricing
- https://cloud.google.com/sql/pricing
- https://cloud.google.com/vpc/network-pricing
- https://cloud.google.com/cdn/pricing
- https://gcloud-compute.com/e2-standard-2.html
- https://gcloud-compute.com/g2-standard-4.html
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/locations
- https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions

**Azure**
- https://prices.azure.com/api/retail/prices (queries for centralindia VMs, PostgreSQL Flexible, Redis Cache, Bandwidth)
- https://learn.microsoft.com/en-us/azure/networking/azure-network-latency (dataset ending 2026-07-30)

**Oracle**
- https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/?currencyCode=USD
- https://www.oracle.com/cloud/networking/pricing/

**Other providers**
- https://www.digitalocean.com/pricing/droplets
- https://www.digitalocean.com/pricing/managed-databases
- https://docs.digitalocean.com/products/databases/
- https://www.hetzner.com/cloud/
- https://www.e2enetworks.com/pricing
- https://www.e2enetworks.com/compute-products

**LLMs**
- https://ai.google.dev/gemini-api/docs/pricing
- https://ai.google.dev/gemini-api/docs/deprecations
- https://platform.claude.com/docs/en/about-claude/pricing
- https://developers.openai.com/api/docs/pricing
- https://developers.openai.com/api/docs/models/gpt-4.1-mini
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://developers.openai.com/api/docs/guides/your-data
- https://docs.sarvam.ai/api-reference-docs/getting-started/models/sarvam-105b
- https://www.sarvam.ai/blogs/sarvam-30b-105b
- https://huggingface.co/api/models/sarvamai/sarvam-30b ; https://huggingface.co/api/models/sarvamai/sarvam-30b-fp8 ; https://huggingface.co/api/models/sarvamai/sarvam-30b-gguf
- https://artificialanalysis.ai/models/gemini-2-5-flash-lite/providers
- https://artificialanalysis.ai/models/gemini-3-1-flash-lite-preview/providers
- https://artificialanalysis.ai/models/gemini-3-5-flash-lite
- https://artificialanalysis.ai/models/gpt-6-luna
- https://artificialanalysis.ai/models/sarvam-105b/providers (via search snippet)

**Latency and networks**
- https://www.cloudping.co/ (p50, 1-day)
- https://aiccloud.in/blog/india-cloud-latency-benchmark-2026 (vendor)
- https://www.bitsand.cloud/posts/cross-az-latencies
- https://www.cybertec-postgresql.com/en/postgresql-network-latency-does-make-a-big-difference/
- https://www.postgresql.org/docs/current/pgbench.html
- https://www.speedtest.net/global-index/india
- https://telecomtalk.info/jio-leads-mobile-speeds-india-speedgeo-q12026/1006590/
- https://insights.opensignal.com/reports/2026/02/india/mobile-network-experience
- https://ddkisan.in/help/airtel-vs-jio-which-is-faster/

**Load pattern**
- https://zerodha.tech/blog/scaling-with-common-sense/
- https://journals.sagepub.com/doi/abs/10.1177/0972652720930586
- https://www.monash.edu/__data/assets/pdf_file/0008/925811/intraday_liquidity_patterns_in_indian_stock_market.pdf

**Effort anchors**
- GitHub REST API: repos/zerodha/kite-mcp-server, repos/massive-com/mcp_massive (created_at, releases, contributors)

**FX**
- https://www.bookmyforex.com/currency-converter/usd-to-inr/forecast/ (₹95.96 on 2026-09-24, secondary; rounded to ₹96)
