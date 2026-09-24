"""Pure-Python reference computations for tiny golden fixtures (no libraries)."""
from math import log, sqrt, erf, exp

def N(x):
    return 0.5 * (1 + erf(x / sqrt(2)))

closes = [10.0, 11.0, 10.5, 11.5, 12.0, 11.0]

def _rsi(ag, al):
    # Spec: AL=0 & AG>0 -> 100; AG=0 & AL>0 -> 0; AG=AL=0 -> undefined (None)
    if al == 0 and ag == 0: return None
    if al == 0: return 100.0
    return 100 - 100 / (1 + ag / al)

# RSI, Wilder (RMA seeded with SMA of first n changes), n=3
def rsi_wilder(c, n):
    ch = [c[i] - c[i-1] for i in range(1, len(c))]
    g = [max(x, 0) for x in ch]; l = [max(-x, 0) for x in ch]
    out = [None] * len(c)
    ag = sum(g[:n]) / n; al = sum(l[:n]) / n
    out[n] = _rsi(ag, al)
    for i in range(n, len(ch)):
        ag = (ag * (n - 1) + g[i]) / n; al = (al * (n - 1) + l[i]) / n
        out[i+1] = _rsi(ag, al)
    return out

# RSI with EMA (alpha=2/(n+1)) smoothing, SMA seed -- the "EMA-RSI" variant
def rsi_ema(c, n):
    ch = [c[i] - c[i-1] for i in range(1, len(c))]
    g = [max(x, 0) for x in ch]; l = [max(-x, 0) for x in ch]
    a = 2 / (n + 1); out = [None] * len(c)
    ag = sum(g[:n]) / n; al = sum(l[:n]) / n
    out[n] = _rsi(ag, al)
    for i in range(n, len(ch)):
        ag = a * g[i] + (1 - a) * ag; al = a * l[i] + (1 - a) * al
        out[i+1] = _rsi(ag, al)
    return out

def ema_sma_seed(c, n):
    a = 2 / (n + 1); out = [None] * len(c)
    e = sum(c[:n]) / n; out[n-1] = e
    for i in range(n, len(c)):
        e = a * c[i] + (1 - a) * e; out[i] = e
    return out

def ema_first_seed(c, n):
    a = 2 / (n + 1); out = []; e = None
    for x in c:
        e = x if e is None else a * x + (1 - a) * e; out.append(e)
    return out

c2 = [10.0, 14.0, 11.0, 13.0, 12.0]  # EMA seeding fixture, n=3

# Session VWAP, hlc3, bars: (H, L, C, V)
bars = [(101, 99, 100, 1000), (102, 100, 101, 3000), (101, 98, 99, 2000)]
def vwap(b):
    pv = 0; v = 0; out = []
    for h, l, c, vol in b:
        tp = (h + l + c) / 3; pv += tp * vol; v += vol; out.append(pv / v)
    return out

# ATR (Wilder, SMA seed) + Supertrend (TradingView band carry-forward rules)
ohlc = [  # (H, L, C)
    (10.5, 9.0, 9.5), (10.5, 9.5, 10.0), (11.0, 10.0, 10.8), (12.6, 11.0, 12.4),
    (11.2, 10.2, 10.4), (10.6, 9.4, 9.6), (10.0, 8.8, 9.0), (9.8, 9.0, 9.7),
]
def supertrend(o, n, m):
    tr = [o[0][0] - o[0][1]]
    for i in range(1, len(o)):
        h, l, _ = o[i]; pc = o[i-1][2]
        tr.append(max(h - l, abs(h - pc), abs(l - pc)))
    atr = [None] * len(o)
    atr[n-1] = sum(tr[:n]) / n
    for i in range(n, len(o)):
        atr[i] = (atr[i-1] * (n - 1) + tr[i]) / n
    ub = [None]*len(o); lb = [None]*len(o); st = [None]*len(o); d = [None]*len(o)
    for i in range(n-1, len(o)):
        h, l, c = o[i]; hl2 = (h + l) / 2
        bu = hl2 + m * atr[i]; bl = hl2 - m * atr[i]
        if ub[i-1] is None or i == n-1:
            ub[i], lb[i] = bu, bl; d[i] = -1  # start as downtrend (TV: initially isDownTrend)
            st[i] = ub[i]; continue
        pc = o[i-1][2]
        ub[i] = bu if (bu < ub[i-1] or pc > ub[i-1]) else ub[i-1]
        lb[i] = bl if (bl > lb[i-1] or pc < lb[i-1]) else lb[i-1]
        if st[i-1] == ub[i-1]:
            d[i] = 1 if c > ub[i] else -1
        else:
            d[i] = -1 if c < lb[i] else 1
        st[i] = lb[i] if d[i] == 1 else ub[i]
    return tr, atr, ub, lb, st, d

