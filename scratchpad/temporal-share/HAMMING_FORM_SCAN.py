#!/usr/bin/env python3
"""HAMMING_FORM_SCAN -- is the true classical whole-only maximum

        maxshare(k) = (k - ceil(log2(k+1))) * ln 2   ?

Method reused from CLASSICAL_MAX_K5.py (sibling agent): the whole-only share of a
pair-uniform state p on {0,1}^k is exactly  k*ln2 - H(p)  (the pair envelope's top
is the uniform state, which is itself pair-uniform), so

        max classical share at k   =   k*ln2  -  min { H(p) : p in P_k }

with  P_k = { p in the simplex on 2^k points : phat(S) = 0 for all 1 <= |S| <= 2 }.

H is CONCAVE, so its minimum over the compact polytope P_k is attained at a VERTEX.
For k <= 4 we enumerate every vertex exactly (rational arithmetic) -- that is a
proof by exhaustion.  For k >= 5 exhaustive vertex enumeration is out of reach
(C(32,16) = 6.0e8 already), so we combine
  * exact constructions          (upper bounds on min H),
  * exact analytic lower bounds  (collision-probability / frame arguments),
  * randomised searches          (labelled SAMPLED, never presented as exhaustive).

Stages
  1  exhaustive exact vertex enumeration, k = 2, 3, 4
  2  auxiliary conjectures: max atom (exact, symmetry-reduced LP, all k) and
     max Fourier mass Q = sum_{|S|>=3} phat(S)^2  (exact at k<=4, searched above)
  3  the ladder: base lemma at k=4 and collision-monotonicity under marginals
  4  exact constructions (code states) for k = 2..7
  5  searches at k = 6, 7, 8   [SAMPLED]
  6  the Hadamard-12 orthogonal array: an exact counterexample at k = 8..11
  7  summary table

Run:  scratchpad/temporal-share/qenv/bin/python HAMMING_FORM_SCAN.py
"""

from __future__ import annotations

import itertools
import json
import math
import os
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

LN2 = math.log(2.0)
RNG = np.random.default_rng(20260725)
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Setup: the pair-uniform polytope P_k, per k
# ---------------------------------------------------------------------------


def chi(S: int, v: int) -> int:
    """Fourier character chi_S(v) = (-1)^{|S & v|}."""
    return -1 if bin(S & v).count("1") & 1 else 1


class Poly:
    """The pair-uniform polytope on {0,1}^k in standard form  A p = b, p >= 0."""

    def __init__(self, k: int):
        self.k = k
        self.N = 1 << k
        self.subsets = [1 << i for i in range(k)] + [
            (1 << i) | (1 << j) for i in range(k) for j in range(i + 1, k)
        ]
        self.r = 1 + len(self.subsets)          # rows: normalisation + Fourier
        A = np.zeros((self.r, self.N), dtype=np.int64)
        A[0, :] = 1
        for row, S in enumerate(self.subsets, start=1):
            for v in range(self.N):
                A[row, v] = chi(S, v)
        self.A_INT = A
        self.A = A.astype(float)
        self.b = np.zeros(self.r)
        self.b[0] = 1.0
        # rank check: the rows are distinct characters, hence orthogonal
        assert np.linalg.matrix_rank(self.A) == self.r
        self.dim = self.N - self.r             # affine dimension of P_k
        _u, _s, _vt = np.linalg.svd(self.A)
        self.nullspace = _vt[(_s > 1e-9).sum():]
        self.pts = np.array([[(v >> i) & 1 for i in range(k)] for v in range(self.N)],
                            dtype=np.int8)

    # -- numeric helpers ----------------------------------------------------
    def entropy(self, p: np.ndarray) -> float:
        q = p[p > 1e-15]
        return float(-(q * np.log(q)).sum())

    def in_P(self, p: np.ndarray, tol: float = 1e-9) -> bool:
        return bool(p.min() > -tol and np.abs(self.A @ p - self.b).max() < tol)

    def random_point(self, n_kicks: int = 40) -> np.ndarray:
        """A random point of P: uniform + repeated random null-space steps, each
        taken a random fraction of the way to the boundary."""
        p = np.full(self.N, 1.0 / self.N)
        for _ in range(n_kicks):
            d = self.nullspace.T @ RNG.normal(size=self.nullspace.shape[0])
            nrm = np.linalg.norm(d)
            if nrm < 1e-12:
                continue
            d /= nrm
            neg = d < -1e-14
            if not neg.any():
                continue
            t_max = float((p[neg] / -d[neg]).min())        # exact step to boundary
            cand = p + RNG.uniform(0.0, 1.0) * t_max * d
            if cand.min() >= -1e-12:
                p = np.maximum(cand, 0.0)
        return p

    # -- exact helpers ------------------------------------------------------
    def exact_solve_on_support(self, support: list[int]):
        """Unique exact rational solution of A[:, support] x = b, else None."""
        n = len(support)
        rows = [[Fraction(int(self.A_INT[rr, v])) for v in support]
                + [Fraction(int(self.b[rr]))] for rr in range(self.r)]
        piv_col: list[int] = []
        rk = 0
        for c in range(n):
            piv = next((i for i in range(rk, self.r) if rows[i][c] != 0), None)
            if piv is None:
                continue
            rows[rk], rows[piv] = rows[piv], rows[rk]
            inv = Fraction(1) / rows[rk][c]
            rows[rk] = [x * inv for x in rows[rk]]
            for i in range(self.r):
                if i != rk and rows[i][c] != 0:
                    f = rows[i][c]
                    rows[i] = [a - f * bb for a, bb in zip(rows[i], rows[rk])]
            piv_col.append(c)
            rk += 1
            if rk == self.r:
                break
        if len(piv_col) < n:
            return None                       # not a unique point
        x = [Fraction(0)] * n
        for i, c in enumerate(piv_col):
            x[c] = rows[i][n]
        for rr in range(self.r):               # verify
            acc = sum(Fraction(int(self.A_INT[rr, v])) * x[i]
                      for i, v in enumerate(support))
            if acc != Fraction(int(self.b[rr])):
                return None
        return x

    def exact_check_pair_uniform(self, probs: dict[int, Fraction]) -> bool:
        """All ten (or C(k,2)) pair marginals exactly uniform, and normalised."""
        if sum(probs.values()) != 1:
            return False
        for S in self.subsets:
            acc = sum(pr * chi(S, v) for v, pr in probs.items())
            if acc != 0:
                return False
        return True


def exact_entropy(probs) -> float:
    return sum(float(q) * math.log(1.0 / float(q)) for q in probs if q != 0)


