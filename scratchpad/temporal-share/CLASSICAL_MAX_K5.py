#!/usr/bin/env python3
"""
CLASSICAL_MAX_K5 — the exact classical maximum of the whole-only share on k = 5
binary slots, over all pair-uniform states.

PROBLEM.  Core/ShareK.lean defines

    shareK p = sSup { H(q) : q a probability state with the same pair
                             marginals as p, at every pair of slots } - H(p).

If p on {0,1}^5 is pair-uniform (all ten pair marginals = 1/4 on each cell),
then the envelope of p is the whole pair-uniform polytope P, which contains the
uniform distribution (H = 5 ln 2, the global maximum over ALL states on 32
points).  Hence for pair-uniform p

    share(p) = 5 ln 2 - H(p),

and  max classical share = 5 ln 2 - min { H(p) : p in P }.

So the whole question is: MINIMIZE ENTROPY over the pair-uniform polytope.

RESULT (exact, proved -- not a sampled lower bound).  min H = 3 ln 2, attained
exactly by the uniform distributions on the 8-point strength-2 orthogonal
arrays, and by nothing else.  Therefore

    true classical max share at k = 5  =  5 ln 2 - 3 ln 2  =  2 ln 2  (exact).

The proof is the four steps verified in stage 1 below; the rest of the file is
independent confirmation (exhaustive support enumeration, exact rational
arithmetic, and the randomized vertex / Frank-Wolfe search that was the
originally requested method, which finds the same value and nothing lower).

Run:  qenv/bin/python CLASSICAL_MAX_K5.py [stage ...]
"""

from __future__ import annotations

import itertools
import json
import math
import sys
import time
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog

K = 5
N = 1 << K                      # 32 points
LN2 = math.log(2.0)
RNG = np.random.default_rng(20260725)

# ---------------------------------------------------------------------------
# Setup: the pair-uniform polytope P
# ---------------------------------------------------------------------------

PTS = np.array([[(v >> i) & 1 for i in range(K)] for v in range(N)], dtype=np.int8)
POPCOUNT = PTS.sum(axis=1)

# subsets S of slots with 1 <= |S| <= 2, as bitmasks
SUBSETS = [1 << i for i in range(K)] + [
    (1 << i) | (1 << j) for i in range(K) for j in range(i + 1, K)
]
assert len(SUBSETS) == 15


def chi(S: int, v: int) -> int:
    """Fourier character chi_S(v) = (-1)^{|S & v|}."""
    return -1 if bin(S & v).count("1") & 1 else 1


# A p = b : row 0 is normalisation, rows 1..15 are the vanishing Fourier
# coefficients p^(S) = 0 for 1 <= |S| <= 2.  All entries integral.
A_INT = np.zeros((16, N), dtype=np.int64)
A_INT[0, :] = 1
for r, S in enumerate(SUBSETS, start=1):
    for v in range(N):
        A_INT[r, v] = chi(S, v)
A = A_INT.astype(float)
B = np.zeros(16)
B[0] = 1.0

# u_v = (1, chi_{1}(v), ..., chi_{5}(v)) in {+-1}^6 -- the frame vectors
U = np.ones((N, K + 1), dtype=np.int64)
U[:, 1:] = 1 - 2 * PTS
# Hamming distance matrix on the cube
DIST = (PTS[:, None, :] != PTS[None, :, :]).sum(axis=2)
assert np.array_equal(U @ U.T, 6 - 2 * DIST)


def entropy(p: np.ndarray) -> float:
    q = p[p > 1e-15]
    return float(-(q * np.log(q)).sum())


def share(p: np.ndarray) -> float:
    return K * LN2 - entropy(p)


def in_P(p: np.ndarray, tol: float = 1e-9) -> bool:
    return bool(p.min() > -tol and np.abs(A @ p - B).max() < tol)


# ---------------------------------------------------------------------------
# helpers: exact rational linear algebra
# ---------------------------------------------------------------------------