# Floor pivots from prior day H, L, C
H, L, C = 22150.0, 21900.0, 22050.0
P = (H + L + C) / 3
piv = dict(P=P, R1=2*P-L, S1=2*P-H, R2=P+(H-L), S2=P-(H-L), R3=H+2*(P-L), S3=L-2*(H-P))

# Black-76 call/put on forward
def black76(F, K, T, r, s, cp):
    d1 = (log(F/K) + 0.5*s*s*T) / (s*sqrt(T)); d2 = d1 - s*sqrt(T); df = exp(-r*T)
    if cp == 'c':
        return df*(F*N(d1) - K*N(d2)), df*N(d1)
    return df*(K*N(-d2) - F*N(-d1)), -df*N(-d1)

# PCR (OI) and max pain
chain = {  # strike: (call_OI, put_OI)
    21900: (100, 500), 22000: (300, 400), 22100: (600, 200), 22200: (800, 50),
}
pcr_oi = sum(p for _, p in chain.values()) / sum(c for c, _ in chain.values())
def pain(S):
    return sum(max(S-K,0)*co + max(K-S,0)*po for K,(co,po) in chain.items())
mp = {K: pain(K) for K in chain}

if __name__ == '__main__':
    print('RSI wilder n=3:', [round(x, 4) if x is not None else None for x in rsi_wilder(closes, 3)])
    print('RSI flat n=3:', rsi_wilder([5.0]*6, 3), ' rising-only:', rsi_wilder([1.,2.,3.,4.,5.], 3))
    print('RSI ema    n=3:', [round(x, 4) if x is not None else None for x in rsi_ema(closes, 3)])
    print('EMA sma-seed n=3 on', c2, [round(x, 4) if x is not None else None for x in ema_sma_seed(c2, 3)])
    print('EMA first-seed n=3 on', c2, [round(x, 4) for x in ema_first_seed(c2, 3)])
    print('VWAP hlc3:', [round(x, 4) for x in vwap(bars)])
    tr, atr, ub, lb, st, d = supertrend(ohlc, 3, 1.0)
    r = lambda xs: [round(x, 4) if x is not None else None for x in xs]
    print('TR', r(tr)); print('ATR', r(atr)); print('UB', r(ub)); print('LB', r(lb)); print('ST', r(st)); print('dir', d)
    print('Pivots', {k: round(v, 2) for k, v in piv.items()})
    for cp in 'cp':
        pr, de = black76(22000, 22000, 7/365, 0.065, 0.12, cp)
        print('B76', cp, round(pr, 4), 'delta', round(de, 4))
    print('PCR_OI', round(pcr_oi, 4), 'pain', mp, 'max_pain', min(mp, key=mp.get))
    # warm-up residual seed weight to 1e-4
    import math
    for n in (14,):
        k_rma = math.log(1e-4)/math.log(1-1/n); k_ema = math.log(1e-4)/math.log((n-1)/(n+1))
        print('warmup bars to 1e-4, n=14: RMA', round(k_rma,1), 'EMA', round(k_ema,1))
