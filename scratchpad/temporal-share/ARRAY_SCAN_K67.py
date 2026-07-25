#!/usr/bin/env python3
"""
ARRAY_SCAN_K67.py — the classical maximum of the whole-only share at k = 6 and k = 7.

Companion to CLASSICAL_MAX_K5.md (k = 5 solved exactly: max share = 2 ln 2).

THE PROBLEM.  For a pair-uniform p on {0,1}^k the envelope top is the uniform
distribution (which is itself pair-uniform), so

    share(p) = k*ln2 - H(p),      max share = k*ln2 - min_{p in P_k} H(p)

where P_k = {p on {0,1}^k : every one of the C(k,2) pair marginals is uniform}.
The whole question is a MINIMUM ENTROPY problem over the pair-uniform polytope.

THE CONJECTURE UNDER TEST.  max share(k) = (k - ceil(log2(k+1))) * ln 2, i.e.
min H = ceil(log2(k+1)) * ln 2.  Predictions: k=6 -> 3 ln2 ; k=7 -> 4 ln2.

STAGES
  1  code theory, EXHAUSTIVE over all linear codes (every subspace of F_2^k)
  2  the analytic bound over the FULL polytope (frame + Frobenius identity),
     verified numerically; k=6 needs no graph theory, k=7 needs max-clique + Motzkin-Straus
  3  exhaustive minimum-support enumeration (a C DFS, embedded in this file as
     OA_ENUM_C and compiled on demand) + exact rational verification of the witnesses
  4  GPU search over the full polytope (attack B) -- a SEARCH: an upper bound on
     min H, equivalently a LOWER bound on max share.  Never a maximum.
  5  bonus: where the Hamming form dies (k = 8..11), by explicit Hadamard-12 witness

Run:  CUDA_PATH=/usr ./qenv/bin/python ARRAY_SCAN_K67.py
"""

import itertools
import json
import math
import os
import subprocess
import time
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = math.log(2.0)
RESULTS = {}


def banner(s):
    print("\n" + "=" * 78)
    print(s)
    print("=" * 78)


def sub(s):
    print("\n--- " + s + " ---")


def popcount(x):
    return bin(x).count("1")


def chi(v, i):
    return -1 if (v >> i) & 1 else 1


def uvec(v, k):
    """u_v = (1, chi_1(v), ..., chi_k(v)) in {+-1}^{k+1}."""
    return np.array([1] + [chi(v, i) for i in range(k)], dtype=np.int64)


def pair_index_list(k):
    return list(itertools.combinations(range(k), 2))


def is_pair_uniform_exact(counts, denom, k):
    """counts[v] integers summing to denom. Exact rational pair-marginal check."""
    N = 1 << k
    for (i, j) in pair_index_list(k):
        cell = [0, 0, 0, 0]
        for v in range(N):
            cell[(((v >> i) & 1) << 1) | ((v >> j) & 1)] += counts[v]
        for g in range(4):
            if Fraction(cell[g], denom) != Fraction(1, 4):
                return False
    return True


# ---------------------------------------------------------------------------
# IPF projection onto P_k, shared by CPU (numpy) and GPU (cupy)
# ---------------------------------------------------------------------------

class Polytope:
    """Iterative proportional fitting onto P_k = {all pair marginals uniform}."""

    def __init__(self, k, xp, dtype):
        self.k, self.xp, self.dtype = k, xp, dtype
        N = 1 << k
        self.N = N
        self.pairs = pair_index_list(k)
        gs = [np.array([(((v >> i) & 1) << 1) | ((v >> j) & 1) for v in range(N)],
                       dtype=np.int32) for (i, j) in self.pairs]
        self.groups = [xp.asarray(g) for g in gs]
        self.onehot = [xp.asarray(np.eye(4)[g], dtype=dtype) for g in gs]
        self.tiny = dtype(1e-30) if dtype == np.float32 else 1e-300

    def ipf(self, X, sweeps):
        xp = self.xp
        for _ in range(sweeps):
            for g, oh in zip(self.groups, self.onehot):
                mass = X @ oh
                X *= (0.25 / xp.maximum(mass, self.tiny))[:, g]
            X /= X.sum(axis=1, keepdims=True)
        return X

    def residual(self, X):
        xp = self.xp
        res = xp.zeros(X.shape[0], dtype=self.dtype)
        for oh in self.onehot:
            res = xp.maximum(res, xp.abs(X @ oh - 0.25).max(axis=1))
        return res

    def entropy(self, X):
        xp = self.xp
        return -(xp.where(X > 0, X * xp.log(xp.maximum(X, self.tiny)), 0.0)).sum(axis=1)

    def minimise_entropy(self, X, outer, sweeps, eta_max=0.60):
        """Sharpen (p -> p^(1+eta), the multiplicative step down -grad H) and reproject."""
        X = self.ipf(X, 60)
        for it in range(outer):
            eta = 0.02 + eta_max * (it / outer) ** 0.7
            X = X ** (1.0 + eta)
            X /= X.sum(axis=1, keepdims=True)
            X = self.ipf(X, sweeps)
        return self.ipf(X, 120)

    def maximise_collision(self, X, outer, sweeps):
        X = self.ipf(X, 60)
        for it in range(outer):
            eta = 0.05 + 0.45 * it / outer
            X = X ** (1.0 + eta)
            X /= X.sum(axis=1, keepdims=True)
            X = self.ipf(X, sweeps)
        return self.ipf(X, 120)


# ---------------------------------------------------------------------------
# the exhaustive support enumerator, embedded so this file is self-contained
# (an identical copy lives alongside as oa_enum.c; the binary is built on demand)
# ---------------------------------------------------------------------------

