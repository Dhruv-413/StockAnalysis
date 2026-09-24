# Research papers: India-first market assistant (events, sentiment, explanation, RAG faithfulness, indicators, retail AI harm)

Author role: quant-researcher. Research and access date for every URL: **2026-09-24**. Read-only web research; no repo edits, no installs, no paid or live data APIs.
Product context: India-first (NSE/BSE) information-only assistant with a US second leg. It covers news, sentiment, indicators, events, deals and history, targets 300 ms card answers, and does not forecast for users.

**Deliberately not repeated.** These are already covered in existing appendices, and this report cites them by section instead:
- `research/papers.md`
  - §9: MacKinlay; Brown & Warner.
  - §10: Boudoukh et al.; Tetlock; Roll; Jeon et al.
  - §11: ALCE, RAGAS, AIS, FActScore.
  - §12: FinBen, StockBench, LiveTradeBench, FinSearchComp, "Beyond the Reported Cutoff".
  - §4: FinanceBench.
  - §3: look-ahead / point-in-time LMs.
- `research/accuracy-indicators-algos.md`
  - §2.1: SEBI F&O studies FY22, FY22–24, FY25, FY26.
  - §2.2: Park & Irwin; Bajgrowicz & Scaillet; the *Quantitative Finance* 11(2) India TA paper.
  - §2.3: India sentiment indices.
  - §3: retail algo framework, PaRRVA, RA amendments, SEBI AI/ML consultation of 20 Jun 2025.
  - §5: arXiv 2607.11414.
- `research/finance-models-evidence.md`: time-series foundation models, FinGPT/Fin-R1, and "The Memorization Problem".
- `research/global-news-and-data.md` §3 ("Sentiment", "Open models"): MuRIL/IndicBERT and the absence of a Hindi financial-sentiment benchmark.
- `research/india-market-data-and-sebi.md` §3 ("SEBI regulation affecting the assistant", item 5): the finfluencer circulars.
- `research/assistant-300ms-and-jev.md` §2.3 (entity-resolution stage) and §3.3 (evals, including the own golden set with Hinglish).

This report adds new papers. It also upgrades one prior item: the **SEBI FY22–FY25 table, which is now read at primary level (H)**.

**Labels**
- Confidence:
  - **H**: bibliographic facts and the quoted numbers were read on the primary page. That means the publisher, arXiv abstract or HTML, the PMC full text, or a sebi.gov.in PDF.
  - **M**: from a search-engine summary, a secondary article, or an automated abstract extraction not checked line by line.
  - **L**: a single secondary or unattributed source.
- Peer-review status:
  - **PR**: journal or proceedings venue confirmed.
  - **ACC**: "accepted at X" per the arXiv comment only, not checked on the venue site.
  - **WP**: working paper, arXiv or SSRN only.
  - **REG**: regulator publication.
- Verdict:
  - **MVP**: shapes the first release.
  - **Later**: a later experiment, the eval harness, or the backtesting module.
  - **Not in plan**: do not build on it or cite it as evidence of usefulness.
- Content markers: **[V]** verified fact; **[I]** inference; **[P]** our proposal; **[U]** unverified.

---

## 0. Bottom line

1. **The Indian event literature says *which* disclosures carry price information. It does not license showing an expected return.**
   - Insider (SEBI PIT) purchases are followed by a 90-day CAAR of about 6.67% (Aziz 2026).
   - Bulk trades show cumulative returns up to about 7.49% around the trade date, with evidence of front-running (Chaturvedula et al. 2015).
   - Promoter pledging predicts crash risk (Kalia 2024).
   - Earnings announcements show significant pre-event drift in 32 of 37 quarters (Sehgal & Bijoy 2015).
   - These tell us **which event types to ingest, label and time-stamp**.
   - None of these studies meets 06 §7. None has costs, a point-in-time universe or a deflated Sharpe, and most are pre-2020 or single-sample. So they are MVP evidence for *what to show*, and Not in plan as *signals*.
2. **Three findings change our wording.**
   - (a) Indian FII flows **follow** returns: returns Granger-cause flows, i.e. positive feedback trading (Mukherjee & Tiwari 2022). "Stock fell on FII selling" can put causation the wrong way round, so use "coincided with".
   - (b) Bulk and block deal files and FII/DII provisional data are published **after the close**. Under invariant 6 they must be labelled "published after the move began".
   - (c) Pre-announcement drift and front-running are documented, so "the move started before the filing" is a normal case, not an error. The explanation card needs a "move began before disclosure" state.
3. **Retail harm evidence is now primary-sourced and severe.**
   - The SEBI FY25 PDF gives loss-makers per year: FY22 90.2%, FY23 91.7%, FY24 91.1%, FY25 91.0% [V, H].
   - FY25 net loss was ₹1,05,603 cr across 96 lakh traders (top-13 brokers).
   - The SEBI intraday cash study found 71% of individual intraday traders lost money in FY23 [V, H for the headline].
   - The IOSCO May 2025 finfluencer and digital-engagement reports and the ESMA March 2025 investor warning on AI all point the same way.
   - This supports the no-forecast, no-"signal" stance and a mandatory risk-context line.
4. **Hindi and Hinglish financial sentiment has no usable benchmark.**
   - The only Hindi stock-tweet dataset found is a 2023 LNDECT chapter (LSTM, 72% test accuracy). It isn't a benchmark.
   - The Hinglish sentiment corpora (SemEval-2020 Task 9 and others) are not financial.
   - FinVQA / FIND (arXiv 2605.13330) is the first Indic multilingual *financial reasoning* set: 6 languages, 18,900 items. It is QA, not sentiment, and its data licence is unverified.
   - **We must label our own Hindi/Hinglish finance set.** This confirms global-news-and-data §3.
5. **The "NIFTY" dataset is a trap.** "NIFTY Financial News Headlines" (arXiv 2405.09747) stands for "News-Informed Financial Trend Yield". It covers the **US S&P 500 (SPY)** with WSJ/Reuters headlines from 2010–2020 [V, H]. It is not Indian. Do not use it as India evidence.
6. **Among the Indian sentiment datasets, SEntFiN 1.0 is the credible one.** It has 10,753 entity-annotated headlines from Indian outlets (JASIST 2022). The paper is CC BY 4.0, but the **dataset licence and the rights to the underlying headline text (ET/Moneycontrol) are unverified**. It is fine for an internal baseline eval only, never for product training, until the licence is checked.
7. **Numerical faithfulness is still a retrieval problem, and tools beat RAG for prices.**
   - Kang & Liu (2023): LLMs cannot recall historical prices. With RAG they still fail; with tool calls they reach 98–100% accuracy.
   - Financial Touchstone (2026): retrieval causes 48.9% of failures.
   - Vals Finance Agent Benchmark (2025): the best agent (o3) scores 46.8%.
   - Fin-RATE (KDD 2026): accuracy falls 14–19% on longitudinal and cross-entity tasks, with temporal mismatches.
   - DocFinQA (ACL 2024): the best evaluated model (GPT-3.5) reached 42.6% over 123k-word documents.
   - Direct MVP support for invariant 5: numbers come from deterministic tools, never from model memory or free RAG text.
8. **There is still no benchmark for "why did it move" explanation faithfulness.** This confirms the papers.md §12 gap. The nearest pieces are:
   - FinDVer (EMNLP 2024): claim verification over filings.
   - Fin-Fact (WWW 2025 companion): claims plus justifications.
   - FinGround (ACC ACL 2026 Industry): atomic-claim verification that notes existing detectors miss 43% of computational errors.
   - A grounded 8-K event-extraction release (arXiv 2607.08346): 119-type taxonomy, 601k tags, precision 12–96% depending on its quality score.
   - None tests abstention on no-news moves, or the timing of the cited evidence against the move.
9. **Technical indicators in India: no study meets 06 §7 at the NIFTY-stock level (absence finding).**
   - Multi-market studies with data-snooping control do exist:
     - Heyman, Inghelbrecht & Pauwels (2012): 34 emerging markets, White's Reality Check (WRC) + SPA, significant in only 4 of 34.
     - Rink (FMPM 2023): 41 markets, SPA. Results are in-sample only, erased by moderate costs, and not persistent out of sample.
   - **Whether India is in these samples is unverified.**
   - The India-only studies lack data-snooping control: Muruganandan 2020 (Sensex, RSI/MACD) and IMFI 2023 (14 stocks over 8 months).
   - Indicators stay descriptive only.

---

## 1. Registry table

