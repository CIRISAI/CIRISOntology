"""rent_islands.py — does rent/nat SAWTOOTH, with islands of cheapness at the magic sizes?

Pre-registered in scratchpad/RENT_ISLANDS_PREREG.md, committed at 19f80c6 BEFORE this file
existed. Construction facts the prereg quotes are in rent_islands_design_check.py.

SCOPE (prereg §0): designed substrates. A CONTROL, not a discovery about nature. The
"island of stability" name is an ANALOGY — shared abstract structure only ("discrete
existence constraints create non-monotone stability landscapes"), no shared mechanism,
no nuclear physics anywhere.

THE INSTRUMENT (prereg §5). Rent at level s = the CONSTANT q* whose stationary state has
share exactly s. Found by bisection. This is the fixed point the parent's controller was
converging to, defined at the fixed point instead of approached from a transient — which
removes the parent's two flagged artifacts (frac-target overshoot, frac=1.0 boundary) by
construction.

Two exact routes, both population-limit, neither carrying sampling error:
  QUOTIENT — linear substrates. p_inf is constant on cosets of C, so everything is a
             Walsh-Hadamard transform of size 2^(k-m) over the DUAL code. Exact, tiny.
  FULL     — the Paley/Hadamard OA substrates, which have no group structure: the full
             2^k distribution, on the GPU for k >= 18.

Usage:
    python3 rent_islands.py --gate
    python3 rent_islands.py --run
"""
import sys, os, json, time, argparse
from itertools import combinations
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import array_cap_experiment as ACE
import maintenance_sweep as MS
import rent_islands_design_check as DC

LN2 = float(np.log(2))
GPU_FROM_K = 18

try:
    import cupy as cp
    _HAS_GPU = True
except Exception:                                             # pragma: no cover
    cp = None
    _HAS_GPU = False


# =====================================================================================
# primitives
# =====================================================================================

def wht(a, xp=np):
    """wht(p)[T] = sum_v p_v (-1)^{T.v}; involution up to the factor n."""
    a = a.astype(xp.float64, copy=True)
    n, h = a.size, 1
    while h < n:
        a = a.reshape(-1, 2, h)
        x, y = a[:, 0, :].copy(), a[:, 1, :].copy()
        a[:, 0, :] = x + y
        a[:, 1, :] = x - y
        a = a.reshape(n)
        h *= 2
    return a


def popcount_arr(n, xp=np):
    pc = xp.zeros(n, dtype=xp.int8)
    idx = xp.arange(n, dtype=xp.int64)
    b = 0
    while (1 << b) < n:
        pc += ((idx >> b) & 1).astype(xp.int8)
        b += 1
    return pc


def entropy(p, xp=np):
    q = xp.maximum(p, 0.0)
    return float(-xp.sum(xp.where(q > 0, q * xp.log(xp.where(q > 0, q, 1.0)), 0.0)))


def g_vec(q, eps, kmax, xp=np):
    """Stationary Fourier gain per weight: g_w = q / (1 - (1-q) lam^w), g_0 = 1."""
    lam = 1.0 - 2.0 * eps
    w = xp.arange(kmax + 1, dtype=xp.float64)
    g = q / (1.0 - (1.0 - q) * lam ** w)
    g[0] = 1.0
    return g


def f2_rank_nullspace(G):
    """Basis of {T : G T = 0} over F2, for G an (m x k) 0/1 matrix. Returns (k-m) x k."""
    G = np.asarray(G, dtype=np.int8) % 2
    m, k = G.shape
    A = G.copy()
    piv, row = [], 0
    for col in range(k):
        sel = next((r for r in range(row, m) if A[r, col]), None)
        if sel is None:
            continue
        A[[row, sel]] = A[[sel, row]]
        for r in range(m):
            if r != row and A[r, col]:
                A[r] ^= A[row]
        piv.append(col)
        row += 1
        if row == m:
            break
    free = [c for c in range(k) if c not in piv]
    B = []
    for f in free:
        v = np.zeros(k, dtype=np.int8)
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = A[i, f]
        B.append(v)
    B = np.array(B, dtype=np.int8)
    assert B.shape[0] == k - len(piv)
    assert np.all((G @ B.T) % 2 == 0)
    return B


def rows_to_masks(M, k):
    """Each 0/1 row of M as an integer bitmask, slot 0 = most significant (matches
    MS.bits_to_idx)."""
    return np.array([sum(int(M[i, j]) << (k - 1 - j) for j in range(k))
                     for i in range(M.shape[0])], dtype=np.int64)


def xor_span(masks, n_bits):
    """span[u] = XOR of masks[i] over the set bits i of u, for u in [0, 2^n_bits)."""
    span = np.zeros(1 << n_bits, dtype=np.int64)
    for i in range(n_bits):
        half = 1 << i
        span[half:2 * half] = span[:half] ^ int(masks[i])
    return span


_PC16 = np.array([bin(i).count('1') for i in range(1 << 16)], dtype=np.int8)


def popcount64(a):
    a = np.asarray(a, dtype=np.int64)
    return (_PC16[a & 0xFFFF] + _PC16[(a >> 16) & 0xFFFF] +
            _PC16[(a >> 32) & 0xFFFF] + _PC16[(a >> 48) & 0xFFFF]).astype(np.int64)


# =====================================================================================
# substrates
# =====================================================================================

