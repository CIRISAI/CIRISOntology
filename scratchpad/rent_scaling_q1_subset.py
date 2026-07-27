"""rent_scaling_q1_subset.py — H-SUBSET: is H-IFF a fact about supports, or about a column order?

Pre-registered in RENT_SCALING_PREREG.md AMENDMENT 1 (commit 3b32006), frozen BEFORE this file
existed and before any random-subset structure had been evaluated in any way.

WHY THIS ARM EXISTS. Every truncation in the parents -- and in the canonical Q1 sweep -- is the
FIRST k columns of the normalised Hadamard array. For a non-linear array that ordering is
arbitrary. So a verdict on H-IFF drawn from the canonical ladder alone is strictly a statement
about `rent_islands_design_check.py`'s column order, not about supports. This arm draws random
k-column subsets instead.

ROSTER, fixed by the amendment: N in {12, 20, 24, 28}; 6 <= k <= min(N-1, 20); 5 random
k-column subsets each; numpy.random.default_rng(20260727). Sylvester orders are excluded and
the amendment says why: every truncation of a linear array is linear, hence transitive, hence
restorable by theorem (T) -- there is nothing to test and including them would inflate the
tally.

ALL DRAWS ARE MADE BEFORE ANY IS EVALUATED. draw_roster() runs to completion and is written to
the output file before the first call to aut_data, so no subset can be selected after seeing a
result.

SEARCH CAPS, per the prereg's harvest gate: NODE_BUDGET is inherited unchanged from
rent_scaling_aut.py (2e7). A structure whose search exhausts it is recorded exact=False,
reported as UNDETERMINED, and EXCLUDED from the tally rather than counted either way.
"""
import sys, os, json, time, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rent_islands_design_check as DC
import rent_scaling_aut as AUT

HERE = os.path.dirname(os.path.abspath(__file__))
SUBSET_ORDERS = [12, 20, 24, 28]
SUBSET_SEED = 20260727
N_SUBSETS = 5
KMIN, KCAP = 6, 20
EQUIV_TOL = 1e-12                      # the parents' criterion, unchanged