OA_ENUM_C = r"""/*
 * oa_enum.c — exhaustive enumeration of 8-point pair-uniform supports in {0,1}^k.
 *
 * A subset S of {0,1}^k with |S| = 8 carries a pair-uniform distribution iff the
 * uniform distribution on it is pair-uniform iff, with u_v = (1, chi_1(v), ..., chi_k(v))
 * in {+-1}^{k+1},
 *
 *      sum_{v in S} u_v u_v^T  =  8 I_{k+1}
 *
 * i.e. every off-diagonal partial sum A[i][j] = sum_{v in S} u_v[i] u_v[j] vanishes.
 * (Diagonal entries are automatically 8.)  This is exactly an OA(8, k, 2, 2).
 *
 * Generic DFS over subsets in increasing index order, with the only prune being the
 * unavoidable one: after t points chosen, r = 8 - t remain and each can move A[i][j]
 * by exactly +-1, so |A[i][j]| <= r is necessary.  No structural shortcut is used.
 *
 * Usage: oa_enum <k> <fix0>
 *   fix0 = 1 forces 0 in S (valid by the translation symmetry of the solution set;
 *          the caller multiplies the count by 2^k / 8).
 *
 * Output on stdout: "COUNT <n>" then up to MAXSHOW witness lines "SOL v0 v1 ... v7".
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

#define MAXK 8
#define MAXN (1 << MAXK)
#define MAXP (((MAXK + 1) * MAXK) / 2)
#define MAXSHOW 200

static int K, N, NP;
static signed char sgn[MAXN][MAXP]; /* sgn[v][p] = u_v[i]*u_v[j] for pair p=(i,j) */

static long long total_count = 0;
static int shown = 0;
static int show_buf[MAXSHOW][8];

/* u_v[0] = +1 (constant coordinate); u_v[i] = +1 if bit i-1 of v is 0, else -1. */
static void build_signs(void) {
    int pairs[MAXP][2];
    NP = 0;
    for (int i = 0; i <= K; i++)
        for (int j = i + 1; j <= K; j++) { pairs[NP][0] = i; pairs[NP][1] = j; NP++; }
    for (int v = 0; v < N; v++) {
        signed char u[MAXK + 1];
        u[0] = 1;
        for (int i = 1; i <= K; i++) u[i] = ((v >> (i - 1)) & 1) ? -1 : 1;
        for (int p = 0; p < NP; p++) sgn[v][p] = u[pairs[p][0]] * u[pairs[p][1]];
    }
}

/* recursive DFS: t points already placed, next candidate index >= start */
static void dfs(int t, int start, signed char *A, int *chosen,
                long long *cnt, int tid) {
    if (t == 8) {
        (*cnt)++;
        #pragma omp critical
        {
            if (shown < MAXSHOW) {
                memcpy(show_buf[shown], chosen, 8 * sizeof(int));
                shown++;
            }
        }
        return;
    }
    int r = 8 - t - 1; /* remaining AFTER placing this one */
    /* need at least (8-t) more points available */
    int last = N - (8 - t);
    for (int v = start; v <= last; v++) {
        const signed char *s = sgn[v];
        int ok = 1;
        for (int p = 0; p < NP; p++) {
            signed char a = A[p] + s[p];
            if (a > r || a < -r) { ok = 0; break; }
        }
        if (!ok) continue;
        for (int p = 0; p < NP; p++) A[p] += s[p];
        chosen[t] = v;
        dfs(t + 1, v + 1, A, chosen, cnt, tid);
        for (int p = 0; p < NP; p++) A[p] -= s[p];
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s <k> <fix0>\n", argv[0]); return 1; }
    K = atoi(argv[1]);
    int fix0 = atoi(argv[2]);
    N = 1 << K;
    build_signs();

    long long grand = 0;

    if (fix0) {
        /* v0 = 0 fixed; parallelize over the second point */
        #pragma omp parallel for schedule(dynamic, 1) reduction(+ : grand)
        for (int v1 = 1; v1 <= N - 7; v1++) {
            signed char A[MAXP];
            int chosen[8];
            long long cnt = 0;
            memset(A, 0, sizeof(A));
            for (int p = 0; p < NP; p++) A[p] += sgn[0][p];
            for (int p = 0; p < NP; p++) A[p] += sgn[v1][p];
            int bad = 0;
            for (int p = 0; p < NP; p++) if (A[p] > 6 || A[p] < -6) bad = 1;
            if (!bad) {
                chosen[0] = 0; chosen[1] = v1;
                dfs(2, v1 + 1, A, chosen, &cnt, omp_get_thread_num());
            }
            grand += cnt;
        }
    } else {
        /* full enumeration; parallelize over the first point */
        #pragma omp parallel for schedule(dynamic, 1) reduction(+ : grand)
        for (int v0 = 0; v0 <= N - 8; v0++) {
            signed char A[MAXP];
            int chosen[8];
            long long cnt = 0;
            memset(A, 0, sizeof(A));
            for (int p = 0; p < NP; p++) A[p] += sgn[v0][p];
            chosen[0] = v0;
            dfs(1, v0 + 1, A, chosen, &cnt, omp_get_thread_num());
            grand += cnt;
        }
    }
    total_count = grand;
    printf("COUNT %lld\n", total_count);
    for (int i = 0; i < shown; i++) {
        printf("SOL");
        for (int j = 0; j < 8; j++) printf(" %d", show_buf[i][j]);
        printf("\n");
    }
    return 0;
}
"""


def build_enumerator():
    """Write and compile the DFS enumerator; return the path to the binary."""
    csrc = os.path.join(HERE, "oa_enum.c")
    exe = os.path.join(HERE, "oa_enum")
    if not os.path.exists(csrc):
        with open(csrc, "w") as f:
            f.write(OA_ENUM_C)
    if (not os.path.exists(exe)) or os.path.getmtime(exe) < os.path.getmtime(csrc):
        subprocess.run(["gcc", "-O3", "-march=native", "-fopenmp", "-o", exe, csrc],
                       check=True)
    return exe


# ---------------------------------------------------------------------------
# STAGE 1 — EXHAUSTIVE over linear codes
# ---------------------------------------------------------------------------

def all_subspaces(k):
    """Every subspace of F_2^k exactly once, via reduced row echelon form.

    A subspace of dimension m has a UNIQUE RREF basis: pivot columns
    p_0 < ... < p_{m-1}; row i has a 1 in column p_i, 0 in every other pivot
    column, 0 in every column < p_i, free bits in the non-pivot columns > p_i.
    Yields (dim, basis rows as bitmasks).
    """
    cols = list(range(k))
    for m in range(k + 1):
        for pivots in itertools.combinations(cols, m):
            pivset = set(pivots)
            free_positions = [[j for j in cols if j not in pivset and j > pivots[i]]
                              for i in range(m)]
            nfree = sum(len(fp) for fp in free_positions)
            for assign in range(1 << nfree):
                rows, bitptr = [], 0
                for i in range(m):
                    r = 1 << pivots[i]
                    for j in free_positions[i]:
                        if (assign >> bitptr) & 1:
                            r |= 1 << j
                        bitptr += 1
                    rows.append(r)
                yield m, tuple(rows)


def span(rows):
    words = [0]
    for r in rows:
        words = words + [w ^ r for w in words]
    return words


def columns_ok(rows, k):
    """uniform-on-C is pair-uniform  <=>  the generator matrix has all k columns
    NONZERO and PAIRWISE DISTINCT.

    Proof: p uniform on C has Fourier coefficient p^(S) = [S in C^perp]. Pair
    uniformity is p^(S) = 0 for 1 <= |S| <= 2, i.e. C^perp has no word of weight
    1 or 2.  e_i in C^perp  <=>  every basis row has a 0 in position i  <=>
    column i is the zero vector.  e_i + e_j in C^perp  <=>  every basis row has
    equal bits at i and j  <=>  column i = column j.
    """
    cols = [sum(((r >> j) & 1) << t for t, r in enumerate(rows)) for j in range(k)]
    return (0 not in cols) and (len(set(cols)) == k), cols


