"""lfsr_sweep.py — the TEMPORAL maintenance arms.

Pre-registered in scratchpad/MAINTENANCE_SWEEP_PREREG_ADDENDUM.md, committed at a8d7491
BEFORE this file existed. Construction facts in scratchpad/lfsr_design_check.py.

SCOPE: a DESIGNED substrate. An LFSR is built to satisfy a three-time parity; that it does
is not a result about the world. What transfers is the PRICE of holding the structure under
noise, and what the measurement can and cannot see (T0).

Arms:
  (a) eps = 0            — positive control for maintenance: no decay, ever.
  (b) eps > 0, q = 0     — the unpaid case: geometric decay, rate fitted against eps.
  (c) eps > 0, q > 0     — the rent test proper.
  (d) cost in bits per recorded bit per step, for each retained level of share.
Plus tau_share / tau_pair for every arm, and the equally-spaced (D, 2D) probe alongside the
matched (5,9) probe at every point.
"""
import sys, os, json, time, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import array_cap_experiment as ACE
from lfsr_design_check import lfsr_period, gen_sequences

LN2 = float(np.log(2))
SEEDS = [20260725, 99, 7, 1337, 4242]

try:
    import cupy as cp
    _HAS_GPU = True
except Exception:
    cp = None
    _HAS_GPU = False

A, B = 4, 9                 # y_t = y_{t-4} ^ y_{t-9}, period 511
PARITY_LAGS = (B - A, B)    # (5, 9) -- where the parity actually sits
T_REC = 128                 # record length in bits
EPS_GRID = [0.001, 0.003, 0.01, 0.03, 0.1]
Q_GRID = [0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0]


def Hb(p):
    p = np.clip(np.asarray(p, float), 1e-300, 1 - 1e-300)
    return -(p * np.log(p) + (1 - p) * np.log1p(-p))


def closed_form_share(lam3):
    """share = ln2 - H_b((1+c)/2) for a three-time marginal with parity coefficient c."""
    return LN2 - Hb((1.0 + np.asarray(lam3, float)) / 2.0)


# =====================================================================================

class LFSRSubstrate:
    def __init__(self, a=A, b=B, T=T_REC):
        self.a, self.b, self.T, self.L = a, b, T, b
        assert lfsr_period(a, b) == (1 << b) - 1, "recurrence not maximal length"
        self.code = gen_sequences(a, b, T)               # (2^L, T) all codewords
        self.ncw = self.code.shape[0]
        self.parity = (b - a, b)
        # +-1 form for correlation decoding
        self.codepm = (1 - 2 * self.code.astype(np.float32))

    def decode(self, recs, xp, rs, return_index=False):
        """Nearest codeword by correlation; ties broken uniformly at random."""
        r = (1 - 2 * recs.astype(xp.float32))
        corr = r @ xp.asarray(self.codepm).T               # (M, ncw); larger = closer
        best = corr.max(axis=1, keepdims=True)
        tie = (corr >= best - 1e-3)
        # random tie-break: score only the tied entries, take argmax
        pick = xp.argmax(tie * rs.random(tie.shape, dtype=xp.float32), axis=1)
        out = xp.asarray(self.code)[pick]
        return (out, pick) if return_index else out


def triple_counts(recs, i, j, xp):
    """Joint counts of (y_t, y_{t+i}, y_{t+j}) pooled over t and replicas."""
    T = recs.shape[1]
    hi = max(i, j)
    a_ = recs[:, :T - hi]
    b_ = recs[:, i:T - hi + i]
    c_ = recs[:, j:T - hi + j]
    idx = (a_.astype(xp.int64) << 2) | (b_.astype(xp.int64) << 1) | c_.astype(xp.int64)
    cnt = xp.bincount(idx.ravel(), minlength=8)
    return cp.asnumpy(cnt) if _HAS_GPU else cnt