class Lattice:
    """A pair-uniform support S on k slots, with an exact stationary-state solver.

    route == 'quotient' : S is a linear code; work over the dual, size 2^(k-m).
    route == 'full'     : S is a general OA; work with the full 2^k distribution.
    """

    def __init__(self, tag, arm, k, S=None, G=None, name='', force_full=False):
        self.tag, self.arm, self.k, self.name = tag, arm, k, name
        self.xp = np
        self.gpu = False
        if G is not None and not force_full:
            self.route = 'quotient'
            self._init_linear(G)
        else:
            self.route = 'full'
            self._init_full(S)
        self.share_max = self.k * LN2 - np.log(self.ns)
        self.density = self.share_max / self.k

    # ---- linear (quotient) route ----------------------------------------------
    def _init_linear(self, G):
        G = np.asarray(G, dtype=np.int8) % 2
        self.G = G
        self.m = G.shape[0]
        self.S = MS.linear_code(self.k, G)
        self.ns = len(set(map(tuple, self.S.tolist())))
        assert self.ns == 1 << self.m, f"{self.tag}: generator not full rank"
        self.kind = 'linear'
        Hchk = f2_rank_nullspace(G)                       # (k-m) x k, basis of the dual
        self.Hchk = Hchk
        self.r = self.k - self.m
        dual_masks = rows_to_masks(Hchk, self.k)
        self.dual_words = xor_span(dual_masks, self.r)     # every dual codeword
        self.dual_w = popcount64(self.dual_words)          # its Hamming weight
        assert self.dual_w[0] == 0
        # Column syndromes: syndrome of the unit vector e_j.
        # BIT ORDER IS LOAD-BEARING. `dual_words` indexes u by bit i = dual generator i
        # (xor_span uses 1<<i), and wht pairs bit i of u with bit i of the output index.
        # So the syndrome must put parity-check row i at bit i as well; the MSB-first
        # convention used elsewhere in this file silently permutes the syndromes, which
        # leaves the entropies right (they are order-free sums) and cost_flips WRONG.
        # Caught by gate G8. Do not "tidy" this to match rows_to_masks.
        colsyn = np.array([sum(int(Hchk[i, j]) << i for i in range(self.r))
                           for j in range(self.k)], dtype=np.int64)
        self.colsyn = colsyn
        self.leader_w = self._coset_leaders(colsyn)
        A = np.bincount(self.dual_w, minlength=self.k + 1).astype(float)
        self.A = A                                          # A_w for a linear code
        self.d = int(next((w for w in range(1, self.k + 1) if A[w] > 0), -1))
        self.N = 1 << self.k

    def _coset_leaders(self, colsyn):
        """BFS: minimum weight of a vector with each syndrome."""
        n = 1 << self.r
        lead = np.full(n, -1, dtype=np.int16)
        lead[0] = 0
        frontier = np.array([0], dtype=np.int64)
        w = 0
        filled = 1
        while filled < n:
            w += 1
            nxt = (frontier[:, None] ^ colsyn[None, :]).ravel()
            nxt = np.unique(nxt)
            nxt = nxt[lead[nxt] < 0]
            lead[nxt] = w
            filled += len(nxt)
            frontier = nxt
            if len(nxt) == 0:
                raise RuntimeError("coset BFS stalled")
        return lead

    # ---- general OA (full) route ----------------------------------------------
    def _init_full(self, S):
        S = np.asarray(S, dtype=np.int8)
        self.S = S
        self.sidx = MS.bits_to_idx(S)
        uniq = np.unique(self.sidx)
        self.sidx = uniq
        self.ns = len(uniq)
        self.m = None
        self.kind = 'oa'
        self.N = 1 << self.k
        self.gpu = _HAS_GPU and self.k >= GPU_FROM_K
        xp = cp if self.gpu else np
        self.xp = xp
        self.pc = popcount_arr(self.N, xp)
        p0 = xp.zeros(self.N, dtype=xp.float64)
        p0[xp.asarray(self.sidx)] = 1.0 / self.ns
        self.p0 = p0
        self.phat0 = wht(p0, xp)
        Aw = xp.bincount(self.pc.astype(xp.int64), weights=self.phat0 ** 2,
                         minlength=self.k + 1)
        self.A = (cp.asnumpy(Aw) if self.gpu else Aw).astype(float)
        self.d = int(next((w for w in range(1, self.k + 1) if self.A[w] > 1e-12), -1))
        self.mindist = self._mindist()
        self._decw = None
        if self.N <= (1 << 18):
            w = self._hamming_block(0, self.N)
            tie = (w == w.min(axis=1, keepdims=True))
            self._decw = tie / tie.sum(axis=1, keepdims=True)
        self._c_cache = {}
        self._cd = self._build_cd()
        self._kr = self.xp.asarray(self._krawtchouk())
        # Equivariance is DESCRIPTIVE ONLY. The general solver below is exact whether or
        # not it holds, so no number in this file depends on where the line is drawn.
        # Criterion (exact, no noise level, no eps-scan): with
        #   R_i(a) = sum_j Cd[i,j,a] = sum_x W_{x,i} * #{j : |x ^ s_j| = a},
        # dec# of (uniform on S) convolved with ANY radial kernel is uniform on S iff
        # R_i(a) does not depend on i. Measured spread separates the two populations by
        # ~12 orders of magnitude, so the classification is not a threshold judgement.
        R = self._cd.sum(axis=1)
        Rn = cp.asnumpy(R) if self.gpu else np.asarray(R)
        self.profile_dev = float(np.abs(Rn - Rn.mean(axis=0, keepdims=True)).max()
                                 / (self.N / self.ns))
        self.equiv_dev = self._equiv_dev()
        self.equivariant = bool(self.profile_dev < 1e-12)

    def _equiv_dev(self):
        """Max relative deviation of dec#(uniform(S) (x) noise) from uniform on S, over a
        span of noise levels. This is prereg gate G7, kept as a MEASUREMENT: a nonzero
        value means the closed form of the parent's §3.3 does not apply and the general
        solver must be used."""
        xp = self.xp
        worst = 0.0
        for eps in (0.005, 0.01, 0.02, 0.05, 0.10, 0.20):
            ph = wht(self.p0, xp) * (xp.asarray(1 - 2 * eps) ** self.pc.astype(xp.float64))
            pn = wht(ph, xp) / self.N
            onS = self.decode_push(pn)
            onS = cp.asnumpy(onS) if self.gpu else onS
            worst = max(worst, float(np.abs(onS - 1.0 / self.ns).max() * self.ns))
        return worst

    def _hamming_block(self, lo, hi):
        """(hi-lo, ns) Hamming distances to every support point. Uses dist(x,s) =
        popcount(x^s) = pc[x^s], a gather rather than a bit loop."""
        xp = self.xp
        sid = xp.asarray(self.sidx)
        x = xp.arange(lo, hi, dtype=xp.int64)[:, None]
        return self.pc[x ^ sid[None, :]]

    def _mindist(self):
        xp = self.xp
        out = xp.empty(self.N, dtype=xp.int8)
        chunk = 1 << 19
        for lo in range(0, self.N, chunk):
            hi = min(lo + chunk, self.N)
            out[lo:hi] = self._hamming_block(lo, hi).min(axis=1)
        return out

    def decode_push(self, p):
        """Pushforward through the uniform-tie-break nearest-point decoder: the induced
        distribution on the ns support points.

        Cached as a dense (N, |S|) weight matrix where that fits, because gate G5 calls
        this thousands of times to iterate the exact step map; chunked and recomputed
        above that, where only a handful of calls are ever made."""
        xp = self.xp
        if self._decw is not None:
            return p @ self._decw
        onS = xp.zeros(self.ns, dtype=xp.float64)
        chunk = 1 << 19
        for lo in range(0, self.N, chunk):
            hi = min(lo + chunk, self.N)
            w = self._hamming_block(lo, hi)
            tie = (w == w.min(axis=1, keepdims=True))
            wts = tie / tie.sum(axis=1, keepdims=True)
            onS += (p[lo:hi][:, None] * wts).sum(axis=0)
        return onS

    # ---- the stationary state, both routes ------------------------------------
    def stat_share(self, q, eps, want=('share',)):
        """Exact stationary quantities at constant upkeep probability q.
        Returns dict with share, share_pre, and (optionally) flips / neg-mass."""
        if self.route == 'quotient':
            return self._stat_quotient(q, eps, want)
        return self._stat_full(q, eps, want)

    def _stat_quotient(self, q, eps, want):
        lam = 1.0 - 2.0 * eps
        g = g_vec(q, eps, self.k)
        f = g[self.dual_w]
        pq = wht(f) / self.N                                   # per-coset probability
        mult = float(1 << self.m)
        Hp = float(-np.sum(np.where(pq > 0, mult * pq * np.log(np.maximum(pq, 1e-320)),
                                    0.0)))
        f_pre = (lam ** self.dual_w) * g[self.dual_w]
        pq_pre = wht(f_pre) / self.N
        Hpre = float(-np.sum(np.where(pq_pre > 0,
                                      mult * pq_pre * np.log(np.maximum(pq_pre, 1e-320)),
                                      0.0)))
        out = dict(share=self.k * LN2 - Hp, share_pre=self.k * LN2 - Hpre,
                   H=Hp, H_pre=Hpre, H_c=float(np.log(self.ns)),
                   mass=float(mult * pq.sum()), mass_pre=float(mult * pq_pre.sum()),
                   neg=float(min(0.0, pq.min()) * mult),
                   neg_pre=float(min(0.0, pq_pre.min()) * mult),
                   leak=0.0, c_iters=0, c_err=0.0)
        if 'flips' in want:
            out['flips'] = float(q * mult * np.sum(np.maximum(pq_pre, 0.0)
                                                   * self.leader_w))
        return out

    def _build_cd(self):
        """Cd[i, j, a] = total decode-weight onto support point i, summed over the points
        x at Hamming distance a from support point j.

        Why this exists. The stationary c solves c = C(q) c with
            C(q)_{ij} = sum_x W_{x,i} * kappa_q(|x ^ s_j|),
        and kappa_q -- the Fourier multiplier lam^w g_w pulled back to x-space -- depends
        on x ONLY through |x|, because it is a function of Fourier weight alone. So the
        whole q-dependence factors through a (k+1)-vector and Cd is q-INDEPENDENT.
        Build it once (cost N*|S|, since each x carries decode weight on its tie set only)
        and every later q costs an |S|x|S| contraction instead of a 2^k pass.
        """
        xp = self.xp
        ns, k = self.ns, self.k
        Cd = xp.zeros((ns, ns, k + 1), dtype=xp.float64)
        colbase = xp.arange(ns, dtype=xp.int64)[None, :] * (k + 1)
        chunk = 1 << 16
        for lo in range(0, self.N, chunk):
            hi = min(lo + chunk, self.N)
            D = self._hamming_block(lo, hi)
            tie = (D == D.min(axis=1, keepdims=True))
            W = tie / tie.sum(axis=1, keepdims=True)
            Di = D.astype(xp.int64)
            for i in range(ns):
                wi = W[:, i]
                nz = wi > 0
                if not bool(nz.any()):
                    continue
                idx = (colbase + Di[nz])
                wts = xp.broadcast_to(wi[nz][:, None], idx.shape)
                Cd[i] += xp.bincount(idx.ravel(), weights=wts.ravel(),
                                     minlength=ns * (k + 1)).reshape(ns, k + 1)
        return Cd

    def _krawtchouk(self):
        """Kr[w, a] = sum_{|T| = w} (-1)^{T.x} for any x of weight a."""
        from math import comb
        k = self.k
        Kr = np.zeros((k + 1, k + 1))
        for w in range(k + 1):
            for a in range(k + 1):
                Kr[w, a] = sum((-1) ** i * comb(a, i) * comb(k - a, w - i)
                               for i in range(0, min(a, w) + 1) if w - i <= k - a)
        return Kr

    def solve_c_exact(self, q, eps):
        """c as the exact Perron vector of the |S| x |S| operator. No iteration."""
        xp = self.xp
        if self._cd is None:
            self._cd = self._build_cd()
            self._kr = xp.asarray(self._krawtchouk())
        lam = 1.0 - 2.0 * eps
        g = g_vec(q, eps, self.k, xp)
        mult = (xp.asarray(lam) ** xp.arange(self.k + 1, dtype=xp.float64)) * g
        kappa = (mult[:, None] * self._kr).sum(axis=0) / self.N          # kappa[a]
        C = (self._cd * kappa[None, None, :]).sum(axis=2)                # (i, j)
        Cn = cp.asnumpy(C) if self.gpu else np.asarray(C)
        A = Cn - np.eye(self.ns)
        A[-1, :] = 1.0
        b = np.zeros(self.ns)
        b[-1] = 1.0
        c = np.linalg.solve(A, b)
        colsum = float(np.abs(Cn.sum(axis=0) - 1.0).max())
        return xp.asarray(c), colsum

    def _solve_c(self, q, eps, tol=1e-14, itmax=400):
        """The distribution `c` that upkeep actually deposits on S at stationarity.

        The step map is LINEAR and the decoder has rank |S|, so the whole fixed-point
        problem collapses to |S| unknowns. Writing E for the embedding of R^|S| into
        R^{2^k} and onS for the decode pushforward,

            p_inf = (1-q)*noise(p_inf) + q*E c      =>   p_inf^(T) = g_{|T|} (Ec)^(T)
            c     = onS(noise(p_inf))               =>   c = C(q) c,  C(q) column-stochastic

        so c is the Perron vector of an |S| x |S| matrix. Solved by warm-started power
        iteration, which is exact in one step when the decoder is equivariant (c stays
        uniform) and converges geometrically otherwise. NO equivariance is assumed.
        """
        xp = self.xp
        lam = 1.0 - 2.0 * eps
        g = g_vec(q, eps, self.k, xp)
        gp = g[self.pc.astype(xp.int64)]
        kern = (xp.asarray(lam) ** self.pc.astype(xp.float64)) * gp        # noise o resolvent
        key = round(eps, 12)
        c = self._c_cache.get(key)
        if c is None:
            c = xp.full(self.ns, 1.0 / self.ns, dtype=xp.float64)
        sid = xp.asarray(self.sidx)
        it, err = 0, 0.0
        for it in range(1, itmax + 1):
            v = xp.zeros(self.N, dtype=xp.float64)
            v[sid] = c
            u = wht(kern * wht(v, xp), xp) / self.N
            cn = self.decode_push(u)
            cn = cn / cn.sum()
            err = float(xp.abs(cn - c).max())
            c = cn
            if err < tol:
                break
        self._c_cache[key] = c
        return c, gp, kern, it, err

    def _stat_full(self, q, eps, want):
        # No equivariance branch: the |S|x|S| Perron solve is exact either way, and it
        # returns the uniform c of its own accord wherever equivariance does hold.
        xp = self.xp
        g = g_vec(q, eps, self.k, xp)
        gp = g[self.pc.astype(xp.int64)]
        kern = ((xp.asarray(1.0 - 2.0 * eps) ** self.pc.astype(xp.float64)) * gp)
        c, colsum = self.solve_c_exact(q, eps)
        it, err = 0, colsum
        v = xp.zeros(self.N, dtype=xp.float64)
        v[xp.asarray(self.sidx)] = c
        chat = wht(v, xp)
        p = wht(gp * chat, xp) / self.N
        p_pre = wht(kern * chat, xp) / self.N
        Hp, Hpre = entropy(p, xp), entropy(p_pre, xp)
        cc = cp.asnumpy(c) if self.gpu else np.asarray(c)
        Hc = float(-np.sum(np.where(cc > 0, cc * np.log(np.maximum(cc, 1e-320)), 0.0)))
        # PAIR-UNIFORMITY IS NOT FREE HERE. share = sSup(pair envelope) - H(p) equals
        # k*ln2 - H(p) only when p is exactly pair-uniform, which holds iff c is uniform.
        # On a LOSSY substrate c is not uniform, weight-1 and weight-2 Fourier mass leaks
        # in, and k*ln2 - H(p) OVER-READS the share (it reported ceilings above share_max
        # before this was put in). The pairwise-maxent top of the envelope is
        #     H_maxent = k*ln2 - (1/2) * sum_{1<=|T|<=2} phat(T)^2 + O(leak^2),
        # so the corrected share is the raw reading minus half the leak. The residual is
        # O(leak^2), reported per row so the remaining error is bounded and visible.
        low = (self.pc <= 2) & (self.pc >= 1)
        phat_inf = gp * chat
        leak = float(xp.sum(xp.where(low, phat_inf ** 2, 0.0)))
        leak_pre = float(xp.sum(xp.where(low, (kern * chat) ** 2, 0.0)))
        out = dict(share=self.k * LN2 - Hp - 0.5 * leak,
                   share_pre=self.k * LN2 - Hpre - 0.5 * leak_pre,
                   share_raw=self.k * LN2 - Hp,
                   H=Hp, H_pre=Hpre, H_c=Hc,
                   mass=float(p.sum()), mass_pre=float(p_pre.sum()),
                   neg=float(min(0.0, float(p.min()))),
                   neg_pre=float(min(0.0, float(p_pre.min()))),
                   leak=leak, leak_pre=leak_pre, c_iters=it, c_err=err)
        if 'flips' in want:
            out['flips'] = float(q * float(xp.sum(xp.maximum(p_pre, 0.0)
                                                  * self.mindist.astype(xp.float64))))
        if 'state' in want:
            out['p'] = p
            out['p_pre'] = p_pre
            out['c'] = c
        return out

    # ---- the exact step map, for the verification gate -------------------------
    def step_full(self, p, eps, q):
        xp = self.xp
        lam = 1.0 - 2.0 * eps
        ph = wht(p, xp)
        ph *= xp.asarray(lam) ** self.pc.astype(xp.float64)
        p_pre = wht(ph, xp) / self.N
        if q <= 0:
            return p_pre
        onS = self.decode_push(p_pre)
        full = xp.zeros(self.N, dtype=xp.float64)
        full[xp.asarray(self.sidx)] = onS
        return (1.0 - q) * p_pre + q * full

    def pair_dev(self):
        """max |pair marginal - 1/4| on the design state, by direct counting on S."""
        S = np.asarray(self.S, dtype=np.int8)
        Su = np.unique(S, axis=0)
        n = len(Su)
        worst = 0.0
        for i, j in combinations(range(self.k), 2):
            c = np.bincount(Su[:, i].astype(int) * 2 + Su[:, j].astype(int), minlength=4)
            worst = max(worst, float(np.abs(c / n - 0.25).max()))
        return worst