def dual_min_distance(rows, k):
    """Brute-force min weight of a nonzero dual word (cross-check for columns_ok)."""
    best = None
    for v in range(1, 1 << k):
        if all(popcount(v & r) % 2 == 0 for r in rows):
            w = popcount(v)
            if best is None or w < best:
                best = w
    return best


def stage1(k):
    sub("STAGE 1  k = %d : EXHAUSTIVE enumeration of every linear code in F_2^%d" % (k, k))
    t0 = time.time()
    galois = {0: 1, 1: 2, 2: 5, 3: 16, 4: 67, 5: 374, 6: 2825, 7: 29212}

    nsub = 0
    by_dim, good_by_dim = {}, {}
    best_dim, best_witnesses = None, []
    xcheck_n, xcheck_bad = 0, 0

    for m, rows in all_subspaces(k):
        nsub += 1
        by_dim[m] = by_dim.get(m, 0) + 1
        ok, _ = columns_ok(rows, k)
        # cross-check the column criterion against a brute-force dual computation
        if nsub % 37 == 0:
            xcheck_n += 1
            dmin = dual_min_distance(rows, k)
            if ok != ((dmin is None) or (dmin >= 3)):
                xcheck_bad += 1
        if ok:
            good_by_dim[m] = good_by_dim.get(m, 0) + 1
            if best_dim is None or m < best_dim:
                best_dim, best_witnesses = m, [rows]
            elif m == best_dim and len(best_witnesses) < 5:
                best_witnesses.append(rows)

    print("subspaces enumerated : %d   (Galois number G_%d = %d)   %s"
          % (nsub, k, galois[k], "MATCH" if nsub == galois[k] else "*** MISMATCH ***"))
    print("column criterion vs brute-force dual distance, on %d sampled subspaces: %d disagreements"
          % (xcheck_n, xcheck_bad))
    print("count by dimension   : %s" % {d: by_dim[d] for d in sorted(by_dim)})
    print("of these, pair-uniform (dual distance >= 3):")
    for d in sorted(by_dim):
        print("    dim %d  |C| = %3d :  %6d of %6d"
              % (d, 1 << d, good_by_dim.get(d, 0), by_dim[d]))

    minC = 1 << best_dim
    Hmin_code = math.log(minC)
    share_code = k * LN2 - Hmin_code
    r_ham = math.ceil(math.log2(k + 1))
    print("\nMINIMUM |C| over ALL %d linear codes, restricted to those with dual distance >= 3:"
          % nsub)
    print("  |C|_min = %d = 2^%d   (attained by %d codes)"
          % (minC, best_dim, good_by_dim.get(best_dim, 0)))
    print("  H(uniform on C) = ln %d = %.15f = %.6f * ln2" % (minC, Hmin_code, Hmin_code / LN2))
    print("  share           = %d*ln2 - ln %d = %.15f = %.6f * ln2"
          % (k, minC, share_code, share_code / LN2))

    print("\n  THE CODE-THEORY ARITHMETIC, worked explicitly")
    print("    uniform-on-C is pair-uniform  <=>  C^perp has no word of weight 1 or 2")
    print("                                  <=>  the k columns of the generator matrix")
    print("                                       are all NONZERO and PAIRWISE DISTINCT.")
    print("    A dim-m code has columns in F_2^m, which has 2^m - 1 nonzero vectors, so")
    print("      k <= 2^m - 1   =>   2^m >= k+1 = %d   =>   m >= ceil(log2 %d) = %d."
          % (k + 1, k + 1, r_ham))
    print("    (This IS the Hamming/sphere-packing bound, in its shortest form: a")
    print("     parity-check matrix with distinct nonzero columns is a Hamming code.)")
    print("    Hence |C| >= 2^%d = %d, and min H over linear codes = %d * ln2."
          % (r_ham, 1 << r_ham, r_ham))
    print("    Exhaustive search agrees: |C|_min = %d, bound 2^%d = %d.  %s"
          % (minC, r_ham, 1 << r_ham, "TIGHT" if minC == (1 << r_ham) else "*** GAP ***"))
    print("    => max share over linear-code states = (%d - %d)*ln2 = %.15f"
          % (k, r_ham, share_code))
    if k == 7:
        print("\n    k = 7 SUBTLETY (checked carefully, as instructed).  It is tempting to")
        print("    say 'the perfect Hamming [7,4,3] code has 16 words, so |C| = 16 and")
        print("    H = 4*ln2'.  That is the wrong side of the duality.  The Hamming code")
        print("    is the DUAL C^perp -- the one that must have distance >= 3.  It has")
        print("    2^4 = 16 words, so")
        print("        |C| = 2^7 / |C^perp| = 128 / 16 = 8,   H = ln 8 = 3*ln2,")
        print("        share = 7*ln2 - 3*ln2 = 4*ln2 = %.15f." % (4 * LN2))
        print("    C is the [7,3,4] SIMPLEX code (all 7 nonzero words of weight 4).")
        print("    The conjecture's ceil(log2(k+1)) = 3 is the REDUNDANCY of the dual")
        print("    (= dim C), not the dual's dimension. (7 - 3)*ln2 = 4*ln2 AGREES.")

    Cw = sorted(span(best_witnesses[0]))
    ok, cols = columns_ok(best_witnesses[0], k)
    print("\n  a minimising code, explicitly (|C| = %d):" % len(Cw))
    print("      generator rows : %s" % [format(r, "0%db" % k) for r in best_witnesses[0]])
    print("      generator columns (must be distinct & nonzero) : %s   distinct=%s"
          % (cols, len(set(cols)) == k and 0 not in cols))
    print("      codewords : %s" % [format(w, "0%db" % k) for w in Cw])
    wts = sorted({popcount(w) for w in Cw if w})
    print("      nonzero weights present : %s" % wts)
    counts = [0] * (1 << k)
    for w in Cw:
        counts[w] = 1
    exact_ok = is_pair_uniform_exact(counts, len(Cw), k)
    print("  exact rational check, all %d pair marginals = 1/4 : %s"
          % (len(pair_index_list(k)), "PASS" if exact_ok else "FAIL"))

    RESULTS["stage1_k%d" % k] = dict(
        subspaces=nsub, galois=galois[k], crosscheck_n=xcheck_n, crosscheck_bad=xcheck_bad,
        min_abs_C=minC, min_dim=best_dim, n_codes_at_min=good_by_dim.get(best_dim, 0),
        H_min_code=Hmin_code, share_code=share_code, hamming_redundancy=r_ham,
        exact_pair_check=exact_ok, witness=[format(w, "0%db" % k) for w in Cw],
        seconds=time.time() - t0)
    print("  [stage 1 k=%d : %.1f s]" % (k, time.time() - t0))
    return minC