def oa_full(N):
    """The normalised Hadamard OA of order N as an (N x N-1) 0/1 array."""
    H = DC.hadamard(N).copy()
    H = H * np.where(H[:, [0]] == -1, -1, 1)
    return np.ascontiguousarray(((1 - H[:, 1:]) // 2).astype(np.int8))


def draw_roster():
    """Every draw, made before any evaluation. Deterministic in the declared seed."""
    rng = np.random.default_rng(SUBSET_SEED)
    out = []
    for N in SUBSET_ORDERS:
        for k in range(KMIN, min(N - 1, KCAP) + 1):
            for s in range(N_SUBSETS):
                cols = sorted(rng.choice(N - 1, size=k, replace=False).tolist())
                out.append(dict(order=N, k=k, draw=s, cols=[int(c) for c in cols],
                                label=f'H{N}/k{k}/s{s}', source=DC.had_source(N)))
    return out


def partition_key(lab):
    seen, out = {}, []
    for x in lab:
        if x not in seen:
            seen[x] = len(seen)
        out.append(seen[x])
    return tuple(out)


def evaluate(S, spec):
    S = np.unique(np.asarray(S, dtype=np.int8), axis=0)
    ns, k = S.shape
    t0 = time.time()
    a = AUT.aut_data(S)
    t_aut = time.time() - t0
    t0 = time.time()
    R, dev = AUT.profile_R(S)
    lab, nlev = AUT.profile_levels(R)
    t_prof = time.time() - t0

    orb = a['orbit_id']
    restorable = bool(dev < EQUIV_TOL)
    sz = np.array(a['orbit_sizes'], dtype=float)
    row = dict(spec)
    row.update(
        ns=int(ns), k_eff=int(k), rows_distinct=bool(ns == spec['order']),
        aut_order=a['aut_order'], perm_order=a['perm_order'],
        n_translations=a['n_translations'], orbit_sizes=a['orbit_sizes'],
        n_orbits=a['n_orbits'], transitive=a['transitive'], exact=a['exact'],
        profile_dev=float(dev), restorable=restorable,
        n_levels=int(nlev), level_sizes=sorted(
            (lab.count(t) for t in set(lab)), reverse=True),
        share_max=float(k * np.log(2) - np.log(ns)),
        orbit_imbalance=float(1.0 - (sz ** 2).sum() / ns ** 2),
        orbit_ratio=float(sz.max() / sz.min()),
        # the two verdicts
        iff_ok=bool(restorable == a['transitive']),
        orbit_eq_levels=bool(partition_key(orb) == partition_key(lab)),
        orbits_refine_levels=bool(all(lab[i] == lab[j] for i in range(ns)
                                      for j in range(ns) if orb[i] == orb[j])),
        t_aut=round(t_aut, 2), t_profile=round(t_prof, 2))
    return row


def main(out):
    roster = draw_roster()
    meta = dict(prereg='RENT_SCALING_PREREG.md AMENDMENT 1 (3b32006)',
                seed=SUBSET_SEED, orders=SUBSET_ORDERS, n_subsets=N_SUBSETS,
                kmin=KMIN, kcap=KCAP, node_budget=AUT.NODE_BUDGET,
                equiv_tol=EQUIV_TOL, n_planned=len(roster), roster=roster,
                drawn_at=time.strftime('%Y-%m-%dT%H:%M:%S'))
    json.dump(dict(meta=meta, rows=[]), open(out, 'w'), indent=1)
    print(f"drew {len(roster)} subsets from rng({SUBSET_SEED}); roster written to {out} "
          f"BEFORE any evaluation", flush=True)

    cache, rows = {}, []
    t_all = time.time()
    for spec in roster:
        N = spec['order']
        if N not in cache:
            cache[N] = oa_full(N)
        r = evaluate(cache[N][:, spec['cols']], spec)
        rows.append(r)
        print(f"  {r['label']:16s} |S|={r['ns']:3d} |Aut|={r['aut_order']:10d} "
              f"orb={str(r['orbit_sizes'])[:22]:22s} trans={str(r['transitive']):5s} "
              f"dev={r['profile_dev']:.2e} rest={str(r['restorable']):5s} "
              f"lev={r['n_levels']:3d} IFF={str(r['iff_ok']):5s} "
              f"ORB={str(r['orbit_eq_levels']):5s} exact={str(r['exact']):5s} "
              f"[{r['t_aut']:.1f}+{r['t_profile']:.1f}s]", flush=True)
        json.dump(dict(meta=meta, rows=rows), open(out, 'w'), indent=1)

    ok = [r for r in rows if r['exact']]
    und = len(rows) - len(ok)
    iff_bad = [r for r in ok if not r['iff_ok']]
    orb_bad = [r for r in ok if not r['orbit_eq_levels']]
    ref_bad = [r for r in ok if not r['orbits_refine_levels']]
    print(f"\n{'='*80}\nH-SUBSET: {len(rows)} drawn, {len(ok)} decided, {und} UNDETERMINED "
          f"(excluded)\n  H-IFF violations   : {len(iff_bad)}")
    for r in iff_bad:
        print(f"     {r['label']} orbits={r['orbit_sizes']} dev={r['profile_dev']:.2e} "
              f"restorable={r['restorable']} transitive={r['transitive']}")
    print(f"  H-ORBIT violations : {len(orb_bad)}")
    for r in orb_bad[:20]:
        print(f"     {r['label']} orbits={r['orbit_sizes']} levels={r['level_sizes']}")
    print(f"  (T) violations     : {len(ref_bad)}  <-- must be 0; nonzero = instrument fault")
    print(f"[{time.time()-t_all:.0f}s] -> {out}")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(HERE, 'rent_scaling_q1_subset.json'))
    main(ap.parse_args().out)
