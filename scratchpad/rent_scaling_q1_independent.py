"""rent_scaling_q1_independent.py — three INDEPENDENT checks on Q1's refutation.

Q1's headline is a NEGATIVE from a backtracking search ("no isometry carries S to S^c"), and a
negative from a search is only as good as the search. RENT_SCALING_PREREG.md §2.2 makes an
intransitive-but-restorable structure the falsifier of H-IFF, so before that verdict is read
the negative has to survive something other than the instrument that produced it. Three
checks, in increasing order of what they settle.

CHECK 1 — the cheap invariants, and they FAIL to certify. A column permutation preserves row
  weights, and the column Gram matrix S^T S is invariant under row permutation and only
  CONJUGATED by a column permutation. So a mismatch in either would prove intransitivity with
  no search at all. Measured: on H12/k11, H20/k19, H24/k22, H24/k23 and H28/k27 the weight
  multiset and every Gram invariant (entry multiset, sorted-row multiset, spectrum) are
  IDENTICAL for all |S|-1 translates. These designs are too regular for a cheap certificate.
  Recorded because it is the reason checks 2 and 3 are needed, and because "distance-invariant
  but not transitive" is exactly the classical distinction the prior art names.

CHECK 2 — the structural prediction the engine must reproduce. Deleting one column of H_N
  breaks the matrix's own symmetry down to a POINT STABILISER, so |P| must come out as
  |Aut(H_N)| / N and not as something arbitrary:
      H12 (Paley-I q=11):  M12 acts on 12 points, |M12|/12 = 95040/12 = 7920 = |M11|
      H24 (Paley-I q=23):  PSL(2,23) acts on the 24 points of the projective line,
                           |PSL(2,23)|/24 = 6072/24 = 253
  Both are reproduced exactly. This is the same check that validated the Mathieu chain in
  RENT_COMPARISON.md's correction, applied at full width where the refutation lives.

CHECK 3 — EXHAUSTIVE ENUMERATION of the small counterexample. H12/k5 has k = 5, so the entire
  isometry group of the cube is 5! * 2^5 = 3840 elements and every one can be tested. No
  stabiliser chain, no node budget, no pruning that could be wrong. If enumeration returns
  |Aut| = 20 with orbits [10, 2] while profile_dev is 0, H-IFF's necessity direction is dead
  on a certificate that no search was involved in producing.
"""
import sys, os, itertools, math, time
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rent_islands_design_check as DC
import rent_scaling_aut as AUT


