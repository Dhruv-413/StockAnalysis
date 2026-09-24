# Research: Accuracy, reliability and honest claims for an AI trading assistant (India F&O/equities, US, global)

Research date: 2026-09-24. Author role: Quant Researcher. Status: research input for 06-quantitative-validation.md and research/papers.md, not a decision.
Labels: **[V]** verified fact, with a source and confidence H/M/L. **[I]** inference. **[A]** assumption. **[P]** proposal or spec (ours; no external source). **[U]** unverified.
All URLs accessed on 2026-09-24 unless stated otherwise.

---

## 0. Executive summary

1. **"Canonical" indicators do not exist across platforms.** RSI, EMA, MACD, ATR and Supertrend differ by smoothing type, seeding, warm-up length, bar alignment, whether the live (forming) bar is included, and close definition. We must publish our own versioned spec. TA-Lib and TradingView are *oracles*, not definitions. Tolerances only apply after a derived warm-up: 125 bars for RSI(14)/RMA and about 65 bars for EMA(14) to reach a 1e-4 residual seed weight.
2. **India market microstructure changed repeatedly between Nov 2024 and Sep 2026**, and all of it must be point-in-time data:
   - weekly expiry limited to one index per exchange (Nov 2024);
   - NSE expiry on Tuesday and BSE on Thursday (from 1 Sep 2025);
   - lot-size revisions (Nifty 75 → 65, Jan 2026 series);
   - F&O pre-open session (8 Dec 2025);
   - closing auction session (CAS) for F&O stocks (3 Aug 2026);
   - new pre-open phases (7 Sep 2026);
   - an open SEBI consultation on the expiry-day settlement price (Sep 2026).
3. **Evidence on retail outcomes is bleak.**
   - SEBI: 91% of individual F&O traders lost money in FY25 (July 2025 study, top-13 brokers) and 87.7% in FY26 (Aug 2026 study, top-15 brokers, about 90% of individuals). About 92% of FY26 losses came from options.
   - Academic evidence shows technical-rule profits do not survive data-snooping control plus costs (Bajgrowicz & Scaillet 2012).
   - LLM trading benchmarks show no robust edge.
   - **The product must not claim profitability, predictive accuracy or "signals that work".**
4. **Regulation limits what the assistant may offer. This is for counsel, not a legal verdict.**
   - Black-box algos need a SEBI Research Analyst (RA) registration.
   - All API algo orders need an exchange algo ID via an empanelled provider and broker.
   - "Education" may not use prices from the last 3 months.
   - Past-performance claims must go through PaRRVA (operational from 4 May 2026).
   - RAs must disclose their use of AI.
   - Showing live indicators and "algo signals" is therefore unlikely to count as "education".
5. **Reliability comes from architecture, not from model choice.**
   - A deterministic engine produces every number; the LLM only phrases.
   - A post-generation check verifies every numeral against the engine or refuses.
   - Staleness-based abstention.
   - Instruments keyed on ISIN plus exchange token.
   - Precomputed indicator snapshots, to fit roughly 300 ms.
   - No published source gives hallucination rates for fast small LLMs on this task, so we must measure them ourselves.

---

## 1. Indicator correctness

### 1.1 Known cross-platform discrepancies (evidence)

| Item | Finding | Source | Conf. |
|---|---|---|---|
| TradingView RSI | `avgGain = rma(gain,14)`, `avgLoss = rma(loss,14)`, i.e. Wilder smoothing, "exactly equal to rsi(close,14)" | https://www.tradingview.com/support/solutions/43000502338-relative-strength-index-rsi/ | H |
| TradingView RMA seed | `ta.rma` seeds with an SMA of the first *n* values | Pine reference (recall; the page did not render) | M [U] |
| TradingView EMA seed | `sum := na(sum[1]) ? src : alpha*src + (1-alpha)*nz(sum[1])`, i.e. it seeds with the **first source value**, not an SMA | https://pineify.app/pine-script-ta-ema (third-party reproduction of the Pine reference) | M |
| TA-Lib EMA/RSI | Recursive indicators "have memory ... seeded from the start of the data". The unstable period defaults to 0 (no warm-up bars discarded). About 23 functions are affected, including EMA, RSI, ATR, ADX and KAMA | https://ta-lib.org/api/unstable-period/ | H |
| TA-Lib 0.6.x bug | C 0.6.0 inserted `TA_FUNC_UNST_IMI` at slot 12, so `set_unstable_period('RSI')` targets the wrong function ID in ta-lib-python built against 0.6.x | https://github.com/TA-Lib/ta-lib-python/issues/664 (search snippet) | M. Fix status in 0.6.8 [U] |
| TA-Lib versions | ta-lib-python 0.6.x supports NumPy 2. Binary wheels bundling the C library ship from 0.6.5. PyPI shows 0.6.8 | https://github.com/TA-Lib/ta-lib-python/blob/master/CHANGELOG ; https://libraries.io/pypi/TA-Lib | M |
| Zerodha Kite RSI | Kite/ChartIQ reportedly uses EMA-type smoothing, not Wilder. Kite Connect developers see mismatches from the start timestamp and warm-up length, and are advised to use 2–3× N extra candles | https://kite.trade/forum/discussion/12213/ ; https://kite.trade/forum/discussion/13014/calculation-of-rsi | L (forum posts; not an official spec) |
| RSI smoothing | EMA-smoothed RSI can run "3–7 points" away from Wilder RSI in trends | https://rsimonitor.com/articles/wilder-smoothing | L (blog). Our fixture shows 87.5 vs 84.6 on 5 bars |
| TradingView VWAP | Anchor = Session/Week/Month/…/Earnings/Dividends/Splits. Source default `hlc3`. Extended hours change the line | https://www.tradingview.com/support/solutions/43000502018-volume-weighted-average-price-vwap/ (via search) | M |
| TradingView ATR | Default RMA of the true range; SMA/EMA/WMA are selectable | https://www.tradingview.com/support/solutions/43000501823-average-true-range-atr/ (via search) | M |
| TradingView Supertrend | `hl2 ± mult·ATR`; band carry-forward rules as in §1.3; starts as a downtrend | https://www.tradingview.com/support/solutions/43000634738-supertrend/ | H |
| pandas-ta | The maintainer announced archival on 1 July 2026 unless funded; a yearly release cadence. Last release seen: 14 Sep 2025. Snyk rates it "Inactive". The canonical repo location has moved (twopirllc returns 404) | https://pypi.org/project/pandas-ta/ ; https://snyk.io/advisor/python/pandas-ta ; https://github.com/twopirllc/pandas-ta (404) | M. Post-July-2026 status [U] |
| talipp | Incremental O(1) updates; v2.7.0 | https://github.com/nardew/talipp ; https://nardew.github.io/talipp/2.7.0/ | M. Seeding conventions per indicator [U] |
| polars_ta | Several unrelated projects share the name (wukan1986/polars_ta for Python; Rust crates) | https://github.com/wukan1986/polars_ta ; https://crates.io/crates/polars-ta | M. Maintenance and seeding [U] |
| tulipy | Not researched this session | — | [U] |