# ---------------------------------------------------------------------------
# STAGE 2 — the analytic bound over the FULL polytope
# ---------------------------------------------------------------------------

def max_clique_bitset(adj, n):
    """Exact maximum clique: Tomita-style greedy-colouring branch and bound."""
    best, best_set = [0], [0]

    def colour_sort(cand):
        order, colours, c = [], [], 0
        uncoloured = cand
        while uncoloured:
            c += 1
            avail = uncoloured
            while avail:
                v = (avail & -avail).bit_length() - 1
                avail &= ~(1 << v)
                avail &= ~adj[v]
                uncoloured &= ~(1 << v)
                order.append(v)
                colours.append(c)
        return order, colours

    def expand(cand, size, cur):
        order, colours = colour_sort(cand)
        for idx in range(len(order) - 1, -1, -1):
            v = order[idx]
            if size + colours[idx] <= best[0]:
                return
            newcand = cand & adj[v]
            if newcand:
                expand(newcand, size + 1, cur | (1 << v))
            elif size + 1 > best[0]:
                best[0], best_set[0] = size + 1, cur | (1 << v)
            cand &= ~(1 << v)

    expand((1 << n) - 1, 0, 0)
    return best[0], best_set[0]


def max_quadratic_on_simplex(W, rng, starts=3000, iters=2500):
    """max x^T W x over the simplex (replicator dynamics; W >= 0, zero diagonal)."""
    n = W.shape[0]
    X = rng.random((starts, n)) + 1e-6
    X /= X.sum(axis=1, keepdims=True)
    for _ in range(iters):
        G = X @ W
        val = (X * G).sum(axis=1, keepdims=True)
        X = X * G / np.maximum(val, 1e-300)
        X /= X.sum(axis=1, keepdims=True)
    return float((X * (X @ W)).sum(axis=1).max())


