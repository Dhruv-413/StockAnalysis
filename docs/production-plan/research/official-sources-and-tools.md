# Research: new tools and official data sources (India-first, US second leg)

- **Author:** tech-scout
- **Access date for every URL:** 2026-09-24
- **Scope:** things the existing appendices do not already cover. Items that are already covered get a single "delta only" row that points to the appendix. The appendices checked were tech-radar, global-news-and-data, fast-fetch, finance-models-catalogue, india-market-data-and-sebi, infrastructure, assistant-300ms-and-jev and distribution-and-competitors-india.
- **Method:** read-only.
  - Registry metadata: PyPI JSON API, crates.io API, Hugging Face `/api/models`, and GitHub REST via `gh api` (licence SPDX, `pushed_at`, latest release, LICENSE file text).
  - Official pages: read with curl plus an HTML-to-text pass, or with WebFetch.
  - Web search, used for leads only.
  - Nothing was installed, downloaded into the repo, signed up for or executed, and no repo files were edited.
- **Confidence labels:**
  - **H:** a primary page or registry was read directly.
  - **M:** a primary page was read through a summarizer, or a reputable secondary source was used.
  - **L:** a search snippet or a third-party blog.
- **Tags:** as in the India appendix.
  - **[F]:** a verified fact.
  - **[F-sec]:** a fact from a secondary source.
  - **[I]:** an inference.
  - **[P]:** a proposal.
  - **[E]:** an estimate.
- **Disclosure: NSE, BSE and AMFI access during this research.** Every request was a single read with a browser User-Agent, and was one-off. Here is exactly what was fetched:
  - **NSE:** HTTP-status probes of the ToU page and `/all-reports`. Each probe transferred the full page once, about 310 KB and 640 KB.
  - **NSE RSS:** `Online_announcements.xml` was pulled in full once during a reachability probe (about 900 KB) and then read once more as a byte range of about 2.5 KB. The ToU page was fetched once more to extract clauses.
  - **NSE pages:** the RSS index, the XBRL information page and the NSE D&A page, once each.
  - **BSE:** `notices.xml` in full once (about 15 KB) plus one ranged read. The `beta.bseindia.com` RSS page and the terms URLs, once each.
  - **AMFI:** `NAVAll.txt` in full once (about 1.5 MB, discarded) plus one ranged read. The NAV-download and terms pages, once each.
  - **Not fetched:** no bhavcopy, participant-OI or deal files, and no data file was stored.
  - This was research reading, not collection. I recommend **no further scripted access** until the counsel question in §7 is answered.

---

## 0. Bottom line

1. **Both exchanges now publish official RSS for corporate filings.** [F, H]
   - **NSE:** 23 RSS feeds on `nsearchives.nseindia.com/content/RSS/`, covering announcements, insider trading, SAST Reg 29/31, financial results, integrated filing, board meetings, corporate actions, shareholding and others. `ttl=5`.
   - **BSE:** 12 feeds under `/data/xml/`, including `announcements.xml`, `InsiderTradingFeed.xml` and `CorpActionFeed.xml`.
   - **Context:** in its June 2025 order against BSE, SEBI had pointed to RSS as the fix for paid API subscribers getting disclosures before the public.
   - **Why it matters:** this is the cheapest **official** filing-event path for India. Some NSE items link straight to **XBRL instance files**, for example `.../corporate/xbrl/REG30_Restructuring_..._WebXMLFile_....xml`.
   - **But NSE's Terms of Use still bar "any systematic or automated data collection activities (including scraping, data mining, data extraction and data harvesting)"** and any reproduction or display "without prior written permission of NSE" [F, H].
   - **Status:** whether polling an RSS feed that NSE itself publishes counts as "automated data collection" is an **open legal question**. It is not a green light. Treat it as a counsel question plus a written request to NSE and BSE (Q-O1).
2. **Every open-source Indian market-data library I checked scrapes nseindia.com or bseindia.com.**
   - This covers jugaad-data, nsepython, nselib, `nse` (NseIndiaApi), openchart, bsedata, nsetools, nsepy and `bhavcopy`.
   - Most call undocumented JSON endpoints behind a cookie-warmed session, for example `www.nseindia.com/api/...` and `charting.nseindia.com/v1/...`.
   - **All of them go to Hold for product use**, whatever their licence.
   - The official broker SDKs (`kiteconnect`, `upstox-python-sdk`, `dhanhq`, `fyers-apiv3`, `breeze-connect`, `smartapi-python`) do not scrape. They are bound by broker data terms, which in general mean per-user data and no public display (see india-market-data-and-sebi §2).
3. **The "free" official data has strings attached.**
   - **AMFI NAV:** AMFI's site ToU grants "personal and non-commercial use only". It prohibits public display and derivative works [F, H]. The free NAV file is therefore **not** cleared for a commercial app.
   - **AMFI format change:** the old-format NAV file is withdrawn **after 30 Sep 2026** [F, H]. The new `NAVAll.txt` splits Plan and Option into separate columns.
   - **FBIL benchmarks** (MIBOR, reference rates) are **fee-liable for redistributors** (M).
   - **RBI's site terms prohibit caching, and prohibit deep-linking to internal pages without prior permission** [F, H]. RBI RSS is therefore not a free-to-use event source either.
   - **MoSPI** re-based its series in 2026: CPI to 2024=100 (Feb 2026), GDP to 2022-23 (Feb 2026) and IIP to 2022-23 (May 2026). This is a **series break** that any card showing inflation or growth history must handle (M).
4. **Licence flags found in this pass:**
   - **Arize Phoenix: ELv2** [H].
   - **DragonflyDB v2.0.0: BSL 1.1**, change date 2030-11-01 to Apache-2.0, with a grant excluding in-memory-data-store services [H].
   - **Meilisearch: MIT AND BUSL-1.1** (Enterprise Edition parts) [H].
   - **`sec-edgar-mcp`: AGPL-3.0** [H]. fast-fetch listed it without a licence.
   - **Krutrim models:** a custom community licence. Commercial use needs a separate licence, and "Commercial Use" is defined by a threshold of more than 1M MAU [H].
   - **Sarvam-1: "Sarvam non-commercial license"** [H].
   - **`sarvam-translate` weights: GPL-3.0** [H].
   - **Typesense server: GPL-3.0** [H].
   - **jugaad-data:** "YOLO licence" (public-domain dedication; no OSI licence) [H].
   - **nselib:** GitHub says Apache-2.0, but PyPI has no licence field [H].
5. **Fast path: nothing here displaces the current design.** That design is a Valkey exact-key cache, a deterministic router and templates.
   - Upgrades worth noting are **Valkey 9.1** (per-database ACLs, I/O threading up to 17%, `MSETEX`, `HGETDEL`) and **cachetools 7.2 / moka-py 0.5** as an in-process L1.
   - For Indic LLMs, the news is that **Sarvam-30B and Sarvam-105B are open weights under Apache-2.0**.
     - Sarvam-30B is an MoE with **2.4B active non-embedding parameters** [H].
     - The Sarvam API lists Sarvam 105B at ₹29.28 in / ₹73.20 out per 1M tokens (M). Sarvam 30B and Sarvam-M are marked **Deprecated** in the API docs (H).
   - **Candidate:** Sarvam-30B, self-hosted in Mumbai, is the only credible India-hosted small LLM for the Hindi/Hinglish phrasing step. Its latency is **unmeasured**.
6. **MCP servers: a correction to distribution-and-competitors-india.**
   - **Groww has an official hosted MCP** at `https://mcp.groww.in/mcp`, launched 2025-08-04, and **it can place orders**: "DDPI authorisation to place sell orders" [F, H].
   - The hosted **Kite MCP** is still "read-only except GTT". The README says it "excludes potentially destructive trading operations" [H].
   - **Dhan and Angel One:** still no official MCP found (M).
   - **Financial Datasets MCP:** stale (last push 2025-06-05) [H].
