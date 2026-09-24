# Research appendix: finance-specialised models and toolkits (Kronos and its peers)

> **Tech-lead note (2026-09-24).** Where this catalogue differs from [finance-models-evidence](finance-models-evidence.md), the evidence appendix governs. That applies in particular to: Kronos as the #1 forecasting feature; Kronos in Trial; and showing a forecast band to users. This catalogue did not take into account the negative post-cutoff NSE replication (kronos-candlecast). The adopted placements are in [15](../15-finance-model-layer.md) and [ADR-009](../adr/ADR-009-finance-model-layer.md): Kronos is in Assess, as an internal volatility challenger only, and no forecasts or sentiment scores are shown to users.

- **Author:** tech-scout
- **Research date / access date for every URL:** 2026-09-24 unless noted otherwise
- **Method:** read-only metadata only.
  - GitHub REST via `gh api`: stars, licence SPDX, `pushed_at`, latest release.
  - Hugging Face `/api/models` and `/api/datasets`, plus the raw model cards.
  - The PyPI JSON API.
  - arXiv HTML full text, grepped for the Kronos, FinCast and two independent-evaluation papers.
  - Web search for venues.
  - Nothing was downloaded to the project, installed or executed. Repo files are untouched.
- **Scope:** product is an India (NSE/BSE) + US market assistant. The tasks scored are:
  - **F**: forecasting as a feature, i.e. a precomputed signal or band, not advice.
  - **S**: sentiment and tagging.
  - **Q**: QA over filings.
  - **R**: risk and portfolio.
- **Fit score:** 0 to 5 per task, for our product.
- **Licence flags** use the scout guardrail list (AGPL/BSL/SSPL/ELv2/Commons Clause), plus:
  - **NC**: non-commercial weights or data.
  - **NOLIC**: no licence file. This means all rights are reserved, which blocks commercial use until clarified.
  - **Llama-2 / Llama-1**: the upstream licence terms apply.

## 0. Key findings up front

1. **Kronos does cover India.**
   - The arXiv 2508.02739 appendix corpus table lists:
     - National Stock Exchange of India: 2,554 stocks/ETFs, 242.4M records, 5-min to weekly bars.
     - Bombay Stock Exchange: 5,491 instruments, 284.4M records.
     - "India Stock Index": 113 series, 3.19M records.
   - XNSE is one of the six *in-distribution* test exchanges.
   - Test period starts **July 2024**, after the pre-training cut-off of June 2024, so it is a genuine temporal out-of-sample split.
   - The only trading backtest is **Chinese A-shares (CSI300/CSI800)** in Qlib, top-k/drop-n long-only, with **0.15% cost per trade**. There is no India or US backtest.
   - **Model sizes in the results.** The paper's result tables report Kronos-S (small), Kronos-B (base) and Kronos-L (large) side by side, so the released sizes *are* evaluated. Kronos-mini is not in the paper.
   - **XNSE price-forecast row, as parsed from the arXiv HTML (column mapping M-confidence because of duplicated MathML text):**
     - IC: S ≈ 0.063, B ≈ 0.065, L ≈ 0.063.
     - RankIC: S ≈ 0.043, B ≈ 0.046, L ≈ 0.049.
     - Across full-shot supervised baselines, IC ranges from about −0.03 to 0.057, and the best baseline sits close to Kronos.
     - So on NSE, Kronos's edge over a well-tuned supervised baseline is **small**. All models' XNSE IC lies in roughly the −0.03 to 0.065 range. (H for existence, M for exact column mapping)
2. **Code and weights are MIT for Kronos-mini/small/base and both tokenizers.** Kronos-large (499M) is **not released**; the HF ID returns not-found. (H)
3. **The "Kronos + Qlib" integration is real.**
   - `finetune/` contains `qlib_data_preprocess.py` and `qlib_test.py`.
   - `finetune_csv/` allows fine-tuning on arbitrary CSV data, which is the route for NSE/BSE bars.
   - Last commit was 2026-04-13. There are no GitHub releases, so pin a commit. (H)
4. **Independent evidence tempers every TSFM claim, Kronos included.**
   - arXiv 2607.05291 (Jul 2026): 8 of 9 general TSFMs zero-shot do not beat Log-HAR on realized volatility across 50 assets. Kronos and FinCast were *not* tested.
   - arXiv 2606.27100 (Jun 2026): TSFMs win the rankings on 5 US stocks, but "gains over the random-walk benchmark are small and sparse" and are not evidence of alpha.
   - Rahimikia et al., arXiv 2511.18578: off-the-shelf TSFMs underperform CatBoost/LightGBM on daily excess returns, and finance-native pre-training closes much of the gap.
   - FINSABER, arXiv 2505.07078 (KDD 2026 D&B, oral): LLM trading-agent advantages "substantially decline" over 20 years and 100+ symbols, because of survivorship and data-snooping bias.
   - **Implication:** use Kronos-type output as a *feature or visualisation band*, never as a headline "prediction". (H)
