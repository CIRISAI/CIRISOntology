"""rent_scaling_aut.py — EXACT automorphism orders, orbit structure on the support, and the
G7 decode-weight profile, for every wired Hadamard order and every truncation width.

Pre-registered in scratchpad/RENT_SCALING_PREREG.md, committed at 45b6877 BEFORE this file
existed. Question 1 there: is the restorability boundary exactly algebraic — does full upkeep
restore the design state IFF Aut(S) is transitive on the support?

WHY THE INSTRUMENT IS BUILT THIS WAY. `maintenance_sweep.find_automorphisms()` is a bounded
random search whose output saturates at its cap; reading it as a group order is what forced
RENT_COMPARISON.md's correction. `aut_counts_exact.py` fixed that by ENUMERATING every
(sigma, c) pair, which is exact but dies on anything with a large group -- and the interesting
structures here (Paley-24 at full width, the Sylvester simplex codes) have groups of order 1e8
and up. So this file counts WITHOUT enumerating:

    translate so 0 in S; then  |Aut(S)| = |P| * |C|
      P = {sigma in S_k : sigma(S) = S}            -- the pure coordinate-permutation part
      C = {c in S : exists sigma, sigma(S) = S+c}  -- and C is exactly the orbit of 0

  (proof: (sigma,c) in Aut and 0 in S forces c = sigma(0)^c in S; for fixed c the valid sigma
   form a coset of P, since (sigma,c)^-1 (tau,c) is a pure permutation.)

|P| comes from a stabiliser chain, |P| = prod_t |orbit of t under the pointwise stabiliser of
0..t-1|, and every orbit-membership question is ONE single-solution backtracking search. So the
cost is O(k^2) searches, not |Aut| of them, and the answer is a group order.

Orbits on the support come from the same primitive: s_i ~ s_j iff some coordinate permutation
carries S^s_i onto S^s_j.

SEARCH CAPS ARE DECLARED (prereg §4). Every search carries a node budget; a search that
exhausts it returns UNDETERMINED, never a count and never a decision.
"""
import sys, os, json, time, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rent_islands_design_check as DC

NODE_BUDGET = 20_000_000          # prereg §4, declared


class Budget(Exception):
    pass


# =====================================================================================
# the single primitive: is there a column permutation carrying rowset(T) onto rowset(U)?
# =====================================================================================