7. **Evaluation and observability:**
   - **Langfuse** stays MIT-core, with commercial `ee/` directories. It was **acquired by ClickHouse (announced 2026-01-16)** and its copyright line is now "ClickHouse, Inc." [H].
   - **Phoenix** is **ELv2**. Internal self-hosting is allowed; offering it as a managed service is not.
   - **Recommendation:** self-host Langfuse in Mumbai for traces, with OpenTelemetry/OpenInference (Apache-2.0) instrumentation, and keep DeepEval in CI.

---

## 1. Official Indian sources

Columns: what it is, access, terms (software/service), data rights, scraping stance, latest observed, India coverage, price, fit (0–5), confidence.

### 1.1 NSE

| Source | What / access | Terms and data rights | Scraping | Latest observed | Price | Fit | Conf |
|---|---|---|---|---|---|---|---|
| **NSE RSS (23 feeds)** | RSS 2.0 at `nsearchives.nseindia.com/content/RSS/*.xml`. Feeds: Online_announcements, InsiderTrading, Sast_Regulation29/31, Sast_ReasonForEncumbrance, Financial_Results, Integrated_Filing_Financials, Board_Meetings, Corporate_action, Shareholding_Pattern, Voting_Results, Related_Party_Trans, Offer_Documents, Annual_Reports, Circulars, brsr, Daily_Buyback, Corporate_Governance, Secretarial_Compliance, Statement_Of_Deviation, Share_Transfers, Investor_Complaints, Unitholding_Patterns. `ttl` 5 min. Items: company name, PDF or **XBRL** link, subject, `pubDate` | ToU: no copying, reproducing, storing, displaying or redistributing "without prior written permission of NSE". Content is NSE-owned or NSE-licensed | **ToU prohibits "systematic or automated data collection"** on the Website. Whether RSS polling falls under it is **unresolved** | Feed `lastBuildDate` Thu 24 Sep 2026 22:13 +0530 | $0 to read. Display rights: written permission needed | 4 if permitted; 1 until then | H |
| NSE RSS timestamp format | `pubDate` is **`24-Sep-2026 22:12:05` with no timezone** (IST implied), and it is not RFC-822 | [I] It must be parsed as Asia/Kolkata and stored as UTC plus our own `ingest_ts` (invariant 1). It is the exchange **dissemination** time, not the company's submission time | — | — | — | — | H |
| **NSE XBRL taxonomies (LODR)** | Downloadable taxonomy ZIPs on `/static/companies-listing/xbrl-information`. Coverage now goes well beyond results: Reg 30 event types (board-meeting outcome, orders/contracts, agreements, restructuring, CIRP, forensic audit, change in management, auditor/director resignation), SHP (2025-10-31), PIT (2026-06), Integrated Filing Finance (Ind AS/Banking/NBFC/Insurance, 2026-07/08), BRSR (2026-03) | Taxonomy files are published for filers. Terms of reuse are not stated (unverified) | Download of published files; same ToU caveat | Newest ZIPs dated 2026-09-03 (SHP, Reconciliation of Share Capital) | $0 | **5** as a schema for parsing (structured Reg 30 events mean no PDF LLM extraction) | H |
| **Bhavcopy (CM UDiFF)** | Daily EOD file `BhavCopy_NSE_CM_0_0_0_YYYYMMDD_F_0000.csv.zip`. The old format was discontinued 2024-07-08 (NSE circular 62424, 2024-06-12) | Same ToU. NSE D&A sells EOD and historical data under licence | Scripted download = automated collection (ToU) | — | $0 on the site; licensed via NSE D&A (quote) | 3 (gold-fixture reference only, internal) | M (circular via secondary source; filename from search result) |
| **F&O participant-wise OI** | Daily after close (secondary sources say ~19:00 IST). Split into Client / DII / FII / Pro, long and short, for index/stock futures and options. Archive path seen in nsepython: `archives.nseindia.com/content/nsccl/fao_participant_oi_*` | Same ToU | Same | — | $0 / licensed | 3 (EOD context card: "FII net short index futures") | M |
| **FII/DII trading activity** | `nseindia.com/reports/fii-dii`: cash-market provisional figures for NSE, BSE and MSEI | Same ToU | Same | — | $0 / licensed | 3 | M |
| **NSE Data & Analytics products** | Categories: streaming (L1/L2/L3/TBT), snapshot, **EOD**, **historical**, **Corporate Data**, Fixed Income Valuations. Page "Updated on: 24/04/2026". Contact marketdata@nse.co.in | Licensed. The licensed route for announcements, bulk/block deals and EOD data (Q22 in global-news) | n/a (licensed feed) | — | Quote; tariffs in india-market-data-and-sebi §1.3 | **5** (the lawful product path) | H (page) / M (fees) |
| Bulk/block deal files | Covered in global-news §6 and india-market-data. Libraries hit `archives.nseindia.com/content/equities/bulk.csv`, `block.csv` and `www.nseindia.com/api/historicalOR/bulk-block-short-deals` | Delta: none | ToU | — | — | — | — |

### 1.2 BSE

| Source | What / access | Terms / data rights | Scraping | Latest | Price | Fit | Conf |
|---|---|---|---|---|---|---|---|
| **BSE RSS (12 feeds)** | `/data/xml/announcements.xml`, `notices.xml`, `sensexrss.xml`, `/Data/XML/InsiderTradingFeed.xml`, `FinancialResultsFeed.xml`, `BoardMeetingsFeed.xml`, `ShareholdingPattern_Feed.xml`, `AnnualReportFeed.xml`, `MediaRelease_Feed.xml`, `IndexMediaRelease_Feed.xml`, `/data/XML/CorpActionFeed.xml`, `VotingResultFeed.xml`. The page describes them as "real time updates" for feed readers | `<copyright>Copyright 2010, BSE.</copyright>` in the feed. **BSE ToU is unreadable**: `www.bseindia.com/termsofuse.html` returns 403 or a 158-byte block to WebFetch and to curl, and the `beta.` host returns a "page moved" 404. It is unverified | Unverified. Assume it is restricted like NSE until read | `notices.xml` item 2026-09-24 16:28:41 GMT (RFC-822 with timezone) | $0 to read | 4 if permitted | H (feed list via beta.bseindia.com page and feed header) / L (terms) |
| **SEBI order in the matter of BSE**, No. QJA/SS/MRD/MRD-SEC-1/31485/2025-26, **dated 2025-06-25** | **Inspection period:** Feb 2021 – Sep 2022. **SCN:** 2024-09-23, alleging that before 2023-09-13 BSE's architecture let paid clients and LCM receive announcements before website viewers, "due to lack of RSS feed". **SEBI sample findings:** in **6 of 100** instances paid subscribers received data before replication to the website DBs; in **47 of 100**, before the latest DB2A/2B timestamp. **Held:** a violation of SECC Reg 39(3) (equal, fair access). **Penalty:** ₹15 lakh for Reg 39(3), plus ₹10 lakh on unrelated circular violations | [I] **Paid exchange API feeds historically led the public web.** Measure official RSS latency against the NSE D&A / BSE paid feed before claiming "fast". BSE's RSS feeds now exist, which fits the SCN's criticism | — | Order PDF read in full text | — | — | **H** |

### 1.3 Regulators and government