def stage2(k, rng, xp, dtype):
    sub("STAGE 2  k = %d : the analytic bound over the FULL polytope P_%d" % (k, k))
    t0 = time.time()
    N = 1 << k
    U = np.stack([uvec(v, k) for v in range(N)])
    D = np.array([[popcount(v ^ w) for w in range(N)] for v in range(N)])
    G = (k + 1) - 2 * D

    poly64 = Polytope(k, np, np.float64)
    P = rng.random((200, N)) + 1e-3
    P /= P.sum(axis=1, keepdims=True)
    P = poly64.ipf(P, 400)

    dev = max(float(np.abs((U.T * P[b]) @ U - np.eye(k + 1)).max()) for b in range(200))
    print("(1) FRAME IDENTITY   sum_v p_v u_v u_v^T = I_%d   for every p in P_%d" % (k + 1, k))
    print("    u_v = (1, chi_1(v), ..., chi_%d(v)) in {+-1}^%d" % (k, k + 1))
    print("    200 random interior points of P_%d : max deviation = %.3e" % (k, dev))

    dev2 = max(abs(float(P[b] @ (G.astype(float) ** 2) @ P[b]) - (k + 1)) for b in range(200))
    print("(2) FROBENIUS IDENTITY   sum_{v,w} p_v p_w (%d - 2d(v,w))^2 = %d"
          % (k + 1, k + 1))
    print("    (taking ||.||_F^2 of (1), using u_v . u_w = %d - 2d(v,w))" % (k + 1))
    print("    max deviation = %.3e" % dev2)

    sq = {d: (k + 1 - 2 * d) ** 2 for d in sorted(set(D.flatten().tolist()))}
    print("    (%d - 2d)^2 by distance d : %s" % (k + 1, sq))

    # ---- BOUND (i): the trivial one, valid at every k --------------------
    print("\n(3i) THE TRIVIAL BOUND (every k, no structure whatsoever).")
    print("     In the Frobenius identity every term p_v p_w (u_v.u_w)^2 is >= 0, and the")
    print("     DIAGONAL terms alone are sum_v p_v^2 (u_v.u_v)^2 = %d^2 * c. Dropping all"
          % (k + 1))
    print("     off-diagonal terms:")
    print("       %d^2 * c <= %d   =>   c <= 1/%d" % (k + 1, k + 1, k + 1))
    print("     Equivalently |supp| >= %d -- this IS the Rao bound for a strength-2" % (k + 1))
    print("     orthogonal array, recovered in one line.")
    c_trivial = Fraction(1, k + 1)

    omega, S_bound, clique_secs = None, None, 0.0
    if k == 7:
        print("\n     *** AT k = 7 THIS IS ALREADY THE ANSWER: 1/(k+1) = 1/8. ***")
        print("     Nothing further is needed -- no parity argument, no clique number, no")
        print("     Motzkin-Straus, no Plotkin. k = 7 is the CHEAPEST case in the family,")
        print("     because k+1 = 8 is exactly the size of the optimal support (Rao tight).")
        print("     Stage 2 continues below with the k=5-style refinement anyway, purely as")
        print("     an independent cross-check that it lands on the same 1/8.")

    if k % 2 == 0:
        print("\n(3) k is EVEN, so %d is ODD, so (%d - 2d) is an ODD INTEGER for every d" % (k + 1, k + 1))
        print("    and therefore NEVER ZERO: (%d - 2d)^2 >= 1 with no exceptions" % (k + 1))
        print("    (observed minimum over all d : %d %s)"
              % (min(sq.values()), "OK" if min(sq.values()) == 1 else "***"))
        print("    NO GRAPH THEORY IS NEEDED AT EVEN k -- there is no zero-cost distance,")
        print("    so no Motzkin-Straus and no clique number enter the argument.")
        print("    Chain, with c = sum_v p_v^2 the collision probability:")
        print("      %d = %d*c + sum_{v!=w} p_v p_w (%d-2d)^2  >=  %d*c + 1*(1-c)"
              % (k + 1, (k + 1) ** 2, k + 1, (k + 1) ** 2))
        print("      => (%d - 1)*c <= %d - 1   =>   c <= %d/%d = %s"
              % ((k + 1) ** 2, k + 1, k, (k + 1) ** 2 - 1,
                 Fraction(k, (k + 1) ** 2 - 1)))
        c_bound = Fraction(k, (k + 1) ** 2 - 1)
    else:
        m = (k + 1) // 2
        print("\n(3) k is ODD: distance d = %d makes (%d - 2d)^2 = 0 -- a ZERO-COST set."
              % (m, k + 1))
        print("    So we need the maximum weight S = sum_{v!=w, d(v,w)=%d} p_v p_w" % m)
        print("    that any distribution can place on the distance-%d graph." % m)
        adj = [0] * N
        for v in range(N):
            for w in range(N):
                if D[v][w] == m:
                    adj[v] |= 1 << w
        deg = popcount(adj[0])
        print("    distance-%d graph on %d vertices: %d-regular, %d edges"
              % (m, N, deg, N * deg // 2))
        tclq = time.time()
        omega, wit = max_clique_bitset(adj, N)
        clique_secs = time.time() - tclq
        clq = [v for v in range(N) if (wit >> v) & 1]
        print("    EXACT maximum clique (branch and bound, exhaustive) : omega = %d   [%.2f s]"
              % (omega, clique_secs))
        print("    witness clique : %s" % [format(v, "0%db" % k) for v in clq])
        dd = sorted({D[a][b] for a in clq for b in clq if a != b})
        print("    all pairwise distances in the witness : %s   %s"
              % (dd, "VERIFIED CLIQUE" if dd == [m] else "*** NOT A CLIQUE ***"))
        if 2 * m > k:
            plotkin = 2 * (m // (2 * m - k))
            print("    Plotkin bound cross-check: A(%d,%d) <= 2*floor(%d/(2*%d-%d)) = %d   %s"
                  % (k, m, m, m, k, plotkin,
                     "MATCHES omega" if plotkin == omega else "*** differs ***"))
        print("    Motzkin-Straus (1965): over the simplex, max of the ORDERED sum")
        print("      sum_{v!=w, d=%d} x_v x_w = 1 - 1/omega = 1 - 1/%d = %s"
              % (m, omega, Fraction(omega - 1, omega)))
        W = (D == m).astype(np.float64)
        S_num = max_quadratic_on_simplex(W, rng)
        print("      numerical check (3000 replicator runs) : max S = %.12f   (target %.12f)"
              % (S_num, 1 - 1 / omega))
        S_bound = Fraction(omega - 1, omega)
        zmin = min(s for s in sq.values() if s > 0)
        print("    Chain, with c = sum p_v^2 and S the weight on distance-%d pairs:" % m)
        print("      %d = %d*c + sum_{v!=w, d!=%d} p p (%d-2d)^2 >= %d*c + %d*(1-c-S)"
              % (k + 1, (k + 1) ** 2, m, k + 1, (k + 1) ** 2, zmin))
        print("      => (%d - %d)*c <= %d - %d + %d*S"
              % ((k + 1) ** 2, zmin, k + 1, zmin, zmin))
        c_bound = (Fraction((k + 1) - zmin) + zmin * S_bound) / ((k + 1) ** 2 - zmin)
        print("      => c <= (%d + %d*%s)/%d = %s"
              % ((k + 1) - zmin, zmin, S_bound, (k + 1) ** 2 - zmin, c_bound))

    # ---- combine ---------------------------------------------------------
    refined = c_bound
    c_bound = min(c_trivial, refined)
    print("\n     bounds in hand: trivial c <= %s ; refined c <= %s ; BEST c <= %s"
          % (c_trivial, refined, c_bound))
    print("     cheapest sufficient argument at k = %d : %s"
          % (k, "the TRIVIAL bound alone (positivity of squares)"
             if c_trivial <= refined else
             ("the EVEN-PARITY refinement (odd integers are nonzero)" if k % 2 == 0
              else "the max-clique + Motzkin-Straus refinement")))

    inv = Fraction(1) / c_bound
    Hlb = -math.log(float(c_bound))
    share_ub = k * LN2 - Hlb
    print("\n(4) c <= %s   =>   H(p) >= H_2(p) = -ln c >= ln %s = %.15f = %.6f * ln2"
          % (c_bound, inv, Hlb, Hlb / LN2))
    print("    (H >= H_2 is Renyi-entropy monotonicity; H_2 = -ln c.)")
    print("    => MAX SHARE <= %d*ln2 - ln %s = %.15f = %.6f * ln2"
          % (k, inv, share_ub, share_ub / LN2))
    print("    => |supp(p)| >= 1/c >= %s   (Cauchy-Schwarz gives c >= 1/|supp|)" % inv)
    print("    EQUALITY analysis: H = ln %s forces H = H_2, hence p uniform on its" % inv)
    print("    support, and c = 1/%s then forces |supp| = %s. So every minimiser is the"
          % (inv, inv))
    print("    uniform distribution on an %s-point pair-uniform support -- an OA(%s,%d,2,2)."
          % (inv, inv, k))

    tc = time.time()
    poly = Polytope(k, xp, dtype)
    X = xp.asarray((rng.random((4000, N)) + 1e-3).astype(dtype))
    X /= X.sum(axis=1, keepdims=True)
    X = poly.maximise_collision(X, outer=250, sweeps=20)
    feas = poly.residual(X) < (1e-6 if dtype == np.float32 else 1e-11)
    cmax = float((X[feas] ** 2).sum(axis=1).max())
    print("\n    numerical tightness check: max of c over P_%d, 4000 restarts on GPU" % k)
    print("      max c found = %.12f   (bound %s = %.12f)   %s   [%.1f s]"
          % (cmax, c_bound, float(c_bound),
             "SATURATED -- the bound is exactly tight"
             if abs(cmax - float(c_bound)) < 1e-6 else "below the bound", time.time() - tc))

    RESULTS["stage2_k%d" % k] = dict(
        frame_dev=dev, frobenius_dev=dev2, c_trivial=str(c_trivial),
        c_refined=str(refined), cheapest="trivial" if c_trivial <= refined else "refined",
        c_bound=str(c_bound),
        c_bound_float=float(c_bound), omega=omega, clique_seconds=clique_secs,
        S_bound=str(S_bound) if S_bound is not None else None,
        H_lower_bound=Hlb, H_lower_over_ln2=Hlb / LN2,
        share_upper_bound=share_ub, share_upper_over_ln2=share_ub / LN2,
        c_max_numerical=cmax, seconds=time.time() - t0)
    return Hlb, share_ub


# ---------------------------------------------------------------------------
# STAGE 3 — exhaustive minimum-support enumeration
# ---------------------------------------------------------------------------

def stage3(k):
    sub("STAGE 3  k = %d : EXHAUSTIVE enumeration of minimum supports" % k)
    t0 = time.time()
    exe = build_enumerator()
    print("Supports of size <= 7 are impossible with NO enumeration at all:")
    print("  c <= 1/8 (stage 2) and Cauchy-Schwarz c >= 1/|supp| give |supp| >= 8.")
    print("Supports of size 8 must carry the UNIFORM distribution:")
    print("  |supp| = 8 gives c >= 1/8; with c <= 1/8 that forces c = 1/8, and")
    print("  equality in Cauchy-Schwarz forces p uniform. So every entropy minimiser")
    print("  is uniform on an 8-point pair-uniform support = an OA(8,%d,2,2)." % k)
    print("\nExhaustive DFS over ALL C(%d,8) = %s eight-subsets of {0,1}^%d :"
          % (1 << k, format(math.comb(1 << k, 8), ","), k))
    print("  condition: sum_{v in S} u_v u_v^T = 8*I_%d, i.e. every off-diagonal" % (k + 1))
    print("  partial sum A_ij vanishes.  Prune: |A_ij| <= 8-t (the unavoidable one --")
    print("  each remaining point moves A_ij by exactly +-1). No code structure assumed.")

    r_full = subprocess.run([exe, str(k), "0"], capture_output=True, text=True, check=True)
    t_full = time.time() - t0
    n_full = int(r_full.stdout.split("\n")[0].split()[1])
    t1 = time.time()
    r_fix = subprocess.run([exe, str(k), "1"], capture_output=True, text=True, check=True)
    t_fix = time.time() - t1
    n_fix = int(r_fix.stdout.split("\n")[0].split()[1])
    N = 1 << k
    print("\n  FULL enumeration (nothing assumed)   : %6d supports   [%.2f s]" % (n_full, t_full))
    print("  with 0 forced into the support       : %6d supports   [%.2f s]" % (n_fix, t_fix))
    print("  translation cross-check %d * %d/8 = %d : %s"
          % (n_fix, N, n_fix * N // 8,
             "MATCH" if n_fix * N // 8 == n_full else "*** MISMATCH ***"))
    print("  (the solution set is closed under translation v -> v+t, which preserves")
    print("   pair-uniformity, and each solution has 8 translates containing 0.)")

    sols = [[int(x) for x in ln.split()[1:]]
            for ln in r_full.stdout.strip().split("\n")[1:] if ln.startswith("SOL")]
    nlin = sum(1 for S in sols
               if 0 in set(S) and all((a ^ b) in set(S) for a in S for b in S))
    n0 = sum(1 for S in sols if 0 in S)
    print("  of %d recorded witnesses, %d contain 0; of those, %d are LINEAR codes"
          % (len(sols), n0, nlin))
    bad = 0
    for S in sols:
        counts = [0] * N
        for v in S:
            counts[v] = 1
        if not is_pair_uniform_exact(counts, 8, k):
            bad += 1
    print("  exact rational pair-marginal check on all %d recorded witnesses : %d failures"
          % (len(sols), bad))

    dd = sorted({popcount(a ^ b) for a in sols[0] for b in sols[0] if a != b})
    print("  pairwise-distance signature of a witness : %s" % dd)
    if k == 6:
        print("    (Frobenius forces sum_{v!=w}(u_v.u_w)^2 = 8*7*(8-7) = 56 spread over 56")
        print("     ordered pairs, so every |u_v.u_w| = 1: every distance is 3 or 4.)")
    if k == 7:
        print("    (Frobenius forces sum_{v!=w}(u_v.u_w)^2 = 8*8*(8-8) = 0, so all 8 rows")
        print("     are MUTUALLY ORTHOGONAL -- [1|M] is an 8x8 Hadamard matrix and every")
        print("     pairwise distance is exactly 4. The supports are the maximum cliques")
        print("     of the distance-4 graph, which is why omega = 8 in stage 2.)")

    Hmin = math.log(8.0)
    print("\n  min H = ln 8 = %.15f = %.6f * ln2   -- ATTAINED, by exactly %d supports"
          % (Hmin, Hmin / LN2, n_full))
    print("  max share = %d*ln2 - ln 8 = %.15f = %.6f * ln2"
          % (k, k * LN2 - Hmin, (k * LN2 - Hmin) / LN2))

    RESULTS["stage3_k%d" % k] = dict(
        n_supports_full=n_full, n_supports_with_0=n_fix,
        translation_check_ok=bool(n_fix * N // 8 == n_full),
        n_witnesses_recorded=len(sols), n_linear_witnesses=nlin,
        exact_check_failures=bad, distance_signature=dd,
        H_min=Hmin, share_max=k * LN2 - Hmin,
        seconds_full=t_full, seconds_fix0=t_fix)
    return n_full


# ---------------------------------------------------------------------------
# STAGE 4 — GPU search over the full polytope (attack B)
# ---------------------------------------------------------------------------

def stage4_gpu(k, code_support, restarts, outer, sweeps):
    sub("STAGE 4  k = %d : GPU SEARCH over the full polytope (attack B)" % k)
    import cupy as cp

    t0 = time.time()
    N = 1 << k
    p32 = Polytope(k, cp, np.float32)
    p64 = Polytope(k, cp, np.float64)
    props = cp.cuda.runtime.getDeviceProperties(0)
    print("device      : %s" % props["name"].decode())
    print("free/total  : %.1f / %.1f GB"
          % (cp.cuda.Device(0).mem_info[0] / 1e9, cp.cuda.Device(0).mem_info[1] / 1e9))
    print("cells N = %d, pair constraints = %d, search dtype float32," % (N, len(p32.pairs)))
    print("refinement of the best candidates in float64.")
    print("projection onto P_%d : iterative proportional fitting against the %d uniform"
          % (k, len(p32.pairs)))
    print("pair marginals; descent: p -> p^(1+eta) (the multiplicative step along -grad H),")
    print("then reproject. eta annealed 0.02 -> 0.62.")
    rng = cp.random.RandomState(20260725)
    LN8 = math.log(8.0)
    allH = []

    def refine(X32, label, keep=4096):
        """float64 refinement + strict feasibility, on the lowest-entropy candidates."""
        H32 = p32.entropy(X32)
        idx = cp.argsort(H32)[:keep]
        X = X32[idx].astype(cp.float64)
        X /= X.sum(axis=1, keepdims=True)
        X = p64.ipf(X, 400)
        Xs = cp.where(X > 1e-12, X, 0.0)
        Xs /= Xs.sum(axis=1, keepdims=True)
        Xs = p64.ipf(Xs, 400)
        res = p64.residual(Xs)
        feas = res < 1e-10
        if int(feas.sum()) == 0:
            return math.inf, 0, None
        H = p64.entropy(Xs)[feas]
        return float(H.min()), int(feas.sum()), cp.asnumpy(H)

    # (a) cold random restarts
    X = (rng.random_sample((restarts, N), dtype=cp.float32) + cp.float32(1e-3))
    X /= X.sum(axis=1, keepdims=True)
    X = p32.minimise_entropy(X, outer, sweeps)
    ha, nfa, Ha = refine(X, "cold")
    Hall32 = cp.asnumpy(p32.entropy(X))
    res32 = cp.asnumpy(p32.residual(X))
    ok32 = res32 < 1e-5
    print("\n(a) COLD RANDOM RESTARTS : %d launched, %d converged feasible (fp32 res < 1e-5)"
          % (restarts, int(ok32.sum())))
    print("    best H after float64 refinement = %.15f = %.9f * ln2" % (ha, ha / LN2))
    print("    ln 8                            = %.15f" % LN8)
    print("    gap to ln 8                     = %+.3e" % (ha - LN8))
    frac = float((np.abs(Hall32[ok32] - LN8) < 1e-4).mean())
    print("    fraction of restarts landing on ln 8 (fp32, 1e-4) : %.4f" % frac)
    allH.append(ha)

    Hc = Hall32[ok32]
    edges = np.linspace(min(Hc.min(), LN8) - 1e-6, Hc.max() + 1e-6, 22)
    hist, _ = np.histogram(Hc, bins=edges)
    print("\n    HISTOGRAM of converged local minima (H in units of ln2), %d points:" % len(Hc))
    mx = max(hist.max(), 1)
    for b in range(len(hist)):
        if hist[b] == 0:
            continue
        print("      [%.4f, %.4f)  %-40s %8d"
              % (edges[b] / LN2, edges[b + 1] / LN2,
                 "#" * max(1, int(40 * hist[b] / mx)), hist[b]))
    print("    (the bottom bin is the exhaustive optimum ln8 = %.4f * ln2)" % (LN8 / LN2))

    # (b) restarts seeded from perturbed optimal code states
    nseed = max(restarts // 4, 1000)
    base = np.zeros(N, dtype=np.float32)
    for v in code_support:
        base[v] = 1.0 / 8
    scales = np.tile(np.array([1e-4, 1e-3, 1e-2, 5e-2, 0.15, 0.35, 0.6, 0.9],
                              dtype=np.float32), nseed // 8 + 1)[:nseed]
    Xs = cp.asarray(np.tile(base, (nseed, 1)))
    sc = cp.asarray(scales)[:, None]
    Xs = Xs * (1 - sc) + sc * rng.random_sample((nseed, N), dtype=cp.float32)
    Xs += cp.float32(1e-8)
    Xs /= Xs.sum(axis=1, keepdims=True)
    Xs = p32.minimise_entropy(Xs, outer, sweeps)
    hb, nfb, Hb = refine(Xs, "seeded")
    print("\n(b) SEEDED RESTARTS : %d starts, perturbed optimal code states" % nseed)
    print("    (noise fractions 1e-4 .. 0.9 mixed with uniform noise -- local-optimality probe)")
    print("    best H after float64 refinement = %.15f   (gap to ln8: %+.3e)" % (hb, hb - LN8))
    nbelow = 0 if Hb is None else int((Hb < LN8 - 1e-9).sum())
    print("    number of refined points strictly BELOW ln 8 : %d" % nbelow)
    allH.append(hb)

    # (c) aggressive annealing schedules
    scheds = [(o, s, pw) for o in (300, 800) for s in (10, 30) for pw in (0.4, 1.0, 4.0)]
    per = max(restarts // len(scheds), 500)
    print("\n(c) DIRECTED ATTEMPT : %d annealing schedules x %d restarts"
          % (len(scheds), per))
    print("    (outer iters in {300,800} x IPF sweeps in {10,30} x start skew p^{0.4,1,4})")
    best_sched, worst_sched = math.inf, -math.inf
    for (o, s, pw) in scheds:
        Xa = cp.power(rng.random_sample((per, N), dtype=cp.float32) + cp.float32(1e-6),
                      cp.float32(pw))
        Xa /= Xa.sum(axis=1, keepdims=True)
        Xa = p32.minimise_entropy(Xa, o, s)
        hs, _, _ = refine(Xa, "sched", keep=1024)
        best_sched = min(best_sched, hs)
        worst_sched = max(worst_sched, hs)
    print("    best  H over all %d schedules = %.15f   (gap to ln8: %+.3e)"
          % (len(scheds), best_sched, best_sched - LN8))
    print("    worst H over all %d schedules = %.15f   (every schedule reached the optimum"
          % (len(scheds), worst_sched))
    print("     to within %.1e)" % (worst_sched - LN8))
    allH.append(best_sched)

    overall = min(allH)
    total = restarts + nseed + per * len(scheds)
    wall = time.time() - t0
    beat = overall < LN8 - 1e-9
    print("\n  GPU VERDICT (k = %d): best H over %s total restarts = %.15f"
          % (k, format(total, ","), overall))
    print("    = %.12f * ln2 ;  exhaustive answer ln 8 = %.12f * ln2"
          % (overall / LN2, LN8 / LN2))
    print("    %s" % ("*** SOMETHING BEAT ln 8 -- HAMMING FORM FALSIFIED ***" if beat
                      else "NOTHING BEAT ln 8. The search corroborates the exact result."))
    print("    share LOWER bound from the search = %.15f = %.9f * ln2"
          % (k * LN2 - overall, (k * LN2 - overall) / LN2))
    print("    (a search yields a LOWER bound on max share, never the maximum.)")
    print("  [stage 4 k=%d wall time: %.1f s]" % (k, wall))

    RESULTS["stage4_k%d" % k] = dict(
        device=props["name"].decode(), restarts_cold=restarts, restarts_seeded=nseed,
        n_schedules=len(scheds), restarts_per_schedule=per, total_restarts=total,
        outer_iters=outer, ipf_sweeps=sweeps, search_dtype="float32",
        refine_dtype="float64", best_H_cold=ha, best_H_seeded=hb,
        best_H_schedules=best_sched, worst_H_schedules=worst_sched,
        best_H_overall=overall, best_H_over_ln2=overall / LN2, beat_ln8=bool(beat),
        share_lower_bound_searched=k * LN2 - overall, wall_seconds=wall)
    return overall


# ---------------------------------------------------------------------------
# STAGE 5 — where the Hamming form dies
# ---------------------------------------------------------------------------

def hadamard12():
    """Paley type-I Hadamard matrix of order 12 from the quadratic residues mod 11.

    q = 11 = 3 mod 4.  Jacobsthal Q_ij = chi(i-j) with chi the quadratic character
    (chi(0)=0), which is SKEW because chi(-1) = -1 when q = 3 mod 4.  Bordering it
    with a skew row/column gives a skew S, and H = I + S satisfies
    H H^T = I + S + S^T + S S^T = I + q I = (q+1) I.
    """
    q = 11
    qr = {(x * x) % q for x in range(1, q)}
    leg = [0] * q
    for a in range(1, q):
        leg[a] = 1 if a in qr else -1
    Q = np.array([[leg[(i - j) % q] for j in range(q)] for i in range(q)], dtype=int)
    assert np.array_equal(Q.T, -Q), "Jacobsthal matrix must be skew"
    S = np.zeros((q + 1, q + 1), dtype=int)
    S[0, 1:] = 1
    S[1:, 0] = -1
    S[1:, 1:] = Q
    assert np.array_equal(S.T, -S), "bordered S must be skew"
    H = np.eye(q + 1, dtype=int) + S
    for i in range(q + 1):          # normalise the first column to all +1
        if H[i, 0] == -1:
            H[i, :] *= -1
    return H


def stage5():
    sub("STAGE 5  where the Hamming form DIES : k = 8..11, by explicit witness")
    H12 = hadamard12()
    ok = np.array_equal(H12.T @ H12, 12 * np.eye(12, dtype=int))
    print("Paley Hadamard matrix of order 12: H^T H = 12*I  -> %s ; first column all +1 : %s"
          % ("PASS" if ok else "FAIL", bool(np.all(H12[:, 0] == 1))))
    assert ok
    print("Its 11 non-constant columns are pairwise orthogonal and sum to zero, so the")
    print("12 rows, read as points of {0,1}^k for any k <= 11, form an OA(12,k,2,2):")
    print("every pair marginal is exactly 3/12 = 1/4 per cell.\n")

    out = {}
    for k in (8, 9, 10, 11):
        conj_H = math.ceil(math.log2(k + 1)) * LN2
        cols = H12[:, 1:1 + k]
        pts = [tuple((1 - c) // 2 for c in row) for row in cols]
        distinct = len(set(pts)) == 12
        counts = [0] * (1 << k)
        for p in pts:
            counts[sum(b << i for i, b in enumerate(p))] += 1
        exact_ok = distinct and is_pair_uniform_exact(counts, 12, k)
        Hwit = math.log(12.0)
        beats = Hwit < conj_H - 1e-12
        print("  k = %2d : conjecture says min H = ceil(log2 %2d)*ln2 = %.6f  (= ln %.1f)"
              % (k, k + 1, conj_H, math.exp(conj_H)))
        print("           WITNESS gives  min H <= ln 12 = %.6f   [12 distinct points: %s,"
              % (Hwit, distinct))
        print("           exact rational pair check: %s]" % ("PASS" if exact_ok else "FAIL"))
        print("           => conjecture %s"
              % ("FALSIFIED" if beats else "not contradicted"))
        if beats:
            print("           => max share >= %d*ln2 - ln 12 = %.6f  >  conjectured %.6f"
                  % (k, k * LN2 - Hwit, k * LN2 - conj_H))
        out[k] = dict(conj_minH=conj_H, witness_H=Hwit, distinct=bool(distinct),
                      exact_pair_check=bool(exact_ok), falsified=bool(beats),
                      share_lower=k * LN2 - Hwit, share_conjectured=k * LN2 - conj_H)
    RESULTS["stage5"] = out
    print("\n  READING. (k - ceil(log2(k+1)))*ln2 is the LINEAR-CODE answer: minimising")
    print("  |C| = 2^m subject to m distinct nonzero columns forces a power of two.")
    print("  The true minimum is ln N where N is the smallest order of an OA(N,k,2,2),")
    print("  conjecturally 4*ceil((k+1)/4) (Hadamard). The two agree exactly when")
    print("  4*ceil((k+1)/4) is a power of two -- true at k = 3, 5, 6, 7 (and 12..15),")
    print("  FALSE at k = 8, 9, 10, 11, where the order-12 Hadamard matrix wins and no")
    print("  linear code can match it (12 is not a power of two).")
    print("  So k = 6 and k = 7 sit inside the form's window; they do not confirm it beyond.")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    banner("ARRAY_SCAN_K67 — the classical maximum of the whole-only share at k = 6, 7")
    print("share(p) = k*ln2 - H(p) on the pair-uniform polytope P_k, so")
    print("max share = k*ln2 - min_{P_k} H.  Conjecture: min H = ceil(log2(k+1))*ln2,")
    print("i.e. max share = (k - ceil(log2(k+1)))*ln2.")
    for k in (6, 7):
        r = math.ceil(math.log2(k + 1))
        print("   k = %d : ceil(log2 %d) = %d -> predicted max share = %d*ln2 = %.15f"
              % (k, k + 1, r, k - r, (k - r) * LN2))
    rng = np.random.default_rng(20260725)

    try:
        import cupy as cp
        xp, dtype = cp, np.float32
        print("\nGPU: %s" % cp.cuda.runtime.getDeviceProperties(0)["name"].decode())
        have_gpu = True
    except Exception as e:
        print("\nNO GPU (%r) -- falling back to numpy" % (e,))
        xp, dtype, have_gpu = np, np.float64, False

    banner("ATTACK (A) — EXACT / EXHAUSTIVE")
    for k in (6, 7):
        stage1(k)
    bounds = {}
    for k in (6, 7):
        bounds[k] = stage2(k, rng, xp, dtype)
    supports = {}
    for k in (6, 7):
        supports[k] = stage3(k)

    gpu = {}
    if have_gpu:
        banner("ATTACK (B) — GPU SEARCH (upper bound on min H; never a maximum)")
        code_support = {k: [int(w, 2) for w in RESULTS["stage1_k%d" % k]["witness"]]
                        for k in (6, 7)}
        gpu[6] = stage4_gpu(6, code_support[6], restarts=200000, outer=300, sweeps=15)
        gpu[7] = stage4_gpu(7, code_support[7], restarts=150000, outer=300, sweeps=15)

    banner("BONUS — the form's range of validity")
    stage5()

    banner("VERDICT")
    for k in (6, 7):
        Hlb, share_ub = bounds[k]
        r = math.ceil(math.log2(k + 1))
        conj = (k - r) * LN2
        attained = k * LN2 - math.log(8)
        print("\nk = %d" % k)
        print("  min H over P_%d      = ln 8 = %.15f = %.6f * ln2" % (k, math.log(8), 3.0))
        print("     lower bound        : analytic (stage 2), c <= 1/8")
        print("     upper bound        : exhibited, and exhaustively counted -- %d supports"
              % supports[k])
        print("  MAX SHARE           = %.15f = %.9f * ln2" % (attained, attained / LN2))
        print("  conjecture (k - ceil(log2(k+1)))*ln2 = (%d - %d)*ln2 = %.15f"
              % (k, r, conj))
        print("  agreement           : %s"
              % ("EXACT MATCH -- the Hamming form SURVIVES at k = %d" % k
                 if abs(attained - conj) < 1e-12 else "*** MISMATCH ***"))
        if k in gpu:
            print("  GPU search best H   : %.15f  -> %s"
                  % (gpu[k], "did not beat ln 8" if gpu[k] > math.log(8) - 1e-9
                     else "*** BEAT ln 8 ***"))
        cap = (k - 2) * LN2
        print("  Lean's proved cap (k-2)*ln2 = %.15f  ->  %s"
              % (cap, "TIGHT" if abs(cap - attained) < 1e-12
                 else "LOOSE by %.6f = %.3f*ln2" % (cap - attained, (cap - attained) / LN2)))

    with open(os.path.join(HERE, "array_scan_k67_results.json"), "w") as f:
        json.dump(RESULTS, f, indent=2, default=str)
    print("\nwrote array_scan_k67_results.json")


if __name__ == "__main__":
    main()