class PermSearch:
    """Single-solution backtracking for a column permutation pi with

        rowset( T[:, pi] ) == rowset( U )

    Positions are filled left to right; the multiset of row prefixes must match U's own at
    every depth. Rows are unordered throughout -- the row bijection is never named, which is
    what makes the prune cheap.

    Optional `pinned` fixes pi on an initial segment (that is the stabiliser chain's
    constraint). Node budget declared by the caller; exceeding it raises Budget.
    """

    def __init__(self, T, U, budget=NODE_BUDGET):
        self.T = np.asarray(T, dtype=np.int64)
        self.U = np.asarray(U, dtype=np.int64)
        self.n, self.k = self.T.shape
        assert self.U.shape == (self.n, self.k)
        self.budget = budget
        self.nodes = 0
        # target prefix signatures of U: sorted row codes on the first p+1 columns
        sig, code = [], np.zeros(self.n, dtype=np.int64)
        for p in range(self.k):
            code = 2 * code + self.U[:, p]
            sig.append(np.sort(code))
        self.sig = sig
        # column invariant, by joint colour refinement on the row/column incidence of T and
        # U together (1-WL on the bipartite graph). A coordinate permutation preserves row
        # weights, hence every colour derived from them; refining three rounds prunes far
        # harder than the raw weight multiset and costs O(rounds * n * k) once per pair.
        self.invT, self.invU = self._colours()

    def _colours(self, rounds=3):
        T, U, n, k = self.T, self.U, self.n, self.k
        rT, rU = T.sum(axis=1), U.sum(axis=1)
        cT, cU = T.sum(axis=0), U.sum(axis=0)
        for _ in range(rounds):
            kTc = [(int(cT[j]),) + tuple(sorted(int(rT[i]) for i in range(n) if T[i, j]))
                   for j in range(k)]
            kUc = [(int(cU[p]),) + tuple(sorted(int(rU[i]) for i in range(n) if U[i, p]))
                   for p in range(k)]
            kTr = [(int(rT[i]),) + tuple(sorted(int(cT[j]) for j in range(k) if T[i, j]))
                   for i in range(n)]
            kUr = [(int(rU[i]),) + tuple(sorted(int(cU[p]) for p in range(k) if U[i, p]))
                   for i in range(n)]
            mc, mr = {}, {}
            cT = np.array([mc.setdefault(x, len(mc)) for x in kTc])
            cU = np.array([mc.setdefault(x, len(mc)) for x in kUc])
            rT = np.array([mr.setdefault(x, len(mr)) for x in kTr])
            rU = np.array([mr.setdefault(x, len(mr)) for x in kUr])
        return [int(v) for v in cT], [int(v) for v in cU]

    def run(self, pinned=()):
        """Return a permutation (list of length k, pi[p] = source column) or None."""
        pinned = list(pinned)
        used = [False] * self.k
        code = np.zeros(self.n, dtype=np.int64)
        for p, j in enumerate(pinned):
            if used[j] or self.invT[j] != self.invU[p]:
                return None
            used[j] = True
            code = 2 * code + self.T[:, j]
            if not np.array_equal(np.sort(code), self.sig[p]):
                return None
        return self._rec(len(pinned), used, code, pinned)

    def _rec(self, p, used, code, acc):
        if p == self.k:
            return list(acc)
        invp = self.invU[p]
        for j in range(self.k):
            if used[j] or self.invT[j] != invp:
                continue
            self.nodes += 1
            if self.nodes > self.budget:
                raise Budget()
            nc = 2 * code + self.T[:, j]
            if not np.array_equal(np.sort(nc), self.sig[p]):
                continue
            used[j] = True
            acc.append(j)
            got = self._rec(p + 1, used, nc, acc)
            if got is not None:
                return got
            acc.pop()
            used[j] = False
        return None


def orbits_by_search(S, budget=NODE_BUDGET):
    """The orbit partition computed the slow, independent way: s_i ~ s_j iff some coordinate
    permutation carries S^s_i onto S^s_j. O(|S|^2) searches. Kept only as the cross-check on
    the generator-closure route (gate Q1-G2)."""
    S = np.unique(_rows(S), axis=0)
    n = len(S)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(n):
        for j in range(i + 1, n):
            if find(i) == find(j):
                continue
            if perm_equiv(S ^ S[i][None, :], S ^ S[j][None, :], budget):
                ra, rb = find(i), find(j)
                parent[max(ra, rb)] = min(ra, rb)
    lab = [find(i) for i in range(n)]
    u = sorted(set(lab))
    m = {x: t for t, x in enumerate(u)}
    return [m[x] for x in lab]


def perm_equiv(T, U, budget=NODE_BUDGET, pinned=()):
    """True / False / None(=UNDETERMINED, budget exhausted)."""
    try:
        return PermSearch(T, U, budget).run(pinned) is not None
    except Budget:
        return None


# =====================================================================================
# the group: exact order, and the orbit partition of the support
# =====================================================================================

def _rows(S):
    return np.asarray(S, dtype=np.int64)


