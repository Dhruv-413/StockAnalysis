# Research Review: Explainable Watchlist Alerts, LLM Grounding, and Backtesting Evidence Standards

Research date / access date for every URL: **2026-09-24**
Reviewer role: quantitative finance research reviewer. Product context: near-real-time US equity/ETF watchlist monitoring. It detects abnormal price and volume moves deterministically, attaches cited evidence (news, 8-K and other SEC filings, earnings dates), and may add an LLM summary grounded only in the retrieved sources. A backtesting module may come later.

Confidence legend:
- **High**: bibliographic facts confirmed on the publisher, arXiv, ACL Anthology, NBER, SSRN or RePEc page.
- **Medium**: taken from a search snippet or from an automated extraction of a PDF body, and not checked line by line.
- **Unverified**: could not be confirmed. This is stated inline.

Verdict key:
- **MVP**: directly shapes the first release.
- **Later**: belongs to a later experiment or to the backtesting module.
- **Not in plan**: should not be built or relied on.

---

## Summary table

| # | Work | Venue / year | Verdict |
|---|------|--------------|---------|
| 1 | Lopez-Lira & Tang, LLM return predictability | arXiv/SSRN 2023–2025; reported forthcoming in JFE (unconfirmed) | Not in plan (as a signal); Later (research only) |
| 2 | Glasserman & Lin, look-ahead vs distraction | arXiv/SSRN 2023 | MVP (design principle); Later (method) |
| 3a | Sarkar & Vafa, lookahead bias in LMs | SSRN 2024; ICML 2025 workshop (DIG-BUGS) | MVP (principle) |
| 3b | He, Lv, Manela & Wu, ChronoBERT/ChronoGPT | arXiv/SSRN 2025 | Later |
| 3c | Drinkall et al., Time Machine GPT | Findings of NAACL 2024 | Later |
| 3d | Gao, Jiang & Yan, Lookahead Propensity test | arXiv/SSRN 2025 | Later |
| 3e | Yan et al., DatedGPT; Kelly et al., Scaling PiT LMs; Benhenda, Look-Ahead-Bench | arXiv 2026 | Later |
| 4 | FinanceBench (Islam et al.) | arXiv 2023 | MVP (as an eval warning and template) |
| 5 | BloombergGPT; FinGPT | arXiv 2023 | Not in plan |
| 6 | TradingAgents (Xiao et al.) | arXiv 2024 (v7 2025) | Not in plan |
| 7 | Deflated Sharpe Ratio; Probability of Backtest Overfitting | JPM 2014; J. Comp. Finance 2017 | Later (required for backtesting) |
| 8 | Harvey, Liu & Zhu, multiple testing | RFS 2016 | MVP (alert thresholds); Later (strategies) |
| 9 | MacKinlay 1997; Brown & Warner 1985 | JEL 1997; JFE 1985 | MVP (core method) |
| 10 | Boudoukh et al. 2019/2013; Tetlock 2007; Roll 1988; Cutler, Poterba & Summers 1989; Jeon et al. 2022 | RFS, JF, JPM, JFE | MVP (sets expectations: many moves have no news) |
| 11 | ALCE; RAGAS; AIS; FActScore | EMNLP 2023; EACL 2024 demo; CL 2023; EMNLP 2023 | MVP (evaluation of explanations) |
| 12 | FinBen, StockBench, LiveTradeBench, INVESTORBENCH, FinSearchComp, Ploutos, Beyond the Reported Cutoff, Nguyen & Pham 2026 | 2024–2026 | Mixed (see below) |
| 13 | Shumway 1997; Novy-Marx & Velikov 2016; Frazzini, Israel & Moskowitz 2018; Almgren & Chriss 2000 | JF, RFS, SSRN, J. Risk | Later (backtesting) |
| 14 | Kronos (Shi et al.); Rahimikia et al.; Noguer i Alonso & Franklin; Brini; MarS; FinVerse; FinGPT / Fin-R1 / Palmyra-Fin | AAAI 2026; arXiv 2025–2026; ICLR 2025 | Kronos: Later (volatility challenger only), never user-facing. Others: evidence inputs (see §14) |

---

## 1. Lopez-Lira & Tang: "Can ChatGPT Forecast Stock Price Movements? Return Predictability and Large Language Models"

- **Citation**: Alejandro Lopez-Lira and Yuehua Tang (University of Florida). arXiv:2304.07619, first submitted 2023-04-15. arXiv lists v6 on 2025-10-28. The HTML/PDF rendering I fetched showed a header reading "This Version: August 24, 2026". I did not resolve this conflict, so both dates are reported. The paper is also SSRN 4412788, which returned HTTP 403 when fetched.
- **Venue**: A search snippet reports it as *forthcoming in the Journal of Financial Economics*. The paper's acknowledgments thank "Dimitris Papanikolaou (the editor)". **The publication status is reported but not confirmed on a publisher page. Confidence: medium.**
- **URLs**: https://arxiv.org/abs/2304.07619 ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4412788
- **Problem**: Can general-purpose LLMs, without financial fine-tuning, turn news headlines into signals that predict returns?
- **Claimed contribution**: GPT-4 scores capture the initial market reaction. The abstract reports about 90% portfolio-day hit rates for that non-tradable initial reaction. The scores also predict the subsequent drift, more strongly for small stocks and negative news. Predictive ability rises with model size. Returns to the strategy fall as LLM adoption rises, which is consistent with prices becoming more efficient.
- **Data and evaluation (from an automated PDF extraction, medium confidence)**:
  - Sample runs from October 2021 to May 2024, after the September 2021 cutoff of the GPT-4 snapshot used. This is the paper's control for look-ahead bias.
  - Data sources are CRSP, RavenPack-matched headlines, and TAQ.
  - About 159k firm-headline observations across about 4.1k stocks.
  - The long-short strategy survives about 5 bp round-trip costs, degrades sharply at 10 bp, and is unprofitable at about 20 bp.
