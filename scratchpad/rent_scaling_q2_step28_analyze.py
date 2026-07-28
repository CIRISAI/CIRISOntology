"""rent_scaling_q2_step28_analyze.py — P-STEP28 and the k=24 trend correction, adjudicated.

These are PRE-REGISTERED predictions that nobody had closed. RENT_SCALING_PREREG.md §3.3
(committed 45b6877, long before any k > 24 datum) stakes both, and
RENT_SCALING_Q2_ADJUDICATION.md covers only P-STEP32. An unclosed pre-registered prediction is
exactly what the discipline says must be reported as plainly as a survival, so this closes them.

THE RULE, quoted from the committed prereg §3.3 and applied verbatim:

  "Trend-corrected reading, and it is the one that carries the weight -- the parent's §7(a)
   statistic, which k = 24 could not receive because k = 25, 26, 27 were missing: the step's
   log-jump minus the mean log-jump within the run of four that follows it. Both k = 24 and
   k = 28 become correctable here. Predicted: positive residual at both, of order the negative
   of the ceiling's own trend-corrected tooth, with elasticity in the 1-1.5 band the parent
   measured at k <= 20. FALSIFIER: trend-corrected residual negative at both step points, or
   elasticity outside [0.3, 3] at both."

So, with L(k) = ln(rent/nat)(k) - ln(rent/nat)(k-1), FORWARD baseline (unlike P-STEP32, whose
baseline had to be backward because no run follows k=32):

    tooth(24) = L(24) - mean(L(25), L(26), L(27))
    tooth(28) = L(28) - mean(L(29), L(30), L(31))

Ceiling's own trend-corrected teeth under the same forward convention, pure design arithmetic:
    k = 24: -1.035 pp        k = 28: -0.757 pp
elasticity(k) = tooth(k) / |ceiling tooth(k)|.

THE INSTRUMENT JOIN IS A REAL HAZARD AND IS CHECKED, NOT ASSUMED. ARM A at k <= 24 comes from
rent_islands_results.json and at k >= 25 from rent_scaling_q2_A*.json. tooth(24) uses
L(25) = ln r(25) - ln r(24), which straddles the two instruments, so ANY constant offset
between them would manufacture a tooth at exactly this step. Gate Q2-G1 pins the overlap at
k = 20..24 to <= 2.3e-14 relative (rent_scaling_q2_gate.log); the join is sound and the check
is named here rather than left implicit.
"""
import sys, os, json, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CEIL = {24: -1.035, 28: -0.757}          # pp, forward convention, design arithmetic
STEPS = [24, 28]


def load():
    """ARM A rent/nat by (eps, target_label) at every k, from both sources."""
    out = {}
    R = json.load(open(os.path.join(HERE, 'rent_islands_results.json')))['rows']
    for r in R:
        if r['arm'] != 'A' or r.get('dropped'):
            continue
        out.setdefault((r['eps'], r['target_label']), {})[r['k']] = float(r['rent_per_nat'])
    src = {k: 'islands' for k in range(5, 25)}
    for k in range(25, 32):
        p = os.path.join(HERE, f'rent_scaling_q2_A{k}.json')
        if not os.path.exists(p):
            continue
        for r in json.load(open(p))['rows']:
            if r.get('dropped'):
                continue
            out.setdefault((r['eps'], r['target_label']), {})[k] = float(r['rent_per_nat'])
        src[k] = 'q2'
    return out, src


def main():
    data, src = load()
    ks = sorted({k for v in data.values() for k in v})
    print('=' * 88)
    print(f'P-STEP28 and the k=24 trend correction — ARM A.  k present: {min(ks)}..{max(ks)}')
    print(f'source: k<=24 rent_islands, k>=25 rent_scaling_q2 (join gated by Q2-G1 <= 2.3e-14)')
    print('=' * 88)

    res = {s: [] for s in STEPS}
    for step in STEPS:
        need = [step - 1, step, step + 1, step + 2, step + 3]
        print(f'\n--- step k = {step}  (baseline = run after: '
              f'{step+1}, {step+2}, {step+3}) ---')
        print(f'{"condition":24s}{"L(step)":>10s}{"base":>10s}{"tooth pp":>11s}'
              f'{"elasticity":>12s}')
        for key in sorted(data):
            v = data[key]
            if any(x not in v for x in need):
                continue
            L = lambda k: np.log(v[k]) - np.log(v[k - 1])
            base = np.mean([L(step + 1), L(step + 2), L(step + 3)])
            t = (L(step) - base) * 100
            e = t / abs(CEIL[step])
            res[step].append((key, t, e))
            print(f'eps={key[0]:<6} tgt={key[1]:<10s}{L(step):10.5f}{base:10.5f}'
                  f'{t:11.3f}{e:12.2f}')
        if not res[step]:
            print('  NO CONDITION HAS THE REQUIRED k RANGE — NOT EVALUABLE')
            continue
        tt = np.array([x[1] for x in res[step]])
        ee = np.array([x[2] for x in res[step]])
        print(f'  n={len(tt)}  positive {int((tt>0).sum())}/{len(tt)}  '
              f'mean tooth {tt.mean():+.3f} pp  (ceiling tooth {CEIL[step]:+.3f} pp)')
        print(f'  elasticity mean {ee.mean():.2f}  range [{ee.min():.2f}, {ee.max():.2f}]  '
              f'-- prereg band 1.0-1.5, falsifier outside [0.3, 3]')

    print('\n' + '=' * 88)
    print('VERDICT, by the committed prereg §3.3 falsifier')
    print('=' * 88)
    neg = {s: int((np.array([x[1] for x in res[s]]) < 0).sum()) for s in STEPS if res[s]}
    n = {s: len(res[s]) for s in STEPS if res[s]}
    out_band = {s: int(((np.array([x[2] for x in res[s]]) < 0.3) |
                        (np.array([x[2] for x in res[s]]) > 3)).sum())
                for s in STEPS if res[s]}
    for s in STEPS:
        if res[s]:
            print(f'  k={s}: negative in {neg[s]}/{n[s]}, elasticity outside [0.3,3] in '
                  f'{out_band[s]}/{n[s]}')
    both_neg = all(neg.get(s, 0) > n.get(s, 1) / 2 for s in STEPS if res[s]) and len(res[24]) \
        and len(res[28])
    both_out = all(out_band.get(s, 0) > n.get(s, 1) / 2 for s in STEPS if res[s]) and \
        len(res[24]) and len(res[28])
    if both_neg:
        v = 'FIRED — residual negative at BOTH step points'
    elif both_out:
        v = 'FIRED — elasticity outside [0.3, 3] at BOTH step points'
    else:
        pos_all = all(int((np.array([x[1] for x in res[s]]) > 0).sum()) == len(res[s])
                      for s in STEPS if res[s])
        v = ('SURVIVES, and positive in every condition at both steps' if pos_all
             else 'SURVIVES the falsifier, but not uniformly positive — report per-step')
    print(f'\n  P-STEP28 / k=24 VERDICT: {v}')
    print('\n  NOTE: the prereg makes this a FALSIFIER test, not a confirmation rule. Surviving')
    print('  a falsifier is not the same as confirming a prediction, and it is not reported as')
    print('  one. The only forward-CONFIRMED tooth in this campaign is P-STEP32.')


if __name__ == '__main__':
    main()