| Source | Access | Terms / data rights | Scraping stance | Latest observed | India cov. | Fit | Conf |
|---|---|---|---|---|---|---|---|
| **SEBI RSS** `sebi.gov.in/sebirss.xml` | RSS, `ttl` 60. Items: orders, circulars, press releases, board-meeting decisions | Copyright/terms pages at the obvious URLs return 404, so this is **unverified**. Factual regulatory releases are low risk to link and summarise (L) | None found | `lastBuildDate` 24 Sep 2026 22:00:02. **Item `pubDate` has the date only** ("24 Sep, 2026 +0530"), so our `ingest_ts` is the only intraday time | Regulator | 4 (regulatory-event cards; SEBI orders on listed names) | H (feed) / L (terms) |
| **RBI RSS** (`rbi.org.in/Scripts/rss.aspx`) | 7 feeds: press releases, notifications, speeches, publications, bulletin, annual report, tenders | **RBI Disclaimer (`/Scripts/Disclaimer.aspx`), read in full:** "caching and links to, and the framing of this Web Site or any of the contents are **prohibited**", except as follows. Linking to the **home page** is allowed "upon notifying RBI in writing". Hyper-linking to an **internal page** requires that the user "secure permission from RBI prior to hyper-linking". RBI may block any IP | RSS is offered, but storing (caching) items and deep-linking to them are restricted | Site "last updated Sep 24, 2026" | Central bank | **2 until permission** (then 4) | H |
| **RBI DBIE** | Web portal, Excel/CSV downloads. **Still no official public API found** (M) | See global-news §5 | — | — | Macro, banking, FX | 3 | M |
| DBIE mirror "dbie.rbihub.in" (GitHub org `Reserve-Bank-Innovation-Hub`) | Static site plus MCP. Its own README says it **scrapes** 252 DBIE SDMX series. MIT | **Provenance unconfirmed**: the org is not verified, was created 2025-08, has 3 repos, the repo has 0 stars, and rbihub.in does not link to it. **Treat as a possible impersonation or unofficial mirror** | Scraper | Pushed 2026-09-23 | — | 1 | L (provenance) |
| **MCA21 V3** | Company/LLP master data on the V3 portal (a human web app). **No public documented MCA API** (secondary). The official machine route is the OGD extract on data.gov.in. Commercial "MCA APIs" (Sandbox, Surepass, etc.) are intermediaries | MCA terms not read (the site returned 403 to curl) | Portal access may need login and fees | — | All companies (CIN, charges, directors) | 2 (company master and aliases for symbol resolution, via OGD) | M |
| **data.gov.in (OGD) API** | REST with a free API key; heavily rate-limited (numbers not published in what I read) | **GODL-India**: worldwide, royalty-free, commercial use and derivatives allowed; attribution required | Permitted via API | — | Many datasets (varies) | 3 | M |
| **MoSPI: eSankhyiki / api.mospi.gov.in** | Swagger UI at `api.mospi.gov.in`. The portal publishes `llms.txt` and `.well-known/ard.json` (agent discovery) listing NAS, CPI, IIP, PLFS, ASI, HCES and others. eSankhyiki MCP (MIT) **v2.2.0 released 2026-04-30**, pushed 2026-09-23 | GODL (global-news §5). **Delta: 2026 re-basing**: CPI 2024=100 (first release 2026-02-12), GDP base 2022-23 (2026-02-27), IIP base 2022-23 (May 2026) | Official API | See left | Official macro | 4 (CPI/IIP/GDP release cards) | H (api, llms.txt, MCP release) / M (re-basing dates) |
| **PIB RSS** | `pib.gov.in/RssMain.aspx` redirects to `?reg=48&lang=2`. Per-region and per-language `ViewRss.aspx?reg=&lang=` | PIB copyright policy allows free reproduction with acknowledgement (global-news §2) | Permitted by policy | — | Govt press releases, Hindi and English | 3 | M |
| **NSDL FPI Monitor** (`fpi.nsdl.co.in`) | Web reports: daily trends (Excel export), fortnightly sector-wise, monthly, yearly. **New: daily DII reporting announced 2026-06-01** (MFs, AIFs, banks, insurers), aligned with the FPI framework | Terms and conditions page exists but was **not read**: both the `/web/Reports/` and `/Reports/` URLs timed out twice | Unverified | — | FPI and DII flows | 3 | M |
| CDSL FPI data | Not found in this pass | — | — | — | — | — | unverified |
| **AMFI NAV** (`portal.amfiindia.com/spages/NAVAll.txt`) | Semicolon-delimited text: Scheme Code; ISIN payout/growth; ISIN reinvest; Scheme Name; **Plan; Option**; NAV; Date. History max 90 days per query. **Old format (`Original_NAVAll.txt`) is available "only till 30th September 2026"** | **AMFI ToU: licence "for your personal and non-commercial use only"; "You may not publicly perform, publicly display, transmit, publish... or create derivative works"** | Automated retrieval not addressed, but commercial use is excluded | File date 23-Sep-2026 | All MF schemes | 2 until AMFI grants permission (then 4) | H |
| **FBIL / CCIL** | FBIL publishes benchmarks (MIBOR, MIFOR, FX reference rates, G-sec valuations); CCIL hosts some pages | **Fee-liable**. Data-vendor licence e.g. MIBOR ₹1,00,000/month; under 1,000 terminals ₹5,00,000/yr per benchmark (2018 FAQ). FBIL Reference Rate fee-liable from 2019-04-01 | Licence required for redistribution | Fee docs from 2018/2023 | Rates | 1 (not core) | M |

### 1.4 XBRL for Indian filings

| Taxonomy | Owner | Use | Conf |
|---|---|---|---|
| **LODR taxonomies** (NSE page; BSE publishes equivalents) | Exchanges, under SEBI LODR | Parse Reg 30 announcements, results, SHP, PIT and integrated filings into typed events. The RSS item links to the instance XML | H (NSE list) |
| **MCA Ind AS / C&I taxonomy** (`mca.gov.in/XBRL/`) | MCA | AOC-4 XBRL annual financials (T+30 days after AGM), so it is slow and useful only for fundamentals backfill | M |
| NSE `Taxonomy_Archives_20260731` | NSE | Older versions, for point-in-time parsing of historical filings | H (link exists) |

---

## 2. Open-source libraries for Indian market data

Every row was checked for the domains the source code calls, using raw source from GitHub. "Scrapes" means it calls nseindia.com or bseindia.com web or undocumented JSON endpoints.