def oa(N, k=None):
    H = DC.hadamard(N).copy()
    H = H * np.where(H[:, [0]] == -1, -1, 1)
    A = np.ascontiguousarray(((1 - H[:, 1:]) // 2).astype(np.int8))
    return np.unique(A if k is None else A[:, :k], axis=0)


# ---------------------------------------------------------------- check 1
def gram_invariants(A):
    G = A.astype(np.int64).T @ A.astype(np.int64)
    return (tuple(np.sort(G.ravel()).tolist()),
            tuple(sorted(tuple(np.sort(r).tolist()) for r in G)),
            tuple(np.round(np.sort(np.linalg.eigvalsh(G.astype(float))), 6).tolist()))


def check1(cases):
    print("--- CHECK 1: do the cheap invariants certify intransitivity? ---")
    for N, k in cases:
        S = oa(N, k)
        n = S.shape[0]
        S0 = S ^ S[0][None, :]
        bw = tuple(np.sort(S0.sum(axis=1)))
        bg = gram_invariants(S0)
        sw = sum(tuple(np.sort((S0 ^ S0[i][None, :]).sum(axis=1))) != bw for i in range(1, n))
        sg = sum(gram_invariants(S0 ^ S0[i][None, :]) != bg for i in range(1, n))
        print(f"  H{N}/k{k}: weight multiset separates {sw}/{n-1}, "
              f"Gram invariants separate {sg}/{n-1}  -> "
              f"{'CERTIFIES' if sw or sg else 'INCONCLUSIVE (search required)'}")


# ---------------------------------------------------------------- check 2
def check2():
    """The quantity the point-stabiliser argument constrains is |Aut(S)| = |P|*|C|, NOT |P|.
    Deleting one column deletes one POINT of the construction's natural action, so what
    survives is that point's stabiliser. Comparing |P| alone is simply the wrong quantity —
    on H12/k11 it reads 660 against a group of order 7920, because there |C| = 12."""
    print("\n--- CHECK 2: |Aut(S)| must equal the point stabiliser |G|/N ---")
    for N, k, gname, gorder in ((12, 11, 'M12', 95040), (24, 23, 'PSL(2,23)', 6072)):
        S = oa(N, k)
        S0 = S ^ S[0][None, :]
        out = AUT.perm_stab_order_safe(S0)
        p, ok = out[0], out[1]
        C = sum(1 for i in range(S0.shape[0])
                if AUT.perm_equiv(S0, S0 ^ S0[i][None, :]) is True)
        want = gorder // N
        print(f"  H{N}/k{k}: |Aut| = |P|*|C| = {p}*{C} = {p*C:6d}   "
              f"predicted |{gname}|/{N} = {gorder}/{N} = {want:6d}   exact={ok}   "
              f"{'MATCH' if p * C == want else '*** MISMATCH ***'}")
    print("  (the prediction is against the CONSTRUCTION's natural group, which lower-bounds")
    print("   the matrix's full automorphism group, so a match is a consistency check on the")
    print("   engine and not a proof of the order.)")


# ---------------------------------------------------------------- check 3
def check3(N=12, k=5):
    print(f"\n--- CHECK 3: H{N}/k{k} by EXHAUSTIVE ENUMERATION of all {math.factorial(k)*(1<<k)}"
          f" cube isometries ---")
    S = oa(N, k)
    n = _k = S.shape[0], S.shape[1]
    n, _k = S.shape
    target = set(map(tuple, S.tolist()))
    auts = []
    for sigma in itertools.permutations(range(_k)):
        P = S[:, list(sigma)]
        for cmask in range(1 << _k):
            c = np.array([(cmask >> b) & 1 for b in range(_k)], dtype=np.int8)
            if set(map(tuple, (P ^ c[None, :]).tolist())) == target:
                auts.append((sigma, cmask))
    par = list(range(n))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    idx = {tuple(r): i for i, r in enumerate(S.tolist())}
    for sigma, cmask in auts:
        c = np.array([(cmask >> b) & 1 for b in range(_k)], dtype=np.int8)
        img = S[:, list(sigma)] ^ c[None, :]
        for i in range(n):
            a, b = find(i), find(idx[tuple(img[i].tolist())])
            if a != b:
                par[max(a, b)] = min(a, b)
    lab = [find(i) for i in range(n)]
    sizes = sorted((lab.count(t) for t in set(lab)), reverse=True)
    R, dev = AUT.profile_R(S)
    _, nlev = AUT.profile_levels(R)
    print(f"  |Aut| enumerated = {len(auts)}   orbits = {sizes}   "
          f"transitive = {len(set(lab)) == 1}")
    print(f"  profile_dev = {dev:.3e}  -> RESTORABLE = {dev < 1e-12}   R-level-sets = {nlev}")
    print(f"  VERDICT: restorable={dev < 1e-12} and transitive={len(set(lab)) == 1}"
          f"  ->  H-IFF necessity {'REFUTED' if (dev < 1e-12) and len(set(lab)) > 1 else 'intact'}"
          f"; H-ORBIT {'REFUTED' if nlev != len(set(lab)) else 'intact'}"
          f" ({nlev} level set(s) vs {len(set(lab))} orbits)")


if __name__ == '__main__':
    t = time.time()
    check1([(12, 11), (20, 19), (24, 22), (24, 23), (28, 27)])
    check2()
    check3()
    print(f"\n[{time.time()-t:.1f}s]")