5. **Licence traps found:**
   - OpenBB is **AGPL-3.0**.
   - vectorbt is **Apache-2.0 + Commons Clause**, so it cannot be sold as part of a paid product.
   - Moirai-2.0 weights are **CC-BY-NC-4.0**.
   - Palmyra-Fin is under the **Writer open model licence, non-commercial only**.
   - FinanceBench data is **CC-BY-NC-4.0**.
   - Financial PhraseBank, the training data behind ProsusAI/finbert, is **CC-BY-NC-SA-3.0**.
   - The Finance-Llama and FinGPT adapters carry **Llama-2/3 base terms**.
   - SEC-BERT and FiNER-139 are **CC-BY-SA-4.0**.
   - FinTSB is **GPL-3.0**; NautilusTrader is **LGPL-3.0**.
   - XuanYuan-6B and AdaptLLM finance-chat are under **Llama-2** terms.
   - **NOLIC** (no licence): StockMixer, InvestLM, XuanYuan repo, FinanceBench repo, lob_bench, FinBen repo, EconBERTa repo, and the ProsusAI/finbert and finbert-tone HF cards (their GitHub repos are Apache-2.0).
6. **Look-alike and squatted PyPI names:**
   - `qlib` on PyPI is an unrelated 2018 "Q Engineering" package. The real one is **`pyqlib`**.
   - `kronos` on PyPI is an unrelated 2011 package (jgorset). Kronos has no official PyPI package; use a GitHub pin.
   - `tradingagents` on PyPI (v0.7.0) is published by **Mai0313**, a third party, not TauricResearch.
   - `fingpt` 0.0.1 (2023) and `finrobot` 0.1.5 (2024) are stale relative to their repos. (H)
7. **India-specific finance LLMs:**
   - No credible model has been found. HF search on "india-finance", "indian-finance", "nifty", "indian-stock" and "fin-india" returns only hobby fine-tunes with fewer than 1k downloads.
   - `sapt3009/AI4Invest-Indian-FinBERT` is labelled "Indian" but its card says it is trained on `zeroshot/twitter-financial-news-sentiment`, a **US** dataset. It is mislabelled.
   - The only real India-specific artefact is the benchmark **IndiaFinBench** (arXiv 2604.19298): 406 QA over SEBI/RBI text. (H for the null result as of this date.)
8. **Owner-relevant: TradingAgents v0.5.1 (2026-09-24) already integrates TypeSafe Jev.** Verified in code, in `tradingagents/agents/post_screen.py`:
   - It calls `https://api.typesafe.ai/v1/systemone` with model `jev-latest`, and only when `TYPESAFE_API_KEY` is set.
   - It asks two questions per StockTwits/Reddit post: is the post on-topic, and what is its stance.
   - It drops a post only when p(on-topic) < 0.3.
   - On failure it falls back to unscreened posts.
   - This is **background tagging**. It is consistent with our existing constraint that Jev is used for background tagging only and stays on Hold for the India live path (US-West hosting, about 233 ms RTT). (H)

## 1. Financial time-series / K-line / order-flow foundation models

