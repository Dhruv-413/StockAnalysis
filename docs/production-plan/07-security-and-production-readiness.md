# 07 — Security and Production Readiness

← [Index](README.md) · Previous: [06 Quantitative validation](06-quantitative-validation.md) · Next: [08 Roadmap](08-implementation-roadmap.md)

Passing unit tests, a clean build or a polished UI does **not** make this product production-ready. It is production-ready when **every gate below has recorded evidence**. All service-level targets are **proposals** until they are measured in Stage 3–4 ([08](08-implementation-roadmap.md)).

---

## 1. Immediate security actions (before any other work)

| # | Action | Owner | Evidence of completion |
|---|---|---|---|
| S0.1 | Rotate or revoke the Google, Finnhub, Twelve Data and Alpha Vantage keys that were committed in `9a6f32a`/`c79b38a`. The repository is **public**. | Repo owner (only they can do it) | Provider dashboards show the old keys revoked |
| S0.2 | Decide whether to purge the history (`git filter-repo` plus a force-push, which breaks forks and clones). Rotation is mandatory; purging is optional hygiene. | Repo owner | Decision recorded in an [ADR](adr/) |
| S0.3 | Enable GitHub secret scanning and push protection on the repository | Repo owner | Settings screenshot or API output |
| S0.4 | Add `.env.example` with placeholder values only. Keep the Claude Code guard hook ([10](10-claude-code-setup.md)). | Dev | File present; hook tests pass |

## 2. Security architecture (target)

- **AuthN:** a managed identity provider with email magic link or passkey, and optional OAuth. The provider choice is in [05](05-target-architecture.md). Sessions use HTTP-only secure cookies. No passwords are stored by us.
- **AuthZ:**
  - A single-tenant-per-user model in the MVP.
  - Every row that belongs to a user carries `user_id`.
  - Every query path is scoped in the repository/service layer.
  - Postgres Row-Level Security is enabled as defence-in-depth on user tables (`watchlists`, `alert_rules`, `alerts_delivered`, `feedback`).
  - Market-data tables are global and read-only to the application role.
- **Tenant isolation tests:** automated tests assert that user A cannot read or modify user B's watchlists, alerts or exports, through both the API and direct SQL with the app role.
- **Secrets:**
  - Stored in the platform secret store (for example Fly/Render secrets or AWS Secrets Manager), never in the repo.
  - A separate key per environment.
  - Rotation runbook, with a quarterly rotation drill.
  - The LLM provider runs on a **paid tier only**: the Gemini free tier uses content to improve Google's products ([market-data §F](research/market-data.md)).
