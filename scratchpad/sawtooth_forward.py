"""sawtooth_forward.py — the forward runs staked in SAWTOOTH_FORWARD_PREREG.md (022096e).

Two kinds of run, both on rent_scaling_q2's instrument, unchanged:

  natural k      : arm B as-is, m = ceil(log2(k+1)).            -> P-AFTER / P-ABSENT (k=33,34,35)
  planted k,m    : the SAME linear family at a NON-MINIMAL m,   -> P-PLANT / P-LINEAR
                   which plants a ceiling step of n*ln2 at k.

The column rule is armB_columns' own canonical branch, applied at the forced m, so the
substrate differs from arm B in exactly one respect: the run size. Gate: dual distance d >= 3
and share_max = k*ln2 - ln(ns) exactly, else the row is discarded before any rent is read.
"""
import sys, os, json, time, argparse, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rent_islands as RI
import rent_islands_design_check as DC
import rent_scaling_q2 as Q2

LN2 = float(np.log(2))


def canonical_columns(m, k):
    """armB_columns' canonical branch (design_check.py:173-175) at a FORCED m."""
    assert (1 << m) - 1 >= k, f'm={m} has only {(1 << m) - 1} nonzero columns for k={k}'
    half = 1 << (m - 1)
    canon = list(range(half, 1 << m)) + list(range(1, half))
    return canon[:k]


def systematic_columns(m, k):
    """[I | P]: the m unit vectors, then the remaining nonzero vectors in increasing order.
    Full rank BY CONSTRUCTION for any m <= k, and all columns distinct and nonzero, so the
    dual distance is >= 3. Needed because the canonical prefix is rank-deficient when
    k < 2^(m-1) + m (at m=7, k=28 it never sets bit 5)."""
    assert (1 << m) - 1 >= k, f'm={m} has only {(1 << m) - 1} nonzero columns for k={k}'
    units = [1 << i for i in range(m)]
    rest = [c for c in range(1, 1 << m) if c not in set(units)]
    return (units + rest)[:k]


def highweight_columns(m, k):
    """Nonzero vectors of F_2^m sorted by (popcount DESCENDING, value ASCENDING), first k.
    Deterministic, full rank, and NON-DEGENERATE: high-weight columns balance every
    functional, so the code keeps a large minimum distance where systematic_columns
    collapses to d_min = 1. Needed for the linearity test, because the canonical branch is
    rank-deficient at m = 7 for every k < 33."""
    assert (1 << m) - 1 >= k, f'm={m} has only {(1 << m) - 1} nonzero columns for k={k}'
    return sorted(range(1, 1 << m), key=lambda c: (-bin(c).count('1'), c))[:k]


RULES = {'canonical': canonical_columns, 'systematic': systematic_columns,
         'hiwt': highweight_columns}


def build(k, m, rule='canonical'):
    cols = RULES[rule](m, k)
    L = Q2.LeanQuotient(f'P{k}m{m}', 'P', k, RI.MS.cols_to_G(m, cols),
                        name=f'planted linear [{k},{m}] ({rule})')
    L.cols = list(map(int, cols))
    return L


def gate(L):
    """Q2-G4: pair-uniform (dual distance >= 3) and share_max exact."""
    exact = L.k * LN2 - math.log(L.ns)
    dev = abs(L.share_max - exact)
    pd = float(L.pair_dev())
    ok = (L.d >= 3) and dev < 1e-12 and pd < 1e-12
    return ok, dict(d=int(L.d), share_max_dev=dev, pair_dev=pd)


def run(k, m, tag, rule='canonical'):
    t0 = time.time()
    L = build(k, m, rule)
    ok, g = gate(L)
    print(f'[{tag}] k={k} m={m} rule={rule} ns={L.ns} r={L.r} d={g["d"]} '
          f'share_max={L.share_max:.9f} gate={"PASS" if ok else "FAIL"} {g}', flush=True)
    if not ok:
        return None, dict(tag=tag, k=k, m=m, gate_fail=g)
    rows = []
    for eps in Q2.EPS:
        for fr in Q2.FRACS:
            rows.append(Q2.measure_rent(L, eps, fr * L.share_max, 'frac', f'{fr}'))
        for s in Q2.ABS_LEVELS:
            if s < 0.98 * L.share_max:
                rows.append(Q2.measure_rent(L, eps, s, 'abs', f'{s}nat'))
    for r in rows:
        r['tag'], r['arm'], r['planted_m'] = tag, 'P', m
        print(f'   eps={r["eps"]} {r["target_label"]:>7} rent/nat={r["rent_per_nat"]:.9f} '
              f'q*={r["q_star"]:.6e} resid={r["target_resid_rel"]:.2e} '
              f'neg_mass={r["neg_mass"]:.2e} dropped={r["dropped"]}', flush=True)
    meta = dict(tag=tag, arm='P', k=k, m=m, rule=rule, ns=L.ns, r=L.r, d=int(L.d), cols=L.cols,
                route=L.route, name=L.name, share_max=L.share_max, density=L.density,
                pair_dev=float(L.pair_dev()), gate=g, secs=round(time.time() - t0, 1))
    if hasattr(L, 'free'):
        L.free()
    return rows, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--k', type=int, required=True)
    ap.add_argument('--m', type=int, default=0, help='0 = minimal (natural arm B)')
    ap.add_argument('--rule', default='canonical', choices=['canonical','systematic','hiwt'])
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    m = a.m if a.m else int(math.ceil(math.log2(a.k + 1)))
    nat = (m == int(math.ceil(math.log2(a.k + 1))))
    tag = (f'B{a.k}' if nat else f'P{a.k}m{m}') + {'canonical': '', 'systematic': 'sys', 'hiwt': 'hw'}[a.rule]
    out = a.out or os.path.join(HERE, f'sawtooth_{tag}.json')
    rows, meta = run(a.k, m, tag, a.rule)
    json.dump({'rows': rows or [], 'meta': meta, 'natural': nat,
               'prereg': 'SAWTOOTH_FORWARD_PREREG.md @ 022096e'}, open(out, 'w'), indent=1)
    print(f'[{tag}] wrote {out}  ({meta.get("secs")} s)', flush=True)


if __name__ == '__main__':
    main()