**[I]** The dominant sources of "your RSI is wrong" complaints are, in order:
1. EMA vs Wilder smoothing;
2. seed and warm-up length;
3. including the forming (live) bar;
4. bar alignment and session boundaries, such as a 09:15 anchor and pre-open or auction prints;
5. the close definition (last traded price vs official close);
6. adjusted vs unadjusted history.

Floating-point differences between TA-Lib versions are about 1e-13 and negligible.

### 1.2 India-specific facts that affect computations

| Item | Fact | Source | Conf. |
|---|---|---|---|
| Normal session | 09:15–15:30 IST continuous | NSE (general knowledge; https://www.nseindia.com/resources/exchange-communication-holidays) | H |
| Equity pre-open (from 7 Sep 2026) | 09:00–09:05: market and limit orders. 09:05–09:10: limit only, with a random close in the last 2 minutes. 09:10–09:12: matching. 09:12–09:15: buffer | https://www.kotakneo.com/news/trading/nse-pre-open-session-new-order-rules-7-september/ ; Business Standard 2026-09-07 (403) | M (secondary; get the NSE circular) |
| F&O pre-open | Since 8 Dec 2025: 09:00–09:15, order entry with a random close around 09:07–09:08, matching until 09:12 | https://www.business-standard.com/markets/capital-market-news/nse-to-commence-pre-opening-session-in-f-o-segment-from-december-08-125110400728_1.html | M |
| Closing Auction Session | From 3 Aug 2026 for Category I (F&O-enabled) stocks. CAS runs 15:15–15:30; the close is finalised between 15:30 and 15:35. The reference price is the VWAP from 15:00 to 15:15, with a ±3% band. It **replaces** the old close (VWAP of the last 30 minutes). Other stocks keep the old method | https://nsearchives.nseindia.com/content/circulars/CMTR73362.pdf (not fetched) ; https://www.business-standard.com/markets/capital-market-news/sebi-changes-closing-price-calculation-methodology-for-equity-cash-segment-126011700338_1.html ; https://groww.in/blog/closing-auction-session | M. Whether continuous trading halts at 15:15 for Category I [U] |
| Expiry-day settlement consultation | SEBI consultation (12 Sep 2026; comments until 3 Oct 2026). Option 1 is a "Blended VWAP" settlement price, plus changes to CAS/IEP | https://www.deccanherald.com/business/sebi-proposes-changes-to-expiry-day-settlement-price-methodology-floats-consultation-paper-4144062 | M |
| Expiry days | From 1 Sep 2025, NSE contracts (weekly, monthly, quarterly, half-yearly) expire on **Tuesday** and BSE's on **Thursday** (SEBI circular of 26 May 2025) | https://www.zeebiz.com/market-news/news-sebi-approves-nse-expiry-day-change-to-tuesday-and-bse-expiry-day-shifted-to-thursday-370127 ; https://www.newsonair.gov.in/nse-bse-swap-derivatives-expiry-days | M (secondary; SEBI circular not fetched) |
| Weekly expiry limit | One benchmark index per exchange (Nifty 50 on NSE; Sensex on BSE), effective 20 Nov 2024. Minimum contract value ₹15 lakh, set at ₹15–20 lakh at review | https://www.sebi.gov.in/legal/circulars/oct-2024/measures-to-strengthen-equity-index-derivatives-framework-for-increased-investor-protection-and-market-stability_87208.html ; https://zerodha.com/z-connect/business-updates/sebis-new-rules-for-index-derivatives-heres-whats-changing | H |
| Lot sizes | From the Jan 2026 series: Nifty 75 → 65, Bank Nifty 35 → 30, FinNifty 65 → 60, Midcap Select 140 → 120. Next 50 unchanged. Based on September 2025 average prices | https://nsearchives.nseindia.com/content/circulars/FAOP70616.pdf (not fetched) ; https://zerodha.com/marketintel/bulletin/429705/ | M |
| Price bands | Market-wide circuit breakers at 10/15/20% on Nifty or Sensex halt all equity and derivatives trading. Non-F&O stocks have 2/5/10/20% bands. F&O stocks have a dynamic 10% band that is relaxed in 5% steps after a cooling period | https://www.nism.ac.in/blog/circuit-breaker-in-share-market ; https://www.oquilia.com/news/nse-individual-stock-circuit-filter-bands | M |
| Holidays 2026 | 16 weekday holidays, plus an ad-hoc 15 Jan 2026 holiday (Maharashtra municipal elections). 8 Nov 2026 is a holiday with Muhurat trading (timings by circular) | https://www.nseindia.com/resources/exchange-communication-holidays ; https://niftylens.in/market-calendar/2026/ | M |
| F&O corporate actions | Strike and multiplier are adjusted for bonus, split, rights and similar actions. A dividend at or above **2% of market value** (the close before the board-meeting announcement date) is treated as extraordinary and adjusted; the threshold was 5% before June 2022. Adjustment happens after the close on the last cum day | https://www.sebi.gov.in/legal/circulars/jun-2022/adjustment-in-derivative-contracts-for-dividend-announcements_60306.html ; https://www.nseindia.com/static/products-services/equity-derivatives-corporate-actions-adjustments | H |
| India VIX method | CBOE-style variance swap on Nifty options with cubic-spline adjustments. Forward = latest traded price of the Nifty future for that expiry. Rate = NSE MIBOR of the relevant tenor | https://nsearchives.nseindia.com/web/sites/default/files/inline-files/India_VIX_comp_meth.pdf (via search) | M |
| NSE option-chain IV | Reportedly Black-Scholes on **spot**; some brokers use Black-76 on futures | https://www.quora.com/How-does-the-NSE-calculate-option-chain-IV-What-is-an-example | L [U] |

### 1.3 Canonical indicator spec list [P]

Conventions for every indicator:
- Session anchor, bar alignment and auction handling are **parameters of the exchange calendar**: XNSE/XBOM at 09:15 IST, XNYS at 09:30 ET, and so on. The India values are given below.
- Bars are built from exchange trades. Timestamps are in IST for display and UTC in storage.
- Bars are left-closed and right-open, anchored at 09:15:00 IST. A 5-minute bar covers 09:15 ≤ t < 09:20.
- The last regular bar of the day ends at 15:30. For Category I stocks after 3 Aug 2026, the CAS uncross print is recorded as a separate `auction_close` event and is **not merged into the 15:25 bar**.
- The pre-open equilibrium print is recorded as `auction_open`. It becomes the day's open, and it is included in the first bar's volume only if the exchange reports it as a trade.
- **Every displayed value carries `bar_state ∈ {closed, forming}`.** The alert and "signal" logic uses closed bars only. Forming values are labelled "live (repaints)".
- Every series carries `adjustment_basis ∈ {raw, split_bonus_adjusted, total_return}`. Price indicators default to `split_bonus_adjusted`, using factors from the versioned corporate-action table. Dividends are not adjusted for price indicators.
- The close for daily indicators is the **official exchange close as of that date**: the CAS price after 3 Aug 2026 for Category I stocks, and the VWAP of the last 30 minutes otherwise. LTP is only used for a "forming" daily bar. The history file has to record this regime change.
- Output is null until warm-up is complete. The warm-up needed for a residual seed influence of 1e-4 is `W = ceil(ln(1e-4)/ln(1-α))`:

  | Smoothing | α | W for n = 14 |
  |---|---|---|
  | RMA | 1/n | 125 bars |
  | EMA | 2/(n+1) | 65 bars |

  We fetch at least W + n history bars. Any output inside the warm-up is flagged `unstable`.

| Indicator | Canonical definition (ours) | Oracle for cross-check | Divergence notes |
|---|---|---|---|
| SMA(n) | Arithmetic mean of the last n closes | TA-Lib `SMA` | none |
| EMA(n) | α = 2/(n+1). **Seed = SMA of the first n values** (TA-Lib convention) | TA-Lib `EMA` exact. TradingView differs before warm-up, since it seeds from the first value | Store `seed_mode`. We offer a `tv_compat` mode (first-value seed) so displayed values match TradingView charts |
| RSI(n) | Changes Δ = C_t − C_{t−1}. G = max(Δ,0), L = max(−Δ,0). Wilder RMA (α = 1/n) seeded with the SMA of the first n G/L values. RSI = 100 − 100/(1+AG/AL). Edge cases: AL = 0 and AG > 0 gives 100. AG = 0 and AL > 0 gives 0. **AG = AL = 0 gives `undefined` (null)**, which covers flat, suspended or illiquid windows | TA-Lib `RSI` (unstable period set correctly; see bug) and TradingView `ta.rsi` after W | Kite (EMA-type smoothing) is not an oracle. **Both oracles disagree with us on the flat case** (recall, to verify against source): TA-Lib returns 0 when gain + loss = 0, and TradingView returns 100 when down = 0. Exclude that case from oracle diffs |
| MACD(12,26,9) | EMA12 − EMA26. Signal = EMA9 of MACD, seeded when MACD first exists. Histogram = MACD − signal | TA-Lib `MACD` (TA-Lib aligns the fast EMA's seed to the slow lookback, so early bars differ from a plain EMA12 − EMA26) | Early-bar differences from both TA-Lib and TradingView decay; compare only after W(26) + W(9) bars |
| ATR(n) | TR = max(H−L, \|H−C_{t−1}\|, \|L−C_{t−1}\|). TR on the first bar = H−L. RMA seeded with the SMA of TR[0..n−1], so the first ATR is at bar n−1 | TA-Lib `ATR`; TradingView `ta.atr` | TA-Lib's TRANGE is believed to have lookback 1, i.e. an ATR seeded on TR[1..n] with the first value at bar n (recall; verify against the TA-Lib source). Our fixture distinguishes the two: seeded on TR[1..3], ATR at bar 3 = 1.2667 vs our 1.3778. Some community scripts use an SMA ATR ("changeATR=false") |
| Supertrend(n, m) | hl2 = (H+L)/2. Basic bands = hl2 ± m·ATR(n). Final UB_t = basicUB if (basicUB < UB_{t−1} or C_{t−1} > UB_{t−1}), else UB_{t−1}. LB is symmetric. Direction starts down. If ST_{t−1} = UB_{t−1}: up if C_t > UB_t. Otherwise: down if C_t < LB_t. ST = LB when up, UB when down. **Output encoding: `dir = +1` means up, `−1` means down** | TradingView built-in `ta.supertrend` (the spec above follows its help page) | TradingView's `ta.supertrend` is believed to return direction −1 for up and +1 for down, the opposite of ours (recall; verify against the Pine reference). Map the signs before comparing. Community scripts differ in ATR type, initial direction and the > vs ≥ comparison. Pin the version |
| VWAP (session) | Σ(tp·v)/Σv from session start (09:15 IST, or the pre-open uncross if included). tp = hlc3 per bar, **or tick-level price·qty when ticks are available (preferred)**. Reset daily. Anchored variants reset at a user-selected timestamp | TradingView VWAP (anchor = Session, source = hlc3) on 1-minute bars; exchange-published VWAP/ATP | Bar-based hlc3 VWAP ≠ exchange ATP. Label which one is shown. Never compute VWAP on an index (no volume); for index F&O, use the futures contract |
| Floor pivots | P = (H+L+C)/3 of the **prior completed session** (daily, weekly or monthly). R1 = 2P−L, S1 = 2P−H, R2 = P+(H−L), S2 = P−(H−L), R3 = H+2(P−L), S3 = L−2(H−P). H, L and C are the **official exchange (bhavcopy) values**, not aggregated from our intraday bars; under CAS the close can otherwise fall outside the bar-derived [L, H] | Hand calculation; TradingView "Pivot Points Standard" (Traditional) | Camarilla, Woodie and Fibonacci are separate named variants. "Support/resistance" from swing highs and lows is **not** canonical and must be labelled heuristic |
| Black-76 Greeks | Price on forward F. F = the same-expiry futures price, or synthetic F = K + e^{rT}(C−P) at the ATM strike. European exercise. r = NSE MIBOR matching the tenor, as in the India VIX methodology. T = (expiry at 15:30 IST − now)/(365·24·3600), calendar time [P, choice to confirm]. **Delta is reported with respect to F (futures delta)**; delta with respect to spot requires a carry adjustment. IV by Brent root-find, bounded to [0.01, 5]. No IV if the price is below intrinsic or the quote is stale or zero-bid | QuantLib `BlackCalculator`; py_vollib `black` | Do **not** claim to match the NSE option-chain IV (spot-based BS, L). Using BSM on spot with r but no dividend yield misprices index options by the carry. Black-76 on F absorbs it |
| PCR | PCR_OI = ΣPut OI / ΣCall OI for **one underlying and one expiry**, across all listed strikes, at the snapshot timestamp. PCR_Vol is separate. The scope is always printed | Exchange option chain | Scope ambiguity (all expiries vs nearest) is the main source of mismatch |
| Max pain | argmin over strikes K* of Σ_K [CallOI_K·max(K*−K,0) + PutOI_K·max(K−K*,0)] over listed strikes, one expiry | Hand calculation | **We found no predictive evidence.** Display as descriptive only |
| OI change | ΔOI = OI_t − OI at the previous official end-of-day snapshot for the same contract. Intraday OI updates are exchange-snapshot based (the frequency depends on the vendor [U]) | Exchange bhavcopy (EOD) | Label the "as of" timestamp |

### 1.4 Test approach [P]

1. **The spec is the definition.** Each indicator has a versioned spec ID (e.g. `RSI.wilder.smaseed.v1`) stored with every output.
2. **Golden fixtures, hand-computed** (below). These are checked with a pure-Python reference script at `scratchpad/fixtures_check.py`; port it to `research/` with a manifest when approved.
3. **Oracle deltas after warm-up.**
   - Compare against TA-Lib on 5 years of daily data and 60 days of 1-minute data for 50 NSE symbols, drawn from local snapshots only.
   - Tolerance vs TA-Lib: |Δ| ≤ 1e-9 relative, **applied only after W bars**, because the seed and alignment conventions differ (ATR TR[0], MACD fast-EMA alignment).
   - Tolerance vs TradingView CSV exports: |Δ| ≤ 1e-4 × value, also only after W bars, in `tv_compat` mode.
   - Excluded from all oracle diffs: RSI's flat-window (undefined) bars.
4. **Streaming equals batch.** An incremental engine (talipp-style or our own) fed bar by bar must equal batch recomputation bit-for-bit, or within 1e-12.
5. **Property tests:**
   - RSI ∈ [0,100] when defined;
   - a constant series gives RSI = `undefined`;
   - a strictly rising series gives RSI = 100;
   - session VWAP ∈ [session low, session high];
   - Supertrend changes direction only when the close crosses the active band;
   - pivots are ordered S3 < S2 < S1 < P < R1 < R2 < R3, given the precondition L ≤ C ≤ H and H > L (official values);
   - Black-76 put-call parity: C − P = e^{−rT}(F − K);
   - the Greeks agree with finite differences;
   - adjustment is idempotent.
6. **Regime fixtures:**
   - a split or bonus day;
   - an extraordinary-dividend F&O adjustment;
   - a Muhurat session (8 Nov 2026 is a **Sunday**, so the calendar must allow weekend sessions);
   - an ad-hoc holiday (15 Jan 2026);
   - an expiry that moves because of a holiday;
   - the lot-size change boundary (Dec 2025 / Jan 2026);
   - the expiry-weekday change boundary: last Thursday expiry on 28 Aug 2025, first Tuesday expiry on 2 Sep 2025;
   - the first CAS day (3 Aug 2026);
   - the first day of the new pre-open (7 Sep 2026);
   - a market-wide circuit-breaker halt (synthetic fixture);
   - a stock frozen at its upper band.

#### Golden fixtures (hand-verified; values reproduced by `fixtures_check.py`)

0. **RSI edge cases, n = 3.**
   - A flat series `[5]*6` is undefined at every index.
   - A strictly rising series `[1, 2, 3, 4, 5]` gives 100 at indices 3 and 4.
1. **RSI Wilder, n = 3.**
   - Closes `[10, 11, 10.5, 11.5, 12, 11]`, so Δ = [+1, −0.5, +1, +0.5, −1].
   - At index 3: AG = 2/3, AL = 1/6, RS = 4, **RSI = 80.0000**.
   - At index 4: AG = (2/3·2 + 0.5)/3 = 0.6111, AL = 0.1111, RS = 5.5, **RSI = 84.6154**.
   - At index 5: AG = AL = 0.4074, **RSI = 50.0000**.
   - The EMA-smoothed RSI variant gives 80.0, **87.5, 35.0**. This demonstrates the platform gap.
2. **EMA seeding, n = 3 (α = 0.5).**
   - Series `[10, 14, 11, 13, 12]`.
   - SMA seed: [–, –, 11.6667, 12.3333, 12.1667].
   - First-value seed (TradingView-style): [10, 12, 11.5, 12.25, 12.125].
3. **Session VWAP, hlc3.**
   - Bars (H, L, C, V) = (101, 99, 100, 1000), (102, 100, 101, 3000), (101, 98, 99, 2000).
   - Typical prices are 100, 101, 99.3333. **VWAP = 100.0000, 100.7500, 100.2778.**
4. **ATR(3) and Supertrend(3, 1.0).** HLC input:

   | Bar | H | L | C |
   |---|---|---|---|
   | 0 | 10.5 | 9.0 | 9.5 |
   | 1 | 10.5 | 9.5 | 10.0 |
   | 2 | 11.0 | 10.0 | 10.8 |
   | 3 | 12.6 | 11.0 | 12.4 |
   | 4 | 11.2 | 10.2 | 10.4 |
   | 5 | 10.6 | 9.4 | 9.6 |
   | 6 | 10.0 | 8.8 | 9.0 |
   | 7 | 9.8 | 9.0 | 9.7 |

   Outputs:

   | Series | Bar 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
   |---|---|---|---|---|---|---|---|---|
   | TR | 1.5 | 1.0 | 1.0 | 1.8 | 2.2 | 1.2 | 1.2 | 0.8 |
   | ATR | – | – | 1.1667 | 1.3778 | 1.6519 | 1.5012 | 1.4008 | 1.2005 |
   | UB | – | – | 11.6667 | 11.6667 | 12.3519 | 11.5012 | 10.8008 | 10.6005 |
   | LB | – | – | 9.3333 | 10.4222 | 10.4222 | 8.4988 | 8.4988 | 8.4988 |
   | ST | – | – | 11.6667 (down, −1) | 10.4222 (**flip up, +1**: 12.4 > UB 11.6667) | 12.3519 (**flip down, −1**: 10.4 < LB 10.4222) | 11.5012 | 10.8008 | 10.6005 |

   - At bar 4 the UB resets because the previous close (12.4) was above the previous UB.
   - A TA-Lib-style ATR seeded on TR[1..3] would first appear at bar 3 as 1.2667, not 1.3778, so the fixture distinguishes the two conventions.
5. **Floor pivots.**
   - Prior day H = 22150, L = 21900, C = 22050.
   - P = 22033.33, R1 = 22166.67, S1 = 21916.67, R2 = 22283.33, S2 = 21783.33, R3 = 22416.67, S3 = 21666.67.
6. **Black-76.**
   - F = K = 22000, T = 7/365, r = 6.5%, σ = 12%.
   - Call = Put = **145.67** (parity at the money, forward).
   - Futures deltas: Δ_call = 0.5027, Δ_put = −0.4961.
7. **PCR and max pain.**
   - OI: 21900 (C100/P500), 22000 (300/400), 22100 (600/200), 22200 (800/50).
   - PCR_OI = 1150/1800 = **0.6389**.
   - Pain at each strike: 21900: 95,000; 22000: 40,000; 22100: 55,000; 22200: 150,000. **Max pain = 22000**.

---

## 2. Evidence on what retail traders gain (for honest claims)

### 2.1 SEBI studies. Samples differ; never blend them.

| Study | Sample | Headline | Source | Conf. |
|---|---|---|---|---|
| Jan 2023 (FY22) | — | 89% of individual F&O traders lost money | https://www.business-standard.com/amp/article/markets/sebi-study-suggests-89-retail-traders-in-equity-f-o-suffered-losses-123012501466_1.html | M |
| Sep 2024 (FY22–FY24) | top-10 brokers [U] | 93% lost money. Aggregate losses > ₹1.8 lakh crore over 3 years | https://www.sebi.gov.in/media-and-notifications/press-releases/sep-2024/updated-sebi-study-reveals-93-of-individual-traders-incurred-losses-in-equity-fando-between-fy22-and-fy24-aggregate-losses-exceed-1-8-lakh-crores-over-three-years_86906.html | H |
| 7 Jul 2025 (FY25) | top-13 brokers, about 96 lakh traders | **91%** lost money. Net loss ₹1,05,603 cr (FY24: ₹74,812 cr). Loss-makers paid a further 28% of their trading losses as costs; profit-makers paid 15–50% of profits as costs | https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html | M (secondary) |
| 20 Aug 2026 (FY25–FY26), SEBI DEPA | top-15 brokers, about 90% of individuals | FY26: **87.7%** lost money. Net loss about ₹91,685 cr (FY25 on this sample: about ₹1.12 lakh cr). Average loss about ₹1.17 lakh. Active traders 98.1 lakh (FY25) → 78.6 lakh (FY26). Costs about ₹25,000 cr in FY26. About **92%** of losses were from options. About 59% of index-option turnover was 0DTE | Study page: https://www.sebi.gov.in/reports-and-statistics/research/aug-2026/study-profitability-of-individual-traders-in-the-equity-derivatives-segment-fy25-fy26-_103835.html ; figures from https://www.corplawupdates.in/updates/sebi-equity-derivatives-retail-trader-study-fy26 and https://taxguru.in/sebi/sebi-studies-key-trends-retail-participation-trading-behaviour-profitability-equity-derivatives.html | Existence: H. Figures: M (the PDF was not read) |

Algo profits: secondary reports say algo entities earned about 99% of prop/FPI profits, and that prop firms earned about ₹44,000 cr and FPIs about ₹14,000 cr in FY26 (openthemagazine). Confidence L; unverified.

Conflicting secondary figures, recorded rather than resolved:
- participation of 87.5 lakh (−18%) vs 78.6 lakh (−20%);
- "about 91% over FY25–26" (mostlyeconomics blog) vs 87.7% for FY26.

Treat the corplawupdates/taxguru numbers as provisional until the SEBI PDF is read.

### 2.2 Technical analysis profitability

- **Park & Irwin (2007), *J. Econ. Surveys* 21(4):786–826.**
  - Of 95 modern studies, 56 found positive results.
  - Stock-market profits largely disappear after the late 1980s.
  - Many studies have data-snooping, ex-post rule-selection and cost problems.
  - Verdict: background only.
  - https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6419.2007.00519.x (H)
- **Bajgrowicz & Scaillet (2012), *JFE* 106:473–491.**
  - Data: DJIA 1897–2011, with false-discovery-rate control.
  - An investor "would never have been able to select ex ante the future best-performing rules", and in-sample performance is "completely offset" by low transaction costs.
  - https://www.sciencedirect.com/science/article/abs/pii/S0304405X1200116X (H)
- **India.** "How rewarding is technical analysis in the Indian stock market?", *Quantitative Finance* 11(2).
  - It reports that moving-average rules capture direction but returns are eroded by costs.
  - The numbers were not verified: an unattributed snippet quoted 36.53% before costs and 31.05% after, but **we do not use these**.
  - https://www.tandfonline.com/doi/full/10.1080/14697680903493581 (L for specifics)

**[I]** Indian-TA studies generally lack point-in-time universes, deflated Sharpe and realistic STT, stamp duty and slippage for intraday F&O. None meets 06 §7.

### 2.3 Sentiment → returns (India)

- **Composite sentiment index, NSE 2015–2024** (PCA of turnover, advance/decline, MF flows, India VIX, FII/DII flows and IPO count). No significant relationship with sectoral returns at 5%. Source: SSRN working paper. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7189538 (L: an unrefereed student paper [U])
- **Older NSE studies (2001–2013).** Sentiment affects contemporaneous excess returns and volatility asymmetrically. Contemporaneous links are not tradable prediction. https://www.researchgate.net/publication/286923378 (L–M)
- **Emerging-markets nonlinear predictive regression.** The effect is contemporaneous and short-lived, then decays. https://pmc.ncbi.nlm.nih.gov/articles/PMC10194879/ (M)
- **Verdict [I]:** show sentiment as a *descriptive* aggregate with its source, window and method. Make no claim that it predicts returns. Consistent with 06 §7, LLM "sentiment alpha" is rejected as evidence.

### 2.4 LLM trading-agent benchmarks

| Benchmark | Data / eval | Result | Limitations | Verdict |
|---|---|---|---|---|
| StockBench (arXiv 2510.02209) | Top 20 DJIA stocks, 3 Mar–30 Jun 2025 (82 trading days), daily decisions, 14 LLMs, $100k | Abstract: "most models struggle to outperform the simple buy-and-hold baseline". Buy-and-hold +0.4% (max drawdown −15.2%); best (Kimi-K2) +1.9% (max drawdown −11.8%) | **No costs, slippage or liquidity modelled**; one 4-month window; US large caps only | Evidence of *no demonstrated edge*; never cite as edge. H for the facts |
| LiveTradeBench (arXiv 2511.03628) | 50-day live run, 21 LLMs, US stocks plus Polymarket | High LMArena score does not imply better trading | Short window; no significance testing reported [U] | Same |
| "When Agents Trade" (arXiv 2510.11695) | A **separate** live multi-market benchmark (not LiveTradeBench) | Not read in detail [U] | — | — |
| FinBen (NeurIPS 2024 D&B, arXiv 2402.12659) | 42 datasets, 24 tasks, including a stock-trading task | GPT-4 best on trading among those tested | Short trading windows [U] | Useful for QA eval subsets, not for trading claims |

**[I]** No benchmark shows a robust, cost-adjusted edge for LLM agents. Our product should use LLMs only to explain deterministic outputs.

---

## 3. SEBI retail algo framework: what the assistant can offer

Primary source read in full: the SEBI circular of 4 Feb 2025, SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013. The Sep 2025 extension page shows `.../2025/132`, which is probably the extension circular's own number [U]. PDF via https://www.cse-india.com/upload/upload/Feb_042025.pdf; page https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html (H).

- **§5.I(a)** The broker is the principal; the algo provider is its agent.
- **§5.I(b)** All API algo orders are tagged with an exchange-provided unique identifier.
- **§5.I(c)** A self-built retail algo must be registered only above an orders-per-second threshold, which the ISF sets. It may be used for family only.
- **§5.I(d)** No open APIs. Access uses a vendor-client-specific API key plus a static IP whitelist, OAuth and 2FA. Providers must be empanelled.
- **§5.II(a)** Exchange permission is needed for **each algo**; any modification needs re-approval.
- **§5.III** Algo providers are not SEBI-regulated but must be empanelled with exchanges. Charges must be fully disclosed.
- **§5.V** Algos fall into two types:
  - **White box / execution algos**: logic "disclosed and replicable".
  - **Black box algos**: "logic is not known to the user and is not replicable". The provider **must register as a Research Analyst**, maintain a research report per algo, and re-register on any logic change.
- **§7** Standards were due by 1 Apr 2025, with applicability from 1 Aug 2025.
- **Later timeline.** The dates were extended (SEBI, 30 Sep 2025): brokers that are ready could go live from 1 Oct 2025; the framework applies to **all brokers from 1 Apr 2026**. https://www.sebi.gov.in/legal/circulars/sep-2025/extension-of-timeline-for-implementation-of-sebi-circular-dated-february-04-2025-on-safer-participation-of-retail-investors-in-algorithmic-trading-_96979.html (existence H; dates M, from ICICI Direct/secondary sources)
- **NSE implementation standards** (5 May 2025; operational modalities of 23 Jul 2025): the threshold is **10 orders per second**. Below it, no registration is needed but orders are still tagged; above it, registration is required. https://nsearchives.nseindia.com/content/circulars/INVG67858.pdf (fetch timed out) ; https://zerodha.com/z-connect/general/a-comprehensive-overview-of-nses-circular-on-the-new-retail-algo-trading-framework (M)

Adjacent rules:
- **Finfluencer/education circular, 29 Jan 2025.** Regulated entities may not associate with unregistered persons giving advice or recommendations or making performance claims. The education carve-out requires that **no market price data of the preceding 3 months** be used. https://www.business-standard.com/markets/news/sebi-finfluencer-circular-live-stock-data-market-education-rules-125013000571_1.html (M; read the primary text)
- **PaRRVA.** The framework was issued on 4 Apr 2025. CARE Ratings is the agency and NSE the data centre. Pilot from 8 Dec 2025; fully operational from 4 May 2026. Past-performance claims by IAs, RAs and algo providers must be verified. https://taxguru.in/sebi/sebi-operationalises-parrva-due-verified-performance-disclosure-securities-market.html (M)
- **RA (Third Amendment) Regulations, 16 Dec 2024.** Reg 19(vii) requires disclosure of the extent of AI-tool use. Reg 20(4) requires recommendations to be corroborated by data and analysis. https://www.scconline.com/blog/post/2024/12/19/sebi-research-analyst-third-amendment-regulations-2024/ (M)
- **SEBI AI/ML consultation (20 Jun 2025):** model governance, testing, disclosure and auditability. Final status [U]. https://bhatiabhola.com/index.php/blog/2025/06/28/sebi-consultation-paper-dated-20-06-2025-guidelines-for-responsible-usage-of-artificial-intelligence-ai-and-machine-learning-ml-in-indian-securities-markets/ (M)

**Offering tiers.** These are research inferences **for counsel; not a legal opinion.**

| Tier | What it is | Regulatory exposure (inference) |
|---|---|---|
| A | Descriptive analytics on user-chosen instruments: indicator values, option-chain analytics, deals and news, with no buy/sell language | Lowest; still subject to data licences. Probably not "education" under the 29 Jan 2025 circular because it uses live prices; also probably not advice if it carries no recommendation [U] |
| B | User-authored rule backtests (white box: the user writes and sees the rules), on historical data, with costs, and no performance marketing | Moderate. Any published performance claim triggers PaRRVA |
| C | Pre-built strategies or "algos" suggested by us that generate buy/sell signals | Likely **Research Analyst** territory. If the logic is hidden, it is a **black-box algo**, which needs RA registration plus exchange registration via a broker |
| D | Order routing / automated execution | Broker principal–agent chain, provider empanelment, exchange algo ID, static IP and OAuth. Not an MVP item |

---

## 4. Reliability checklist [P unless cited]

**Numbers**
- [ ] Every numeral in an LLM reply is produced by the deterministic engine and carries `(value, unit, as_of_ts, source, spec_id, bar_state)`.
- [ ] The post-generation validator extracts every number with a regex plus a units parser and matches it to a tool value within tolerance (exact for integers, 1e-6 relative for floats, displayed rounding respected). Any failure means refusal or a template fallback. This matches 06 §5, "Hard gates".
- [ ] Templates handle numeric slots. The LLM writes only the connective prose, and within the 300 ms budget it is optional, streamed after the numbers.
- [ ] No forecasts, confidence scores or directional language, enforced by a deny-list plus a classifier (06 §5).

**Freshness and abstention**
- [ ] A per-field staleness SLA, e.g. LTP ≤ 2 s in real-time mode, option-chain OI ≤ the vendor's snapshot interval, EOD fields = last official session. Past the SLA the field is greyed out or omitted.
- [ ] Abstain when:
  - the market is closed and the data is from the last session (label it);
  - the instrument is halted (market-wide circuit breaker) or frozen at a band;
  - the indicator is in warm-up (`unstable`);
  - there is a corporate-action day and the adjustment table has not been updated;
  - two sources disagree beyond tolerance.
- [ ] Label every reply real-time, delayed-N or EOD (06 §2.4).

**Instrument identity (India)**
- [ ] Key on the internal `instrument_id`, mapped to (ISIN, exchange, exchange_token/security_id). The trading symbol is a time-varying attribute.
- [ ] Symbol changes, demerger ISIN changes, and F&O contract rollovers are stored as validity intervals.
- [ ] Derivative contracts are keyed on (underlying, expiry_date, strike, option_type, lot_size_as_of).

**Bad-tick and data-quality checks** (spec; no external source)
- [ ] The price is within the applicable band: the static band for non-F&O stocks, the dynamic band for F&O stocks, and ±3% of the reference price during CAS. Anything outside is rejected and logged.
- [ ] Freeze detection: the price is pinned at an upper or lower band, with one-sided depth and few trades. Mark the stock "at circuit". Treat indicators and VWAP as unreliable and flag them.
- [ ] Volume is monotone within the session for cumulative-volume feeds, and OI is never negative.
- [ ] Put-call parity check per strike against the future: |C − P − e^{−rT}(F−K)| above a threshold flags a stale quote.
- [ ] Futures basis sanity: |F/S − 1| lies within the carry bound plus a tolerance.
- [ ] Daily cross-source reconciliation against the exchange bhavcopy (the official close, OI and settlement price), following the 06 §4 model.
- [ ] The calendar comes from exchange circulars (holidays, Muhurat, ad-hoc closures, expiry shifts), never from weekday arithmetic. For India, check `exchange_calendars` XBOM/XNSE coverage [U].

**Citations (news, deals)**
- [ ] Every cited ID exists in the retrieved set. The timestamp is the first-publication time. Bulk and block deals come from the exchange files, with their as-of date.
- [ ] Parametric-leak test (06 §5).

**Latency (about 300 ms)**
- [ ] Precompute indicator snapshots on bar close. The forming-bar update is O(1) via an incremental engine.
- [ ] The LLM is not on the critical path for numbers. Measure p50/p95/p99 end-to-end.

---

## 5. Evaluation plan [P]

1. **Indicator conformance suite (CI gate).** Golden fixtures (§1.4), oracle deltas after warm-up, streaming = batch, property tests and regime fixtures. Gate: 100% pass.
2. **Data-quality replay.**
   - Six months of stored NSE/BSE ticks or bars from local snapshots, including the known event days (expiry-weekday switch, lot-size switch, first CAS day, new pre-open).
   - Metrics: false-reject rate of band checks, missed-bad-tick rate on injected corruptions, and reconciliation mismatch rate vs bhavcopy.
   - **Calibrate the anomaly thresholds to an empirical target false-alert rate** (e.g. ≤ 1 false data-quality flag per 100 symbol-days) using empirical quantiles, not Gaussian tables.
3. **Numeric grounding eval.**
   - Build an in-house **point-in-time India QA set** of about 600 items, generated from frozen snapshots. The question types are "What is RSI(14) daily for X as of T?", PCR, max pain, Greeks, VWAP, deal lookups and "why did X move?".
   - Gold answers come from the engine; include deliberately unanswerable items (stale, halted, warm-up).
   - Metrics:
     - numeric exact-match within tolerance;
     - **abstention coverage–accuracy curve** (selective accuracy at 90/95/99% coverage);
     - false-abstention rate;
     - unit/sign errors;
     - citation validity (100%);
     - p95 latency.
   - Run it per candidate fast model; **we have no published hallucination rate for small models on this task, so we measure it.**
4. **Public benchmarks (secondary, US-filings-based).** None of these are India- or indicator-specific, so none replaces item 3.
   - **FinQA, TAT-QA:** numeric reasoning.
   - **FinanceBench (Patronus, 2023).** GPT-4-Turbo with retrieval answered 81% of questions incorrectly or refused. https://www.patronus.ai/announcements/patronus-ai-launches-financebench-the-industrys-first-benchmark-for-llm-performance-on-financial-questions (H)
   - **FinSearchComp:** 639 expert questions on time-sensitive fetch, historical lookup and investigation. https://arxiv.org/abs/2509.13160 (M)
   - Recent work finds financial-reasoning errors harder to detect (probe AUROC about 0.73–0.79) than factual errors. https://arxiv.org/html/2607.11414 (M)
5. **Any "algo" or "setup" feature.** Apply 06 §7 verbatim:
   - point-in-time data including delisted names;
   - walk-forward with a purge gap, plus a holdout;
   - DSR > 0.95 and PBO < 0.2 (Bailey & López de Prado 2014, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551);
   - t > 3;
   - costs at 5/10/20/50 bp, **and** India-specific costs: STT on the option premium or on intrinsic value at exercise, exchange charges, stamp duty, GST and slippage [rates U];
   - baselines: buy-and-hold Nifty/Sensex, sector indices and simple momentum.
   - **Add 06 §7 India baselines [P]:** "do nothing" and "buy-and-hold Nifty 50 TRI". For option strategies, add a naive short-straddle/long-straddle baseline with margin cost.
6. **Human audit.** 50 replies per week; two raters with ≥ 20% overlap; κ ≥ 0.6 (06 §5).

---

## 6. Honest-claims guidance [P, grounded in §2–3]

**Can say (if tested):**
- "RSI(14) computed with Wilder smoothing on closed daily bars, split/bonus-adjusted, as of 15:30 IST 23-Sep-2026. Matches TradingView within 0.01 after 125 bars."
- "Greeks from Black-76 on the Nifty October future; IV is ours and may differ from the NSE option chain."
- "Sentiment score = share of positive minus negative headlines over the last 24 h from sources X, Y; descriptive only."
- "Backtest of *your* rule on 2019–2026 data, net of the costs listed; past results do not predict future returns."

**Must not say:**
- "Accurate signals", "high-probability setups", "X% win rate", "AI predicts".
- Any profitability claim without PaRRVA verification.
- "Education" for anything using prices from the last 3 months.
- "Real-time" when the data is delayed.
- Max pain or PCR as predictive.

**Mandatory context:**
- Show SEBI's risk disclosure: 9 in 10 lose money, citing the dated study. SEBI requires brokers to show this at login; for us it is good practice [I].
- Label the source, timestamp and entitlement class on every number.

---

## 7. Unverified items and open methodological risks

1. SEBI Aug 2026 study figures were taken from secondary reproductions; the SEBI PDF has not been read. Conflicts remain: participation 87.5 vs 78.6 lakh; "91% over FY25–26" vs 87.7% FY26.
2. The SEBI 26 May 2025 expiry-day circular and the NSE algo implementation-standard PDFs (10 OPS threshold; 1 Apr 2026 all-broker date) are not yet read at primary level (fetch timed out).
3. Pine `ta.rma` SMA seed (recall) and `ta.ema` first-value seed (third-party reproduction). Confirm against the Pine v6 reference.
4. Whether the TA-Lib 0.6.x unstable-period ID mis-targeting is fixed in 0.6.8. Check the release notes; oracle tests would catch it either way.
5. The current pandas-ta status after the 1 July 2026 archival deadline, and the canonical repo URL.
6. Seeding conventions and maintenance of talipp, polars_ta and tulipy.
7. Whether continuous trading halts at 15:15 for Category I stocks under CAS (read NSE CMTR73362). This affects the last-bar definition.
8. NSE option-chain IV methodology (spot BS vs Black-76). L.
9. Official pre-open circular text for 7 Sep 2026 (only a secondary source so far).
10. The outcome of the SEBI expiry-settlement consultation (comments due 3 Oct 2026). This can change the settlement price used for expiry P&L and max-pain "realisation".
11. Kite's exact RSI/EMA smoothing (forum-level evidence only).
12. Hallucination rates of fast small LLMs on numeric finance QA: **no source found**; must be measured.
13. Intraday OI update frequency by vendor, and whether exchange VWAP/ATP is licensed for display.
14. The legal status of Tier A/B/C offerings: counsel required.
15. The India TA study figures (L), and the SSRN sentiment paper (unrefereed).
16. `exchange_calendars` coverage and accuracy for XNSE/XBOM, including ad-hoc holidays.
17. Current India transaction-cost rates (STT, stamp duty, exchange charges) for the cost model.
18. Algo-entity share of prop/FPI profits in FY26 (secondary, L).
19. To verify against source:
    - TA-Lib RSI returns 0 when gain + loss = 0, and TradingView returns 100 when down = 0.
    - TA-Lib TRANGE/ATR lookback is 1, with the ATR seeded on TR[1..n].
    - TradingView `ta.supertrend` returns direction −1 for up and +1 for down.

    All three are recall. The fixtures are designed to expose them.

**Methodological risks for data-engineer / realtime-engineer:**
- Close-definition regime change (CAS) across history.
- Auction prints in bars and VWAP.
- Forming-bar repaint.
- Warm-up length vs history fetch cost.
- Point-in-time lot size and expiry calendars.
- Band-pinned stocks distorting VWAP and ATR.

These go to `financial-correctness-reviewer`.