def fmt_ln2(x: float) -> str:
    """Render a value as a multiple of ln 2 when it is one, else numerically."""
    r = x / LN2
    if abs(r - round(r)) < 1e-9:
        return f"{round(r)}*ln2"
    for d in (12, 10, 6, 20, 24, 3, 5, 7, 9, 11, 14, 18):
        if abs(x - math.log(d)) < 1e-9:
            return f"ln{d}"
    return f"{x:.9f}"


# ---------------------------------------------------------------------------
# STAGE 1 -- exhaustive exact vertex enumeration, k = 2, 3, 4
# ---------------------------------------------------------------------------

def stage1() -> dict:
    print("=" * 78)
    print("STAGE 1  EXHAUSTIVE EXACT VERTEX ENUMERATION  (k = 2, 3, 4)")
    print("=" * 78)
    print("H is concave => min over P_k is at a vertex; vertices of {Ap=b, p>=0}")
    print("are the basic feasible solutions, so enumerating all C(2^k, r) column")
    print("subsets is EXHAUSTIVE.  All arithmetic is exact (fractions.Fraction).\n")
    out: dict = {}
    for k in (2, 3, 4):
        P = Poly(k)
        n_cand = math.comb(P.N, P.r)
        print(f"k = {k}:  N = 2^{k} = {P.N} cells, r = rank(A) = {P.r}, "
              f"dim P = {P.dim}, candidate bases C({P.N},{P.r}) = {n_cand}")
        verts: dict[tuple, list[Fraction]] = {}
        for cols in itertools.combinations(range(P.N), P.r):
            sol = P.exact_solve_on_support(list(cols))
            if sol is None:
                continue
            if any(x < 0 for x in sol):
                continue
            full = [Fraction(0)] * P.N
            for i, v in enumerate(cols):
                full[v] = sol[i]
            verts[tuple(full)] = full
        V = list(verts.values())
        print(f"          distinct vertices: {len(V)}")
        recs = []
        for p in V:
            supp = [v for v in range(P.N) if p[v] != 0]
            H = exact_entropy(p)
            c = sum(x * x for x in p)                     # collision probability
            mx = max(p)                                   # largest atom
            Q = sum((sum(p[v] * chi(S, v) for v in range(P.N))) ** 2
                    for S in range(1, P.N))               # sum_{S != 0} phat(S)^2
            recs.append(dict(p=p, supp=supp, H=H, c=c, mx=mx, Q=Q))
        Hmin = min(r["H"] for r in recs)
        Hmax = max(r["H"] for r in recs)
        cmax = max(r["c"] for r in recs)
        mxmax = max(r["mx"] for r in recs)
        Qmax = max(r["Q"] for r in recs)
        argmin = [r for r in recs if r["H"] < Hmin + 1e-12]
        supports = sorted(tuple(r["supp"]) for r in argmin)
        sizes = sorted({len(s) for s in supports})
        print(f"          min H  = {Hmin:.12f}  = {fmt_ln2(Hmin)}")
        print(f"          max H over VERTICES = {Hmax:.12f} = {fmt_ln2(Hmax)}  (the")
        print(f"                envelope top k*ln2 is attained at the uniform state,")
        print(f"                which lies in P but is interior for k >= 3)")
        print(f"          => max classical share = {k}*ln2 - min H = "
              f"{k*LN2 - Hmin:.12f} = {fmt_ln2(k*LN2 - Hmin)}")
        print(f"          minimisers: {len(argmin)} vertices, support size(s) {sizes}")
        print(f"          all minimisers uniform on their support: "
              f"{all(len(set(r['p'][v] for v in r['supp'])) == 1 for r in argmin)}")
        print(f"          max collision prob  max_P sum_v p_v^2 = {cmax} = {float(cmax):.9f}")
        print(f"          max atom            max_P max_v p_v   = {mxmax} = {float(mxmax):.9f}")
        print(f"          max Fourier mass    max_P Q           = {Qmax} = {float(Qmax):.9f}")
        conj = (k - math.ceil(math.log2(k + 1))) * LN2
        got = k * LN2 - Hmin
        print(f"          Hamming form (k - ceil(log2(k+1)))*ln2 = {conj:.12f}"
              f"   -> {'MATCH' if abs(conj-got) < 1e-9 else 'MISMATCH'}")
        if k <= 3:
            for r in argmin:
                print(f"            minimiser support {r['supp']}  p = "
                      f"{[str(x) for x in r['p'] if x != 0][:1]} x {len(r['supp'])}")
        out[k] = dict(
            n_vertices=len(V), minH=Hmin, maxshare=got, conj=conj,
            match=abs(conj - got) < 1e-9,
            n_minimisers=len(argmin), minimiser_support_sizes=sizes,
            minimiser_supports=[list(s) for s in supports],
            max_collision=str(cmax), max_atom=str(mxmax), max_Q=str(Qmax),
            exhaustive=True, candidates=n_cand,
        )
        print()
    return out


# ---------------------------------------------------------------------------
# STAGE 2 -- auxiliary conjectures
# ---------------------------------------------------------------------------

def krawtchouk_table(k: int):
    """K_w(j) = sum_i (-1)^i C(j,i) C(k-j, w-i)  =  sum_{|v|=w} chi_S(v), |S| = j."""
    def C(n: int, m: int) -> int:
        return 0 if m < 0 or m > n or n < 0 else math.comb(n, m)
    tab = [[sum((-1) ** i * C(j, i) * C(k - j, w - i) for i in range(0, j + 1))
            for j in range(k + 1)] for w in range(k + 1)]
    # brute-force check of the identity  K_w(j) = sum_{|v| = w} chi_S(v), |S| = j
    for w in range(k + 1):
        for j in range(k + 1):
            S = (1 << j) - 1
            acc = sum(chi(S, v) for v in range(1 << k) if bin(v).count("1") == w)
            assert acc == tab[w][j], (k, w, j, acc, tab[w][j])
    return tab