| Package (PyPI) | Latest (PyPI upload) | First release | Code licence | Maintained? | What it calls | Scrapes? | Lookalike / provenance notes | Fit | Conf |
|---|---|---|---|---|---|---|---|---|---|
| `jugaad-data` | 0.35.9 (2026-09-23) | 2020-08-20 | **"YOLO licence"**: public-domain dedication in `LICENSE.YOLO.md`; no SPDX; GitHub licence null | Active (repo `jugaad-py/jugaad-data`, 579★) | `www.nseindia.com/api/...`, `NextApi/apiClient/GetQuoteApi`, `report-detail/eq_security`, niftyindices.com, rbi.org.in | **Yes** | PyPI author email is the placeholder `abc@xyz.com`; homepage marketsetup.in. Same author as `jugaad_trader` (0.20, 2025-12-19) | 0 (product) / 1 (research) | H |
| `nsepython` | 2.97 (2025-05-26) | 2020-06-22 | GPL-3.0 (GitHub). PyPI says "GNU" | Moderate (pushed 2026-03-07; no release for 16 months) | `archives.nseindia.com` bulk.csv, block.csv, `fao_participant_oi_`, `sec_bhavdata_full_`, plus www API | **Yes** | — | 0 | H |
| `nselib` | 2.5.1 (2026-05-01) | 2023-06-19 | Apache-2.0 on GitHub; **no licence in PyPI metadata** | Active (pushed 2026-07-18) | `www.nseindia.com/api/historicalOR/*`, `corporates-financial-results`, `holiday-master`, and **`nsewebsite-staging.nseindia.com`** | **Yes** (including a staging host) | — | 0 | H |
| `nse` (NseIndiaApi) | 4.0.1 (2026-08-31) | 2023-10-17 | GPL-3.0 | Active | `www.nseindia.com/api`, `nsearchives.nseindia.com` bhavcopy | **Yes** | Very generic name `nse`. Confirm the author is BennyThadikaran before any use | 0 | H |
| `openchart` | 0.2.0 (2026-01-16) | 2024-10-20 | MIT (LICENSE file; GitHub API shows NOASSERTION) | Low | `charting.nseindia.com/v1/charts/symbolHistoricalData` and `symbolsDynamic`, after warming `www.nseindia.com` cookies | **Yes** | Author Rajandran R (marketcalls) | 0 | H |
| `bsedata` | 0.6.0 (2024-03-14) | 2018-06-26 | MIT | Stale (no release for 2.5 years) | `m.bseindia.com/StockReach.aspx`, BSE BhavCopy download page, and **an r2.dev bucket `stk.json`** of unknown ownership | **Yes** (plus a third-party bucket) | The r2.dev dependency is an integrity risk | 0 | H |
| `nsetools` | 2.0.1 (2025-03-18) | 2015-01-02 | MIT | Low | NSE site (per its docs; not re-grepped) | Yes (M) | — | 0 | M |
| `nsepy` | 0.8 (2020-03-07) | 2015 | none on PyPI | **Dead** | Old NSE endpoints | Yes | — | 0 | H |
| `bhavcopy` | 3.0 (2023-07-29) | 2023-07-29 | MIT | Single release | "Download NSE Bhavcopy Data" | Yes | **No homepage or repo; personal gmail author. Provenance unverifiable, so do not use** | 0 | H |
| `nsefin` | 0.1.5 (2025-09-08) | 2025-07-09 | MIT | New, small | NSE (per name; not grepped) | Likely | — | 0 | L |
| **`kiteconnect`** (official Zerodha; GitHub repo `zerodha/pykiteconnect`) | **5.2.2 (2026-09-15)** | 2016-01-27 | MIT | Active (1,310★) | Kite Connect API (licensed broker API) | **No** | **`pykiteconnect` does not exist on PyPI (404)**. If it ever appears, treat it as a squat | 2 (per-user BYO only; Kite terms bar public display) | H |
| `upstox-python-sdk` | 2.30.0 (2026-09-07) | 2023-07-07 | MIT | Active | Upstox API | No | Official (github.com/upstox) | 2 | H |
| `dhanhq` | 2.2.0 (2026-04-24) | 2022-09-01 | MIT | Active | DhanHQ API | No | Official (dhanhq.co) | 2 | H |
| `fyers-apiv3` | 3.1.18 (2026-09-17) | 2023-08-18 | MIT | Active | Fyers API | No | Official (FyersDev) | 2 | H |
| `breeze-connect` | 1.0.69 (2026-04-14) | 2021-12-20 | MIT | Active | ICICI Breeze | No | Official (Idirect-Tech) | 2 | H |
| `smartapi-python` | 1.5.5 (2025-02-07) | 2020-10-28 | none on PyPI | Low (no release for 19 months) | Angel One SmartAPI | No | **Lookalike: `smartapi` (1.1.0, 2017, Asema Electronics) is unrelated. Never `pip install smartapi`** | 2 | H |

**Table defaults (§2):**
- **Price:** $0 (open source).
- **India coverage:** NSE and/or BSE by design.
- **Data rights:** these are **separate from the code licence**.
  - For the scrapers there are **no data rights at all**: the data belongs to NSE/BSE under their ToU, whatever the MIT/GPL/YOLO code licence says.
  - For the broker SDKs, data rights are the broker's API terms: per-user data, no public display (Kite: see india-market-data-and-sebi §2).
- **Broker API prices** (from the India appendix, not re-verified):
  - Kite Connect ₹500/mo;
  - Dhan Data API ₹499/mo;
  - Upstox, Fyers, Breeze and SmartAPI stated as free.

[I] No open-source Indian library gives lawful, display-grade exchange data. The lawful routes are:
- NSE D&A or an authorised vendor for the product;
- broker SDKs for per-user, bring-your-own-account data only;
- official RSS, pending permission.

---

## 3. Fast-path infrastructure (answer p95 300 ms, Mumbai)

### 3.1 Key-value / cache servers

| Item | Latest (registry) | Code licence | Maintenance | What's new / relevant | Price | India | Fit | Conf |
|---|---|---|---|---|---|---|---|---|
| **Valkey** | 9.1.2 and 9.0.6 (2026-09-01); 9.1.0 on 2026-05-19; 9.0.0 on 2025-10-21 | BSD-3-Clause | Very active (27k★) | **9.0:** hash-field expiration (HEXPIRE, HPERSIST), atomic slot migration, numbered DBs in cluster mode. Throughput claims: "up to 40%" (pipeline prefetch), "up to 20%" (zero-copy), MPTCP "25%" latency. **No methodology on the blog.** **9.1:** redesigned I/O threading "up to 17%", up to 20% less memory for strings under 128 B, **database-level ACLs**, TLS cert auto-reload, `MSETEX`, `HGETDEL`, `CLUSTERSCAN`. valkey-bundle ships JSON, Bloom, Search 1.2 and LDAP | $0 self-host; ElastiCache supports 9.1 (2026-06) | Self-host in Mumbai (ElastiCache in ap-south-1 not re-verified) | 5 | H (releases) / M (feature blog via summarizer) |
| Valkey clients | `valkey` (valkey-py) 6.1.1 (2025-08-11, MIT); **`valkey-glide` 2.5.2 (2026-09-02, Apache-2.0)** | — | valkey-py: no release for 13 months; GLIDE active | GLIDE has a Rust core with Python bindings and is the maintained official client. redis-py also works | $0 | — | 4 | H |
| **DragonflyDB** | **v2.0.0 (2026-09-16)** | **BSL 1.1 (flag).** Change Date 2030-11-01 to Apache-2.0. Additional Use Grant allows use "only as part of your own product or service, provided it is not an in-memory data store product or service" | Active (31.6k★) | v2.0 adds Valkey 9 RDB loading and memory and parsing cuts. No new major feature | $0 self-host under the grant | — | 2 (allowed for us under the grant, but brings no benefit over Valkey at our scale) | H |
| Redis 8 server | 8.10.2 (2026-09-17) | RSALv2 / SSPLv1 / AGPLv3 (flag) | — | **Delta only.** Covered in assistant-300ms and infrastructure. redis-py 8.1.0 (MIT) is unchanged | — | — | — | H |

### 3.2 Embedded (in-process L1) caches

| Package | Latest | Licence | Maintenance | Notes | Fit | Conf |
|---|---|---|---|---|---|---|
| **cachetools** | 7.2.0 (2026-09-16), Py ≥ 3.10 | MIT | Active | TTLCache/LRUCache, pure Python. Needs a lock around shared access under asyncio or threads | **5** (L1 for symbol dictionary and hot cards) | H |
| **moka-py** | 0.5.0 (2026-08-21), Py ≥ 3.10 | MIT | Active (311★) | Python binding over the Rust `moka` (0.12.16, 2026-08-09, `(MIT OR Apache-2.0) AND Apache-2.0`). TinyLFU admission, per-entry TTL. **Published by a third party (`deliro`), not by the moka-rs authors.** It is not a typosquat, but it is not first-party | 3 | H |
| cashews | 7.6.0 (2026-09-17) | MIT | Active | Async cache decorators with memory or Redis backends, plus early-refresh and stampede locks | 3 | H |
| aiocache | 0.12.3 (**2024-09-25**) | BSD-3 (GitHub) | **No release for 2 years** (repo pushed 2026-06) | — | 1 (Hold) | H |

**Table defaults (§3.2):** price $0; runs in-process anywhere, including Mumbai; no data rights involved (no data shipped).

### 3.3 Symbol and fuzzy matching, and Indic transliteration

