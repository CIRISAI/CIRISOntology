"""rent_scaling_q1_verify.py — independent verification of the two H-IFF counterexamples.

A finding that kills a pre-registered hypothesis gets checked by a DIFFERENT instrument
before it is written down, and both legs of each counterexample are checked:

  leg 1  the group order and orbit structure, re-derived by FULL ENUMERATION of every
         (sigma, c) pair -- `aut_counts_exact.py`'s method, which shares no code with the
         stabiliser chain beyond numpy.

  leg 2  the equivariance, re-derived in EXACT INTEGER ARITHMETIC instead of float64.
         Grouping the cube by tie multiplicity t makes R_i(a) = sum_t C_t[i,a]/t with every
         C_t[i,a] an exact integer, so "R_i(a) does not depend on i" becomes a rational
         identity on small integers and the float64 floor never enters. This turns
         "profile_dev = 2.7e-15" into "exactly zero" or exposes it as a rounding artifact.
"""
import sys, os, json, time
import numpy as np
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rent_islands_design_check as DC
import rent_scaling_aut as AU
from aut_counts_exact import aut_order as enum_aut_order


def oa(N, k):
    H = DC.hadamard(N).copy()
    H = H * np.where(H[:, [0]] == -1, -1, 1)
    return ((1 - H[:, 1:]) // 2).astype(np.int64)[:, :k]


def exact_profile(S, chunk=1 << 16):
    """R_i(a) as exact Fractions, via per-tie-multiplicity integer accumulators.

    C[t][i,a] = # of (x, j) with x in the tie set of size t, i in that tie set, and
    |x ^ s_j| = a.  Then R_i(a) = sum_t C[t][i,a] / t, exactly.
    """
    S = np.unique(np.asarray(S, dtype=np.int64), axis=0)
    n, k = S.shape
    N = 1 << k
    pc = np.zeros(N, dtype=np.int8)
    idx = np.arange(N, dtype=np.int64)
    b = 0
    while (1 << b) < N:
        pc += ((idx >> b) & 1).astype(np.int8)
        b += 1
    del idx
    sid = (S * (1 << np.arange(k - 1, -1, -1, dtype=np.int64))[None, :]).sum(axis=1)
    C = {}
    off = None
    for lo in range(0, N, chunk):
        hi = min(lo + chunk, N)
        m = hi - lo
        x = np.arange(lo, hi, dtype=np.int64)[:, None]
        D = pc[x ^ sid[None, :]].astype(np.int64)
        tie = (D == D.min(axis=1, keepdims=True))
        tcount = tie.sum(axis=1)
        if off is None or off.shape[0] != m:
            off = (k + 1) * np.arange(m, dtype=np.int64)[:, None]
        cnt = np.bincount((D + off).ravel(), minlength=m * (k + 1)
                          ).reshape(m, k + 1)                      # n_a(x), exact ints
        for t in np.unique(tcount):
            sel = tcount == t
            acc = C.setdefault(int(t), np.zeros((n, k + 1), dtype=np.int64))
            # rows of `cnt` where x has tie multiplicity t, distributed to the tied i
            acc += tie[sel].T.astype(np.int64) @ cnt[sel]
    R = [[Fraction(0) for _ in range(k + 1)] for _ in range(n)]
    for t, acc in C.items():
        for i in range(n):
            for a in range(k + 1):
                if acc[i, a]:
                    R[i][a] += Fraction(int(acc[i, a]), t)
    exact_equiv = all(R[i][a] == R[0][a] for i in range(n) for a in range(k + 1))
    maxdev = max(abs(R[i][a] - R[0][a]) for i in range(n) for a in range(k + 1))
    return exact_equiv, maxdev, R


CASES = [('H12/k5', 12, 5), ('H24/k23', 24, 23),
         ('H20/k19-control', 20, 19), ('H12/k8-control', 12, 8),
         ('H12/k11-control', 12, 11), ('H24/k22-control', 24, 22)]


if __name__ == '__main__':
    print("=" * 92)
    print("INDEPENDENT VERIFICATION of the H-IFF counterexamples (and four controls)")
    print("=" * 92)
    out = {}
    for label, N, k in CASES:
        S = oa(N, k)
        Su = np.unique(S, axis=0)
        t0 = time.time()
        chain = AU.aut_data(S)
        t1 = time.time()
        try:
            enum = enum_aut_order(Su)
            enum_s = f"{enum}"
            agree = (enum == chain['aut_order'])
        except Exception as e:                                   # pragma: no cover
            enum, enum_s, agree = None, f'FAILED {e}', None
        t2 = time.time()
        ex_eq, maxdev, _ = exact_profile(Su)
        t3 = time.time()
        rec = dict(label=label, k=k, ns=int(len(Su)),
                   aut_chain=chain['aut_order'], aut_enumerated=enum,
                   orders_agree=agree, transitive=chain['transitive'],
                   orbit_sizes=chain['orbit_sizes'],
                   exact_equivariant=bool(ex_eq),
                   exact_max_dev=str(maxdev),
                   secs=dict(chain=round(t1 - t0, 1), enum=round(t2 - t1, 1),
                             exact=round(t3 - t2, 1)))
        out[label] = rec
        print(f"\n{label}  |S|={rec['ns']}  k={k}")
        print(f"  |Aut| stabiliser chain : {chain['aut_order']}   [{rec['secs']['chain']}s]")
        print(f"  |Aut| full enumeration : {enum_s}   [{rec['secs']['enum']}s]"
              f"   -> {'AGREE' if agree else 'DISAGREE'}")
        print(f"  orbits                 : {chain['orbit_sizes']}  "
              f"transitive={chain['transitive']}")
        print(f"  EXACT equivariance     : {ex_eq}   max |R_i(a) - R_0(a)| = {maxdev}"
              f"   [{rec['secs']['exact']}s]")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'rent_scaling_q1_verify.json'), 'w'), indent=1)
    print("\nwrote rent_scaling_q1_verify.json")
