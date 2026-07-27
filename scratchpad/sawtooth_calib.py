"""sawtooth_calib.py — CALIBRATION on data that ALREADY EXISTS.

Computes the P-STEP32 tooth statistic at EVERY k in the parent's k=5..24 curve
(rent_islands_results.json) and the Q2 extension k=25..32, separately for
  ARM A: minimum-size OA, ns = N0(k) = 4*ceil((k+1)/4)   -> steps at k = 0 mod 4
  ARM B: minimal linear code, ns = 2^ceil(log2(k+1))     -> steps at k = 2^j
and reports each tooth against the ln-jump in ns at that k.

Nothing here is a forward prediction. This file exists to (a) check the
ceiling-tracking mechanism's LOCATION claim on data already on disk and (b) fix
the height ratio that the forward prereg will stake.
"""
import json, os, math, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = math.log(2.0)
CONDS = [(0.01, '0.1'), (0.01, '0.5'), (0.01, '1.0nat'),
         (0.05, '0.1'), (0.05, '0.5'), (0.05, '1.0nat')]


def N0(k):
    return 4 * ((k + 1 + 3) // 4)


def mB(k):
    return int(math.ceil(math.log2(k + 1)))


def load():
    """rent[arm][(eps,label)][k] = rent_per_nat, plus ns[arm][k]."""
    rent = {'A': collections.defaultdict(dict), 'B': collections.defaultdict(dict)}
    ns = {'A': {}, 'B': {}}
    par = json.load(open(os.path.join(HERE, 'rent_islands_results.json')))
    for r in par['rows']:
        if r.get('dropped'):
            continue
        nm, k = r['name'], r['k']
        if nm.startswith('OA('):
            arm = 'A'
        elif nm.startswith('linear ['):
            arm = 'B'
        else:
            continue                      # perfect Hamming / Golay / comparators
        rent[arm][(r['eps'], r['target_label'])][k] = r['rent_per_nat']
        ns[arm][k] = r['ns']
    for arm in ('A', 'B'):
        for k in range(25, 33):
            p = os.path.join(HERE, f'rent_scaling_q2_{arm}{k}.json')
            if not os.path.exists(p):
                continue
            for r in json.load(open(p))['rows']:
                if r.get('dropped'):
                    continue
                rent[arm][(r['eps'], r['target_label'])][k] = r['rent_per_nat']
                ns[arm][k] = r['ns']
    return rent, ns


def teeth(series, kmin, kmax):
    """tooth(k) = L(k) - mean(L(k-3),L(k-2),L(k-1)); L(k)=ln rent(k)-ln rent(k-1).
    Returns {k: (tooth, sd_of_baseline)} in percentage points."""
    out = {}
    L = {}
    for k in range(kmin + 1, kmax + 1):
        if k in series and (k - 1) in series:
            L[k] = math.log(series[k]) - math.log(series[k - 1])
    for k in sorted(L):
        base = [L[j] for j in (k - 3, k - 2, k - 1) if j in L]
        if len(base) < 3:
            continue
        out[k] = (100.0 * (L[k] - float(np.mean(base))), 100.0 * float(np.std(base, ddof=1)))
    return out


def main():
    rent, ns = load()
    for arm in ('A', 'B'):
        ks = sorted(ns[arm])
        print('=' * 100)
        print(f'ARM {arm}   ns(k): ' + '  '.join(f'{k}:{ns[arm][k]}' for k in ks))
        # ln-jump in ns at each k
        jump = {k: 100.0 * (math.log(ns[arm][k]) - math.log(ns[arm][k - 1]))
                for k in ks if (k - 1) in ns[arm]}
        allt = {}
        for cond in CONDS:
            s = rent[arm][cond]
            if len(s) < 5:
                continue
            allt[cond] = teeth(s, min(s), max(s))
        if not allt:
            print('  (no rows)')
            continue
        kk = sorted(set().union(*[set(t) for t in allt.values()]))
        hdr = f'{"k":>4} {"dlnNs":>8} | ' + ' '.join(f'{f"{e}/{l}":>11}' for e, l in CONDS) + f' | {"mean":>8} {"sd_base":>8}'
        print(hdr)
        print('-' * len(hdr))
        for k in kk:
            vals = [allt[c][k][0] if c in allt and k in allt[c] else float('nan') for c in CONDS]
            sds = [allt[c][k][1] if c in allt and k in allt[c] else float('nan') for c in CONDS]
            j = jump.get(k, 0.0)
            mark = ' <== STEP' if j > 1e-9 else ''
            print(f'{k:>4} {j:>8.3f} | ' + ' '.join(f'{v:>11.3f}' for v in vals) +
                  f' | {np.nanmean(vals):>8.3f} {np.nanmean(sds):>8.4f}{mark}')
        # ratio at steps
        print()
        for k in kk:
            j = jump.get(k, 0.0)
            if j <= 1e-9:
                continue
            vals = np.array([allt[c][k][0] for c in CONDS if c in allt and k in allt[c]])
            print(f'  STEP k={k}: dln(ns)={j:.3f} pp   teeth {vals.min():.3f}..{vals.max():.3f} pp'
                  f'   ratio {vals.min()/j:.4f}..{vals.max()/j:.4f}  (mean {vals.mean()/j:.4f})')
        # non-step spread
        nonstep = np.array([allt[c][k][0] for c in CONDS for k in kk
                            if c in allt and k in allt[c] and jump.get(k, 0.0) <= 1e-9])
        if nonstep.size:
            print(f'  NON-STEP k: n={nonstep.size}  |tooth| max {np.abs(nonstep).max():.3f} pp'
                  f'  mean {nonstep.mean():.3f}  sd {nonstep.std(ddof=1):.3f}')


if __name__ == '__main__':
    main()