# =====================================================================================
# roster
# =====================================================================================

def has_zero_triple(cols):
    """d == 3 for distinct nonzero columns iff some three of them XOR to zero."""
    c = list(cols)
    s = set(c)
    for i in range(len(c)):
        for j in range(i + 1, len(c)):
            if (c[i] ^ c[j]) in s:
                return True
    return False


def armB_prime_columns(k, m, rng):
    """The d = 3 constrained comparator, run only at the two k where ARM B's
    maximise-dual-distance rule returns d = 4 (prereg §2, P-DISSOCIATION confound).

    Rules, fixed here and disclosed in the results:
      k = 8  — exhaustive over all C(15,8) = 6435 column sets, keep d = 3, maximise
               the code's minimum distance (the same secondary criterion as ARM B).
      k = 16 — MINIMAL PERTURBATION of ARM B: replace exactly one column of ARM B's
               own column set by each unused nonzero vector of F_2^5, keep those that
               give d = 3, maximise minimum distance. A one-column edit isolates d
               from every other difference, which is what a d-matched control is for.
    """
    pool = list(range(1, 1 << m))
    best = None
    from math import comb
    if comb(len(pool), k) <= 20000:
        cands = [list(c) for c in combinations(pool, k)]
        how = f'exhaustive C({len(pool)},{k}) = {len(cands)}, d=3 kept, max d_min'
    else:
        _, base, _ = DC.armB_columns(k)
        base = list(base)
        unused = [c for c in pool if c not in base]
        cands = []
        for i in range(k):
            for u in unused:
                cands.append(sorted(base[:i] + base[i + 1:] + [u]))
        how = (f'minimal perturbation of ARM B: one-column edits ({len(cands)} of them), '
               f'd=3 kept, max d_min')
    for cols in cands:
        if len(set(cols)) != k or not has_zero_triple(cols):
            continue
        W = MS.linear_code(k, MS.cols_to_G(m, cols))
        dmin = DC.code_min_distance(W)
        if best is None or dmin > best[0]:
            best = (dmin, list(cols))
    assert best is not None, f"no d=3 comparator found at k={k}, m={m}"
    return best[1], how, best[0]