| Package | Latest | Licence | Maintenance | Relevance | Fit | Conf |
|---|---|---|---|---|---|---|
| rapidfuzz | 3.14.6 (2026-08-30), **Py ≥ 3.11** | MIT | Active | Already in the design (assistant-300ms). Note the Python floor is 3.11, which is fine for 3.12 | 5 | H |
| symspellpy | 6.10.0 (2026-07-11) | MIT | Active | Spelling correction for typos in company names. **`symspell` on PyPI is a 404: always use `symspellpy`** | 3 | H |
| tantivy (py) | 0.26.2 (2026-09-17). Crate 0.26.2 (2026-09-08) | MIT | Active (16k★ core) | Embedded BM25 index, if the alias dictionary exceeds what rapidfuzz handles | 2 | H |
| Typesense | server v30.2 (2026-04-19); `typesense` client 2.0.0 (2026-02-16) | **Server GPL-3.0** (not AGPL, so network use does not trigger copyleft); client Apache-2.0 | Active | Typo-tolerant search server. Adds a network hop, which is overkill for about 10k symbols | 2 | H |
| Meilisearch | v1.54.0 (2026-09-21); `meilisearch` 0.43.0 (MIT) | **`MIT AND BUSL-1.1`**: Enterprise Edition parts are BUSL (flag) | Active | Same as above. Watch which features are EE | 2 | H |
| **indic-transliteration** | 2.3.82 (2026-04-06) | MIT | Active, long-lived | Rule-based script conversion (Devanagari ↔ ITRANS/IAST/…). Deterministic, so it suits alias generation, but it is **not** a Hinglish phonetic model | 3 | H |
| **AI4Bharat IndicXlit** | PyPI `ai4bharat-transliteration` 1.1.3 (**2022-09-14**); GitHub MIT, last push 2023-10; HF model card MIT (modified 2025-03) | MIT (code and model) | **Stale package** | Romanised → native-script neural transliteration ("reliance" → "रिलायंस"). Use **offline** to pre-generate Hindi and Hinglish aliases for the symbol dictionary, not per request | 3 | H |
| **IndicTrans2** | HF `indictrans2-en-indic-1B` / `-indic-en-dist-200M`: **MIT**, HF-gated ("auto"), modified 2025-05. Toolkit `IndicTransToolkit` 1.1.1 (2025-07-23, MIT, VarunGumma, which is the upstream-designated maintainer) | MIT (code and weights) | Maintained via toolkit | Offline translation of **card templates** into Hindi and other languages, reviewed by a human. **PyPI `indictrans2` 0.1.3 (2024-05) uses a gmail author and is not referenced by the upstream README, so treat its provenance as unverified and prefer the toolkit** | 3 | H |
| AI4Bharat IndicBERT-v3 (270M / 1B / 4B) | HF, 2026-06-12 | MIT | New | Hindi and Indic encoder for internal tagging. Complements the radar's "own English + Hindi finance encoder" | 3 | H |

**Table defaults (§3.3):**
- **Price:** $0 self-host. Typesense Cloud and Meilisearch Cloud prices and regions were not checked.
- **India:**
  - IndicXlit, IndicTrans2, indic-transliteration and IndicBERT-v3 are **built for Indian languages**. IndicTrans2 covers 22 scheduled languages.
  - rapidfuzz, symspellpy and tantivy are language-agnostic.
- **Data rights:** only model weights are shipped, not market data. **Training-data provenance** for the AI4Bharat models is documented in their papers, which I did not re-read.

### 3.4 Small and Indic LLMs

| Model / API | Latest | Weights / code licence | Relevance | Price | India hosting / latency | Fit | Conf |
|---|---|---|---|---|---|---|---|
| **Sarvam-30B** (open weights) | HF 2026-03-23 (FP8 and GGUF variants) | **Apache-2.0** | MoE, **2.4B active non-embedding params**, 22 Indian languages, 65k context in evals. Self-host candidate for the Hindi/Hinglish **phrasing** step only (numbers come from code, invariant 5) | Self-host GPU cost | Can be self-hosted in Mumbai. **Latency not measured** | **4** | H |
| **Sarvam-105B** (open weights and API) | HF 2026-09-21 | **Apache-2.0** | Too large for the 300 ms path; possible background narrative | API **₹29.28 in / ₹10.98 cached / ₹73.20 out per 1M tokens** | Vendor says it is trained and hosted in India. The secondary source's "<200 ms" claim is for voice, is **unverified** and comes with no methodology | 2 | H (weights) / M (price) / L (latency) |
| Sarvam API: Sarvam 30B, Sarvam-M | Docs mark both **"Deprecated"** | — | Do not build on them | — | — | 1 | H |
| Sarvam translate / transliterate API | — | `sarvam-translate` weights **GPL-3.0** (flag, if self-hosted and redistributed) | Hindi card localisation | ₹0.005 per character (PAYG), falling to ₹0.004 (Business) | India | 3 | M |
| `sarvamai` Python SDK | 0.1.34 (2026-09-18) | **No licence in PyPI metadata; the repo link `sarvamai/sarvam-python-sdk` returns 404 (private or moved)** | The org `sarvamai` is genuine (blog sarvam.ai) | — | — | 2 | H (metadata) |
| Sarvam-1 (2B) | HF 2024-11 | **"Sarvam non-commercial license"** | Not usable commercially | — | — | 0 | H |
| Sarvam-M | HF 2025-05 | Apache-2.0 | Superseded by 30B | — | — | 1 | H |
| **Krutrim** (Krutrim-1/2-instruct, Vyakyarth, Chitrarth, …) | HF up to 2026-03 | **Krutrim Community License v1.0.** Commercial use needs a separate licence. The definition ties "Commercial Use" to Licensees with "more than 1 million monthly active users", while s.2 also frames the grant around research and personal use. The wording is ambiguous | Hold unless there is a written licence | — | Ola (India) | 0 | H |
| AI4Bharat models | See §3.3 | MIT / CC-BY-4.0 (IndicConformer) | Encoders, translation, ASR | $0 | Self-host | 3 | H |
| **Krutrim Cloud (API)** | — | Service terms not read | Hosts third-party open models plus Krutrim's own models | INR pricing, reported as e.g. Llama-4-Scout ₹7/1M tokens, Gemma-3-27B ₹8/1M, DeepSeek-R1 ₹11/1M, "Spectre-V2" ₹16.60/1M | Vendor states **data stored in Indian data centres**. No latency figure found | 2 | L (third-party pricing summary; primary `docs.cloud.olakrutrim.com/basics/pricing` not read) |

**Notes on §3.4:**
- **Sarvam API account terms (H):**
  - ₹100 free signup credits that never expire.
  - Per-account token-bucket rate limits by plan (Starter, Pro, Business). The **LLM-specific limits were not captured**.
  - The "Commercial Licensing" page covers **audio/TTS Output rights only**. It "does not grant rights to Sarvam's models".
- **Sarvam data residency:** the vendor's India-hosting statement was found **only in secondary sources**. The docs index (`llms.txt`) does not state a hosting region, and `llms-full.txt` returned an empty body.
- **Weights data rights:** the Sarvam-30B and 105B model cards do not disclose training-data provenance in the lines I read, so treat provenance as **undisclosed**.

### 3.5 Structured generation (only if we self-host an LLM)

| Package | Latest | Licence | Notes | Fit | Conf |
|---|---|---|---|---|---|
| outlines | 1.3.3 (2026-08-06) | Apache-2.0 | **`requires_python <3.14`**, so it does not support Python 3.14 yet | 2 | H |
| xgrammar | 0.2.7 (2026-09-15) | Apache-2.0 | Grammar engine used by vLLM and SGLang. Relevant only if we serve Sarvam-30B ourselves | 3 (conditional) | H |
| llguidance | 1.8.0 (2026-08-11) | MIT (Microsoft) | Alternative engine | 2 | H |
| lm-format-enforcer | 0.11.3 (2025-08-24) | MIT | Slowing | 1 | H |
| instructor | 1.17.0 (2026-09-09) | MIT | **Delta only** (infrastructure §12). Repo moved to `567-labs/instructor` | — | H |

---

**Table defaults (§3.5):** price $0; self-host anywhere; no data rights involved. These tools matter only if we self-host an LLM in Mumbai.

## 4. Finance MCP servers and agent tools

**Table defaults (§4):**
- **Code licence** is as listed per row.
- **Data rights are the vendor's or broker's own data terms, not the MCP code licence.**
  - Broker MCPs serve the user's own account data under the broker's terms (no public display).
  - Vendor MCPs (Alpha Vantage, Massive, Financial Datasets) inherit that vendor's plan terms (see global-news §2/§4).
- **Price:** the MCP itself is free. You pay for the underlying API plan. The Groww MCP needs a Claude Pro subscription (for the connector) plus a Groww account.
- **India:** Kite, Groww and Upstox are India-only. Alpha Vantage, Massive and Financial Datasets are US-centric. Alpha Vantage's India coverage (BSE symbols) was not re-checked.