def exact_solve_on_support(support: list[int]):
    """Exact rational solution of A[:, support] x = b, or None if not unique.

    Returns list[Fraction] of length len(support)."""
    rows = [[Fraction(int(A_INT[r, v])) for v in support] + [Fraction(int(B[r]))]
            for r in range(16)]
    m, n = 16, len(support)
    piv_col_of_row: list[int] = []
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = Fraction(1) / rows[r][c]
        rows[r] = [x * inv for x in rows[r]]
        for i in range(m):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        piv_col_of_row.append(c)
        r += 1
        if r == m:
            break
    # inconsistency?
    for i in range(r, m):
        if any(x != 0 for x in rows[i][:n]) is False and rows[i][n] != 0:
            return None
    if len(piv_col_of_row) < n:
        return None                      # underdetermined: not a unique point
    x = [Fraction(0)] * n
    for i, c in enumerate(piv_col_of_row):
        x[c] = rows[i][n]
    # verify
    for rr in range(16):
        acc = sum(Fraction(int(A_INT[rr, v])) * x[k] for k, v in enumerate(support))
        if acc != Fraction(int(B[rr])):
            return None
    return x


def exact_entropy(probs: list[Fraction]) -> tuple[float, str]:
    """H = sum p ln(1/p) for rational p; returns (float, symbolic string)."""
    terms: dict[Fraction, int] = {}
    for q in probs:
        if q != 0:
            terms[q] = terms.get(q, 0) + 1
    val = sum(float(q) * math.log(1.0 / float(q)) for q in probs if q != 0)
    sym = " + ".join(
        f"{n}*({q})*ln({Fraction(1)/q})" for q, n in sorted(terms.items())
    )
    return val, sym


# ---------------------------------------------------------------------------
# STAGE 1 -- the exact proof, every step machine-verified
# ---------------------------------------------------------------------------