def build_roster(kmax=24):
    """Every substrate named in prereg §3. Nothing is selected after seeing a result."""
    rng = np.random.default_rng(20260725)
    R = {}
    for k in range(5, kmax + 1):
        S = DC.maxshare_oa(k)
        n0 = DC.N0(k)
        if (n0 & (n0 - 1)) == 0:
            # Sylvester order: the OA is the simplex code, punctured -- use the exact
            # quotient route via its generator (rows of the OA span the code).
            G = simplex_generator(k, int(np.log2(n0)))
            R[f'A{k}'] = Lattice(f'A{k}', 'A', k, G=G,
                                 name=f'OA({n0},{k},2,2) [{DC.had_source(n0)}]')
        else:
            R[f'A{k}'] = Lattice(f'A{k}', 'A', k, S=S,
                                 name=f'OA({n0},{k},2,2) [{DC.had_source(n0)}]')
    for k in range(5, kmax + 1):
        m, cols, how = DC.armB_columns(k)
        R[f'B{k}'] = Lattice(f'B{k}', 'B', k, G=MS.cols_to_G(m, cols),
                             name=f'linear [{k},{m}] ({how})')
        R[f'B{k}'].cols = list(map(int, cols))
        R[f'B{k}'].search = how
    for k, m in ((8, 4), (16, 5)):
        cols, how, dmin = armB_prime_columns(k, m, rng)
        R[f'P{k}'] = Lattice(f'P{k}', "B'", k, G=MS.cols_to_G(m, cols),
                             name=f"d=3 comparator [{k},{m}] ({how})")
        R[f'P{k}'].cols = list(map(int, cols))
        R[f'P{k}'].search = how
    for k in (7, 15):
        r = int(np.log2(k + 1))
        Hchk = np.array([[(c >> b) & 1 for c in range(1, 1 << r)] for b in range(r)],
                        dtype=np.int8)
        G = f2_rank_nullspace(Hchk)
        R[f'C{k}'] = Lattice(f'C{k}', 'C', k, G=G, name=f'perfect Hamming [{k},{k-r}]')
    R['C23'] = Lattice('C23', 'C', 23, G=DC.golay23(), name='perfect Golay [23,12,7]')
    return R