def perm_stab_order_safe(S, budget=NODE_BUDGET):
    """|P| = |{sigma in S_k : sigma(S) = S}|, exactly, by a stabiliser chain.

    |P| = prod_t |O_t|,  O_t = { pi(t) : pi in P, pi(i) = i for i < t }, and each membership
    question is ONE single-solution search. Returns (order, ok) with ok False if any search
    exhausted its node budget -- in which case the order is NOT reported as a count.
    """
    S = _rows(S)
    n, k = S.shape
    srch = PermSearch(S, S, budget)
    order = 1
    pin = []
    ok = True
    gens = []
    for t in range(k):
        orb = 0
        for j in range(t, k):
            try:
                got = srch.run(pin + [j])
            except Budget:
                ok = False
                got = None
            if got is not None:
                orb += 1
                if j != t:
                    gens.append(got)              # a transversal element at this level
        if orb == 0:                       # cannot happen: pi = identity fixes S
            ok = False
            break
        order *= orb
        pin.append(t)
    return order, ok, gens


def aut_data(S, budget=NODE_BUDGET):
    """Everything Q1 needs about one support set.

    Returns dict with: ns, k, aut_order, perm_order, orbit sizes, transitive flag, and the
    orbit id of every support point (in the order the points are given).
    """
    S = np.unique(_rows(S), axis=0)
    n, k = S.shape
    base = S[0].copy()
    S0 = (S ^ base[None, :])                      # 0 in S0, row 0 is the zero row
    zrow = int(np.where(S0.sum(axis=1) == 0)[0][0])

    # ---- C = orbit of 0 = { c in S0 : exists sigma, sigma(S0) = S0 ^ c }.
    # Each success hands back an EXPLICIT automorphism, which is what makes the orbit
    # partition below free: g(x) = x[pi] ^ c.
    C, ok, gens = [], True, []
    for i in range(n):
        c = S0[i]
        try:
            pi = PermSearch(S0, S0 ^ c[None, :], budget).run()
        except Budget:
            ok, pi = False, None
        if pi is not None:
            C.append(i)
            gens.append((pi, c.copy()))
    # ---- |P|, and its transversal elements (pure permutations, c = 0)
    pord, ok2, pgens = perm_stab_order_safe(S0, budget)
    ok = ok and ok2
    zero = np.zeros(k, dtype=np.int64)
    gens += [(pi, zero) for pi in pgens]

    # ---- orbit partition, by CLOSURE under the generators found above. The transversals
    # of a stabiliser chain generate the group, and the C-representatives cover every coset
    # of P in Aut, so these generate Aut and their orbits ARE Aut's orbits. This replaces
    # O(|S|^2) further searches with a BFS; gate Q1-G2 checks |orbit(0)| == |C|, and the
    # search-based partition is kept as `orbits_by_search` for the cross-check.
    idx = {tuple(int(v) for v in r): i for i, r in enumerate(S0)}
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for pi, c in gens:
        for i in range(n):
            img = tuple(int(v) for v in (S0[i][list(pi)] ^ c))
            j = idx.get(img)
            if j is None:
                raise RuntimeError('generator does not preserve the support — bug')
            union(i, j)
    labels = [find(i) for i in range(n)]
    uniq = sorted(set(labels))
    remap = {u: t for t, u in enumerate(uniq)}
    orbit_id = [remap[l] for l in labels]
    sizes = sorted((orbit_id.count(t) for t in range(len(uniq))), reverse=True)

    return dict(ns=int(n), k=int(k), perm_order=int(pord), n_translations=len(C),
                aut_order=int(pord) * len(C), orbit_sizes=sizes,
                n_orbits=len(uniq), transitive=bool(len(uniq) == 1),
                orbit_id=orbit_id, exact=bool(ok),
                zero_orbit_size=int(sum(1 for t in orbit_id if t == orbit_id[zrow])))


# =====================================================================================
# the G7 decode-weight profile  R_i(a) = sum_x W_{x,i} * #{ j : |x ^ s_j| = a }
# =====================================================================================

def popcount_arr(n):
    pc = np.zeros(n, dtype=np.int8)
    idx = np.arange(n, dtype=np.int64)
    b = 0
    while (1 << b) < n:
        pc += ((idx >> b) & 1).astype(np.int8)
        b += 1
    return pc


def bits_to_idx(S):
    S = np.asarray(S, dtype=np.int64)
    k = S.shape[1]
    return (S * (1 << np.arange(k - 1, -1, -1, dtype=np.int64))[None, :]).sum(axis=1)