| # | Work | Venue / year | Market, data | Key finding | Status | Conf. | Verdict |
|---|---|---|---|---|---|---|---|
| 1.1 | SEBI, "Comparative study of growth in EDS vis-à-vis cash market after recent measures" (incl. FY25 P&L) | SEBI research, Jul 2025 | NSE/BSE; top-13 brokers, about 96 lakh traders | Loss-makers FY22–25: 90.2 / 91.7 / 91.1 / 91.0%. FY25 net loss ₹1,05,603 cr | REG | H | MVP (risk context) |
| 1.2 | SEBI intraday cash-segment study | SEBI, 24 Jul 2024 | Top-10 brokers; FY19, FY22, FY23 | 71% of individual intraday traders lost money in FY23 | REG | H (headline), M (details) | MVP (risk context) |
| 1.3 | SEBI FY25–FY26 profitability and trading-behaviour studies | SEBI DEPA, 20 Aug 2026 | Top-15 brokers; random sample of 5,000 traders | Already in accuracy-indicators-algos §2.1. New detail: about 97% of traders mainly buy options; about 90% who lost two years running lost again in the third | REG | M (secondary) | MVP (risk context) |
| 1.4 | Aziz, "Are insider purchases informative? Evidence from Indian firms" | *DECISION* (Springer), 2026 | High-value PIT purchase disclosures | 90-day CAAR 6.67%. Stronger for small firms and promoters | PR | M | MVP (event type); Not in plan (signal) |
| 1.5 | Chaturvedula, Bang, Rastogi & Kumar, "Price manipulation, front running and bulk trades" | *Emerging Markets Review* 23, 2015 | BSE/NSE bulk trades, 2004–2012 | Cumulative returns up to 7.49% around trades. Evidence of front-running. Buy/sell asymmetry | PR | M | MVP (event type, timing label) |
| 1.6 | Kalia, promoter pledging and crash risk | *J. Advances in Management Research* 21(2), 2024 | 257 S&P BSE 500 firms, 2011–2020 | Pledging is positively related to future crash risk and negatively to performance (fixed effects, IV-2SLS) | PR | H | MVP (show pledge % as context) |
| 1.7 | Shruti R, Ghosh & Thenmozhi, "Strengthening pledgee rights and stock price crash risk" | SSRN 5592738 | India; pre/post IBC 2016 | Pledging raised crash risk only after IBC | WP | M | Later |
| 1.8 | Gupta, Patel & Sane (LEAP blog on Aggarwal et al. 2025): market reaction to SEBI insider-trading orders | LEAP blog, May 2026 | 176 SEBI orders, 42 SAT decisions, NSE, 2009–2023 | CARs(−10,+10) indistinguishable from zero (the SEC comparator is −3.47%) | WP | M | MVP (enforcement orders ≠ price catalyst) |
| 1.9 | Sehgal & Bijoy, stock price reactions to earnings announcements in India | *Vision* (SAGE), 2015 | 469 firms, Dec 2002–Dec 2011, 37 quarters | Significant pre-event AR in 32/37 quarters; post-event in 35/37 | PR | M | MVP (pre-disclosure drift is normal) |
| 1.10 | Mukherjee & Tiwari, "Trading behaviour of FIIs: evidence from Indian stock markets" | *Asia-Pacific Financial Markets* 29(4):605–629, 2022 | NSDL daily FII flows, Nifty 50/Sensex, Apr 2014–Nov 2019 | Returns Granger-cause FII flows (positive feedback). LSV herding in 47/50 Nifty stocks | PR | H | MVP (wording rule) |
| 1.11 | Dasgupta, Sane & Suresh, cyber incidents | LEAP blog, Jan 2024 | 48 incidents, 40 firms, 2013–2023 | Mean CAR −3.48% in the first month. Media dates, not exchange-filing dates | WP | M | Later (illustrates the date-source problem) |
| 2.1 | Sinha, Kedas, Kumar & Malo, SEntFiN 1.0 | *JASIST* 73(9):1314–1335, 2022; arXiv 2305.12257 | 10,753 Indian headlines (ET, Moneycontrol), 2002–2017 per search [M]; 1,000+ entities | RoBERTa/FinBERT about 94.3% accuracy, 93.3% F1 on entity sentiment | PR | H (paper), U (data licence) | Later (internal baseline only) |
| 2.2 | Saqur et al., "NIFTY Financial News Headlines Dataset" | arXiv 2405.09747, 2024 | **US: SPY, WSJ/Reuters, 2010–2020**. HF card MIT; paper CC BY-NC-ND | Not Indian despite the name | WP | H | Not in plan (for India) |
| 2.3 | Chaithra, Kadimisetty & Mohan, adaptive sentiment for NIFTY 50 | ACC CODS 2025; arXiv 2512.20082 | "SentiFin" headlines; 3B LLaMA, RAG, PPO | Reports gains in accuracy/F1/"market alignment". Abstract gives no numbers or costs | ACC | M | Not in plan |
| 2.4 | Chari, Hegde Desai, Borde & George, "Aggregate news sentiment and stock market returns in India" | *JRFM* 16(8):376, 2023 | Dictionary sentiment, big-move days, GARCH | Effect is short-lived; strongest from business and politics news | PR | M | Later (supports descriptive-only) |
| 2.5 | Anushka, Mohit & Lavanya, Hindi stock-market tweets | LNDECT vol 166 (Springer), 2023 | Hindi tweets, 2 annotators | LSTM test accuracy 72.19%, F1 0.77 | PR (proceedings) | M | Not in plan (too small and weak) |
| 2.6 | SemEval-2020 Task 9 (Hinglish SentiMix) and derivatives | SemEval 2020; arXiv 2008.04277 | About 17k general-domain code-mixed tweets | Not finance | PR | M | Later (router/tokeniser eval only) |
| 2.7 | Das et al., FIND / FinVQA | arXiv 2605.13330, May 2026 | 18,900 items; EN, HI, BN, MR, GU, TA; 14 financial domains | First Indic multilingual financial reasoning set. Abstract gives no Hindi–English gap numbers | WP | H (existence), U (data licence) | Later (eval) |
| 2.8 | Pall, IndiaFinBench | arXiv 2604.19298, Apr/May 2026 | 406 QA pairs from 192 SEBI/RBI documents | Zero-shot 70.4–89.7%. Numerical reasoning has a 35.9 pp spread | WP | H (arXiv); repo URL 404 on fetch | Later (eval) |
| 2.9 | MultiFinBen | arXiv 2506.14028 (v3 Oct 2025) | 5 languages (Hindi not listed), multimodal | GPT-4o 46.01% overall; sharp multilingual drop | WP | H | Later (reference) |
| 3.1 | El Ghoul, Guedhami, Mansi & Sy, "Event studies in international finance research" | *JIBS* 54(2):344–364, 2022 | Methods review | Mild-segmentation benchmark; Dimson lags for non-synchronous trading; bootstrap tests; clustering | PR | H | MVP (method) |
| 3.2 | Dolphin et al., grounded event extraction from 8-K filings | arXiv 2607.08346, Jul 2026 | 292,984 8-Ks, 2022–26; 119 types; 601,088 tags | Precision 12–96% by quality score; unsupported tags fall from 8% to about 0 at high scores | WP | H | MVP (US leg taxonomy and grounding pattern) |
| 3.3 | Yao et al., DelistBench | arXiv 2608.22770, Aug 2026 | 1,200 delisting records | Best joint accuracy 81.5% within 7 days; 27.3% still routed to human review | WP | H | Later (corporate-action ledger QA) |
| 3.4 | Zhao et al., FinDVer | EMNLP 2024 main; arXiv 2411.05764 | Expert-annotated claim verification over long filings | GPT-4o lags human experts. Size: 2,400 (arXiv) vs 4,000 (snippet); conflict recorded | PR | H | MVP (eval design) |
| 3.5 | Rangapur, Wang & Shu, Fin-Fact | WWW 2025 Companion; arXiv 2309.08793 | 3,369 claims with rulings and justifications | Multimodal fact-check and explanation benchmark (PolitiFact-style) | PR | H | Later |
| 3.6 | Guo, Wu & Yiu, FinGround | ACC ACL 2026 Industry; arXiv 2604.23588 | Text plus tables | −68% hallucination vs the best baseline at equal retrieval. 8B detector F1 91.4%. Existing detectors miss 43% of computational errors | ACC | H | MVP (verifier design) |
| 4.1 | Kang & Liu, "Deficiency of LLMs in finance: hallucination" | arXiv 2311.15548, 2023 | Historical price queries | Zero-shot 0% accuracy (Llama-2) or abstain (GPT). RAG didn't fix it. Tool calls reach 98.4–100% | WP | H | MVP (invariant 5) |
| 4.2 | Reddy et al., DocFinQA | ACL 2024 (short) | 7,437 FinQA questions with full filings (about 123k words) | Best evaluated model 42.6% (GPT-3.5; setting not read); retrieval-assisted GPT-4 ≈ non-expert humans | PR | M | Later (eval) |
| 4.3 | SEC-QA | FinNLP 2025 workshop; arXiv 2406.14394 | Multi-document, refreshable | RAG "systematically fails" on multi-document questions; refreshable to post-cutoff documents | PR (workshop) | M | Later (refresh idea: MVP) |
| 4.4 | Jiang et al., Fin-RATE | KDD 2026; arXiv 2602.07294 | SEC filings; 17 LLMs | Accuracy −18.6% (longitudinal) and −14.35% (cross-entity); temporal-mismatch hallucinations | ACC | H | MVP (eval axis) |
| 4.5 | Bigeard et al., Finance Agent Benchmark (Vals AI) | arXiv 2508.00828, 2025 | 537 expert questions; EDGAR plus search tools | Best o3 46.8% at $3.79/query; 10 models scored 0 on Trends | WP | H | Later |
| 4.6 | Spörer, "Can open-weight models compete on financial text comprehension?" | ACC FinLLM@IJCAI 2026; arXiv 2608.08634 | 2,967 questions over 495 annual reports | Best 88.4%. **Retrieval = 48.9% of failures** | ACC | H | MVP (retrieval-first) |
| 4.7 | Zhang et al., FAITH | ACC ICAIF 2025; arXiv 2508.05201 | S&P 500 annual reports, masked-span | A framework for tabular hallucination; abstract gives no rates | ACC | H | Later |
| 4.8 | Zhu et al., FinTMMBench | ACC ACM MM 2025; arXiv 2503.05185 | NASDAQ-100: tables, news, prices, charts | Temporal-aware RAG; "notable gaps remain" | ACC | H | Later |
| 4.9 | Zhao & Welsch, point-in-time financial RAG | arXiv 2605.31201, 2026 | 89 Nasdaq stocks (FNSPID) plus PiT EDGAR | Macro-F1 0.438 → 0.471; Sharpe 0.52 → 0.84 (no costs stated) | WP | H | Later (PiT retrieval design); Not in plan (signal) |
| 4.10 | Wang, "Confidently wrong" | arXiv 2607.11414 | FinQA/TAT-QA, 8–9B models | Already cited in accuracy §5 (0.73–0.79 overall). **Adds the confident-answer subset:** probe AUROC 0.68–0.77; 5–19% of 8/8-consistent answers wrong | WP | H | Later |
| 5.1 | Heyman, Inghelbrecht & Pauwels, technical trading rules in emerging stock markets | SSRN 1998036, 2012 | 34 emerging markets | WRC + SPA with costs: significant in only 4/34; more profitable in crises | WP | M (India inclusion U) | Later (method template) |
| 5.2 | Rink, "The predictive ability of technical trading rules" | *FMPM* 37(4):403–456, 2023 | 23 developed + 18 emerging indices; 6,406 rules; up to 66 years | SPA: in-sample outperformance, decaying over time, erased by moderate costs, not persistent out of sample | PR | H (abstract) | Later (evidence input) |
| 5.3 | Sermpinis, Hassanniakalager, Stasinakis & Psaradellis, discrete FDR | arXiv 1811.06766; JIFMIM version [U] | 12 MSCI markets, 2004–2015, 21k rules | "Short-term value" with frequent rebalancing; persistence weak | WP/PR [U] | M | Later |
| 5.4 | Muruganandan, "Testing the profitability of technical trading rules across market cycles: evidence from India" | *Colombo Business Journal* 11(1):24–46, 2020 | Sensex, Feb 2000–May 2018; RSI, MACD | No data-snooping correction. MACD sell signal "beat" the mean in bear markets, but not risk-adjusted; RSI failed | PR | H | Not in plan (fails 06 §7) |
| 5.5 | "The effectiveness of technical trading strategies: evidence from Indian equity markets" | *IMFI* (Business Perspectives), 2023 | 14 Nifty stocks, hourly, Jan–Aug 2022 | SMA net-profitable for 8/14 stocks; beat buy-and-hold for 6/14 | PR | M | Not in plan (canonical example of failing 06 §7) |
| 6.1 | IOSCO, "AI in Capital Markets: Use Cases, Risks, and Challenges" (consultation) and "Supervisory Toolkit for AI Use" (final FR/02/2026) | IOSCO, Mar 2025 and 25 May 2026 | Member and industry surveys | Top uses: client communications 66.7%, algo trading 63.3%, robo-advice 60% | REG | M | MVP (governance framing) |
| 6.2 | IOSCO final reports on finfluencers, online imitative trading, and digital engagement practices | IOSCO, 19 May 2025 | — | Risks: unregistered advice, conflicts, gamified nudges to trade more | REG | M | MVP (UX constraints) |
| 6.3 | ESMA public statement on AI and investment services (ESMA35-335435667-5924) | ESMA, 30 May 2024 | MiFID II | Disclose AI use in client interactions; firm stays responsible | REG | H (existence), M (content) | MVP (disclosure) |
| 6.4 | ESMA and NCAs, investor warning on using AI for investing | ESMA, Mar 2025 | — | Investor warning; the wording was not read (PDF) | REG | M | MVP (copy reference) |
| 6.5 | FCA Mills Review (engagement paper 27 Jan 2026; final report 6 Jul 2026) | FCA | UK retail | Engagement paper cites 28m UK adults using AI for money (Lloyds data). **Final report not read** | REG | M / U | Later |
| 6.6 | SEC withdrawal of the predictive-data-analytics conflicts proposal (S7-12-23) | SEC, 12 Jun 2025 | US | The proposal is withdrawn; no US PDA rule exists | REG | H (existence) | Later (watch) |
| 6.7 | D'Acunto, Prabhala & Rossi, "The promises and pitfalls of robo-advising" | *RFS* 32(5):1983–2020, **2019** (pre-2020, kept because it uses Indian brokerage data) | Robo-optimiser adopters at an Indian brokerage, Indian equities, Apr 2015–Jan 2017 (India setting M, via CFA Digest summary) | Helps under-diversified investors (fewer than 5 stocks); for others, more trading with no performance gain. Reduces but does not remove disposition effect and trend chasing | PR | H (citation), M (India setting) | MVP (design lesson) |
| 6.8 | Kakhbod, Kazempour, Livdan & Schürhoff, "Finfluencers" | SSRN 4428232, 2023 | StockTwits tweet-level data | 28% skilled (+2.6%/month), 16% unskilled, 56% antiskilled (−2.3%/month); antiskilled have more followers | WP | M | MVP (no social "signal" features) |
| 6.9 | Lalwani, "Finfluencer recommendations" | *Economics Letters* 255, 112511, 2025 | Indian financial YouTubers | Recommendations chase past returns and volume. **Recommendation frequency predicts higher future returns** (magnitude not read) | PR | H (citation), M (findings) | Later (do not surface as a signal) |
| 6.10 | Cheng, Lin & Zhao, "Does generative AI facilitate investor trading? Evidence from ChatGPT outages" | *J. Accounting & Economics* 80, 101821, 2025 | US; outage natural experiment | Volume falls during outages, especially for firms with fresh news; GenAI use improves long-run price informativeness | PR | M | Later (context) |
| 6.11 | Even-Tov, Lourie, Munevar & Nekrasov, "The effect of AI on retail investor behavior" | SSRN 5778246, Nov 2025 | Account-level brokerage data; Italy ChatGPT ban | During the ban: fewer assets traded, fewer new positions, a shift to popular assets | WP | M | Later (context) |
| 6.12 | Choukhmane, de Silva, Lin & Akuzawa, "AI financial advice: supply, demand, and life-cycle implications" | arXiv 2608.01607, Aug 2026 | Representative-sample prompts to GPT-5.2 | Advice nudges toward life-cycle norms. Recommendations differ by gender, about 2/3 via prompt wording | WP | H (abstract) | Later (fairness eval idea) |
| 6.13 | FINRA Foundation, "The machines are coming…" | FINRA Foundation, 2024 | US survey, n = 1,033, Feb 2024 | 5% would use AI for a financial decision, but trust in AI and in an advisor was equal (34% vs 33%) on the same statement | REG (foundation) | M | Later (UX trust calibration) |