| Server | Owner | Latest | Licence | Read-only? | Data rights / notes | Fit | Conf |
|---|---|---|---|---|---|---|---|
| Kite MCP (hosted `mcp.kite.trade/mcp`) | Zerodha (official) | Release v0.3.2 (2026-07-10); pre-releases v0.4.0-dev17 (2026-09-10) | MIT | **Hosted: no place/modify/cancel** ("excludes potentially destructive trading operations"). **GTT tools present, so it is not strictly read-only.** Self-hosted exposes `place_order` etc. unless `EXCLUDED_TOOLS` is set | Per-user. **Delta only**: the scope is unchanged from india-market-data-and-sebi §2 | 2 (companion, not backend) | H |
| **Groww MCP** (`mcp.groww.in/mcp`) | **Groww (official)** | Launched 2025-08-04 | Hosted, proprietary | **No: can place orders**; "DDPI authorisation to place sell orders" | Stocks and F&O only; "early-stage"; Claude Pro connector or `mcp-remote`. **Corrects distribution-and-competitors-india**, which said there was no official Groww MCP | 1 (companion only; write tools) | H |
| Upstox MCP | Upstox (official) | — | Hosted | Read-only (per distribution appendix) | Delta: none re-verified | 2 | M |
| Dhan / Angel One | — | — | — | — | **No official MCP found.** Community servers exist, some with order tools (e.g. `vikkysarswat/dhan-mcp-server`). A MadeForTrade thread is a *proposal* for an official Dhan MCP | 0 | M |
| finstack-mcp | Community (PyPI 0.10.0, 2026-04-09) | — | MIT | Data | **Default data source is yfinance** (conflicts with invariant 7) | 0 | H |
| Financial Datasets MCP | financial-datasets (official) | No releases; **last push 2025-06-05** | MIT | Read (data) | US fundamentals. **Stale** | 1 | H |
| Alpha Vantage MCP (`alphavantage/alpha_vantage_mcp`, hosted `mcp.alphavantage.co`) | Alpha Vantage (official) | Pushed 2026-09-21; no GitHub releases | MIT | Read (data) | AV data terms apply. No `alpha-vantage-mcp` on PyPI (404) | 2 | H |
| Massive MCP (`massive-com/mcp_massive`) | Massive (official) | v0.10.0 (2026-05-05) | MIT | Read (data) | **Delta only** (fast-fetch §6) | 2 (US leg research) | H |
| `sec-edgar-mcp` | Community (Stefano Amorelli) | 1.1.0 (2026-08-20) | **AGPL-3.0 (flag)** | Read | Research use only; Hold in product | 1 | H |

---

## 5. Evaluation and observability

| Tool | Latest | Licence | Maintenance / ownership | Relevance | Fit | Conf |
|---|---|---|---|---|---|---|
| **Langfuse** | Server v4.45.1 (2026-09-24); `langfuse` SDK 4.15.6 (2026-09-24) | **MIT core; `ee/`, `web/src/ee/` and `worker/src/ee/` fall under `ee/LICENSE` (commercial)** | **Acquired by ClickHouse, Inc. (announced 2026-01-16).** LICENSE copyright line is now "ClickHouse, Inc."; vendor states no licence change planned | Self-host in Mumbai: traces, prompt versions, eval scores per answer card, with OTel ingestion | **4** | H (licence, versions) / M (acquisition, via vendor blog) |
| **Arize Phoenix** | `arize-phoenix` 20.16.0 (2026-09-23) | **Elastic License 2.0 (flag)**: no providing as a hosted or managed service; no circumventing licence keys | Very active | Internal self-host is allowed. `arize-phoenix-otel` 0.17.1 and `openinference-instrumentation` 0.1.66 are **Apache-2.0** | 3 | H |
| `phoenix` (PyPI) | 0.9.1 (**2013**) | "UNKNOWN" | Unrelated | **Name collision: always install `arize-phoenix`** | — | H |
| OpenInference instrumentation | 0.1.66 (2026-09-24) | Apache-2.0 | Active | Vendor-neutral OTel semantic conventions for LLM spans. Works with Langfuse or Phoenix | 4 | H |
| DeepEval | 4.2.6 (2026-09-24) | Apache-2.0 | **Delta only** (infrastructure §12) | — | — | H |
| Ragas | 0.4.3 (2026-01-13); repo pushed 2026-02-24 | Apache-2.0 | **Delta: still no activity since February**, so it is slowing | — | — | H |
| promptfoo | GitHub 0.123.1 (2026-09-18); PyPI 0.2.0 is a wrapper | MIT | **Delta only** (OpenAI-owned since 2026-03) | — | — | H |
| inspect-ai | 0.3.268 (2026-09-22) | MIT | Delta only | — | — | H |

**Table defaults (§5):**
- **Price:** $0 self-host.
- **Data rights:** these tools store **our users' queries and answers** (traces). That is personal data, so hosting location matters.
- **Langfuse Cloud regions (H):**
  - US: Oregon, us-west-2.
  - EU: Ireland, eu-west-1.
  - Japan: Tokyo, ap-northeast-1.
  - HIPAA: Oregon.
  - **There is no India region.** The page also says it runs on AWS "partly managed by Clickhouse".
- **Langfuse Cloud pricing (M, secondary):**
  - Hobby: free, 50k units/mo.
  - Core: 100k units/mo.
  - Pro: $199/mo.
  - Overage: $8 per 100k units.
- **Arize AX (hosted Phoenix):** pricing and regions were not checked.
- **[P] Self-host Langfuse or Phoenix in Mumbai**, so that user traces stay in India. This fits the DPDP Act posture; that is an inference, and a compliance-analyst item.

---

## 6. Proposed radar ring changes (the radar itself is not edited)

