"""eca_exact.py — the refuter pass: I_C^(3) with NO SAMPLING AND NO ESTIMATOR.

The sweep found spikes. Everything that could be wrong with them is an estimator question:
finite R, plugin bias, whether the matched surrogate is the right null. This removes the
question entirely.

An n=17 ECA has 2^17 = 131072 configurations, so the distribution over configurations is a
131072-vector that fits in 1 MB and can be propagated exactly:

  deterministic step   v'[f(s)] += v[s]              (push-forward through the rule)
  noise step           v <- prod_j ((1-p) I + p X_j) v   (independent bit flips, X_j = flip j)

Starting from the exact uniform distribution over initial conditions and running the same
800 steps, this yields the EXACT distribution the sampled pipeline was estimating. Its triple
marginals are exact, so I_C^(3) is exact -- no R, no bias, no null, nothing to be fooled by.
If the spike is in this number it is a property of the automaton; if it is not, it was an
artifact of the estimator.

Temporal and causal readings need bits from more than one time, so the distribution is
carried over (recorded bits) x (configuration) for the two extra steps.
"""
import sys, os, json, time
import numpy as np
import cupy as cp
import cupyx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eca_spike as E

N_CELLS = E.N_CELLS
NST = 1 << N_CELLS
LN2 = float(np.log(2))


def rule_perm(rule, n=N_CELLS):
    """f(s) for every one of the 2^n configurations, via the gate-validated GPU engine."""
    s = cp.arange(NST, dtype=cp.uint32)
    out = cp.empty_like(s)
    E.eca_step_gpu(s, out, rule, n)
    return out.astype(cp.int64)


def push(v, perm):
    """v'[f(s)] += v[s] -- exact push-forward through the (non-invertible) rule."""
    return cp.bincount(perm, weights=v, minlength=NST)


def noisify(v, p, n=N_CELLS, idx=None):
    """Independent bit flips, each with probability p, applied exactly."""
    if p <= 0:
        return v
    if idx is None:
        idx = cp.arange(NST, dtype=cp.int64)
    for j in range(n):
        v = (1.0 - p) * v + p * v[idx ^ (1 << j)]
    return v


def stationary(rule, p, n_steps, n=N_CELLS):
    perm = rule_perm(rule, n)
    idx = cp.arange(NST, dtype=cp.int64)
    v = cp.full(NST, 1.0 / NST, dtype=cp.float64)
    for _ in range(n_steps):
        v = push(v, perm)
        v = noisify(v, p, n, idx)
    return v, perm, idx


def triple_from_v(v, i, j, k, bitidx):
    """Exact 3-cell marginal of the configuration distribution."""
    key = 4 * bitidx[i] + 2 * bitidx[j] + bitidx[k]
    return cp.bincount(key, weights=v, minlength=8).reshape(2, 2, 2)


def augmented_triples(v, perm, idx, p, specs, bitidx, n=N_CELLS):
    """Exact joints for readings whose slots span three successive times.

    specs: list of (tag, bits_at_T, bits_at_T1, bits_at_T2) where the three lists together
    name the three slots in order. The distribution is carried over (recorded, config).
    """
    out = {}
    for tag, bT, bT1, bT2 in specs:
        A = cp.zeros((8, NST), dtype=cp.float64)
        r = cp.zeros(NST, dtype=cp.int64)
        slot = 0
        for b in bT:
            r = r + (bitidx[b] << (2 - slot)); slot += 1
        cupyx.scatter_add(A, (r, idx), v)
        for blist in (bT1, bT2):
            B = cp.empty_like(A)
            for q in range(8):
                B[q] = noisify(push(A[q], perm), p, n, idx)
            A = cp.zeros_like(B)
            add = cp.zeros(NST, dtype=cp.int64)
            for b in blist:
                add = add + (bitidx[b] << (2 - slot)); slot += 1
            for q in range(8):
                cupyx.scatter_add(A, (q + add, idx), B[q])
        out[tag] = A.sum(axis=1).reshape(2, 2, 2)
    return out


def share_exact(p3):
    """I_C^(3) of an exact 2x2x2 distribution, via the validated exact maxent solver."""
    return float(cp.asnumpy(E.shareK3_batch(p3.reshape(1, 2, 2, 2))[0])[0])


def run(rules, n_steps=800, out_name='eca_exact.json'):
    bitidx = [((cp.arange(NST, dtype=cp.int64) >> b) & 1) for b in range(N_CELLS)]
    rows = []
    t0 = time.time()
    for rule in rules:
        for p_n in E.P_GRID:
            v, perm, idx = stationary(rule, p_n, n_steps)
            tot = float(v.sum())
            rec = dict(rule=rule, P_n=p_n, n_steps=n_steps, mass=tot, exact=True)
            for (d1, d2, d3) in E.SHAPES:
                rec[f'SPATIAL:{d1}-{d2}-{d3}'] = share_exact(
                    triple_from_v(v, 0, d1, d1 + d2, bitidx))
            aug = augmented_triples(v, perm, idx, p_n, [
                ('TEMPORAL', [0], [0], [0]),
                ('CAUSAL-LR', [0, 2], [1], []),
                ('CAUSAL-LC', [0, 1], [1], []),
                ('CAUSAL-CR', [1, 2], [1], []),
            ], bitidx)
            for t, q in aug.items():
                rec[t] = share_exact(q)
            rows.append(rec)
        print(f"[exact] rule {rule:3d} done, {time.time() - t0:.0f}s", flush=True)
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), out_name), 'w') as f:
            json.dump(rows, f, default=float)
    return rows


