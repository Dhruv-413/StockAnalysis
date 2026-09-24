# Evidence review: Kronos and other financial foundation models for an India (NSE/BSE) + US market assistant

Author: quant-researcher. Research date: 2026-09-24. All sources were accessed on 2026-09-24 unless a different date is noted.
Scope: an evidence review only. No repo files were edited and no third-party packages were run. The Kronos paper text was read from arXiv HTML v1.
Confidence: H means read in the primary source; M means a secondary summary or an inference from the primary source; L means a vendor claim or unverified.

---

## 0. Bottom line

1. **Kronos has not shown it can predict returns in a way users can act on.** Its paper's headline gains are relative ("+93% RankIC"), but the absolute numbers are tiny: IC is about 0.02–0.07.
   - The only portfolio test is on China A-shares only, with a fixed 0.15% cost. It reports no significance tests and no deflated Sharpe.
   - The headline figures come from **Kronos-large (499.2M), whose weights are closed**.
   - The best open model, Kronos-small, averages 17.9% AER in the China backtest against 16.8% for Moment-large. It has no significance test, and there is no equal-weight top-k baseline, even though nearly every baseline also shows positive "excess" return.
   - Three independent post-cutoff checks all come out negative: NSE calibration, AAPL daily, and BTC/gold direction. They tested Kronos-small, -mini and -base only, none of which were peer-reviewed.
2. **NSE and BSE are explicitly in Kronos's pretraining corpus, from 2020-01-31 up to June 2024** (paper Table 13, H). US data from Nasdaq and NYSE goes back to 2000. So any evaluation window that ends on or before 2024-06-30 is contaminated for both our markets. Only about 26 months of clean data exist, from 2024-07 to 2026-09 (roughly 540 sessions).
3. **Independent studies of time-series FMs on financial returns** agree:
   - Off-the-shelf zero-shot use is poor. Rahimikia et al. 2025 find every R²_OS negative.
   - Pretrained-model wins over random walk are tiny and mostly not statistically significant (Noguer i Alonso & Franklin 2026).
   - For volatility, only a small model (TTM) beats Log-HAR, and narrowly. Much of that gain is scaling, not better dynamics (Brini 2026).
4. **Verdicts for our product:**
   - (a) Forecasts shown to users: **NEVER** in the MVP, on both regulatory and evidence grounds.
   - (b) Internal volatility-regime or anomaly features: **LATER**, only as a challenger to HAR/EWMA/GARCH behind the validation protocol in §6.
   - (c) Synthetic test data: **NOT NEEDED**. GARCH-t and block bootstrap cover fixtures, and FM output has unknown data provenance.
   - (d) Scenario and stress testing: **LATER, research only**. Use historical post-cutoff episodes and parametric shocks first.
   - Financial LLMs (FinGPT, Fin-R1, Palmyra-Fin): **NEVER** for return forecasting. **LATER** for text tasks such as summarising filings, and only with citation grounding.

---

## 1. Kronos: the facts