| Model | Org / repo / weights | Paper, venue | Latest activity | Code licence | Weights licence | Sizes | Training data (India?) | I/O | Reported results and methodology | F | S | Q | R | Conf |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Kronos** | shiyu-coder/Kronos (39.4k stars); HF NeoQuasar | arXiv 2508.02739, **AAAI 2026** | commit 2026-04-13; no releases; HF weights 2025-09-09 | MIT | MIT (mini/small/base, Tokenizer-base, Tokenizer-2k); large unreleased | 4.1M (ctx 2048), 24.7M, 102.3M (ctx 512); 499M closed | 12B+ K-lines, 45 exchanges, 7 frequencies, pre-train to 2024-06. **Includes NSE and BSE**, also NYSE/NASDAQ, crypto and FX | In: OHLCV(+amount) plus timestamps. Out: sampled future OHLCV paths (probabilistic via T/top_p/sample_count), volatility, synthetic K-lines | RankIC +93% vs best TSFM; vol MAE −9%; generative fidelity +22%. Out-of-sample from Jul-2024. Backtest only on CN A-shares at 0.15% cost; no India/US backtest; 25 baselines, self-reported | 4 | 0 | 0 | 3 | H |
| **FinCast** | vincent05r/FinCast-fts (131 stars); HF Vincent05R/FinCast | arXiv 2508.19609, **CIKM 2025** | commit 2026-06-22 | Apache-2.0 | Apache-2.0 | 1B sparse MoE (4 experts, top-2) | 20B+ points: stock 44%, FX 16%, crypto 9%, futures 8%, other 22%, "public APIs". **India not mentioned** | Any-length univariate series. Out: point + quantiles | Zero-shot, supervised and few-shot MSE/MAE wins vs TSFMs. **No trading backtest, no costs**. HF download counter shows 0, so an independent sanity check is needed | 3 | 0 | 0 | 3 | M |
| **FinText TSFMs** (the real "TimesFM-finance" / "Chronos-finance") | HF org FinText: 216 Chronos + 144 TimesFM checkpoints | Rahimikia et al., arXiv 2511.18578 | HF 2025-11 | n/a | Apache-2.0 (checked Chronos_Small_2023_Global) | Chronos Tiny/Mini/Small (8–46M), TimesFM 8M/20M | Daily excess returns, 89 markets, about 2B observations, **year-vintage expanding window** (no look-ahead). Global vs US variants; India is presumably inside "Global" but this is unverified | Returns in, returns out | Finance-native pre-training closes much of the gap to CatBoost/LightGBM; zero-shot generic TSFMs are weak. Portfolio results reported | 3 | 0 | 0 | 2 | M |
| MarS / Large Market Model | microsoft/MarS (1.8k stars) | arXiv 2409.07486, **ICLR 2025** | release v0.1.0 2026-09-24 (security fix replacing pickle) | MIT | 2M/5M/10M order models released; larger "pending approval" | 2–10M released | Order-level data (Chinese market, per paper; unverified here) | Orders in, simulated order flow / market impact out | Stylised-fact realism, market-impact demos. Needs full order-level data | 1 | 0 | 0 | 2 | M |
| TRADES (DeepMarket) | LeonardoBerti00/DeepMarket (110 stars) | arXiv 2502.07071 | 2026-01-27 | MIT | checkpoints released (per paper) | — | LOBSTER US LOB (TSLA/INTC per paper; unverified) | LOB diffusion simulator | Realism metrics on LOB-Bench | 0 | 0 | 0 | 1 | M |
| LOBS5 | peernagy/LOBS5 (32 stars) | cited in LOB-Bench | 2026-03-10 | MIT | — | — | LOBSTER | Message-level LOB generation | Best on most LOB-Bench scores (self-reported by the same group) | 0 | 0 | 0 | 1 | M |
| StockMixer | SJTU-DMTai/StockMixer (378 stars) | AAAI 2024 (venue from memory; unverified) | 2024-03-19 | **NOLIC** | — | small MLP | NASDAQ/NYSE/S&P500 | Per-stock returns | Ranking return metrics, no costs | 1 | 0 | 0 | 0 | M |
| Time-MoE (general) | Time-MoE/Time-MoE (1.0k stars); HF Maple728 | ICLR 2025 (from memory; unverified) | 2026-03-21 | Apache-2.0 | Apache-2.0 | 50M/200M released | Time-300B, general and **not finance-specific** | Univariate | General TSF benchmarks | 2 | 0 | 0 | 1 | M |
| Moirai-2.0 (general) | SalesforceAIResearch/uni2ts | — | 2026-06-02 | Apache-2.0 | **CC-BY-NC-4.0 (NC)** | small+ | General | — | Strong in the 2606.27100 US-stocks ranking | 0 (NC) | 0 | 0 | 0 | H |
| Chronos-Bolt / Chronos-2 (general) | amazon-science/chronos-forecasting; PyPI chronos-forecasting 2.3.2 (2026-09-08) | Chronos-2 arXiv 2510.15821 | 2026-09-17 | Apache-2.0 | Apache-2.0 | 9M–710M | General (<1% finance) | — | Generic baseline; weak zero-shot on returns (Rahimikia) | 2 | 0 | 0 | 1 | H |
| TimesFM 2.5 (general) | google-research/timesfm; PyPI timesfm 3.0.2 (2026-09-09) | — | 2026-09-15 | Apache-2.0 | Apache-2.0 | 200M | General | — | Best average rank on 5 US stocks in 2606.27100, but tiny edge over random walk | 2 | 0 | 0 | 1 | H |
| IBM TTM r2 (general) | HF ibm-granite/granite-timeseries-ttm-r2 | — | 2025-02 | — | Apache-2.0 | <1M–5M | General | — | **Only TSFM to beat Log-HAR on realized vol** in 2607.05291, by 1.3–1.8% | 2 | 0 | 0 | 3 | M |

**Benchmarks in this family:**

- **FinTSB**
  - Repo: TongjiFinLab/FinTSB, 132 stars.
  - Licence: **GPL-3.0**.
  - Paper: arXiv 2502.18834, Frontiers of CS 2026 and ICAIF-W 2025 best paper.
  - Data: Chinese market.
- **LOB-Bench**
  - Repo: peernagy/lob_bench, 46 stars, **NOLIC**.
  - Paper: arXiv 2502.09172, **ICML 2025**.
  - Use: for LOB generators only.

**Not found as named:**