- **Encryption:** TLS everywhere, including to the database. Encryption at rest is provided by the managed Postgres and object store. Exports are delivered through short-lived signed URLs.
- **Input and LLM safety:**
  - Structured requests only (no free-text prompt path in the MVP).
  - Retrieved documents are treated as untrusted data and placed in delimited prompt sections.
  - The LLM has no tools and no secrets in context.
  - Output is JSON-schema validated plus the hard gates in [06 §5](06-quantitative-validation.md#5-llm-explanations-evaluation).
- **Web:**
  - Strict CORS allow-list. This replaces `*` with credentials ([01 finding 19](01-repository-assessment.md#44-medium--security-and-operations)).
  - CSRF protection for cookie auth.
  - CSP headers.
  - Generic error bodies with a correlation ID. Internal exception text is never returned ([01 finding 18](01-repository-assessment.md#44-medium--security-and-operations)).
- **Rate limits:**
  - Per-user and per-IP limits at the edge and in the app, backed by Redis (or Postgres) so they apply across instances.
  - Separate budgets for expensive endpoints such as exports.
- **Dependency security:**
  - A lock file (`uv.lock`) with hashes.
  - Dependabot or Renovate.
  - `pip-audit` in CI, which fails on high-severity issues.
  - SBOM generation on release.
  - Container image scanning.
- **Audit log** (append-only table, retained 1 year): authentication events, watchlist and rule changes, export downloads, admin actions, detector/prompt/model version changes, and data-vendor switches.
- **Privacy:**
  - Store the minimum: email and watchlists.
  - Watchlists are sensitive, because they can reveal positions: treat them as confidential and exclude them from analytics exports.
  - Provide data export and deletion on request.
  - The privacy policy names the LLM subprocessor.
  - EU/UK users would bring in GDPR. They are out of pilot scope unless decided otherwise ([11](11-evidence-and-open-questions.md)).

## 3. Proposed service-level objectives

| Service | SLI | Proposed SLO | Measurement |
|---|---|---|---|
| Web/API availability | Successful requests / total, market hours | 99.5% monthly (pilot); 99.9% (GA) | Synthetic checks every minute plus server metrics |
| Alert latency | `notify_ts − bar_publish_ts` | p95 ≤ 90 s, p99 ≤ 180 s during market hours | Per-alert timestamps ([04 §1](04-real-time-data-strategy.md#1-timestamps-the-data-model-is-required-to-carry-all-five)) |
| Data freshness | Share of subscribed symbols with a fresh bar | ≥ 99% of market minutes | Freshness monitor |
| Evidence freshness | EDGAR acceptance → ledger | p95 ≤ 3 min | Poll timestamps |
| Alert delivery | Notifications accepted by the provider / attempted | ≥ 99.5%; zero duplicates | Delivery log with idempotency keys |
| Data correctness | Daily reconciliation mismatches that are unexplained | 0 open for more than 1 trading day | Reconciliation job ([06 §4](06-quantitative-validation.md#4-alert-engine-validation-mvp)) |
| Recovery | RPO / RTO for the database | RPO ≤ 15 min, RTO ≤ 2 h | Quarterly restore drill |

## 4. Release gates

Each gate needs **artifact evidence** linked from the release checklist. "It works on my machine" does not count.

| Gate | Criteria | Test method | Required evidence |
|---|---|---|---|
| **G1 Functional** | All MVP workflows in [02 §4](02-product-thesis.md#4-scope-of-the-first-release) work end to end | API tests plus Playwright E2E on staging with a replayed market day | CI run URL; E2E video or trace |
| **G2 Financial correctness** | AR, z, RVOL and adjustments match golden fixtures; property tests pass; 20 fixture days include a split, ex-dividend, half-day, halt, DST and IPO | pytest golden and property tests ([06 §4](06-quantitative-validation.md#4-alert-engine-validation-mvp)) | Test report; fixture spreadsheet checked in |
| **G3 Data quality & freshness** | 10 consecutive trading days of shadow operation. Freshness SLO met. Reconciliation shows 0 unexplained mismatches. Every displayed price carries an entitlement label. | Shadow run; reconciliation job; UI label audit | Dashboards export; reconciliation log |
| **G4 Explanation quality** | [06 §5](06-quantitative-validation.md#5-llm-explanations-evaluation) gates met on a gold set of about 800 cases | Offline eval harness plus a human AIS audit | Eval report with confidence intervals; rater κ |
| **G5 Reliability & recovery** | All failure-scenario drills (§5) pass. Backup restore succeeds within RTO. | Chaos and replay drills on staging | Drill log with timings |
| **G6 Security & access** | Zero high/critical findings from `pip-audit` and image scans. Tenant-isolation tests pass. Secrets are only in the store. Keys rotated (S0.1). An external review or pentest of auth and IDOR before GA. | CI scanners; isolation tests; pentest | Reports; rotation evidence |
| **G7 Performance** | At 2× expected pilot load (for example 400 users, 3,000 symbols, a peak burst at the open), alert p95 ≤ 90 s and API p95 ≤ 300 ms | Load test (k6 or Locust) with the replay feed at 1× and 5× speed | Load-test report |
| **G8 Usability & accessibility** | WCAG 2.2 AA on core flows. 5-user usability test completes the main tasks without help. Freshness labels are understood (≥ 4 of 5 users can explain "Delayed 15 min"). | axe-core in CI; moderated tests | Axe report; usability notes |
| **G9 Operations** | Runbooks for every §5 scenario. On-call rota (even if it is one person, with a documented escalation path). Status page. Support inbox. | Tabletop exercise | Runbook links; tabletop notes |
| **G10 Licensing & regulatory** | Signed vendor agreements covering **display to paying users**, storage and derived data. Exchange agreements where required (for example NYSE delayed redistribution; DataCT before 2027-03-01 if real-time). Non-pro attestation flow. Counsel memo on the publisher's exclusion, disclaimers and marketing claims (no AI-washing, [products §regulation](research/products.md)). Terms of Service and Privacy Policy published. | Legal review | Signed contracts; counsel memo |

**GA additionally requires:** G1–G10 green, and the stop/go criteria in [08](08-implementation-roadmap.md#stopgo-gates) met.

## 5. Failure scenarios (each needs a runbook and a drill)

| Scenario | Detection | Expected behaviour | Drill |
|---|---|---|---|
| Provider downtime or WebSocket disconnect | Heartbeat or connection-state metric; stale-symbol share | Reconnect with back-off. Enter `prices-degraded` after 2 min. Banner shown. No alerts on stale symbols. Backfill on recovery with no push for old moves. | Kill the ingestor connection on staging during a replay |
| Stale or corrupted prices (for example a price ×100, negative volume, a bar outside the day's high/low) | Validation rules on ingest (pandera-style schema plus range checks versus the previous close); cross-source spot check | The bar is quarantined and never feeds the detector. Incident opened. Symbol marked "data under review". | Inject bad bars in replay |
| Duplicate or out-of-order events | Natural-key upsert conflicts; lateness histogram | Idempotent upsert. No duplicate alerts (deterministic alert key). | Replay with shuffled and duplicated bars |
| Missing events or partial backfill | Gap detector versus benchmark bars; backfill job status | Backfill runs. Alerts for backfilled windows are archive-only. The partial state is visible in the admin view. A backfill job is resumable by (symbol, window). | Interrupt a backfill midway |
| Corporate-action error (missed split, wrong ratio) | Pre-open check comparing the adjusted previous close with the vendor's adjusted value; the z-score outlier cluster that follows | Block alerts for the symbol. Correct the CA table (versioned). Re-derive affected alerts and mark them "corrected". | Fixture with a deliberately wrong split |
| LLM outage, drift or hallucination | Error rate; hard-gate failure rate; weekly human audit | Fall back to the deterministic ledger. Auto-disable summaries if the hard-gate failure rate exceeds 1% in an hour. | Fault-inject LLM timeouts and garbage output |
| Alert delivery failure (email or push provider) | Provider webhooks; delivery lag | Retry with an idempotency key. The in-app alert is always stored. A second channel can be used if configured. | Point email at a sandbox that returns 5xx |
| Deployment failure | Health checks; error-rate SLO burn | Blue/green or rolling deploy with automatic rollback. Deploys are blocked during market hours except for hotfixes. | Deploy a deliberately failing build to staging |
| Migration failure | Migration job exit status | Expand/contract migrations only. They are backward compatible for one release, so rollback of code does not need rollback of the schema. Take a backup before any destructive step. | Run the migration against a restored production snapshot |
| Clock skew | Chrony offset metric | Alert if the offset is over 250 ms, because latency SLIs depend on the clock. | — |
| Quota exhaustion at a vendor | Budget counters | Shed low-priority work (for example backfills) first. Never fall back to an unlicensed source. | Lower the quota on staging |

## 6. Operational support

- **Observability:**
  - OpenTelemetry traces and metrics.
  - Structured JSON logs with a correlation ID. No raw user queries or watchlists in logs.
  - Error tracking in Sentry or equivalent.
  - Dashboards: freshness, latency, alert volume, LLM gate failures, vendor quota.
  - Tooling choices are in [03](03-market-and-tooling-research.md) and [05](05-target-architecture.md).
- **Incident response:**
  - Severity levels: SEV1 is incorrect data shown to users or an outage in market hours. SEV2 is degraded evidence or latency. SEV3 is everything else.
  - A status page.
  - A post-incident review within 5 business days for SEV1/2.
  - Incorrect-data incidents include a user notice and correction of the affected alerts.
- **Backups:**
  - Managed Postgres PITR with 7–14 days of retention.
  - A daily logical dump to object storage, retained 35 days.
  - A quarterly restore drill.
- **Data retention (proposal):**
  - Raw bars: as long as the licence allows (record this per vendor).
  - Alerts and ledgers: 2 years.
  - Audit log: 1 year.
  - Application logs: 30 days.
  - LLM prompts and outputs: 180 days (needed for evaluation).
- **Documentation:** a runbook per scenario, an architecture overview ([05](05-target-architecture.md)), a data dictionary, and a vendor/licence register.

## 7. Regulatory questions to resolve (counsel required; not legal advice)

1. Does per-watchlist alerting with grounded summaries stay within the Investment Advisers Act publisher's exclusion? The relevant tests are impersonal, bona fide, and general and regular circulation. *Seeking Alpha* (S.D.N.Y. 2024) is supportive but not binding precedent. The safer design is **one canonical explanation per event, shared by all users** ([products §regulation](research/products.md)).
2. Disclaimers and marketing language. Avoid performance or "AI accuracy" claims that cannot be substantiated (the SEC's 2024 AI-washing actions).
3. Jurisdiction of the operating entity and of the users. The owner's location, and whether non-US users are served, are open ([11](11-evidence-and-open-questions.md)).
4. Consequences of the professional/non-professional attestation and record-keeping duties under vendor and exchange agreements.
