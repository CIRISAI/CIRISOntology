"""rent_scaling_q2_b32_analyze.py — P-STEP32, adjudicated by the rule AMENDMENT 2 fixed.

Written BEFORE the k=32 datum existed, so the verdict is applied by rule and not by eye.

THE STATISTIC, pinned in AMENDMENT 2 (commit dbbe1d5) before any k=32 number was computed.
With L(k) = ln(rent/nat)(k) - ln(rent/nat)(k-1),

    tooth(32) = L(32) - mean(L(29), L(30), L(31))

The baseline is the run BEFORE the step, not the parent's run-after, because there is no run
after k=32 -- the campaign stops there and ARM B's next step is at k=64. It is also the better
baseline here: ARM B has no step anywhere in k = 17..31, so those three log-jumps are pure
trend.

THE PREDICTION, staked before the run: the ceiling's own tooth under this same convention is
-3.869 pp, and with the elasticity band [1.0, 2.0] that §4.3 used for P-STEP28,

    P-STEP32: tooth(32) is POSITIVE, +3.87 to +7.74 pp, in >= 4 of the 6 conditions.

    CONFIRMED         positive in >= 4 of 6 AND size inside [0.5, 2.0] x 3.869 pp
    FIRED             negative in >= 4 of 6
    BELOW RESOLUTION  anything else, with the k=29..31 residual scatter quoted as the resolution

NOT EVALUABLE is a real outcome and is reported as one: if B28..B31 are missing from the
sibling's run the residual is NOT computed and no substitute baseline is used.
"""
import sys, os, json, glob, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CEILING_TOOTH_PP = -3.869        # AMENDMENT 2, pure design arithmetic, pinned before the run
NEEDED = [28, 29, 30, 31, 32]


def load_arm(arm, kk):
    """rent/nat per (eps, target_label) for ARM `arm` at each k, from the per-k JSONs."""
    out = {}
    for k in kk:
        p = os.path.join(HERE, f'rent_scaling_q2_{arm}{k}.json')
        if not os.path.exists(p):
            continue
        try:
            rows = json.load(open(p))['rows']
        except Exception:
            continue
        for r in rows:
            if r.get('dropped'):
                continue
            key = (r['eps'], r['target_label'])
            out.setdefault(key, {})[k] = float(r['rent_per_nat'])
    return out


def main(arm):
    data = load_arm(arm, NEEDED)
    have = sorted({k for v in data.values() for k in v})
    print('=' * 84)
    print(f'P-STEP32 — ARM {arm}.  k present: {have}')
    print('=' * 84)
    missing = [k for k in NEEDED if k not in have]
    if missing:
        print(f'\n  MISSING k = {missing}')
        print('  VERDICT: NOT EVALUABLE — the pinned statistic needs L(29),L(30),L(31),L(32),')
        print('  i.e. rent/nat at k = 28..32. No substitute baseline is used (AMENDMENT 2).')
        return

    print(f'\n{"condition":22s}{"L(29)":>10s}{"L(30)":>10s}{"L(31)":>10s}'
          f'{"L(32)":>10s}{"tooth(32) pp":>14s}')
    teeth, scatter = [], []
    for key in sorted(data):
        v = data[key]
        if any(k not in v for k in NEEDED):
            continue
        L = {k: np.log(v[k]) - np.log(v[k - 1]) for k in (29, 30, 31, 32)}
        base = np.mean([L[29], L[30], L[31]])
        t = (L[32] - base) * 100
        teeth.append(t)
        scatter.append(np.std([L[29], L[30], L[31]]) * 100)
        print(f'eps={key[0]:<6} tgt={key[1]:<8s}'
              f'{L[29]:10.5f}{L[30]:10.5f}{L[31]:10.5f}{L[32]:10.5f}{t:14.3f}')

    teeth = np.array(teeth)
    n = len(teeth)
    pos = int((teeth > 0).sum())
    neg = int((teeth < 0).sum())
    lo, hi = 0.5 * abs(CEILING_TOOTH_PP), 2.0 * abs(CEILING_TOOTH_PP)
    in_band = int(((teeth >= lo) & (teeth <= hi)).sum())
    print(f'\nn conditions {n}   positive {pos}   negative {neg}')
    print(f'tooth: mean {teeth.mean():+.3f} pp   median {np.median(teeth):+.3f} pp   '
          f'range [{teeth.min():+.3f}, {teeth.max():+.3f}]')
    print(f'predicted band (elasticity [1,2] x {abs(CEILING_TOOTH_PP)} pp): '
          f'[{lo:.3f}, {hi:.3f}] pp  — inside: {in_band}/{n}')
    print(f'baseline scatter sd(L(29..31)) mean {np.mean(scatter):.3f} pp '
          f'(the resolution floor)')
    print(f'elasticity tooth/|ceiling tooth|: mean {teeth.mean()/abs(CEILING_TOOTH_PP):.2f}')

    if pos >= 4 and in_band >= 4:
        v = 'CONFIRMED'
    elif neg >= 4:
        v = 'FIRED — the sawtooth is wounded where it should have been easiest to see'
    else:
        v = 'BELOW RESOLUTION / MIXED'
    print(f'\n  P-STEP32 VERDICT: {v}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--arm', default='B')
    main(ap.parse_args().arm)