def simplex_generator(k, m):
    """Generator of the punctured simplex code whose codewords are the FIRST k columns
    of the normalised Sylvester OA of order 2^m. Verified against DC.maxshare_oa."""
    S = DC.maxshare_oa(k)                    # the 2^m OA rows, truncated to k columns
    rows = [r for r in S]
    G, seen = [], {tuple(np.zeros(k, dtype=np.int8))}
    for r in rows:
        t = tuple(int(x) for x in r)
        if t in seen:
            continue
        G.append(np.array(r, dtype=np.int8))
        span = {tuple(np.zeros(k, dtype=np.int8))}
        for gg in G:
            span |= {tuple(np.array(s, dtype=np.int8) ^ gg) for s in span}
        seen = span
        if len(seen) == 1 << m:
            break
    G = np.array(G, dtype=np.int8)
    W = MS.linear_code(k, G)
    assert set(map(tuple, W.tolist())) == set(map(tuple, S.tolist())), \
        f"simplex generator mismatch at k={k}"
    return G


# =====================================================================================
# the rent measurement
# =====================================================================================

def solve_q(lat, eps, target, itmax=200):
    """The constant q whose stationary share is exactly `target`. Bisection; share_inf
    is verified increasing in q by gate G6, so the root is unique.

    NOTE the ceiling is share_inf(q=1), NOT share_max: on a substrate whose decoder is
    not equivariant, full upkeep does not restore the design state (the parent's
    pre-registered failure mode RC-A), so the attainable ceiling is strictly lower."""
    lo, hi = 0.0, 1.0
    s_hi = lat.stat_share(1.0, eps)['share']
    if target > s_hi:
        return None, dict(reason=f'target {target:.6f} above attainable ceiling '
                                 f'{s_hi:.6f} (share_max {lat.share_max:.6f})')
    for _ in range(itmax):
        mid = 0.5 * (lo + hi)
        s = lat.stat_share(mid, eps)['share']
        if s < target:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-15:
            break
    q = 0.5 * (lo + hi)
    r = lat.stat_share(q, eps, want=('flips',))
    r['ceiling'] = s_hi
    return q, r