---

## 2. Per-topic synthesis

### Topic 1: India market microstructure and events

**1.1 SEBI, EDS growth study with the FY25 P&L section (primary PDF read, H).**
- Source: https://www.sebi.gov.in/sebi_data/attachdocs/jul-2025/1751900271726.pdf ; landing page https://www.sebi.gov.in/reports-and-statistics/research/jul-2025/comparative-study-of-growth-in-equity-derivatives-segment-vis-vis-cash-market-after-recent-measures_95105.html
- **Data.** Section C covers the top 13 EDS brokers, about 96 lakh of the roughly 107 lakh unique EDS traders, FY2024-25. "Individual" means Individual plus HUF. Data comes from NSE and BSE.
- **Table 11 [V, H]:**

  | Year | Net P&L (₹ cr) | Traders (lakh) | Loss-makers | Avg P&L per person (₹) |
  |---|---|---|---|---|
  | FY22 | −40,824 | 42.7 | 90.2% | −95,517 |
  | FY23 | −65,747 | 58.4 | 91.7% | −1,12,677 |
  | FY24 | −74,812 | 86.3 | 91.1% | −86,728 |
  | FY25 | −1,05,603 | 96.0 | 91.0% | −1,10,069 |

- **Quarterly FY25 (Table 12).** Loss-makers were 84.5 / 86.3 / 88.5 / 86.4%. Unique traders fell from 61.4 to 42.7 lakh, Q1 to Q4, after the 20 Nov 2024 measures.
- **Activity, Dec 2024–May 2025 vs a year earlier.** Unique individual EDS traders −20%. Index-option premium turnover −9%, notional −29%.
- **Limitations.**
  - Broker coverage changes between studies: top-10 in the Sep 2024 study, top-13 here, top-15 in Aug 2026. The series is **not a like-for-like panel**.
  - The Sep 2024 headline of "93% over FY22–24" is a *three-year cumulative* measure. It is a different statistic from the per-year 90–92%. Do not mix them in one sentence.
  - The PDF itself says "causality can be difficult to establish".