| Radar row (existing) | Item | From → To | Reason |
|---|---|---|---|
| Filings / news | **NSE RSS (23 feeds) + BSE RSS (12 feeds)** | new → **Assess** (internal evaluation only; **not Trial** until Q-O1 is answered in writing) | These are official exchange feeds that link to XBRL instances. NSE ToU bans automated collection and any display without permission |
| Filings / news | **NSE/BSE LODR XBRL taxonomies** as the parsing schema for Reg 30 events | new → **Trial** (schema and parser against recorded fixtures) | Structured announcement events instead of PDF extraction. Test fixtures need no live access |
| Filings / news | **NSE Data & Analytics "Corporate Data" / EOD** | new → **Assess** (quote Q22) | The lawful product route for announcements and EOD data |
| Filings / news | **SEBI RSS, PIB RSS** | new → **Trial** | Regulator and government feeds. PIB reproduction is allowed with acknowledgement. SEBI terms were not found (link-out only until then). Note SEBI's day-only `pubDate` |
| Filings / news | **RBI RSS** | new → **Assess** (pending permission Q-O5) | The RBI Disclaimer prohibits caching, and prohibits deep-linking without prior permission |
| Market-data clients | **Unofficial NSE/BSE libraries**: jugaad-data, nsepython, nselib, `nse`, openchart, bsedata, nsetools, nsepy, `bhavcopy`, nsefin | new → **Hold** | All of them scrape exchange sites (ToU). Some add a staging host or a third-party bucket. `bhavcopy` has no provenance |
| Market-data clients | Broker SDKs `kiteconnect`, `upstox-python-sdk`, `dhanhq`, `fyers-apiv3`, `breeze-connect`, `smartapi-python` | new → **Assess** (per-user BYO only) | Official and non-scraping, but broker terms bar public display. Also add the PyPI look-alike **`smartapi`** to Hold |
| *Macro / official releases (proposed new row)* | **MoSPI API / eSankhyiki MCP v2.2.0** | new → **Trial** | Official API under GODL. **Handle the 2026 base-year breaks** |
| *Macro / official releases (proposed new row)* | **AMFI NAVAll.txt** | new → **Hold** (product) | ToU is personal and non-commercial. The format change on 2026-09-30 breaks parsers |
| *Macro / official releases (proposed new row)* | FBIL benchmarks | new → **Hold** | Fee-liable for redistribution |
| *Macro / official releases (proposed new row)* | `dbie.rbihub.in` / `Reserve-Bank-Innovation-Hub` GitHub | new → **Hold** | Unconfirmed provenance, and it is itself a scraper |
| Assistant answer path | Valkey | Adopt (unchanged) → **Adopt, pin ≥ 9.1**; client **valkey-glide** | Per-DB ACLs, I/O threading, `MSETEX` |
| Assistant answer path | **cachetools** as in-process L1 | new → **Adopt** | MIT, active, zero dependencies |
| Assistant answer path | moka-py | new → **Trial** | Faster TinyLFU. Third-party binding |
| Assistant answer path | aiocache | new → **Hold** | No release since 2024-09 |
| Assistant answer path | DragonflyDB v2 | new → **Hold** | BSL 1.1, and no gain over Valkey for us |
| Assistant answer path | Typesense / Meilisearch | new → **Assess** | A network hop with no need at our symbol count. Meilisearch EE is BUSL |
| Assistant answer path | **rapidfuzz + symspellpy + indic-transliteration + IndicXlit (offline alias generation)** | new → **Trial** | Deterministic Hindi/Hinglish symbol resolution |
| Fast text decisions | **Sarvam-30B (Apache-2.0, 2.4B active), self-hosted in Mumbai** | new → **Assess** | The only open India-hosted phrasing model. Latency is unmeasured |
| Fast text decisions | Sarvam 105B API | new → **Assess** | India-hosted per the vendor. Too large for the 300 ms path |
| Fast text decisions | Sarvam-1, Krutrim | new → **Hold** | Non-commercial or custom licence |
| Fast text decisions | xgrammar / outlines | new → **Assess** (conditional on self-hosting) | outlines does not support Python 3.14 |
| Finance NLP | IndicBERT-v3 (MIT), IndicTrans2 (MIT, via IndicTransToolkit) | new → **Assess** | Hindi tagging; offline template translation |
| Agents (research only) | **Groww MCP (official, can trade)** | new → **Hold** for agent tooling | Order-placing tools |
| Agents (research only) | `sec-edgar-mcp` (AGPL), finstack-mcp (yfinance) | new → **Hold** | Licence; invariant 7 |
| (new row) Observability / evals | **Langfuse self-hosted + OpenInference/OTel** | new → **Trial** | MIT core. Watch the ClickHouse ownership and the `ee/` boundary |
| (new row) Observability / evals | Arize Phoenix | new → **Assess** | **ELv2**: internal use only |
| (new row) Observability / evals | Ragas | → **Hold** for new work | Inactive since 2026-02 |

**Ranked recommendation**
1. NSE D&A Corporate Data (licensed) is the product path. Official NSE/BSE RSS plus XBRL is the evaluation path once permission is in writing.
2. SEBI and PIB RSS plus the MoSPI API are free, official event sources. RBI RSS needs RBI's permission first (Q-O5).
3. Deterministic Hinglish symbol resolution: rapidfuzz, symspellpy, and IndicXlit/indic-transliteration aliases, with cachetools L1 and Valkey 9.1.
4. Langfuse self-hosted in Mumbai for answer tracing.
5. Sarvam-30B as a Mumbai-hosted phrasing challenger, behind the existing interface.

**Conditions that would change this**
- **NSE or BSE confirm in writing that RSS may be polled and linked out:** move exchange RSS to Trial and make it the primary India filing trigger.
- **They refuse:** exchange RSS moves to Hold.
- **A Sarvam-30B p95 under about 120 ms for a 60-token phrasing on one Mumbai GPU:** move it to Trial.
- **AMFI grants written commercial permission:** move AMFI NAV to Trial.
- **Langfuse changes its licence under ClickHouse:** re-evaluate.
- **Valkey ElastiCache is unavailable in ap-south-1 at 9.1:** self-host.

---

## 7. Questions to send (drafts; not sent)

- **Q-O1 (NSE Data & Analytics / NSE Legal, and BSE):** "May a commercial information-only app poll your published RSS feeds (NSE: nsearchives `/content/RSS/*.xml`; BSE: `/data/xml/*.xml`) at the stated TTL, store item metadata (title, subject, timestamp, link) and show headline-level items with a link back to the exchange document? Does NSE ToU §'automated data collection' apply to your own RSS? If not permitted, what does the Corporate Data feed cost for display to N users?"
- **Q-O2 (AMFI):** "May a commercial app display daily NAVs from NAVAll.txt to its users with attribution? If not, which licensed route (for example RTAs or vendors) do you recommend?"
- **Q-O3 (NSDL):** "What are the reuse terms for FPI and the new daily DII reports displayed in a commercial app?"
- **Q-O4 (Sarvam):** "What rate limits, data-residency guarantee (region) and p50/p95 time-to-first-token apply to Sarvam 105B from Mumbai? Will a hosted Sarvam-30B return?"
- **Q-O5 (RBI, Web Information Manager):** "We request permission to hyperlink to internal pages (press releases, notifications) referenced in your RSS feeds, and to store item titles and timestamps from those feeds, in a commercial information-only app. Please state any conditions."
- **Counsel:** whether polling exchange-published RSS is "systematic or automated data collection" under the NSE ToU. BSE terms are unread (403).

---

## 8. Unverified list

1. **BSE Terms of Use**: the www host returns 403 or a 158-byte block; the beta host returns 404. The BSE RSS reuse terms are unknown.
2. Whether **RSS polling** is covered by the NSE ToU automated-collection ban (legal).
3. **SEBI website copyright or terms page**: the obvious URLs 404, and the homepage has no terms link that curl could see. (RBI terms were read; see §1.3.)
4. NSDL FPI portal terms: both URL forms timed out. CDSL FPI data not found.
5. Participant-wise OI and FII/DII publish times (~19:00 IST is from a secondary source). Bhavcopy UDiFF filename and circular numbers are from search results; the circular PDFs were not opened.
6. (Resolved) The SEBI BSE order was read in full: dated 2025-06-25, H.
7. MoSPI re-basing release dates (secondary). The IIP new-series release date has not been confirmed.
8. MCA "no public API" (secondary). The MCA site blocked curl.
9. data.gov.in rate-limit numbers.
10. FBIL fees are from 2018/2023 documents; current fees are unconfirmed.
11. Sarvam hosting region (not stated in the docs index), LLM-specific rate limits, and latency. The "<200 ms" figure is a secondary voice claim with no methodology. The API price was read through a summarizer.
12. Valkey 9.0/9.1 throughput claims have **no published methodology**. The 9.1 feature list comes from search summaries and the Linux Foundation press release, not the release notes. ElastiCache Valkey 9.1 availability in ap-south-1 has not been checked.
13. Upstox MCP read-only status was not re-verified this pass.
14. The `dbie.rbihub.in` / `Reserve-Bank-Innovation-Hub` provenance (possible impersonation).
15. The `indictrans2` PyPI package's provenance (gmail author, not referenced upstream).
16. The `sarvamai` SDK licence (none in metadata; repo 404).
17. Krutrim licence interpretation (the MAU-threshold wording is ambiguous; needs counsel).
18. `nsetools` and `nsefin` endpoints were not grepped; scraping is inferred.
19. The Langfuse acquisition date and "no licence change" statement are vendor-stated (M).
20. The Typesense GPL-3.0 network-use reading is my own inference, not legal advice.
21. Krutrim Cloud pricing and India-DC claims (third-party summary; the primary pricing page was not read).
22. Langfuse Cloud plan prices (secondary). Arize AX pricing and regions.

---

## 9. Sources (all accessed 2026-09-24)