def profile_R(S, chunk=1 << 16, kmax_full=27):
    """Exact R (ns, k+1) and the prereg's profile_dev, by a full 2^k pass.

    Same normalisation as rent_islands.py: profile_dev = max |R - mean_i R| / (2^k / ns), so
    the number is a fraction of the cell mass a uniform decoder would place.
    """
    S = np.unique(_rows(S), axis=0)
    n, k = S.shape
    if k > kmax_full:
        return None, None
    N = 1 << k
    pc = popcount_arr(N)
    sid = bits_to_idx(S)
    R = np.zeros((n, k + 1), dtype=np.float64)
    off = None
    for lo in range(0, N, chunk):
        hi = min(lo + chunk, N)
        m = hi - lo
        x = np.arange(lo, hi, dtype=np.int64)[:, None]
        D = pc[x ^ sid[None, :]].astype(np.int64)            # (m, n)
        mn = D.min(axis=1, keepdims=True)
        tie = (D == mn)
        W = tie / tie.sum(axis=1, keepdims=True)
        if off is None or off.shape[0] != m:
            off = (k + 1) * np.arange(m, dtype=np.int64)[:, None]
        cnt = np.bincount((D + off).ravel(), minlength=m * (k + 1)
                          ).reshape(m, k + 1).astype(np.float64)
        R += W.T @ cnt
    dev = float(np.abs(R - R.mean(axis=0, keepdims=True)).max() / (N / n))
    return R, dev


def profile_levels(R, tol=1e-9):
    """Level-set partition of the support induced by R_i(.). Returns a label per point."""
    n = R.shape[0]
    lab = [-1] * n
    nxt = 0
    for i in range(n):
        if lab[i] >= 0:
            continue
        lab[i] = nxt
        for j in range(i + 1, n):
            if lab[j] < 0 and np.abs(R[i] - R[j]).max() <= tol * max(1.0, np.abs(R[i]).max()):
                lab[j] = nxt
        nxt += 1
    return lab, nxt


# =====================================================================================
# GATES
# =====================================================================================

def _same_part(a, b):
    ma, mb = {}, {}
    for x, y in zip(a, b):
        if ma.setdefault(x, y) != y or mb.setdefault(y, x) != x:
            return False
    return True