def exact_max_atom(k: int) -> tuple[Fraction, list]:
    """EXACT max over P_k of p(v0), by symmetry reduction + exhaustive basis
    enumeration of the reduced 3-equation LP.

    P_k and the objective p(0) are invariant under the coordinate permutations
    S_k (which fix the cell 0), so averaging any optimum over S_k gives a
    weight-symmetric optimum: p(v) = p_{|v|}.  In those k+1 unknowns the
    constraints are  sum_w C(k,w) p_w = 1  and  sum_w K_w(j) C(k,w) p_w / C(k,w)
    ... written directly:  sum_w p_w * (sum_{|v|=w} chi_S(v)) = 0  for |S| = 1, 2.
    Three equations, k+1 unknowns: every vertex has <= 3 nonzero p_w, so
    enumerating C(k+1,3) bases is exhaustive.  All exact."""
    K = krawtchouk_table(k)
    # rows: [normalisation] + [j=1] + [j=2]; column w has coefficient
    rows = [[Fraction(math.comb(k, w)) for w in range(k + 1)],
            [Fraction(K[w][1]) for w in range(k + 1)],
            [Fraction(K[w][2]) for w in range(k + 1)]]
    rhs = [Fraction(1), Fraction(0), Fraction(0)]
    best = Fraction(0)
    best_sol = None
    for basis in itertools.combinations(range(k + 1), 3):
        M = [[rows[i][w] for w in basis] + [rhs[i]] for i in range(3)]
        # exact 3x3 solve
        piv_col, rk = [], 0
        for c in range(3):
            piv = next((i for i in range(rk, 3) if M[i][c] != 0), None)
            if piv is None:
                continue
            M[rk], M[piv] = M[piv], M[rk]
            inv = Fraction(1) / M[rk][c]
            M[rk] = [x * inv for x in M[rk]]
            for i in range(3):
                if i != rk and M[i][c] != 0:
                    f = M[i][c]
                    M[i] = [a - f * b for a, b in zip(M[i], M[rk])]
            piv_col.append(c)
            rk += 1
        if len(piv_col) < 3:
            continue
        x = [Fraction(0)] * 3
        for i, c in enumerate(piv_col):
            x[c] = M[i][3]
        if any(v < 0 for v in x):
            continue
        pw = [Fraction(0)] * (k + 1)
        for i, w in enumerate(basis):
            pw[w] = x[i]
        # verify exactly
        if sum(math.comb(k, w) * pw[w] for w in range(k + 1)) != 1:
            continue
        if any(sum(K[w][j] * pw[w] for w in range(k + 1)) != 0 for j in (1, 2)):
            continue
        if pw[0] > best:
            best, best_sol = pw[0], pw
    return best, best_sol


def stage2(s1: dict) -> dict:
    print("=" * 78)
    print("STAGE 2  AUXILIARY CONJECTURES  (routes to a Lean base case)")
    print("=" * 78)
    out: dict = {}

    print("(a) MAX-ATOM.  Is max_x p(x) <= 1/8 for every pair-uniform p?")
    print("    Exact, by symmetry reduction (see exact_max_atom docstring) --")
    print("    the reduced LP is solved by exhaustive basis enumeration, so this")
    print("    is an exact maximum, not a search.\n")
    print("    The threshold that would make the route work at slot count k is")
    print("    1/N0(k), N0 = the smallest support a minimiser can have (4 for k<=3,")
    print("    8 for 4<=k<=7, 12 for 8<=k<=11): max atom <= 1/N0 => sum p^2 <= 1/N0")
    print("    => H >= ln N0.  Anything above 1/N0 kills the route at that k.\n")
    print("      k   max atom (exact)      value      target 1/N0   verdict")
    atoms = {}
    for k in range(3, 9):
        mx, sol = exact_max_atom(k)
        atoms[k] = mx
        N0 = 4 if k <= 3 else (8 if k <= 7 else 12)
        tgt = Fraction(1, N0)
        verdict = (f"<= 1/{N0}: route (a) WORKS at k={k}" if mx <= tgt
                   else f"EXCEEDS 1/{N0} -- route (a) DEAD at k={k}")
        print(f"      {k}   {str(mx):>12}   {float(mx):.9f}   1/{N0:<2} = {float(tgt):.4f}  {verdict}")
        out[f"max_atom_k{k}"] = str(mx)
        if k in (4, 5):
            wts = {w: str(sol[w]) for w in range(k + 1) if sol[w] != 0}
            supp = sum(math.comb(k, w) for w in range(k + 1) if sol[w] != 0)
            print(f"          attained by the weight-symmetric state p_w = {wts}"
                  f"  (support {supp})")
    # cross-check against the exhaustive enumeration where we have it
    for k in (3, 4):
        assert str(atoms[k]) == s1[k]["max_atom"], (k, atoms[k], s1[k]["max_atom"])
    print("      cross-check vs stage-1 exhaustive vertex enumeration at k=3,4: OK")

    print("\n(b) FOURIER MASS.  Is Q = sum_{|S|>=3} phat(S)^2 <= 1 at k = 4?")
    print("    Q is convex, so its max over P_4 is at a vertex -> stage 1 is exact.")
    Q4 = s1[4]["max_Q"]
    c4 = s1[4]["max_collision"]
    print(f"      k=4:  max Q = {Q4}   (conjecture: <= 1)   -> "
          f"{'HOLDS' if Fraction(Q4) <= 1 else 'FAILS'}")
    print(f"      k=4:  max collision prob = {c4} = {float(Fraction(c4)):.9f}"
          f"   (conjecture: <= 1/8)  -> "
          f"{'HOLDS' if Fraction(c4) <= Fraction(1,8) else 'FAILS'}")
    print("      identity used: sum_v p_v^2 = (1 + Q)/2^k, so Q <= 1 <=> c <= 1/8 at k=4.")
    out["max_Q_k4"] = Q4
    out["max_collision_k4"] = c4

    # searched collision maxima for k = 5, 6, 7 (convex max: SAMPLED lower bounds)
    print("\n    Searched collision maxima (convex maximisation, SAMPLED lower")
    print("    bounds on the true max; the PROVED upper bound is 1/8 -- stage 3):")
    for k in (5, 6, 7):
        P = Poly(k)
        best = 0.0
        for _ in range(60):
            p = P.random_point()
            for _ in range(40):                      # linearise: max of convex fn
                cvec = -2.0 * p
                res = linprog(cvec, A_eq=P.A, b_eq=P.b, bounds=(0, None),
                              method="highs")
                if not res.success:
                    break
                q = res.x
                if float(q @ q) <= float(p @ p) + 1e-15:
                    break
                p = q
            best = max(best, float(p @ p))
        print(f"      k={k}: best sum_v p_v^2 found = {best:.12f}   (1/8 = 0.125)")
        out[f"searched_max_collision_k{k}"] = best
    print()
    return out


# ---------------------------------------------------------------------------
# STAGE 3 -- the ladder
# ---------------------------------------------------------------------------