- **Reproducibility**: No code or data release was found. RavenPack, CRSP and TAQ are licensed. Closed-model snapshots may be deprecated.
- **Limitations**:
  - The headline 90% figure refers to the *non-tradable* initial reaction.
  - The tradable drift is concentrated in small stocks and negative news, where costs and short-sale constraints are highest.
  - Profits are fragile to costs.
  - Alpha decays as adoption rises.
- **Relevance**: This paper shows that LLMs read the *direction* of news well. It supports using an LLM to *classify and label* retrieved headlines in an alert. It does **not** support selling LLM sentiment as a forecast.
- **Verdict**: **Not in plan** as a predictive signal. **Later experiment** only as an internal research replication under the evidence standards in section (a).

## 2. Glasserman & Lin: "Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis"

- **Citation**: Paul Glasserman and Caden Lin. arXiv:2309.17322, 2023-09-29. SSRN 4586726 (doi:10.2139/ssrn.4586726). Working paper; no journal venue confirmed. Confidence: high.
- **URLs**: https://arxiv.org/abs/2309.17322 ; https://dx.doi.org/10.2139/ssrn.4586726
- **Problem**: LLM training periods overlap with backtest periods. The paper separates two effects:
  - *Look-ahead bias*: the model knows what happened after the news.
  - *Distraction effect*: general knowledge about the named company interferes with the sentiment reading.
- **Contribution**: The authors anonymize company identifiers in headlines and compare strategy performance with and without anonymization. In sample, anonymized headlines performed *better*. The distraction effect outweighed look-ahead bias and was strongest for large firms. Out of sample, look-ahead bias stops mattering but the distraction effect remains. Anonymization is proposed as a debiasing tool.
- **Reproducibility**: The method is simple and replicable (entity masking). The news data are licensed. No code release was found.
- **Limitations**: It covers one model family and one task (headline sentiment). The sample period comes from the abstract only.
- **Relevance**: Two design rules for the MVP follow:
  1. Any LLM labeling of news should be tested with ticker and company-name masking.
  2. Evaluation of LLM explanations must be stratified by firm size, because large, well-known firms are where parametric knowledge leaks in.
- **Verdict**: **MVP** as a design principle for the evaluation harness. **Later** for replicating the method.

## 3. Lookahead bias in pretrained LMs and point-in-time ("time machine") models

All of the following were verified to exist.

**3a. Sarkar & Vafa, "Lookahead Bias in Pretrained Language Models"**
- SSRN 4754678 (dated 2024-06-28). Also presented at the ICML 2025 *workshop* DIG-BUGS; the icml.cc page lists it as a workshop paper. Confidence: high.
- URLs: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4754678 ; https://icml.cc/virtual/2025/51018 ; https://openreview.net/pdf?id=fn9cJkB86T
- Method: direct tests that assume some events are unpredictable from a prespecified information set.
- Finds lookahead bias in two applications: risk factors from earnings calls, and election winners from candidate biographies.
- Recommends models trained only on data from before the analysis period.
- Verdict: **MVP** as a principle. Any "backtest" of LLM outputs on pre-cutoff data is invalid by default.

**3b. He, Lv, Manela & Wu, "Chronologically Consistent Large Language Models" (ChronoBERT and ChronoGPT)**
- arXiv:2502.21206 (2025). SSRN 5159615. Confidence: high.
- URLs: https://arxiv.org/abs/2502.21206 ; https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5159615
- The models are trained only on text available at each point in time, with cutoffs starting in 1999.
- In an application predicting next-day returns from news, their real-time outputs give Sharpe ratios comparable to a much larger Llama model. The authors read this as "lookahead bias is modest" in that setting.
- Verdict: **Later**. Use these models if the product ever backtests LLM-derived signals.

**3c. Drinkall, Rahimikia, Pierrehumbert & Zohren, "Time Machine GPT" (TiMaGPT)**
- Findings of NAACL 2024. arXiv:2404.18543. Confidence: high.
- URLs: https://aclanthology.org/2024.findings-naacl.208/ ; https://arxiv.org/abs/2404.18543
- A series of point-in-time ("nonprognosticative") LLMs.
- Verdict: **Later**.

**3d. Gao, Jiang & Yan, "Detecting Lookahead Bias in LLM Forecasts"**
- Previously titled "A Test of Lookahead Bias in LLM Forecasts". arXiv:2512.23847. SSRN 5985277. Confidence: high.
- URLs: https://arxiv.org/abs/2512.23847 ; https://www.ssrn.com/abstract=5985277
- Introduces "Lookahead Propensity" (LAP), estimated from date-only recall queries. LAP is positive before the model's cutoff and near zero after it.
- The LLM's predictive power is amplified on high-LAP firm-date pairs.
- Verdict: **Later**. This is a cheap audit to run on any LLM-signal backtest.