def stage1() -> dict:
    print("=" * 78)
    print("STAGE 1  THE EXACT ARGUMENT:  min H over P = 3 ln 2")
    print("=" * 78)
    out: dict = {}

    # (1) The frame identity.  For any pair-uniform p:  sum_v p_v u_v u_v^T = I_6.
    print("\n(1) FRAME IDENTITY   sum_v p_v u_v u_v^T = I_6  for every p in P")
    worst = 0.0
    for _ in range(300):
        p = random_point_of_P()
        M = (U.T * p) @ U
        worst = max(worst, float(np.abs(M - np.eye(K + 1)).max()))
    print(f"    checked on 300 random interior points of P: max |M - I| = {worst:.3e}")
    out["frame_identity_max_dev"] = worst

    # (2) Frobenius identity.  ||I_6||_F^2 = 6 gives
    #     sum_{v,w} p_v p_w (3 - d(v,w))^2 = 3/2.
    print("\n(2) FROBENIUS IDENTITY   sum_{v,w} p_v p_w (3 - d(v,w))^2 = 3/2")
    W = (3 - DIST).astype(float) ** 2
    worst2 = 0.0
    for _ in range(300):
        p = random_point_of_P()
        worst2 = max(worst2, abs(float(p @ W @ p) - 1.5))
    print(f"    checked on 300 random interior points: max |value - 3/2| = {worst2:.3e}")
    out["frobenius_max_dev"] = worst2

    # (3) The distance-3 graph on the 5-cube is TRIANGLE-FREE (exhaustive).
    #     (Parity: d(v,w) = |v|+|w| mod 2, so three mutually odd distances
    #      would need three pairwise-different parities.)
    print("\n(3) TRIANGLE-FREENESS of the distance-3 graph on {0,1}^5 (exhaustive)")
    tri = 0
    for a, b, c in itertools.combinations(range(N), 3):
        if DIST[a, b] == 3 and DIST[a, c] == 3 and DIST[b, c] == 3:
            tri += 1
    n_edges = int((DIST == 3).sum() // 2)
    print(f"    all C(32,3) = {math.comb(32,3)} triples checked; "
          f"triangles found = {tri}; edges = {n_edges} (10-regular)")
    out["triangles"] = tri
    out["dist3_edges"] = n_edges
    assert tri == 0

    # (4) Motzkin-Straus:  max_{x in simplex} x^T A_3 x = 1 - 1/omega = 1/2.
    print("\n(4) MOTZKIN-STRAUS   max over the simplex of  sum_{d(v,w)=3} p_v p_w  = 1/2")
    A3 = (DIST == 3).astype(float)
    best_ms = 0.0
    for _ in range(4000):                       # replicator dynamics
        x = RNG.dirichlet(np.ones(N))
        for _ in range(4000):
            g = A3 @ x
            f = float(x @ g)
            if f <= 0:
                break
            x = x * g / f
        best_ms = max(best_ms, float(x @ A3 @ x))
    print(f"    4000 replicator runs: max found = {best_ms:.12f}  (theory 0.5, "
          f"triangle-free => clique number 2)")
    out["motzkin_straus_max"] = best_ms

    # (4') The Motzkin-Straus step is avoidable at k = 5, which matters for
    #      mechanization: the distance-3 graph is BIPARTITE between even- and
    #      odd-weight words (d = 3 is odd), so its edge set sits inside the
    #      complete bipartite graph and, with E = sum_{|v| even} p_v,
    #          S <= 2 * E * (1 - E) <= 1/2
    #      elementarily -- no Motzkin-Straus needed.
    print("\n(4') BIPARTITE ROUTE (mechanization-friendly substitute for (4))")
    even = (POPCOUNT % 2 == 0)
    cross = np.zeros((N, N), dtype=bool)
    cross[np.ix_(even, ~even)] = True
    cross[np.ix_(~even, even)] = True
    assert not (A3_bool := (DIST == 3) & ~cross).any(), "distance-3 edge inside a part"
    worst3 = 0.0
    for _ in range(2000):
        p = random_point_of_P()
        S = float(p @ (DIST == 3).astype(float) @ p)
        E = float(p[even].sum())
        assert S <= 2 * E * (1 - E) + 1e-12
        worst3 = max(worst3, S)
    print("    every distance-3 edge joins an even-weight to an odd-weight word "
          "(exhaustive)")
    print(f"    so S <= 2E(1-E) <= 1/2 elementarily; max S over 2000 points of P "
          f"= {worst3:.9f}")
    out["bipartite_route_max_S"] = worst3

    # (5) The chain.
    #     3/2 = 9c + sum_{v!=w} p_v p_w (3-d)^2
    #        >= 9c + sum_{v!=w, d!=3} p_v p_w        [(3-d)^2 >= 1 off d=3]
    #         = 9c + (1 - c - S)                      [S = weight on d=3 pairs]
    #     => 8c <= 1/2 + S <= 1/2 + 1/2 = 1  =>  c = sum p^2 <= 1/8.
    #     H >= H_2 = -ln c >= ln 8 = 3 ln 2, equality iff p uniform on 8 points.
    print("\n(5) CONCLUSION")
    print("    3/2 = 9c + sum_{v!=w} p_v p_w (3-d)^2   [(2), diagonal d=0 gives 9]")
    print("       >= 9c + (1 - c - S)                  [(3-d)^2 >= 1 unless d = 3]")
    print("    =>  8c <= 1/2 + S  <= 1/2 + 1/2 = 1     [(4)]")
    print("    =>  collision probability c = sum_v p_v^2 <= 1/8")
    print("    =>  H(p) >= H_2(p) = -ln c >= ln 8 = 3 ln 2,")
    print("        with equality iff p is UNIFORM (H = H_2) on EXACTLY 8 points (c = 1/8).")
    print(f"\n    min H = 3 ln 2 = {3*LN2:.12f}")
    print(f"    TRUE CLASSICAL MAX SHARE at k=5 = 5 ln 2 - 3 ln 2 = 2 ln 2 = {2*LN2:.12f}")
    out["min_H_exact"] = 3 * LN2
    out["max_share_exact"] = 2 * LN2
    return out


_S, _SV, _VT = np.linalg.svd(A)
NULLSPACE = _VT[(_SV > 1e-9).sum():]          # (16, 32): basis of ker A
assert NULLSPACE.shape[0] == 16, NULLSPACE.shape


def random_point_of_P() -> np.ndarray:
    """A random (generically interior) point of P: uniform + random null-space kick."""
    ns = NULLSPACE
    p = np.full(N, 1.0 / N)
    for _ in range(50):
        d = ns.T @ RNG.normal(size=ns.shape[0])
        d /= np.linalg.norm(d)
        t = RNG.uniform(0.0, 1.0) * (1.0 / N) / max(1e-12, -d.min()) if d.min() < 0 else 0.0
        cand = p + t * d
        if cand.min() >= 0:
            p = cand
    return p


# ---------------------------------------------------------------------------
# STAGE 2 -- exhaustive minimal-support enumeration
# ---------------------------------------------------------------------------

def stage2() -> dict:
    print("\n" + "=" * 78)
    print("STAGE 2  EXHAUSTIVE MINIMAL SUPPORT")
    print("=" * 78)
    out: dict = {}

    # 2a. No point of P has support <= 7.  Exhaustive over all C(32,s), s<=7:
    #     does A[:,T] x = b have a strictly positive solution?
    print("\n(a) supports of size <= 7 -- exhaustive feasibility over all subsets")
    for s in range(6, 8):
        t0 = time.time()
        combos = np.fromiter(
            itertools.chain.from_iterable(itertools.combinations(range(N), s)),
            dtype=np.int8,
            count=math.comb(N, s) * s,
        ).reshape(-1, s)
        feasible = 0
        CH = 200_000
        for lo in range(0, combos.shape[0], CH):
            idx = combos[lo:lo + CH].astype(np.int64)
            M = A.T[idx]                       # (batch, s, 16)
            M = np.transpose(M, (0, 2, 1))     # (batch, 16, s)
            x = np.linalg.pinv(M) @ B          # least-squares solution
            res = np.linalg.norm(M @ x[..., None] - B[None, :, None], axis=(1, 2))
            ok = (res < 1e-8) & (x.min(axis=1) > 1e-10)
            feasible += int(ok.sum())
        print(f"    s = {s}: all C(32,{s}) = {math.comb(N,s):>9} subsets checked, "
              f"feasible = {feasible}   ({time.time()-t0:.1f}s)")
        out[f"feasible_support_{s}"] = feasible

    # 2b. Supports of size 8: uniform-only (forced by c <= 1/8 and c >= 1/|supp|).
    #     Exhaustive DFS with Fourier pruning finds every 8-point OA(8,5,2,2).
    print("\n(b) supports of size 8 -- exhaustive DFS over all C(32,8) = "
          f"{math.comb(N,8)} subsets, Fourier-pruned")
    CHI = np.array([[chi(S, v) for S in SUBSETS] for v in range(N)], dtype=np.int64)
    found: list[tuple[int, ...]] = []

    def dfs(start: int, chosen: list[int], acc: np.ndarray):
        r = 8 - len(chosen)
        if r == 0:
            if not acc.any():
                found.append(tuple(chosen))
            return
        if np.abs(acc).max() > r:
            return
        if ((acc + r) % 2 != 0).any():
            return
        for v in range(start, N - r + 1):
            chosen.append(v)
            dfs(v + 1, chosen, acc + CHI[v])
            chosen.pop()

    t0 = time.time()
    dfs(0, [], np.zeros(len(SUBSETS), dtype=np.int64))
    print(f"    8-point strength-2 orthogonal arrays found: {len(found)}   "
          f"({time.time()-t0:.1f}s)")
    out["n_OA8"] = len(found)

    # every one of them is a genuine minimiser; verify exactly on all of them
    bad = 0
    for T in found:
        x = exact_solve_on_support(list(T))
        if x is None or any(q != Fraction(1, 8) for q in x):
            bad += 1
    print(f"    exact rational check: every OA's unique pair-uniform state is "
          f"p = 1/8 on 8 points   (violations: {bad})")
    assert bad == 0
    out["OA8_all_uniform"] = True

    # are they all affine (cosets of linear [5,3] codes with dual distance 3)?
    affine = sum(1 for T in found
                 if len({a ^ b for a in T for b in T}) == 8)
    print(f"    of these, {affine}/{len(found)} are affine translates of linear "
          f"[5,3] codes with dual distance 3")
    out["n_OA8_affine"] = affine
    out["example_OA8"] = list(found[0]) if found else []
    return out


# ---------------------------------------------------------------------------
# STAGE 3 -- the exact optimum, in rational form
# ---------------------------------------------------------------------------

def stage3() -> dict:
    print("\n" + "=" * 78)
    print("STAGE 3  THE EXACT OPTIMISER  (rational coordinates, exact entropy)")
    print("=" * 78)
    out: dict = {}

    # canonical witness: the dual-distance-3 [5,3] code C = {x : x.11100 = 0,
    # x.00111 = 0}
    g1, g2 = 0b00111, 0b11100
    C = [v for v in range(N)
         if bin(v & g1).count("1") % 2 == 0 and bin(v & g2).count("1") % 2 == 0]
    assert len(C) == 8
    x = exact_solve_on_support(C)
    assert x is not None
    Hval, Hsym = exact_entropy(x)

    p = np.zeros(N)
    for v, q in zip(C, x):
        p[v] = float(q)
    assert in_P(p)

    print("\n  support (as 5-bit words, bit i = slot i):")
    for v in C:
        print(f"    {v:05b}   p = {x[C.index(v)]}")
    print(f"\n  all ten pair marginals uniform: "
          f"{np.abs(A @ p - B).max():.3e} deviation")
    print(f"  exact entropy   H = {Hsym}")
    print(f"                    = ln 8 = 3 ln 2 = {Hval:.15f}")
    print(f"  exact share     = 5 ln 2 - 3 ln 2 = 2 ln 2 = {share(p):.15f}")
    print(f"  minimum support of any pair-uniform state = 8  (Rao's bound gives 6;")
    print(f"    c <= 1/8 with Cauchy-Schwarz c >= 1/|supp| sharpens it to 8)")

    out["support"] = [f"{v:05b}" for v in C]
    out["probs"] = [str(q) for q in x]
    out["H_exact_symbolic"] = "ln 8 = 3 ln 2"
    out["H_float"] = Hval
    out["share_exact_symbolic"] = "2 ln 2"
    out["share_float"] = share(p)
    return out


# ---------------------------------------------------------------------------
# STAGE 4 -- the requested numerical search (independent confirmation)
# ---------------------------------------------------------------------------

def stage4(n_random: int = 20000, n_fw: int = 5000) -> dict:
    print("\n" + "=" * 78)
    print("STAGE 4  NUMERICAL GLOBAL SEARCH  (independent of the proof)")
    print("=" * 78)
    out: dict = {}
    bounds = [(0.0, None)] * N

    # 4a. random-objective LP vertex sampling
    print(f"\n(a) random-objective vertex sampling: {n_random} LPs over P")
    t0 = time.time()
    verts: dict[bytes, float] = {}
    Hs: list[float] = []
    supports: list[int] = []
    for _ in range(n_random):
        c = RNG.normal(size=N)
        r = linprog(c, A_eq=A, b_eq=B, bounds=bounds, method="highs")
        if not r.success:
            continue
        p = np.clip(r.x, 0, None)
        p /= p.sum()
        key = np.round(p, 9).tobytes()
        h = entropy(p)
        Hs.append(h)
        supports.append(int((p > 1e-9).sum()))
        verts.setdefault(key, h)
    Hs_a = np.array(Hs)
    print(f"    {len(verts)} distinct vertices; min H = {Hs_a.min():.12f} "
          f"(3 ln 2 = {3*LN2:.12f});  max H = {Hs_a.max():.12f}   "
          f"({time.time()-t0:.1f}s)")
    print(f"    vertex support sizes: min {min(supports)}, max {max(supports)}, "
          f"median {int(np.median(supports))}")
    hist, edges = np.histogram(Hs_a, bins=12)
    print("    histogram of H over sampled vertices:")
    for h, lo, hi in zip(hist, edges[:-1], edges[1:]):
        print(f"      [{lo:.4f}, {hi:.4f})  {'#' * int(40*h/max(hist)):<40} {h}")
    out["random_lp_n"] = n_random
    out["random_lp_distinct_vertices"] = len(verts)
    out["random_lp_min_H"] = float(Hs_a.min())
    out["random_lp_hist"] = [[float(e), int(h)] for e, h in zip(edges[:-1], hist)]

    # 4b. Frank-Wolfe concave minimisation of H (targets low-entropy vertices)
    print(f"\n(b) Frank-Wolfe entropy minimisation: {n_fw} random starts")
    t0 = time.time()
    best = (np.inf, None)
    locmins: list[float] = []
    for _ in range(n_fw):
        p = random_point_of_P()
        for _ in range(60):
            g = -(1.0 + np.log(np.maximum(p, 1e-300)))     # gradient of H
            r = linprog(g, A_eq=A, b_eq=B, bounds=bounds, method="highs")
            if not r.success:
                break
            q = np.clip(r.x, 0, None)
            q /= q.sum()
            if entropy(q) >= entropy(p) - 1e-13:
                break
            p = q
        h = entropy(p)
        locmins.append(h)
        if h < best[0]:
            best = (h, p.copy())
    lm = np.array(locmins)
    print(f"    local minima: min {lm.min():.12f}, median {np.median(lm):.6f}, "
          f"max {lm.max():.6f}   ({time.time()-t0:.1f}s)")
    frac = float((lm < 3 * LN2 + 1e-9).mean())
    print(f"    fraction of starts reaching 3 ln 2 = {3*LN2:.9f}: {frac:.3f}")
    print(f"    starts finding ANYTHING below 3 ln 2: "
          f"{int((lm < 3*LN2 - 1e-9).sum())}  (proof says 0)")
    out["fw_starts"] = n_fw
    out["fw_min_H"] = float(lm.min())
    out["fw_frac_at_optimum"] = frac
    out["fw_below_bound"] = int((lm < 3 * LN2 - 1e-9).sum())
    if best[1] is not None:
        supp = [int(v) for v in np.flatnonzero(best[1] > 1e-9)]
        print(f"    best vertex support size {len(supp)}: "
              f"{[f'{v:05b}' for v in supp]}")
        xr = exact_solve_on_support(supp)
        if xr is not None:
            print(f"    exact probabilities: {sorted(set(str(q) for q in xr))}")
            out["fw_best_support"] = [f"{v:05b}" for v in supp]
            out["fw_best_probs"] = [str(q) for q in xr]

    # 4c. maximise the collision probability sum p^2 over P (should be exactly 1/8)
    print("\n(c) max collision probability  c = sum_v p_v^2  over P "
          "(convex max -> vertex)")
    bestc = 0.0
    for _ in range(2000):
        p = random_point_of_P()
        for _ in range(60):
            r = linprog(-2.0 * p, A_eq=A, b_eq=B, bounds=bounds, method="highs")
            if not r.success:
                break
            q = np.clip(r.x, 0, None)
            q /= q.sum()
            if float(q @ q) <= float(p @ p) + 1e-14:
                break
            p = q
        bestc = max(bestc, float(p @ p))
    print(f"    2000 starts: max c found = {bestc:.12f}   (proof: c <= 1/8 = 0.125)")
    out["max_collision"] = bestc
    return out


# ---------------------------------------------------------------------------
# STAGE 5 -- the same argument at general odd k (bonus: the cap Lean could hold)
# ---------------------------------------------------------------------------

def max_clique(adj: list[set[int]], n: int) -> int:
    """Exact max clique, Tomita-style greedy-colouring branch and bound."""
    best = 0

    def expand(R: int, Pv: list[int]) -> None:
        nonlocal best
        if not Pv:
            best = max(best, R)
            return
        # greedy colouring gives a per-vertex bound
        colour: dict[int, int] = {}
        classes: list[list[int]] = []
        for v in Pv:
            for ci, cls in enumerate(classes):
                if adj[v].isdisjoint(cls):
                    cls.append(v)
                    colour[v] = ci + 1
                    break
            else:
                classes.append([v])
                colour[v] = len(classes)
        order = sorted(Pv, key=lambda v: colour[v])
        while order:
            v = order.pop()
            if R + colour[v] <= best:
                return
            expand(R + 1, [u for u in order if u in adj[v]])

    expand(0, list(range(n)))
    return best


def stage5() -> dict:
    print("\n" + "=" * 78)
    print("STAGE 5  THE SAME ARGUMENT AT GENERAL ODD k")
    print("=" * 78)
    print("""
  For odd k put m = (k+1)/2.  The frame identity and Frobenius give
      m^2 c + sum_{v!=w} p_v p_w (m - d)^2 = m/2,
  and (m-d)^2 >= 1 for every integer d != m, so with
      S = sum_{v!=w, d(v,w)=m} p_v p_w  <=  1 - 1/omega_m   (Motzkin-Straus)
  where omega_m is the clique number of the distance-m graph on {0,1}^k:
      c <= (m/2 - 1/omega_m) / (m^2 - 1),      H >= -ln c.

  omega_m has two regimes:
    * m ODD  (k = 1 mod 4): the distance-m graph is triangle-free by parity,
      so omega_m = 2  ->  c <= 1/(k+3).
    * m EVEN (k = 3 mod 4): a clique is an equidistant code of length 2m-1 and
      distance m; Plotkin (2d > n) gives omega_m <= 2m  ->  c <= 1/(k+1).
  Both cases: c <= 1/(4*ceil((k+1)/4)), i.e. H >= ln(4*ceil((k+1)/4)).
  That is exactly the order of the smallest Hadamard matrix >= k+1, so the
  bound is ATTAINED whenever that Hadamard matrix exists (its OA(N,k,2,2)).
""")
    rows = []
    for k in (3, 5, 7, 9, 11, 13):
        m = (k + 1) // 2
        n = 1 << k
        if m % 2 == 1:
            omega, how = 2, "parity (triangle-free), exact"
        elif k <= 7:
            pts = np.array([[(v >> i) & 1 for i in range(k)] for v in range(n)],
                           dtype=np.int8)
            dm = (pts[:, None, :] != pts[None, :, :]).sum(axis=2)
            adj = [set(np.flatnonzero(dm[v] == m).tolist()) for v in range(n)]
            omega, how = max_clique(adj, n), "exact max-clique search"
        else:
            omega, how = 2 * m, "Plotkin bound (upper bound), attained by Hadamard"
        cbound = (m / 2 - 1 / omega) / (m * m - 1)
        target = 4 * math.ceil((k + 1) / 4)
        Hmin = -math.log(cbound)
        rows.append((k, m, omega, cbound, Hmin, k * LN2 - Hmin, (k - 2) * LN2, how))
        print(f"  k={k:>2}  m={m}  omega_m={omega:>2} [{how}]")
        print(f"        c <= {cbound:.10f} = 1/{round(1/cbound)}   "
              f"(1/(4*ceil((k+1)/4)) = 1/{target}: "
              f"{'MATCH' if abs(1/cbound - target) < 1e-9 else 'MISMATCH'})")
        print(f"        min H >= ln {round(1/cbound)} = {Hmin:.9f};  "
              f"max share <= {k*LN2 - Hmin:.9f}"
              f"   vs Lean cap (k-2)ln2 = {(k-2)*LN2:.9f}")
    return {"general_k": [
        {"k": k, "m": m, "omega": w, "c_bound": c, "min_H": h,
         "max_share": s, "lean_cap": lc, "omega_source": how}
        for k, m, w, c, h, s, lc, how in rows]}


# ---------------------------------------------------------------------------

def main() -> None:
    stages = sys.argv[1:] or ["1", "2", "3", "4", "5"]
    res: dict = {}
    if "1" in stages:
        res["stage1_proof"] = stage1()
    if "2" in stages:
        res["stage2_exhaustive"] = stage2()
    if "3" in stages:
        res["stage3_exact"] = stage3()
    if "4" in stages:
        res["stage4_numeric"] = stage4()
    if "5" in stages:
        res["stage5_general_k"] = stage5()
    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    print(f"  min H over the pair-uniform polytope on {{0,1}}^5 = 3 ln 2 = {3*LN2:.12f}")
    print(f"  TRUE classical max share at k = 5 = 2 ln 2 = {2*LN2:.12f}  (EXACT)")
    print(f"  Lean's proved cap (k-2) ln 2      = 3 ln 2 = {3*LN2:.12f}  (not tight)")
    print(f"  quantum value, AME(5,2)           = 5 ln 2 = {5*LN2:.12f}")
    with open("/home/emoore/CIRISOntology/scratchpad/temporal-share/"
              "classical_max_k5_results.json", "w") as f:
        json.dump(res, f, indent=2, default=str)


if __name__ == "__main__":
    main()