- **Side fact [V, H].** The PDF footnote says that from January 2025 BSE index derivatives expired on Tuesday and NSE's on Thursday. The accuracy-indicators-algos §1.2 point-in-time expiry table must include this interim regime, before the 1 Sep 2025 swap to NSE Tuesday and BSE Thursday.
- **Verdict: MVP.** Use it as the dated risk-context line on any F&O card.

**1.2 SEBI intraday cash-segment study (Jul 2024).**
- Press release https://www.sebi.gov.in/media-and-notifications/press-releases/jul-2024/sebi-study-finds-that-7-out-of-10-individual-intraday-traders-in-equity-cash-segment-make-losses_84948.html (headline H).
- **Details from secondary sources (M):**
  - Business Standard https://www.business-standard.com/markets/news/over-70-intra-day-traders-incur-losses-during-fy23-reveals-sebi-study-124072401110_1.html
  - TaxGuru https://taxguru.in/sebi/sebi-study-finds-7-10-individual-intraday-traders-equity-cash-segment-losses.html
- **Sample and findings (M):**
  - Top-10 brokers, about 86% of individual cash-segment clients. Years FY19, FY22 and FY23.
  - 71% lost money in FY23.
  - 80% of traders with more than 500 trades a year lost money.
  - 76% of traders under 30 lost money.
  - For loss-makers, trading costs added 57% on top of trading losses. Profit-makers spent 19% of profits on costs.
  - Participation rose from about 15 to 69 lakh (4.6×). One secondary source says "threefold", which is a conflict (§6).
- **Verdict: MVP.** Use it for risk context on intraday cards. It is the cash-segment counterpart to 1.1.

**1.3 SEBI Aug 2026 studies.**
- Already in accuracy-indicators-algos §2.1.
- New items from secondary sources (M):
  - about 97% of traders mainly follow options-buying strategies;
  - about 90% of traders who lost two consecutive years and kept trading lost again;
  - about 35% had no equity holdings;
  - about 78% had equity portfolios under ₹1 lakh;
  - small-portfolio traders accounted for about 70% of losses on about half the turnover.
- Sources: https://www.sebi.gov.in/reports-and-statistics/research/aug-2026/study-trading-behaviour-of-individual-traders-in-the-equity-derivatives-segment-fy25-fy26-_103836.html ; secondary https://taxguru.in/sebi/sebi-studies-key-trends-retail-participation-trading-behaviour-profitability-equity-derivatives.html
- **Verdict: MVP** (risk context). Read the PDF before quoting (§7).

**1.4 Aziz (2026), insider purchases (PIT).**
- https://link.springer.com/article/10.1007/s40622-026-00473-3 (Springer blocked the fetch; details from search summaries, M).
- **Data and method.** High-value insider purchases disclosed under SEBI PIT; event study over 30, 60 and 90 days.
- **Findings.**
  - 90-day CAAR 6.67%.
  - Strongly negative relation between size and CAR.
  - Drift persists beyond the reaction window.
  - Stronger for promoter trades and small caps.
- **Limitations.**
  - No costs.
  - Small-cap concentration, where impact and illiquidity are highest.
  - Sample period and N not read.
  - Benchmark model not read.
- **Verdict.** MVP for including PIT/SAST disclosures as a first-class event type, time-stamped at exchange dissemination time. Not in plan as a return signal.

**1.5 Chaturvedula, Bang, Rastogi & Kumar (2015), bulk trades.**
- *Emerging Markets Review* 23:26–45. SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2625924 ; RePEc https://econpapers.repec.org/RePEc:eee:ememar:v:23:y:2015:i:c:p:26-45 (M).
- **Data.** BSE and NSE bulk trades, 2004–2012; event study.
- **Findings.**
  - Cumulative returns up to 7.49% around trades.
  - Front-runners could earn about 5–7% within a week.
  - Buy and sell trades react asymmetrically.
  - Volume and delivery explain the manipulation.
- **Limitations.** Pre-2013 data. The bulk-deal definition (above 0.5% of equity) is unchanged, but block-deal rules changed in Dec 2025 (see global-news-and-data). No costs.
- **Verdict.** MVP for two things:
  - (a) bulk and block deals are a card;
  - (b) a mandatory **"deal disclosed after close; price moved before disclosure"** timing label.

**1.6 Kalia (2024), promoter pledging.**
- Emerald https://www.emerald.com/insight/content/doi/10.1108/jamr-01-2023-0003/full/html (H, abstract read).
- **Data and method.** 257 S&P BSE 500 firms, 2011–2020; panel fixed effects and IV-2SLS.
- **Finding.** Pledging is positively related to future crash risk and negatively to future performance.
- **Limitations.** Index constituents only, so survivor bias. The crash-risk measures are the standard NCSKEW/DUVOL type (not read).
- **Related work.**
  - Shruti R, Ghosh & Thenmozhi, SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5592738 (M): the effect appears only after IBC 2016.
  - A JAEE paper on pledging and earnings quality: https://www.emerald.com/jaee/article/doi/10.1108/JAEE-11-2024-0482/1358373 (not read).
- **Verdict.** MVP for showing promoter pledge %, and changes in it, as descriptive context with the as-of shareholding-pattern date. It never becomes a "crash risk score".

**1.7 Market reaction to SEBI insider-trading enforcement.**
- LEAP https://blog.theleapjournal.org/2026/05/market-reaction-to-insider-trading.html (M), summarising Aggarwal et al. 2025. The underlying paper was not read.
- **Findings.** CAR(−10,+10) is indistinguishable from zero for 176 SEBI final orders and 42 SAT decisions (NSE, 2009–2023).
- **Implication.** A SEBI order is *not* a reliable catalyst for a price move. The explainer should not rank it high by default.
- **Verdict: MVP** (ranking prior).

**1.8 Sehgal & Bijoy (2015), earnings announcements.**
- *Vision* (SAGE), doi:10.1177/0972262914564042 (M; SAGE returned 403).
- **Data.** 469 firms, Dec 2002–Dec 2011.
- **Findings.** Significant pre-event AR in 32/37 quarters and post-event AR in 35/37.
- **Limitations.** Old sample; the timing convention for announcements during vs after trading hours was not read.
- **Also found (not read):**
  - Ganguli, PEAD for Indian turnaround firms (SSRN 1545647).
  - PEAD in NSE value/glamour stocks, 100 firms, 2014–2018 (ResearchGate).
- **Verdict.** MVP as a design fact: pre-announcement drift is common, so the "move began before disclosure" state must exist.

**1.9 Mukherjee & Tiwari (2022), FII behaviour.**
- PMC full text https://pmc.ncbi.nlm.nih.gov/articles/PMC9145119/ ; doi:10.1007/s10690-022-09361-z (H).
- **Data and method.** Daily NSDL FII flows, Apr 2014–Nov 2019, Nifty 50 and Sensex constituents. Granger causality, LSV and CSSD/CSAD.
- **Findings.**
  - Market returns Granger-cause FII flows at lags 1–4 (F = 3.62–8.05).
  - LSV herding in 47 of 50 Nifty stocks.
  - No market-wide herding under stress.
- **Limitations.** Pre-2020; large caps only. Granger causality is not structural causality.
- **Verdict: MVP wording rule.** On index or stock cards, FII/DII net flows are shown as *co-occurring* context, for example "FIIs were net sellers of ₹X cr (provisional, published after close)". Never "fell because FIIs sold". This also applies to invariant 6: provisional FII/DII numbers are published after the close.

**1.10 Absence findings for topic 1** (searches listed in §5).
- (a) No peer-reviewed NSE study of **price-band or circuit effects** (magnet effect, delayed price discovery) was found. The literature found is China-based and is not used here.
- (b) No event study specific to **Reg 30 LODR disclosures** that uses exchange dissemination timestamps.
- (c) No study that combines results-announcement timing with FII/DII flows.
- Each is a gap our own descriptive analytics must fill carefully, with no forecasting.

### Topic 2: News and sentiment in Indian markets

**2.1 SEntFiN 1.0.**
- *JASIST* 73(9):1314–1335 (2022), doi:10.1002/asi.24634 ; arXiv https://arxiv.org/abs/2305.12257 (H for the paper facts).
- **Data.**
  - 10,753 human-annotated headlines; 2,847 contain multiple entities, often with conflicting sentiment.
  - An entity database of 1,000+ entities and 5,000+ surface forms.
  - Sources (per search summary, M): Indian equities 2002–2017 from ET and Moneycontrol.