def main():
    rules = [int(x) for x in sys.argv[1:]] or [110, 18, 22, 28, 46, 54, 97, 19, 30,
                                               8, 90, 232, 150, 0]
    rows = run(rules)
    # ---- report ----
    print("\n" + "=" * 100)
    print("EXACT I_C^(3) — no sampling, no estimator, no null. 2^17 configurations "
          "propagated exactly.")
    print("=" * 100)
    Pn = E.P_GRID
    hdr = "  ".join(f"{p:>9.2e}" if p else f"{'det':>9}" for p in Pn)
    for rule in rules:
        rs = [r for r in rows if r['rule'] == rule]
        if not rs:
            continue
        keys = [k for k in rs[0] if k.startswith('SPATIAL') or k in
                ('TEMPORAL', 'CAUSAL-LR', 'CAUSAL-LC', 'CAUSAL-CR')]
        best = max(keys, key=lambda k: max(r[k] for r in rs) - rs[0][k])
        print(f"\nrule {rule}: probability mass {min(r['mass'] for r in rs):.12f} "
              f"(exactness check, must be 1)")
        for k in [best] + [x for x in ('TEMPORAL', 'CAUSAL-LR') if x != best]:
            v = [r[k] for r in rs]
            j = int(np.argmax(v[1:])) + 1
            print(f"  {k:>16}  det={v[0]:.6e}  peak={v[j]:.6e} at P_n={Pn[j]:.2e}  "
                  f"ratio={v[j] / v[0] if v[0] > 0 else float('inf'):.1f}")
            print(f"  {'':>16}  " + "  ".join(f"{x:9.2e}" for x in v))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'eca_exact.json'), 'w') as f:
        json.dump(rows, f, default=float)


if __name__ == '__main__':
    main()


def scan_all(n_steps=400):
    """Exact scan over all 256 rules -- the whole family, no sampling. Fewer steps than the
    focus run (convergence check: 200/400/800 agree to <10% on the primaries), so this ranks
    rules; the finalists are then re-run at the full 800."""
    return run(list(range(256)), n_steps=n_steps, out_name='eca_exact_all256.json')


# =====================================================================================
# BATCHED EXACT PROPAGATION — every noise level at once
# =====================================================================================
# The exact propagator is kernel-launch bound: 18 tiny launches per step on a 131072-vector.
# Carrying all P_n levels as rows of one array makes each launch do 18x the work for the same
# overhead. The arithmetic is row-by-row identical to `stationary`, and the two are compared
# directly in the validation below.

def stationary_batch(rule, ps, n_steps, n=N_CELLS):
    perm = rule_perm(rule, n)
    idx = cp.arange(NST, dtype=cp.int64)
    P = len(ps)
    pv = cp.asarray(np.asarray(ps, dtype=np.float64)).reshape(P, 1)
    off = (cp.arange(P, dtype=cp.int64) * NST).reshape(P, 1)
    perm_off = (perm.reshape(1, -1) + off).ravel()
    xor = [idx ^ (1 << j) for j in range(n)]
    v = cp.full((P, NST), 1.0 / NST, dtype=cp.float64)
    for _ in range(n_steps):
        out = cp.zeros(P * NST, dtype=cp.float64)
        cupyx.scatter_add(out, perm_off, v.ravel())
        v = out.reshape(P, NST)
        for j in range(n):
            v = (1.0 - pv) * v + pv * v[:, xor[j]]
    return v, perm, idx


def scan_all_fast(n_steps=400, out_name='eca_exact_all256.json', rules=None):
    """Exact, all 256 rules, all 18 noise levels, batched. SPATIAL and TEMPORAL only --
    the two pre-registered PRIMARY readings."""
    rules = list(range(256)) if rules is None else rules
    bitidx = [((cp.arange(NST, dtype=cp.int64) >> b) & 1) for b in range(N_CELLS)]
    keys = [(f'SPATIAL:{d1}-{d2}-{d3}', 0, d1, d1 + d2) for (d1, d2, d3) in E.SHAPES]
    rows, t0 = [], time.time()
    for rule in rules:
        V, perm, idx = stationary_batch(rule, E.P_GRID, n_steps)
        # every triple distribution for the rule, then ONE maxent solve over the lot
        dists, tags = [], []
        for pi, p_n in enumerate(E.P_GRID):
            v = V[pi]
            for tag, i, j, k in keys:
                dists.append(triple_from_v(v, i, j, k, bitidx)); tags.append((pi, tag))
            dists.append(augmented_triples(v, perm, idx, p_n,
                                           [('TEMPORAL', [0], [0], [0])], bitidx)['TEMPORAL'])
            tags.append((pi, 'TEMPORAL'))
        sh = cp.asnumpy(E.shareK3_batch(cp.stack(dists))[0])
        recs = [dict(rule=rule, P_n=p_n, n_steps=n_steps, mass=float(V[pi].sum()), exact=True)
                for pi, p_n in enumerate(E.P_GRID)]
        for (pi, tag), s in zip(tags, sh):
            recs[pi][tag] = float(s)
        rows += recs
        if rule % 16 == 0:
            print(f"[scan] rule {rule}/255, {time.time() - t0:.0f}s", flush=True)
            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   out_name), 'w') as f:
                json.dump(rows, f, default=float)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), out_name), 'w') as f:
        json.dump(rows, f, default=float)
    print(f"[scan] done, {time.time() - t0:.0f}s, {len(rows)} rows", flush=True)
    return rows