def stage3() -> dict:
    print("=" * 78)
    print("STAGE 3  THE LADDER:  base lemma at k=4  +  collision-monotonicity")
    print("=" * 78)
    out: dict = {}

    print("LEMMA A (k = 4).  p pair-uniform on {0,1}^4  =>  sum_v p_v^2 <= 1/8.")
    print("  Proof in one line: with t = chi_{1234} and c_S = E_p[t*chi_S] for")
    print("  |S| <= 1,   0 <= E_p[(t - sum_{|S|<=1} c_S chi_S)^2] = 1 - sum c_S^2,")
    print("  because E_p[chi_S chi_S'] = E_p[chi_{S xor S'}] = delta_{SS'} for")
    print("  |S|,|S'| <= 1 (pair-uniformity kills degrees 1 and 2).  Every T with")
    print("  |T| >= 3 is 1234 xor S for exactly one S with |S| <= 1, so")
    print("  Q = sum_{|T|>=3} E[chi_T]^2 = sum_{|S|<=1} c_S^2 <= 1, and")
    print("  sum_v p_v^2 = (1 + Q)/16 <= 2/16 = 1/8.")
    P4 = Poly(4)
    worst = 0.0
    for _ in range(4000):
        p = P4.random_point()
        cS = np.array([sum(p[v] * chi(S, v) for v in range(16))
                       for S in range(16)])
        Q = float((cS[[S for S in range(1, 16) if bin(S).count('1') >= 3]] ** 2).sum())
        lhs = float((p * (np.array([chi(15, v) for v in range(16)])
                          - sum(cS[15 ^ S] * np.array([chi(S, v) for v in range(16)])
                                for S in [0, 1, 2, 4, 8])) ** 2).sum())
        worst = max(worst, abs(lhs - (1.0 - Q)))
        assert Q <= 1 + 1e-9, Q
        assert float(p @ p) <= 0.125 + 1e-12, float(p @ p)
    print(f"  verified on 4000 random points of P_4: identity E[(t-sum c_S chi_S)^2]")
    print(f"  = 1 - Q holds to {worst:.2e}; Q <= 1 and sum p^2 <= 1/8 never violated.")
    out["lemmaA_identity_max_dev"] = worst

    print("\nLEMMA B (monotone).  Marginalising merges atoms, which cannot decrease")
    print("  the collision probability:  sum_x (sum_y p(x,y))^2 >= sum_{x,y} p(x,y)^2;")
    print("  and any marginal of a pair-uniform state is pair-uniform.  Hence for")
    print("  every k >= 4 and every pair-uniform p on {0,1}^k,")
    print("        sum_v p_v^2  <=  (its 4-slot marginal's collision prob)  <= 1/8.")
    viol = 0
    tested = 0
    for k in (5, 6, 7, 8):
        P = Poly(k)
        for _ in range(200):
            p = P.random_point()
            c_full = float(p @ p)
            marg = p.reshape([2] * k).sum(axis=tuple(range(4, k))).ravel()
            c_marg = float(marg @ marg)
            tested += 1
            if not (c_marg >= c_full - 1e-12 and c_marg <= 0.125 + 1e-9):
                viol += 1
    print(f"  verified numerically on {tested} random points of P_5..P_8: "
          f"{viol} violations.")
    out["lemmaB_tested"] = tested
    out["lemmaB_violations"] = viol

    print("\nLEMMA C (Renyi).  H(p) >= -ln sum_v p_v^2   (Jensen on ln).")
    print("\n=> for every k >= 4:  min H >= ln 8 = 3*ln2, so share <= (k-3)*ln2.")
    print("   The SAME three-lemma shape at the trivial base k = 2 (pair-uniform on")
    print("   2 bits IS the uniform state on 4 points, c = 1/4) gives c <= 1/4 and")
    print("   share <= (k-2)*ln2 for every k >= 2 -- which is exactly the cap")
    print("   Core/ShareK.lean already proves.  Lemma A is the next rung.\n")
    return out


def max_clique(adj: list[set[int]], n: int) -> int:
    """Exact max clique by greedy-coloured branch and bound."""
    best = 0

    def expand(R: list[int], Pset: list[int]) -> None:
        nonlocal best
        while Pset:
            if len(R) + len(Pset) <= best:
                return
            v = Pset.pop()
            newP = [u for u in Pset if u in adj[v]]
            if len(R) + 1 > best:
                best = len(R) + 1
            if newP:
                expand(R + [v], newP)

    expand([], list(range(n)))
    return best