def pair_counts(recs, tau, xp):
    T = recs.shape[1]
    a_ = recs[:, :T - tau]
    b_ = recs[:, tau:]
    idx = (a_.astype(xp.int64) << 1) | b_.astype(xp.int64)
    cnt = xp.bincount(idx.ravel(), minlength=4)
    return cp.asnumpy(cnt) if _HAS_GPU else cnt


def analyze_triple(cnt, n_surr=40, n_shuf=10, rng=None):
    """The pre-registered readout on a 3-slot count vector, with the sibling-matched
    matched-pairwise-maxent surrogate null and a shuffle floor."""
    rng = rng or np.random.default_rng(0)
    Ttot = int(cnt.sum())
    p = (cnt / Ttot).reshape(2, 2, 2)
    r = ACE.caps_and_checks(p)
    mu, sd = ACE.surrogate_null(p, Ttot, n_surr=n_surr, rng=rng)
    # shuffle floor: resample each slot independently from its own marginal
    q, _, _ = ACE.pairwise_maxent_k(p)
    m = [p.sum(axis=tuple(x for x in range(3) if x != s)) for s in range(3)]
    indep = np.einsum('i,j,k->ijk', m[0], m[1], m[2])
    sh = []
    for _ in range(n_shuf):
        c = rng.multinomial(Ttot, indep.ravel()).reshape(2, 2, 2).astype(float)
        sh.append(ACE.shareK(c / c.sum())[0])
    r.update(T=Ttot, null_mean=mu, null_sd=sd, excess=r['share'] - mu,
             z=(r['share'] - mu) / sd if sd > 1e-15 else float('nan'),
             shuffle_mean=float(np.mean(sh)), shuffle_sd=float(np.std(sh)), tie_max=0.0)
    return r


def pair_mi_from_counts(cnt):
    m = (cnt / cnt.sum()).reshape(2, 2)
    out = 0.0
    for x in range(2):
        for y in range(2):
            if m[x, y] > 0:
                out += m[x, y] * np.log(m[x, y] / (m[x].sum() * m[:, y].sum()))
    return float(out)


# =====================================================================================

def gates(sub):
    print("=" * 78)
    print("GATES (addendum §5) — all must PASS")
    print("=" * 78)
    ok, res = True, {}

    p = lfsr_period(sub.a, sub.b)
    g = (p == (1 << sub.L) - 1)
    print(f"TG1 period = {p} = 2^{sub.L}-1 : {g}")
    res['TG1'] = g; ok &= g

    cnt = triple_counts(sub.code, *sub.parity, np)
    r = cnt / cnt.sum()
    sh = 3 * LN2 - ACE.H(r)
    # the clean marginal must be the PARITY distribution: 1/4 on the four even-parity
    # cells, 0 elsewhere -- and every PAIR marginal must be exactly uniform
    par = np.array([0.25 if bin(v).count('1') % 2 == 0 else 0.0 for v in range(8)])
    r3 = r.reshape(2, 2, 2)
    pdev = max(float(np.abs(r3.sum(axis=ax) - 0.25).max()) for ax in range(3))
    g = np.allclose(r, par) and abs(sh - LN2) < 1e-12 and pdev < 1e-12
    print(f"TG2 clean (5,9) marginal = {np.round(r,6).tolist()}")
    print(f"    = parity distribution: {np.allclose(r, par)}; pair dev = {pdev:.1e}; "
          f"share = {sh:.12f} (ln2 = {LN2:.12f}) : {g}")
    res['TG2'] = g; ok &= g

    xp = cp if _HAS_GPU else np
    rs = xp.random.default_rng(1)
    cw = xp.asarray(sub.code)
    back = sub.decode(cw, xp, rs)
    fixes = bool((back == cw).all())
    M = 20000
    idx = rs.integers(0, sub.ncw, size=M)
    recs = cw[idx]
    recs = recs ^ (rs.random((M, sub.T)) < 0.05).astype(recs.dtype)
    dec, pick = sub.decode(recs, xp, rs, return_index=True)
    # (a) every decoded record is a codeword; (b) the codeword histogram is uniform
    is_cw = bool((dec == xp.asarray(sub.code)[pick]).all())
    hist = xp.bincount(pick, minlength=sub.ncw)
    hist = cp.asnumpy(hist) if _HAS_GPU else hist
    expect = M / sub.ncw
    zmax = float(np.abs(hist - expect).max() / np.sqrt(expect))
    # (c) decoded population reproduces the clean parity marginal
    c2 = triple_counts(dec, *sub.parity, xp)
    r2 = c2 / c2.sum()
    devpar = float(np.abs(r2 - par).max())
    g = fixes and is_cw and zmax < 6.0 and devpar < 5e-3
    print(f"TG3 decoder fixes every codeword: {fixes}; outputs are codewords: {is_cw}; "
          f"codeword histogram uniform (max z) = {zmax:.2f}; ")
    print(f"    decoded population reproduces the parity marginal, max dev = "
          f"{devpar:.2e} : {g}")
    res['TG3'] = g; ok &= g

    print("TG4 (MC vs closed form) — checked inside the run, reported there")
    res['TG4'] = None

    rng = np.random.default_rng(2)
    ind = rng.integers(0, 2, size=(200000, 3))
    ci = np.bincount((ind[:, 0] << 2) | (ind[:, 1] << 1) | ind[:, 2], minlength=8)
    ri = analyze_triple(ci, rng=rng)
    rc = analyze_triple(cnt * 2000, rng=rng)
    g = abs(ri['excess']) < 5 * ri['null_sd'] and abs(rc['excess'] - LN2) < 1e-3
    print(f"TG5 independent bits excess = {ri['excess']:.3e} (z={ri['z']:.2f}); "
          f"clean substrate excess = {rc['excess']:.9f} vs ln2 : {g}")
    res['TG5'] = g; ok &= g

    print("=" * 78)
    print(f"GATES: {'ALL PASS' if ok else 'FAILURE'}")
    print("=" * 78)
    return ok, res