**Registries**
- PyPI JSON: https://pypi.org/pypi/{jugaad-data, nsepython, nselib, bsedata, kiteconnect, pykiteconnect(404), openchart, nsepy, nse, bhavcopy, nsefin, nsetools, jugaad_trader, upstox-python-sdk, dhanhq, smartapi-python, smartapi, fyers-apiv3, breeze-connect, valkey, valkey-glide, redis, cachetools, aiocache, moka-py, cashews, rapidfuzz, symspellpy, symspell(404), typesense, meilisearch, meilisearch-python-sdk, tantivy, indic-transliteration, ai4bharat-transliteration, indictrans2, IndicTransToolkit, sarvamai, krutrim(404), outlines, xgrammar, instructor, langfuse, arize-phoenix, phoenix, arize-phoenix-otel, openinference-instrumentation, deepeval, ragas, promptfoo, inspect-ai, llguidance, lm-format-enforcer, finstack-mcp, alpha-vantage-mcp(404), sec-edgar-mcp}/json
- crates.io: https://crates.io/api/v1/crates/moka ; https://crates.io/api/v1/crates/tantivy
- Hugging Face: https://huggingface.co/api/models?author=sarvamai ; ?author=ai4bharat ; ?author=krutrim-ai-labs ; https://huggingface.co/api/models/sarvamai/sarvam-30b ; …/sarvam-105b ; …/sarvam-1 ; https://huggingface.co/sarvamai/sarvam-1/raw/main/README.md ; https://huggingface.co/sarvamai/sarvam-30b/raw/main/README.md ; https://huggingface.co/api/models/ai4bharat/indictrans2-en-indic-1B ; https://huggingface.co/api/models/ai4bharat/IndicXlit
- GitHub: repos and LICENSE for jugaad-py/jugaad-data, aeron7/nsepython, RuchiTanmay/nselib, sdabhi23/bsedata, zerodha/pykiteconnect, marketcalls/openchart, BennyThadikaran/NseIndiaApi, zerodha/kite-mcp-server, valkey-io/valkey, dragonflydb/dragonfly, redis/redis, moka-rs/moka, deliro/moka-py, typesense/typesense, meilisearch/meilisearch, quickwit-oss/tantivy, wolfgarbe/SymSpell, AI4Bharat/IndicXlit, AI4Bharat/IndicTrans2, VarunGumma/IndicTransToolkit, langfuse/langfuse, Arize-ai/phoenix, promptfoo/promptfoo, confident-ai/deepeval, vibrantlabsai/ragas, dottxt-ai/outlines, mlc-ai/xgrammar, 567-labs/instructor, nso-india/esankhyiki-mcp, financial-datasets/mcp-server, alphavantage/alpha_vantage_mcp, massive-com/mcp_massive, ola-krutrim/Krutrim-2-12B, aio-libs/aiocache, tkem/cachetools, rapidfuzz/RapidFuzz, finstacklabs/finstack-mcp, Reserve-Bank-Innovation-Hub/dbie.rbihub.in

**Official pages**
- NSE ToU: https://www.nseindia.com/static/nse-terms-of-use
- NSE RSS index: https://www.nseindia.com/static/rss-feed ; sample: https://nsearchives.nseindia.com/content/RSS/Online_announcements.xml
- NSE XBRL info: https://www.nseindia.com/static/companies-listing/xbrl-information
- NSE D&A: https://www.nseindia.com/static/nse-data-and-analytics
- NSE FII/DII: https://www.nseindia.com/reports/fii-dii ; all reports: https://www.nseindia.com/all-reports
- BSE RSS: https://beta.bseindia.com/rss-feed.html ; https://www.bseindia.com/data/xml/notices.xml ; BSE ToU (403): https://www.bseindia.com/termsofuse.html
- SEBI RSS: https://www.sebi.gov.in/sebirss.xml ; SEBI BSE order: https://www.sebi.gov.in/sebi_data/attachdocs/jun-2025/order_bse_matter.pdf (not opened) ; summary: https://boringmoney.in/p/bse-sent-company-info-paid-subs
- RBI RSS: https://rbi.org.in/Scripts/rss.aspx ; DBIE: https://data.rbi.org.in/
- MoSPI: https://api.mospi.gov.in/ ; https://esankhyiki.mospi.gov.in/llms.txt ; https://esankhyiki.mospi.gov.in/.well-known/ard.json ; re-basing: https://www.mospi.gov.in/cpi ; https://utkarsh.com/current-affairs/national/economy-update/mospi-revises-base-year-for-gdp-cpi-and-iip-series
- PIB RSS: https://www.pib.gov.in/RssMain.aspx ; https://www.pib.gov.in/ViewRss.aspx?reg=3&lang=2
- data.gov.in GODL: https://www.data.gov.in/Godl
- MCA: https://www.mca.gov.in/ (403 to curl) ; https://qorpiq.com/learn/mca-company-master-data-explained (secondary)
- AMFI: https://www.amfiindia.com/net-asset-value/nav-download ; https://www.amfiindia.com/terms-of-use ; https://portal.amfiindia.com/spages/NAVAll.txt
- NSDL: https://www.fpi.nsdl.co.in/Reports/Latest.aspx ; DII daily: https://www.thehansindia.com/business/nsdl-to-begin-daily-reporting-of-dii-investment-trends-to-enhance-market-transparency-1081811
- FBIL fees: https://www.fbil.org.in/uploads/Data_Fee_Schedule_FAQ_repl_3576a15203_f39da07c83.pdf ; https://www.fbil.org.in/uploads/FAQ_s_updates_30th_Nov_2023_edited_version_1def7b65bb.pdf
- UDiFF: https://www.nseclearing.in/udiff ; https://teamleaseregtech.com/updates/article/32105/nse-issued-a-circular-regarding-the-standardization-of-exchange-to-mem/
- MCA XBRL: https://in.xbrl.org/important-mca-filings/

**Infrastructure, LLMs, MCP, evaluation**
- Valkey 9: https://valkey.io/blog/introducing-valkey-9/ ; 9.1: https://valkey.io/blog/valkey-9-1-delivers-improvements-in-security-performance-and-more/ ; https://www.linuxfoundation.org/press/valkey-enhances-efficiency-security-and-modular-performance-with-9.1-release-and-new-ecosystem-integrations ; https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-elasticache-valkey-9-1/ ; releases: https://github.com/valkey-io/valkey/releases
- Dragonfly: https://github.com/dragonflydb/dragonfly/blob/main/LICENSE.md ; https://github.com/dragonflydb/dragonfly/releases/tag/v2.0.0
- Sarvam: https://www.sarvam.ai/api-pricing ; https://docs.sarvam.ai/api/getting-started/ratelimits ; https://docs.sarvam.ai/llms.txt ; hosting claims: https://entrepreneurloop.com/sarvam-ai-epoch-2026-sovereign-ai-infrastructure-roadmap/ (L)
- Kite MCP: https://github.com/zerodha/kite-mcp-server
- Groww MCP: https://groww.in/updates/groww-mcp
- Dhan MCP (proposal): https://madefortrade.in/t/official-dhan-mcp-server-for-direct-cloud-ai-integration-advanced-analysis/89843
- Langfuse / ClickHouse: https://clickhouse.com/blog/clickhouse-acquires-langfuse-open-source-llm-observability ; https://langfuse.com/blog/joining-clickhouse ; https://github.com/langfuse/langfuse/blob/main/LICENSE
- Phoenix licence: https://github.com/Arize-ai/phoenix/blob/main/LICENSE
- Meilisearch licence: https://github.com/meilisearch/meilisearch/blob/main/LICENSE
- RBI Disclaimer: https://rbi.org.in/Scripts/Disclaimer.aspx
- SEBI BSE order (full text read): https://www.sebi.gov.in/sebi_data/attachdocs/jun-2025/order_bse_matter.pdf
- Langfuse regions: https://langfuse.com/security/data-regions ; pricing (secondary): https://www.cekura.ai/blogs/langfuse-pricing
- Sarvam docs: https://docs.sarvam.ai/api/getting-started/commercial-licensing.md ; https://docs.sarvam.ai/api/getting-started/ratelimits.md
- Krutrim Cloud pricing (secondary): https://myaiguide.co/tools/ola-krutrim ; primary (not read): https://docs.cloud.olakrutrim.com/basics/pricing