**3e. 2026 point-in-time work (verified on arXiv)**
- **Yan, Tang, Gao, Jiang & Lu, "DatedGPT"** (arXiv:2603.11838). Twelve 1.3B-parameter models, one per annual cutoff from 2013 to 2024. https://arxiv.org/abs/2603.11838
- **Kelly, Malamud, Schwab & Xu, "Scaling Point-in-Time Language Models"** (arXiv:2607.11889; NBER w35247; SSRN 6681860). Up to 4B parameters trained on 1T chronologically filtered tokens, with monthly checkpoints 2013–2024. Code and models are released. https://arxiv.org/abs/2607.11889
- **Benhenda, "Look-Ahead-Bench"** (arXiv:2601.13770, 2026-01-20; code at https://github.com/benstaf/lookaheadbench). Single author, affiliated with a vendor of point-in-time models (PiT-Inference). Treat as a potential conflict of interest.
- Verdict for all three: **Later**.

## 4. FinanceBench (Islam et al., 2023)

- **Citation**: Pranab Islam, Anand Kannappan, Douwe Kiela, Rebecca Qian, Nino Scherrer and Bertie Vidgen (Patronus AI and others). arXiv:2311.11944, 2023-11-20. Preprint. Confidence: high.
- **URLs**: https://arxiv.org/abs/2311.11944 ; https://github.com/patronus-ai/financebench ; Hugging Face dataset PatronusAI/financebench
- **Problem**: Open-book question answering over public-company filings (10-K, 10-Q, 8-K, earnings reports).
- **Contribution**:
  - 10,231 questions with answers and evidence strings.
  - 16 model configurations evaluated on a 150-question sample, with 2,400 manually reviewed answers.
  - GPT-4-Turbo with a shared vector store "incorrectly answered or refused to answer 81% of questions."
  - Long context helps but is impractical because of latency and document length.
- **Reproducibility**: **Only the 150-case open-source sample is public** on GitHub and Hugging Face. The full 10,231-question set is not implied to be released.
- **Limitations**:
  - The results use 2023-era models and retrieval setups; current models are likely better.
  - The benchmark measures QA, not summarization.
  - The results depend heavily on the retrieval configuration.
- **Relevance**: Retrieval failure, not generation, is the dominant failure mode. For the MVP, citations must point to exact filing passages (8-K item plus text span). The system must verify that each claim is entailed by a cited span. FinanceBench's evidence-string format is a good template for an in-house eval set.
- **Verdict**: **MVP**, as an evaluation template and a risk warning.

## 5. BloombergGPT and FinGPT

- **BloombergGPT**: Shijie Wu et al. (Bloomberg). arXiv:2303.17564 (2023; v3 2023-12-21). Confidence: high. https://arxiv.org/abs/2303.17564
  - A 50B-parameter model trained on 363B tokens of financial data (FinPile) plus 345B general tokens.
  - Weights and data are proprietary and not released.
  - Its training corpus spans the periods any backtest would use, so it has look-ahead exposure.
- **FinGPT**: Hongyang Yang, Xiao-Yang Liu and Christina Dan Wang. arXiv:2306.06031 (2023-06-09). Confidence: high. https://arxiv.org/abs/2306.06031 ; code at github.com/AI4Finance-Foundation/FinGPT
  - An open-source, data-centric pipeline with LoRA fine-tuning.
  - It is a framework and vision paper, not a rigorous evaluation.
- **Relevance**: The product's LLM job is narrow: summarize retrieved sources with citations. General frontier models plus retrieval are the practical choice. Later benchmarks (FinBen, StockBench, "Beyond the Reported Cutoff") show that domain pretraining does not automatically bring reasoning or trading gains.
- **Verdict**: **Not in plan**.

## 6. TradingAgents (Xiao et al., 2024)

- **Citation**: Yijia Xiao, Edward Sun, Di Luo and Wei Wang. arXiv:2412.20138 (submitted December 2024; v7 2025-06-03). Preprint; no peer-reviewed venue confirmed. Confidence: high. Code: https://github.com/TauricResearch/TradingAgents
- **URL**: https://arxiv.org/abs/2412.20138
- **Problem and contribution**: A multi-agent LLM "trading firm" with fundamental, sentiment, news and technical analysts, bull and bear researchers, a trader, and a risk team. It reports better cumulative return, Sharpe ratio and max drawdown than rule-based baselines.
- **Evaluation setup** (from an automated extraction of the arXiv HTML; the figures are **medium confidence**):
  - Backtest window **2024-01-01 to 2024-03-29, about 3 months**.
  - Headline results are for **3 tickers** (AAPL, GOOGL, AMZN), with a few others mentioned.
  - Models: o1-preview for "deep thinking", gpt-4o and gpt-4o-mini for "quick thinking".
  - Reported: cumulative return about 23–27%, **Sharpe 5.60–8.21**, max drawdown about 1–2%.
  - **No transaction-cost assumption is stated.**
  - The authors themselves say the 3-month window was forced by LLM cost (about 11 LLM calls plus 20+ tool calls per decision).
- **Criticisms**:
  - Nguyen & Pham (arXiv:2603.27539, March 2026; https://arxiv.org/html/2603.27539v1) call the Sharpe "consistent with trend following in a favorable regime rather than genuine risk-adjusted alpha". They list five common evaluation failures: look-ahead bias, survivorship bias, overfitting, cost neglect, and regime blindness.
  - **Statistical check (reviewer's calculation)**: the standard error of an annualized Sharpe ratio is approximately √((1 + SR²/2) / T_years), the Lo / Bailey & López de Prado logic. With SR = 5.6 and T = 0.25 years, SE ≈ √((1 + 15.7) / 0.25) ≈ 8.2. The reported Sharpe is therefore **less than one standard error from zero**.
  - **Pretraining look-ahead is not asserted here.** I did not check whether each model's training cutoff falls before January 2024. The window may be post-cutoff for some models. However, the agent's tools retrieve news and fundamentals, so the timestamp hygiene of that retrieval is a separate leakage risk.
- **Verdict**: **Not in plan**. At most, it is a UX reference for presenting multi-perspective reasoning. It is not evidence of profitability.

## 7. Bailey & López de Prado: Deflated Sharpe Ratio; Bailey, Borwein, López de Prado & Zhu: Probability of Backtest Overfitting

- **Deflated Sharpe Ratio (DSR)**
  - Citation: "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality." *Journal of Portfolio Management* 40(5):94–107, 2014 (40th Anniversary issue). SSRN 2460551, dated 2014-07-31. Confidence: high.
  - URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
  - Method: adjusts the Sharpe ratio for the number of trials, for skew and kurtosis of returns, and for track-record length. Returns the probability that the true Sharpe exceeds 0 (or a benchmark) after selection.
- **Probability of Backtest Overfitting (PBO)**
  - Citation: *Journal of Computational Finance* 20(4):39–69, 2017. doi:10.21314/JCF.2016.322. SSRN 2326253. Confidence: high.
  - URLs: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253 ; https://www.risk.net/journal-of-computational-finance/volume-20-number-4-april-2017
  - Method: combinatorially symmetric cross-validation (CSCV) estimates the probability that the in-sample-best configuration underperforms the median out of sample.
- **Reproducibility**: Both have closed-form or algorithmic definitions with public implementations (for example the R package `pbo`, and code in Stefan Jansen's ML4T materials).
- **Limitations**:
  - DSR needs an honest count of trials, including the variance across trials.
  - CSCV assumes the blocks are exchangeable, which is imperfect when returns are serially dependent.
- **Relevance**: These are mandatory gates for any later strategy or backtest module. They are not needed for alert detection itself.
- **Verdict**: **Later** (required as soon as backtesting exists).

## 8. Harvey, Liu & Zhu: "...and the Cross-Section of Expected Returns"

- **Citation**: *Review of Financial Studies* 29(1):5–68, 2016 (Editor's Choice). NBER w20592. Confidence: high.
- **URLs**: https://academic.oup.com/rfs/article-abstract/29/1/5/1843824 ; https://www.nber.org/papers/w20592
- **Contribution**: A multiple-testing framework (Bonferroni, Holm, BHY) applied to 300+ published factors. A new factor should clear roughly **t > 3.0**. The authors argue that most claimed findings are likely false.
- **Relevance**:
  - (i) For later strategy research, adopt t > 3 or an FDR-controlled hurdle.
  - (ii) **For the MVP alert engine the same logic applies.** Consider N tickers × many bars per day × several detectors. A fixed |z| > 3 threshold under a normal assumption will produce a predictable stream of false alerts. Fat tails (see Roll 1988 below) make the realized rate worse than the normal distribution implies.
  - Thresholds should be calibrated empirically to a **target false-alert rate per watchlist-day**, for example from the historical per-ticker distribution of standardized moves. They should not be read off a normal table.
- **Verdict**: **MVP** (threshold calibration principle); **Later** (strategy hurdle).

## 9. Event-study methodology

- **MacKinlay, A. C. (1997)**, "Event Studies in Economics and Finance." *Journal of Economic Literature* 35(1):13–39. Confidence: high. https://econpapers.repec.org/RePEc:aea:jeclit:v:35:y:1997:i:1:p:13-39
  - Defines normal-return models: constant mean, market model, and factor models.
  - Estimation window separated from the event window.
  - Abnormal return AR_t = R_t − (α̂ + β̂·R_m,t).
  - Standardized AR uses the estimation-window residual σ.
  - Covers CAR aggregation, test statistics, and power.
- **Brown, S. J. & Warner, J. B. (1985)**, "Using Daily Stock Returns: The Case of Event Studies." *Journal of Financial Economics* 14(1):3–31. doi:10.1016/0304-405X(85)90042-X. Confidence: high. https://ideas.repec.org/a/eee/jfinec/v14y1985i1p3-31.html
  - Simple market-model methods on daily data are generally well specified.
  - Event-induced variance changes and autocorrelation can matter.
- **Relevance**: This is the core of the deterministic detector.
  - Use the market-model abnormal return with SPY or a sector ETF as the benchmark; a sector-adjusted variant is also possible.
  - Standardize by the stock's own residual volatility, estimated over a trailing window (for example 120–250 trading days) that ends *before* the event window.
  - Handle overnight and intraday segments separately.
  - Use a variance estimator robust to earnings days, for example by excluding past earnings dates from the estimation window.
- **Verdict**: **MVP**.

## 10. Evidence linking news to price moves, and the "unexplained move" base rate

- **Boudoukh, Feldman, Kogan & Richardson (2019)**, "Information, Trading, and Volatility: Evidence from Firm-Specific News." *RFS* 32(3):992–1033. doi:10.1093/rfs/hhy083. Confidence: high.
  - URLs: https://academic.oup.com/rfs/article-abstract/32/3/992/5061375 ; SSRN https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2193667
  - Textually identified fundamental news explains **49.6% of overnight** idiosyncratic volatility but only **12.4% during trading hours**.
- **Boudoukh, Feldman, Kogan & Richardson (2013)**, "Which News Moves Stock Prices? A Textual Analysis." NBER w18725. Confidence: high. https://www.nber.org/papers/w18725
  - Once relevant news is identified by type and tone, the link between news and price is much stronger.
  - The median stock's return variance on identified-news days is **2.2×** that on no-news days.
  - Much press coverage is irrelevant to fundamentals.
- **Tetlock, P. C. (2007)**, "Giving Content to Investor Sentiment: The Role of Media in the Stock Market." *Journal of Finance* 62(3):1139–1168. doi:10.1111/j.1540-6261.2007.01232.x. Confidence: high. https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.2007.01232.x
  - Pessimism in a WSJ column predicts market-level downward pressure followed by reversion.
  - Extreme pessimism predicts high volume.
  - The findings are at market level, not firm level.
- **Roll, R. (1988)**, "R²." *Journal of Finance* 43(3):541–566, July 1988 (AFA Presidential Address). Confidence: high. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1988.tb04591.x
  - Systematic, industry and public firm-specific news together explain only about 0.35 of monthly and 0.20 of daily return variation for large stocks, measured by adjusted R².
  - Removing news dates barely changes R², but it changes kurtosis.
- **Cutler, Poterba & Summers (1989)**, "What Moves Stock Prices?" *Journal of Portfolio Management* 15(3):4–12. NBER w2538. Confidence: high. https://www.nber.org/papers/w2538
  - Macro news explains at most about one-third of aggregate return variance.
  - Many of the largest market moves have no identifiable news.
- **Jeon, McCurdy & Zhao (2022)**, "News as Sources of Jumps in Stock Returns: Evidence from 21 Million News Articles for 9000 Companies." *JFE* 145(2). doi:10.1016/j.jfineco.2021.08.002. Confidence: high. https://www.sciencedirect.com/science/article/pii/S0304405X21003470
  - Jump probability is significantly related to news flow and content, and the effect has grown over time.
  - The link is stronger for high-visibility firms.
- **Relevance, and the key product implication**: For a near-real-time *intraday* product, "no identified catalyst" is **the common case, not an edge case**. Only about 12% of intraday idiosyncratic volatility is tied to identified news. The system must treat **abstention as a primary, first-class output**, for example "No company-specific news or filing found in the window; the move coincides with the sector or market move" or "unexplained". Several design consequences follow:
  - Coverage is better for large, high-visibility names. Expect lower explanation rates for small caps.
  - Tetlock's results are market-level. Do not extrapolate them to firm-level sentiment claims.
  - Fat tails in daily returns (Roll) argue against assuming normal z-scores.
- **Verdict**: **MVP**, as the base rates and expectation setting behind the abstention design.

## 11. Grounding, attribution and citation-faithfulness evaluation

- **ALCE**: Tianyu Gao, Howard Yen, Jiatong Yu and Danqi Chen, "Enabling Large Language Models to Generate Text with Citations." *EMNLP 2023*. arXiv:2305.14627. Code: https://github.com/princeton-nlp/ALCE . Confidence: high. https://aclanthology.org/2023.emnlp-main.398/
  - Automatic metrics for fluency, correctness and **citation recall and precision**, computed with NLI entailment. The paper shows they correlate with human judgment.
  - Directly applicable: every sentence in an alert explanation must be entailed by its cited sources (recall), and each citation must support its sentence (precision).
- **RAGAS**: Shahul Es, Jithin James, Luis Espinosa-Anke and Steven Schockaert, "RAGAs: Automated Evaluation of Retrieval Augmented Generation." *EACL 2024 System Demonstrations*, pp. 150–158. Confidence: high. https://aclanthology.org/2024.eacl-demo.16/
  - Reference-free faithfulness, answer relevance and context relevance, judged by an LLM.
  - Useful for cheap continuous monitoring, but LLM-judge metrics must be calibrated against human labels.
- **AIS**: Hannah Rashkin et al., "Measuring Attribution in Natural Language Generation Models." *Computational Linguistics* 49(4):777–840, 2023. Confidence: high. https://direct.mit.edu/coli/article/49/4/777/116438/Measuring-Attribution-in-Natural-Language
  - The "Attributable to Identified Sources" human-annotation protocol. Use it as the basis for the human rating rubric.
- **FActScore**: Sewon Min et al., *EMNLP 2023*. arXiv:2305.14251. Code: https://github.com/shmsw25/FActScore . Confidence: high. https://aclanthology.org/2023.emnlp-main.741/
  - Decomposes text into atomic facts and reports the fraction supported by the source.
  - Good for measuring unsupported-claim rates in multi-sentence explanations.
- **Verdict**: **MVP** for the evaluation harness. Specifically: ALCE-style citation precision and recall, FActScore-style atomic-claim support, and the AIS human rubric. RAGAS-style LLM judges are for monitoring only after calibration.

## 12. 2024–2026 papers on LLM trading agents, financial benchmarks, and explanation quality

All verified to exist unless noted otherwise.

- **FinBen**: Qianqian Xie et al., "FinBen: A Holistic Financial Benchmark for Large Language Models." *NeurIPS 2024 Datasets & Benchmarks*. Confidence: high. https://proceedings.neurips.cc/paper_files/paper/2024/hash/adb1d9fa8be4576d28703b396b82ba1b-Abstract-Datasets_and_Benchmarks_Track.html
  - 42 datasets and 24 tasks.
  - LLMs are good at information extraction and textual analysis, but weak at forecasting and complex generation.
  - Supports using LLMs for **extraction and labeling** of news and filings, not for forecasting.
  - Verdict: **MVP** (supports the task choice).
- **StockBench**: Yanxu Chen et al., "StockBench: Can LLM Agents Trade Stocks Profitably in Real-world Markets?" arXiv:2510.02209 (2025-10-02; revised 2026-03-02). Also on OpenReview. Confidence: high. https://arxiv.org/abs/2510.02209
  - Claims to be contamination-free, with a multi-month window.
  - **Most LLM agents fail to beat buy-and-hold.**
  - Verdict: **Not in plan** for trading. It is useful as evidence for the product's "no forecasts" stance.
- **LiveTradeBench**: Haofei Yu, Fenghai Li and Jiaxuan You (UIUC), "LiveTradeBench: Seeking Real-World Alpha with Large Language Models." arXiv:2511.03628 (2025). Confidence: high. https://arxiv.org/abs/2511.03628
  - Live streaming evaluation, which avoids offline leakage by construction.
  - 21 LLMs across US stocks and Polymarket.
  - General-reasoning rank does not predict trading performance.
  - Verdict: **Later**. Its live, forward-only protocol is the gold standard if the product ever evaluates LLM decisions.
- **INVESTORBENCH**: Haohang Li et al., "INVESTORBENCH: A Benchmark for Financial Decision-Making Tasks with LLM-based Agents." *ACL 2025 (long)*. arXiv:2412.18174. Confidence: high. https://aclanthology.org/2025.acl-long.126/
  - Backtest-style environments over stocks, crypto and ETFs, using 13 backbone LLMs.
  - Uses historical data, so look-ahead caveats apply.
  - Verdict: **Not in plan**.
- **FinSearchComp**: arXiv:2509.13160 (2025-09-19). Confidence: high. https://arxiv.org/abs/2509.13160
  - 639 expert-written financial search and reasoning questions, including time-sensitive data fetching.
  - Relevant to the *retrieval* half of the alert pipeline.
  - Verdict: **Later**, as an optional external check on the retrieval agent.
- **Shah, Ye, Jaskowski, Xu & Chava, "Beyond the Reported Cutoff: Where Large Language Models Fall Short on Financial Knowledge."** *COLM 2025*. arXiv:2504.00042. Code and outputs released. Confidence: high. https://arxiv.org/abs/2504.00042
  - 197k questions.
  - LLMs are **more likely to hallucinate for larger companies, especially for recent years**.
  - Supports enforcing "use retrieved sources only" and stratifying evaluation by firm size.
  - Verdict: **MVP** (eval design).
- **Nguyen & Pham, "Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems: Taxonomy, Coordination Primacy, and Cost Awareness."** arXiv:2603.27539 (March 2026); a Springer chapter version also appears. Confidence: high for existence, medium for specific numbers. https://arxiv.org/html/2603.27539v1
  - Five minimum standards: contamination control, point-in-time universes, rolling-window reporting with variance, net-of-cost returns, and multi-regime coverage.
  - Gives about **0.9%/yr** as a survivorship-bias estimate. This figure is *their* number, not Shumway's.
  - Verdict: **Later** (backtesting checklist).
- **Ploutos**: Hanshuang Tong, Jun Li, Ning Wu, Ming Gong, Dongmei Zhang and Qi Zhang, "Ploutos: Towards Interpretable/Explainable Stock Movement Prediction with Financial Large Language Model." *Companion Proceedings of the ACM Web Conference 2025*. doi:10.1145/3701716.3715254. arXiv:2403.00782. Confidence: high for existence. https://dl.acm.org/doi/10.1145/3701716.3715254
  - Generates *rationales for predictions* ("rearview-mirror prompting").
  - It is **not** an evaluation of grounded, cited explanations of observed moves.
  - Verdict: **Not in plan**.
- **Gap finding**: After targeted searches, I found **no peer-reviewed or arXiv benchmark that evaluates the faithfulness or citation quality of "why is this stock moving" explanations** of observed abnormal moves. Such a benchmark would evaluate explanations with abstention on no-news moves and with timestamp checks on sources. This is a finding of absence based on search, and moderate confidence is appropriate. It supports **building an in-house evaluation set** (section b).

## 13. Survivorship bias and transaction-cost references for a later backtesting module

- **Shumway, T. (1997)**, "The Delisting Bias in CRSP Data." *Journal of Finance* 52(1):327–340. doi:10.1111/j.1540-6261.1997.tb03818.x. Confidence: high. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1997.tb03818.x
  - Performance-related delistings are surprises, and correct delisting returns are missing for most of them.
  - The omitted returns are large and negative.
  - Follow-up: Shumway & Warther (1999), JF, on Nasdaq delistings and the size effect: https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00192
  - Implication: backtests need a point-in-time universe that includes dead tickers, and delisting returns must be included or imputed.
- **Novy-Marx, R. & Velikov, M. (2016)**, "A Taxonomy of Anomalies and Their Trading Costs." *RFS* 29(1):104–147. NBER w20721. Confidence: high. https://academic.oup.com/rfs/article-abstract/29/1/104/1844518
  - Most anomalies with more than about 50% monthly turnover do not survive costs.
  - A buy/hold spread is the most effective cost mitigation.
- **Frazzini, Israel & Moskowitz (2018)**, "Trading Costs." SSRN 3229719. Working paper. Confidence: high. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3229719
  - Based on $1.7T of live institutional executions across 21 markets over 19 years.
  - A calibrated price-impact model.
- **Almgren, R. & Chriss, N. (2000/2001)**, "Optimal Execution of Portfolio Transactions." *Journal of Risk* 3(2):5–39. This is the commonly cited form. **Medium confidence; not verified on the publisher site.** The search summary gave inconsistent volume and page numbers, and those are not repeated here. Author PDF: https://www.smallake.kr/wp-content/uploads/2016/03/optliq.pdf
  - Permanent and temporary linear-impact model with an execution efficient frontier.
  - A standard slippage model for sizing assumptions.
- **Verdict**: **Later** (backtesting module).

---

## (a) Evidence standards before calling any signal, strategy or forecast "useful"

The product must not label anything "predictive", "useful" or "alpha" unless **all** of the following hold.

1. **Point-in-time data only.**
   - Prices, universe membership (including delisted names, per Shumway), fundamentals, news and filings must all carry *first-available* timestamps. This means the SEC EDGAR acceptance time and the news wire time, not the event date.
   - Every feature must be computable at decision time t.
   - Earnings dates must be the ones *announced* as of t.
2. **No LLM look-ahead.**
   - Any LLM-derived feature must be evaluated only on data after the model's documented training cutoff, or produced by a point-in-time model (ChronoGPT, TiMaGPT, DatedGPT, Kelly et al.).
   - Run entity-masking (Glasserman & Lin) and LAP-style (Gao et al.) audits.
3. **Out-of-sample by construction.**
   - Walk-forward or rolling-origin evaluation with an embargo or purge gap between training and test sets.
   - A final untouched holdout period.
   - Ideally, a period of live paper-trading or forward monitoring (the LiveTradeBench principle).
4. **Honest multiple-testing accounting.**
   - Log every variant tried.
   - Report the **Deflated Sharpe Ratio**, using the number of trials and their variance, and the **PBO** from CSCV. Require PBO below a preset level (for example < 0.2) and DSR > 0.95.
   - Require t > 3 or FDR-controlled significance (Harvey, Liu & Zhu).
5. **Net of realistic costs.**
   - Include spread, commission and market impact (a Frazzini, Israel & Moskowitz-style or Almgren-Chriss model), plus borrow costs for shorts.
   - Report a cost-sensitivity curve, for example 5, 10, 20 and 50 bp round trip. Lopez-Lira & Tang's result turning negative at about 20 bp is the cautionary example.
   - Report turnover and capacity.
6. **Sufficient length and regimes.**
   - At least several years, spanning bull, bear and high-volatility regimes.
   - Report the Sharpe standard error. A 3-month backtest with Sharpe 5.6 has SE ≈ 8 and proves nothing.
   - Use a broad, point-in-time universe, not a handful of hand-picked mega-caps.
7. **Beat simple baselines.** Compare against buy-and-hold, market or sector ETFs, and simple momentum or reversal. StockBench and LiveTradeBench show that LLM agents often fail this test.
8. **Full reproducibility and disclosure.** Keep a versioned code, data and prompt snapshot. Keep a pre-registered hypothesis log. Report failures alongside successes.
9. **For the alert engine**, which is not a forecast:
   - Claim only *descriptive* statistics, for example "this is a 4.1σ abnormal return versus the stock's 120-day residual volatility".
   - Publish a calibrated false-alert rate per watchlist-day.
   - Never imply future direction.

## (b) Evaluation plan for grounded LLM alert explanations

**Unit of evaluation.** An (alert, retrieved evidence set, generated explanation) triple.

**Build an in-house gold set. No suitable public benchmark exists.**
- Sample historical alerts, stratified across these axes:
  - news or filing present vs. **no identifiable catalyst**. Deliberately oversample no-news cases: they are about half of the product's real traffic intraday, per Boudoukh et al.
  - overnight/gap moves vs. intraday moves.
  - large vs. small caps. Size is a known failure axis in both Glasserman & Lin and Shah et al.
  - event type: earnings, 8-K item type, analyst action, sector or market sympathy move, ETF flow.
- For each case, annotators record:
  - the correct catalyst or catalysts, with source and timestamp; or "none identifiable";
  - the relevant text spans, in the style of FinanceBench evidence strings.

**Automatic hard checks (must be 100%; any failure blocks release):**
1. **Timestamp gating.** Every cited source's publication or acceptance timestamp must be ≤ the move's start time, or be clearly labeled as a "subsequent report". A source published after the move began, presented as its cause, is post-hoc rationalization. This is the explanation-layer equivalent of look-ahead bias.
2. **Citation existence.** Every citation resolves to a retrieved document ID and span in the evidence set. There must be zero fabricated URLs, tickers or filings.
3. **Numeric consistency.** Every number in the explanation (return %, EPS, guidance figures) must match the deterministic engine or the cited span exactly.

**Automatic soft metrics (tracked continuously, gated on thresholds):**
- **Citation precision and recall**, ALCE-style, using NLI entailment per sentence and per citation.
- **Atomic-claim support rate**, FActScore-style: the share of atomic claims entailed by the cited evidence.
- **RAGAS faithfulness and context relevance**. Use as a monitor only, after checking agreement with human labels (target Cohen's κ ≥ 0.6 between the LLM judge and humans).
- **Abstention quality**, computed on the no-news stratum:
  - *false-attribution rate*: the model names a catalyst when gold is "none";
  - *false-abstention rate*: the model says "none" when a gold catalyst exists;
  - report both with confidence intervals.
- **Retrieval-ablation (parametric-leak) test**: run the generator with the evidence removed, or with irrelevant evidence. If it still names a specific catalyst, it is using parametric memory. The target is near 0%. Also run with entity masking.

**Human rating rubric** (AIS-based; each item scored per explanation):
1. **Attribution (AIS)**: are all claims attributable to the cited sources? Yes / partial / no.
2. **Catalyst correctness**: is the named cause the gold cause, or a correct "none identifiable"?
3. **Causal overreach**: does the text assert causation ("fell *because of*") where the evidence only shows co-occurrence? The preferred phrasing is "coincided with".
4. **Completeness**: are material evidence items that were retrieved but omitted, for example an 8-K filed that morning?
5. **Market or sector context**: is the move correctly framed as idiosyncratic or as systematic, consistent with the abnormal-return decomposition?
6. **Clarity and no advice**: plain language, with no forecast or recommendation language.

Use two independent raters on **at least 20% overlap** and report Cohen's κ, with κ ≥ 0.6 as the target. Disagreements go to adjudication.

**Sample sizes:**
- A proportion estimated to about **±5 percentage points** at 95% confidence needs **n ≈ 385** per stratum of interest (worst case p = 0.5). About **±3 pp** needs **n ≈ 1,070**.
- For rare, severe failures such as fabricated citations or wrong numbers, use the **rule of three**: 0 failures in n = 150 bounds the true rate below about 2% at 95% confidence; 0 in 300 bounds it below about 1%.
- Suggested initial gold set: about 400 news-present and about 400 no-news alerts, balanced across the overnight/intraday and size strata, for roughly 800 in total. After launch, continuously sample about 50 live alerts per week for human audit.

**Release gates (suggested):**
- 100% pass on the hard checks.
- Citation precision ≥ 0.95.
- Atomic-claim support ≥ 0.95.
- False-attribution rate on no-news cases ≤ 5%, with the upper 95% CI bound ≤ 8%.
- Parametric-leak rate ≤ 1%.
- Human "fully attributable" ≥ 90%.

**Operational rule:** When evidence is absent, stale (published after the move began), or low relevance, the system shows the deterministic alert with "No company-specific catalyst found in [window]; sector/market moved X%". It does not show a generated narrative.

---

## Unverified or partly verified items

- Lopez-Lira & Tang's JFE "forthcoming" status: reported in a search snippet only, and the SSRN page returned 403. The v6 (2025-10-28) vs. "This Version: Aug 24, 2026" conflict is unresolved.
- Numeric details for Lopez-Lira & Tang (sample, N, cost breakeven) and TradingAgents (Sharpe, returns, MDD) came from automated extraction of the paper body: **medium** confidence.
- Almgren & Chriss volume and pages: medium confidence, not checked on the publisher site.
- The about 0.9%/yr survivorship figure is attributed to Nguyen & Pham (2026) and was not independently checked.
- Training-cutoff overlap for TradingAgents' models vs. the Jan–Mar 2024 window was not checked.
- No dedicated "why is the stock moving" explanation-faithfulness benchmark was found. This is an absence finding.

---

## 14. Financial foundation models (added 2026-09-24)

The full review is in [finance-models-evidence](finance-models-evidence.md), with its registry in §7. The catalogue of models, licences and India coverage is in [finance-models-catalogue](finance-models-catalogue.md). What this means for the plan is in [15](../15-finance-model-layer.md).

- **Kronos** (arXiv 2508.02739, AAAI 2026) is a foundation model for OHLCV candles.
  - Its training data includes NSE and BSE from 2020 and runs up to 2024-06, so any evaluation before 2024-07 is contaminated.
  - Its headline results come from the closed Kronos-large.
  - Independent post-cutoff checks are negative. On NSE its 80% intervals covered only 41.3% of outcomes. On AAPL it did worse than simply repeating the last price. **Verdict:** Later, as a volatility challenger only.
- **Rahimikia et al. (2511.18578):** off-the-shelf time-series foundation models forecast returns poorly (every out-of-sample R² is negative). Pretraining them on financial data closes the gap to CatBoost.
- **Noguer i Alonso & Franklin (2606.27100):** 2 of about 50 model–asset pairs are significant under Diebold–Mariano tests, which is what chance alone would produce.
- **Brini (2607.05291):** only TTM beats Log-HAR on realised volatility, and narrowly. An equal-weight TTM + Log-HAR blend is the most robust option.
- **MarS (ICLR 2025):** trained on China A-share order data. Never for the MVP.
- **FinGPT, Fin-R1, Palmyra-Fin:** never for forecasting; later for text tasks, and only with citations.