def measure_rent(lat, eps, target, mode, target_label):
    """One pre-registered row, with every hygiene number attached (prereg §5)."""
    q, r = solve_q(lat, eps, target)
    row = dict(tag=lat.tag, arm=lat.arm, k=lat.k, ns=lat.ns, m=lat.m, d=lat.d,
               kind=lat.kind, route=lat.route, name=lat.name,
               equivariant=bool(getattr(lat, 'equivariant', True)),
               equiv_dev=float(getattr(lat, "equiv_dev", 0.0)),
               profile_dev=float(getattr(lat, "profile_dev", 0.0)),
               share_max=lat.share_max, density=lat.density,
               eps=eps, mode=mode, target_label=target_label, target=float(target))
    if q is None:
        row.update(dropped=True, drop_reason=r['reason'])
        return row
    achieved = r['share']
    resid = abs(achieved - target) / max(target, 1e-30)
    # General cost identity: the entropy upkeep erases is q * (H(pre) - H(what upkeep
    # deposits on S)). H(deposit) = ln|S| ONLY when the decoder is equivariant, so the
    # general form is used everywhere and the two agree wherever equivariance holds.
    cost_erase = q * (r['H_pre'] - r['H_c'])
    row.update(
        q_star=float(q),
        achieved=float(achieved), achieved_frac=float(achieved / lat.share_max),
        ceiling=float(r.get('ceiling', lat.share_max)),
        ceiling_frac=float(r.get('ceiling', lat.share_max) / lat.share_max),
        target_resid_rel=float(resid),
        share_pre=float(r['share_pre']),
        cost_erase=float(cost_erase),
        cost_flips=float(r.get('flips', np.nan)),
        rent_per_nat=float(cost_erase / achieved),
        flips_per_nat=float(r.get('flips', np.nan) / achieved),
        mass_dev=float(abs(r['mass'] - 1.0)),
        neg_mass=float(r['neg']),
        pair_leak=float(r.get('leak', 0.0)),
        # How far the upkeep deposit falls short of uniform-on-S. Zero iff equivariant;
        # nonzero means upkeep itself is a second, independent cost channel, and the
        # confound audit in the analysis compares it against the tooth being claimed.
        Hc_deficit=float(np.log(lat.ns) - r['H_c']),
        share_raw=float(r.get('share_raw', achieved)),
        leak_correction_rel=float(0.5 * r.get('leak', 0.0) / achieved),
        leak_residual_rel=float(r.get('leak', 0.0) ** 2 / achieved),
        c_iters=int(r.get('c_iters', 0)), c_err=float(r.get('c_err', 0.0)),
        dropped=False, drop_reason='')
    if resid > 1e-6:
        row.update(dropped=True, drop_reason=f'target residual {resid:.2e} > 1e-6')
    if not (1e-9 < q < 1 - 1e-9):
        row.update(dropped=True, drop_reason=f'q* saturated at {q:.3e}')
    return row


# =====================================================================================
# GATES
# =====================================================================================