def stage3b() -> dict:
    """The collision-probability (frame / Frobenius) bounds, per k."""
    print("=" * 78)
    print("STAGE 3b  THE GENERAL-k COLLISION BOUND  (what is proved, per k)")
    print("=" * 78)
    print("Frame identity: u_v = (1, chi_1(v), ..., chi_k(v)) in {+-1}^{k+1} has")
    print("  sum_v p_v u_v u_v^T = I_{k+1}  for every pair-uniform p, and")
    print("  u_v . u_w = (k+1) - 2 d(v,w).  Taking ||.||_F^2 of both sides:")
    print("  sum_{v,w} p_v p_w ((k+1) - 2d(v,w))^2 = k+1.\n")
    out: dict = {}
    for k in range(2, 16):
        P = Poly(k) if k <= 9 else None
        if P is not None:                                # verify both identities
            U = np.ones((P.N, k + 1), dtype=np.int64)
            U[:, 1:] = 1 - 2 * P.pts
            DIST = (P.pts[:, None, :] != P.pts[None, :, :]).sum(axis=2)
            assert np.array_equal(U @ U.T, (k + 1) - 2 * DIST)
            devs = []
            for _ in range(30):
                p = P.random_point()
                M = (U * p[:, None]).T @ U
                devs.append(float(np.abs(M - np.eye(k + 1)).max()))
                W = float(p @ (((k + 1) - 2 * DIST) ** 2) @ p)
                devs.append(abs(W - (k + 1)))
            dev = max(devs)
        else:
            dev = float("nan")
        if k % 2 == 0:
            # (k+1) odd => (k+1-2d) is odd, hence nonzero, hence squared >= 1
            assert all(((k + 1) - 2 * d) ** 2 >= 1 for d in range(1, k + 1))
            cbound = Fraction(1, k + 2)
            why = f"even k: (k+1-2d)^2 >= 1 for all d >= 1  =>  c <= 1/(k+2)"
        else:
            m = (k + 1) // 2
            if m % 2 == 1:
                omega, src = 2, "distance-m graph is bipartite (m odd), so omega = 2"
            elif k in (3, 7):
                n = 1 << k
                pts = np.array([[(v >> i) & 1 for i in range(k)] for v in range(n)])
                D = (pts[:, None, :] != pts[None, :, :]).sum(axis=2)
                adj = [set(np.nonzero(D[v] == m)[0].tolist()) for v in range(n)]
                omega = max_clique(adj, n)
                src = f"exact max clique on the distance-{m} graph ({n} vertices)"
            else:
                # a clique in the distance-m graph is an equidistant code of
                # length n = 2m-1 and distance d = m; Plotkin (2d > n) gives
                # A(n,d) <= 2*floor(d/(2d-n)) = 2m.
                n_, d_ = 2 * m - 1, m
                omega = 2 * (d_ // (2 * d_ - n_))
                src = f"Plotkin: A({n_},{d_}) <= 2*floor({d_}/{2*d_-n_}) = {omega}"
            cbound = (Fraction(m, 2) - Fraction(1, omega)) / (m * m - 1)
            why = f"odd k, m = {m}: omega = {omega} ({src})  =>  c <= {cbound}"
        N0 = 4 * math.ceil((k + 1) / 4)
        tight = "TIGHT" if cbound == Fraction(1, N0) else f"loose (Hadamard N0 = {N0})"
        print(f"  k={k:>2}: identity max deviation {dev:.2e}   c <= {str(cbound):>6}"
              f" = 1/{Fraction(1)/cbound}   {tight}")
        print(f"        {why}")
        out[k] = dict(c_bound=str(cbound), N0=N0, tight=cbound == Fraction(1, N0),
                      identity_dev=dev)
    print("\n  => min H >= -ln(c bound); the bound equals ln N0(k) (the Hadamard/OA")
    print("     value) for every k in 2..12 EXCEPT k = 8, where it gives only ln 10")
    print("     against a construction at ln 12.  k = 4 is the case Lemma A closes")
    print("     (the frame bound alone gives only 1/6 there).\n")
    return out


# ---------------------------------------------------------------------------
# STAGE 4 -- exact constructions (code states)
# ---------------------------------------------------------------------------

CODES = {
    # k: (name, list of codewords as int bitmasks)
    2: ("uniform on {0,1}^2", list(range(4))),
    3: ("even-weight [3,2] code (the parity state)", [0b000, 0b011, 0b101, 0b110]),
    4: ("even-weight [4,3] code", [v for v in range(16) if bin(v).count("1") % 2 == 0]),
    5: ("[5,3] code {x : x.11100 = 0, x.00111 = 0}", None),   # filled below
    6: ("punctured [7,3] simplex code -> [6,3]", None),
    7: ("[7,3] simplex code (dual of Hamming [7,4])", None),
}


def simplex_code(m: int) -> list[int]:
    """The [2^m - 1, m] simplex code: rows = all linear functionals evaluated on
    the 2^m - 1 nonzero points.  Dual = Hamming code, dual distance 3."""
    cols = [x for x in range(1, 1 << m)]        # the 2^m - 1 nonzero columns
    words = []
    for a in range(1 << m):                     # message a in F_2^m
        w = 0
        for i, c in enumerate(cols):
            if bin(a & c).count("1") & 1:
                w |= 1 << i
        words.append(w)
    return words


def build_codes() -> None:
    """Fill in the k = 5, 6, 7 code states (idempotent)."""
    if CODES[5][1] is not None:
        return
    C5 = [v for v in range(32)
          if bin(v & 0b00111).count("1") % 2 == 0 and bin(v & 0b11100).count("1") % 2 == 0]
    CODES[5] = (CODES[5][0], C5)
    C7 = simplex_code(3)
    CODES[7] = (CODES[7][0], C7)
    C6 = sorted({w >> 1 for w in C7})           # puncture the first coordinate
    CODES[6] = (CODES[6][0], C6)


def stage4() -> dict:
    print("=" * 78)
    print("STAGE 4  EXACT CONSTRUCTIONS (upper bounds on min H), k = 2..7")
    print("=" * 78)
    out: dict = {}
    build_codes()
    for k in range(2, 8):
        name, words = CODES[k]
        P = Poly(k)
        n = len(words)
        probs = {}
        for w in words:
            probs[w] = probs.get(w, Fraction(0)) + Fraction(1, n)
        ok = P.exact_check_pair_uniform(probs)
        H = exact_entropy(list(probs.values()))
        share = k * LN2 - H
        print(f"  k={k}: {name}")
        print(f"        |support| = {len(probs)}  pair-uniform (exact): {ok}   "
              f"H = {fmt_ln2(H)} = {H:.9f}   share = {fmt_ln2(share)} = {share:.9f}")
        assert ok
        out[k] = dict(name=name, support=len(probs), H=H, share=share)
    print()
    return out


# ---------------------------------------------------------------------------
# STAGE 5 -- searches at k = 6, 7, 8   [SAMPLED, NOT EXHAUSTIVE]
# ---------------------------------------------------------------------------

def _descend(P: Poly, p: np.ndarray, floor: float = 1e-12) -> np.ndarray:
    """Frank-Wolfe on the CONCAVE H: linearise, jump to the LP vertex, repeat.
    Each jump cannot increase H (concavity of H gives f(v) <= f(p) + <grad, v-p>
    and the LP makes that inner product <= 0), so this descends to a vertex --
    a LOCAL minimiser."""
    for _ in range(60):
        g = -(1.0 + np.log(np.maximum(p, floor)))              # grad of H
        res = linprog(g, A_eq=P.A, b_eq=P.b, bounds=(0, None), method="highs")
        if not res.success:
            break
        q = np.maximum(res.x, 0.0)
        if P.entropy(q) >= P.entropy(p) - 1e-11:
            break
        p = q
    return p


def fw_min_entropy(P: Poly, n_starts: int, n_kicks: int = 12
                   ) -> tuple[float, np.ndarray, dict]:
    """Iterated local search: descend, then kick back into the interior by mixing
    with a random point of P, and descend again.  SAMPLED -- a search over local
    minima, never a proof."""
    best, best_p = float("inf"), None
    hist: dict[str, int] = {}
    for _ in range(n_starts):
        cur = _descend(P, P.random_point())
        h_cur = P.entropy(cur)
        for _ in range(n_kicks):
            alpha = RNG.uniform(0.05, 0.65)
            cand = _descend(P, (1 - alpha) * cur + alpha * P.random_point())
            h_cand = P.entropy(cand)
            if h_cand < h_cur - 1e-11:
                cur, h_cur = cand, h_cand
        key = f"{h_cur:.9f}"
        hist[key] = hist.get(key, 0) + 1
        if h_cur < best:
            best, best_p = h_cur, cur
    return best, best_p, hist


def best_known_state(k: int) -> np.ndarray:
    """The best construction we have at slot count k, as a float vector."""
    p = np.zeros(1 << k)
    if k <= 7:
        build_codes()
        words = CODES[k][1]
    else:
        H12 = paley_hadamard_12()
        OA = (1 - H12[:, 1:]) // 2
        words = [int(sum(int(OA[i, j]) << j for j in range(k))) for i in range(12)]
    for w in words:
        p[w] += 1.0 / len(words)
    return p


def stage5() -> dict:
    print("=" * 78)
    print("STAGE 5  SEARCHES AT k = 6, 7, 8      *** SAMPLED, NOT EXHAUSTIVE ***")
    print("=" * 78)
    print("Vertex enumeration is out of reach here (C(64,22) ~ 5e17 at k=6), so")
    print("these are searches.  A search can only ever give an UPPER bound on")
    print("min H (a lower bound on max share).  Nothing below is a proof.")
    print("Calibration: the same searcher, run at k = 4 and k = 5 where the answer")
    print("is known exactly, recovers 3*ln2 -- see the calibration line below.\n")
    out: dict = {}
    for k in (4, 5):
        b, _, _ = fw_min_entropy(Poly(k), 25)
        print(f"  calibration k={k}: searcher's best H = {b:.12f} = {fmt_ln2(b)}"
              f"   (exact answer 3*ln2 -> {'RECOVERED' if abs(b-3*LN2)<1e-9 else 'MISSED'})")
    print()
    plan = {6: (150, 3000), 7: (120, 1500), 8: (100, 800)}
    for k, (n_fw, n_rand) in plan.items():
        P = Poly(k)
        print(f"  k = {k}  (N = {P.N}, r = {P.r}, dim P = {P.dim})")
        best_fw, p_fw, hist = fw_min_entropy(P, n_fw)
        print(f"    Frank-Wolfe entropy minimisation, {n_fw} random starts:")
        print(f"      min H found = {best_fw:.12f} = {fmt_ln2(best_fw)}")
        top = sorted(hist.items(), key=lambda kv: -kv[1])[:4]
        print(f"      distinct H values reached (top 4 by frequency): "
              + ", ".join(f"{v}x{fmt_ln2(float(h))}" for h, v in top))
        # random-objective vertex sampling
        best_rand = float("inf")
        supports = {}
        for _ in range(n_rand):
            cvec = RNG.normal(size=P.N)
            res = linprog(cvec, A_eq=P.A, b_eq=P.b, bounds=(0, None), method="highs")
            if not res.success:
                continue
            q = np.maximum(res.x, 0.0)
            h = P.entropy(q)
            s = int((q > 1e-10).sum())
            supports[s] = supports.get(s, 0) + 1
            best_rand = min(best_rand, h)
        print(f"    random-objective vertex sampling, {n_rand} LPs:")
        print(f"      min H over sampled vertices = {best_rand:.12f} = {fmt_ln2(best_rand)}")
        print(f"      support-size histogram: {dict(sorted(supports.items()))}")
        # seeded descents: start next to the best construction and try to beat it
        seed = best_known_state(k)
        h_seed = P.entropy(seed)
        best_seed = h_seed
        for _ in range(200):
            alpha = RNG.uniform(0.02, 0.5)
            q = _descend(P, (1 - alpha) * seed + alpha * P.random_point())
            best_seed = min(best_seed, P.entropy(q))
        print(f"    seeded descents (200 perturbations of the best construction,")
        print(f"      H = {h_seed:.12f} = {fmt_ln2(h_seed)}): best H = {best_seed:.12f}"
              f" = {fmt_ln2(best_seed)}")
        print(f"      -> construction beaten: "
              f"{'YES' if best_seed < h_seed - 1e-9 else 'no'}")
        out[f"seeded_k{k}"] = dict(seed_H=h_seed, best_H=best_seed)
        best = min(best_fw, best_rand, best_seed)
        print(f"    => best (i.e. lowest) H found at k={k}: {best:.12f} = {fmt_ln2(best)}")
        print(f"       => share >= {k*LN2 - best:.12f} = {fmt_ln2(k*LN2-best)}  [SAMPLED]")
        out[k] = dict(best_H_found=best, fw=best_fw, rand=best_rand,
                      sampled=True, support_hist={str(a): b for a, b in supports.items()})
        print()
    return out


# ---------------------------------------------------------------------------
# STAGE 6 -- the Hadamard-12 orthogonal array: exact counterexample at k = 8..11
# ---------------------------------------------------------------------------

def paley_hadamard_12() -> np.ndarray:
    """Paley type-I construction, q = 11 (= 3 mod 4): a Hadamard matrix of order 12."""
    q = 11
    resid = {(x * x) % q for x in range(1, q)}
    def leg(a: int) -> int:
        a %= q
        if a == 0:
            return 0
        return 1 if a in resid else -1
    S = np.zeros((q + 1, q + 1), dtype=np.int64)
    for j in range(1, q + 1):
        S[0, j] = 1
        S[j, 0] = -1
    for a in range(q):
        for b in range(q):
            S[a + 1, b + 1] = leg(a - b)
    H = np.eye(q + 1, dtype=np.int64) + S
    assert np.array_equal(H @ H.T, 12 * np.eye(12, dtype=np.int64)), "not Hadamard"
    # normalise the first column to +1
    for i in range(12):
        if H[i, 0] == -1:
            H[i, :] *= -1
    assert np.all(H[:, 0] == 1)
    return H


def stage6() -> dict:
    print("=" * 78)
    print("STAGE 6  THE HADAMARD-12 ORTHOGONAL ARRAY  (exact counterexample)")
    print("=" * 78)
    H12 = paley_hadamard_12()
    print("  Paley(11) Hadamard matrix of order 12 built and verified: H H^T = 12 I.")
    OA = (1 - H12[:, 1:]) // 2          # 12 x 11 array over {0,1}, first col dropped
    print(f"  -> OA(12, 11, 2, 2): {OA.shape[0]} runs, {OA.shape[1]} binary factors.")
    out: dict = {}
    for k in (8, 9, 10, 11):
        cols = OA[:, :k]
        words = [int(sum(int(cols[i, j]) << j for j in range(k))) for i in range(12)]
        probs: dict[int, Fraction] = {}
        for w in words:
            probs[w] = probs.get(w, Fraction(0)) + Fraction(1, 12)
        P = Poly(k)
        ok = P.exact_check_pair_uniform(probs)
        H = exact_entropy(list(probs.values()))
        share = k * LN2 - H
        conj = (k - math.ceil(math.log2(k + 1))) * LN2
        verdict = "HAMMING FORM FALSIFIED" if share > conj + 1e-9 else "consistent"
        print(f"  k={k}: uniform on the first {k} columns -> support "
              f"{len(probs)}, pair-uniform (exact): {ok}")
        print(f"        H = {fmt_ln2(H)} = {H:.9f}   share = {share:.9f}"
              f"   vs Hamming form {conj:.9f}   -> {verdict}")
        assert ok
        out[k] = dict(support=len(probs), H=H, share=share, conj=conj,
                      falsified=share > conj + 1e-9)
    print("\n  Why the Hamming/linear-code reasoning misses these: pair-uniformity of a")
    print("  UNIFORM-ON-LINEAR-CODE state forces |C| = 2^m >= k+1 (Hamming bound), i.e.")
    print("  H = ceil(log2(k+1))*ln2.  But a state need not be uniform on a LINEAR code.")
    print("  The right constraint is the orthogonal-array one: N runs with 4 | N and")
    print("  N >= k+1 (Rao), i.e. N0(k) = 4*ceil((k+1)/4) whenever the matching Hadamard")
    print("  matrix exists.  2^ceil(log2(k+1)) = 4*ceil((k+1)/4) for k <= 7 and for")
    print("  k = 12..15, and they DIVERGE at k = 8..11 (16 vs 12), which is exactly")
    print("  where the conjecture breaks.\n")
    return out


def light_oa_check(words: list[int], k: int) -> bool:
    """Exact strength-2 check on a multiset of codewords, without building the
    2^k-dimensional constraint matrix: every pair of columns must see each of the
    four combinations equally often, and every column each value equally often."""
    n = len(words)
    if n % 4:
        return False
    for i in range(k):
        if sum((w >> i) & 1 for w in words) * 2 != n:
            return False
        for j in range(i + 1, k):
            cnt = [0, 0, 0, 0]
            for w in words:
                cnt[(((w >> i) & 1) << 1) | ((w >> j) & 1)] += 1
            if any(c * 4 != n for c in cnt):
                return False
    return True


def stage6b() -> dict:
    print("=" * 78)
    print("STAGE 6b  THE NEXT BAND, k = 12..15 (the 16-run simplex code)")
    print("=" * 78)
    S15 = simplex_code(4)                    # [15,4] simplex code, 16 words
    out: dict = {}
    for k in range(12, 16):
        words = [w & ((1 << k) - 1) for w in S15]
        distinct = len(set(words))
        ok = light_oa_check(words, k)
        H = math.log(distinct) if distinct == len(words) else float("nan")
        share = k * LN2 - H
        conj = (k - math.ceil(math.log2(k + 1))) * LN2
        print(f"  k={k}: 16 words, distinct after puncturing: {distinct}, "
              f"OA(16,{k},2,2) exact check: {ok}")
        print(f"        H = {fmt_ln2(H)}   share = {share:.9f}   "
              f"Hamming form {conj:.9f}   -> "
              f"{'agree' if abs(share-conj) < 1e-9 else 'DIVERGE'}")
        assert ok
        out[k] = dict(H=H, share=share, conj=conj)
    print("  (Here 2^ceil(log2(k+1)) = 16 = 4*ceil((k+1)/4), so the Hamming form and")
    print("   the orthogonal-array form agree again, and the conjecture is right")
    print("   for k = 13, 14, 15 -- proved by the stage-3b bound + this construction.")
    print("   k = 12 stays open the same way k = 8 does.)\n")
    return out


def stage8(s1) -> dict:
    """Count the supports that attain min H = ln 8, k = 4..7."""
    print("=" * 78)
    print("STAGE 8  THE ATTAINING SUPPORTS AT k = 4..7")
    print("=" * 78)
    print("At the optimum H = ln 8 = -ln c with c = 1/8, so p is uniform on a")
    print("support of exactly 8 points, i.e. its support is an OA(8, k, 2, 2).")
    print("Here we enumerate all 3-dimensional LINEAR codes whose uniform state is")
    print("pair-uniform, and all of their cosets (a coset of an OA is an OA: a fixed")
    print("bit-flip pattern permutes the four outcomes of every pair).\n")
    out: dict = {}
    for k in range(4, 8):
        subspaces = set()
        rng = range(1, 1 << k)
        for a in rng:
            for b in rng:
                if b <= a:
                    continue
                for c in rng:
                    if c <= b:
                        continue
                    span = frozenset({0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c})
                    if len(span) == 8:
                        subspaces.add(span)
        good = []
        for span in subspaces:
            words = sorted(span)
            if light_oa_check(words, k):
                good.append(words)
        n_cosets = 1 << (k - 3)
        total = len(good) * n_cosets
        # verify every coset really is an OA, exactly
        checked = 0
        for words in good:
            for shift in range(1 << k):
                if light_oa_check([w ^ shift for w in words], k):
                    checked += 1
        assert checked == len(good) * (1 << k)
        print(f"  k={k}: 3-dim subspaces {len(subspaces)}, of which pair-uniform: "
              f"{len(good)};  distinct cosets each: {n_cosets}")
        print(f"        => {len(good)} x {n_cosets} = {total} eight-point supports "
              f"(all {len(good)*(1<<k)} translate checks passed)")
        note = ""
        if k == 4:
            note = (f"   cross-check vs stage-1 exhaustive enumeration: "
                    f"{s1[4]['n_minimisers']} -> "
                    f"{'MATCH' if total == s1[4]['n_minimisers'] else 'MISMATCH'}")
        if k == 5:
            note = ("   cross-check vs CLASSICAL_MAX_K5.md exhaustive count (60): "
                    + ("MATCH" if total == 60 else "MISMATCH"))
        if note:
            print(note)
        out[k] = dict(n_codes=len(good), n_cosets=n_cosets, total=total)
    print("\n  Caveat: this counts the supports that are cosets of LINEAR codes.")
    print("  It is exactly the full count at k = 4 (stage 1 enumerated every vertex)")
    print("  and at k = 5 (the sibling's exhaustive 8-subset sweep found 60 and all")
    print("  60 were affine).  At k = 6, 7 it is a count of the linear ones; that it")
    print("  is the complete count rests on the (unverified here) classical fact that")
    print("  every Hadamard matrix of order 8 is equivalent to the Sylvester one.\n")
    return out


# ---------------------------------------------------------------------------
# STAGE 7 -- summary
# ---------------------------------------------------------------------------

def stage7(s1, s3b, s4, s6, s6b) -> dict:
    print("=" * 78)
    print("STAGE 7  SUMMARY TABLE")
    print("=" * 78)
    print("  upper bd on max share = k*ln2 + ln(c-bound)   [stage 3b, or the exact")
    print("                          vertex enumeration at k <= 4]")
    print("  lower bd on max share = k*ln2 - H(best construction)  [stages 4, 6, 6b]")
    print()
    print(f"  {'k':>2} {'Hamming form':>13} {'lower bd':>11} {'upper bd':>11} "
          f"{'exact?':>7}  verdict on the Hamming form")
    rows = []
    for k in range(2, 16):
        conj = (k - math.ceil(math.log2(k + 1))) * LN2
        cb = Fraction(s3b[k]["c_bound"])
        upper = k * LN2 + math.log(float(cb))
        if k in s1:                                   # exhaustive beats the frame bd
            upper = min(upper, s1[k]["maxshare"])
        if k <= 7:
            lower = s4[k]["share"]
        elif k <= 11:
            lower = s6[k]["share"]
        else:
            lower = s6b[k]["share"]
        exact = abs(upper - lower) < 1e-9
        if exact:
            verdict = ("CONFIRMED" if abs(lower - conj) < 1e-9
                       else f"FALSIFIED (true = {lower:.6f} > {conj:.6f})")
        else:
            if lower > conj + 1e-9:
                verdict = "FALSIFIED (construction already beats it)"
            elif upper < conj - 1e-9:
                verdict = "FALSIFIED (proved cap is below it)"
            elif abs(lower - conj) < 1e-9:
                verdict = "consistent, NOT exact (gap is [lower, upper])"
            else:
                verdict = "undecided (gap straddles it)"
        print(f"  {k:>2} {conj:13.9f} {lower:11.6f} {upper:11.6f} "
              f"{'YES' if exact else 'no':>7}  {verdict}")
        rows.append(dict(k=k, hamming=conj, lower=lower, upper=upper,
                         exact=exact, verdict=verdict))
    print()
    return dict(rows=rows)


def stage9() -> dict:
    """Adversarial self-check of the two load-bearing claims, by a second route."""
    print("=" * 78)
    print("STAGE 9  SELF-CHECK OF THE TWO LOAD-BEARING CLAIMS")
    print("=" * 78)
    out: dict = {}

    print("(i) The SOS certificate handed to the Lean agent, checked EXACTLY:")
    print("      1/8 - sum_v p_v^2  =  (1/16) * sum_v p_v * y(v)^2,")
    print("    y(v) = chi_{1234}(v) - sum_{|S|<=1} c_S chi_S(v),  c_S = sum_v p_v chi_{S^c}(v).")
    P4 = Poly(4)
    verts = []
    for cols in itertools.combinations(range(16), P4.r):
        sol = P4.exact_solve_on_support(list(cols))
        if sol is None or any(x < 0 for x in sol):
            continue
        full = [Fraction(0)] * 16
        for i, v in enumerate(cols):
            full[v] = sol[i]
        if full not in verts:
            verts.append(full)

    def certificate_holds(p: list[Fraction]) -> bool:
        low = [0, 1, 2, 4, 8]                      # |S| <= 1 as bitmasks
        c = {S: sum(p[v] * chi(15 ^ S, v) for v in range(16)) for S in low}
        rhs = Fraction(0)
        for v in range(16):
            y = Fraction(chi(15, v)) - sum(c[S] * chi(S, v) for S in low)
            rhs += p[v] * y * y
        lhs = Fraction(1, 8) - sum(x * x for x in p)
        return lhs == rhs / 16

    bad = [i for i, p in enumerate(verts) if not certificate_holds(p)]
    print(f"    all {len(verts)} vertices of P_4, exact rational check: "
          f"{len(bad)} failures")
    # random rational points of P_4 (convex combinations of vertices)
    fails = 0
    for _ in range(300):
        w = [Fraction(int(RNG.integers(0, 100)), 100) for _ in verts]
        tot = sum(w)
        if tot == 0:
            continue
        w = [x / tot for x in w]
        p = [sum(w[i] * verts[i][v] for i in range(len(verts))) for v in range(16)]
        assert P4.exact_check_pair_uniform({v: p[v] for v in range(16)})
        if not certificate_holds(p):
            fails += 1
    print(f"    300 random rational points of P_4, exact check: {fails} failures")
    print("    (the certificate is a polynomial identity on P_4; every term on the")
    print("     right is p_v >= 0 times a square, which is the whole proof)")
    out["certificate_vertex_failures"] = len(bad)
    out["certificate_random_failures"] = fails
    assert not bad and fails == 0

    print("\n(ii) The k = 8 counterexample, re-checked by direct combination counting")
    print("     (no Fourier transform, no polytope machinery):")
    H12 = paley_hadamard_12()
    OA = (1 - H12[:, 1:]) // 2
    rows = [tuple(int(OA[i, j]) for j in range(8)) for i in range(12)]
    counts_ok = True
    for i in range(8):
        for j in range(i + 1, 8):
            cnt: dict[tuple, int] = {}
            for r in rows:
                cnt[(r[i], r[j])] = cnt.get((r[i], r[j]), 0) + 1
            if sorted(cnt.values()) != [3, 3, 3, 3]:
                counts_ok = False
    print(f"     all 28 pairs of the 8 columns show each of the 4 combinations")
    print(f"     exactly 3 times out of 12: {counts_ok}")
    print(f"     distinct rows: {len(set(rows))} of 12  ->  H = ln 12 = "
          f"{math.log(12):.9f}")
    print(f"     share = 8*ln2 - ln12 = {8*LN2 - math.log(12):.9f}  >  "
          f"(8 - 4)*ln2 = {4*LN2:.9f}   => Hamming form falsified\n")
    assert counts_ok and len(set(rows)) == 12
    out["k8_direct_count_ok"] = counts_ok
    return out


def main() -> None:
    s1 = stage1()
    s2 = stage2(s1)
    s3 = stage3()
    s3b = stage3b()
    s4 = stage4()
    s5 = stage5()
    s6 = stage6()
    s6b = stage6b()
    s8 = stage8(s1)
    s9 = stage9()
    s7 = stage7(s1, s3b, s4, s6, s6b)
    res = dict(stage1=s1, stage2=s2, stage3=s3, stage3b=s3b, stage4=s4,
               stage5=s5, stage6=s6, stage6b=s6b, stage8=s8, stage9=s9, stage7=s7)
    with open(os.path.join(HERE, "hamming_form_scan_results.json"), "w") as f:
        json.dump(res, f, indent=1, default=str)
    print("wrote hamming_form_scan_results.json")


if __name__ == "__main__":
    main()