- "Moirai-finance": HF search `moirai-fin` returns only one hobby fine-tune.
- "TimeGPT-finance": no product found. TimeGPT is a closed Nixtla API and is excluded by 2607.05291 for reproducibility.
- "Chronos-Bolt fine-tuned on stocks": the closest real artefact is FinText.
- A direct *successor* to Kronos: none found. arXiv 2607.26792 "Crossing-Free Probabilistic K-Line Forecasts Without Retraining" is a post-processing add-on and was not read in full.

## 2. Financial LLMs

| Model | Repo / HF | Paper, venue | Activity | Code lic | Weights lic | Sizes / base | Data (India?) | Reported results | F | S | Q | R | Conf |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **FinGPT** (incl. Forecaster, FinGPT-MT) | AI4Finance-Foundation/FinGPT (21.3k stars); HF FinGPT/* | arXiv 2306.06031 (FinGPT); FinGPT benchmark papers | release v1.0.0 2026-04-08 (marketing-style notes, low information); PyPI `fingpt` 0.0.1 is stale | MIT | LoRA adapters Apache-2.0/MIT, **but the base is Llama-2 / Llama-3 / Qwen, so the base licence applies** | 7–8B LoRA | US news/Dow30 (forecaster), public sentiment sets. No India | Forecaster: next-week up/down on Dow30, no cost-aware backtest | 1 | 3 | 1 | 0 | M |
| **Fin-R1** | SUFE-AIFLM-Lab/Fin-R1 (817 stars); HF | arXiv 2503.16252 (tech report) | 2025-03 | README badge says Apache-2.0 but there is **no LICENSE file** (flag) | same, no HF licence tag | 7B, Qwen2.5-7B | 60k distilled CoT (DeepSeek-R1 teacher), mostly Chinese plus FinQA/ConvFinQA. No India | FinQA 76.0, ConvFinQA 85.0; avg 75.2 vs DeepSeek-R1 78.2 (self-reported) | 0 | 1 | 3 | 1 | M |
| **DianJin-R1** | aliyun/qwen-dianjin (621 stars, MIT); HF DianJin | arXiv 2504.15716 | 2026-08-28 | MIT | MIT (7B, 32B) | Qwen2.5-7B/32B | CFLUE, FinQA, Chinese compliance corpus. Chinese-heavy | Beats non-reasoning bases on CFLUE/FinQA/CCC | 0 | 1 | 3 | 1 | M |
| Palmyra-Fin | HF Writer/Palmyra-Fin-70B-32K | Writer blog 2024-07 | 2025-01 | — | **Writer open model licence, NC only; commercial use needs a Writer grant** | 70–72B | English finance | CFA-style claims (marketing) | 0 | 2 | 3 | 1 | H (licence) |
| FinMA / PIXIU | The-FinAI/PIXIU (888 stars, MIT); HF ChanceFocus/finma-7b-full (gated) | NeurIPS 2023 D&B | 2025-03 | MIT | tagged MIT but LLaMA-1 base (**NC upstream**, flag) | 7B/30B | FLARE instruction data | Superseded | 0 | 2 | 1 | 0 | M |
| XuanYuan | Duxiaoman-DI/XuanYuan (1.3k stars) | reports in repo | 2025-01 | **NOLIC** | 6B: **Llama-2** licence | 6B–70B | Chinese finance | Chinese evals | 0 | 0 | 1 | 0 | M |
| CFGPT | TongjiFinLab/CFGPT (97 stars) | arXiv 2309.10654 (from memory) | 2026-06-03 | Apache-2.0 | not checked | 7B | Chinese | Chinese | 0 | 0 | 1 | 0 | L |
| InvestLM | AbaciNLP/InvestLM (156 stars); HF yixuantt/InvestLM-mistral-AWQ | arXiv 2309.13064 (from memory) | 2024-11 | **NOLIC** | not checked; original was LLaMA-65B based (NC upstream) | 65B / Mistral AWQ | English CFA/SEC | small self-evaluation | 0 | 1 | 2 | 0 | L |
| AdaptLLM finance-chat | HF AdaptLLM/finance-chat | ICLR 2024 (from memory) | 2024-12 | — | **Llama-2** | 7B | English | — | 0 | 1 | 1 | 0 | M |
| BloombergGPT | closed | arXiv 2303.17564 | — | — | not available | 50B | Bloomberg | — | n/a | n/a | n/a | n/a | H |
| finance-Llama3-8B | HF instruction-pretrain/finance-Llama3-8B (7k downloads) | Instruction Pre-Training, arXiv 2406.14491 | 2026-03 | — | **Llama-3 licence** | 8B | English finance corpora | domain-benchmark gains (self-reported) | 0 | 2 | 2 | 0 | M |
| Finance-Llama-8B (community) | HF tarun7r/Finance-Llama-8B | none | 2026-02 | — | tagged Apache-2.0, but the **base is Llama-3.1, so Llama-3.1 terms still apply** (flag) | 8B | not published | none | 0 | 1 | 1 | 0 | L |
| India-specific LLMs | none credible (see §0.7) | — | — | — | — | — | — | — | — | — | — | — | H (null) |

## 3. Financial NLP (encoders)

| Model | Repo / HF | Paper, venue | Code lic | Weights / data lic | Data (India?) | Notes | S | Q | Conf |
|---|---|---|---|---|---|---|---|---|---|
| **ProsusAI/finbert** | ProsusAI/finBERT (2.2k stars, Apache-2.0, last push 2022-09); HF 5.1M downloads | arXiv 1908.10063 | Apache-2.0 | HF card has **no licence tag**. Fine-tuned on Financial PhraseBank, **verified CC-BY-NC-SA-3.0** (HF `takala/financial_phrasebank` tag). **Data-rights flag for commercial use**: whether the NC data licence reaches the weights is a legal question; flag it for legal review | English news, no India | 3-class pos/neg/neu; the de-facto baseline | 3 | 0 | H |
| **yiyanghkust/finbert-tone** | yya518/FinBERT (Apache-2.0); HF 1.2M downloads | Huang, Wang, Yang, Contemp. Acct. Research 2023 (from memory) | Apache-2.0 | HF card NOLIC tag | 10-K/10-Q, calls, analyst reports (4.9B tokens) | Also has finbert-esg | 3 | 1 | H |
| **FinBERT2** | valuesimplex/FinBERT (940 stars, MIT) | arXiv 2506.06335, **KDD 2025 ADS** | MIT | HF valuesimplex-ai-lab/FinBERT2-base is Apache-2.0 | **Chinese** 32B tokens, so not usable for English/Hindi without work | Strong retrieval/embeddings, Chinese only | 1 | 1 | H |
| SEC-BERT | HF nlpaueb/sec-bert-base | FiNER paper, ACL 2022 | — | **CC-BY-SA-4.0** | EDGAR filings | Good for numeric tokens in filings | 1 | 2 | H |
| FiNER-139 (dataset) | nlpaueb/finer (MIT code) | ACL 2022 | MIT | dataset **CC-BY-SA-4.0** | 10-K XBRL tags | XBRL NER training data | — | 2 | H |
| FLANG-BERT / FLUE | SALT-NLP/FLANG (Apache-2.0) | EMNLP 2022 | Apache-2.0 | HF card NOLIC tag | English | Superseded | 2 | 1 | M |
| EconBERTa | worldbank/econberta-econie (NOLIC) | EMNLP Findings 2023 | **NOLIC** | HF ID not found at `worldbank/econberta-fs` via API | Economics papers | Out of scope | 0 | 0 | M |
| FinBERT-India-v1 (community) | HF Vansh180 | none | — | MIT | "India-focused articles", custom dataset, not published | acc 0.77 self-reported; hobby | 2 | 0 | L |
| AI4Invest-Indian-FinBERT (community) | HF sapt3009 | none | — | no tag | **Trained on a US Twitter dataset**; mislabelled as Indian | Do not use as an "India" model | 1 | 0 | H (mislabel) |

## 4. Toolkits and platforms

| Toolkit | Repo (stars) | Latest release (registry) | Licence | India support | What it gives us | F | S | Q | R | Conf |
|---|---|---|---|---|---|---|---|---|---|---|
| **Microsoft Qlib** | microsoft/qlib (48.8k) | **pyqlib 0.9.7, 2025-08-15**; repo active 2026-09-22 | MIT | Yahoo collector supports `region IN` (Yahoo ToS is a **data-rights** issue) | Factor library (Alpha158/360), model zoo, backtester; Kronos paper and fine-tune scripts use it | 4 | 0 | 0 | 3 | H |
| **RD-Agent (Q)** | microsoft/RD-Agent (14.7k) | **rdagent 1.0.0, 2026-09-23** | MIT | via Qlib | LLM agent for factor/model R&D. arXiv 2505.15155, **NeurIPS 2025**: about 2x ARR vs Alpha158 with 70% fewer factors, CN market, <$10/cycle (self-reported) | 3 | 0 | 0 | 1 | H |
| **TA-Lib** | TA-Lib/ta-lib-python (12.3k) | **TA-Lib 0.8.1, 2026-09-21** (author mrjbq7, matches) | BSD-2 (wrapper); C lib BSD | market-agnostic | 150+ indicators: RSI, MACD, patterns. Deterministic, sub-ms | 3 | 0 | 0 | 2 | H |
| **skfolio** | skfolio/skfolio (2.4k) | **1.3.1, 2026-09-23** | BSD-3 | agnostic | sklearn-style portfolio/risk (CVaR, HRP, cross-validation) | 0 | 0 | 0 | 4 | H |
| **PyPortfolioOpt** | PyPortfolio/PyPortfolioOpt (6.1k; moved org) | **1.6.0, 2026-02-26** | MIT | agnostic | MVO, Black-Litterman, HRP | 0 | 0 | 0 | 3 | H |
| **TradingAgents** | TauricResearch/TradingAgents (108k) | **GitHub v0.5.1, 2026-09-24**. PyPI `tradingagents` 0.7.0 is a **third-party look-alike** (Mai0313) | Apache-2.0 | yfinance/Alpha Vantage/EDGAR vendors; India via Yahoo `.NS` | Multi-agent analyst/trader LLM graph; **Jev screening built in** (v0.5.1). Paper arXiv 2412.20138: backtest Jan–Mar 2024 on 5 US mega-caps, short window (FINSABER critique applies) | 1 | 2 | 2 | 1 | H |
| **FinRobot** | AI4Finance-Foundation/FinRobot (8.1k) | GitHub desktop-v0.1.0, 2026-07-07; PyPI 0.1.5 (2024, stale) | Apache-2.0 | US-centric | Agent platform for equity-research reports | 0 | 1 | 3 | 1 | M |
| FinRL / FinRL-Meta / FinRL-DeepSeek | FinRL (16.4k), Meta (1.9k), DeepSeek (137) | GitHub v0.3.8, 2026-03-20; PyPI finrl 0.3.7 (2024) | MIT | FinRL-Meta has env adapters (India unverified) | RL trading research; not product-grade | 1 | 0 | 0 | 1 | M |
| FinMem | pipiku915/FinMem-LLM-StockTrading (960) | 2024-08 | MIT | no | Memory-agent trading research | 0 | 1 | 0 | 0 | M |
| FinAgent | paper only (KDD 2024, NTU); **no official repo found** | — | — | no | Multimodal trading agent | 0 | 0 | 0 | 0 | M |
| OpenBB (ODP) | OpenBB-finance/OpenBB (73k) | openbb 4.7.2, 2026-05-26; "Open Data Platform" desktop 1.0.2 | **AGPL-3.0** (flag) | provider plugins | Data-connector layer | 1 | 1 | 1 | 1 | H |
| vectorbt | polakowo/vectorbt (9.2k) | 1.1.0, 2026-07-05 | **Apache-2.0 + Commons Clause** (flag: no selling) | agnostic | Fast vectorised backtests; internal research only | 1 | 0 | 0 | 2 | H |
| NautilusTrader | nautechsystems/nautilus_trader (29k) | 1.231.0, 2026-08-02 | **LGPL-3.0** (flag, mild) | adapters; India unverified | Event-driven trading engine; out of scope unless executing | 0 | 0 | 0 | 1 | H |

## 5. Evaluation suites

| Suite | Where | Venue | Licence | India? | Use for us | Conf |
|---|---|---|---|---|---|---|
| **IndiaFinBench** | arXiv 2604.19298 (GitHub link in paper, not fetched) | preprint 2026-04 | not checked | **Yes**: 406 QA from 192 SEBI/RBI docs. Zero-shot 70.4% (Gemma 4 E4B) to 89.7% (Gemini 2.5 Flash) | Q gate for any India regulatory QA | M |
| **FinQA** | czyssrs/FinQA (MIT) | EMNLP 2021 | MIT | no | Numeric QA over tables | H |
| **FinBen / PIXIU / FLARE** | The-FinAI/PIXIU (MIT), FinBen repo NOLIC | NeurIPS 2024 D&B (FinBen) | mixed per dataset | no | Broad task suite; take the sentiment subsets for S | M |
| **Open FinLLM Leaderboard** | HF Space TheFinAI/Open-FinLLM-Leaderboard; also finosfoundation; code Open-Finance-Lab/FinLLM-Leaderboard (MIT) | arXiv 2501.10963 | MIT | no | Model shortlist | M |
| **FinanceBench** | patronus-ai/financebench (NOLIC repo) | arXiv 2311.11944 | dataset **CC-BY-NC-4.0** (flag) | no | Internal eval only, never ship or train on it | H |
| **BizBench** | HF kensho/bizbench | ACL 2024 | Apache-2.0 (HF tag) | no | Program-synthesis QA | H |
| **FinTSB** | TongjiFinLab/FinTSB | FCS 2026 / ICAIF-W 2025 | **GPL-3.0** | no (CN) | Methodology reference for F-feature evals | H |
| **LOB-Bench** | peernagy/lob_bench | ICML 2025 | NOLIC | no | N/A for us | H |
| FINSABER | arXiv 2505.07078 | **KDD 2026 D&B oral** | not checked | no | Required reading before any agent/LLM trading claim | H |

## 6. Constraints that shape the scores

- **Latency.** Kronos and FinCast are sampling-based generative models. Run them **precomputed or batch**, e.g. EOD or intraday refresh into the answer-card store. They do not belong on the ~300 ms live path. This matches the existing router plus precomputed-card design.
- **Data rights are separate from model licence.**
  - Fine-tuning Kronos on NSE/BSE bars raises the NSE data-licensing issue already documented in `docs/production-plan/research/india-market-data-and-sebi.md`.
  - Qlib's Yahoo collector (`region IN`) inherits the Yahoo ToS.
  - Kronos pre-training corpus provenance is **undisclosed**, so its data-rights status is unknown. Flag it for legal; the MIT weights licence and the data rights are separate questions.
- **Regulation.** Showing price forecasts to Indian retail users likely engages SEBI Research Analyst / Investment Adviser rules. See the existing SEBI doc; not re-researched here. Present forecasts as an uncertainty band or feature, with disclaimers, subject to legal review.

## 7. Ranked recommendation

1. **Kronos-small (then -base) as the forecasting feature.**
   - Why: MIT code and weights; NSE and BSE are in the pre-training data; out-of-sample test split; fine-tune path via `finetune_csv`.
   - How: run in batch, and output a probabilistic band plus a volatility estimate.
   - Gate: before any UI exposure, run our own walk-forward eval on NIFTY 500 and S&P 500 against naive/HAR/LightGBM baselines, net of costs.
2. **TA-Lib + Qlib (pyqlib) as the deterministic indicator and factor backbone.** Qlib also hosts the Kronos eval harness. Use RD-Agent(Q) for offline factor research only.
3. **FinBERT family for sentiment.**
   - Use finbert-tone for filings and calls. Its labelled-data provenance is unchecked.
   - ProsusAI/finbert is fine as an *internal baseline only*, because it was trained on Financial PhraseBank, which is CC-BY-NC-SA-3.0.
   - For product use, fine-tune our own encoder on an English + Hindi India-news labelled set. No credible India model exists.
   - `zeroshot/twitter-financial-news-sentiment` (MIT) is a usable commercial seed set.
4. **skfolio (primary) and PyPortfolioOpt for risk** (BSD/MIT). Consider IBM TTM r2 or plain HAR for realized-vol features, given 2607.05291.
5. **For QA over filings, use a general LLM plus retrieval, gated by FinQA, BizBench and IndiaFinBench.** DianJin-R1 (MIT) or Fin-R1 (Apache per badge, no LICENSE file) could be self-host options, but they are Chinese-centric. Palmyra-Fin is NC.
6. **Assess only:**
   - FinCast (Apache, 1B; verify weights and India transfer).
   - FinText TSFMs (vintage-clean baselines, useful for leakage-free evaluation).
   - TradingAgents (Apache; already Jev-integrated, but agent-trading claims are weak per FINSABER).
7. **Hold:**
   - OpenBB (AGPL).
   - vectorbt in product (Commons Clause).
   - Moirai-2.0 and Palmyra-Fin (NC).
   - FinanceBench as training data (NC).
   - FinGPT-Forecaster as a signal (Llama-2 base, short-window evaluation).
   - MarS, TRADES and LOBS5 (order-level data we don't have).

**Proposed radar rings (for tech-lead; the radar file was not edited):**
- **Trial:** Kronos, TA-Lib, pyqlib, FinBERT-tone/ProsusAI, skfolio.
- **Assess:** FinCast, FinText, RD-Agent, TradingAgents, DianJin-R1, Fin-R1, IndiaFinBench.
- **Hold:** OpenBB, vectorbt, Moirai-2.0, Palmyra-Fin, FinanceBench-as-train, `qlib`/`kronos`/`tradingagents` PyPI look-alikes.

**What would change this ranking:**
- An independent (non-author) India walk-forward eval showing Kronos ≤ a LightGBM/HAR baseline net of costs would demote it to Assess.
- A Kronos-large release, or a successor with a published India backtest, would promote it.
- An NSE data licence that forbids model training would block fine-tuning and leave zero-shot only.
- A credible English + Hindi India finance encoder appearing would replace step 3.

## 8. Unverified list

- Kronos-large release status beyond "not on HF, README says not open-source". Also Kronos pre-training data vendors and licence.
- FinCast HF weights actually loadable. The HF download counter shows 0; the sizes in the checkpoint are not inspected.
- FinText "Global" including India.
- MarS training market. TRADES and LOBS5 datasets.
- StockMixer, Time-MoE, InvestLM, CFGPT, AdaptLLM and FinMem venues (from memory).
- Exact Kronos column mapping in the XNSE results table (the HTML duplicates MathML text).
- finbert-tone labelled-data licence.
- Fin-R1 licence: badge-only, no LICENSE file.
- CFGPT weights licence; InvestLM weights licence.
- IndiaFinBench licence and repo.
- FinRL-Meta India environments; NautilusTrader India adapters.
- EconBERTa current HF ID.
- arXiv 2607.26792 (K-line forecast post-processing) not read.

## Sources (all accessed 2026-09-24)

- Kronos: https://github.com/shiyu-coder/Kronos ; https://arxiv.org/html/2508.02739 ; https://huggingface.co/NeoQuasar
- FinCast: https://github.com/vincent05r/FinCast-fts ; https://arxiv.org/abs/2508.19609 ; https://huggingface.co/Vincent05R/FinCast ; https://dl.acm.org/doi/10.1145/3746252.3761261
- FinText: https://huggingface.co/FinText ; https://arxiv.org/abs/2511.18578
- Independent TSFM evals: https://arxiv.org/abs/2607.05291 ; https://arxiv.org/abs/2606.27100 ; FINSABER https://arxiv.org/abs/2505.07078
- MarS: https://github.com/microsoft/MarS ; https://iclr.cc/virtual/2025/poster/29246
- TRADES: https://github.com/LeonardoBerti00/DeepMarket ; https://arxiv.org/abs/2502.07071
- LOB-Bench: https://arxiv.org/abs/2502.09172 ; https://github.com/peernagy/lob_bench ; LOBS5 https://github.com/peernagy/LOBS5
- FinTSB: https://github.com/TongjiFinLab/FinTSB ; https://arxiv.org/abs/2502.18834
- StockMixer: https://github.com/SJTU-DMTai/StockMixer
- Time-MoE: https://github.com/Time-MoE/Time-MoE
- uni2ts/Moirai: https://huggingface.co/Salesforce/moirai-2.0-R-small
- Chronos: https://pypi.org/pypi/chronos-forecasting/json
- TimesFM: https://pypi.org/pypi/timesfm/json
- TTM: https://huggingface.co/ibm-granite/granite-timeseries-ttm-r2
- FinGPT: https://github.com/AI4Finance-Foundation/FinGPT ; https://huggingface.co/FinGPT/fingpt-forecaster_dow30_llama2-7b_lora
- Fin-R1: https://github.com/SUFE-AIFLM-Lab/Fin-R1 ; https://arxiv.org/abs/2503.16252
- DianJin-R1: https://github.com/aliyun/qwen-dianjin ; https://huggingface.co/papers/2504.15716
- Palmyra-Fin: https://huggingface.co/Writer/Palmyra-Fin-70B-32K ; https://writer.com/legal/open-model-license/
- PIXIU/FinMA: https://github.com/The-FinAI/PIXIU
- XuanYuan: https://github.com/Duxiaoman-DI/XuanYuan
- CFGPT: https://github.com/TongjiFinLab/CFGPT
- InvestLM: https://github.com/AbaciNLP/InvestLM
- FinBERT: https://huggingface.co/ProsusAI/finbert ; https://huggingface.co/yiyanghkust/finbert-tone ; https://github.com/valuesimplex/FinBERT ; https://arxiv.org/abs/2506.06335
- SEC-BERT: https://huggingface.co/nlpaueb/sec-bert-base
- FiNER: https://github.com/nlpaueb/finer
- FLANG: https://github.com/SALT-NLP/FLANG
- EconBERTa: https://aclanthology.org/2023.findings-emnlp.774/
- Community India models: https://huggingface.co/Vansh180/FinBERT-India-v1 ; https://huggingface.co/sapt3009/AI4Invest-Indian-FinBERT
- Qlib: https://github.com/microsoft/qlib ; https://pypi.org/pypi/pyqlib/json ; look-alike https://pypi.org/pypi/qlib/json
- RD-Agent: https://github.com/microsoft/RD-Agent ; https://arxiv.org/abs/2505.15155
- TA-Lib: https://pypi.org/pypi/TA-Lib/json
- skfolio: https://pypi.org/pypi/skfolio/json
- PyPortfolioOpt: https://pypi.org/pypi/pyportfolioopt/json
- TradingAgents: https://github.com/TauricResearch/TradingAgents/releases ; https://arxiv.org/abs/2412.20138 ; look-alike https://pypi.org/pypi/tradingagents/json
- FinRobot: https://github.com/AI4Finance-Foundation/FinRobot
- FinRL: https://github.com/AI4Finance-Foundation/FinRL
- FinMem: https://github.com/pipiku915/FinMem-LLM-StockTrading
- FinAgent: https://arxiv.org/abs/2402.18485
- OpenBB: https://github.com/OpenBB-finance/OpenBB (LICENSE on develop)
- vectorbt: https://github.com/polakowo/vectorbt (LICENSE.md)
- NautilusTrader: https://pypi.org/pypi/nautilus_trader/json
- Evaluation suites:
  - IndiaFinBench: https://arxiv.org/abs/2604.19298
  - FinQA: https://github.com/czyssrs/FinQA
  - FinBen: https://proceedings.neurips.cc/paper_files/paper/2024/file/adb1d9fa8be4576d28703b396b82ba1b-Paper-Datasets_and_Benchmarks_Track.pdf
  - Open FinLLM Leaderboard: https://huggingface.co/spaces/TheFinAI/Open-FinLLM-Leaderboard ; https://arxiv.org/abs/2501.10963
  - FinanceBench: https://huggingface.co/datasets/PatronusAI/financebench
  - BizBench: https://aclanthology.org/2024.acl-long.452/