def gates(R):
    print("=" * 84)
    print("GATES — all must PASS before any measurement is read (prereg §6)")
    print("=" * 84)
    res, ok = {}, True

    print("\n--- G1: shared share machinery (array_cap_experiment.gate) ---")
    g1 = bool(ACE.gate())
    res['G1'] = g1; ok &= g1

    print("\n--- G2: every substrate exactly pair-uniform; share_max = k ln2 - ln|S| ---")
    g2 = True
    for tag in sorted(R, key=lambda t: (R[t].arm, R[t].k)):
        L = R[tag]
        pd = L.pair_dev()
        A12 = float(L.A[1] + L.A[2])
        sm_ok = abs(L.share_max - (L.k * LN2 - np.log(L.ns))) < 1e-12
        ipf = ''
        if L.k <= 11:
            p0 = np.zeros(1 << L.k)
            p0[np.unique(MS.bits_to_idx(np.unique(L.S, axis=0)))] = 1.0 / L.ns
            si = ACE.shareK(p0.reshape((2,) * L.k))[0]
            good_ipf = abs(si - L.share_max) < 1e-9
            ipf = f" ipf={si:.9f} {'OK' if good_ipf else 'FAIL'}"
            g2 &= good_ipf
        good = (pd < 1e-12) and (A12 < 1e-12) and sm_ok
        g2 &= good
        print(f"  {tag:5s} k={L.k:2d} |S|={L.ns:5d} d={L.d:2d} {L.route:8s} "
              f"pairdev={pd:.1e} A1+A2={A12:.1e} share_max={L.share_max:.9f}"
              f"{ipf} {'OK' if good else 'FAIL'}")
    res['G2'] = bool(g2); ok &= g2

    print("\n--- G3: Hadamard orders verified; strength 2 by direct counting (no Fourier) ---")
    g3 = True
    for N in (8, 12, 16, 20, 24, 28):
        H = DC.hadamard(N)
        v = bool(np.array_equal(H @ H.T, N * np.eye(N, dtype=int)))
        g3 &= v
        print(f"  H{N:3d} {DC.had_source(N):16s} H H^T = {N} I : {v}")
    for k in (11, 19, 23, 24):
        S = np.unique(DC.maxshare_oa(k), axis=0)
        cnt_ok = all(np.all(np.bincount(S[:, i].astype(int) * 2 + S[:, j].astype(int),
                                        minlength=4) == len(S) // 4)
                     for i, j in combinations(range(k), 2))
        g3 &= cnt_ok
        print(f"  OA k={k:2d}: {len(S)} distinct rows, every column pair shows each symbol "
              f"pair exactly {len(S)//4}x: {cnt_ok}")
    res['G3'] = bool(g3); ok &= g3

    print("\n--- G4: Fourier noise propagator == brute-force convolution ---")
    g4 = True
    for tag in ('A8', 'A11'):
        L = R[tag]
        for eps in (0.01, 0.05):
            xp = L.xp
            p = np.asarray(cp.asnumpy(L.p0) if L.gpu else L.p0)
            pc = np.asarray(cp.asnumpy(L.pc) if L.gpu else L.pc)
            ker = np.array([eps ** pc[m_] * (1 - eps) ** (L.k - pc[m_])
                            for m_ in range(L.N)])
            bf = np.zeros(L.N)
            allx = np.arange(L.N)
            for m_ in range(L.N):
                bf += ker[m_] * p[allx ^ m_]
            ph = wht(p) * (1 - 2 * eps) ** pc
            fast = wht(ph) / L.N
            e = float(np.abs(bf - fast).max())
            g4 &= e < 1e-12
            print(f"  {tag} eps={eps}: max|brute - fourier| = {e:.3e}")
    res['G4'] = bool(g4); ok &= g4

    print("\n--- G5: the solved stationary state IS the fixed point of the exact step ---")
    print("        (iterate the exact map FROM it; a true fixed point does not move.")
    print("         Plus a from-p0 convergence run.)")
    g5 = True
    for tag in sorted(R, key=lambda t: (R[t].arm, R[t].k)):
        L = R[tag]
        if L.route != 'full':
            continue                       # linear: C-equivariance is algebraic; G8 checks
        nst = 30 if L.k <= 20 else 12
        # NOTE the comparison is in the RAW convention (k ln2 - H) plus a convention-free
        # STATE drift. `share` itself is leak-corrected, and comparing a corrected number
        # against a raw one manufactures a fake failure of exactly half the leak.
        worst_s, worst_p = 0.0, 0.0
        for (eps, q) in ((0.01, 0.05), (0.05, 0.30)):
            r0 = L.stat_share(q, eps, want=('flips', 'state'))
            p = r0['p'].copy()
            s0 = r0['share_raw']
            for _ in range(nst):
                p = L.step_full(p, eps, q)
            s1 = L.k * LN2 - entropy(p, L.xp)
            worst_s = max(worst_s, abs(s1 - s0))
            # RELATIVE state drift. The absolute-times-N form is scale-blind: float64
            # WHT rounding alone grows with N and manufactured failures at k = 21..23.
            worst_p = max(worst_p, float(L.xp.abs(p - r0['p']).max()
                                         / L.xp.abs(r0['p']).max()))
        good = worst_s < 1e-10 and worst_p < 1e-9
        g5 &= good
        print(f"  {tag:5s} k={L.k:2d} |S|={L.ns:3d} equivariant={str(L.equivariant):5s} "
              f"drift over {nst} exact steps: share {worst_s:.3e}  state (relative) "
              f"{worst_p:.3e} {'OK' if good else 'FAIL'}")
    # From p0, the trajectory must CONVERGE to the solved fixed point. On a lossy
    # substrate the step map's slowest mode is much closer to 1 than the equivariant
    # (1-q)*lam^d, so this is a convergence demonstration at checkpoints, not a
    # single-shot tolerance: the gap must fall monotonically and end below 1e-10.
    for tag in ('A8', 'A11', 'A16'):
        L = R[tag]
        eps, q = 0.02, 0.1
        s_cf = L.stat_share(q, eps)['share_raw']
        p = L.p0.copy()
        cps, gaps, t = [200, 600, 1800, 3600], [], 0
        for cp_t in cps:
            while t < cp_t:
                p = L.step_full(p, eps, q)
                t += 1
            gaps.append(abs((L.k * LN2 - entropy(p, L.xp)) - s_cf))
        # "Falling" must tolerate having ALREADY arrived: once the gap reaches the
        # float64 floor (~1e-13) it stops falling and jitters, which is convergence, not
        # failure. So: non-increasing except where both ends are already at the floor.
        mono = all(gaps[i + 1] <= gaps[i] or gaps[i + 1] < 1e-12
                   for i in range(len(gaps) - 1))
        good = mono and gaps[-1] < 1e-10
        g5 &= good
        print(f"  {tag:5s} from p0, gap to the solved fixed point at t = {cps}: "
              f"{['%.2e' % v for v in gaps]}  converging: {mono} "
              f"{'OK' if good else 'FAIL'}")
    print("        (this leg shows the solved fixed point is ATTRACTING; that it IS the")
    print("         fixed point is the zero-drift leg above, which holds at 1e-15.)")
    print("  cross-check: the exact |S|x|S| Perron solve vs warm-started power iteration")
    for tag in ('A8', 'A16', 'A20'):
        L = R[tag]
        ce, colsum = L.solve_c_exact(0.3, 0.05)
        ci, _g, _k, nit, _e = L._solve_c(0.3, 0.05)
        e = float(L.xp.abs(ce - ci).max())
        g5 &= e < 1e-11
        print(f"  {tag:5s} max |c_exact - c_iterated| = {e:.3e} (iteration took {nit} "
              f"steps); operator column sums off 1 by {colsum:.2e}")
    res['G5'] = bool(g5); ok &= g5

    print("\n--- G6: share_inf(q) strictly increasing; 0 at q->0; ceiling at q=1 ---")
    print("        (the ceiling is share_inf(1), which EQUALS share_max only where the")
    print("         decoder is equivariant — see G7.)")
    g6 = True
    for tag in ('A7', 'A12', 'A16', 'A23', 'A24', 'B20', 'C15'):
        L = R[tag]
        qs = np.concatenate([[1e-9], np.logspace(-6, 0, 60)])
        sv = np.array([L.stat_share(float(q), 0.05)['share'] for q in qs])
        mono = bool(np.all(np.diff(sv) > -1e-12))
        ends = (sv[0] < 1e-6 * L.share_max) and (sv[-1] <= L.share_max + 1e-10)
        g6 &= mono and ends
        print(f"  {tag:5s} monotone: {mono}   share(1e-9) = {sv[0]:.3e}   "
              f"share(1) = {sv[-1]:.9f} = {sv[-1]/L.share_max:.9f} x share_max")
    res['G6'] = bool(g6); ok &= g6

    print("\n--- G7: is dec#(uniform(S) (x) noise) uniform on S? ---")
    print("        PRE-REGISTERED AS A MEASUREMENT WITH BOTH OUTCOMES MEANINGFUL")
    print("        (prereg §6). Non-uniform => that substrate's upkeep is LOSSY: full")
    print("        upkeep does not restore the design state. Those rows are then solved")
    print("        without the equivariance assumption, and flagged.")
    equiv = {}
    for tag in sorted(R, key=lambda t: (R[t].arm, R[t].k)):
        L = R[tag]
        if L.route != 'full':
            continue
        equiv[tag] = dict(profile_dev=L.profile_dev, eps_scan_dev=L.equiv_dev)
        ceil1 = L.stat_share(1.0, 0.05)['share'] / L.share_max
        print(f"  {tag:5s} k={L.k:2d} |S|={L.ns:3d} profile spread = {L.profile_dev:.3e} "
              f"(eps-scan {L.equiv_dev:.3e})  "
              f"{'EQUIVARIANT' if L.equivariant else 'LOSSY      '}  "
              f"attainable ceiling at q=1, eps=.05: {ceil1:.9f} x share_max")
    for tag in ('B24', 'C23'):
        L = R[tag]
        print(f"  {tag:5s} linear: C-equivariance is algebraic (parent §3.4); coset-leader "
              f"table complete, max leader weight {int(L.leader_w.max())}")
    res['G7'] = 'measured'
    res['equivariance_dev'] = equiv

    print("\n--- G8: quotient route == full route, on the same linear substrate ---")
    g8 = True
    for tag in ('A7', 'A15', 'B11', 'C15'):
        L = R[tag]
        F = Lattice(tag + '_full', L.arm, L.k, S=np.unique(L.S, axis=0),
                    name=L.name, force_full=True)
        for (eps, q) in ((0.01, 0.02), (0.05, 0.30)):
            a = L.stat_share(q, eps, want=('flips',))
            b = F.stat_share(q, eps, want=('flips',))
            e = max(abs(a['share'] - b['share']), abs(a['share_pre'] - b['share_pre']),
                    abs(a['flips'] - b['flips']))
            g8 &= e < 1e-10
            print(f"  {tag:5s} eps={eps} q={q}: max |quotient - full| over "
                  f"(share, share_pre, flips) = {e:.3e}")
    res['G8'] = bool(g8); ok &= g8

    print("\n" + "=" * 84)
    print(f"GATES: {'ALL PASS' if ok else 'FAILURE — run stops'}")
    for kk in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'):
        print(f"  {kk}: {res[kk]}")
    lossy = [t for t in sorted(equiv, key=lambda t: R[t].k) if not R[t].equivariant]
    print(f"  G7 result: LOSSY substrates = {lossy}")
    print(f"             equivariant      = "
          f"{[t for t in sorted(equiv, key=lambda t: R[t].k) if R[t].equivariant]}")
    print("=" * 84)
    return ok, res


# =====================================================================================
# the sweep
# =====================================================================================

EPS = [0.01, 0.05]
FRACS = [0.1, 0.5]
ABS_LEVELS = [1.0]


def sweep(R):
    print("\n" + "=" * 84)
    print("MEASUREMENT — rent at the fixed point, all arms, all conditions")
    print("=" * 84)
    rows = []
    t0 = time.time()
    for tag in sorted(R, key=lambda t: (R[t].arm, R[t].k)):
        L = R[tag]
        for eps in EPS:
            for fr in FRACS:
                rows.append(measure_rent(L, eps, fr * L.share_max, 'frac', f'{fr}'))
            for s in ABS_LEVELS:
                if s < 0.98 * L.share_max:
                    rows.append(measure_rent(L, eps, s, 'abs', f'{s}nat'))
        print(f"  {tag:5s} k={L.k:2d} {L.route:8s} done ({time.time()-t0:.1f}s)")
    return rows


def compare_instruments(R):
    """The parent's controller, re-run UNCHANGED on two substrates, so the change of
    instrument is documented as a number rather than asserted (prereg §5)."""
    print("\n" + "=" * 84)
    print("INSTRUMENT COMPARISON — parent controller vs fixed-point definition")
    print("=" * 84)
    out = []
    old = json.load(open('/home/emoore/CIRISOntology/scratchpad/'
                         'maintenance_sweep_results.json'))['rent']
    for tag_old, tag_new in (('H11', 'A11'), ('L12', 'A12'), ('L11', 'B11'),
                             ('H8', 'A8'), ('E8', 'B8')):
        L = R[tag_new]
        for eps in (0.01, 0.05):
            for fr in (0.1, 0.5):
                o = old.get(f'{tag_old}|{eps}|{fr}')
                if o is None:
                    continue
                n = measure_rent(L, eps, fr * L.share_max, 'frac', f'{fr}')
                out.append(dict(old_tag=tag_old, new_tag=tag_new, eps=eps, frac=fr,
                                old_achieved=o['share_held'] / o['share_max'],
                                old_rent_per_nat=o['cost_erase'] / o['share_held'],
                                old_q=o['q_star'],
                                new_achieved=n['achieved_frac'],
                                new_rent_per_nat=n['rent_per_nat'], new_q=n['q_star']))
                r = out[-1]
                print(f"  {tag_old:4s}->{tag_new:4s} eps={eps} frac={fr}: "
                      f"achieved {r['old_achieved']:.4f} -> {r['new_achieved']:.6f} | "
                      f"rent/nat {r['old_rent_per_nat']:.5f} -> "
                      f"{r['new_rent_per_nat']:.5f} | q* {r['old_q']:.5f} -> "
                      f"{r['new_q']:.5f}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--kmax', type=int, default=24)
    ap.add_argument('--out', default='/home/emoore/CIRISOntology/scratchpad/'
                                     'rent_islands_results.json')
    a = ap.parse_args()

    print(f"GPU: {'cupy available' if _HAS_GPU else 'CPU only'} "
          f"(full route on GPU from k >= {GPU_FROM_K})")
    print(f"prereg 19f80c6 | building the roster to k = {a.kmax} ...")
    t0 = time.time()
    R = build_roster(a.kmax)
    print(f"roster: {len(R)} substrates, built in {time.time()-t0:.1f}s")

    ok, gres = gates(R)
    if not ok:
        print("GATE FAILURE — stopping, per prereg §6.")
        sys.exit(1)
    if a.gate:
        return

    rows = sweep(R)
    cmp_rows = compare_instruments(R)
    res = dict(
        prereg='19f80c6', gates=gres,
        roster={t: dict(tag=t, arm=R[t].arm, k=R[t].k, ns=R[t].ns, m=R[t].m, d=R[t].d,
                        kind=R[t].kind, route=R[t].route, name=R[t].name,
                        share_max=R[t].share_max, density=R[t].density,
                        A=[float(x) for x in R[t].A],
                        cols=getattr(R[t], 'cols', None),
                        search=getattr(R[t], 'search', None))
                for t in R},
        rows=rows, instrument_comparison=cmp_rows,
        conditions=dict(eps=EPS, fracs=FRACS, abs_levels=ABS_LEVELS))
    with open(a.out, 'w') as f:
        json.dump(res, f, indent=1)
    print(f"\nwrote {a.out}  ({len(rows)} rows)")


if __name__ == '__main__':
    main()