def gates():
    import maintenance_sweep as MS
    print("=" * 84)
    print("Q1 GATES (prereg §4)")
    print("=" * 84)
    ok = True

    print("\n--- Q1-G1: exact order reproduces every enumerated order in "
          "aut_counts_exact.json ---")
    known = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'aut_counts_exact.json')))
    specs = MS.build_structures()
    g1 = True
    for tag, rec in known.items():
        S = MS.Substrate(tag, specs[tag]).S
        d = aut_data(S)
        good = (d['aut_order'] == rec['exact']) and d['exact']
        g1 &= good
        print(f"  {tag:5s} k={d['k']:2d} |S|={d['ns']:5d}  enumerated {rec['exact']:9d}"
              f"   chain {d['aut_order']:9d}  |P|={d['perm_order']:8d}"
              f" |C|={d['n_translations']:5d}  {'OK' if good else 'MISMATCH'}")
    print(f"  Q1-G1 {'PASS' if g1 else 'FAIL'}")
    ok &= g1

    print("\n--- Q1-G2: |Aut| = |P|*|C|, |C| = orbit of 0, closure orbits == search orbits ---")
    g2 = True
    for tag in ('H8', 'H9', 'H11', 'L11', 'R12'):
        S = MS.Substrate(tag, specs[tag]).S
        d = aut_data(S)
        srch = orbits_by_search(S)
        same = _same_part(d['orbit_id'], srch)
        good = (d['n_translations'] == d['zero_orbit_size']) and same
        g2 &= good
        print(f"  {tag:5s} |C|={d['n_translations']:4d}  orbit(0)={d['zero_orbit_size']:4d}"
              f"  closure orbits={str(d['orbit_sizes']):16s} search-agrees={same}"
              f"  {'OK' if good else 'MISMATCH'}")
    # and on the two structures where the split is the whole point
    for k in (5, 6, 8):
        S = DC.maxshare_oa(k) if k >= 5 else None
        H = DC.hadamard(12).copy()
        H = H * np.where(H[:, [0]] == -1, -1, 1)
        S = ((1 - H[:, 1:]) // 2).astype(np.int64)[:, :k]
        d = aut_data(S)
        same = _same_part(d['orbit_id'], orbits_by_search(S))
        g2 &= same
        print(f"  H12/k{k:<2d} orbits={str(d['orbit_sizes']):16s} search-agrees={same}")
    print(f"  Q1-G2 {'PASS' if g2 else 'FAIL'}")
    ok &= g2

    print("\n--- Q1-G3: the dye test — planted structures with known groups ---")
    g3 = True
    cases = []
    # (a) the full cube on 4 bits: Aut = the whole isometry group, 4! * 2^4 = 384
    cube = np.array([[(i >> b) & 1 for b in range(4)] for i in range(16)], dtype=np.int64)
    cases.append(('full cube k=4', cube, 384, True))
    # (b) the even-weight code on 4 bits [4,3]: |Aut| = |PAut| * |S| = 4! * 8 = 192
    ev = np.array([r for r in cube if r.sum() % 2 == 0], dtype=np.int64)
    cases.append(('even-weight [4,3]', ev, 24 * 8, True))
    # (c) the repetition code {0000, 1111}: |Aut| = 4! * 2 = 48, transitive
    rep = np.array([[0, 0, 0, 0], [1, 1, 1, 1]], dtype=np.int64)
    cases.append(('repetition [4,1]', rep, 24 * 2, True))
    # (d) a deliberately BROKEN support with an isolated point: {000,001,010} on 3 bits.
    #     Only sigma swapping coords 1,2 with c = 0 works, so |Aut| = 2, orbits {000},{001,010}
    brk = np.array([[0, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=np.int64)
    cases.append(('broken 3-point', brk, 2, False))
    for name, S, want, want_trans in cases:
        d = aut_data(S)
        good = (d['aut_order'] == want) and (d['transitive'] == want_trans)
        g3 &= good
        print(f"  {name:20s} |Aut| want {want:5d} got {d['aut_order']:5d}"
              f"  transitive want {str(want_trans):5s} got {str(d['transitive']):5s}"
              f"  orbits={d['orbit_sizes']}  {'OK' if good else 'FAIL'}")
    print(f"  Q1-G3 {'PASS' if g3 else 'FAIL'}")
    ok &= g3

    print("\n--- Q1-G4: R_i(a) here matches rent_islands.py's stored profile_dev ---")
    stored = {}
    RJ = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     'rent_islands_results.json')))
    for r in RJ['rows']:
        stored.setdefault(r['tag'], r['profile_dev'])
    g4 = True
    for k in (8, 9, 10, 11, 16, 19, 20, 23):
        S = DC.maxshare_oa(k)
        _, dev = profile_R(S)
        want = stored[f'A{k}']
        good = abs(dev - want) < 1e-12 + 1e-9 * max(want, 1e-12)
        g4 &= good
        print(f"  A{k:<3d} stored {want:.6e}   here {dev:.6e}   {'OK' if good else 'MISMATCH'}")
    print(f"  Q1-G4 {'PASS' if g4 else 'FAIL'}")
    ok &= g4

    print("\n" + "=" * 84)
    print(f"Q1 GATES: {'ALL PASS' if ok else 'FAILURE — run stops'}")
    print("=" * 84)
    return ok


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    a = ap.parse_args()
    if a.gate:
        t = time.time()
        good = gates()
        print(f"[{time.time()-t:.1f}s]")
        sys.exit(0 if good else 1)