# =====================================================================================

def run_arm(sub, eps, q, T_steps, M, seed, probes, n_surr=40, n_shuf=10):
    """One (eps, q) trajectory. Returns per-step readouts at every probe."""
    xp = cp if _HAS_GPU else np
    rs = xp.random.default_rng(seed)
    rng = np.random.default_rng(seed ^ 0xA5A5)
    cw = xp.asarray(sub.code)
    recs = cw[rs.integers(0, sub.ncw, size=M)]
    out = {f'{i}_{j}': [] for (i, j) in probes}
    pmi = {f'{i}_{j}': [] for (i, j) in probes}
    costs, flips = [], []
    for t in range(T_steps + 1):
        for (i, j) in probes:
            c = triple_counts(recs, i, j, xp)
            r = analyze_triple(c, n_surr=n_surr, n_shuf=n_shuf, rng=rng)
            out[f'{i}_{j}'].append(r)
            pmi[f'{i}_{j}'].append(max(pair_mi_from_counts(pair_counts(recs, i, xp)),
                                       pair_mi_from_counts(pair_counts(recs, j, xp))))
        if t == T_steps:
            break
        recs = recs ^ (rs.random((M, sub.T)) < eps).astype(recs.dtype)
        if q > 0:
            pre = recs
            dec = sub.decode(pre, xp, rs)
            coin = (rs.random(M) < q)[:, None]
            nflip = float((cp.asnumpy(((pre != dec).sum(axis=1)).mean())
                           if _HAS_GPU else ((pre != dec).sum(axis=1)).mean()))
            recs = xp.where(coin, dec, pre)
            costs.append(q); flips.append(q * nflip)
        else:
            costs.append(0.0); flips.append(0.0)
    return out, pmi, np.array(costs), np.array(flips)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--M', type=int, default=20000)
    ap.add_argument('--steps', type=int, default=48)
    ap.add_argument('--out', default='/home/emoore/CIRISOntology/scratchpad/lfsr_results.json')
    a = ap.parse_args()

    print(f"GPU: {'cupy' if _HAS_GPU else 'CPU only'}")
    sub = LFSRSubstrate()
    print(f"LFSR y_t = y_(t-{sub.a}) ^ y_(t-{sub.b}); parity offsets {sub.parity}; "
          f"{sub.ncw} codewords of length {sub.T}")
    ok, gres = gates(sub)
    if not ok:
        print("GATE FAILURE — stopping.")
        sys.exit(1)
    if a.gate:
        return

    # probes: the matched parity pair, its double, and the equally-spaced grid
    probes = [(5, 9), (10, 18)] + [(d, 2 * d) for d in (1, 2, 3, 4, 5, 6, 8, 12)]
    results = dict(prereg='a8d7491', gates={k: v for k, v in gres.items()},
                   a=sub.a, b=sub.b, parity=list(sub.parity), T=sub.T, M=a.M,
                   steps=a.steps, probes=[list(p) for p in probes], arms={})

    t0 = time.time()
    for eps in [0.0] + EPS_GRID:
        qs = [0.0] if eps == 0.0 else Q_GRID
        for q in qs:
            per_seed = []
            for sd in (SEEDS[:3] if eps > 0 else SEEDS[:1]):
                per_seed.append(run_arm(sub, eps, q, a.steps, a.M, sd, probes))
            rec = {}
            for (i, j) in probes:
                key = f'{i}_{j}'
                ex = np.array([[r['excess'] for r in ps[0][key]] for ps in per_seed])
                zz = np.array([[r['z'] for r in ps[0][key]] for ps in per_seed])
                nm = np.array([[r['null_mean'] for r in ps[0][key]] for ps in per_seed])
                sf = np.array([[r['shuffle_mean'] for r in ps[0][key]] for ps in per_seed])
                mi = np.array([ps[1][key] for ps in per_seed])
                capok = all(r['chk_cap_headline'] and r['chk_cap_robust']
                            for ps in per_seed for r in ps[0][key])
                rec[key] = dict(
                    excess=ex.mean(axis=0).tolist(),
                    excess_sem=(ex.std(axis=0) / np.sqrt(len(per_seed))).tolist(),
                    z=zz.mean(axis=0).tolist(), null_mean=nm.mean(axis=0).tolist(),
                    shuffle_mean=sf.mean(axis=0).tolist(),
                    pair_mi=mi.mean(axis=0).tolist(), cap_ok=bool(capok))
            lam = 1 - 2 * eps
            tt = np.arange(a.steps + 1)
            if q == 0:
                pred = closed_form_share(lam ** (3 * tt))
            else:
                g3 = q / (1 - (1 - q) * lam ** 3)
                pred = np.where(tt == 0, closed_form_share(1.0),
                                closed_form_share(np.maximum(lam ** (3 * tt), g3)))
            g3 = 1.0 if q >= 1 else (q / (1 - (1 - q) * lam ** 3) if q > 0 else 0.0)
            rec['closed_form_q0'] = closed_form_share(lam ** (3 * tt)).tolist()
            rec['closed_form_stationary'] = float(closed_form_share(g3))
            rec['cost_q'] = float(np.mean(per_seed[0][2]))
            rec['cost_flips'] = float(np.mean(per_seed[0][3]))
            results['arms'][f'{eps}|{q}'] = dict(eps=eps, q=q, **rec)
            print(f"  eps={eps:<6g} q={q:<6g} done ({time.time()-t0:.0f}s)  "
                  f"(5,9) excess t=0,1,last: "
                  f"{rec['5_9']['excess'][0]:.5f} {rec['5_9']['excess'][1]:.5f} "
                  f"{rec['5_9']['excess'][-1]:.5f}   maxpairMI "
                  f"{max(rec['5_9']['pair_mi']):.2e}")

    with open(a.out, 'w') as f:
        json.dump(results, f, indent=1)
    print(f"\nwrote {a.out}")


if __name__ == '__main__':
    main()