| Item | Finding | Conf. | Source |
|---|---|---|---|
| Paper | Shi, Fu, Chen, Zhao, Xu, Zhang, Li. arXiv 2508.02739 v1, 2025-08-02. Accepted to AAAI 2026 (repo news dated 2025-11-10). | H | [arXiv](https://arxiv.org/abs/2508.02739), [repo](https://github.com/shiyu-coder/Kronos), [AAAI OJS](https://ojs.aaai.org/index.php/AAAI/article/view/39730/43691) |
| Problem | A foundation model trained directly on OHLCV(A) "K-lines", because generic time-series FMs underperform on financial data. It targets forecasting, volatility, and synthetic K-line generation. | H | arXiv HTML |
| Architecture | Two stages. (1) A tokenizer quantises each multivariate K-line into a k-bit code split into coarse and fine subtokens (n=2), using a hierarchical/BSQ-style quantiser. (2) A decoder-only Transformer autoregressively predicts coarse then fine subtokens, trained with cross-entropy. Context is 512 tokens (small, base, large) and 2048 for mini. | H | arXiv HTML Table 1; repo |
| Sizes | mini 4.1M (open), small 24.7M (open), base 102.3M (open), large 499.2M (**closed**). Issues #347 and #325 request access to large. | H | [repo](https://github.com/shiyu-coder/Kronos), [issues](https://github.com/shiyu-coder/Kronos/issues) |
| Training data | Over 12B K-line records (Table 13 total: 12.11B, 96,569 assets). The paper says "over 45 global exchanges" in one place and "over 40 exchanges, 30+ countries" in another. Asset classes: equities, ETFs, indices, crypto, futures, FX. Frequencies run from 1-minute to weekly. **The pretraining data goes up to June 2024.** The data vendor is **not disclosed**. Issue #100 asks for the training data to be released, and it hasn't been. | H | arXiv HTML appendix, Table 13 |
| **India included?** | **Yes.** From Table 13: **National Stock Exchange of India**, stock and ETF, 5T–W, 2,554 assets, 242,429,169 observations, starting 2020-01-31. **Bombay Stock Exchange**, stock and ETF, 5,491 assets, 284,428,211 observations, starting 2020-01-31. India stock indices: 113 series, 3.19M observations. US: Nasdaq 8,725 assets, about 2.48B observations from 2000-01-01; NYSE 7,073 assets, about 2.13B observations from 2000-01-01. | H | arXiv HTML Table 13 |
| Eval protocol | Test period starts July 2024 for every task, a "strict temporal separation". **The end date of the test period isn't stated.** Stock exchanges: XSHG, XNAS, XJPX, **XNSE**, XKRX and XHKG count as "in-distribution"; XIDX, XKLS and XTAI as out-of-distribution. Also all Binance spot pairs and over 1,000 FX pairs. Frequency runs from 5-minute to daily. Look-back and horizon pairs (Table 8): 5min 480→96 … daily 40→12. | H | arXiv HTML |
| Tasks and metrics | Price-series forecasting: IC and RankIC between the predicted and true path, averaged over the O/H/L/C channels. Note that this is **path correlation within a sample, not cross-sectional return IC**. Return forecasting: IC and RankIC. Realised volatility: MAE and R². Synthetic generation: discriminative score and TSTR (IC/RankIC). Investment simulation: annualised excess return (AER) and information ratio (IR). | H | arXiv HTML |
| Baselines | 25 in total. Zero-shot TSFMs: Time-MoE, Moirai, TimesFM, Moment, Chronos. Full-shot: iTransformer, TimesNet, TimeMixer, PatchTST, TimeXer, NSTransformer, DLinear, FEDformer. Econometric: ARCH and GARCH(p,q), with p,q ≤ 3 chosen by BIC. Generative: DiffusionTS, TimeVAE, TimeGAN. **The baselines leave out HAR/Log-HAR, EWMA/RiskMetrics, and random walk or persistence.** | H | arXiv HTML |
| Headline claims | +93% RankIC over the best TSFM and +87% over the best non-pretrained model on price forecasting; −9% MAE on volatility; +22% generative fidelity. These come from **Kronos-large**. | H (claims) | abstract |
| Absolute sizes | Ablation (Table 2, Kronos-small against internal variants, not external baselines): price IC 0.0431 and RankIC 0.0254; return IC 0.0665 and RankIC 0.0622; volatility MAE 0.0384 and R² 0.2490. For comparison, the Prob-AR variant scores 0.0179 / 0.0102 / 0.0356 / 0.0329 / 0.0464 / 0.1383. These rows compare Kronos with its own internal variants, not with external TSFMs, so they don't correspond to the "+93%" claim. Across the per-exchange tables (for example, XNSE price IC is about 0.063 for all three Kronos sizes), absolute IC is in the range of about 0.02–0.07. | H | Table 2; Tables 14–17 |
| XNSE volatility row | The Table 18 XNSE row reads MAE: Kronos-S 0.0264, B 0.0269, L 0.0267; ARCH 0.0269; GARCH 0.0271. R²: Kronos-S 0.1803, L 0.1815; GARCH 0.1548. On NSE Kronos beats GARCH by about **2.6% in MAE**, with no significance test. The frequency and horizon of this row aren't confirmed; the HTML extraction duplicates cells and I parsed it by hand. | M | Table 18 (HTML text) |
| Backtest | China A-shares only, on CSI300 (top-k=50, drop-n=5) and CSI800 (k=200, n=10). Equal-weight long-only. Signal is the mean expected return over 10 days from a 90-day look-back, with a minimum hold of 5 days and **0.15% cost per trade**. Table 10 AER/IR on CSI300 and CSI800: Kronos-large 21.9% / 1.42 and 19.7% / 1.88; Kronos-small 18.1% / 1.24 and 17.7% / 1.61; Moment-large 16.6% / 1.20 and 17.1% / 1.54; Moirai-large 14.7% / 0.97 and 16.8% / 1.52; TimesFM 7.9% / 0.74 and 13.6% / 1.64; Chronos-large −6.6% / −0.77 and 0.6% / 0.09. There is **no significance test, no deflated Sharpe, no stated trial count, no end date, no NSE or US portfolio test, no capacity or impact model, and no random or equal-weight top-k baseline**.
- **Column mapping check.** Column 5 is the mean of columns 1 and 3. For Kronos-large, (0.2193 + 0.1974) / 2 = 0.2084 AER, and (1.4177 + 1.8805) / 2 = 1.6491 IR.
- **Common tilt.** Nearly every model, including DLinear, FEDformer and NSTransformer, has positive CSI800 AER. Much of the "excess" is likely the equal-weight top-k tilt and the 2024–25 China market, not forecasting signal.
- **Open-weights comparison.** Kronos-small (open) averages 17.9% AER against 16.8% for Moment-large, a gap of about 1.1 pp with no test. | H | Table 10 |
| Limitations | The paper has no dedicated limitations section. Appendix H discusses design questions only. | H | arXiv HTML |
| Reproducibility | MIT licence. Weights for mini, small and base are on Hugging Face. Kronos-small's HF commits: "add model" on 2025-06-30 and only README changes afterwards, so the weights **have not been revised since the paper**. Fine-tune scripts are included for Qlib A-shares and generic CSV (released 2025-08-17). The **pretraining data, the full evaluation harness for the 25-baseline grid, and Kronos-large are not released.** Open issues include #52 (online demo doesn't match offline reproduction), #252 (tensor reshape bug in autoregressive inference), and #403 (predict hangs on Windows after 20–40 calls). | H | [repo](https://github.com/shiyu-coder/Kronos), [HF commits](https://huggingface.co/NeoQuasar/Kronos-small/commits/main), [issues](https://github.com/shiyu-coder/Kronos/issues) |
| Popularity | About 39.4k GitHub stars. This is **not evidence** of how well the model works. | H | repo |

