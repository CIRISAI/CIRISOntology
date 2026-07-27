"""rent_scaling_q1_census.py — EXTENSION: a COMPLETE census, because H-SUBSET was underpowered.

DISCLOSURE OF MOTIVATION, in full, because this is post-hoc. AMENDMENT 1's H-SUBSET arm ran
250 random column subsets and returned 0 H-IFF violations. That result cannot be read as
support, for two reasons found only after the arm had run:

  1. NEITHER canonical counterexample is inside the arm's roster. The amendment fixed
     6 <= k <= min(N-1, 20) for cost, before any counterexample was known. The canonical
     violations are H12/k5 (k = 5, BELOW the floor) and H24/k23 (k = 23, ABOVE the cap). The
     arm could not have found either.
  2. H-IFF's necessity direction can only be violated by a RESTORABLE structure, and the arm
     produced 15 restorable rows out of 250 -- 6 after the distinct-and-non-canonical filter,
     all of them Paley-12 at k = 9, 10, 11. So the arm's power against necessity is 6, not
     236, and 0 violations out of 6 is not evidence of anything.

So the honest reading of H-SUBSET is UNDERPOWERED, not CONFIRMED, and this file is the repair.
It replaces sampling with exhaustion where exhaustion is affordable:

  CENSUS-12  every column subset of Paley-12 with 3 <= k <= 11 -- all sum_k C(11,k) = 1981 of
             them. No sampling, no seed, no selection. This settles H-IFF on that Hadamard
             order completely, and it contains the k = 5 cell where the canonical
             counterexample lives.
  CENSUS-24  every column subset of Paley-24 at k = 21, 22, 23 -- C(23,21) + C(23,22) +
             C(23,23) = 253 + 23 + 1 = 277 -- the high-k cells containing the other canonical
             counterexample, which the amendment's cap of 20 excluded.

Being exhaustive, a census has no sample-size caveat and no floor to match: every subset in
range is measured, so a count of counterexamples IS the count, and zero would be a real zero.
"""
import sys, os, json, time, argparse
from itertools import combinations
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rent_islands_design_check as DC
import rent_scaling_aut as AUT

HERE = os.path.dirname(os.path.abspath(__file__))
EQUIV_TOL = 1e-12


def oa_full(N):
    H = DC.hadamard(N).copy()
    H = H * np.where(H[:, [0]] == -1, -1, 1)
    return np.ascontiguousarray(((1 - H[:, 1:]) // 2).astype(np.int8))


def partition_key(lab):
    seen, out = {}, []
    for x in lab:
        if x not in seen:
            seen[x] = len(seen)
        out.append(seen[x])
    return tuple(out)


def evaluate(S, N, cols):
    S = np.unique(np.asarray(S, dtype=np.int8), axis=0)
    ns, k = S.shape
    a = AUT.aut_data(S)
    R, dev = AUT.profile_R(S)
    lab, nlev = AUT.profile_levels(R)
    restorable = bool(dev < EQUIV_TOL)
    return dict(order=N, k=int(k), cols=[int(c) for c in cols], ns=int(ns),
                rows_distinct=bool(ns == N),
                aut_order=a['aut_order'], perm_order=a['perm_order'],
                n_translations=a['n_translations'], orbit_sizes=a['orbit_sizes'],
                n_orbits=a['n_orbits'], transitive=a['transitive'], exact=a['exact'],
                profile_dev=float(dev), restorable=restorable, n_levels=int(nlev),
                iff_ok=bool(restorable == a['transitive']),
                orbit_eq_levels=bool(partition_key(a['orbit_id']) == partition_key(lab)),
                orbits_refine_levels=bool(all(lab[i] == lab[j] for i in range(ns)
                                              for j in range(ns)
                                              if a['orbit_id'][i] == a['orbit_id'][j])))


def census(N, ks, out):
    A = oa_full(N)
    ncol = A.shape[1]
    rows, t0 = [], time.time()
    total = sum(len(list(combinations(range(ncol), k))) for k in ks)
    print(f"CENSUS-{N}: exhaustive over k in {list(ks)}, {total} subsets of {ncol} columns",
          flush=True)
    done = 0
    for k in ks:
        ce = 0
        for cols in combinations(range(ncol), k):
            r = evaluate(A[:, list(cols)], N, cols)
            rows.append(r)
            done += 1
            if not r['iff_ok']:
                ce += 1
                print(f"    COUNTEREXAMPLE k={k} cols={list(cols)} |S|={r['ns']} "
                      f"orbits={r['orbit_sizes']} |Aut|={r['aut_order']} "
                      f"dev={r['profile_dev']:.2e} restorable={r['restorable']} "
                      f"transitive={r['transitive']}", flush=True)
        nk = [r for r in rows if r['k'] == k]
        nrest = sum(1 for r in nk if r['restorable'])
        print(f"  k={k:2d}: {len(nk):5d} subsets, {nrest:4d} restorable, {ce:3d} H-IFF "
              f"counterexamples, {sum(1 for r in nk if not r['exact'])} undetermined "
              f"[{time.time()-t0:.0f}s]", flush=True)
        json.dump(rows, open(out, 'w'), indent=1)
    json.dump(rows, open(out, 'w'), indent=1)

    print(f"\n{'='*84}\nCENSUS-{N} COMPLETE — {len(rows)} subsets, exhaustive")
    dec = [r for r in rows if r['exact']]
    rest = [r for r in dec if r['restorable']]
    ce = [r for r in dec if not r['iff_ok']]
    tviol = [r for r in dec if not r['orbits_refine_levels']]
    print(f"  decided {len(dec)}, undetermined {len(rows)-len(dec)}")
    print(f"  restorable {len(rest)}  <-- the ONLY population that can violate necessity")
    print(f"  H-IFF counterexamples {len(ce)}   ({100.0*len(ce)/max(len(rest),1):.1f}% of "
          f"restorable)")
    print(f"  (T) violations {len(tviol)}  <-- must be 0")
    byk = {}
    for r in ce:
        byk.setdefault(r['k'], 0)
        byk[r['k']] += 1
    for k in sorted(byk):
        nk = sum(1 for r in dec if r['k'] == k and r['restorable'])
        print(f"     k={k}: {byk[k]} counterexamples of {nk} restorable subsets")
    print(f"[{time.time()-t0:.0f}s] -> {out}")
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--order', type=int, default=12)
    ap.add_argument('--ks', default='')
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    ks = ([int(x) for x in a.ks.split(',')] if a.ks
          else (list(range(3, 12)) if a.order == 12 else [21, 22, 23]))
    out = a.out or os.path.join(HERE, f'rent_scaling_q1_census_{a.order}.json')
    census(a.order, ks, out)