- **Result.** RoBERTa/FinBERT about 94.29% accuracy and 93.27% F1.
- **Licence, recorded as three separate fields:**

  | Field | Status |
  |---|---|
  | Paper | CC BY 4.0 (arXiv) [V] |
  | Annotation / dataset | [U] |
  | Source-text rights (ET/Moneycontrol headlines) | [U]; publisher-owned |
  | Commercial use | unknown |

- A Kaggle dataset by the same first author exists (https://www.kaggle.com/datasets/ankurzing/sentiment-analysis-for-financial-news); the fetch didn't render. Its link to SEntFiN is [U].
- **Verdict.** Later: an internal-only English-India baseline for our entity-level tagger. The entity dictionary is the most useful asset for our alias resolver (assistant-300ms-and-jev §2.3, stage 1, "Normalise + entity resolution"), subject to its licence.

**2.2 "NIFTY" dataset (Saqur et al. 2024). Misleadingly named.**
- arXiv https://arxiv.org/abs/2405.09747 ; HF https://huggingface.co/datasets/raeidsaqur/NIFTY (H).
- NIFTY stands for "News-Informed Financial Trend Yield". Coverage is **US SPY**, with WSJ and Reuters headlines from 2010-01-06 to 2020-09-21; 2,111 rows.

  | Field | Status |
  |---|---|
  | HF licence tag | MIT |
  | Paper licence | CC BY-NC-ND 4.0 |
  | Source-text rights | WSJ/Reuters [U] |
  | Commercial use | unknown |

- **Verdict: Not in plan.** It is not India data, and search engines surface it for "NIFTY sentiment" queries.

**2.3 CODS 2025 NIFTY 50 adaptive sentiment (Chaithra et al.).**
- arXiv https://arxiv.org/abs/2512.20082 (M).
- Uses "SentiFin": one search summary says 10,572 headlines; the abstract fetch says headlines "from 2024 to 2025"; a second summary says 8,000.
- **Unresolved whether "SentiFin" is SEntFiN (10,753).** Treat them as possibly the same corpus.
- The method optimises sentiment for "market alignment" with PPO. That bakes return prediction into the labeller, which is exactly what we must not do (invariant 5, no sentiment-as-forecast).
- The abstract reports no numbers and no costs.
- **Verdict: Not in plan.**

**2.4 Chari et al. (2023), aggregate news sentiment.**
- *JRFM* 16(8):376, doi:10.3390/jrfm16080376 (M; MDPI returned 403).
- **Method.** Dictionary-based sentiment on big-move days; GARCH plus regressions.
- **Finding.** The influence is short-lived; business and politics news matter most.
- **Verdict.** Later. It supports a descriptive-only sentiment display, consistent with accuracy §2.3.

**2.5 Hindi and Hinglish.**
- **Hindi stock tweets (Anushka, Mohit & Lavanya 2023).** LNDECT vol 166, Springer. https://link.springer.com/chapter/10.1007/978-981-99-0835-6_17 (M).
  - Two annotators; LSTM with 94.04% train and 72.19% test accuracy, F1 0.77.
  - The size gap and the low test accuracy suggest overfitting. The dataset licence is unknown.
  - **Not in plan.**
- **SemEval-2020 Task 9 (SentiMix).** About 17k Hinglish tweets, general domain. https://arxiv.org/pdf/2008.04277 (M).
  - Hinglish-24k merges it with another 11k set: https://arxiv.org/abs/2601.05091, NLPIR 2025, brand monitoring, **not finance** (H).
  - **Later**, only for testing tokenisation and routing on code-mixed input, not for financial polarity.
- **FIND / FinVQA** (Das et al., arXiv https://arxiv.org/abs/2605.13330, H for existence).
  - 18,900 items in 6 languages including Hindi, covering 14 financial domains. Formats: multiple choice, fill-in, table matching, true/false.
  - This is financial *reasoning* QA, not sentiment. The data licence is unverified; the paper is CC BY 4.0.
  - **Later**, for the Hindi numeric-QA eval.
- **IndiaFinBench** (arXiv https://arxiv.org/abs/2604.19298, H).
  - 406 items from SEBI and RBI documents; zero-shot accuracy 70.4–89.7%.
  - The GitHub URL from the paper returned 404 on 2026-09-24. The data licence is unverified; the paper is CC BY 4.0.
  - Single author; not peer reviewed.
  - **Later**, as a regulatory-text QA eval. It is already named in tech-radar.
- **MultiFinBen** (arXiv 2506.14028): 5 languages, **Hindi not listed**. GPT-4o 46.01%, with sharp multilingual drops. **Later**, reference only.
- **Synthesis [I].** There is no peer-reviewed Hindi or Hinglish *financial sentiment* benchmark with a usable licence. Follow the plan already in assistant-300ms-and-jev §3.3 (own golden set) and global-news-and-data §3:
  - build an in-house labelled set of Hindi, Hinglish and English Indian finance headlines and queries;
  - have two annotators with at least 20% overlap and κ ≥ 0.6;
  - report per-language macro-F1 with bootstrap CIs.
  - [P] Minimum size: about 385 items per language × polarity stratum for ±5 pp (worst-case p = 0.5), consistent with papers.md §(b).

**2.6 Indian news-to-returns (summary).**
- The credible evidence is contemporaneous and short-lived: Chari et al. 2023, plus the accuracy §2.3 items.
- No India study was found that shows a cost-adjusted, point-in-time, out-of-sample news-sentiment edge.
- **Verdict.** Sentiment is shown as a descriptive aggregate with its source, window and method (unchanged).

### Topic 3: Event detection and "why did it move"

**3.1 El Ghoul et al. (2022), international event-study methods.**
- *JIBS* 54(2):344–364, doi:10.1057/s41267-022-00534-6 ; PMC https://pmc.ncbi.nlm.nih.gov/articles/PMC9264305/ (H).
- **Recommendations:**
  - Choose the benchmark by market integration, with a "mild segmentation" local-plus-global model for emerging markets.
  - Use Dimson lead/lag betas for non-synchronous trading.
  - Use bootstrap tests alongside asymptotic ones.
  - Account for cross-sectional correlation from clustered events.
  - Screen out low-priced stocks.
- **Verdict: MVP.** It sets the India detector spec additions in §4.

**3.2 Grounded 8-K event extraction (Dolphin et al., arXiv 2607.08346).**
- https://arxiv.org/abs/2607.08346 (H).
- **Data.** 292,984 8-Ks from 2022–2026; 119-type, three-tier taxonomy; 601,088 tags released under CC BY 4.0 per the abstract. The repo licence is [U].
- **Method.** Two stages:
  1. A constrained taxonomy plus fuzzy n-gram quote anchoring.
  2. A second pass re-judges each quote against the category definitions.
- **Findings.**
  - Precision runs from 12% to 96% across quality-score bins. Unsupported tags fall from 8% to about 0 at high scores.
  - SEC item codes are too coarse on their own.
  - Evaluation is by an LLM judge on 5,125 tags, so it is not human-gold.
- **Verdict.**
  - **MVP** for the US leg: adopt the *pattern*, i.e. constrained taxonomy, quote-anchored spans, and a second-pass verifier with an abstention threshold.
  - **Later**: an analogous taxonomy for SEBI Reg 30 Schedule III event categories on NSE/BSE announcements. No India equivalent exists (absence finding).

**3.3 DelistBench** (arXiv https://arxiv.org/abs/2608.22770, H).
- Search-enabled LLMs rebuild delisting records.
- Best joint accuracy is 81.5% within ±7 days; 27.3% of records still go to human review.
- **Verdict.** Later, as a warning: LLM-populated corporate-action ledgers need human review queues. Our ledger comes from exchange files, not from LLMs (invariant 3).

**3.4 Faithfulness and claim-verification benchmarks.**
- **FinDVer** (EMNLP 2024; https://aclanthology.org/2024.emnlp-main.818/, H).
  - Explainable claim verification over long, hybrid filings, with long-context and RAG settings; 25 LLMs evaluated per a search summary.
  - GPT-4o lags human experts.
  - Size conflict: 2,400 (arXiv abstract) vs 4,000 (search snippet).
  - **MVP** as an eval-design reference: claim-level verdicts plus explanations.
- **Fin-Fact** (WWW 2025 Companion, doi:10.1145/3701716.3715292; arXiv 2309.08793, H).
  - 3,369 claims with truth labels, ruling statements and evidence.
  - The claims are fact-checker style (PolitiFact-like), not market-move explanations.
  - **Later.**
- **FinGround** (ACC ACL 2026 Industry; arXiv https://arxiv.org/abs/2604.23588, H).
  - Pipeline: hybrid text-and-table retrieval, then atomic claims routed by type (including formula reconstruction), then citation-grounded rewriting.
  - Results: −68% hallucination vs the strongest baseline at equal retrieval; an 8B distilled detector reaches F1 91.4% at 18× lower latency.
  - It notes that existing detectors miss 43% of computational errors.
  - **MVP** for verifier design. It matches our "numbers from the engine; verify every numeral" rule.
- **Gap (confirms papers.md §12).** No benchmark tests:
  - (i) abstention on no-news moves;
  - (ii) whether cited evidence was published before or after the move started;
  - (iii) co-occurrence vs causation phrasing.
- The in-house gold set in papers.md §(b) remains required. **Add India strata:**
  - band-hit days;
  - after-close deal disclosures;
  - FII/DII provisional-flow days;
  - results announced during market hours vs after the close;
  - Hindi/Hinglish user queries.

### Topic 4: Retrieval-augmented financial QA and hallucination

- **Kang & Liu (2023)** (https://arxiv.org/abs/2311.15548, H).
  - Historical-price queries: zero-shot Llama-2 gets 0% (MAE about $6.4k); GPT-3.5 and GPT-4 abstain.
  - RAG did not fix it.
  - Prompted tool calls reach 76–100%; one-shot tool learning gives 100%.
  - **MVP.** This is the cleanest evidence for invariant 5. Prices and indicator values are tool outputs rendered by templates, never generated.
- **DocFinQA** (ACL 2024 short, https://aclanthology.org/2024.acl-short.42/, M).
  - 7,437 questions over full filings averaging about 123k words.
  - The best evaluated model was GPT-3.5 at 42.6%; the retrieval setting of that figure was not read [U].
  - Retrieval-free GPT-4 scored about half of non-expert human performance; retrieval-assisted GPT-4 is about equal to non-expert humans.
  - **Later.**
- **SEC-QA** (FinNLP 2025, https://aclanthology.org/2025.finnlp-2.15/, M).
  - A multi-document QA *generator* that can be refreshed on documents newer than the model cutoff. RAG "systematically fails" on multi-document questions.
  - **The refresh idea is MVP** for our India eval: generate QA from each new quarter's NSE/BSE filings, so the eval stays post-cutoff and contamination-free.
- **Fin-RATE** (KDD 2026, https://arxiv.org/abs/2602.07294, H).
  - 17 LLMs. Accuracy falls 18.60% on longitudinal tracking and 14.35% on cross-entity tasks, together with temporal-mismatch and entity-confusion hallucinations.
  - **MVP.** Add "as-of quarter" and "which entity" axes to our eval.
- **Finance Agent Benchmark (Vals)** (https://arxiv.org/abs/2508.00828, H).
  - 537 questions; the best agent (o3) scores 46.8% at $3.79 per query; 10 models scored 0 on Trends.
  - **Later.** It also shows that agentic search does not fit the 300 ms budget.
- **Financial Touchstone** (Spörer, ACC FinLLM@IJCAI 2026, https://arxiv.org/abs/2608.08634, H).
  - 20 models; best 88.4% (Claude Opus 4.6).
  - The lowest hallucination rate is 0.08% (Gemini 2.5 Pro). That exact figure is also reported for "refusals", so the metric definition is [U].
  - **Retrieval is 48.9% of failures.**
  - **MVP** (retrieval-first engineering).
- **FAITH** (ACC ICAIF'25, https://arxiv.org/abs/2508.05201, H).
  - Masked-span tabular hallucination over S&P 500 annual reports. Rates were not read.
  - **Later.** The masking method could generate India table-QA items from annual reports.
- **Point-in-time and temporal retrieval.**
  - **FinTMMBench** (ACC ACM MM 2025, https://arxiv.org/abs/2503.05185, H): temporal-aware multimodal RAG over NASDAQ-100 tables, news, prices and charts; "notable gaps remain". **Later.**
  - **Zhao & Welsch** (https://arxiv.org/abs/2605.31201, H): point-in-time RAG with a Bayesian source memory updated from *matured* residual returns. Macro-F1 0.438 → 0.471; Sharpe 0.52 → 0.84.
    - 89 stocks, one dataset, no costs stated, so it fails 06 §7.
    - **Later** for the design idea: "only matured feedback updates retrieval weights", which is a no-look-ahead pattern. **Not in plan** as a signal.
  - TempFinRAG (MDPI *Symmetry* 18(9)) and TimelyRAG (arXiv 2609.11572) were found but not read [U].
- **Addition to accuracy-indicators-algos §5 on arXiv 2607.11414 (not a correction).**
  - The abstract gives about 0.73–0.79 AUROC for financial reasoning errors overall; that is the figure in the accuracy doc, and it is correct.
  - On the harder subset of *confident* answers (unanimous across 8 runs), the probe reaches 0.68–0.77, vs 0.55–0.63 for the baselines.
  - Within that subset, 5–19% of answers are wrong: Llama-3.1-8B 5%, Gemma-2-9B 14%, Qwen3-8B 19% [V, H].
  - Implication: self-consistency is not a safe confidence gate for small models.

### Topic 5: Technical indicators' empirical value in India

- **Multi-market, data-snooping-controlled studies.**
  - **Heyman, Inghelbrecht & Pauwels (2012)**, SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1998036 (M).
    - 34 emerging markets; White's Reality Check plus Hansen SPA, with costs.
    - Technical rules do not consistently beat buy-and-hold; they are significant in 4/34 markets and more profitable in crises.
    - **India's inclusion and the identity of the 4 markets are [U]**: the full text was not fetchable.
  - **Rink (2023)**, *FMPM* 37(4):403–456; RePEc https://ideas.repec.org/a/kap/fmktpm/v37y2023i4d10.1007_s11408-023-00433-2.html (H for the abstract).
    - 23 developed and 18 emerging indices, 6,406 rules, up to 66 years, with an SPA-type test.
    - In-sample outperformance is common, especially in emerging markets. But predictability "diminishes drastically over time", is "very sensitive to … moderate transaction costs", and is "not persistent" out of sample.
    - **India's inclusion is [U].**
  - **Sermpinis et al.**, arXiv 1811.06766 (M): 21k rules on 12 MSCI indices, 2004–2015, discrete FDR. "Short-term value" with frequent rebalancing; weak persistence. The published venue is [U].
- **India-only studies.** Neither has data-snooping control, so both fail 06 §7:
  - **Muruganandan (2020)**, *Colombo Business Journal* 11(1):24–46, doi:10.4038/cbj.v11i1.56 (H). Sensex, 2000–2018, RSI/MACD. No WRC/SPA. The MACD sell signal is conditionally better in bear markets but not after risk; RSI failed.
  - **IMFI 2023**, https://businessperspectives.org/journals/investment-management-and-financial-innovations/issue-430/the-effectiveness-of-technical-trading-strategies-evidence-from-indian-equity-markets (M). 14 Nifty stocks, hourly, **Jan–Aug 2022 (8 months)**. The SMA rule was net-profitable for 8/14 stocks and beat buy-and-hold for 6/14.
    - It has no data-snooping control, a tiny sample and one regime.
    - **This is the canonical example of what fails 06 §7.** An 8-month Sharpe has a standard error of about √(1/0.67) ≈ 1.2 even at SR = 0.
- **Answer to "what do they find for NIFTY stocks" [I].**
  - No study was found that tests technical rules on NIFTY constituents with a point-in-time universe, WRC/SPA/StepM or FDR control, realistic Indian costs (STT, stamp duty, exchange fees, GST, slippage), and walk-forward validation.
  - The best available multi-market evidence says in-sample gains in emerging markets are not persistent and do not survive moderate costs.
  - This is an absence finding; see §5 for the searches.
- **Verdict.** Indicators stay descriptive (spec-versioned values, accuracy-indicators-algos §1.3). Any future "setup" or backtest feature must use SPA/StepM or DSR/PBO with the full rule universe logged.

### Topic 6: AI tools in retail investing (regulators and academia)

- **IOSCO.**
  - Consultation report "AI in Capital Markets: Use Cases, Risks, and Challenges", Mar 2025: https://www.iosco.org/library/pubdocs/pdf/IOSCOPD788.pdf (M). Use cases: client communications 66.7%, algorithmic trading 63.3%, robo-advice 60%. Top concern: cybersecurity (4.26/5).
  - Final "Supervisory Toolkit for AI Use in Capital Markets", FR/02/2026, 25 May 2026: https://www.iosco.org/library/pubdocs/pdf/IOSCOPD823.pdf (M). Non-binding supervisory tools.
  - Final reports on **finfluencers, online imitative trading and digital engagement practices**, 19 May 2025: https://www.iosco.org/news/pdf/IOSCONEWS768.pdf (fetch 403; M via A&O Shearman https://finreg.aoshearman.com/IOSCO-publishes-final-reports-on-finfluencers-onl). The reports warn about unregistered advice, conflicts, and DEPs that push more frequent, riskier trading.
  - **MVP implications for UX:**
    - no streaks, confetti or leaderboards;
    - no "trending buys";
    - no copy/imitative features.
- **ESMA.**
  - Public statement on AI and investment services, 30 May 2024: https://www.esma.europa.eu/sites/default/files/2024-05/ESMA35-335435667-5924__Public_Statement_on_AI_and_investment_services.pdf. Firms must disclose AI use in client interactions and remain responsible under MiFID II (existence H; content M).
  - Investor warning "on the use of AI for investing" with NCAs, Mar 2025: https://www.esma.europa.eu/document/warning-use-ai-investing (existence H; the wording was not read).
  - **MVP:** an AI-use disclosure on every narrative.
- **FCA Mills Review.**
  - Engagement paper 27 Jan 2026; final report 6 Jul 2026. https://www.fca.org.uk/publications/calls-input/review-long-term-impact-ai-retail-financial-services-mills-review (M).
  - The 28m UK adults figure is attributed to Lloyds, not the FCA.
  - **The final report was not read [U].** Later.
- **SEC.** The predictive-data-analytics conflicts proposal (S7-12-23) was withdrawn on 12 Jun 2025: https://www.sec.gov/rules-regulations/2025/06/s7-12-23 (H for existence). There is no US PDA-specific rule. FINRA 2210 still governs projections (finance-models-evidence §5).
- **SEBI.** The 20 Jun 2025 AI/ML consultation is already covered. No final circular was found as of 2026-09-24 [U].
- **Academic.**
  - **D'Acunto, Prabhala & Rossi (RFS 2019)**, https://academic.oup.com/rfs/article/32/5/1983/5427774 (H for the citation).
    - It uses **Indian** brokerage data (Indian equities, Apr 2015–Jan 2017). This comes from the CFA Digest summary, https://rpc.cfainstitute.org/research/cfa-digest/2019/09/dig-v49-n9-1, so the India setting is M; the OUP page did not render the abstract.
    - The paper is pre-2020.
    - The robo-adviser helped under-diversified investors (fewer than 5 stocks).
    - Investors with more than 10 stocks traded more, with no performance gain.
    - Biases were reduced but not removed.
    - *Lesson:* tools raise attention and trading. An information product can raise turnover, which the SEBI studies show is harmful at retail.
    - **MVP design constraint:** don't optimise for session count or trades.
  - **Kakhbod et al., "Finfluencers"**, SSRN 4428232 (M). 56% of finfluencers are antiskilled (−2.3%/month); they get more engagement and followers.
    - **MVP:** no social-media "buzz" signal shown as a quality or return indicator.
  - **Lalwani (Economics Letters 2025)**, doi:10.1016/j.econlet.2025.112511 (M). Indian YouTube finfluencers recommend past winners and high-volume stocks, and recommendation frequency *predicts higher* future returns.
    - This conflicts with Kakhbod in direction, but the settings differ: an aggregate frequency measure vs individual skill.
    - Magnitude, costs and horizon were not read.
    - **Later**, research only. Surfacing it as a signal would run into SEBI finfluencer rules.
  - **Cheng, Lin & Zhao (JAE 2025)** (M): ChatGPT outages cut trading volume, especially around fresh news; GenAI improves long-run price informativeness.
  - **Even-Tov et al. (SSRN 2025)** (M): the Italy ban led to fewer assets traded and a shift to popular assets.
  - Together these show retail investors *do* act on GenAI output. That raises the stakes of explanation errors.
  - **Choukhmane et al. (arXiv 2608.01607)** (H, abstract): GPT-5.2 advice follows life-cycle norms but varies by gender, about 2/3 via prompt wording. **Later:** a fairness probe for narrative phrasing across demographically varied prompts.
  - **FINRA Foundation (2024)** (M): only 5% would use AI for a financial decision, but trust in the same statement was equal for AI and for humans (34% vs 33%). **Later:** trust calibration means labels must carry the weight, not tone.
- **Also found, not read [U]:**
  - "Finfluencers on TikTok" (arXiv 2607.05203);
  - "UK Finfluencers" (arXiv 2505.01941);
  - an Indian finfluencer registration study reporting "33% give stock tips, 6% SEBI-registered" (Business Standard, Jul 2026). Its publisher is unattributed.

---

## 3. What this changes in our plan

These are proposals [P] for the owners of 06, 13 and 15, and for data-engineer, realtime-engineer and financial-correctness-reviewer.

1. **Event taxonomy (India).** Add first-class, time-stamped event types:
   - PIT/SAST insider trades;
   - promoter pledge creation and release;
   - bulk and block deals;
   - results (with a during-hours / after-close flag);
   - Reg 30 Schedule III categories;
   - SEBI orders, with a **low default catalyst prior** (1.7).

   Timestamps are exchange dissemination time (NSE/BSE announcement feed), **not** media time. The cyber-incident study (1.11) shows how media dates blur event timing.
2. **Timing states in the explanation card** (invariant 6). Each cited item gets one of:
   - `before_move`;
   - `after_move_start` ("published after move began");
   - `after_close_disclosure`, for bulk/block deals and FII/DII provisional flows.

   Pre-announcement drift (1.8) and front-running (1.5) make `after_move_start` common. The gold set must oversample these cases.
3. **Wording rules.**
   - For flows and deals: "coincided with", never "because of" (1.9).
   - SEBI loss statistics must cite the study, the year and the broker coverage. Never blend "93% over FY22–24" with the per-year 91%.
4. **Detector spec additions for India** (06; 3.1). See §4 for formulas:
   - Dimson-adjusted beta for thin trading;
   - a local benchmark (Nifty 500 or a sector index), with a global factor only for the US leg;
   - a **band-censoring flag**: when a stock closes at its band, its AR is a *lower bound*, and no standardised score is shown as exact;
   - thresholds from empirical per-stock quantiles, not Gaussian tables.
5. **Evaluation harness.**
   - Add Fin-RATE-style axes (as-of quarter; entity) and SEC-QA-style **quarterly refresh** of India QA from new filings, which keeps the eval post-cutoff.
   - Add FinGround-style atomic-claim routing, with formula reconstruction for derived numbers.
   - Add a Hindi/Hinglish stratum. There is no external benchmark, so label our own.
   - Treat IndiaFinBench and FinVQA as secondary, licence-pending.
6. **Datasets.**
   - SEntFiN: internal eval only, pending licence.
   - "NIFTY" (US): exclude.
   - CODS "SentiFin": exclude until its provenance is known.
   - Every dataset record needs three fields: annotation licence, source-text rights, commercial use.
7. **Numbers path.** Kang & Liu plus Financial Touchstone confirm tool-first, retrieval-first design. No LLM ever emits a price, return, flow or indicator value. This is unchanged but now better evidenced.
8. **Indicators.** Remain descriptive; no "signal", "setup" or win-rate. Any future backtest feature must log the full rule universe and pass SPA/StepM plus DSR/PBO (06 §7).
9. **Retail-harm UX constraints** (IOSCO DEPs; D'Acunto et al.; SEBI studies):
   - no engagement mechanics;
   - no trending-buy lists;
   - no social-buzz scores;
   - an AI-use disclosure (ESMA 2024);
   - a dated SEBI risk line on F&O and intraday cards;
   - metrics for trades or sessions per user are **not** product KPIs.

---

## 4. Formulas and a hand-computed fixture (for financial-correctness-reviewer)

**Market-model abnormal return with a Dimson thin-trading adjustment** [P, following MacKinlay 1997 and El Ghoul et al. 2022]:
- **Session calendar.** Estimation window: trading days [τ₀−250, τ₀−21], ending 20 sessions before the event day τ₀.
  - Sessions come from the NSE/BSE holiday circulars.
  - `exchange_calendars` is reported to ship XBOM but **no XNSE calendar** (search summary, M). XBOM/XNSE holiday parity and ad-hoc closures are [U], per accuracy-indicators-algos §7 item 16.
  - Do not hard-code "XNSE" until this is confirmed.
- Exclude past results days, band-hit days and ex-dates (under the price-return basis) from the estimation window.
- Regress R_i,t = α + Σ_{k=−1..+1} β_k R_m,t+k + ε_t. Set β_D = β₋₁ + β₀ + β₊₁ and α̂ = the intercept. σ̂ is the residual standard deviation.
- Abnormal return: AR_i,t = R_i,t − (α̂ + β_D·R_m,t).
- **Return basis: both legs must be on the same basis.**
  - *Preferred:* total return for both. The stock TR comes from raw closes plus the versioned corporate-action table (invariant 3); R_m is the Nifty 500 TRI.
  - *Fallback,* if the TRI is not licensed: price return for both. The stock return is split/bonus-adjusted and dividend-unadjusted; R_m is the Nifty 500 price index. Flag ex-dates in the event window, and exclude them from estimation.
  - Mixing a stock price return with an index TR creates a spurious AR of about −D/P on ex-dates and biases α̂ by the dividend-yield gap. The spec records `return_basis ∈ {TR, PR}` on every output.
- Returns are close-to-close on the **official close**. The CAS close applies for Category I stocks from 3 Aug 2026 (accuracy §1.2).
- CAR(τ₁, τ₂) = Σ AR_t. Standardised: SCAR = CAR / (σ̂ · √L), where L = τ₂ − τ₁ + 1.
- **Band-hit flag.** Set `censored = true` if |close/prev_close − 1| is within one tick of the **band in force at the close on day t, after any intraday flex**.
  - F&O stocks have a dynamic band that is relaxed in 5% steps (accuracy §1.2). Non-F&O stocks have their static band, which is point-in-time per stock.
  - A static lookup would wrongly flag an F&O stock that closes at +10% after flexing to 15%, and would miss one pinned at 15%.
  - The true unconstrained AR is ≥ the observed AR for an upper hit (≤ for a lower hit).
- **Threshold.** The alert fires when |SCAR| exceeds the empirical 1 − q quantile of the stock's own historical |SCAR| distribution (block bootstrap), with q set for the target false-alert rate per watchlist-day. **No Gaussian p-values.**
- **What it does not claim.** No causal attribution and no prediction of subsequent returns.

**Fixture E1 (hand-computed)** [P]:
- Inputs: α̂ = 0.0005, β_D = 1.2, σ̂ = 0.02, band in force at the day-1 close = 10% (non-F&O stock), return basis PR for both legs, no ex-date in the window.
- Days 0–2: R = [0.020, 0.100, −0.010]; R_m = [0.005, 0.010, −0.002].
- Day 1 closes exactly at +10% (band hit).
- Expected values:
  - AR₀ = 0.020 − (0.0005 + 0.0060) = **0.0135**.
  - AR₁ = 0.100 − (0.0005 + 0.0120) = **0.0875**, with `censored = true` (lower bound).
  - AR₂ = −0.010 − (0.0005 − 0.0024) = **−0.0081**.
  - CAR(0,2) = **0.0929**. SCAR = 0.0929 / (0.02 × √3) = 0.0929 / 0.034641 = **2.6818**. The output must carry `censored = true`, since the CAR is a lower bound.
- **E1b (band flex).** Same inputs, but the stock is F&O and its dynamic band was flexed to 15% intraday on day 1.
  - Day 1 closes at +10%, which is not at the 15% band in force at the close, so `censored = false`.
  - The AR/CAR/SCAR values are unchanged (0.0135, 0.0875, −0.0081; CAR 0.0929; SCAR 2.6818).
- **E1c (ex-date basis check).** Fallback PR basis. Stock close 100 → 98 on an ex-date with a ₹2 dividend; R_m = 0; α̂ = 0.
  - PR stock return = −0.0200, so AR = −0.0200. This is an artefact, so the output must carry `ex_date = true`.
  - Under the TR basis, stock TR = (98 + 2)/100 − 1 = 0, so AR = 0 (with the index TRI R_m = 0).
- Property test: when any day in the window is censored, the UI never shows the SCAR without the censoring label.

---

## 5. Absence findings: searches run on 2026-09-24

| Gap | Search strings used (web search) | Result |
|---|---|---|
| NSE price-band or circuit effects (magnet, delayed discovery) | "price limits circuit breakers India magnet effect individual stock price bands NSE study"; "XKDR working paper price bands circuit filters India"; "'price limits' India stocks volatility spillover delayed price discovery NSE" | Only China and Taiwan studies, plus NSE/SEBI circulars. No peer-reviewed NSE study found |
| Reg 30 LODR disclosure event studies | "event study corporate announcements NSE abnormal returns SEBI LODR"; "'stock market reaction' India 'Regulation 30' OR 'material events' disclosure event study" | Only compliance commentary (KPMG, law firms). No event study using exchange timestamps |
| Results timing combined with FII/DII flows | "earnings announcement returns India intraday 'results announcement' market hours after close timing NSE" | Old PEAD papers only. The NSE-IGIDR WP on insider trading and earnings timed out on fetch |
| Hindi/Hinglish *financial* sentiment benchmark | "Hindi financial news sentiment dataset"; "code-mixed Hinglish financial sentiment analysis dataset stock tweets"; "multilingual Indian languages financial sentiment benchmark" | One small Hindi-tweet chapter, general-domain Hinglish corpora, and Indic financial QA (FinVQA). No sentiment benchmark |
| Snooping-corrected, cost-adjusted TA on NIFTY stocks | "technical trading rules India data snooping White reality check superior predictive ability Hansen NIFTY"; "technical analysis profitability emerging markets false discovery rate transaction costs India" | Multi-market studies (India inclusion unverified) and India-only studies without correction |
| "Why did it move" explanation-faithfulness benchmark | "'why did the stock move' LLM explanation benchmark stock movement attribution news faithfulness" | None. Confirms papers.md §12 |

These are absence findings from search, not proof of non-existence. Confidence M.

---

## 6. Conflicts recorded, not resolved

1. **SEBI F&O.** "93% (FY22–24)" is three-year cumulative; the per-year figures are 90.2–91.7% (FY25 PDF). Broker coverage differs across studies: top-10, then top-13, then top-15.
2. **SEBI intraday participation growth.** "4.6× (15 → 69 lakh)" vs "threefold". Both come from secondary sources.
3. **SEBI press-release numbers.** The fetch returned "37/2024" for both the Jul 2024 and Sep 2024 releases. Do not cite PR numbers.
4. **FinDVer size.** 2,400 (arXiv abstract) vs 4,000 (search snippet).
5. **arXiv 2607.11414 AUROC. Resolved; not a conflict.** 0.73–0.79 is the overall figure and 0.68–0.77 is the confident-answer subset. Both are from the abstract. Always quote the two together with their subsets.
6. **SentiFin vs SEntFiN.** 10,572, 8,000 and "2024–2025" (CODS summaries) vs 10,753 and 2002–2017 (SEntFiN). Possibly the same corpus, or an extension of it.
7. **Finfluencer skill.** Kakhbod et al. find a majority antiskilled (US, individual level); Lalwani finds that aggregate recommendation frequency predicts higher returns (India). The two measures differ.
8. **Financial Touchstone "0.08%".** Reported both as Gemini's hallucination rate and as the Chinese models' refusal rate. The metric definition needs checking.

---

## 7. Unverified list

- The Aziz (2026) sample period, N, benchmark model and CAAR standard errors (Springer blocked).
- The Chaturvedula et al. (2015) method details and N (ScienceDirect 403). The 7.49% comes from the abstract via search.
- The Sehgal & Bijoy (2015) volume, issue and pages; handling of announcement timing.
- Whether India is in Heyman et al. (34 markets), Rink (18 emerging) and Sermpinis et al. (12 MSCI); which 4 markets were significant in Heyman et al.; the published venue of Sermpinis et al.
- Dataset licences: SEntFiN (data), IndiaFinBench (the repo URL returned 404), FinVQA, the 8-K event tags repository, and the Hindi stock-tweet dataset. Source-text rights for every headline corpus.
- The provenance of CODS "SentiFin" and its link to SEntFiN.
- The Chari et al. (2023) news source, period and coefficients (MDPI 403).
- The SEBI Aug 2026 study figures beyond those in accuracy §2.1 (secondary only; PDF not read).
- The SEBI intraday study details beyond the 71% headline.
- IOSCO report contents (PDF fetches 403 or not attempted); ESMA Mar 2025 warning wording; the **FCA Mills final report (6 Jul 2026)**, not read.
- Whether SEBI issued final AI/ML guidelines after the Jun 2025 consultation.
- The Lalwani (2025) magnitude, horizon and cost treatment; Kakhbod et al. publication status beyond SSRN.
- The Even-Tov et al. and Cheng et al. effect sizes (403).
- The "33% of finfluencers give tips, 6% SEBI-registered" study's publisher and method.
- The Aggarwal et al. (2025) underlying paper on SEBI enforcement CARs (only the LEAP blog summary was read).
- The NSE-IGIDR WP "An Analysis of Corporate Insider Trading and Earnings Announcements in India" (fetch timed out).
- The TempFinRAG and TimelyRAG contents.
- Whether `exchange_calendars` ships an XNSE calendar. A search summary says it has XBOM only; this needs checking against the package source.
- The India setting of D'Acunto et al. (2019): the CFA Digest summary says it is India; the paper's own abstract was not rendered.
- The DocFinQA retrieval setting of the 42.6% figure.
- Venue acceptances marked ACC (CODS 2025, ACL 2026 Industry, KDD 2026, FinLLM@IJCAI 2026, ICAIF'25, ACM MM 2025) were taken from arXiv comments and not checked on the venue sites.

## 8. Open methodological risks (hand-off)

- **To data-engineer.**
  - Exchange dissemination timestamps for announcements, deals and PIT/SAST disclosures (not media time).
  - A point-in-time pledge and shareholding history.
  - Band-applicability history per stock, because bands change over time and apply differently to F&O vs non-F&O stocks.
  - FII/DII provisional vs final flow versions.
- **To realtime-engineer.**
  - The band-hit censoring flag in the detector.
  - The `after_close_disclosure` timing state.
  - Empirical-quantile threshold tables refreshed on a fixed schedule, not on demand.
- **To financial-correctness-reviewer.**
  - Fixture E1.
  - The Dimson estimation spec.
  - The wording rules in §3 item 3.
  - Checking that no SEBI statistic is quoted without study, year and broker coverage.