### 1.1 Look-ahead and leakage assessment
- **Pretraining overlap.** The paper's own test windows start after the June 2024 cutoff, which is good. Any third-party backtest of Kronos on NSE, BSE, Nasdaq or NYSE data before 2024-07 is contaminated, and any "Kronos works on Nifty 2020–2024" claim is invalid by construction (H).
- **Normalisation.** Kronos normalises each window using statistics from its own context window. I haven't checked whether the repo's predict path leaks the forecast horizon into those statistics (unverified).
- **Cross-sectional contemporaneity.** The model is univariate per asset, so it has no cross-sectional leakage. It also carries no cross-sectional information.
- **Survivorship.** The corpus construction (Table 13) says nothing about delisted names. Assume it has survivor bias (M).
- **Test period shared with the model builders.** The test window was chosen, and the 25 baselines were tuned, after the fact by the authors. The paper doesn't report the number of configurations tried, so deflating the result for selection bias isn't possible.

### 1.2 Independent replications and critiques of Kronos (all post-cutoff, all smaller variants)

| Study | Model | Data and protocol | Result | Conf. |
|---|---|---|---|---|
| [neopentane7/kronos-candlecast](https://github.com/neopentane7/kronos-candlecast), pre-registered 2026-08-03 | Kronos-small, zero-shot | **NSE**, 59 tickers, daily bars from 2018-01 to 2026-06 (123,479 bars). 708 rolling windows, 12 forecast dates, 30-session horizon, 30-member ensembles. Calibrated on 2024 and evaluated on 2025–26, which is post-cutoff. Block-bootstrap confidence intervals. | Fair CRPS 121.87 against 67.24 for random walk plus drift (**81% worse**). Interval score 978 against 463 (111% worse). **80% prediction intervals covered only 41.3%** of outcomes, against 83.7% for the random walk. The ratio of predicted to realised spread falls from 0.909 at h=1 to 0.481 at h=30, so the uncertainty cone stops widening. Conformal calibration couldn't fix it: the best Kronos arm reached coverage 0.681 at width 0.211, against 0.796 at 0.146 for a conformal random walk. It **does not test** point returns or volatility. | M (a single unreviewed repo, but pre-registered with code) |
| [Issue #354](https://github.com/shiyu-coder/Kronos/issues/354), 2026-07-25 | Kronos-mini | AAPL daily from 2024-07-26 to 2026-07-24. 100 origins at 5-day spacing, horizons of 2, 3 and 5 days, 1,800 forecasts in total. | MAPE 12.8–21.7% **worse than persistence**. Only 33–41% of runs beat persistence. Directional accuracy was 48.5–54.3%. No maintainer reply. | M |
| [Issue #323](https://github.com/shiyu-coder/Kronos/issues/323), 2026-06-06 | Kronos-base | BTCUSDT and gold direction. It also checked 4,682 of the official demo's hourly "upside probability" outputs against realised Binance prices. | Direction is "around chance", and the probabilities are overconfident. | M |
| [Kinlay blog](https://jonathankinlay.com/2026/02/time-series-foundation-models-for-financial-markets-kronos-and-the-rise-of-pre-trained-market-models/), 2026-02-22 | Chronos, not Kronos | GARCH vs Chronos on ES volatility with an 80/20 split | A mixed, regime-dependent commentary. It recommends synthetic data and volatility as the main uses, and "not a production alpha engine". | L (a blog, not a controlled study) |
| [arXiv 2607.26792](https://arxiv.org/abs/2607.26792), 2026-07-29 | Any model | Quantile crossing and K-line crossing (a forecast High below Open or Close) in probabilistic OHLC forecasts | Proposes a post-hoc projection fix, KQSP. The abstract doesn't name Kronos, but the problem it fixes applies to any sampled OHLC generator. | M |

Reading the replications:
- Leakage would flatter Kronos, and these tests are post-cutoff, so their negative results are conservative.
- None tests Kronos-large. The paper's claimed scaling (small to large) is not independently checked.
- None tests volatility forecasting, which is where Kronos's claim is most plausible.

---

## 2. Independent evidence on time-series FMs for financial returns

| Paper | Data and protocol | Key finding | Conf. |
|---|---|---|---|
| Rahimikia, Ni, Wang, "Re(Visiting) Time Series Foundation Models in Finance", [arXiv 2511.18578](https://arxiv.org/abs/2511.18578), 2025-11-23 | Daily excess returns from 94 countries, 1990–2023. US sample: about 18.1M observations and 10,171 securities. Expanding window, retrained yearly, out-of-sample 2001–2023. Chronos (tiny to large), TimesFM, plus about 10 other TSFMs. Benchmarks: OLS, Lasso, Ridge, ENet, PCR, XGBoost, CatBoost, LightGBM, neural nets. | Zero-shot: Chronos-large R²_OS −1.37% and TimesFM-500M −2.80%, both below the benchmarks. Fine-tuning helps little. **Pretraining from scratch** on financial returns plus more data plus hyperparameter optimisation approaches CatBoost (Chronos-small from scratch with global and JKP data: accuracy 51.74%, Sharpe 6.78). **Every R²_OS is negative, including CatBoost at −0.03%.** The Sharpe ratios of 5–7 are daily-rebalanced long-short deciles **before costs**, so they fail 06 §7 as evidence of usefulness. About 50k GPU-hours. The authors flag look-ahead risk for off-the-shelf weights. I haven't verified whether Kronos was among the other TSFMs. | H (abstract), M (numbers via HTML summary) |
| Noguer i Alonso & Franklin, "Pretrained TSFMs for Financial Return Forecasting", [arXiv 2606.27100](https://arxiv.org/abs/2606.27100), 2026-06-25 | Five US large-caps (AAPL, AMZN, GOOG, JPM, META). Rolling origin over 10 windows, 2024–2026. TimeGPT, TimesFM-2.5, Moirai-2.0, Chronos, Chronos-2 against NBEATS, NHITS, PatchTST, iTransformer, KAN and random walk. | Pretrained models win 8 of 10 task-level comparisons, but **one-sided Diebold–Mariano tests reject only 2 model–asset pairs** (Chronos on AMZN, Moirai-2.0 on GOOG). Across about 50 pairs, 2 rejections at 5% is what chance alone predicts. The authors conclude these are "useful practical priors … not universal engines for … alpha". | M |
| Brini, "Forecasting Realized Volatility with TSFMs", [arXiv 2607.05291](https://arxiv.org/abs/2607.05291), 2026-07-06 | VOLARE: 50 assets across equities, FX and futures. 9 zero-shot TSFMs against 8 econometric specs from the HAR family. 3 horizons. Model Confidence Set. | Pooled losses favour TSFMs, but **only TTM (a small model) consistently beats Log-HAR, and narrowly**. After recalibration, "much of the short-horizon advantage reflects better-scaled forecasts", with real informational gain only at the monthly horizon. An **equal-weight TTM + Log-HAR** combination was in the MCS for 98–100% of assets. | M |
| FinVerse (LG AI Research), [arXiv 2608.03259](https://arxiv.org/html/2608.03259v2), 2026-08-20 | 43 FMs, 60,232 targets. Point accuracy, cross-sectional ranking and portfolio backtests, 78 metrics. Mostly US, with **no India**. | "No single model consistently dominates". Rankings correlate with the generic GIFT-Eval ranking at only r = 0.40, so generic leaderboards don't carry over to finance. Kronos's inclusion is unverified. | M |
| FinTSB, Hu et al., [arXiv 2502.18834](https://arxiv.org/abs/2502.18834) (Frontiers of CS 2026; [code](https://github.com/TongjiFinLab/FinTSBenchmark)) | 15 years of stock data, grouped into four movement-pattern regimes. Includes transaction fees and regulatory constraints. | A benchmark design paper. It argues that ignoring market structure inflates results. I didn't extract model-family results from the abstract. | M |
| FinCast, [arXiv 2508.19609](https://arxiv.org/abs/2508.19609), 2025-08-27 | Financial TSFM | Claims strong zero-shot results. I didn't verify its data, baselines or weights. | L |

**Synthesis: where FMs help and where they don't.**
- **Point return or direction prediction: no reliable help.** R²_OS is at or below 0 and directional accuracy is 50–52%. DM significance is rare and consistent with chance. Any portfolio "gains" come before costs or on a single market.
- **Volatility and risk: small, model-specific help at best.** Log-HAR is the bar to beat, and it is cheap, interpretable and fast. The gains from an FM are narrow and partly just a matter of scale.
- **Volume and intraday seasonality:** Kronos's showcase figures include volume forecasts, but I found no independent evidence either way (unverified).
- **Synthetic data:** plausible. Kronos claims +22% discriminative score against DiffusionTS, TimeVAE and TimeGAN. It **did not compare** against GARCH-t, block bootstrap or regime-switching models, which are the right baselines for stress testing.
- **Probabilistic calibration:** Kronos-small's intervals are badly under-dispersed at multi-day horizons on NSE (candlecast).

---

## 3. LOB and market simulators: Microsoft MarS

| Item | Finding | Conf. | Source |
|---|---|---|---|
| Paper | "MarS: a Financial Market Simulation Engine Powered by Generative Foundation Model", arXiv 2409.07486 (v2 2025-03-13). ICLR 2025. | H | [arXiv](https://arxiv.org/abs/2409.07486), [repo](https://github.com/microsoft/MarS) |
| Model | Large Market Model (LMM). An order model with 2M–1.02B parameters (LLaMA-2 style) and an order-batch model with 150M–3B. | M | arXiv HTML |
| Data | **Chinese A-share order-level data, the top 500 stocks by liquidity, 2017–2023.** About 16B order tokens (32B for training the order model). **No India or US data.** | M | arXiv HTML |
| Evaluation | 11 stylized facts (following Cont), market impact that follows the square-root law, a forecasting comparison against DeepLOB, and a manipulation-detection case study. Out-of-sample windows aren't clearly specified. | M | arXiv HTML |
| Release | MIT licence. **Only the 2M, 5M and 10M models are released.** Larger models are awaiting Microsoft legal (CELA) approval. | M | repo |
| Fit for us | We don't have NSE or US order-level (L3) data, and building on it would need licensed exchange feeds. Transfer from China A-shares, with its price limits, T+1 settlement and different tick rules, is unproven. **Verdict: never for the MVP. Later only as a research reference** for stress-test design. See also M3 ([arXiv 2608.19227](https://arxiv.org/pdf/2608.19227), not reviewed). | M | — |

---

## 4. Financial LLMs

| Model | What it is | Evidence quality | Verdict |
|---|---|---|---|
| FinGPT ([repo](https://github.com/AI4Finance-Foundation/FinGPT)) | LoRA fine-tunes of Llama-2, Falcon, ChatGLM2 and others for sentiment, NER and headline tasks, plus FinGPT-Forecaster (movements of Dow 30 stocks). MIT licence. | Sentiment F1 of 0.882 on FPB. **The Forecaster has no rigorous out-of-sample, cost-aware evaluation.** Its base models are from 2023. | Never for forecasting. Sentiment only as a candidate baseline, later. M |
| Fin-R1 ([arXiv 2503.16252](https://arxiv.org/abs/2503.16252)) | A 7B reasoning model trained with SFT and RL on 60,091 chain-of-thought samples distilled from benchmarks | The average of 75.2 is **on a benchmark mix the authors assembled, overlapping the sources of its training data**. This is a contamination risk. | Later, for text QA only, after our own eval. M |
| Palmyra-Fin (Writer, [page](https://writer.com/llms/palmyra-fin/)) | A 70B finance LLM | The "73% on a **sample** CFA Level III MCQ test" and its long-fin-eval results are a **vendor claim on an in-house benchmark**. | Later, for text tasks only. L |
| Look-ahead in LLMs | Lopez-Lira, Tang, Zhu, "The Memorization Problem" ([arXiv 2504.14765](https://arxiv.org/abs/2504.14765)): GPT-4o recalls S&P 500 closes within 1% before its cutoff, and masking doesn't stop it. See also [Look-Ahead-Bench 2601.13770](https://arxiv.org/pdf/2601.13770) and [Gao, Jiang, Yan 2512.23847](https://arxiv.org/html/2512.23847). | Any LLM forecast backtest that falls before the model's cutoff is **invalid**. | Applies to every LLM feature. H (abstracts) |

---

## 5. Regulatory constraints on use case (a), showing forecasts to users

- **India. The SEBI RA (Third Amendment) Regulations 2024** (notified 2024-12-16) require a research analyst to disclose how far AI tools are used (Reg 19(vii)). The RA remains **solely responsible** for the research output and for client data ([SCC Online](https://www.scconline.com/blog/post/2024/12/19/sebi-research-analyst-third-amendment-regulations-2024/), [Lexology](https://www.lexology.com/library/detail.aspx?g=f2e36044-cc40-4c8f-8e74-79141d32031e); M).
  - A price or return forecast for a named security, shown to users, is plausibly a "research recommendation" or advice. That needs RA registration, or a registered partner acting as the responsible entity.
  - The retail algo framework treats black-box algos as requiring an RA (see project memory).
- **SEBI circular SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/51 of 2025-04-04** set up **PaRRVA** (Past Risk and Return Verification Agency). It has been live since 2026-05-04. Any performance or return claim by an RA, IA or algo provider must be verified ([Business Standard](https://www.business-standard.com/markets/news/sebi-launches-return-verification-framework-parrva-to-curb-fake-performance-claims-125120800842_1.html), [TaxGuru](https://taxguru.in/sebi/sebi-operationalises-parrva-due-verified-performance-disclosure-securities-market.html); M).
- SEBI also restricts regulated entities from associating with unregistered persons who make return or performance claims ([TaxTMI](https://www.taxtmi.com/highlights?id=82493); M). The exact circular and date need verifying; I believe it is August 2024.
- **US. FINRA Rule 2210(d)(1)(F)** prohibits predictions or projections of performance in communications. The exception is a "hypothetical illustration of mathematical principles" (calculator-like) that doesn't project a specific investment's performance ([FINRA FAQ](https://www.finra.org/rules-guidance/guidance/faqs/advertising-regulation); H).
  - A proposed amendment to allow some projections and targeted returns was filed in Feb 2026 ([Federal Register 2026-02-25](https://www.federalregister.gov/documents/2026/02/25/2026-03705/self-regulatory-organizations-financial-industry-regulatory-authority-inc-notice-of-filing-of-a); H for the filing). I don't know its adoption status as of 2026-09 (unverified).
  - The SEC Marketing Rule (for advisers) allows hypothetical performance only under conditions ([K&L Gates summary](https://www.klgates.com/FINRA-Meets-the-Marketing-RuleMostly-Performance-Projections-and-Targeted-Returns-Under-Proposed-Amendments-to-Rule-2210-2-23-2026); M).
  - Whether our product counts as a broker-dealer or adviser communication, or falls under the publisher's exclusion, is a legal question for counsel.

---

## 6. Verdicts by use case, with the validation protocol each would need

### (a) Forecasts shown to users: NEVER (MVP and v1)
- **Evidence.** There is no robust post-cutoff evidence that returns or direction can be predicted. Independent tests fail to beat persistence or random walk (#354, candlecast), and Kronos-small's intervals are badly miscalibrated on NSE.
- **Regulation.** A forecast shown to users would bring in SEBI RA and PaRRVA obligations in India and FINRA 2210 in the US.
- **What would reopen this** (only after a legal sign-off). All of the following must hold on data after 2024-07 (after 2026-09 for any re-trained model), from point-in-time NSE/BSE and US data:
  1. Walk-forward with an expanding or rolling origin, the model frozen per fold, and no tuning on test folds.
  2. A cross-sectional daily IC and RankIC with a **Newey–West t-stat**. The IC must beat a naive momentum/reversal factor and a zero forecast.
  3. A long-short or long-only portfolio **net of costs**:
     - India: STT, exchange transaction charges, SEBI fee, stamp duty, GST, brokerage, and a spread or impact estimate.
     - US: spread and impact.
     - Capacity limits taken from ADV.
  4. **Deflated Sharpe ratio** (Bailey & López de Prado 2014), with the number of trials N pre-registered and counting every model, size and hyper-parameter tried.
     - DSR = Φ( (SR̂ − SR₀)·√(T−1) / √(1 − γ₃·SR̂ + ((γ₄−1)/4)·SR̂²) ).
     - SR₀ = √V[SR_n] · ( (1−γ_E)·Φ⁻¹(1 − 1/N) + γ_E·Φ⁻¹(1 − 1/(N·e)) ).
     - SR̂ is the non-annualised per-period Sharpe. γ₃ and γ₄ are the skew and kurtosis of the returns, *not* Gaussian. γ_E ≈ 0.5772. V[SR_n] is the variance of Sharpe ratios across the trials.
     - Verify the formula against the original paper before implementing it.
     - Φ appears here as part of the construction of the test statistic. It is not a Gaussian alert table.
     - **Power, for a single trial and an annualised SR of 1 (SR_daily ≈ 0.063):**
       - At one-sided 5% and 50% power, T ≈ (1.645 / 0.063)² ≈ 680 sessions.
       - At 80% power, T ≈ ((1.645 + 0.84) / 0.063)² ≈ 1,560 sessions.
       - Fat tails and multiple trials push both higher.
     - With about 540 post-cutoff sessions, **the window is badly underpowered today**.
  5. Baselines: zero forecast, persistence, 12-1 momentum, short-term reversal, and a CatBoost model on standard features.
  6. Reported separately for each market, and inside and outside circuit-limited days.

### (b) Internal features for volatility regime and anomaly detection: LATER, as a challenger only
The production baseline stays at EWMA (λ = 0.94), GARCH(1,1) with Student-t innovations, and HAR-RV/Log-HAR. Kronos-small or base, or TTM, could be added as a challenger if and only if it passes the following:
- **Target.** Next-h realised variance. India data is daily only, so use a range proxy:
  - Parkinson: σ²_P = (ln H − ln L)² / (4 ln 2).
  - Garman–Klass: σ²_GK = 0.5 (ln H/L)² − (2 ln 2 − 1)(ln C/O)².
  - Use 5-minute RV where licensed intraday data exists (NSE, or US regular trading hours).
  - Exclude or flag the pre-open, the closing auction session, and days when a stock hit its circuit or price band, because a band-capped High−Low understates true volatility.
- **Loss functions.** Use **QLIKE**, L(σ̂², σ²) = σ²/σ̂² − ln(σ²/σ̂²) − 1, and MSE on variance. Both stay reliable when the volatility proxy is noisy (Patton 2011). **MAE on volatility, the metric Kronos reports, is not robust in this sense.**
- **Tests.** DM test against Log-HAR (HAC variance). Hansen **Model Confidence Set** at 90%. Also test an equal-weight combination of the FM and Log-HAR, per Brini.
- **Windows.** Only data after 2024-07. Pre-register a split: calibrate on 2024-07 to 2025-06, test on 2025-07 onwards.
- **Anomaly or regime flags.** Calibrate thresholds to an **empirical target false-alert rate**, for example 1 alert per symbol per 20 sessions under the null, using quantiles of the historical score distribution, not Gaussian z-tables.
  - Report the realised false-alert rate with block-bootstrap confidence intervals.
- **Operational gates.** Latency must fit the 300 ms budget; Kronos sampling is autoregressive and stochastic, so fix seeds and ensembles. Pin a deterministic version. Licence: MIT for the weights, but **pretraining data provenance is unknown**.
- **Accept only if** the FM is in the MCS and beats Log-HAR on QLIKE with DM p < 0.05 after Holm correction, in both markets. Otherwise don't ship it.

### (c) Synthetic data for testing: NOT NEEDED as an FM; use a classical generator
- Software fixtures and property tests need controlled, reproducible series. **GARCH-t, a stationary block bootstrap (Politis–Romano), and regime-switching models** do this deterministically and with a clean licence.
- If an FM generator is ever used, it must pass:
  1. A **stylized-facts checklist** against held-out post-cutoff data: Hill tail index within the confidence interval of the real data; no ACF in returns; ACF of |r| decaying slowly (volatility clustering); leverage effect (corr(r_t, |r_{t+k}|) < 0); aggregational Gaussianity.
  2. Distributions of **maximum drawdown and of 1% and 5% VaR** within bootstrap confidence intervals.
  3. A **memorisation check**: nearest-neighbour distance from generated windows to the pretraining-period history. NSE and BSE data from 2020–2024 is in Kronos's corpus, so exact regurgitation is possible.
  4. OHLC consistency, L ≤ min(O,C) ≤ max(O,C) ≤ H, holding in 100% of generated bars (see 2607.26792).
- **Licence risk.** The vendor is undisclosed, so generated sequences have unknown provenance. Don't ship FM-generated data as a product asset.

### (d) Scenario and stress testing: LATER, research only
- First, **replay historical post-cutoff episodes**:
  - 2024-08-05, the yen-carry unwind, in both markets.
  - The US tariff shock of April 2025 (exact dates to be verified).
  - India's election-result day, 2024-06-04. It is **inside the Kronos pretraining window**, so it is a contaminated scenario for any FM.
- Then apply parametric shocks: σ × k, gap opens, and circuit-limit hits on NSE's 5/10/20% bands.
- FM-conditioned scenarios (Kronos or MarS) could be explored later if they pass the stylized-facts and tail checks in (c) and a coverage test of their stress quantiles against realised post-cutoff stress days.
- **India mechanics any generator must respect:** price bands and circuit filters, index-wide circuit breakers, the pre-open call auction, the F&O closing auction (from 2026-08-03), T+1 settlement, and point-in-time lot sizes.

---

## 7. Paper registry entries for `research/papers.md` (proposed)

| Paper | Problem | Data | Evaluation | Reproducibility | Limitations | Verdict |
|---|---|---|---|---|---|---|
| Kronos (2508.02739, AAAI 2026) | FM for OHLCV K-lines | 12.1B bars, 40–45 exchanges, **incl. NSE and BSE from 2020**, data to 2024-06 | Post-2024-07 test. IC and RankIC as path correlation. Volatility by MAE. A single China backtest with 0.15% cost, no significance tests. | Code and small weights under MIT. Large weights, data and full eval harness closed. | Headline results come from a closed model. Baselines lack HAR, random walk and EWMA. The test end date is unstated. Independent post-cutoff checks are negative. | **Later** (volatility challenger only). **Never** for user-facing forecasts. |
| Re(Visiting) TSFMs (2511.18578) | Do TSFMs forecast returns? | 94 countries, 1990–2023 | Expanding window, R²_OS, direction, long-short Sharpe (mostly gross) | 50k GPU-hours; code status not verified | Univariate; Sharpe ratios before costs | **Evidence input**: zero-shot is poor |
| Noguer i Alonso & Franklin (2606.27100) | TSFMs vs neural baselines | 5 US stocks, 2024–26 | Rolling origin, DM tests | Not verified | 5 assets; underpowered | **Evidence input**: small, mostly not significant |
| Brini (2607.05291) | TSFMs vs HAR for volatility | 50 assets | MCS, recalibration | Not verified | No India | **Evidence input**: keep Log-HAR as the bar; TTM+HAR is a candidate |
| MarS (2409.07486, ICLR 2025) | Order-level market simulation | China A-shares, 2017–23 | Stylized facts, impact | Small models only | No India or US data; needs L3 feeds | **Never** (MVP); later as a reference |
| FinGPT, Fin-R1, Palmyra-Fin | Finance LLMs | Varied | Self-assembled or vendor benchmarks | Mixed | Contamination; memorisation | **Never** for forecasting. **Later** for text tasks. |

---

## 8. Open methodological risks (hand-off to data-engineer, realtime-engineer and financial-correctness-reviewer)

1. **Contamination.** NSE, BSE, Nasdaq and NYSE are all in Kronos's pretraining through 2024-06. Every evaluation must start on or after 2024-07-01, and the start date must be recorded in the experiment manifest.
2. **Underpowered window.** About 540 post-cutoff sessions can't support a deflated-Sharpe claim for a strategy with Sharpe ≤ 1. That needs about 680 sessions at 50% power, or about 1,560 at 80% power, and more once N > 1 trials.
3. **Point-in-time adjustment.** Back-adjusted prices are rewritten after corporate actions (the candlecast README notes this). Store raw prices plus a corporate-action ledger, and compute adjustment as of each evaluation date.
4. **Band censoring.** NSE price bands and circuits cap High and Low, which biases range-based volatility estimators and K-line tokenisation.
5. **Nondeterminism.** Kronos sampling (temperature and top-p) gives stochastic outputs. Fix seeds and ensemble size for any reproducible feature.
6. **Licence class.** Weights are MIT, but the training-data licence is unknown. Mark the class as "unknown provenance, research only".
7. **Latency.** Autoregressive decoding of a 100M-parameter model for many symbols is unlikely to fit a 300 ms path. It would have to be computed offline or end-of-day (unverified; benchmarking would need approval).

## 9. Unverified items
- The Kronos test-period end date, and the exact frequency and horizon of the XNSE volatility row. My column mapping for Table 18 was parsed by hand from HTML text that duplicates cells.
- How Kronos compares with the zero-shot TSFMs (TimesFM, Chronos, Moirai) on NSE volatility specifically (Table 19). I couldn't parse it reliably.
- Whether the repo's normalisation leaks the forecast horizon.
- Whether Kronos is among the about 10 extra TSFMs in Rahimikia et al., or evaluated in FinVerse.
- Details of FinTSB model-family results, and FinCast's data and weights.
- The number, date and wording of the SEBI association-restriction circular (believed to be August 2024).
- Whether the FINRA 2210 projections amendment was adopted after the Feb 2026 filing.
- Whether MarS larger weights have been released since.
- US stress dates for April 2025.
- The candlecast data source (the repo implies adjusted daily prices; the vendor isn't named) and its 59-ticker universe.
